# Sound: music, licence, ducking, voice, SFX, loudness

Claude cannot listen. Every audio decision is measured, and the report says what was not heard.

## 1. Choosing music
1. Ask the user to pick or download (their Chrome stalls agent downloads behind a Save-as dialog). Offer 3 candidates.
2. **Licence for the target platform first** (research 2026-11-24, re-check each time):
   - Facebook / Instagram Reels: Meta Sound Collection, or a track whose licence names Facebook/Instagram commercial use.
   - YouTube Audio Library standard tracks are cleared for YouTube; third-party guides say they are not cleared for other
     platforms. CC-BY tracks need the credit in the caption.
   - CapCut's in-app "commercial" sounds are cleared for TikTok / CapCut, not for Facebook.
   - Pixabay-style libraries: read the track's own licence; keep a screenshot of it in the project.
   - A university is an organisation posting branded content: treat it as commercial use.
3. `python scripts/music_check.py track.mp3 --lyrics`:
   - near-identical bar repeats > ~50 % → reject ("loops again and again"; accepted track scored 29 %);
   - any lyrics → reject (unless the brief wants a song);
   - note the drops (loudness jumps) and section changes: the edit's big moments go there.
4. Mood: recap = bright, clear beat, sections that change; speech = light, modern, not solemn.

## 2. Levels (measured targets)
| Situation | Music under voice | How |
|---|---|---|
| Recap with student VO | −13 to −15 dB (voice ~11 dB over music) | duck depth 0.78–0.82, hold through the whole VO |
| Short chants / on-camera voices in a recap | −13 dB (voice ~10 dB over) | per-frame envelope from the voice stem, 150 ms attack, 450 ms release |
| Speech-led video (PA speaker, reverb) | **about −20 dB** (voice ~20 dB over) | the user could not hear the teacher at 10 dB |
| No voice | music full, sections shaped by the edit | — |
| SFX under a VO | 55 % volume | — |

Measure voice-over-music by least-squares fitting the known music track out of the mix, or compare stems' RMS where the
voice plays.

## 3. Voice clean-up (PA / reverberant speech)
`highpass=f=100, lowpass=f=9000, afftdn=nr=12:nf=-38, equalizer=f=250:t=q:w=1:g=-3, equalizer=f=3000:t=q:w=1.2:g=4,
acompressor=threshold=-24dB:ratio=2.5:attack=10:release=150:makeup=2, loudnorm=I=-16:TP=-1.5:LRA=11`
(`grade_lut.py --audio clean` applies it while grading, so picture and voice stay one file and CapCut cuts stay in sync.)

## 4. Source sound
- Mute every clip by default (`Project.video(..., vol=0)`). Unmute only the clips the brief names ("Source có voice N")
  and check they have an audio stream.
- Use the real sound of chants and cheers; it is the best hook material.

## 5. SFX
- `python scripts/sfx_gen.py sfx/`: synthesised, licence-free whoosh, swish, riser, impact, glitch, pop, bubble, shutter,
  sparkle, tick + contextual bee, sizzle, splash, horn, ka-ching, heart.
- Recap: a cue on every transition and graphic (whoosh 0.2–0.3 s before a cut, pop on a sticker, shutter on a freeze,
  riser into the title, impact on the title). Formal: sparse.
- In CapCut, spread SFX over several tracks (`Project.sfx` opens "SFX n" tracks as needed).

## 6. Mastering and checks
- `python scripts/master.py in.mp4 out.mp4 [--copy-video] [--preview p.mp4]`: −14 LUFS integrated, true peak ≈ −1.5 dBTP.
  `--copy-video` for a CapCut export (audio only, picture untouched).
- Look at the CapCut project's music volume envelope once (keyframes are in source time; lesson D4).
- An audio-only fix does not need a video re-render: render audio, remux with `-c:v copy`.
- Report: integrated LUFS, true peak, voice-over-music dB, and "not listened to".
