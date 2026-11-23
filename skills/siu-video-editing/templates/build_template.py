# build.py — ONE source of truth for a SIU reel, CapCut-first.
# Copy into <project>/tools/build.py, edit CONFIG / CUTS / TEXTS, run:  python tools/build.py
# Writes: the layered CapCut draft NAME (CapCut must be closed), out/CUT_PLAN.md, qa/boxes.json (for textcheck.py),
#         out/NAME_CapCut.zip (portable, with installer).  Then: open + export in CapCut, master.py --copy-video.
# Everything the client will edit is a separate, named track. Times in seconds on the timeline unless noted.
import glob, json, os, sys


def _skill_scripts():
    """The skill's scripts folder: installed as a skill (~/.claude/skills) or as a plugin (~/.claude/plugins/...)."""
    home = os.path.expanduser("~")
    cands = [os.environ.get("SIU_SKILL_SCRIPTS", ""), os.path.join(home, ".claude", "skills", "siu-video-editing", "scripts")]
    cands += sorted(glob.glob(os.path.join(home, ".claude", "plugins", "**", "siu-video-editing", "scripts"), recursive=True))
    for c in cands:
        if c and os.path.exists(os.path.join(c, "capcut_kit.py")): return c
    sys.exit("Cannot find the siu-video-editing skill's scripts folder; set SIU_SKILL_SCRIPTS to it.")


sys.path.insert(0, _skill_scripts())
from capcut_kit import Project, F, T, TI, TO, TL, FX, KP, hexrgb, US  # noqa: E402

# ------------------------------------------------------------------ CONFIG
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
P = lambda *a: os.path.join(ROOT, *a)
NAME = os.environ.get("REEL_NAME", "SIU_Reel_Demo")
MAX_LEN = 60.0
CLIPS = os.environ.get("REEL_CLIPS", P("graded"))              # graded CFR proxies from grade_lut.py
MUSIC = dict(path=os.environ.get("REEL_MUSIC", P("media", "music.mp3")), offset=49.04)   # offset = where in the track we start
SFX = os.environ.get("REEL_SFX", P("media", "sfx"))           # sfx_gen.py output
VOICES = {}                                                    # {"chant": (path, unmuted source clip audio as .wav)}
CRIMSON, GREEN, YELLOW, CREAM, NAVY, WHITE, INK = (hexrgb(h) for h in
    ("#BB1C3D", "#3D9032", "#FFD23F", "#F0E9D4", "#2C3C82", "#FFFFFF", "#1E1E1E"))

# ------------------------------------------------------------------ CUTS: (source file in CLIPS, source in-point s, duration s,
# transition INTO THE NEXT clip or None, why). Durations in beats are nicer: dur = beats * 60 / BPM.
CUTS = [
    ("7494.mp4", 2.0, 2.0, (T.推近, "0.4s"), "life vests wave: hook, faces at camera"),
    ("7516.mp4", 0.5, 2.0, (T.横向模糊, "0.3s"), "honeycomb frame"),
    ("7520.mp4", 1.0, 2.5, None, "honey tea"),
]

# ------------------------------------------------------------------ TEXTS: (track, text, start, dur, x, y, px, kind, extra)
# The values below are EXAMPLES (in the skill's own test they sat on a face and on life vests): choose x/y per shot on a calm
# area, then run textcheck.py qa/boxes.json and look at the sheet.
TEXTS = [
    ("Stickers", "Ngọt lịm!", 4.6, 1.6, 540, 420, 115, "sticker_yellow", {}),
    ("Chapter · số", "01", 2.2, 2.2, 165, 800, 140, "chapter_num", {}),
    ("Chapter · tên", "Trại ong mật", 2.3, 2.1, 520, 820, 64, "chapter_title", {}),
    ("Phụ đề", "Hôm nay thầy rất vui", 0.3, 1.9, 540, 1665, 66, "subtitle", {"highlight": ["rất vui"]}),
]
SFX_CUES = [(1.75, "whoosh_short", 0.45), (2.2, "pop", 0.4), (4.6, "pop", 0.45)]
DUCK = [(0.0, 1.0)]          # music gain keyframes (timeline s, linear); e.g. [(16.3,1.0),(17.3,0.18),(53.3,0.18),(54.0,1.0)]

STYLES = {   # kind -> kwargs for Project.text (house-style.md)
    "sticker_white": dict(font=F.Coiny_Regular, color=WHITE, border=GREEN, intro=TI.弹入, intro_d="0.35s", outro=TO.渐隐,
                          outro_d="0.2s", loop=TL.调皮, maxw=820, rotation=-4.0),
    "sticker_yellow": dict(font=F.Coiny_Regular, color=YELLOW, border=CRIMSON, intro=TI.弹入, intro_d="0.35s", outro=TO.渐隐,
                           outro_d="0.2s", loop=TL.调皮, maxw=820, rotation=4.0),
    "chapter_num": dict(font=F.Coiny_Regular, color=YELLOW, border=CRIMSON, intro=TI.弹入, intro_d="0.35s", outro=TO.渐隐,
                        rotation=-6.0, maxw=300),
    "chapter_title": dict(font=F.Montserrat, color=WHITE, bold=True, intro=TI.向右滑动, intro_d="0.4s", outro=TO.渐隐, maxw=640,
                          shadow=False),
    "subtitle": dict(font=F.Classic, color=WHITE, bold=True, border=(0, 0, 0), border_w=30, intro=TI.渐显, intro_d="0.12s",
                     maxw=860),
    "formal_line": dict(font=F.Prata_Regular, color=NAVY, shadow=False, intro=TI.渐显, intro_d="0.3s", outro=TO.渐隐, maxw=920),
    "display": dict(font=F.Anton, color=CRIMSON, shadow=False, intro=TI.弹出, intro_d="0.35s", outro=TO.渐隐, maxw=960),
}


def build():
    used = [c[0] for c in CUTS]
    assert len(used) == len(set(used)), f"a source is used twice: {sorted(u for u in used if used.count(u) > 1)}"
    total = sum(c[2] for c in CUTS)
    assert total <= MAX_LEN + 0.01, f"{total:.1f} s > {MAX_LEN} s"

    p = Project(NAME)
    p.tracks(video=["Footage"], effect=["Hiệu ứng"],
             text=sorted({t[0] for t in TEXTS}, key=[t[0] for t in TEXTS].index),
             audio=["Nhạc nền"] + [f"Voice · {k}" for k in VOICES])
    boxes, plan, faces, t = [], [], [], 0.0
    prev_trans = 0.0
    for src, a, d, trans, why in CUTS:
        path = os.path.join(CLIPS, src)
        p.video(path, t, d, src=a, track="Footage", transition=trans)        # muted (vol=0) by default
        plan.append(f"| {t:5.2f}–{t + d:5.2f} | {src} @ {a:.2f} | {trans[0].name if trans else 'cut'} | {why} |")
        # moments where a bad face (closed eyes, squint, looking down) would be SEEN: both sides of the cut, transition
        # windows (CapCut blends ~the transition duration around the cut), and any slowed / held clip (footage-qa.md §4)
        tr = float(trans[1].rstrip("s")) if trans else 0.0
        faces.append(dict(video=path, t0=a, t1=a + max(0.1, prev_trans), why=f"first frames of {src} (cut in)"))
        faces.append(dict(video=path, t0=a + d - max(0.1, tr), t1=a + d, why=f"last frames of {src} (cut out)"))
        prev_trans, t = tr, t + d
    # add HOLDS / stills / slow-mo ranges here, e.g. faces.append(dict(video=x4, t0=.., t1=.., why="slow-mo, every frame"))
    for track, text, s, d, x, y, px, kind, extra in TEXTS:
        seg = p.text(track, text, s, d, x, y, px, **{**STYLES[kind], **extra})
        w = min(px * 0.6 * max(len(l) for l in text.split("\n")), STYLES[kind].get("maxw", 900))   # rough box for textcheck
        h = seg.px * 1.25 * (text.count("\n") + 1)
        boxes.append(dict(label=text, t0=s, t1=s + d, box=[x - w / 2, y - h / 2, x + w / 2, y + h / 2],
                          frames=[_src_at(s + f) for f in (0.15, d / 2, d - 0.15)]))
    p.music(MUSIC["path"], 0, total, src=MUSIC["offset"], gains=DUCK, track="Nhạc nền", fade=("0.05s", "1.2s"))
    for k, (path, s, d) in VOICES.items():
        p.audio(path, s, d, track=f"Voice · {k}")
    for s, name, vol in SFX_CUES:
        p.sfx(s, os.path.join(SFX, name + ".wav"), vol)
    draft = p.save()

    os.makedirs(P("out"), exist_ok=True); os.makedirs(P("qa"), exist_ok=True)
    json.dump(boxes, open(P("qa", "boxes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(faces, open(P("qa", "face_points.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(P("out", "CUT_PLAN.md"), "w", encoding="utf-8").write(
        f"# Cut plan — {NAME} ({total:.1f} s)\n\n| Timeline | Source | Transition | Why |\n|---|---|---|---|\n" + "\n".join(plan) + "\n")
    p.package(P("out", f"{NAME}_CapCut.zip"), guide_title=f"SIU – {NAME}")
    print("draft:", draft, f"\n{total:.1f} s, {len(CUTS)} cuts, {len(TEXTS)} texts. Next: textcheck.py qa/boxes.json, "
          f"eye-check every entry of qa/face_points.json ({len(faces)}), open in CapCut, export.")


def _src_at(t):
    """[footage file, time in that file] under timeline time t (the picture textcheck.py must test)."""
    s = 0.0
    for src, a, d, *_ in CUTS:
        if s <= t < s + d: return [os.path.join(CLIPS, src), round(a + t - s, 3)]
        s += d
    src, a, d, *_ = CUTS[-1]
    return [os.path.join(CLIPS, src), round(a + d - 0.05, 3)]


if __name__ == "__main__":
    build()
