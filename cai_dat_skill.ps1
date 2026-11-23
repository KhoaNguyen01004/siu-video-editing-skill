# Cài skill "siu-video-editing" cho Claude Code vào máy này.
# Cách chạy: bấm đúp file CAI_DAT_SKILL.bat nằm cạnh file này.
#   -Target <thư mục>  : cài vào thư mục khác (mặc định %USERPROFILE%\.claude\skills)
#   -SkipTools         : chỉ chép skill, không hỏi cài Python / FFmpeg / thư viện
param([string]$Target = (Join-Path $env:USERPROFILE '.claude\skills'), [switch]$SkipTools)
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch {}
function Close-Window($code) { Read-Host "`nNhấn Enter để đóng cửa sổ này" | Out-Null; exit $code }
function Ask-Yes($q) { $a = Read-Host "$q  Gõ C (có) hoặc K (không) rồi nhấn Enter"; return ($a -match '^\s*[cCyY]') }
function Update-PathNow { $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') }
function Find-Python {
  # trả về lệnh chạy được Python >= 3.10 (bỏ qua lối tắt "python" của Microsoft Store khi chưa cài Python thật)
  foreach ($c in @(@('python'), @('py', '-3'))) {
    try {
      $exe = $c[0]; $args0 = @($c | Select-Object -Skip 1)
      $out = & $exe @args0 -c "import sys; print(sys.version_info >= (3, 10))" 2>$null
      if ($LASTEXITCODE -eq 0 -and "$out" -match 'True') { return ,$c }
    } catch {}
  }
  return $null
}

Write-Host '=== CÀI SKILL SIU VIDEO EDITING CHO CLAUDE CODE ===' -ForegroundColor Cyan
$src = Join-Path $PSScriptRoot 'skills\siu-video-editing'
if (-not (Test-Path -LiteralPath (Join-Path $src 'SKILL.md'))) {
  Write-Host 'Không thấy thư mục skills\siu-video-editing cạnh file này.' -ForegroundColor Red
  Write-Host 'Hãy GIẢI NÉN TOÀN BỘ file zip (chuột phải > Extract All) rồi bấm đúp lại CAI_DAT_SKILL.bat từ thư mục đã giải nén.'
  Close-Window 1
}

# 1) Chép skill (bản cũ, nếu có, được cất sang skills_backup chứ không xoá)
New-Item -ItemType Directory -Force -Path $Target | Out-Null
$dst = Join-Path $Target 'siu-video-editing'
if (Test-Path -LiteralPath $dst) {
  $bk = Join-Path (Split-Path $Target -Parent) ('skills_backup\siu-video-editing_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
  New-Item -ItemType Directory -Force -Path (Split-Path $bk -Parent) | Out-Null
  Move-Item -LiteralPath $dst -Destination $bk
  Write-Host "Đã có bản cũ, bản cũ được cất vào: $bk"
}
Copy-Item -LiteralPath $src -Destination $dst -Recurse
Write-Host "[1/3] Đã chép skill vào: $dst" -ForegroundColor Green
if ($SkipTools) { Write-Host 'Bỏ qua bước cài công cụ (-SkipTools).'; Close-Window 0 }

# 2) Phần mềm hỗ trợ: Python và FFmpeg (miễn phí). Dùng winget có sẵn trong Windows 10/11.
$hasWinget = [bool](Get-Command winget -ErrorAction SilentlyContinue)
$py = Find-Python
if (-not $py) {
  if ($hasWinget -and (Ask-Yes 'Máy chưa có Python (ngôn ngữ chạy các công cụ của skill). Cài Python 3.12 miễn phí?')) {
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    Update-PathNow; $py = Find-Python
  }
}
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  if ($hasWinget -and (Ask-Yes 'Máy chưa có FFmpeg (công cụ đọc và xử lý video). Cài FFmpeg miễn phí?')) {
    winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
    Update-PathNow
  }
}
Write-Host ('[2/3] Python: ' + $(if ($py) { 'có' } else { 'CHƯA CÓ' }) + ' | FFmpeg: ' + $(if (Get-Command ffmpeg -ErrorAction SilentlyContinue) { 'có' } else { 'CHƯA CÓ (mở lại cửa sổ mới nếu vừa cài)' }))

# 3) Thư viện Python của skill
if ($py) {
  if (Ask-Yes 'Cài các thư viện Python mà skill cần (khoảng 500 MB, mất 5-10 phút)?') {
    $exe = $py[0]; $pre = @($py | Select-Object -Skip 1)
    & $exe @pre -m pip install -r (Join-Path $dst 'scripts\requirements.txt')
    & $exe @pre (Join-Path $dst 'scripts\capcut_kit.py') --selftest
    if ($LASTEXITCODE -eq 0) { Write-Host '[3/3] Thư viện đã cài và tự kiểm tra OK.' -ForegroundColor Green }
    else { Write-Host '[3/3] Có lỗi khi cài thư viện. Mở Claude và nhờ: "cài giúp tôi thư viện của skill siu-video-editing".' -ForegroundColor Yellow }
  }
} else {
  Write-Host '[3/3] Chưa có Python nên chưa cài thư viện. Mở Claude và nhờ: "cài giúp tôi Python và thư viện của skill siu-video-editing".' -ForegroundColor Yellow
}
Write-Host "`nXONG! Mở Claude (mục Code), bắt đầu một phiên MỚI, rồi gõ yêu cầu dựng video SIU. Skill sẽ tự được dùng." -ForegroundColor Cyan
Write-Host 'Mô hình nhận dạng giọng nói (khoảng 3 GB) sẽ tự tải ở lần đầu dùng tới.'
Close-Window 0
