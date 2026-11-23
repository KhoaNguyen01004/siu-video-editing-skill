# Hand-over: an editable CapCut project the client can actually open

Client requirement (Mỹ Tho feedback #8): send the finished MP4 **and** the CapCut project; every element (footage, text,
music, voice, effects, transitions, graphics) on its own layer, nothing flattened, everything still working on their PC.

## What went wrong before
1. The client imported `media/` into a new project and saw only raw footage: the draft held this PC's absolute paths and
   there was no install step (lesson F1).
2. Music ducking 53 s off in the project only (keyframes in source time, lesson D4).
3. Text animation durations of 0 µs (lesson F2); text sizes wrong / wrapped mid-word (F3).
4. A composite title the client could not take apart (F5).

## Package (capcut_kit)
```python
p.save()
p.package("out/<NAME>_CapCut.zip", guide_title="SIU – <tên video>", extra=["out/BAN_DICH_CHO_DUYET.md"])
```
The zip:
```
CAI_DAT_PROJECT.bat        double-click installer (runs cai_dat_project.ps1, ExecutionPolicy Bypass)
cai_dat_project.ps1        finds CapCut's project folder (custom path from Settings honoured), waits for CapCut to close,
                           copies the project, swaps the path token for the real path, fills draft_meta_info, verifies
                           every media file exists
HUONG_DAN.txt              Vietnamese guide (automatic + manual install, how to edit, how to export)
<NAME>/draft_content.json  media paths = __CAPCUT_DRAFT_DIR__/media/...
<NAME>/draft_meta_info.json
<NAME>/media/...           every file the project uses (graded proxies, PNGs, alpha layers, music, voice, SFX)
```
`package()` refuses to write the zip if any path of this PC is left in the draft. Client-facing `.ps1` / `.txt` are
UTF-8 **with BOM** + CRLF (PowerShell 5.1 and Notepad garble Vietnamese otherwise).

## Test like a client (every delivery)
1. Extract the zip to a folder with Vietnamese characters in its path.
2. Rename the original draft's `media` folder (so nothing can resolve to it).
3. Run `powershell -ExecutionPolicy Bypass -File cai_dat_project.ps1 -Name <NAME>_test`.
4. Open CapCut → `<NAME>_test` → the timeline is complete, no red "media missing" clips, fonts and effects load.
5. Check: music volume envelope dips under the voice; text sizes; a transition; one keyframed graphic.
6. Delete `<NAME>_test`, restore the media folder.

## Message to the client (Vietnamese, adapt)
> Mình gửi bạn video thành phẩm và project CapCut để bạn tự chỉnh nha. Cài project như sau:
> 1. Giải nén toàn bộ file zip (chuột phải > Extract All).
> 2. Tắt hẳn CapCut, kể cả biểu tượng dưới khay góc phải.
> 3. Bấm đúp **CAI_DAT_PROJECT.bat**. Nếu Windows hiện "Windows protected your PC" thì bấm More info > Run anyway. Chờ báo XONG.
> 4. Mở CapCut, bấm vào project **<NAME>** trong danh sách Projects. Lần mở đầu cần có mạng để CapCut tải font và hiệu ứng.
> Lưu ý: đừng import thư mục media vào project mới (làm vậy chỉ có footage thô). Mỗi thành phần nằm trên một track riêng có tên,
> bạn bấm vào là sửa được. Hướng dẫn chi tiết trong file HUONG_DAN.txt.

## Versioning
- Name drafts `<NAME>_vN`; keep the previous version's zip until the client confirms the new one.
- Before re-exporting a draft the user may have opened, copy it to a backup folder (the user sometimes edits in CapCut).
- Say what the project needs: CapCut desktop (Windows), version tested, internet on first open, and that it uses only free
  CapCut elements (Pro check passed at export).
