---
name: siu-video-editing
description: Complete method, house style and CapCut toolkit for editing videos for Saigon International University (SIU / ĐH Quốc tế Sài Gòn, TikTok @dhquoctesaigon, SIUTV) - field-trip and event recaps, lecturer / VIP speech reels, campus reels for Facebook Reels / TikTok (9:16, plus an optional 16:9 copy) - delivered as a final MP4 AND an editable, layered CapCut project the client can install and edit on their own PC. Use whenever the user asks to edit, cut, recap, subtitle, re-edit or polish a video for SIU / SIUers / a SIU faculty or partner school, mentions "dhquoctesaigon", "SIUTV", "dựng video", "video recap", "reel cho trường", "lời chúc", "học tập thực tế", "project CapCut", "xuất dự án capcut", "khách tự chỉnh", or sends a brief or client feedback for such a video. Encodes every mistake and every client edit from the approved Mỹ Tho and tiếng Nga reels. Pair with short-form-video (safe zones) and, for motion-graphic layers, remotion-best-practices.
---

# SIU video editing

A SIU video is finished when (1) the client approves the picture and sound, and (2) the client can open **our CapCut
project** on their own PC and edit it. The client publishes from that project, so it is the product, not a by-product.

## Read first
- `references/lessons-learned.md`: 45+ mistakes from three projects, each with its root cause and the check that prevents it.
- `references/client-taste.md`: what the client changed in the two approved videos and why (measured, element by element).
  These are their preferences. Default to them.

## Non-negotiables (each one cost a revision)
1. **CapCut-first.** Build the edit as a layered CapCut draft from one Python source of truth (`templates/build_template.py`
   + `scripts/capcut_kit.py`), export the MP4 from CapCut. Anything only in a Remotion/ffmpeg render never reaches the client.
2. **The best real-sound brand moment in the first 3 s** (chant, cheer, greeting), then a fast montage, then the title.
   ≤ 60 s unless told otherwise. Cut every aside that breaks the title's promise.
3. **"Clean" means cohesive, never plain.** Recaps always get stickers, chapter tags, split screens / grids, a pop-out, a
   transition vocabulary and an SFX on every graphic. Formal speaker videos get restrained, elegant type instead.
4. **Text only on calm areas:** never on faces, gesturing hands, other text, or signage / banners in the footage. One big
   word mark beats a stacked title block. The word **SIU is always crimson/red**. No emoji.
5. **Official assets:** real school emblems, partner logos, the official SIU animated outro. Ask for them; never redraw.
6. **Speed 1× or exactly 2×**; slow motion only from interpolated sources. **A bad face must never be what the viewer
   sees** (closed eye, blink, smiling squint, looking down, mouth half open mid-word, grimace) on the MAIN face of the shot (the person talking, or the subject the shot is about), at:
   a freeze / hold / pop-out still, a title-card or end-card still, the cover, the first and last frames of every cut,
   the frames under a transition, and anywhere inside a slow-motion stretch (a blink at ¼ speed lasts a full second).
   See `references/footage-qa.md` §4.
7. **Colour per clip toward one bright, clear, natural look** (never copy another channel's flat numbers).
8. **Music:** licence valid for the target platform, no lyrics, loopiness < 50 %, big moments on its section changes.
   Voice ~11–15 dB over the music in recaps and ~20 dB in speech videos; the duck holds through the whole voice-over.
9. **Speech:** detect the language of every stretch; subtitle the foreign language only, in natural Vietnamese meaning, from
   the client's own text when it exists. Blank beats wrong. Whisper hallucinations get deleted.
10. **CapCut units:** keyframes of video/audio in SOURCE time, durations as `"0.4s"` strings, `auto_wrapping=False`, text
    size from the measured K per font, transitions on the clip before the cut, media copied into the draft, portable zip
    plus installer, tested like a client.
11. **One heavy job at a time** (render, Whisper large, rembg). Decode-check outputs after any crash.
12. **Claude cannot listen.** Measure (LUFS, dB over music) and say in the report what was not heard and which CapCut
    moments were not opened.

## Workflow (gate at the end of each phase)

| Phase | Do | Tools / references | Gate |
|---|---|---|---|
| 0. Intake | Read the brief; ask once for the missing items (platform, max length, logos, official outro, B-roll, approved text, new VO, music choice) | `references/intake.md` | Answers or stated defaults |
| 1. Inventory | Probe every file; contact sheets; transcribe speech; language map; hallucination check | `scripts/probe.py`, `contact_sheet.py`, `lang_id.py`, `score_text.py`; `references/speech-subtitles.md` | No surprise (silent "voice" clip, HDR, burned-in subs, second language) |
| 2. Plan | Register (recap or formal); story blocks; shot list; text list with positions; music + structure | `references/story-pacing.md`, `house-style.md`, `client-taste.md`, `music_check.py` | `CUT_PLAN.md` shown to the user before building |
| 3. Prepare media | Grade per clip (CFR proxies, voice clean); slow-mo sources; freeze stills with eyes checked; cut-outs; SFX; transparent graphic layers | `grade_lut.py`, `slowmo.py`, `crop_sheet.py`, `cutout.py`, `sfx_gen.py`; `references/footage-qa.md`, `remotion-layers.md` | Before/after colour sheet; eye crops checked |
| 4. Build | Edit `build.py` (copy of `templates/build_template.py`): cuts, texts, music gains, SFX; run it (CapCut closed) | `capcut_kit.py`; `references/capcut-pipeline.md` | Draft written; `CUT_PLAN.md`; `qa/boxes.json`; each source once |
| 5. QA | Text placement; open in CapCut and check sections, text sizes, music envelope, animations (no ⚠); export 1080p; smoothness; black frames; master | `textcheck.py`, `smoothness.py`, `master.py --copy-video`; `references/capcut-gui.md`, `qa-checklist.md` | Every checklist item passed or reported |
| 6. Hand-over | Package the zip; install test under another name from a Unicode path; send a < 30 MB preview; client message | `Project.package()`; `references/capcut-handover.md` | Zip installs and opens complete |
| 7. Learn | Add any new mistake or client edit to `lessons-learned.md` / `client-taste.md`; update project memory | — | Skill updated |

Revisions: change `build.py`, re-run it, re-export. Never patch a draft by hand in JSON after CapCut has opened it.

## Scripts (`scripts/`, Python 3.10, run with `PYTHONIOENCODING=utf-8`, not `python -I`)
| Script | Purpose |
|---|---|
| `capcut_kit.py` | Library: `Project` (tracks, video, text, music, audio, sfx, effect, keys, save, package). CLI: `--selftest`, `--fonts` (which CapCut fonts cover Vietnamese / Cyrillic), `--free` (elements pycapcut marks free). |
| `capcut_install/` | `CAI_DAT_PROJECT.bat` + `cai_dat_project.ps1` + `HUONG_DAN.txt` template, shipped inside every client zip. |
| `capcut_front.ps1` | Restore and maximise the CapCut window (it starts minimised); notes on closing stuck Pro popups. |
| `probe.py` | Inventory: duration, size, rotation, fps, VFR, HDR, audio streams; warnings. |
| `contact_sheet.py` | Labelled frame grid (`--every 1`, `--safe` overlay). |
| `crop_sheet.py` | Eye / face crops over a time range at 0.1 s to choose freeze frames. |
| `grade_lut.py` | Per-clip LUT grade → CFR proxies; `--keep-sat`, `--audio clean`, `--sheet`. |
| `slowmo.py` | 4× motion-interpolated slow-motion source. |
| `cutout.py` | Person cut-out sticker (rembg) for pop-outs. |
| `sfx_gen.py` | Licence-free synthesised SFX kit. |
| `music_check.py` | Tempo, beat grid, drops, section changes, loopiness, `--lyrics`. |
| `lang_id.py` | Language per speech stretch + transcript; flags hallucinations. |
| `score_text.py` | Score candidate transcripts against the audio (forced alignment). |
| `textcheck.py` | Text boxes vs people (rembg) and vs each other; sheet + suggestions. |
| `smoothness.py` | Repeated-frame / cadence stutter per shot of a render. |
| `master.py` | −14 LUFS master; `--copy-video` for CapCut exports; `--preview` 720p. |

`templates/build_template.py`: the CapCut-first build skeleton (styles for stickers, chapter tags, subtitles, formal lines,
display type; source-once and length asserts; writes the draft, `CUT_PLAN.md`, `qa/boxes.json`, the client zip).
Requirements: `scripts/requirements.txt` + ffmpeg + CapCut desktop (tested 9.8).

## References
| File | When |
|---|---|
| `lessons-learned.md` | Always, before planning |
| `client-taste.md` | Planning and design decisions |
| `intake.md` | Start of every project |
| `house-style.md` | Colours, fonts, components with positions |
| `story-pacing.md` | Structure, hook, voice-over placement, music structure |
| `footage-qa.md` | Shot choice, speed, freeze frames, text placement, colour |
| `audio.md` | Music choice and licence, levels, voice clean-up, SFX, mastering |
| `speech-subtitles.md` | Languages, transcription, translation policy, subtitle style |
| `capcut-pipeline.md` | pycapcut units, text sizing, free vs Pro, masks, effects |
| `capcut-handover.md` | Zip, installer, client test, client message |
| `capcut-gui.md` | Opening, checking and exporting in CapCut with computer-use |
| `remotion-layers.md` | Graphics CapCut cannot build, as transparent layers |
| `tools-and-mcp.md` | Free tools and CapCut MCP servers: what to use and why |
| `qa-checklist.md` | Before every delivery |

## Working with this user
- They write in Vietnamese or English; answer in the language of their message. Client-facing text is Vietnamese.
- They judge by watching on a phone: send the 720p preview with SendUserFile; masters stay on the PC.
- They forward client feedback verbatim (docx, chat). Treat every point as a checklist item and answer point by point.
- They pick music well by ear: offer candidates, let them choose, then verify numerically.
- Ask before spending credits (Higgsfield) or installing new tools; ask before controlling CapCut (explain why).
- Reports: what changed, measured numbers, what was not verified. No hedging on what was verified.
