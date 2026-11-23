# Pop-out sticker of a person: freeze one frame, cut the person out (rembg u2net_human_seg), add a white sticker outline.
# Output: <out>.png (RGBA, full canvas size so CapCut scale 1 = true size) and <out>_bg.jpg (the frozen frame).
# Pick the frame with crop_sheet.py first (eyes open). Skip people that touch the frame edge (a cut-off arm looks broken).
# rembg mistakes red lanterns / red shirts on a red background for people sometimes: look at the preview.
#   python cutout.py <video> <time_s> <out_base> [--outline 23]
import io, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter
from rembg import remove, new_session

v, t, base = sys.argv[1], float(sys.argv[2]), sys.argv[3]
ol = int(sys.argv[sys.argv.index("--outline") + 1]) if "--outline" in sys.argv else 23
png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                     capture_output=True, check=True).stdout
img = Image.open(io.BytesIO(png)).convert("RGB")
img.save(base + "_bg.jpg", quality=92)
cut = remove(img, session=new_session("u2net_human_seg"), post_process_mask=True)
a = np.where(np.array(cut.split()[-1]) > 128, 255, 0).astype(np.uint8)
outline = Image.fromarray(a).filter(ImageFilter.MaxFilter(ol | 1)).filter(ImageFilter.GaussianBlur(1.5))
sticker = Image.new("RGBA", img.size, (255, 255, 255, 0)); sticker.putalpha(outline)
person = img.copy(); person.putalpha(Image.fromarray(a).filter(ImageFilter.GaussianBlur(0.8)))
sticker.alpha_composite(person)
sticker.save(base + ".png")
edge = a[:, :3].any() or a[:, -3:].any() or a[-3:, :].any()
prev = Image.new("RGB", img.size, (40, 120, 60)); prev.paste(sticker, (0, 0), sticker); prev.resize((270, 480)).save(base + "_preview.jpg")
print(f"{base}.png bbox {sticker.getbbox()} coverage {100 * (a > 0).mean():.1f}%{'  WARNING: touches the frame edge' if edge else ''}")
