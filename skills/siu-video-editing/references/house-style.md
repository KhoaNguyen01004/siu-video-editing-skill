# SIU house style

Two registers. Pick one per video from the brief; never mix them.

| | **Energetic recap** (field trip, campus life, events, sports) | **Formal speaker** (lecturer, VIP greeting, ceremony, partner event) |
|---|---|---|
| Feeling | young, playful, high energy, "SIUers" | proud, elegant, smart, warm |
| Type | Coiny stickers, Montserrat Bold labels, one Pacifico line at most | navy serif (Playfair / Prata) + one condensed display (Anton); subtitles in TikTok Display |
| Motion | bounce-in stickers with a wiggle loop, whips, zoom blur, split screens, grids, pop-out freezes, speed ramps (1× / 2× / interpolated) | dissolves, slow push-ins on emphasis, slide-in lower third, typewriter on a foreign word |
| SFX | a cue on every transition and graphic (whoosh, pop, shutter, riser, impact, contextual) | sparse: a whoosh on the card, a soft pop per title line |
| Music | bright instrumental, clear beat, sections that change | light, modern, low under the voice (≈ 20 dB down) |
| Examples | Mỹ Tho reel (approved) | tiếng Nga reel (approved) |

## Brand colours
| Token | Hex | Use |
|---|---|---|
| SIU navy | `#2C3C82` | formal text, school names (sampled from the client's approved title card = the emblem blue) |
| SIU red | `#B71E26` | the word "SIU" on formal cards |
| Crimson | `#BB1C3D` (client used `#B71A3A`) | display lines, name bar, chapter pills, sticker outlines |
| Green | `#3D9032` | sticker outlines, recap accents, rings |
| Pop yellow | `#FFD23F` | sticker fill, chapter numbers, ONE highlighted keyword in a subtitle |
| Cream paper | `#F0E9D4` / `#F4ECD8` | title-card paper, role bar, recap backgrounds |
| Ink | `#1E1E1E` | small text on cream (role bar) |

**The word SIU is always crimson/red** (navy only inside a navy logo lockup). The client recoloured "SIU" every time we
left it white or yellow.

## Fonts (all from CapCut's free library, checked for Vietnamese with `capcut_kit.py --fonts`)
| Role | Font (pycapcut `FontType`) | Notes |
|---|---|---|
| Sticker / chapter number | `Coiny_Regular` | VN ok, no Cyrillic. Fill white or yellow, 40-width outline green or crimson |
| Labels, lower third, recap info | `Montserrat` (bold flag for weight) | VN ok, no Cyrillic. The client used a lighter weight for the name in the lower third |
| Formal serif | `PlayfairDisplay_Italic`, `Prata_Regular` | VN + Cyrillic. Navy for statements, crimson for the italic connector ("bằng") |
| Display | `Anton` | VN ok, no Cyrillic. Crimson, big, one line |
| Subtitles | `Classic` (= TikTok Display Medium) | VN ok, no Cyrillic. White, black outline, ≤ 1 yellow keyword |
| Cyrillic / other scripts | Playfair Display Italic, Prata, Philosopher, Alegreya SC, Arno Pro, Oswald ExtraLight, Source Han | others lack Cyrillic |
| Avoid | Poppins, Bebas Neue, most script fonts | **missing Vietnamese diacritics** in CapCut's files |

Max 3 families per video, max 2 per card.

## Components (positions on a 1080×1920 canvas; centre of the element unless noted)

**Recap title (word mark).** Brand rings (red / green / yellow arcs drawing on) + one big word ("MỸ THO") with footage
inside the letters. Nothing else on the card: faculty and place go in the voice-over or the caption.
CapCut: knockout letters as a transparent graphics layer (rendered with alpha) above the live footage; rings as their own
track; rings pass BEHIND the letters (render the rings into the same alpha layer if they must stay behind).

**Formal title card.** Cream paper sheet slides down over the top ~42 % (ends ~y 810 with a thin crimson rule), the
speaker still visible below (face not covered). Top: real emblems + official names of both institutions (~y 120).
Lines: statement in navy serif (~y 280, "SIU" in red bold), sub-line navy serif smaller (~y 370), italic crimson connector
(~y 450), the hook word in crimson Anton (~y 600, the biggest thing on the card). 3 s. Whoosh in, pop per line.

**Chapter tag (recap).** Yellow Coiny number with a crimson outline + crimson pill with a white Montserrat title, left side,
on the calm part of the frame (measured: 01 at (165, 800) / pill centre (532, 820)). 2.3 s, bounce in, fade out.

**Sticker (recap).** Coiny, one line, never wrapped, ≤ 820 px wide, tilted −6°…+6°, bounce-in + "调皮" wiggle loop,
scale-out. White fill + green outline, or yellow fill + crimson outline. In sky / roof / wall space (y ≈ 360–530 measured).
No emoji. 1–1.7 s. Pop SFX.

**Label (recap).** Small cream pill, dark Montserrat ("Tìm hiểu mô hình kinh doanh"), lower left. Ka-ching SFX.

**Lower third (formal).** Crimson bar, white uppercase name (lighter weight); cream bar below with the role, dark text.
Left aligned, wide (x ≈ 24–950), low: name y ≈ 1360, role y ≈ 1480. Slide in from the left, 5 s, slide out.

**Subtitles.** TikTok Display, white, black outline, ~66 px, ≤ 2 lines, ≤ 1 yellow keyword, on the calmest band below the
subject (approved: y ≈ 1665 on a plain tablecloth; default band y 1450–1700, ≥ 220 px from the bottom). Fade in 0.12 s.
Foreign language only, unless the brief asks for full captions.

**Split screen trio / 2×2 grid.** Panels slide or pop in on beats, white rounded borders, cream backdrop. Use the grid for
the hook (many moments at once). CapCut: one clip per panel with a rectangle mask + keyframes.

**Pop-out freeze.** Frame freezes (eyes open!), shrinks into a tilted white-bordered photo card over rays on cream, the
person (rembg cut-out with a white outline) springs out of the card, shutter SFX, sticker above.

**Kinetic chant words.** Coiny words popping in sync with a real chant ("I love SIU!"), placed in the empty part of the
frame (lower grid panels in the approved hook), "SIU" crimson with a white outline.

**Outro.** The official animated SIU logo sting (ask the client for the file). Never recreate the SIU logo or the SIUTV
"EYES ON SIU" sting; concentric brand rings as a nod are fine.

## Channel reference (@dhquoctesaigon, 8 videos studied 2026-11-21)
- Openings: branded sting, or a staggered split screen with a chunky yellow sticker title bouncing in letter by letter.
- Transitions: motion-blur whips, zoom / radial blur, chromatic-aberration flashes, film-burn dips, split-screen panels.
- Pacing: median shot 1.1–1.6 s in montage recaps (0.5 s in sports); longer only for talking heads.
- Their footage look (luma 120–150, saturation ~11, lifted blacks) comes from their cameras; **do not copy those numbers
  onto phone footage** (lesson C1).

## Do / don't
- Do: one palette, 2–3 families, a reason for every graphic, an SFX for every graphic, text on calm areas.
- Don't: emoji in text, text over faces / hands / other text / signage, two languages of decorative text at once, a title
  block of 4 stacked lines, white or yellow "SIU", decoration in the first 3 s of a speech that hides the speaker.
