# Which reading of an unclear phrase fits the AUDIO? Whisper forced alignment gives the probability of every token of a GIVEN
# text for a window of audio; mean log-prob near 0 = fits, below about -2 = does not fit. Use it to judge a client's transcript
# against your ASR passes window by window (tiếng Nga reel: the client's opening line scored -4.49, "Дорогие мои ученики" -0.10).
# Caveat: it favours Whisper's own wording, so a small gap proves little; a big gap does. It cannot read what nobody heard.
#   python score_text.py <audio_or_video> <lang> <candidates.json> [--model large-v3]
#   candidates.json = [{"a": 0.0, "b": 2.7, "cands": [["client", "Рад я ..."], ["whisper", "Дорогие мои ученики!"]]}, ...]
import json, subprocess, sys, tempfile, os
import numpy as np
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio, pad_or_trim
from faster_whisper.tokenizer import Tokenizer

src, lang, cand = sys.argv[1], sys.argv[2], sys.argv[3]
model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "large-v3"
m = WhisperModel(model, device="cpu", compute_type="int8")
tok = Tokenizer(m.hf_tokenizer, True, task="transcribe", language=lang)
audio = decode_audio(src, 16000)
out = []
for w in json.load(open(cand, encoding="utf-8")):
    seg = audio[int(w["a"] * 16000): int(w["b"] * 16000)]
    feats = m.feature_extractor(seg); n = feats.shape[-1]
    enc = m.encode(pad_or_trim(feats))
    print(f"\n== {w['a']:.1f}-{w['b']:.1f} s")
    for label, text in w["cands"]:
        ids = tok.encode(" " + text.strip())
        r = m.model.align(enc, tok.sot_sequence, [ids], n)[0]
        p = np.clip(np.array(r.text_token_probs), 1e-6, 1)
        words, wt = tok.split_to_word_tokens(ids + [tok.eot])
        k, wp = 0, []
        for word, toks in zip(words[:-1], wt[:-1]):
            wp.append((word.strip(), float(np.exp(np.log(p[k:k + len(toks)]).mean())))); k += len(toks)
        score = float(np.log(p).mean())
        weak = " ".join(f"{a}({b:.2f})" for a, b in wp if b < 0.2)
        print(f"  {score:6.2f}  [{label}] {text}\n          weak words: {weak or '-'}")
        out.append(dict(a=w["a"], b=w["b"], label=label, text=text, score=round(score, 3), words=wp))
json.dump(out, open(os.path.splitext(cand)[0] + "_scores.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
