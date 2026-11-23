# Labelled frame grid of a video (PIL labels: ffmpeg drawtext segfaults on Windows builds without fontconfig).
#   python contact_sheet.py <video> <out.jpg> --every 1            one frame per second
#   python contact_sheet.py <video> <out.jpg> 0.5 2.6 4.2 ...      given times
#   options: --cols 8  --width 240  --safe  (draw the 9:16 safe area x 80-1000, y 270-1250 and the subtitle band y 1450-1700)
import io, subprocess, sys
from PIL import Image, ImageDraw, ImageFont


def opt(name, default, cast=float):
    return cast(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def duration(v):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v]))


def frame(v, t, w):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1", "-vf", f"scale={w}:-2",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(b)).convert("RGB") if b else None


def main():
    v, out = sys.argv[1], sys.argv[2]
    flags = {"--every", "--cols", "--width"}
    rest = [a for i, a in enumerate(sys.argv[3:], 3) if not a.startswith("--") and sys.argv[i - 1] not in flags]
    w, cols = int(opt("--width", 240)), int(opt("--cols", 8))
    if "--every" in sys.argv:
        step = opt("--every", 1.0); d = duration(v); ts = [round(k * step, 3) for k in range(int(d / step) + 1) if k * step < d - 0.05]
    else: ts = [float(t) for t in rest]
    try: font = ImageFont.truetype("arialbd.ttf", max(12, w // 13))
    except OSError: font = ImageFont.load_default()
    tiles = []
    for t in ts:
        im = frame(v, t, w)
        if im is None: continue
        d = ImageDraw.Draw(im); k = im.width / 1080
        if "--safe" in sys.argv:
            d.rectangle([80 * k, 270 * k, 1000 * k, 1250 * k], outline=(0, 255, 0), width=2)
            d.rectangle([60 * k, 1450 * k, 1020 * k, 1700 * k], outline=(0, 200, 255), width=2)
        d.rectangle([0, 0, w * 0.42, w * 0.11], fill=(0, 0, 0)); d.text((4, 2), f"{t:.2f}s", fill=(255, 230, 0), font=font)
        tiles.append(im)
    W, H = tiles[0].size; rows = (len(tiles) + cols - 1) // cols
    g = Image.new("RGB", (W * min(cols, len(tiles)), H * rows), "black")
    for i, im in enumerate(tiles): g.paste(im, ((i % cols) * W, (i // cols) * H))
    g.save(out, quality=88)
    print(out, f"{len(tiles)} frames, {g.size[0]}x{g.size[1]}")


if __name__ == "__main__":
    main()
