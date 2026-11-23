# Footage, framing, colour and timing QA

## 1. Inventory (before planning)
- `python scripts/probe.py <folder> --md qa/inventory.md`: duration, size, rotation, fps, VFR, HDR, audio streams.
  - No audio stream on a clip the brief calls "có voice" → tell the user at once.
  - HLG / PQ (iPhone HDR) → tone-map to SDR before grading or it looks grey.
  - VFR → transcode to CFR 30 (grade_lut.py does).
  - Landscape clip in a 9:16 edit → plan a reframe (blurred fill or a crop that keeps heads), never stretch.
- `python scripts/contact_sheet.py <clip> sheet.jpg --every 1` per clip; read them all before choosing shots.
- Transcribe every clip that has speech, and check burned-in text / subtitles in the footage.

## 2. Shot choice
- Natural expressions, smiles, interaction, curiosity; mix wide / medium / close; no two similar angles in a row.
- Each source once (a take continuing itself is fine). Keep a `used` set in the build script and assert it.
- First and last frame of every shot: no clipped heads, no stray hands, nobody blocking the lens
  (`contact_sheet.py` at the in and out points).

## 3. Speed and smoothness
- Only 1× or exactly 2×. Slow motion = `scripts/slowmo.py` (4× motion-interpolated); play the x4 file at 4 (real time),
  2 (0.5×), 4/3 (⅓×). Ramps = constant-speed pieces.
- Ease beat pulses and camera shakes over ≥ 3 frames (a 1-frame zoom reads as a stutter).
- After every render: `python scripts/smoothness.py out.mp4` → 0 STUTTER lines; `ffmpeg -i out.mp4 -vf blackdetect=d=0.03
  -an -f null -` → no black frames.

## 4. Bad faces at cuts, pauses and slow motion
User rule (tiếng Nga reel): "đừng có bao giờ pause ngay lúc người đang có biểu mặt xấu, ví dụ như nhắm mắt hay gì đó".
Bad = closed eyes, a blink, a smiling squint, looking down, eyes half shut, mouth half open mid-word, a grimace, a blurred
face mid-turn. It applies to the MAIN face of the shot: the person talking, or the subject the shot is about (the singer,
the student holding the honeycomb, the speaker). Background faces in a crowd do not need checking (user, 2026-11-24).
In a group shot with no single subject, check the faces nearest the camera / centre. The check is manual (eye crops).

Where the viewer actually sees a single frame or a stretched moment (check all of them):
| Moment | Why it shows | Check |
|---|---|---|
| Freeze / hold / pop-out still / scrapbook photo | held 1–3 s | eye crops 0.1 s around the chosen time; pick an original frame |
| Title-card still, end-card still, cover / thumbnail | held, and the cover is seen before playing | same |
| Last frame before a cut and first frame after it | a hard cut leaves the last frame in the viewer's eye; a blink on the cut reads as a "pause" | ±3 frames (0.1 s) around every in and out point |
| Frames under a transition (dissolve, zoom, blur, 0.3–0.5 s) | the transition blends / slows these frames | the whole transition window of both clips |
| Slow motion (x4 at ½ or ¼ speed) | a 0.15 s blink becomes 0.3–0.6 s | every original frame of the slowed range |
| Punch-in close-ups on a speaker | the face fills the frame | the first and last 0.3 s of each punch-in |

How:
- `python scripts/crop_sheet.py clip.mp4 eyes.jpg <t0> <t1> --box x0 y0 x1 y1 --step 0.033` (one tile per frame) on each
  face's eyes (box ~200×130 px at 1080×1920). Look at every tile; do not decide from the middle one.
- Fix by moving the cut point 2–5 frames away from the blink, shifting the slow-mo range, or picking another still.
  Never cover a bad face with a sticker or a transition.
- A slow-mo that ends on a hold must end ON an original frame (x4 index divisible by 4), and that frame must pass too.
- The build script writes the list of these moments (`qa/face_points.json`); go through all of them before export.

## 5. Text placement
- Never on a face, on the person the shot is about, on gesturing hands, on other text, or on signage / banners / logos
  in the footage (the client removed text that sat on the "SIU BEYOND TOMORROW" backdrop).
- Prefer calm uniform areas: sky, roof, plain wall, tablecloth, floor. A frame full of faces gets no text: move the text
  to the neighbouring shot.
- `python scripts/textcheck.py boxes.json qa/textcheck.jpg` (the build script writes boxes.json) → 0 failures, then look
  at the sheet: rembg sees red lanterns as people and does not see signs.
- Platform UI: the classic safe area is x 80–1000, y 270–1250; the client accepts subtitles and lower thirds lower
  (y 1360–1700) when the bottom of the frame is calm. Keep ≥ 220 px clear at the bottom and ~120 px on the right
  (TikTok buttons).

## 6. Colour
- `python scripts/grade_lut.py <clips> --out graded --sheet qa/grade_compare.jpg`: per-clip LUT toward a shared bright,
  clear, natural look (levels, gamma toward mean luma 0.475 ≈ YAVG 120, gentle S-curve, vibrance toward SATAVG 19 with
  skin protected). `--keep-sat` for scenes that are already vivid.
- Show the before/after sheet to the user; ask "tươi sáng, trong, tự nhiên?" rather than trusting numbers.
- Never copy another channel's luma/saturation numbers onto phone footage.
- In CapCut-first builds the graded proxies ARE the media in the project (the client gets the graded look and can still
  add CapCut filters on top).

## 7. Faces for punch-ins (speaker videos)
- Face boxes every 0.25 s (rembg person mask, the crown of the largest blob) → crop so the face sits at x 540, y 700–745
  for mid (1.2×) / close (1.38×), clear of the text bands (reference implementation: `faces.py` of the tiếng Nga
  project, not included in this skill).
