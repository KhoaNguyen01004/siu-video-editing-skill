# Inventory every clip before planning: duration, size, rotation, fps (real vs nominal), audio streams, HDR.
# Catches what bit us before: a "voice" clip with NO audio stream (Mỹ Tho "Source có voice 3"), variable frame rate
# phone footage (cuts drift unless you transcode to CFR), iPhone HLG/Dolby Vision (looks grey and washed out unless tone-mapped).
#   python probe.py <folder or files...>  [--md out.md]
import json, os, subprocess, sys

VIDEO_EXT = (".mov", ".mp4", ".m4v", ".mkv", ".avi", ".mts")
AUDIO_EXT = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")


def is_vfr(f):
    """True when frame timestamps are irregular (the avg_frame_rate field alone gives false alarms on iPhone clips)."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-read_intervals", "%+20", "-show_entries", "packet=pts_time",
                          "-of", "csv=p=0", f], capture_output=True, text=True).stdout.split()
    t = sorted(float(x) for x in out if x.replace(".", "", 1).isdigit())
    d = [b - a for a, b in zip(t, t[1:])]
    if len(d) < 10: return False
    med = sorted(d)[len(d) // 2]
    return sum(abs(x - med) > 0.002 for x in d) > 0.02 * len(d)


def probe(f):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", f],
                                  capture_output=True, text=True, encoding="utf-8").stdout or "{}")
    v = next((s for s in j.get("streams", []) if s["codec_type"] == "video" and s.get("disposition", {}).get("attached_pic", 0) == 0), None)
    a = [s for s in j.get("streams", []) if s["codec_type"] == "audio"]
    dur = float(j.get("format", {}).get("duration", 0))
    row = dict(file=os.path.basename(f), dur=round(dur, 2), audio=len(a))
    if v:
        rot = 0
        for sd in v.get("side_data_list", []):
            if "rotation" in sd: rot = int(sd["rotation"])
        rot = rot or int(v.get("tags", {}).get("rotate", 0))
        w, h = v["width"], v["height"]
        if abs(rot) in (90, 270): w, h = h, w
        num, den = map(int, v.get("r_frame_rate", "0/1").split("/"))
        fps = num / den if den else 0
        trc = v.get("color_transfer", "")
        row.update(size=f"{w}x{h}", rot=rot, fps=round(fps, 2), vfr=is_vfr(f),
                   hdr="HLG" if trc == "arib-std-b67" else "PQ" if trc == "smpte2084" else "", codec=v["codec_name"])
    return row


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    md = sys.argv[sys.argv.index("--md") + 1] if "--md" in sys.argv else None
    if md in args: args.remove(md)
    files = []
    for a in args:
        if os.path.isdir(a):
            files += [os.path.join(a, f) for f in sorted(os.listdir(a)) if f.lower().endswith(VIDEO_EXT + AUDIO_EXT)]
        else: files.append(a)
    rows = [probe(f) for f in files]
    L = ["| file | dur s | size | rot | fps | VFR | HDR | audio streams |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['file']} | {r['dur']} | {r.get('size', 'audio')} | {r.get('rot', '')} | {r.get('fps', '')} | "
                 f"{'VFR' if r.get('vfr') else ''} | {r.get('hdr', '')} | {r['audio']} |")
    total = sum(r["dur"] for r in rows if "size" in r)
    L.append(f"\n{len(rows)} files, {total / 60:.1f} min of video.")
    warn = [f"- {r['file']}: NO audio stream" for r in rows if r["audio"] == 0] + \
           [f"- {r['file']}: {r['hdr']} HDR -> tone-map to SDR (zscale/tonemap) before grading" for r in rows if r.get("hdr")] + \
           [f"- {r['file']}: variable frame rate -> transcode to CFR 30 before cutting" for r in rows if r.get("vfr")] + \
           [f"- {r['file']}: landscape {r['size']} in a 9:16 edit -> plan a reframe, never stretch" for r in rows
            if "size" in r and int(r["size"].split("x")[0]) > int(r["size"].split("x")[1])]
    if warn: L += ["", "Warnings:"] + warn
    out = "\n".join(L)
    print(out)
    if md: open(md, "w", encoding="utf-8").write(out + "\n")


if __name__ == "__main__":
    main()
