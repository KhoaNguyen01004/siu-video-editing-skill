# SIU Video Editing — Skill dựng video SIU cho Claude

Bộ "kỹ năng" (skill) giúp trợ lý AI **Claude** tự dựng video cho **Trường Đại học Quốc tế Sài Gòn (SIU)** theo đúng
phong cách khách hàng đã duyệt, rồi giao cho bạn:

- **Video thành phẩm** (MP4, dọc 9:16 cho Facebook Reels / TikTok, có thể thêm bản ngang 16:9 để chiếu máy tính).
- **Project CapCut** đầy đủ từng lớp (footage, chữ, sticker, nhạc, voice, hiệu ứng…) để khách **tự mở và chỉnh sửa**.
- **File cài project cho khách** (bấm đúp là xong) và **bản xem trước nhẹ** để xem trên điện thoại.

> Tài liệu này viết cho người **không rành kỹ thuật**. Bạn chỉ cần làm theo từng bước, không cần biết lập trình.

---

## Mục lục

1. [Skill này là gì?](#1-skill-này-là-gì)
2. [Bạn cần chuẩn bị gì?](#2-bạn-cần-chuẩn-bị-gì)
3. [Cài đặt (chọn 1 trong 3 cách)](#3-cài-đặt-chọn-1-trong-3-cách)
4. [Dựng video đầu tiên: từng bước](#4-dựng-video-đầu-tiên-từng-bước)
5. [Ví dụ sử dụng (câu lệnh mẫu)](#5-ví-dụ-sử-dụng-câu-lệnh-mẫu)
6. [Khách hàng nhận gì và mở project thế nào?](#6-khách-hàng-nhận-gì-và-mở-project-thế-nào)
7. [Những điều cần biết](#7-những-điều-cần-biết)
8. [Câu hỏi thường gặp và cách xử lý lỗi](#8-câu-hỏi-thường-gặp-và-cách-xử-lý-lỗi)
9. [Bên trong skill có gì?](#9-bên-trong-skill-có-gì)
10. [Tác giả](#10-tác-giả)

---

## 1. Skill này là gì?

Một vài khái niệm, giải thích thật đơn giản:

| Từ | Nghĩa là |
|---|---|
| **Claude** | Trợ lý AI của công ty Anthropic, trò chuyện bằng tiếng Việt được. |
| **Claude Code** | Một chế độ trong ứng dụng Claude cho phép Claude **làm việc trực tiếp với file trên máy tính của bạn**: xem video, chạy công cụ, tạo project CapCut. |
| **Skill** | Một bộ hướng dẫn + công cụ "dạy nghề" cho Claude. Khi bạn nhờ dựng video SIU, Claude tự mở skill này ra và làm theo. |
| **CapCut** | Phần mềm dựng video miễn phí (của ByteDance, cùng công ty với TikTok). |
| **Project CapCut** | File dự án dựng dở của CapCut: mở ra là thấy từng đoạn video, từng dòng chữ, nhạc… để sửa tiếp. |
| **Footage** | Các đoạn video gốc quay từ điện thoại / máy quay. |

Skill này được đúc kết từ **2 video thật đã được khách duyệt** (video học tập thực tế ở Mỹ Tho và video thầy gửi lời chúc
bằng tiếng Nga), qua nhiều lần sửa theo góp ý của khách. Mọi lỗi từng mắc (nhạc lặp, video bị giật, màu nhợt, chữ che
mặt, dừng hình đúng lúc nhắm mắt, phụ đề dịch sai, project gửi khách không mở được…) đều đã được ghi lại để Claude
**không lặp lại**.

---

## 2. Bạn cần chuẩn bị gì?

| Cần có | Ghi chú |
|---|---|
| Máy tính **Windows 10 hoặc 11** | Các công cụ trong skill chỉ chạy trên Windows. |
| Tài khoản **Claude gói trả phí** (Pro trở lên) | Claude Code chỉ có ở gói trả phí. Đăng ký tại [claude.ai](https://claude.ai). |
| **Ứng dụng Claude cho máy tính** | Tải tại [claude.ai/download](https://claude.ai/download), cài và đăng nhập. |
| **CapCut cho máy tính** | Tải tại [capcut.com](https://www.capcut.com/), bản miễn phí là đủ. Mở CapCut **một lần** cho nó tạo thư mục dự án, rồi tắt. |
| **Internet** | Để tải công cụ, font và hiệu ứng của CapCut. |
| **Ổ đĩa trống khoảng 10 GB** | Công cụ nhận dạng giọng nói (~3 GB), thư viện (~0,5 GB) và các file video. |
| Python, FFmpeg | **Không cần tự cài.** Bộ cài (cách 2) hoặc Claude (cách 1) sẽ cài giúp. |

---

## 3. Cài đặt (chọn 1 trong 3 cách)

Chỉ cần làm **một** trong ba cách. Người mới nên dùng **Cách 1** hoặc **Cách 2**.

### Cách 1: Nhờ Claude cài giúp (dễ nhất)

1. Mở ứng dụng **Claude** trên máy tính.
2. Chọn mục **Code** (chế độ Claude Code).
3. Khi được hỏi thư mục làm việc, chọn một thư mục bất kỳ, ví dụ **Desktop**.
4. Bấm vào ô chat, **dán nguyên đoạn dưới đây** rồi nhấn Enter:

   ```text
   Hãy cài skill "siu-video-editing" cho tôi từ https://github.com/KhoaNguyen01004/siu-video-editing-skill :
   1. Tải repo về máy (git clone hoặc tải file zip).
   2. Chép thư mục skills/siu-video-editing vào %USERPROFILE%\.claude\skills\ (nếu đã có bản cũ thì chuyển bản cũ sang %USERPROFILE%\.claude\skills_backup\).
   3. Kiểm tra máy đã có Python 3.10 trở lên và FFmpeg chưa; nếu chưa thì cài bằng winget (Python.Python.3.12 và Gyan.FFmpeg).
   4. Cài thư viện: python -m pip install -r scripts/requirements.txt (trong thư mục skill vừa chép).
   5. Chạy python scripts/capcut_kit.py --selftest và báo kết quả cho tôi bằng tiếng Việt.
   ```

5. Claude sẽ **hỏi xin phép** trước khi chạy lệnh hoặc cài phần mềm. Đọc qua rồi bấm **Allow / Cho phép**.
6. Khi Claude báo **"selftest ok"** là xong. Đóng phiên chat này và **mở một phiên mới** để skill có hiệu lực.

### Cách 2: Tải về và bấm đúp file cài đặt

1. Bấm vào link này để tải: **[siu-video-editing-skill.zip](https://github.com/KhoaNguyen01004/siu-video-editing-skill/releases/latest/download/siu-video-editing-skill.zip)**
2. Mở thư mục **Downloads** (Tải xuống), **chuột phải** vào file `siu-video-editing-skill.zip` → **Extract All… (Giải nén tất cả)** → **Extract**.
3. Mở thư mục vừa giải nén, **bấm đúp** vào file **`CAI_DAT_SKILL.bat`**.
4. Nếu Windows hiện khung xanh **"Windows protected your PC"**: bấm **More info** → **Run anyway**.
   (File này chỉ chép skill vào máy và hỏi bạn trước khi cài Python / FFmpeg.)
5. Cửa sổ đen sẽ hỏi vài câu. Gõ **C** (có) hoặc **K** (không) rồi nhấn **Enter**:
   - "Cài Python 3.12?" → **C** (nếu máy chưa có)
   - "Cài FFmpeg?" → **C** (nếu máy chưa có)
   - "Cài các thư viện Python?" → **C** (mất 5–10 phút, cần mạng)
6. Khi thấy chữ **XONG!**, nhấn **Enter** để đóng cửa sổ.
7. Mở ứng dụng Claude → mục **Code** → bắt đầu **phiên mới**.

> Nếu cửa sổ báo đã cài Python nhưng bước thư viện vẫn lỗi: đóng cửa sổ, bấm đúp lại `CAI_DAT_SKILL.bat` lần nữa
> (Windows cần mở cửa sổ mới mới "thấy" Python vừa cài).

### Cách 3: Dành cho người quen dùng dòng lệnh (plugin)

Mở cửa sổ dòng lệnh (Terminal) và chạy:

```powershell
claude plugin marketplace add KhoaNguyen01004/siu-video-editing-skill
```

```powershell
claude plugin install siu-video-editing@siu-video
```

Sau đó nhờ Claude cài Python, FFmpeg và thư viện như bước 3–5 của Cách 1. Cập nhật về sau: `claude plugin update siu-video-editing@siu-video`.

### Kiểm tra đã cài thành công chưa

Trong một **phiên mới** của Claude Code, gõ:

```text
Bạn có skill siu-video-editing không? Tóm tắt giúp tôi skill đó làm được gì.
```

Nếu Claude trả lời đúng về skill (dựng video SIU, xuất project CapCut…) là đã cài thành công.

---

## 4. Dựng video đầu tiên: từng bước

**Bước 1. Gom tài liệu vào một thư mục.**
Tạo thư mục mới, ví dụ `Video Mỹ Tho`, rồi chép vào đó:
- Toàn bộ **video gốc** (chép thẳng từ điện thoại / máy quay; **đừng** lấy bản đã gửi qua Zalo, Messenger vì bị nén mờ).
- File **voice** / phỏng vấn (nếu có).
- **Logo** SIU, logo đơn vị đối tác (file PNG nền trong), **đoạn logo động / outro** chính thức (nếu có).
- File **brief** (yêu cầu của khách) hoặc góp ý của khách (Word, PDF, hoặc chép chữ vào file .txt).

**Bước 2. Mở Claude Code tại thư mục đó.**
Mở ứng dụng Claude → mục **Code** → chọn thư mục `Video Mỹ Tho`.

**Bước 3. Gõ yêu cầu bằng tiếng Việt bình thường.** Xem các câu mẫu ở [mục 5](#5-ví-dụ-sử-dụng-câu-lệnh-mẫu).

**Bước 4. Trả lời các câu hỏi của Claude.**
Claude sẽ hỏi một lần những gì còn thiếu: đăng ở đâu (Reels / TikTok), dài tối đa bao nhiêu giây, có logo / outro
chính thức không, có bản dịch / lời phát biểu chính xác không, nhạc nền tự chọn hay để Claude đề xuất…
Không biết thì trả lời **"dùng mặc định"**.

**Bước 5. Duyệt kế hoạch dựng.**
Trước khi dựng, Claude đưa ra **kế hoạch từng cảnh** (file `CUT_PLAN.md`): cảnh nào, bao lâu, chữ gì, nhạc gì.
Đồng ý thì gõ "ok dựng đi", muốn đổi thì nói rõ chỗ cần đổi.

**Bước 6. Nhạc nền.**
Claude đề xuất vài bài **không lời**, kiểm tra bài có bị lặp đi lặp lại không và có dùng hợp lệ trên Facebook / TikTok
không. **Bạn tự tải bài nhạc** (trình duyệt sẽ hỏi chỗ lưu) và bỏ vào thư mục dự án.

**Bước 7. Claude dựng.**
Claude chỉnh màu từng clip, chọn khung hình đẹp (không nhắm mắt), thêm chữ / sticker / hiệu ứng, giảm nhạc khi có người
nói, rồi tạo **project CapCut**. Khi Claude **xin quyền điều khiển CapCut** (để mở project kiểm tra và xuất video):
bấm cho phép, và **đừng dùng CapCut** trong lúc Claude đang làm.

**Bước 8. Xem thử và góp ý.**
Claude gửi **bản xem trước 720p** (nhẹ, xem được trên điện thoại). **Hãy tự nghe** (Claude không nghe được âm thanh) và
góp ý: "đoạn đầu nhanh quá", "nhạc to quá chỗ thầy nói", "đổi chữ này"… Claude sửa và xuất lại.

**Bước 9. Gửi khách.**
Bạn nhận được trong thư mục `out/`:
- `…_9x16.mp4`: video đăng mạng xã hội.
- `…_CapCut.zip`: project CapCut cho khách (kèm file cài).
- Tin nhắn hướng dẫn khách (Claude soạn sẵn, chỉ cần copy gửi).

---

## 5. Ví dụ sử dụng (câu lệnh mẫu)

Copy câu mẫu, sửa lại tên / chi tiết cho đúng việc của bạn, rồi dán vào Claude Code.

### 5.1. Dựng video recap chuyến đi / sự kiện

```text
Dựng video recap chuyến học tập thực tế của sinh viên ngành Quản trị kinh doanh SIU tại Mỹ Tho.
Footage ở thư mục này, brief ở file VIDEO_EDIT_INSTRUCTIONS.md. Clip "Source có voice 1-4" giữ tiếng gốc,
các clip khác tắt tiếng. Đăng Facebook Reels, tối đa 60 giây. Xuất cả project CapCut để khách tự chỉnh.
```

**Claude sẽ:** mở đầu bằng khoảnh khắc sôi động nhất (ví dụ tiếng hô "I love SIU!"), dựng nhanh vài cảnh rồi hiện
tiêu đề, chia chương (01 Trại ong mật, 02 Lò kẹo dừa…), thêm sticker, chia đôi / chia 4 màn hình, hiệu ứng âm thanh,
nhạc nền giảm khi có voice, rồi xuất video + project CapCut.

### 5.2. Dựng video phát biểu / lời chúc (có tiếng nước ngoài)

```text
Dựng video Reel khoảng 60 giây: PGS.TS. Hoàng Văn Việt – Trưởng khoa Khoa học xã hội SIU gửi lời chúc đến học sinh
THPT Ấp Bắc bằng tiếng Nga. Phong cách sang trọng, có lower-third tên thầy, phụ đề tiếng Việt.
Đây là bản dịch thầy gửi: (dán bản dịch vào đây). Logo hai trường ở thư mục logo/.
```

**Claude sẽ:** nhận ra đoạn nào thầy nói tiếng Nga, đoạn nào nói tiếng Việt; chỉ làm phụ đề cho phần tiếng nước ngoài
(theo bản dịch bạn đưa, viết thành câu tiếng Việt tự nhiên); dùng logo thật của hai trường; đặt chữ ở vùng trống, không
che mặt hay tay thầy; nhạc nền thấp hơn giọng thầy khoảng 20 dB.

### 5.3. Sửa video theo góp ý của khách

```text
Khách gửi góp ý trong file feedback.docx. Sửa video theo từng ý, giữ nguyên những phần khách không nhắc tới,
rồi xuất lại video và project CapCut.
```

**Claude sẽ:** đọc từng ý, sửa đúng từng ý, và báo lại từng điểm đã sửa như thế nào.

### 5.4. Kiểm tra nhạc nền trước khi dùng

```text
Kiểm tra giúp tôi 3 bài nhạc trong thư mục music/: bài nào có lời, bài nào bị lặp đi lặp lại,
nhịp bao nhiêu, đoạn cao trào ở giây thứ mấy, và có dùng được trên Facebook Reels không.
```

### 5.5. Kiểm tra khung hình và chữ

```text
Kiểm tra video này: có chỗ nào dừng hình hoặc cắt cảnh đúng lúc người chính đang nhắm mắt / mặt xấu không,
và có dòng chữ nào che mặt, che tay hay che bảng hiệu không. Đề xuất cách sửa.
```

### 5.6. Làm thêm bản ngang 16:9 để chiếu

```text
Làm thêm bản ngang 16:9 của video này để chiếu trên máy chiếu hội trường, không cắt mất đầu người.
```

### 5.7. Làm phụ đề cho đoạn người nói

```text
Làm phụ đề tiếng Việt cho clip phỏng vấn này. Đoạn nào nghe không rõ thì để trống và liệt kê cho tôi,
đừng đoán.
```

### 5.8. Chỉ xin kế hoạch, chưa dựng

```text
Xem hết footage trong thư mục này và đề xuất kế hoạch dựng video recap 60 giây (cảnh nào, bao lâu, chữ gì),
chưa cần dựng.
```

> Muốn chắc chắn Claude dùng skill này, thêm vào đầu câu: **"Dùng skill siu-video-editing:"**

---

## 6. Khách hàng nhận gì và mở project thế nào?

Bạn gửi khách **file video MP4** và **file `…_CapCut.zip`**. Khách làm theo 4 bước (đã có trong file `HUONG_DAN.txt`
bên trong zip):

1. Giải nén toàn bộ file zip (chuột phải → Extract All).
2. **Tắt hẳn CapCut** (kể cả biểu tượng nhỏ dưới góc phải thanh taskbar).
3. Bấm đúp **`CAI_DAT_PROJECT.bat`** (nếu hiện "Windows protected your PC" thì bấm More info → Run anyway). Chờ chữ **XONG**.
4. Mở CapCut, bấm vào project trong danh sách **Projects**. Lần mở đầu cần có mạng để CapCut tải font và hiệu ứng.

> **Quan trọng:** khách **không** được tự "import" thư mục media vào một project mới, làm vậy chỉ thấy footage thô.
> File cài tự sửa đường dẫn để project chạy đúng trên máy của khách.

---

## 7. Những điều cần biết

- **Claude không nghe được âm thanh.** Claude đo âm lượng bằng số, nhưng bạn vẫn phải **tự nghe** bản xem trước.
- **Phụ đề tiếng nước ngoài**: luôn nhờ người biết ngôn ngữ đó (hoặc chính người nói) kiểm tra trước khi đăng.
- **Tên, chức danh**: kiểm tra lại chính tả, dấu (ví dụ "Việt" khác "Viết").
- **Chỉ dùng phần miễn phí của CapCut.** Nếu lúc xuất video CapCut đòi gói Pro, Claude sẽ thay hiệu ứng đó bằng cái miễn phí.
  Khi CapCut hiện quảng cáo Pro: bấm **X**, **đừng bấm mua**.
- **Bản quyền nhạc**: nhạc của YouTube Audio Library hay nhạc "thương mại" trong CapCut chưa chắc dùng được trên Facebook.
  Đăng Facebook thì nên dùng nhạc từ thư viện âm thanh của Meta (Sound Collection) hoặc nhạc có giấy phép ghi rõ Facebook.
- **Đừng mở CapCut** trong lúc Claude đang tạo project (CapCut sẽ ghi đè).
- **Máy yếu**: Claude làm từng việc nặng một (render, nhận dạng giọng nói) để máy không bị quá tải. Cứ để máy chạy.
- **Phiên bản CapCut**: đã thử với CapCut 9.8 cho Windows. Bản CapCut mới hơn có thể khác; Claude sẽ mở thử project trước khi giao.

---

## 8. Câu hỏi thường gặp và cách xử lý lỗi

**Claude không dùng skill / không biết skill là gì?**
Mở **phiên mới** (skill chỉ được nạp khi bắt đầu phiên). Thêm "Dùng skill siu-video-editing:" vào đầu câu. Kiểm tra
file `%USERPROFILE%\.claude\skills\siu-video-editing\SKILL.md` có tồn tại không (dán đường dẫn này vào thanh địa chỉ
của File Explorer).

**Báo lỗi "python is not recognized" hoặc "ffmpeg is not recognized".**
Bấm đúp lại `CAI_DAT_SKILL.bat` và chọn **C** ở câu hỏi cài Python / FFmpeg, hoặc gõ cho Claude:
"Cài giúp tôi Python và FFmpeg để dùng skill siu-video-editing".

**Windows hiện "Windows protected your PC".**
Bấm **More info** → **Run anyway**. Đây là cảnh báo chung cho mọi file tải từ mạng.

**Project không hiện trong danh sách của CapCut.**
Tắt hẳn CapCut (cả biểu tượng ở khay hệ thống góc phải), rồi mở lại.

**Trong CapCut có đoạn màu đỏ / báo thiếu media.**
Project chưa được cài đúng. Cài lại bằng `CAI_DAT_PROJECT.bat` (không import tay).

**Chữ hiện sai font hoặc thiếu hiệu ứng.**
Lần đầu mở, CapCut cần mạng để tải font và hiệu ứng. Đợi vài giây hoặc mở lại project.

**Máy tắt đột ngột khi đang xuất video.**
Mở lại Claude Code ở thư mục dự án, gõ "máy vừa tắt đột ngột, làm tiếp giúp tôi". Claude sẽ kiểm tra file nào bị hỏng
và chạy lại từng việc một.

**Muốn cập nhật skill lên bản mới.**
Làm lại Cách 1 hoặc Cách 2. Bản cũ được tự cất sang `%USERPROFILE%\.claude\skills_backup\`.

**Muốn gỡ skill.**
Xoá thư mục `%USERPROFILE%\.claude\skills\siu-video-editing`.

---

## 9. Bên trong skill có gì?

```text
siu-video-editing-skill/
├── README.md                  ← tài liệu bạn đang đọc
├── CAI_DAT_SKILL.bat          ← bấm đúp để cài (Cách 2)
├── cai_dat_skill.ps1          ← phần chạy của file cài
├── .claude-plugin/            ← để cài dạng plugin (Cách 3)
└── skills/siu-video-editing/  ← chính là skill
    ├── SKILL.md               ← "sổ tay" Claude đọc đầu tiên: quy tắc bắt buộc + quy trình 8 bước
    ├── references/            ← 14 tài liệu chuyên sâu
    │   ├── lessons-learned.md     các lỗi đã mắc, nguyên nhân và cách tránh
    │   ├── client-taste.md        khách đã sửa gì trong 2 video đã duyệt, và vì sao
    │   ├── house-style.md         màu, font, vị trí chữ, sticker, lower-third, phụ đề của SIU
    │   ├── story-pacing.md        bố cục, nhịp dựng, 3 giây đầu, voice-over
    │   ├── audio.md               chọn nhạc, bản quyền, âm lượng, hiệu ứng âm thanh
    │   ├── speech-subtitles.md    nhận dạng giọng nói, nhiều ngôn ngữ, phụ đề
    │   ├── footage-qa.md          chọn cảnh, tốc độ, khung hình mắt nhắm, chữ che mặt, màu
    │   ├── capcut-pipeline.md     cách tạo project CapCut đúng
    │   ├── capcut-handover.md     đóng gói và gửi project cho khách
    │   ├── capcut-gui.md          Claude mở / kiểm tra / xuất video trong CapCut
    │   ├── intake.md              câu hỏi cần hỏi khách trước khi dựng
    │   ├── tools-and-mcp.md       so sánh các công cụ CapCut miễn phí cho Claude
    │   ├── remotion-layers.md     đồ hoạ động mà CapCut không tự làm được
    │   └── qa-checklist.md        danh sách kiểm tra trước khi giao
    ├── scripts/               ← công cụ tự động (Python / PowerShell)
    │   ├── capcut_kit.py          tạo project CapCut nhiều lớp + đóng gói cho khách
    │   ├── capcut_install/        file cài project gửi kèm cho khách
    │   ├── grade_lut.py           chỉnh màu đều giữa các clip
    │   ├── music_check.py         kiểm tra nhạc: nhịp, cao trào, lặp, có lời
    │   ├── lang_id.py             nhận biết đoạn nào nói tiếng gì + chép lời
    │   ├── score_text.py          so bản chép lời nào khớp âm thanh hơn
    │   ├── textcheck.py           kiểm tra chữ có che người không
    │   ├── crop_sheet.py          phóng to vùng mắt từng khung để chọn khung đẹp
    │   ├── smoothness.py          phát hiện chỗ video bị giật
    │   ├── master.py              chuẩn âm lượng -14 LUFS + bản xem trước 720p
    │   └── …                      probe, contact_sheet, slowmo, cutout, sfx_gen
    └── templates/build_template.py   ← khung dựng project CapCut
```

---

## 10. Tác giả

**Nguyễn Việt Anh Khoa**, sinh viên K17, ngành Khoa học Máy tính (chuyên ngành Trí tuệ Nhân tạo), lớp 24DAI,
Trường Đại học Quốc tế Sài Gòn (SIU).

Skill được xây dựng cùng Claude Code (Anthropic). Dự án cá nhân, không liên kết với CapCut / ByteDance hay Anthropic.
Có góp ý hoặc gặp lỗi: tạo mục **Issues** trên trang GitHub này.
