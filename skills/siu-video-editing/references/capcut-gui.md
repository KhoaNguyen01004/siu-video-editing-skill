# Driving CapCut desktop with computer-use (open, check, export)

Needed to: verify a draft really opens, check text sizes and the music envelope, and export the final MP4 from CapCut
(CapCut-first pipeline). Ask the user first; explain why (they denied it once until told the reason).

## Access
- `request_access` for **"CapCut"** first; the visible window belongs to the versioned `capcut.exe` process, so when the
  screenshot says "capcut.exe was hidden", request **"capcut.exe"** as a second call.
- Close Pro / Ultra / trial / notification popups with Cancel / X. **Never** click a purchase, trial or subscription button.
  Some popups are separate Qt windows that ignore synthetic clicks and Escape: list the CapCut windows (title "CapCut",
  the small one is the popup) and send it `WM_CLOSE` (same as its X). Snippet in `scripts/capcut_front.ps1` comments.

## Opening
1. Kill CapCut before writing a draft; start it after (`Start-Process "$env:LOCALAPPDATA\CapCut\Apps\CapCut.exe"`).
2. CapCut often starts minimized: run `scripts/capcut_front.ps1` (ShowWindow 9 + foreground + maximize).
3. Home screen → Projects → click the project card. First open downloads fonts / effects (needs internet, wait).

## Checking
- Clicks on the ruler do not move the playhead; a click in the EMPTY timeline area below the tracks moves it to that x.
  Then step with ← → (1 frame each) and read the time under the preview (HH:MM:SS:FF).
- A ⚠ "Animation" badge on a text clip = an animation resource CapCut could not load (e.g. outro 缩小 in 9.8): replace it.
- Opening a draft makes CapCut 9.8 add a `Timelines/` folder (draft migration). Regenerate the whole draft folder from
  build.py instead of patching an opened draft's JSON.
- Zoom the preview or select a track to see small graphics (a 35 px pin icon is invisible at preview size).
- Things to look at: first frame of each section, every text (size, wrap, position), the music track's volume line,
  the split-screen / grid panels, a pop-out, the end.
- Missing media shows red clips: the install or the paths are wrong (do not hand over).

## Export
1. Export button (top right) → dialog: resolution 1080p, frame rate 30, codec H.264, bit rate "Higher", format MP4,
   **untick "Sync exported videos to space"**.
2. Mouse clicks on the dialog's Export button were often ignored: press **Enter**.
3. If a Pro prompt appears, a Pro element is in the project: cancel, find it (the prompt lists it), replace it with a
   free one or keyframes, export again. Never export with a watermark.
4. Output lands in `%LOCALAPPDATA%\CapCut\Videos\<name>.mp4` (or the folder chosen in the dialog).
5. `python scripts/master.py export.mp4 final.mp4 --copy-video --preview preview_720p.mp4`.

## After
- Close the project and kill CapCut before regenerating the draft (or it keeps the old one in memory).
- Report exactly which moments you looked at in CapCut and which you did not.
