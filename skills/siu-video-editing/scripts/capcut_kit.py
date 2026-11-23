# capcut_kit.py - build a LAYERED, portable CapCut desktop project with pycapcut 0.0.4 (tested: CapCut 9.8 on Windows).
# Every rule in here was paid for by a real mistake (see references/capcut-pipeline.md and references/lessons-learned.md):
#   * keyframes of VIDEO/AUDIO segments are in SOURCE time (CapCut counts from the start of the media file): use kf_time()
#     (a clip-relative time moved the music ducking 53 s early in the Mỹ Tho v4 project);
#     TEXT keyframes are segment-relative.
#   * animation / transition / fade durations must be STRINGS ("0.4s"): a number is read as MICROseconds (v4 shipped 0 us intros).
#   * transitions go on the clip BEFORE the cut, and must be attached before add_segment().
#   * source ranges use floor(target_us * speed), or neighbouring pieces overlap by 1 us.
#   * auto_wrapping=False always (CapCut breaks words mid-word: "Giọng ca và / ng!"); break lines by hand, fit width with PIL.
#   * text size = px / K[font]  (K measured from a CapCut 9.8 export, 1080x1920 canvas). Unknown font -> calibrate (see docs).
#   * media is copied into <draft>/media and the zipped draft carries a TOKEN instead of this PC's path; the bundled installer
#     (scripts/capcut_install) copies the project into CapCut's folder on the client's PC and swaps the token back.
#   * AudioMaterial refuses files with a video stream: extract a .wav first.
#
#   from capcut_kit import Project, F, T, TI, TO, FX, KP, hexrgb
#   p = Project("SIU_Demo")                        # 1080x1920 30 fps draft in CapCut's project folder (replaced if it exists)
#   p.tracks(video=["Footage", "Graphics"], text=["Title", "Subtitles"], audio=["Music", "Voice"])
#   s = p.video("clip.mp4", start=0, dur=3, src=12.0, track="Footage")
#   p.text("Title", "Học tập thực tế", 0.3, 2.5, x=540, y=420, px=96, font=F.Montserrat, color=hexrgb("#BB1C3D"), bold=True)
#   p.music("music.mp3", 0, 30, src=49.0, gains=[(0, 1.0), (5, 0.18), (25, 0.18), (26, 1.0)], track="Music")
#   p.save(); p.package("out/SIU_Demo_CapCut.zip", guide_title="SIU – Demo")
#
#   python capcut_kit.py --free            list CapCut elements pycapcut marks as free (CapCut may still flag some as Pro!)
#   python capcut_kit.py --fonts           which downloaded CapCut fonts cover Vietnamese / Cyrillic
#   python capcut_kit.py --selftest        unit checks of the time / size maths (no CapCut needed)
import glob, json, math, os, re, shutil, sys, unicodedata, zipfile

US = lambda s: int(round(s * 1_000_000))
nfc = lambda s: unicodedata.normalize("NFC", s)          # macOS/Word text can arrive decomposed; CapCut fonts want NFC
hexrgb = lambda h: tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
TOKEN = "__CAPCUT_DRAFT_DIR__"
HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = os.environ.get("LOCALAPPDATA", "")
CACHE = os.path.join(LOCAL, "CapCut", "User Data", "Cache", "effect")


def drafts_dir():
    """CapCut's project folder: the custom path from Settings > Projects if set, else the default."""
    root = os.path.join(LOCAL, "CapCut", "User Data", "Projects", "com.lveditor.draft")
    cfg = os.path.join(LOCAL, "CapCut", "User Data", "Config", "globalSetting")
    if os.path.exists(cfg):
        m = re.search(r"^currentCustomDraftPath=(.+)$", open(cfg, encoding="utf-8", errors="ignore").read(), re.M)
        if m and os.path.isdir(m.group(1).strip()): root = m.group(1).strip()
    return os.path.normpath(root)                        # the setting may use "/" : one spelling everywhere


try:
    import pycapcut as cc
    from pycapcut import trange, ClipSettings, TextStyle, TextShadow, TextBorder, TextBackground, KeyframeProperty as KP
    from pycapcut.metadata import (TransitionType as T, TextIntro as TI, TextOutro as TO, TextLoopAnim as TL, FontType as F,
                                   VideoSceneEffectType as FX, MaskType, FilterType)
except ImportError:                                       # --fonts / --selftest work without pycapcut
    cc = None

# em size in px of a size-1 text on a 1080-wide canvas, measured from CapCut 9.8 exports ("HIH" at size 10, tiếng Nga reel).
# The bold flag does not change the width. Coiny 3.5 +- 0.2: CapCut 9.8 preview (2026-11-24) and the client's export (3.42).
K = {"Montserrat": 5.14, "Anton": 4.3, "PlayfairDisplay_Italic": 4.65, "Prata_Regular": 4.63, "Classic": 6.3, "Coiny_Regular": 3.5}
FONTFILE = {"Montserrat": "Montserrat-Bold.otf", "Anton": "Anton-Regular.ttf", "PlayfairDisplay_Italic": "PlayfairDisplay-Italic*.ttf",
            "Prata_Regular": "Prata-Regular.ttf", "Classic": "TikTok-Display-Medium.ttf", "Coiny_Regular": "Coiny-Regular.ttf"}


def text_width(text, font_name, px, spacing=0.0):
    """Rendered width (px) of the widest line, measured on the font file CapCut downloaded (None if not cached yet)."""
    from PIL import ImageFont
    hits = glob.glob(os.path.join(CACHE, "*", "*", FONTFILE.get(font_name, "~none~")))
    if not hits: return None
    f = ImageFont.truetype(hits[0], max(1, int(round(px))))
    return max(f.getlength(line) + len(line) * spacing * 0.05 * px for line in text.split("\n"))


def fit_px(text, font_name, px, maxw, spacing=0.0):
    """Largest px <= px whose widest line fits maxw. Falls back to 0.6 em per character when the font is not cached."""
    w = text_width(text, font_name, px, spacing)
    if w is None: w = 0.6 * px * max(len(l) for l in text.split("\n"))
    return min(px, px * maxw / max(w, 1e-6))


class Project:
    def __init__(self, name, width=1080, height=1920, fps=30, root=None):
        assert cc, "pip install pycapcut==0.0.4 (0.1.0 renames the track API)"
        self.name, self.W, self.H, self.fps = name, width, height, fps
        self.root = os.path.normpath(root or drafts_dir())
        self.script = cc.DraftFolder(self.root).create_draft(name, width, height, fps, allow_replace=True)
        self.dir = os.path.join(self.root, name)
        self.media = os.path.join(self.dir, "media"); os.makedirs(self.media, exist_ok=True)
        self._mats, self._n, self._sfx = {}, {}, []

    # ---------------------------------------------------------------- tracks: one named track per element (client edits them)
    def tracks(self, video=(), text=(), audio=(), effect=()):
        for kind, names in ((cc.TrackType.video, video), (cc.TrackType.text, text), (cc.TrackType.audio, audio),
                            (cc.TrackType.effect, effect)):
            for n in names:
                i = self._n.get(kind, 0); self.script.add_track(kind, n, relative_index=i); self._n[kind] = i + 1

    def mat(self, path, audio=False):
        """Copy media into <draft>/media once and return its material (the zip ships this folder)."""
        dst = os.path.join(self.media, os.path.basename(path))
        key = (dst, audio)
        if key not in self._mats:
            if not os.path.exists(dst): shutil.copy2(path, dst)
            self._mats[key] = cc.AudioMaterial(dst) if audio else cc.VideoMaterial(dst)
        return self._mats[key]

    # ---------------------------------------------------------------- picture
    def pos(self, x, y):
        """Canvas px of the element CENTRE -> CapCut transform (half-canvas units, +y is UP)."""
        return dict(transform_x=(x - self.W / 2) / (self.W / 2), transform_y=(self.H / 2 - y) / (self.H / 2))

    def video(self, path, start, dur, src=0.0, speed=1.0, vol=0.0, track=None, x=None, y=None, scale=1.0, transition=None,
              settings=None, add=True):
        """Video or still on `track`. vol=0 by default: source sound is MUTED unless the brief says the clip carries voice.
        transition=(T.X, "0.4s") goes on THIS clip and plays at its END (into the next clip on the same track)."""
        m = self.mat(path)
        tgt = trange(US(start), US(dur))
        srcr = cc.Timerange(0, tgt.duration) if m.material_type == "photo" else cc.Timerange(US(src), int(math.floor(tgt.duration * speed)))
        if settings is None:
            settings = ClipSettings(scale_x=scale, scale_y=scale, **self.pos(x if x is not None else self.W / 2, y if y is not None else self.H / 2))
        seg = cc.VideoSegment(m, tgt, source_timerange=srcr, speed=speed, volume=vol, clip_settings=settings)
        if transition: seg.add_transition(transition[0], duration=transition[1])
        if add and track: self.script.add_segment(seg, track)
        return seg

    @staticmethod
    def kf_time(seg, t):
        """Keyframe time for `t` seconds after the segment's start on the timeline (see header: source time vs relative)."""
        if cc and isinstance(seg, cc.TextSegment): return US(t)
        return seg.source_timerange.start + int(US(t) * seg.speed.speed)

    def keys(self, seg, prop, pairs):
        """pairs = [(t_seconds_from_segment_start, value), ...]."""
        for t, v in pairs: seg.add_keyframe(prop, self.kf_time(seg, t), v)
        return seg

    # ---------------------------------------------------------------- text
    def text(self, track, t, start, dur, x, y, px, font, color, *, bold=False, maxw=900, align=1, spacing=0.0, line_spacing=0,
             border=None, border_w=40.0, bg=None, shadow=True, intro=None, intro_d="0.3s", outro=None, outro_d="0.25s", loop=None,
             highlight=(), hl_color=None, rotation=0.0):
        """CapCut text whose CENTRE is at (x, y) px and whose widest line is <= maxw px. Returns the segment (px used in .px)."""
        t = nfc(t)
        fname = font.name
        px = fit_px(t, fname, px, maxw, spacing)
        k = K.get(fname)
        if k is None: print(f"WARNING: no measured K for font {fname}; size guessed (calibrate: references/capcut-pipeline.md)")
        seg = _Text(t, trange(US(start), US(dur)), font=font, highlight=[nfc(h) for h in highlight], hl_color=hl_color or hexrgb("#FFD23F"),
                    style=TextStyle(size=round(px / (k or 5.0), 2), bold=bold, color=color, align=align, auto_wrapping=False,
                                    letter_spacing=spacing, line_spacing=line_spacing),
                    clip_settings=ClipSettings(rotation=rotation, **self.pos(x, y)),
                    border=TextBorder(color=border, width=border_w) if border else None, background=bg,
                    shadow=TextShadow(alpha=0.5, color=(0, 0, 0), diffuse=14, distance=4) if shadow else None)
        if intro: seg.add_animation(intro, intro_d)
        if outro: seg.add_animation(outro, outro_d)
        if loop: seg.add_animation(loop)
        seg.px = px
        self.script.add_segment(seg, track)
        return seg

    # ---------------------------------------------------------------- sound
    def audio(self, path, start, dur, src=0.0, vol=1.0, track=None, fade=None):
        seg = cc.AudioSegment(self.mat(path, audio=True), trange(US(start), US(dur)), source_timerange=trange(US(src), US(dur)), volume=vol)
        if fade: seg.add_fade(*fade)
        if track: self.script.add_segment(seg, track)
        return seg

    def music(self, path, start, dur, src=0.0, gains=(), track="Music", fade=("0.05s", "1.5s")):
        """Music bed with volume keyframes. gains = [(timeline_s, linear_gain)] (e.g. 0.18 ~ -15 dB under a voice).
        Keyframes are written in SOURCE time via kf_time() - check the waveform envelope in CapCut once."""
        seg = self.audio(path, start, dur, src, 1.0, None, fade)
        for t, g in gains:                                # every breakpoint: equal neighbours are HOLDS, never drop them
            if start <= t <= start + dur:
                seg.add_keyframe(self.kf_time(seg, t - start), g)
        self.script.add_segment(seg, track)
        return seg

    def sfx(self, t, path, vol=0.5, prefix="SFX"):
        """Sound effect at timeline t; opens a new 'SFX n' track whenever the existing ones are busy."""
        self._sfx.append((t, path, vol, prefix))

    def _place_sfx(self):
        busy = {}
        for t, path, vol, prefix in sorted(self._sfx, key=lambda r: r[0]):
            m = self.mat(path, audio=True); d = m.duration / 1e6
            lanes = busy.setdefault(prefix, [])
            k = next((i for i, end in enumerate(lanes) if end <= t), None)
            if k is None:
                lanes.append(0.0); k = len(lanes) - 1; self.tracks(audio=[f"{prefix} {k + 1}"])
            self.script.add_segment(cc.AudioSegment(m, trange(US(max(0.0, t)), US(d)), volume=vol), f"{prefix} {k + 1}")
            lanes[k] = t + d

    def effect(self, kind, start, dur, track):
        self.script.add_effect(kind, trange(US(start), US(dur)), track)

    # ---------------------------------------------------------------- save + hand-over
    def save(self):
        self._place_sfx(); self._sfx = []
        self.script.save()
        return self.dir

    def package(self, zip_path, guide_title=None, extra=()):
        """Portable zip: <name>/draft_content.json (paths -> TOKEN), draft_meta_info.json, media/, + installer and guide.
        Fails loudly if any path of this PC is left in the draft."""
        return package(self.dir, zip_path, guide_title or self.name, extra)


class _Text(cc.TextSegment if cc else object):
    """TextSegment with coloured keyword ranges (CapCut keeps one style entry per character range)."""
    def __init__(self, *a, highlight=(), hl_color=(1.0, 0.82, 0.25), **k):
        super().__init__(*a, **k); self.hl, self.hl_color = list(highlight), hl_color

    def export_material(self):
        ret = super().export_material()
        if not self.hl: return ret
        c = json.loads(ret["content"]); base = c["styles"][0]; spans, pos = [], 0
        for w in self.hl:
            i = self.text.find(w, pos)
            if i >= 0: spans.append((i, i + len(w))); pos = i + len(w)
        styles, pos = [], 0
        for i, j in spans + [(len(self.text), len(self.text))]:
            for a, b, col in ((pos, i, None), (i, j, self.hl_color)):
                if b > a:
                    s = json.loads(json.dumps(base)); s["range"] = [a, b]
                    if col: s["fill"]["content"]["solid"]["color"] = list(col)
                    styles.append(s)
            pos = j
        c["styles"] = styles; ret["content"] = json.dumps(c, ensure_ascii=False)
        return ret


def portable(raw, draft_dir):
    """Replace this PC's draft folder (both slash styles, JSON-escaped) by TOKEN in draft_content.json text."""
    out = raw
    d = os.path.normpath(draft_dir)
    for form in {draft_dir, d, d.replace("\\", "/")}:
        esc = json.dumps(form)[1:-1]
        out = out.replace(esc + "\\\\media\\\\", TOKEN + "/media/").replace(esc + "/media/", TOKEN + "/media/")
        out = out.replace(esc + "\\\\media", TOKEN + "/media").replace(esc + "/media", TOKEN + "/media")
    return out


def package(draft_dir, zip_path, guide_title, extra=()):
    draft_dir = os.path.normpath(draft_dir)
    name = os.path.basename(draft_dir)
    raw = open(os.path.join(draft_dir, "draft_content.json"), encoding="utf-8").read()
    out = portable(raw, draft_dir)
    user = os.environ.get("USERNAME") or os.environ.get("USER") or "~none~"
    left = [m.group(0) for m in re.finditer(r'"path"\s*:\s*"([^"]*)"', out) if user in m.group(1) or ":\\\\" in m.group(1)]
    assert not left and out.count(TOKEN) > 0, f"machine-specific media paths left in the draft: {left[:3]}"
    json.loads(out)
    inst = os.path.join(HERE, "capcut_install")
    guide = open(os.path.join(inst, "HUONG_DAN.txt"), encoding="utf-8-sig").read().replace("{TITLE}", guide_title).replace("{NAME}", name)
    os.makedirs(os.path.dirname(os.path.abspath(zip_path)), exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in ("CAI_DAT_PROJECT.bat", "cai_dat_project.ps1"): z.write(os.path.join(inst, fn), fn)
        z.writestr("HUONG_DAN.txt", "\ufeff" + guide)
        for f in extra: z.write(f, os.path.basename(f))
        z.writestr(f"{name}/draft_content.json", out)
        z.write(os.path.join(draft_dir, "draft_meta_info.json"), f"{name}/draft_meta_info.json")
        for fn in sorted(os.listdir(os.path.join(draft_dir, "media"))):
            z.write(os.path.join(draft_dir, "media", fn), f"{name}/media/{fn}", compress_type=zipfile.ZIP_STORED)
    n_media = len(os.listdir(os.path.join(draft_dir, "media")))
    print(f"zip: {zip_path}  {os.path.getsize(zip_path) / 1e6:.0f} MB, {out.count(TOKEN)} media paths portable, {n_media} media files")
    return zip_path


# ------------------------------------------------------------------------------------------------------------------- CLI
def _free():
    import pycapcut.metadata as md
    for E in (md.TransitionType, md.TextIntro, md.TextOutro, md.TextLoopAnim, md.IntroType, md.OutroType, md.VideoSceneEffectType):
        free = [m.name for m in E if not getattr(m.value, "is_vip", False)]
        print(f"== {E.__name__}: {len(free)} free\n  " + ", ".join(free))
    print("\nKnown wrong flags (CapCut 9.8 asked for Pro at export): TextIntro.向上滑动 'Slide Up'. Always run the export Pro check.")


def _fonts():
    from PIL import ImageFont, Image, ImageDraw
    vi = "ẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸĐđơưăâêôạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ"
    ru = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    def r(font, c):
        im = Image.new("L", (90, 90)); ImageDraw.Draw(im).text((10, 10), c, font=font, fill=255); return im.tobytes()
    files = sorted(glob.glob(CACHE + "/*/*/*.[ot]t[fc]"))
    if not files: print("No fonts in", CACHE, "- CapCut downloads a font only when a draft that uses it is opened.")
    for f in files:
        try: font = ImageFont.truetype(f, 40)
        except Exception as e: print("ERR", f, e); continue
        nd = r(font, "\uffff"); miss = lambda s: sum(r(font, c) == nd for c in s)
        mv, mr = miss(vi), miss(ru)
        print(f"vi-missing {mv:3d}  ru-missing {mr:3d}  {os.path.basename(f)}")


def _selftest():
    assert US(0.4) == 400000 and US(1 / 3) == 333333
    assert nfc("Ho\u0300") == "Hò"
    raw = json.dumps({"path": r"C:\Users\x\D\P\media\a.mp4", "p2": "C:/Users/x/D/P/media/b.wav"})
    out = portable(raw, r"C:\Users\x\D\P")
    assert out.count(TOKEN) == 2 and "Users" not in out, out
    if os.name == "nt":                                    # CapCut's setting may give "C:/.../com.lveditor.draft" + "\\name"
        out = portable(raw, "C:/Users/x/D\\P")
        assert out.count(TOKEN) == 2 and "Users" not in out, out
    class S:                                               # kf_time: source start 53 s, speed 1 -> t=2 s is 55 s of the file
        source_timerange = type("R", (), {"start": US(53)})(); speed = type("Sp", (), {"speed": 1.0})()
    assert Project.kf_time(S(), 2.0) == US(55)
    S.speed.speed = 2.0; assert Project.kf_time(S(), 2.0) == US(57)
    assert fit_px("a" * 10, "~nofont~", 100, 300) == 50.0
    print("selftest ok")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--selftest"
    {"--free": _free, "--fonts": _fonts, "--selftest": _selftest}[arg]()
