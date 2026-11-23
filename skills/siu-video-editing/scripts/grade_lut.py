# Even, bright, natural colour across phone clips: one 3D LUT SOLVED PER CLIP on sample frames, then a graded CFR proxy.
# History: v3 copied the official channel's flat numbers (saturation -23 %, blacks lifted) onto phone footage and the client
# wrote "màu bợt, nhợt nhạt, thiếu sức sống", uneven between sources. This solver (Mỹ Tho v4, accepted) does, per clip:
#   levels   0.5 / 99.5 % luma -> 0.015 / 0.975 (dehaze; stretch capped at 1.3x, never compresses)
#   gamma    toward a shared mean luma (keeps 35 % of the clip's own deviation so a bright scene stays brighter)
#   S-curve  gentle (clarity, "độ trong")
#   vibrance toward a shared saturation; dull colours get more than vivid ones; skin tones get 40 % of the boost
#   python grade_lut.py <clips or folder> --out DIR [--target-y 0.475] [--target-s 19 | --keep-sat] [--audio keep|clean|none]
#                       [--sheet compare.jpg]
# --keep-sat: keep each clip's saturation (already vivid scenes: red tablecloth + blue curtain in the tiếng Nga reel).
# --audio clean: voice chain for PA / reverb speech (HP 100, -3 dB @250, +4 dB @3k, light compression, -16 LUFS).
# Output: DIR/<name>.mp4 (1080x1920 30 fps CFR H.264, BT.709), DIR/grade/<name>.cube, DIR/grade/params.json
import glob, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np

SW, SH, N = 270, 480, 10
LUMA = np.array([0.2126, 0.7152, 0.0722])
VOICE_CLEAN = ("highpass=f=100,lowpass=f=9000,afftdn=nr=12:nf=-38,equalizer=f=250:t=q:w=1:g=-3,equalizer=f=3000:t=q:w=1.2:g=4,"
               "acompressor=threshold=-24dB:ratio=2.5:attack=10:release=150:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=11")


def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def encoder():
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "nullsrc=s=256x256:d=0.1", "-c:v", "h264_nvenc", "-f", "null", "-"],
                       capture_output=True)
    return ["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "19"] if r.returncode == 0 else ["-c:v", "libx264", "-preset", "medium", "-crf", "17"]


def samples(f):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    frames = []
    for k in range(N):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{dur * (k + 0.5) / N:.3f}", "-i", f, "-frames:v", "1", "-vf",
                              f"scale={SW}:{SH},format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        if len(raw) >= SW * SH * 3: frames.append(np.frombuffer(raw, np.uint8)[:SW * SH * 3].reshape(SH, SW, 3))
    return np.stack(frames).reshape(-1, 3).astype(np.float32) / 255


def grade(x, a, b, gamma, vib, curve=0.12):
    x = np.clip((x - a) / (b - a), 0, 1) ** (1 / gamma)
    x = x + curve * ((3 * x * x - 2 * x ** 3) - x)
    y = (x @ LUMA)[..., None]
    sig = x.max(-1, keepdims=True) - x.min(-1, keepdims=True)
    f = 1 + vib * (0.35 + 0.65 * (1 - np.minimum(sig / 0.5, 1)))
    r, g, bl = x[..., :1], x[..., 1:2], x[..., 2:]
    hue = 60 * (g - bl) / np.maximum(r - bl, 1e-4)
    skin = ((r > g) & (g > bl) & (y > 0.2) & (y < 0.9)) * np.clip(1 - np.abs(hue - 25) / 25, 0, 1)
    f = 1 + (f - 1) * np.where(vib > 0, 1 - 0.6 * skin, 1)
    return np.clip(y + (x - y) * f, 0, 1)


def stats(x):
    y = x @ LUMA
    u, v = (x[..., 2] - y) / 1.8556 * 224, (x[..., 0] - y) / 1.5748 * 224
    return float(y.mean()), float(np.sqrt(u * u + v * v).mean())       # mean luma (0-1), SATAVG-equivalent (8-bit)


def bisect(fn, lo, hi, target, it=22):
    for _ in range(it):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if fn(mid) < target else (lo, mid)
    return (lo + hi) / 2


def solve(x, target_y, target_s, keep=0.35):
    y = x @ LUMA
    lo, hi = np.percentile(y, [0.5, 99.5])
    s = min(1.3, max(1.0, (0.975 - 0.015) / max(hi - lo, 1e-3)))
    a = min(0.12, max(0.0, lo - 0.015 / s)); b = a + 1 / s
    y0, s0 = stats(x)
    ts = s0 if target_s is None else target_s + keep * (s0 - target_s)
    ty = target_y + keep * (y0 - target_y)
    gamma = bisect(lambda g: stats(grade(x, a, b, g, 0))[0], 0.8, 1.35, ty)
    vib = bisect(lambda v: stats(grade(x, a, b, gamma, v))[1], -0.3, 1.0, ts)
    return dict(a=round(a, 4), b=round(b, 4), gamma=round(gamma, 4), vib=round(vib, 4), before=[round(y0, 3), round(s0, 1)],
                after=[round(v, 3) for v in stats(grade(x, a, b, gamma, vib))])


def cube(path, p, n=33):
    t = np.linspace(0, 1, n, dtype=np.float32)
    bb, gg, rr = np.meshgrid(t, t, t, indexing="ij")                    # .cube order: red fastest
    out = grade(np.stack([rr, gg, bb], -1).reshape(-1, 3), p["a"], p["b"], p["gamma"], p["vib"])
    with open(path, "w") as fh:
        fh.write(f"LUT_3D_SIZE {n}\n"); fh.writelines(f"{r:.5f} {g:.5f} {b:.5f}\n" for r, g, b in out)


def main():
    out = opt("--out", "graded"); os.makedirs(os.path.join(out, "grade"), exist_ok=True)
    ty = float(opt("--target-y", 0.475)); ts = None if "--keep-sat" in sys.argv else float(opt("--target-s", 19.0))
    audio = opt("--audio", "none"); enc = encoder()
    skip = {opt(k, None) for k in ("--out", "--target-y", "--target-s", "--audio", "--sheet")}
    files = []
    for a in sys.argv[1:]:
        if a.startswith("--") or a in skip: continue
        files += sorted(glob.glob(os.path.join(a, "*.[mM][oOpP][vV4]"))) if os.path.isdir(a) else [a]

    def one(f):
        n = os.path.splitext(os.path.basename(f))[0]
        p = solve(samples(f), ty, ts)
        lut = os.path.join(out, "grade", f"{n}.cube"); cube(lut, p)
        lut_ff = lut.replace("\\", "/").replace(":", "\\:")
        vf = (f"fps=30,scale=1080:1920:flags=lanczos,format=rgb24,lut3d=file='{lut_ff}':interp=tetrahedral,"
              "unsharp=5:5:0.3:5:5:0,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p")
        au = {"none": ["-an"], "keep": ["-c:a", "aac", "-b:a", "256k", "-ar", "48000"],
              "clean": ["-af", VOICE_CLEAN, "-c:a", "aac", "-b:a", "256k", "-ar", "48000"]}[audio]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-vf", vf, *au, *enc, "-g", "15", "-bf", "0", "-fps_mode", "cfr",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                        "-movflags", "+faststart", os.path.join(out, f"{n}.mp4")], check=True)
        print(n, p, flush=True)
        return n, p

    pj = os.path.join(out, "grade", "params.json")
    params = json.load(open(pj)) if os.path.exists(pj) else {}
    with ThreadPoolExecutor(2) as ex:                                   # 2 at a time: the laptop shut down once under 3 heavy jobs
        params.update(dict(ex.map(one, files)))
    json.dump(params, open(pj, "w"), indent=1)
    if "--sheet" in sys.argv:                                           # before | after, 4 clips per row: show the client
        from PIL import Image
        tiles = []
        for f in files[:8]:
            n = os.path.splitext(os.path.basename(f))[0]
            for src in (f, os.path.join(out, f"{n}.mp4")):
                raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "1", "-i", src, "-frames:v", "1", "-vf", "scale=270:480,format=rgb24",
                                      "-f", "rawvideo", "-"], capture_output=True).stdout
                tiles.append(Image.frombytes("RGB", (270, 480), raw[:270 * 480 * 3]))
        g = Image.new("RGB", (270 * 8, 480 * ((len(tiles) + 7) // 8)))
        for i, im in enumerate(tiles): g.paste(im, ((i % 8) * 270, (i // 8) * 480))
        g.save(opt("--sheet", "compare.jpg"), quality=88)


if __name__ == "__main__":
    main()
