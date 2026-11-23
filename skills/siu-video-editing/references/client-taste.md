# Client taste: what the SIU client changed in the approved versions, and why

The strongest evidence we have. In both projects the client opened **our CapCut project**, edited it, and exported the
version they approved. Studied 2026-11-24, frame by frame and by aligning the soundtracks (MFCC matching) against our
exports, with every text element's position, font, size and colour read from our `draft_content.json`.
Files: Mỹ Tho `Download.mp4` (60.1 s, 1080×1920), tiếng Nga export (59.0 s, 720×1280).

Three kinds of difference. Do not confuse them:
- **Design choices:** the client changed something we gave them. This is their taste; follow it by default.
- **New material:** things only the client had (a new voice-over script, event B-roll, the official outro). Not our
  mistake, but ask for such material at intake next time (intake.md).
- **Our pipeline gaps:** things in our Remotion render that never existed in the CapCut project, so they never reached the
  client (emoji icons on stickers, the "CHẶNG" kicker and flying icon of chapter cards, rings masked behind letters).
  They were not removed by the client. Lesson F6: build CapCut-first.

---

## 1. Lời chúc bằng tiếng Nga (speaker video)

Audio alignment: client 0–11 s = our 0–11 s exactly; then they cut our 11.0–18.1 s and two short pauses (19.6–21.9 s,
23.0–24.6 s); client 16–39.5 s = our 25.1–48.6 s unchanged; client 40–48 s = new B-roll with the title-card music;
client 48.5–52 s = our ending (mic handed over, applause); client 52.5–59 s = official SIU logo outro.

| Element | Ours (exact, from the draft) | Client | Why (evidence) | Rule |
|---|---|---|---|---|
| **Speech cut** | Kept his Vietnamese passage "Hôm nay rất là sung sướng, tất cả các em đang ở trên mảnh đất này…" (11–18 s) | **Removed** | The video's promise is "lời chúc bằng TIẾNG NGA". A Vietnamese aside in the first 20 s breaks the promise, and our transcription of it was unsure. | Cut everything that does not serve the title's promise, especially in the first 20 s. |
| **Subtitles, content** | Our word-for-word translation of ASR fragments: "Rất, rất tốt, / rất khoẻ mạnh, / và thật tuyệt vời!", "Biết nói sao với các em đây?" | **Rewritten as natural Vietnamese wishes**: "Như người ta đã nói", "Trước khi chúng ta tạm biệt nhau", "Tôi chúc các em có sức khỏe dồi dào", "Luôn luôn xinh đẹp và vui vẻ!" | They know what he meant ("очень здоров… прекрасн…" = a wish for health and beauty; "Как говорится" = "as they say"). Fragments read like a robot. | Translate the meaning into the natural Vietnamese register of the occasion (lời chúc), never ASR fragments. Get their text first. |
| **Subtitles, coverage** | Subtitled his closing Vietnamese wish word for word; ~7 short gaps | **No subtitle** over Vietnamese speech; a ~12 s stretch left blank | Vietnamese viewers understand him; a subtitle there adds noise. Blank beats wrong. | Subtitle the foreign language only, unless the brief asks for full captions. |
| **Subtitles, position** | y = 1185 (his chest and gesturing hands) | **y ≈ 1665**, on the plain red tablecloth | Our line sat on his hands and microphone, a busy background. The tablecloth is calm and uniform. | Put subtitles on the calmest band below the subject, even inside the textbook UI zone (keep ≥ 220 px from the bottom edge). |
| **Subtitles, style** | TikTok Display Medium, white, black stroke, yellow keyword | **Same font, size and colour**; keywords highlighted more sparingly | Style was right. | Keep this subtitle style. ≤ 1 highlighted keyword per line. |
| **Decorative Russian words** | Playfair Italic cream at y 360–390 with a dark top shade, 4 times ("Сегодня я очень рад", "очень-очень…") | **Removed**, except the cold-open line "Дорогие мои ученики!" | They sat on the event backdrop's **"SIU BEYOND TOMORROW"** branding and the school logos, darkened a third of the frame, and doubled the reading load next to the subtitles (two languages at once). | Never put decoration over event or brand signage. Optional decoration = once, at the hook. |
| **Cold open** | "Дорогие мои ученики!" + Vietnamese subtitle "Các em học sinh thân mến!" | Russian line only | A translation under the Russian kills the surprise. | Let the hook stay foreign for a beat. |
| **Title card, top** | Text kicker "SIU × THPT ẤP BẮC" (Prata, crimson) | **Both schools' real emblems + official names** in navy | A partner event must show both institutions officially; logos read instantly and look official. | Use the real logos (ask for them). Never type a school name where its logo belongs. |
| **Title card, type** | Line 1–2 Montserrat Bold, near-black ink | **Navy-blue serif** (#2C3C82, the SIU emblem blue); "SIU" bold red (#B71E26) | Four families on one card (Prata, Montserrat, Playfair, Anton) became two (a serif + Anton), matching the italic "bằng". The brand word gets the colour. Navy ties the card to the logos. | Formal cards: serif + one display face. Brand word highlighted. Use SIU navy for formal text. |
| **Title card, layout** | Text block centred lower (y 335–805); cream sheet to ~y 930 | Block moved up (y ≈ 120–700); sheet ends at ~y 810 with a crimson rule | The teacher's face shows under the card. A tighter block reads as one unit. | Keep the speaker's face visible during a title card. |
| **Lower third** | Crimson name bar at y 995 (x 70–850), cream role bar at 1082, Montserrat Bold | **Same design, wider (x ≈ 24–954), lower (y ≈ 1360 / 1480), lighter name weight** | At 995 it covered his chest and hands; lower it sits at the table edge, bigger for phones. | Lower thirds go low (y 1300–1500), wide and big; never over the speaker's gestures. |
| **Ending** | Slow-mo applause + card "MỘT LỜI CHÚC ĐẶC BIỆT / GỬI ĐẾN HỌC SINH THPT ẤP BẮC" | Q&A B-roll (new material), our applause shot, **official SIU animated logo outro** | The client ends every video on the official sting; our card repeated the title. | End on the official outro when the client has one; a text end card only if asked. |
| Framing, punch-ins, cuts on pauses, music under speech | — | Kept | Worked. | Keep. |

## 2. Mỹ Tho field trip (energetic recap)

Audio alignment: client 0–7.5 s = our 63–72 s (the "S-I-U!" / "I love SIU!" chant section); client 8–11.5 s = our games
section; title at 11.6 s; client ~17–57 s = our 12.6–54.5 s middle in the same order (+2.5 to +4.6 s); the file stops
at 60.1 s with music at full level (looks truncated by the export / download; do not read it as "drop the ending").
Music re-laid as one continuous piece of Circa 1983 from 35.5 s of the track (ours started at 49.0 s).
**New material:** a new, scripted student voice-over (the user confirmed: "the client use different voice") that opens
with "Đối với sinh viên ngành quản trị kinh doanh chúng em, chuyến đi thực tế tại Mỹ Tho, Đồng Tháp…".

| Element | Ours (CapCut project) | Client | Why | Rule |
|---|---|---|---|---|
| **Hook** | 9-shot montage (splash, mud pond, fan spin, boat friends…), title at 8.2 s; chant at the end | **Chant audio first**: "S-I-U! / I love SIU!" over our **2×2 grid** of four moments, then the big group shot (no text), boat friends, e-cart, games, title at 11.6 s | The real chant is the strongest sound-on hook and pure brand; the grid shows four moments in one frame. Our best moment was buried at 63 s where most viewers never arrive. | Open with the best real sound moment + a multi-moment visual. Never save the chant/cheer for the end. |
| **"I love SIU" words** | White "I", "love" with crimson stroke, yellow "SIU!", at y 500 over the group | Moved to the empty lower grid panels (y ≈ 1050); **"SIU" recoloured crimson with a white outline, "!" dropped**; "I love" yellow | Brand word in brand colour; text placed where the frame is empty. | The brand name SIU is always crimson (or navy on formal cards). |
| **Big S-I-U letters + hearts** | Three 70-size letters popping on the beat + hearts confetti | Removed | Too much on one chant; the grid already carries the energy. | One text treatment per moment. |
| **Title** | Rings + "MỸ THO" (footage in letters) + "HỌC TẬP THỰC TẾ" kicker (y 420) + pin + "Đồng Tháp" (y 1150) + "SIUers · Ngành QTKD" (y 1218, size 6.8 ≈ 35 px) | **Rings + "MỸ THO" only** | The unmasked rings drew over the kicker and letters in CapCut (user: "tách các element… bớt chồng lên nhau"); the small lines were unreadable on a phone; the new voice-over now says the faculty and place. | A title = one word mark. Faculty / place go in the voice-over, the caption or one big line, not three small ones. |
| Stickers ("Lên thuyền thôi!", "Không sợ ong!", "Ngọt lịm!", "Tự tay làm!", "Ngon xỉu!", "Giọng ca vàng!"), chapter tags 01–04, "Tìm hiểu mô hình kinh doanh" label, split-screen trio, 2×2 grid, pop-out freeze | Coiny, white/green or yellow/crimson outlines, positions per shot | **Kept: same positions, sizes and colours** (measured) | They work. | Keep this vocabulary for recaps. |
| Middle order (journey → honey farm → coconut candy → đờn ca tài tử → games) | — | Kept, ~2 s trimmed late in the edit | — | Keep the chaptered journey structure. |
| Length | 74.1 s | 60 s | Platform length. | ≤ 60 s by default. |

## 3. Standing preferences (default unless the brief says otherwise)

1. **≤ 60 s.**
2. **First 3 s:** the strongest real-sound brand moment (chant, cheer, greeting) + a picture with many faces / moments.
3. **Every second serves the title's promise.** Cut asides, even good ones.
4. **Official assets** (school emblems, partner logos, the animated SIU outro) instead of typed names or home-made stings.
5. **Few, big text elements on calm areas.** Never on faces, gesturing hands, other text, or event/brand signage.
6. **Brand colour on the brand word:** SIU in crimson; formal text in SIU navy #2C3C82; cream #F0E9D4 paper.
7. **Formal speaker videos:** serif + one condensed display face, restrained motion, lower third low and wide,
   subtitles low on a plain band, foreign language only. **Energetic recaps:** Coiny stickers, chapter tags, split screens,
   grids, pop-outs, SFX.
8. **Subtitles say what the speaker meant, in natural Vietnamese**, from the client's text; blank beats wrong.
9. **The CapCut project is the product.** It must look finished on its own; render-only details do not exist for the client.
