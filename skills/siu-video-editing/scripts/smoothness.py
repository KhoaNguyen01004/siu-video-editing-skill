# "Lag lag" detector for a finished render. The user's "giật / lag" on v3 was PLAYBACK SPEED, not the renderer:
# 30 fps phone footage played at 0.8x repeats frames (17 repeated in one slow-mo), 1.5x steps 1-2-1-2 frames.
# Per shot (cuts found automatically): repeated frames while the picture should move, and cadence jitter of the motion.
# Intended holds (freeze frames, title cards, photos) show up as "static" and are fine; judge the STUTTER lines.
#   python smoothness.py render.mp4 [--from 0 --to 60]
import subprocess, sys
import numpy as np

W, H, FPS = 96, 170, 30


def main():
    v = sys.argv[1]
    a = float(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else 0.0
    b = float(sys.argv[sys.argv.index("--to") + 1]) if "--to" in sys.argv else None
    cmd = ["ffmpeg", "-v", "error", "-ss", str(a)] + (["-t", str(b - a)] if b else []) + \
          ["-i", v, "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"]
    fr = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.uint8).reshape(-1, H, W).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    # shot boundaries: a jump far above the local motion level
    loc = np.array([np.median(d[max(0, i - 8):i + 8]) for i in range(len(d))])
    cuts = [0] + [i + 1 for i in range(len(d)) if d[i] > max(18.0, 4 * loc[i] + 6)] + [len(fr)]
    bad = 0
    print(f"{'shot':>4} {'time':>13}  {'motion':>6} {'repeat':>6} {'jitter':>6}")
    for k, (s, e) in enumerate(zip(cuts, cuts[1:])):
        seg = d[s + 3:e - 3]
        if len(seg) < 8: continue
        med = float(np.median(seg))
        if med < 0.6:
            print(f"{k:4d} {a + s / FPS:6.2f}-{a + e / FPS:6.2f}  {med:6.2f}      -      -  static (hold / title / photo)"); continue
        same = seg < 0.15 * med + 0.05
        # runs of repeated frames: 1-2 in a row = stutter (uneven speed); >= 6 in a row = an intended hold (freeze frame)
        runs, n = [], 0
        for x in list(same) + [False]:
            if x: n += 1
            elif n: runs.append(n); n = 0
        dups = sum(r for r in runs if r <= 2); holds = sum(r for r in runs if r >= 6)
        moving = seg[~same]
        jit = float(np.mean(np.abs(np.diff(moving))) / (np.median(moving) + 1e-6)) if len(moving) > 4 else 0.0
        flag = dups >= 3 or jit > 0.9          # calibrated: v3 (user said "lag") 4-18 per bad shot; accepted v4 <= 2
        bad += flag
        print(f"{k:4d} {a + s / FPS:6.2f}-{a + e / FPS:6.2f}  {med:6.2f} {dups:6d} {jit:6.2f}  {'STUTTER' if flag else 'ok'}"
              f"{f'  (+ hold of {holds} frames)' if holds else ''}")
    print(f"shots flagged: {bad}  (fix: play at exactly 1x or 2x; slow motion only from motion-interpolated sources, see slowmo.py)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
