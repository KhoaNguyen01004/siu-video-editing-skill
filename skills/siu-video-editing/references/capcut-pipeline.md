# CapCut-first pipeline (pycapcut) — architecture, units, gotchas

## Why CapCut-first
The client edits and publishes from the CapCut project (both approved videos were exported from our CapCut drafts after
their edits). Anything that exists only in a Remotion/ffmpeg render never reaches the public (lesson F6). So:

```
footage ─ probe ─ grade_lut (graded CFR proxies, cleaned voice) ─┐
music_check, lang_id/score_text, crop_sheet (freeze frames) ─────┤
                                                                 ├─ build.py  (ONE source of truth: cut list, texts, music,
sfx_gen, cutout, slowmo, transparent graphics layers ────────────┘             SFX, positions)  ──>  CapCut draft (layered)
                                                                                        │
                    CapCut (computer-use): open, check, Export 1080p ──> master.py --copy-video ──> final MP4
                                                                                        │
                                                         capcut_kit.package() ──> client zip + installer
```

Use Remotion (remotion skills) or HyperFrames only for graphics CapCut cannot build (footage inside letters, rings drawn
behind letters, scrapbook frames), exported as **transparent layers** (ProRes 4444 with alpha, full 1080×1920 canvas) and
placed on their own track above the live footage. Never flatten footage + graphics into one clip.

## Project rules
- `pip install pycapcut==0.0.4` (0.1.0 renames the track API). Tested with CapCut desktop 9.8 (Windows), plain-JSON drafts.
  CapCut 10.x may write drafts differently: open one real draft first and compare before trusting the kit.
- Close CapCut (kill `CapCut.exe`) before writing a draft; it overwrites drafts it has open. Back up any draft the user may
  have edited (`create_draft(allow_replace=True)` deletes the old folder).
- One named track per element type or element (client edits by track): `Footage`, `Panels n`, `Graphics`, `Title · …`,
  `Stickers`, `Chapter`, `Phụ đề`, `Nhạc nền`, `Voice`, `SFX n`, `Hiệu ứng`. Track order = creation order per type
  (later = on top).
- All media copied into `<draft>/media` (kit does it) so the zip is self-contained.

## Units and coordinates
| Thing | Unit / rule |
|---|---|
| Times | microseconds (int). `US(seconds)`. |
| Durations of animations, transitions, fades | **strings** `"0.4s"`. A number is microseconds (lesson F2). |
| Position | half-canvas units, origin centre, **+y up**: `transform_x = (x − 540)/540`, `transform_y = (960 − y)/960` for the element's centre in px (`Project.pos`). |
| Keyframes of VIDEO / AUDIO segments | **source time**: `source_start + t × speed` (`Project.kf_time`). Lesson D4: clip-relative times put the music duck 53 s off. |
| Keyframes of TEXT segments | segment-relative `US(t)`. |
| Source range | `floor(target_us × speed)` (lesson F11). Photos: source range = (0, duration). |
| Speeds | 1, 2, or x4 interpolated files at 4 / 2 / 4⁄3 (never 0.8, 1.5). |
| Images | CapCut fits images to the canvas: export overlays as full 1080×1920 PNGs with the element in place. |

## Text
- `Project.text(...)` = `auto_wrapping=False` + size from `K[font]` + width fitted with PIL on CapCut's own font file
  (`%LOCALAPPDATA%\CapCut\User Data\Cache\effect\*\*\<font file>`), `maxw` default 900 px.
- Measured K (px of em per size unit, 1080 canvas, CapCut 9.8): Montserrat 5.14, Anton 4.3, Playfair Display Italic 4.65,
  Prata 4.63, Classic/TikTok Display 6.3, Coiny ≈ 3.5 (±0.2, CapCut preview + client export).
- **Calibrate a font:** draft with "HIH" at size 10 in that font, export from CapCut, measure the H height/width in the
  MP4, compare with PIL at a known px → K. Fonts are downloaded only after a draft that uses them is opened in CapCut.
- Keyword colour ranges: `highlight=["rất vui"]` (kit writes one style per character range).
- Vietnamese text in NFC. No emoji (CapCut renders them inconsistently and the client removes them).
- Animations that loaded and passed the export Pro check in 9.8: intros 渐显, 逐字, 弹出, 弹入, 向右滑动, 向左滑动; outros 渐隐,
  向左滑动; loop 调皮. **Outro 缩小 "shrink" does NOT load in 9.8** (⚠ "Animation" on the clip, empty resource path) although
  pycapcut marks it free: the Mỹ Tho v4 stickers used it. Check every new animation once in CapCut. **向上滑动 "Slide Up" asked for Pro** although pycapcut marks it free → keyframe position_y + alpha.

## Picture
- Transitions on the clip BEFORE the cut, attached before adding the segment: `video(..., transition=(T.叠化, "0.3s"))`.
  Passed free: 叠化, 横向模糊, 推近, 左移/右移, 闪白, 光束, 圆形遮罩, 向左擦除, 色差故障. 向上 on a pushed-down still drew a mirrored edge.
- Masks: `seg.add_mask(MaskType.矩形, size=h_frac, rect_width=w_frac, round_corner=r)`; fractions of the CLIP, so divide by
  the clip's scale. One clip per panel for split screens / grids, panels slide in with position keyframes.
- Effects (scene, on effect tracks): passed free 柔光, 金粉闪闪, 抖动, 五彩纸屑, 仙尘闪闪. List what pycapcut marks free:
  `python scripts/capcut_kit.py --free` (then confirm in CapCut: not every enum entry exists in every CapCut build).
- Pop-out: live clip → freeze still (JPG of an eyes-open ORIGINAL frame) → rays PNG with rotation keyframes → cut-out PNG
  (`cutout.py`) with spring scale keyframes → white flash with alpha keyframes.
- Remotion springs/easings for keyframes: sample the curve at frame steps and write keyframes (exact, not re-implemented).

## Sound
- `AudioMaterial` refuses files with a video stream: extract `.wav` (`ffmpeg -i clip.MOV -vn -ac 2 -ar 48000 x.wav`).
- Music with gain keyframes: `Project.music(path, start, dur, src=offset_in_track, gains=[(t, g)...])`.
- SFX: `Project.sfx(t, path, vol)` (tracks allocated at save).

## 16:9 copy (if asked)
Separate draft 1920×1080: the 9:16 picture centred at scale 0.5625 over a cream / blurred backdrop, title block left, a
chapter tracker right. Never crop portrait footage to 16:9.

## CapCut text templates / sticker packs
Do not plan around them: in 9.8 the template search failed with "network error", most templates are Pro, and the free
ones are cartoon-style (the brief for the speaker video said "tránh hiệu ứng… hoạt hình trẻ con"). Build the look from
fonts + animations + keyframes, which the client can still edit.

## When the kit is not enough
`pycapcut` covers segments, text, keyframes, masks, transitions, effects, filters, audio. For anything else, build it by
hand once in CapCut, save, read that draft's JSON, and copy the structure (that is how the community tools work:
clone from a real draft).
