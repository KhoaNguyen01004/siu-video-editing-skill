# Loudness master for upload: two-pass loudnorm to -14 LUFS integrated, true peak <= -1.5 dBTP, AAC 48 kHz, faststart.
#   python master.py in.mp4 out.mp4                 re-encode video too (Remotion / ffmpeg renders): H.264 high, CRF 18
#   python master.py in.mp4 out.mp4 --copy-video    audio only, picture untouched (a CapCut export: keep CapCut's encode)
#   python master.py in.mp4 out.mp4 --preview p.mp4 also a < 30 MB 720p copy to send to a phone (masters stay on the PC)
# Also prints the result's measured loudness so the report can quote a number instead of "sounds fine" (Claude cannot listen).
import json, re, subprocess, sys

src, dst = sys.argv[1], sys.argv[2]


def measure(f, extra=""):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", f"{extra}loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr).group(0))


m = measure(src)
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
video = ["-c:v", "copy"] if "--copy-video" in sys.argv else \
        ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30", "-g", "60"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, *video, "-af", af, "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                "-movflags", "+faststart", dst], check=True)
o = measure(dst)
print(f"{dst}: {m['input_i']} -> {o['input_i']} LUFS, true peak {o['input_tp']} dBTP")
if "--preview" in sys.argv:
    prev = sys.argv[sys.argv.index("--preview") + 1]
    w, h = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                             "-of", "csv=p=0", dst], text=True).strip().split(","))
    sc = "scale=720:-2" if h >= w else "scale=-2:720"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst, "-vf", sc + ":flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-b:v", "2300k",
                    "-maxrate", "2800k", "-bufsize", "4600k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", prev],
                   check=True)
    print("preview:", prev)
