# Pre-delivery gate (run every item; report the ones you could not check)

## Story and style
- [ ] ≤ 60 s (or the length the brief / user set). Title promise kept; no aside that breaks it.
- [ ] First 3 s: real-sound brand moment + faces; no blank or slow establishing shot.
- [ ] Register consistent (recap vs formal); ≤ 3 font families; SIU in crimson/red; official logos/outro used if provided.
- [ ] Every graphic has a reason and an SFX (recap); optional decoration used once at most.

## Picture
- [ ] `smoothness.py` → 0 STUTTER; `blackdetect` → none.
- [ ] No bad face (closed / half-closed eyes, squint, looking down, mid-word mouth) on the MAIN face (speaker / subject of the shot) at: freezes, holds, pop-out
      and card stills, the cover, ±3 frames of every cut, transition windows, slow-motion stretches, punch-in starts/ends
      (every entry of `qa/face_points.json` checked with eye crops).
- [ ] `textcheck.py` → 0 failures, and the sheet looked at by eye (signs, banners, hands).
- [ ] Each source used once; first/last frame of every shot clean.
- [ ] Grade even across clips; before/after sheet shown.

## Sound
- [ ] Music licence covers the platform (screenshot in the project); no lyrics; loopiness < 50 %.
- [ ] Voice over music: recap VO ≥ 11 dB, speech ≈ 20 dB; duck held through the VO, no pumping.
- [ ] Only the named voice clips unmuted.
- [ ] Master −14 LUFS, true peak ≈ −1.5 dBTP (numbers in the report).

## Words
- [ ] Names, titles, places spelled exactly as the brief; NFC; no emoji.
- [ ] Subtitles: client-approved text or marked "chờ duyệt" with BAN_DICH_CHO_DUYET.md; no hallucinated lines; foreign
      language only unless asked; ≤ 2 lines, ≤ 1 highlighted word.

## CapCut project
- [ ] Every element on its own named track; nothing flattened; graphics CapCut cannot do = transparent layers.
- [ ] Opened in CapCut: no missing media, text sizes right, music envelope right, transitions present.
- [ ] Export Pro check passed (no Pro elements, no watermark).
- [ ] `package()` OK (no machine paths); install test from the zip under another name passed.
- [ ] The MP4 delivered is the CapCut export (CapCut-first) or matches the project.

## Delivery
- [ ] Master on the PC; < 30 MB 720p preview sent to the phone (SendUserFile).
- [ ] Zip + HUONG_DAN + client message ready.
- [ ] Report: what changed, measured numbers, what was NOT verified (listening, any CapCut moment not opened).
