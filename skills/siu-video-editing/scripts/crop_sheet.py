# Pick a freeze frame / hero still by eye: a grid of crops of one region over a time range.
# User rule: never freeze (or hold, or end a slow-mo) on a bad face - closed eyes, a squinting smile, looking down,
# mid-blink, mouth half-open. Check the MAIN face (the person talking / the subject of the shot); background faces need not.
# Zoom on the eyes (box ~200x130 px at 1080x1920) and step 0.1 s; prefer an ORIGINAL frame over an interpolated one.
#   python crop_sheet.py <video> <out.jpg> <t0> <t1> --box x0 y0 x1 y1 [--step 0.1] [--cols 10] [--scale 2]
import io, subprocess, sys
from PIL import Image, ImageDraw


def main():
    v, out, t0, t1 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    i = sys.argv.index("--box"); x0, y0, x1, y1 = (int(float(a)) for a in sys.argv[i + 1:i + 5])
    step = float(sys.argv[sys.argv.index("--step") + 1]) if "--step" in sys.argv else 0.1
    cols = int(sys.argv[sys.argv.index("--cols") + 1]) if "--cols" in sys.argv else 10
    sc = float(sys.argv[sys.argv.index("--scale") + 1]) if "--scale" in sys.argv else 2.0
    n = int(round((t1 - t0) / step)) + 1
    # one decode pass: crop in source pixels (video assumed already 1080x1920 upright; scale first if not)
    vf = f"fps={1 / step},scale=1080:1920,crop={x1 - x0}:{y1 - y0}:{x0}:{y0},scale=iw*{sc}:ih*{sc}:flags=lanczos"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-t", str(t1 - t0 + step / 2), "-i", v, "-vf", vf,
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    ims, k = [], 0
    while k < len(raw) and len(ims) < n:                      # split the PNG stream
        end = raw.find(b"IEND", k) + 8
        ims.append(Image.open(io.BytesIO(raw[k:end])).convert("RGB")); k = end
    W, H = ims[0].size; rows = (len(ims) + cols - 1) // cols
    g = Image.new("RGB", (W * cols, (H + 18) * rows), "black"); d = ImageDraw.Draw(g)
    for j, im in enumerate(ims):
        x, y = (j % cols) * W, (j // cols) * (H + 18)
        g.paste(im, (x, y + 18)); d.text((x + 3, y + 3), f"{t0 + j * step:.2f}s", fill=(255, 230, 0))
    g.save(out, quality=90)
    print(out, f"{len(ims)} crops of {x1 - x0}x{y1 - y0}px")


if __name__ == "__main__":
    main()
