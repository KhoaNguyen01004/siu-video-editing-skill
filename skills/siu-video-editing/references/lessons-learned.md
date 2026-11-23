# Lessons learned: every mistake so far, why it happened, and the rule it produced

Sources: Mỹ Tho field-trip reel v1 → v4 (2026-11-21/22), "lời chúc bằng tiếng Nga" reel v1 → v7 (2026-11-23), the
**client-approved versions of both** (studied 2026-11-24), and the three session transcripts. Each rule names the check that
enforces it. Read this before planning; re-read the matching section before each phase.

## A. Creative direction

| # | What happened | Root cause | Rule (check) |
|---|---|---|---|
| A1 | v1: six font styles, template stickers, a home-made music loop. User: "clean, never template-heavy". | Decorating instead of designing. | One palette, 2–3 font families, every graphic has a job. |
| A2 | v2 obeyed "clean" literally (2 text styles, hard cuts, no effects). User: **"looks exactly like a slide show… where is the creativity"**. | Read a style note as a ban on energy. | "Clean" = cohesive and polished, never plain. SIU recaps always get motion graphics, stickers, a transition vocabulary, VFX moments and a full SFX layer. |
| A3 | v3 got the energy right ("cứ thế mà phát huy") but felt **rushed: "mấy frame đầu lướt qua quá nhanh"**. | 1-beat (0.5 s) shots in the opening. | Shots of 3–5 beats (1.5–2.5 s). First shot ≥ 1.5 s so the eye lands. 1-beat flashes are rare accents only. |
| A4 | v4 feedback: the intro "needs a fast montage of many different moments **before** the title, not entering the title abruptly". | The title came too early. | Hook montage (~1 s shots, first one 1.5 s, 2–3 one-beat accents, a riser), then the title. |
| A5 | Approved Mỹ Tho: the client **moved the "S-I-U! / I love SIU!" chant (our 63–72 s) to the first 7 s**, over our 2×2 grid, then the big group shot, and only then the title (11.6 s). | We saved the strongest brand moment for the end; viewers drop before it. | Put the money shot (real chant, group cheer, the most emotional moment) in the first 3 s. See client-taste.md. |
| A6 | Approved tiếng Nga: client removed our decorative Russian words (they sat on the backdrop's "SIU BEYOND TOMORROW" branding under a dark shade), the duplicate opening subtitle, his Vietnamese aside (our 11–18 s) and our end card. | Optional brief items ("có thể…") implemented at full volume; decoration placed over event signage; an aside kept that broke the "bằng TIẾNG NGA" promise. | Optional decoration = once, at the hook. Never over signage. Cut anything that does not serve the title's promise. (The client also added Q&A B-roll and the official outro: new material we never had; ask for it at intake.) |
| A7 | Both approved videos came back at ~60 s although the Mỹ Tho brief said 70–90 s and the feedback said 75 s. | Platform reality (Reels/TikTok ≤ 60 s plays best) beat the brief. | Default ≤ 60 s for reels; ask the max length and platform up front. Build so cutting to 60 s is easy (structure in blocks). |
| A8 | Approved title cards: the client replaced our typed "SIU × THPT ẤP BẮC" kicker with both schools' emblems, our black Montserrat Bold lines with navy serif (#2C3C82) and coloured the word SIU; on Mỹ Tho they cut the title to the "MỸ THO" word mark. | Too many families on one card (4); typed names where logos belong; small info lines nobody can read on a phone. | Formal card: serif + one display face, SIU navy, logos, brand word coloured. Recap title: one word mark. See client-taste.md. |

## B. Footage, framing and timing

| # | What happened | Root cause | Rule (check) |
|---|---|---|---|
| B1 | "Lag lag": slow-mo at 0.8× repeated 17 frames; 1.5× stepped 1-2-1-2. | Non-integer speeds on 30 fps footage. | Only 1× or exactly 2×. Slow motion only from `slowmo.py` (motion-interpolated). `smoothness.py` = 0 flagged. |
| B2 | Freeze frame "Giọng ca vàng" on closed eyes (client feedback #4); tiếng Nga hook still on a squinting smile; end hold on a boy looking down. User: **"đừng có bao giờ pause ngay lúc người đang có biểu mặt xấu, ví dụ như nhắm mắt"**. | Picked frames by timing, not by face; checked only the main subject. | The MAIN face of the shot (the speaker / the subject), at every moment the viewer can see a single frame or a stretched one: holds, stills, cover, both sides of every cut, transition windows, slow motion (footage-qa.md §4). Manual eye crops per frame; background faces need no check (user, 2026-11-24). |
| B8 | The first version of this skill only covered freezes and holds; cut points, transition windows and slow-motion blinks were unchecked (found in a self-audit, 2026-11-24). | The rule was written from the incident, not from where a bad face can appear. | Build script lists every such moment in `qa/face_points.json`; all pass before export. |
| B3 | Text over faces, over other text and over signs in the footage. | Fixed positions per graphic type. | `textcheck.py` = 0 failures, then look at the sheet (it misses signs, sees red lanterns as people). Move text to empty sky / roof / wall / tablecloth, shrink it, or move it to the next shot. |
| B4 | Same source used twice (v3). | Picking the best shot again for each section. | Each source once (a take continuing itself is fine); the montage uses sources not needed later. Assert it in the build script. |
| B5 | Heads clipped by source framing, a speaker blocking the shot, a stray hand (v2). | Trimmed by time only. | Contact sheet of the first and last frame of every shot before rendering. |
| B6 | Transitions out of special shots flashed black for a frame (v3). | Graphic layers ended a frame early. | `ffmpeg -vf blackdetect=d=0.03` on every render. |
| B7 | "Source có voice 3" had no audio track at all. | Assumed from the file name. | `probe.py` first: audio streams, rotation, HDR, VFR. |

## C. Colour

| # | What happened | Root cause | Rule (check) |
|---|---|---|---|
| C1 | v3 copied the official channel's flat look (saturation −23 %, blacks lifted to YLOW 68). Client: **"bợt, nhợt nhạt, thiếu sức sống"**, uneven between clips. | Matched someone else's numbers instead of the footage. | `grade_lut.py`: a LUT solved per clip toward one bright, clear, natural target; skin protected. Show a before/after sheet. |
| C2 | The tiếng Nga footage was already vivid (red table, blue curtain). | One target for all footage. | `--keep-sat` when a scene is already saturated; raise brightness and clarity only. |

## D. Sound

| # | What happened | Root cause | Rule (check) |
|---|---|---|---|
| D1 | Procedural music (v1) and "Fun Vibe" (v2) **"loop again and again"**. Fun Vibe: 73 % near-identical bars. | Chose by tempo and mood only. | `music_check.py`: reject > ~50 % repeats. The accepted "Circa 1983" scored 29 %. Let the user pick by ear when possible. |
| D2 | "Time of your life" had full sung lyrics about drinking. | Library tags said "no attribution", not "instrumental". | `music_check.py --lyrics`. |
| D3 | Teacher's speech through a PA speaker: user "cannot hear what the teacher is saying" at ~10 dB voice-over-music. | Recap ducking numbers used for a speech video. | Speech-led video: music about 20 dB under the voice, plus the voice clean chain (audio.md). Recap with VO: 11–15 dB. |
| D4 | In the CapCut project the music came back loud **while the student was talking** (rendered mp4 was fine). | CapCut reads keyframe times from the START OF THE MEDIA FILE; we wrote clip-relative times; the music started 53 s into the track. | `Project.kf_time()` (source time). Open the project and look at the volume envelope once. |
| D5 | Background music used from the YouTube Audio Library for a Facebook Reel. | Did not check the licence scope (research 2026-11-24: standard Audio Library licences are aimed at YouTube; CapCut "commercial" sounds cover TikTok/CapCut only). | Check every track's licence for the target platform; Facebook → Meta Sound Collection or a licence that names Facebook. See audio.md. |
| D6 | Claude cannot listen. | — | Measure instead (LUFS, voice-over-music dB, bar loudness) and say plainly what was not heard. |

## E. Speech, language and subtitles

| # | What happened | Root cause | Rule (check) |
|---|---|---|---|
| E1 | Brief said "keep the existing Vietnamese subtitles"; the footage had none. | Brief written from a different file. | Probe for burned-in subs on the first look; ask before translating. |
| E2 | We subtitled the teacher's Vietnamese as if it were Russian, until the user said **"thầy có nói tiếng việt nữa mà"**. | Whisper run for one language. | `lang_id.py` per pause-to-pause stretch (≥ 3 s) before any transcription. |
| E3 | The client's "transcript" was a machine translation of his Vietnamese INTO Russian. | Trusted the client text as Russian. | `score_text.py` scores every reading against the audio. |
| E4 | Our translation of unclear PA-audio Russian was **rewritten line by line** by the client: our ASR fragments "Rất, rất tốt, / rất khoẻ mạnh, / và thật tuyệt vời!" became "Tôi chúc các em có sức khỏe dồi dào / Luôn luôn xinh đẹp và vui vẻ!"; "Как я могу сказать вам?" was really "Как говорится" ("Như người ta đã nói"). They also left his Vietnamese speech unsubtitled. | ASR on reverberant speech, translated word by word. | Ask for the speaker's own text or an approved translation at intake. Translate meaning into natural Vietnamese for the occasion (a wish reads as a wish). Subtitle only the foreign language unless asked. Until approved: separate editable track + review table (BAN_DICH_CHO_DUYET.md); unclear stretches blank. |
| E5 | Whisper hallucinations: "Hãy subscribe cho kênh", "Субтитры создавал…", "Thank you.", "That's all I've got in my head" over music. An initial_prompt made it worse. | Whisper fills silence and music with training-set phrases. | VAD on, no initial_prompt, read timestamps; text that has nothing to do with the event is a hallucination. |
| E6 | Subtitles at y ≈ 1185 sat on the teacher's body; the client moved them to y ≈ 1660 on the plain red tablecloth and the lower third to y ≈ 1360–1480. | Followed the theoretical safe zone only. | A calm, uniform background area beats the textbook safe zone. Offer the low position (y 1550–1700) when the bottom of the frame is plain; keep 2 lines max. |

## F. CapCut project and hand-over

| # | What happened | Root cause | Rule (check) |
|---|---|---|---|
| F1 | The client "only saw raw footage" ("Nó k dô trong đây, mà chỉ có footage thô"). | Absolute media paths of this PC; no install step; the client imported `media/` into a new project. | `Project.package()` (token instead of paths) + the bundled installer. Test like a client: extract to a Unicode path, hide the original media, install under another name, open in CapCut. |
| F2 | Text intros lasted 0 µs in the delivered Mỹ Tho project. | `add_animation(intro, 0.4)` = 0.4 **µs**. | Durations are strings: `"0.4s"`. |
| F3 | Text 1/3 of the size, then overflowing the frame; words broken mid-word ("Giọng ca và / ng!"). | Guessed size factors; auto wrapping on. | `auto_wrapping=False`, measured K per font, width fitted with PIL on CapCut's own font file (`Project.text`). |
| F4 | A wrong "3.1 px per unit" rule made later text 1.6× too big. | One font's factor reused for all. | K is per font (capcut_kit.K); calibrate any new font (capcut-pipeline.md). |
| F5 | User: "tách các element ra giúp tôi, để tôi edit lại bớt chồng lên nhau". | Opening title shipped as one composite layer. | Every element on its own named track (title word, rings, pin, kicker, subtitle line…). Composite only what must stay locked together. |
| F6 | **The client published from the CapCut project, not from our render**: Remotion-only details (emoji icons, flying chapter icons, rays) never reached the public. | Render-first pipeline; CapCut was a second, weaker copy. | CapCut-first: the CapCut project IS the master and the MP4 is exported from it. What CapCut cannot do becomes a transparent graphics layer inside the project. |
| F7 | Text intro "Slide Up" (向上滑动) asked for Pro at export although pycapcut marks it free. | Metadata out of date. | Run the export's Pro check every time; replace Pro items with keyframes. The user's Pro had expired. |
| F8 | Transition "Up" (向上) on a pushed-down still drew a mirrored, stretched edge. | Transition reads outside the frame. | Use 叠化 (dissolve) under a sliding graphic for such moves. |
| F9 | Montserrat, Anton, Coiny, TikTok Display (and Poppins, Bebas Neue) have no Cyrillic; Poppins / Bebas Neue also miss Vietnamese marks. | Assumed font coverage. | `capcut_kit.py --fonts` after CapCut downloaded the fonts. |
| F10 | Images were scaled to fit the canvas. | CapCut fits any image to the canvas. | Overlay PNGs are full 1080×1920 with the element placed, so scale 1 = true size. |
| F11 | Keyframe/segment overlaps of 1 µs between slowed pieces. | Rounding up `target × speed`. | floor() source durations. |
| F12 | Transitions silently missing. | Attached after `add_segment`. | Attach to the clip BEFORE the cut, before adding it. |
| F13 | CapCut kept showing an old draft. | It was open while re-exporting. | Close the project and kill CapCut before writing a draft; back up a draft the user may have edited. |
| F14 | Sticker clips showed ⚠ "Animation" in CapCut 9.8 (found while verifying this skill; the Mỹ Tho v4 stickers had the same outro). | Text outro 缩小 "shrink" has no loadable resource in 9.8 although pycapcut lists it as free. | Use 渐隐 (verified). Open every new animation once in CapCut before using it in a delivery. |
| F15 | A music dip written as sparse breakpoints lost its "hold" points, so the dip ramped from 0 s (found in the kit's own test). | De-duplicating keyframes with equal values. | Write every breakpoint (`Project.music`), then look at the volume line in CapCut. |
| F16 | After CapCut opened a draft, it added a `Timelines/` folder (draft migration). | CapCut 9.x nested-timeline storage. | Regenerate the whole draft from build.py; never hand-patch the JSON of a draft CapCut has opened. |

## G. Machine and tooling

| # | What happened | Rule |
|---|---|---|
| G1 | The laptop shut down with three renders running; the half-written mp4 was corrupt. | One heavy job at a time (render, Whisper large, rembg batch). Remotion `--concurrency=6`. After a crash, decode-check every output: `ffmpeg -v error -i x -f null -`. |
| G2 | Chrome asks where to save each download, so agent-clicked downloads stall behind a native dialog. | Ask the user to download music / assets. |
| G3 | Higgsfield was "connected" but not visible; later it was, but it costs credits. | Check the tool list; ask before spending credits. |
| G4 | cp1252 console crashed on Vietnamese prints; rembg/librosa need user site-packages. | `PYTHONIOENCODING=utf-8`; run our scripts without `python -I`. |
| G5 | `ffmpeg drawtext` segfaults on this Windows build (no fontconfig). | Label frames with PIL (`contact_sheet.py`). |
| G6 | PowerShell 5.1 reads BOM-less UTF-8 as ANSI: Vietnamese strings in the installer turn to mojibake. | Write `.ps1` / `.txt` for clients as UTF-8 **with BOM**, CRLF. |
| G7 | Remotion: per-letter inline blocks broke words mid-line ("khám ph / á"); CSS `clip-path:url()` on a video canvas did nothing. | Group letters per word; use an SVG `<mask>` knockout for footage-in-letters. |
