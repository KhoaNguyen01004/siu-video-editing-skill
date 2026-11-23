# Smooth slow motion from 30 fps phone footage: motion-compensated 4x interpolation of a time range.
# Playing 30 fps footage slower than 1x repeats frames ("lag lag"); interpolate instead. The output is a 30 fps file where
# every original frame became 4: play it at speed 4 = real time, 2 = 0.5x, 4/3 = 1/3x. Speed ramps = constant-speed pieces.
# Water splashes interpolate cleanly; fast crossing limbs / hands can smear -> check the result frame by frame.
# A HELD frame at the end of a slow-mo must be an ORIGINAL frame (x4 index divisible by 4), never an interpolated one.
#   python slowmo.py <src> <t_start> <t_end> <out.mp4>
import subprocess, sys

src, a, b, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
vf = ("fps=30,setpts=PTS-STARTPTS,minterpolate=fps=120:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
      "setpts=4*PTS,fps=30,format=yuv420p")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", src, "-an", "-vf", vf,
                "-c:v", "libx264", "-crf", "16", "-g", "15", "-bf", "0", "-movflags", "+faststart", out], check=True)
print(f"{out}: source {a:.2f}-{b:.2f} s -> {4 * (b - a):.2f} s at 1/4 speed. x4 time t = source {a:.2f} + t/4")
