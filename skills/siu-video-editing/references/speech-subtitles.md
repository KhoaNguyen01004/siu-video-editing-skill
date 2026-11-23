# Speech, languages and subtitles

## Policy (from the approved tiếng Nga reel)
1. **The client's text wins.** Ask at intake for the speaker's script, notes, or an approved translation. Brief rule:
   "không tự dịch lại, không thay đổi câu chữ, không tự tạo thêm nội dung".
2. **Translate meaning, not fragments.** A wish reads as a natural Vietnamese wish ("Tôi chúc các em có sức khỏe dồi dào,
   luôn luôn xinh đẹp và vui vẻ!"), not ASR pieces ("Rất, rất tốt, / rất khoẻ mạnh, / và thật tuyệt vời!").
3. **Subtitle the foreign language only** unless the brief asks for full captions; Vietnamese speech to a Vietnamese
   audience was left unsubtitled by the client.
4. **Blank beats wrong.** Unclear stretch = no subtitle, listed in the review table.
5. **Until approved**, subtitles live on their own CapCut track named "Phụ đề (CHỜ DUYỆT)" and the zip carries
   `BAN_DICH_CHO_DUYET.md`: time, what was heard, the subtitle used, confidence, and the gaps.

## Pipeline
1. **Which language where:** `python scripts/lang_id.py clip.mp4 --langs vi,ru,en --json qa/lang.json`.
   Stretches between pauses, merged to ≥ 3 s and capped at 8 s. A speaker can switch languages mid-speech.
2. **Transcribe each stretch in its own language** (faster-whisper large-v3, `vad_filter=True`, no `initial_prompt`,
   `condition_on_previous_text=False`, beam 5). Run 2–4 passes (raw, denoised, per phrase); keep only readings the passes
   agree on.
3. **Score readings against the audio:** `python scripts/score_text.py clip.mp4 ru cands.json`. Near 0 = fits; below
   about −2 = does not. Use it on a client's transcript too: theirs may be a machine translation (the tiếng Nga client's
   "Russian" text was his Vietnamese machine-translated into Russian).
4. **Hallucination check:** delete lines like "Hãy subscribe cho kênh…", "Субтитры создавал…", "Продолжение следует",
   "Thank you.", "Hẹn gặp lại các bạn" and anything that has nothing to do with the event; they appear over music, applause
   and silence. `lang_id.py` flags the common ones.
5. Short voice clips (chants): caption only what is certain ("I love SIU!", "S-I-U!"); unclear middle words = no caption.

## Subtitle style (approved)
- TikTok Display Medium (`FontType.Classic`), white, black outline, ~66 px, ≤ 2 lines, line breaks by hand at phrase
  boundaries, `auto_wrapping=False`.
- ≤ 1 yellow keyword per line (e.g. "rất vui").
- Position: the calmest band under the subject (approved y ≈ 1665 on the tablecloth). Never on the face, hands or mic.
- Timing: in at the first syllable, out 0.15 s after the last (never overlapping the next line on the track).
- Foreign decorative type (e.g. Russian words): once, at the cold open, never over signage; not at the same time as a
  subtitle.

## Names and titles
Copy exact spellings and titles from the brief ("PGS.TS. HOÀNG VĂN VIỆT", "Trưởng khoa Khoa học xã hội (SIU)"); never
re-case or abbreviate. "Việt" vs "Viết": diacritics matter; normalise all text to NFC (`capcut_kit.nfc`).
