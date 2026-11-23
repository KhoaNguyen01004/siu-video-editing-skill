# Motion-graphic layers with Remotion (only what CapCut cannot build)

CapCut-first means Remotion renders **graphics only**, as transparent layers placed above the live footage in the CapCut
project (never footage + graphics flattened). Reference implementation: the Mỹ Tho project `reel-siu-mytho`
(`src/Reel.tsx`, `src/Graphics.tsx`, comp `SIULayer`, `tools/edl.py`; not included in this skill). Load the `remotion-best-practices` skill first.

## Export a layer
- Composition 1080×1920, 30 fps, transparent background, only the graphic.
- `npx remotion render SIULayer out/layers/<name>.mov --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le`
  (ProRes 4444 keeps alpha; CapCut 9.8 reads it). One heavy render at a time, `--concurrency=6`.
- Put each layer on its own CapCut track; name it after the element ("Graphics · title MỸ THO").
- If something must stay locked together (letters with footage inside + their outline + the zoom-through), keep it one
  layer; everything else (rings, pin, kicker text) separate (user: "tách các element ra…").

## Recipes that worked (Mỹ Tho v3/v4)
| Element | How |
|---|---|
| Footage inside the title letters | SVG `<mask>` knockout of the letters over a cream card; the live footage shows through on the track below. CSS `clip-path:url()` on a video canvas does NOT work. |
| Brand rings | red / green / yellow arcs drawing on (stroke-dashoffset), rotating slowly; render them BEHIND the letters in the same layer if they must not cross the letters (unmasked rings drew over the letters in CapCut). |
| Per-letter sticker bounce | spring per letter, stagger ≤ 0.7 frame (more and words appear half-built); group letters per word (per-letter inline blocks broke words mid-line: "khám ph / á"). In CapCut-first builds, prefer CapCut text with 弹入 instead. |
| Pop-out freeze | frozen frame shrinks into a tilted white-bordered card over rays on cream; rembg cut-out (cutout.py) springs out of the card. In CapCut: still + rays PNG + cut-out PNG with keyframes (no Remotion needed). |
| Speed ramps | `<Freeze frame={remap(f)}>` around the video = arbitrary time remap; in CapCut use constant-speed pieces of the x4 file. |
| Transitions | zoom blur, whip L/R, glitch (hue jitter + RGB bars), iris, brand-band wipe, flash, light leak. In CapCut use its free transitions (capcut-pipeline.md). |
| Energy | beat pulses on downbeats eased over ≥ 3 frames; camera shake on impacts (CapCut effect 抖动 works too). |
| Scrapbook ending | group shot shrinks into a polaroid, the day's freeze frames fly in as photos, Pacifico title. |
| 16:9 copy | phone stage scaled into the centre over cream; title block left; brand rings + "CHẶNG 0X" tracker right. |

## Keyframes from Remotion curves
For a CapCut keyframe animation that must match a Remotion spring, sample the spring per frame in Node
(`spring({frame, fps, config})`) and write those values as CapCut keyframes (exact, not re-implemented).

## Checks
- `node tools/stills.mjs <frames…>` → half-size stills with the safe-area overlay, before the full render.
- After a crash: `ffmpeg -v error -i x.mov -f null -` on every layer before using it.
