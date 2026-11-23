# Cài project CapCut vào máy này: tìm thư mục project của CapCut, chép project vào đó và sửa mọi đường dẫn media theo máy này.
# Chạy bằng cách bấm đúp CAI_DAT_PROJECT.bat (nằm cạnh file này). Tham số -Name đổi tên project khi cài (mặc định = tên thư mục).
param([string]$Name = '')
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch {}
function Stop-Install($msg) { Write-Host "`n$msg" -ForegroundColor Red; Read-Host "`nNhấn Enter để đóng" | Out-Null; exit 1 }

$src = Get-ChildItem -LiteralPath $PSScriptRoot -Directory | Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'draft_content.json') } | Select-Object -First 1
if (-not $src) { Stop-Install 'Không thấy thư mục project cạnh file cài đặt. Hãy GIẢI NÉN TOÀN BỘ file zip (chuột phải > Extract All) rồi chạy lại.' }
if (-not $Name) { $Name = $src.Name }
Write-Host "Cài project CapCut: $Name" -ForegroundColor Cyan

# 1. Thư mục project của CapCut (CapCut > Cài đặt > Projects); mặc định nằm trong %LOCALAPPDATA%
$root = Join-Path $env:LOCALAPPDATA 'CapCut\User Data\Projects\com.lveditor.draft'
$cfg = Join-Path $env:LOCALAPPDATA 'CapCut\User Data\Config\globalSetting'
if (Test-Path -LiteralPath $cfg) {
  $line = Select-String -LiteralPath $cfg -Pattern '^currentCustomDraftPath=(.+)$' | Select-Object -First 1
  if ($line) { $p = $line.Matches[0].Groups[1].Value.Trim().Replace('\\', '\'); if (Test-Path -LiteralPath $p) { $root = $p } }
}
if (-not (Test-Path -LiteralPath $root)) { Stop-Install "Chưa thấy thư mục project của CapCut ($root). Hãy mở CapCut một lần, tắt đi, rồi chạy lại file cài đặt." }
Write-Host "Thư mục project của CapCut: $root"

# 2. CapCut phải tắt hẳn (khi tắt, nó ghi lại danh sách project)
while (Get-Process -Name CapCut -ErrorAction SilentlyContinue) {
  Write-Host "`nCapCut đang mở. Hãy TẮT HẲN CapCut (cả biểu tượng dưới khay hệ thống, góc phải thanh taskbar) rồi nhấn Enter..." -ForegroundColor Yellow
  Read-Host | Out-Null
}

# 3. Chép project (bản cũ cùng tên được giữ lại dưới tên khác, không xoá)
$dst = Join-Path $root $Name
if (Test-Path -LiteralPath $dst) {
  $old = $Name + '_cu_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
  Rename-Item -LiteralPath $dst -NewName $old
  Write-Host "Đã có project cùng tên, bản cũ được đổi tên thành: $old"
}
Write-Host "Đang chép project (có thể mất 1-2 phút)..."
Copy-Item -LiteralPath $src.FullName -Destination $dst -Recurse
$want = (Get-ChildItem -LiteralPath (Join-Path $src.FullName 'media') -File).Count
$got = (Get-ChildItem -LiteralPath (Join-Path $dst 'media') -File).Count
if ($got -ne $want) { Stop-Install "Chép thiếu file media ($got/$want). Kiểm tra dung lượng ổ đĩa rồi chạy lại." }

# 4. Đường dẫn media -> máy này
$utf8 = New-Object Text.UTF8Encoding($false)
$dir = $dst.Replace('\', '/')
$f = Join-Path $dst 'draft_content.json'
$t = [IO.File]::ReadAllText($f, $utf8)
# token written by capcut_kit.package() (older SIU zips used __SIU_DRAFT_DIR__)
$n = ([regex]::Matches($t, '__CAPCUT_DRAFT_DIR__|__SIU_DRAFT_DIR__')).Count
if ($n -eq 0) { Stop-Install 'Project không có đường dẫn media cần sửa (thiếu token). Hãy báo lại cho người gửi.' }
$t = $t.Replace('__CAPCUT_DRAFT_DIR__', $dir).Replace('__SIU_DRAFT_DIR__', $dir)
[IO.File]::WriteAllText($f, $t, $utf8)
# every media path in the project must now exist on this PC
$miss = @([regex]::Matches($t, '"path"\s*:\s*"([^"]*/media/[^"]*)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique | Where-Object { -not (Test-Path -LiteralPath $_) })
if ($miss.Count -gt 0) { Stop-Install ("Thiếu " + $miss.Count + " file media sau khi cài, ví dụ: " + $miss[0]) }
$m = Join-Path $dst 'draft_meta_info.json'
$j = [IO.File]::ReadAllText($m, $utf8)
$j = $j -replace '"draft_fold_path"\s*:\s*"[^"]*"', ('"draft_fold_path":"' + $dir + '"')
$j = $j -replace '"draft_root_path"\s*:\s*"[^"]*"', ('"draft_root_path":"' + $root.Replace('\', '/') + '"')
$j = $j -replace '"draft_name"\s*:\s*"[^"]*"', ('"draft_name":"' + $Name + '"')
[IO.File]::WriteAllText($m, $j, $utf8)

Write-Host "`nXONG! Đã nối $n đường dẫn media và $got file vào project." -ForegroundColor Green
Write-Host "Mở CapCut: project `"$Name`" nằm trong danh sách Projects ở màn hình chính. Bấm vào để mở." -ForegroundColor Green
Write-Host "Lần mở đầu CapCut tự tải các hiệu ứng, chuyển cảnh, font từ thư viện của nó (cần mạng), chờ vài giây."
Read-Host "`nNhấn Enter để đóng" | Out-Null
