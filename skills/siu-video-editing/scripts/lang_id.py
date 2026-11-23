# Which language is spoken WHERE, then a transcript of each stretch in its own language.
# Why: the tiếng Nga reel's teacher switched between Russian and Vietnamese; we subtitled his Vietnamese as if it were Russian
# until the user pointed it out, and the client's "transcript" was a machine translation of his Vietnamese INTO Russian.
# Stretches = speech between pauses (silencedetect), merged to >= 3 s (language ID is unreliable on short windows).
# Whisper on PA / reverberant audio hallucinates ("Hãy subscribe cho kênh", "Субтитры создавал...", "Thank you."): treat
# any line with low avg log-prob, or text that has nothing to do with the event, as a guess; never ship it unreviewed.
#   python lang_id.py <video_or_audio> [--langs vi,ru,en] [--model large-v3] [--json out.json]
import json, re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio


HALLUCINATIONS = ("subscribe", "đăng ký kênh", "la la school", "продолжение следует", "субтитр", "корректор", "редактор",
                  "thank you for watching", "hẹn gặp lại các bạn", "cảm ơn các bạn đã theo dõi", "ghiền mì gõ", "amara.org",
                  "dimatorzok", "игорь негода")


def opt(n, d): return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


def stretches(path, noise="-30dB", min_sil=0.35, min_len=3.0, max_len=8.0):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=noise={noise}:d={min_sil}", "-vn", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore").stderr
    dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", r).groups()[2]) + 60 * float(re.search(r"Duration: (\d+):(\d+)", r).group(2)) \
        + 3600 * float(re.search(r"Duration: (\d+)", r).group(1))
    s_on = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]; s_off = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    speech, t = [], 0.0
    for a, b in zip(s_on, s_off + [dur]):
        if a - t > 0.25: speech.append([t, a])
        t = b
    if dur - t > 0.25: speech.append([t, dur])
    merged = []
    for a, b in speech:                                    # merge short stretches into their neighbour
        short = b - merged[-1][0] < min_len or merged[-1][1] - merged[-1][0] < min_len if merged else False
        if merged and short and a - merged[-1][1] < 1.2 and b - merged[-1][0] <= max_len:
            merged[-1][1] = b
        else: merged.append([a, b])
    out = []                                               # PA audio has few clean pauses: cap windows so one language
    for a, b in merged:                                    # switch or applause does not hide inside a long window
        n = max(1, int(np.ceil((b - a) / max_len)))
        out += [[a + k * (b - a) / n, a + (k + 1) * (b - a) / n] for k in range(n)]
    return out


def main():
    path = sys.argv[1]
    langs = opt("--langs", "vi,ru,en").split(",")
    m = WhisperModel(opt("--model", "large-v3"), device="cpu", compute_type="int8")
    audio = decode_audio(path, 16000)
    # pass 1: language per short window (switches are found at window resolution)
    wins = []
    for a, b in stretches(path):
        lang, p, allp = m.detect_language(audio[int(a * 16000):int(b * 16000)])
        probs = {l: pr for l, pr in allp}
        best = max(langs, key=lambda l: probs.get(l, 0))
        wins.append([a, b, best, probs.get(best, 0)])
    # pass 2: transcribe merged same-language spans (longer context = better text)
    spans = []
    for a, b, l, pr in wins:
        if spans and spans[-1][2] == l and a - spans[-1][1] < 1.2: spans[-1][1] = b; spans[-1][3] = min(spans[-1][3], pr)
        else: spans.append([a, b, l, pr])
    rows = []
    for a, b, best, pr in spans:
        segs, _ = m.transcribe(audio[int(a * 16000):int(b * 16000)], language=best, beam_size=5, vad_filter=False,
                               condition_on_previous_text=False)
        segs = list(segs)
        for s in segs:
            text = s.text.strip()
            halluc = any(h in text.lower() for h in HALLUCINATIONS)
            flag = "  (HALLUCINATION: ignore)" if halluc else "  (weak: check by ear)" if s.avg_logprob < -0.8 or pr < 0.6 else ""
            s0, s1 = min(a + s.start, b), min(a + s.end, b)          # Whisper pads to 30 s: clamp to the span
            rows.append(dict(a=round(s0, 2), b=round(s1, 2), lang=best, p=round(pr, 2), logprob=round(s.avg_logprob, 2),
                             text=text, hallucination=halluc))
            print(f"{s0:6.2f}-{s1:6.2f}  {best} p>={pr:.2f}  lp={s.avg_logprob:5.2f}  {text}{flag}", flush=True)
    if "--json" in sys.argv: json.dump(rows, open(opt("--json", "lang.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
