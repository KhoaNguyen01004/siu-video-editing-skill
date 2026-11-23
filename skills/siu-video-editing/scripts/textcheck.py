# Text placement QA (client rule: text never covers a face, the person the shot is about, other text, or a sign in the footage).
# For every text box: people masks (rembg u2net_human_seg) on the PICTURE UNDER the text at a few times, share of the box over
# people, overlaps with other boxes on screen at the same time, and the freest y in the allowed band. Exit 1 if anything fails.
# Then LOOK at the sheet (people tinted cyan, text box yellow, suggested box green): rembg mistakes red lanterns for people
# and does not know about signs or banners in the footage.
#   python textcheck.py boxes.json sheet.jpg [--max-cover 0.12] [--band 270 1700]
#   boxes.json = [{"label": "Ngọt lịm!", "t0": 12.0, "t1": 14.5, "box": [x0, y0, x1, y1],
#                  "frames": [["graded/IMG_7520.mp4", 3.1], ["graded/IMG_7520.mp4", 4.0]]}, ...]
#   box in 1080x1920 canvas px; frames = (picture-only video, time in THAT file) - the source clip under the text, not the
#   final render (the text would mask itself). The CapCut build script knows both and should write this file.
import io, json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
from rembg import remove, new_session

boxes = json.load(open(sys.argv[1], encoding="utf-8")); sheet = sys.argv[2]
MAX = float(sys.argv[sys.argv.index("--max-cover") + 1]) if "--max-cover" in sys.argv else 0.12
i = sys.argv.index("--band") if "--band" in sys.argv else None
BAND = (int(sys.argv[i + 1]), int(sys.argv[i + 2])) if i else (270, 1700)
sess = new_session("u2net_human_seg")
cache = {}


def picture(v, t):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1", "-vf", "scale=540:960", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(b)).convert("RGB")


def mask(v, t):
    if (v, t) not in cache:
        im = picture(v, t)
        cache[(v, t)] = (im, (np.array(remove(im, session=sess, only_mask=True)) > 128).astype(np.float32))
    return cache[(v, t)]


def cover(m, b):
    x0, y0, x1, y1 = [int(round(v / 2)) for v in b]
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(m.shape[1], x1), min(m.shape[0], y1)
    return float(m[y0:y1, x0:x1].mean()) if x1 > x0 and y1 > y0 else 0.0


def inter(a, b): return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


bad, tiles = 0, []
for o in boxes:
    ms = [mask(v, t) for v, t in o["frames"]]
    b = [float(v) for v in o["box"]]; h = int(round(b[3] - b[1]))
    cov = max(cover(m, b) for _, m in ms)
    clash = [q["label"] for q in boxes if q is not o and q["t0"] < o["t1"] and o["t0"] < q["t1"] and inter(b, q["box"])]
    best = min(((max(cover(m, [b[0], y, b[2], y + h]) for _, m in ms), abs(y - b[1]), y) for y in range(BAND[0], BAND[1] - h + 1, 20)),
               default=None)
    fail = cov > MAX or bool(clash)
    bad += fail
    sug = f" -> try y0={best[2]} ({100 * best[0]:.0f}% people)" if fail and best else ""
    print(f"{o['label'][:30]:30s} {o['t0']:5.1f}-{o['t1']:5.1f}s people {100 * cov:3.0f}%  clash {', '.join(clash) or '-'}{sug}"
          f"{'  FAIL' if fail else ''}")
    im, m = ms[len(ms) // 2]
    tint = Image.blend(im, Image.new("RGB", im.size, (0, 190, 255)), 0.55)   # cyan: SIU footage is full of red shirts
    im = Image.composite(tint, im, Image.fromarray((m * 255).astype(np.uint8)))
    d = ImageDraw.Draw(im); d.rectangle([v / 2 for v in b], outline=(255, 230, 0), width=3)
    if fail and best: d.rectangle([b[0] / 2, best[2] / 2, b[2] / 2, (best[2] + h) / 2], outline=(0, 255, 90), width=3)
    d.rectangle((0, 0, 540, 22), fill=(0, 0, 0)); d.text((5, 4), ("FAIL " if fail else "") + o["label"][:60], fill=(255, 80, 80) if fail else (255, 230, 0))
    tiles.append(im.resize((270, 480)))
cols = 8; g = Image.new("RGB", (270 * min(cols, len(tiles)), 480 * ((len(tiles) + cols - 1) // cols)), "white")
for k, t in enumerate(tiles): g.paste(t, ((k % cols) * 270, (k // cols) * 480))
g.save(sheet, quality=86)
print(f"{len(boxes)} text boxes, {bad} failing -> {sheet}")
sys.exit(1 if bad else 0)
