# Story structure and pacing

## Default lengths
≤ 60 s for Reels / TikTok unless the brief says more. Build in blocks so a 75 s cut can drop to 60 s by removing a block,
not by squeezing every shot.

## Energetic recap (field trip, event, campus day): approved Mỹ Tho shape
| Time | Block | Content |
|---|---|---|
| 0–3 s | **Sound hook** | The best real-sound brand moment (chant "S-I-U!", "I love SIU!", a cheer) over a 2×2 grid or the big group shot. Kinetic words in sync. |
| 3–11 s | Montage | 5–7 different moments, ~1 s each (first 1.5 s), cut on beats, 2–3 one-beat accents, riser into the title. Use sources not needed later. |
| 11–15 s | Title | Rings + one word mark ("MỸ THO"), zoom through the letters into the journey. |
| 15–20 s | Journey | Arrival shots, a sticker ("Lên thuyền thôi!"). Voice-over starts here on a calm, scenic shot. |
| 20–50 s | Chapters | 01 / 02 / 03 tags, stickers, split screen, grid, a label for the learning angle, one pop-out freeze. Footage illustrates each phrase of the VO. |
| 50–60 s | Peak + out | Games / fun at the music's biggest section change, slow-mo splash, then the official outro or a short group moment. |

Pacing: shots of 3–5 beats (1.5–2.5 s) in the body; 1-beat flashes only as accents; nothing at non-integer speed.
The brief's suggested blocks (opening → explore → culture → fun → end) are a menu: reorder for the strongest first 3 s.

## Formal speaker video: approved tiếng Nga shape
| Time | Block | Content |
|---|---|---|
| 0–2 s | Cold open | His most striking line in the foreign language (big italic type, no translation yet). |
| 2–5 s | Title card | Cream sheet with both institutions' emblems, statement + hook word ("bằng TIẾNG NGA…"), his face still visible below. |
| 5–10 s | Who | Lower third (low and wide) as the speech starts. |
| 10–40 s | Speech | Only the passages that serve the promise; cut asides, false starts and long pauses (cut on pauses, ~0.15 s air). Alternate wide / mid (1.2×) / close (1.38×) punch-ins centred on his face; slow 7 % push-in on emphasis. |
| 40–50 s | Context | Audience B-roll if the client has it (reactions, Q&A, raised hands, the wide stage shot with the school banner). |
| 50–60 s | Out | His closing wish, applause, official outro. |

## Voice-over placement (client feedback #7 on Mỹ Tho)
- Start after the intro and a few journey shots, on a calm or scenic shot, never on someone talking on camera.
- Play it uncut (never edit the student's words). Footage illustrates what each phrase says.
- Duck the music before it (~1 s dip), hold the duck through the whole VO (no pumping in pauses), swell back into the
  next section right after it (≥ 0.7 s gap). Cut 0.3 s after the last word (breaths).
- Ask whether a newer VO exists before building (the client replaced ours with a scripted re-recording).

## Music structure
- Start the track on a downbeat; land the big moment (games, chant) on the track's biggest section change
  (`music_check.py` prints them); end on a phrase boundary with a 1.5 s fade.
- A track may be spliced on a downbeat a whole number of bars apart (tiếng Nga reel: two pieces of After Sunset 4 bars
  apart) so the loud part covers both the title card and the ending.
- Every cut on a beat in recaps; speech videos cut on speech pauses, not beats.

## Hook checklist (first 3 s)
- Real sound (voice, chant, laugh) rather than music alone.
- A face or many faces, looking at camera or reacting.
- Something only this event has (not a generic establishing shot).
- On-screen text ≤ 4 words, or none.
