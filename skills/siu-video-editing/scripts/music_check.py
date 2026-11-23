# Vet a music track before building on it (Claude cannot listen, so measure):
#   tempo, beat grid, downbeats, loudness per bar  -> <track>.beats.json (the edit is cut on this grid)
#   loopiness: % of bars nearly identical to the bar 2/4/8 bars earlier. Measured: "Fun Vibe" 73 % and stock "Telecasted"
#              tracks 95-98 % were rejected by the user as "loops again and again"; the accepted "Circa 1983" scored 29 %.
#              Reject > ~50 %.
#   sections:  biggest 4-bar novelty changes (where a drop / section change lands -> put the big moment there)
#   --lyrics:  faster-whisper with VAD; any real words = the track has vocals ("Time of your life" had lyrics about drinking).
#              A lone "Thank you." / "Subscribe" on an intro is a hallucination - check the timestamps.
#   python music_check.py track.mp3 [track2.mp3 ...] [--lyrics] [--model small]
import json, sys
import numpy as np
import librosa


def grid(path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time", tightness=120)
    tempo = float(np.atleast_1d(tempo)[0])
    rms = librosa.feature.rms(y=y, hop_length=512)[0]; rt = librosa.times_like(rms, sr=sr, hop_length=512)
    low = librosa.onset.onset_strength(y=y, sr=sr, fmax=200); ot = librosa.times_like(low, sr=sr)
    strength = [np.mean([low[np.argmin(abs(ot - b))] for b in beats[p::4]]) for p in range(4)]   # downbeat = strongest bass phase
    phase = int(np.argmax(strength)); downs = beats[phase::4]
    bars = [(float(a), float(20 * np.log10(np.mean(rms[(rt >= a) & (rt < b)]) + 1e-9))) for a, b in zip(downs, downs[1:])]
    g = dict(tempo=tempo, beats=[float(b) for b in beats], downbeats=[float(d) for d in downs], bar_db=bars)
    json.dump(g, open(path.rsplit(".", 1)[0] + ".beats.json", "w"), indent=0)
    return y, sr, g


def loopiness(y, sr, g):
    downs = np.array(g["downbeats"])
    ch = librosa.feature.chroma_cqt(y=y, sr=sr); mf = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13); t = librosa.times_like(ch, sr=sr)
    V = []
    for a, b in zip(downs, downs[1:]):
        m = (t >= a) & (t < b)
        if m.sum() < 3: continue
        v = np.concatenate([ch[:, m].mean(1) / (np.linalg.norm(ch[:, m].mean(1)) + 1e-9), mf[1:, m].mean(1) / 60])
        V.append(v / (np.linalg.norm(v) + 1e-9))
    V = np.array(V); S = V @ V.T
    rep = float(np.mean([max(S[i, i - k] for k in (2, 4, 8) if i - k >= 0) > 0.985 for i in range(8, len(V))])) if len(V) > 9 else 0.0
    # 4-bar block novelty: dissimilarity between the 4 bars before and after each bar line
    nov = [(float(downs[i]), float(1 - (V[i - 4:i].mean(0) @ V[i:i + 4].mean(0)) /
                                   (np.linalg.norm(V[i - 4:i].mean(0)) * np.linalg.norm(V[i:i + 4].mean(0)) + 1e-9)))
           for i in range(4, len(V) - 4)]
    return rep, sorted(nov, key=lambda r: -r[1])[:5]


def lyrics(path, model):
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, info = m.transcribe(path, vad_filter=True, beam_size=5)
    segs = [s for s in segs if s.no_speech_prob < 0.6 and len(s.text.split()) >= 2]
    return info.language, segs


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--") and a != (sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else None)]
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "small"
    for f in files:
        y, sr, g = grid(f)
        rep, nov = loopiness(y, sr, g)
        db = [d for _, d in g["bar_db"]]
        period = float(np.median(np.diff(g["beats"]))) if len(g["beats"]) > 1 else 0
        verdict = "REJECT (loops)" if rep > 0.5 else "ok"
        print(f"\n== {f}\n   tempo {g['tempo']:.1f} BPM (beat {period:.3f} s, bar {4 * period:.2f} s), {len(g['downbeats'])} bars, "
              f"first downbeat {g['downbeats'][0]:.2f} s\n   near-identical bar repeats {100 * rep:.0f} %  -> {verdict}\n"
              f"   bar loudness {min(db):.0f}..{max(db):.0f} dB\n   biggest section changes (bar line s, novelty): "
              + ", ".join(f"{t:.2f} ({v:.2f})" for t, v in nov))
        bd = g["bar_db"]
        jumps = sorted(((bd[i][0], np.mean([d for _, d in bd[i:i + 2]]) - np.mean([d for _, d in bd[max(0, i - 2):i]]))
                        for i in range(2, len(bd) - 1)), key=lambda r: -r[1])[:4]
        print("   biggest loudness jumps = drops (bar line s, +dB): " + ", ".join(f"{t:.2f} (+{v:.0f})" for t, v in jumps if v > 2))
        print("   bar dB: " + " ".join(f"{a:.0f}:{d:.0f}" for a, d in g["bar_db"]))
        if "--lyrics" in sys.argv:
            lang, segs = lyrics(f, model)
            words = sum(len(s.text.split()) for s in segs)
            print(f"   lyrics check: {words} words in {len(segs)} segments (lang guess {lang}) -> {'HAS VOCALS' if words > 6 else 'instrumental (check any hits)'}")
            for s in segs[:8]: print(f"     [{s.start:6.1f}-{s.end:6.1f}] {s.text.strip()}")


if __name__ == "__main__":
    main()
