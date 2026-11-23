# Synthesised SFX kit (no licence questions at all) -> <out_dir>/*.wav, 48 kHz stereo, peak-normalised to -3 dBFS.
# Noise-based sounds are shaped in the STFT domain (moving band-pass), so whooshes actually sweep instead of hissing.
# whoosh, whoosh_short, swish_up, riser (2 s), impact, glitch | pop, bubble, shutter, sparkle, tick |
# contextual: bee, sizzle (wok), splash, horn (boat), kaching, heart.   Mix SFX ~55 % under a voice-over.
#   python sfx_gen.py <out_dir>
import os, sys
import numpy as np
from scipy.signal import stft, istft, butter, sosfilt, fftconvolve
import scipy.io.wavfile as wav

SR = 48000
OUT = sys.argv[1] if len(sys.argv) > 1 else "sfx"
rng = np.random.default_rng(11)
t_ = lambda s: np.arange(int(s * SR)) / SR
bp = lambda x, lo, hi: sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)


def shaped_noise(sec, centre, width, env):
    """Noise whose band centre (Hz) and width (octaves) follow functions of normalised time u in [0,1]."""
    n = rng.standard_normal(int(sec * SR))
    f, tt, Z = stft(n, SR, nperseg=1024)
    u = tt / sec
    c = centre(u)[None, :]; w = width(u)[None, :]
    mask = np.exp(-0.5 * (np.log2((f[:, None] + 1) / c) / w) ** 2)
    _, y = istft(Z * mask, SR, nperseg=1024)
    y = y[: len(n)]
    return y * env(np.linspace(0, 1, len(y)))


def verb(x, sec=0.8, mix=0.25):
    ir = rng.standard_normal(int(sec * SR)) * np.exp(-t_(sec) / (sec / 5)); ir = lp(ir, 7000); ir /= np.sqrt((ir ** 2).sum())
    return x + mix * fftconvolve(x, ir)[: len(x)]


def stereo(x, pan=None):
    if pan is None: return np.stack([x, x], 1)
    p = pan(np.linspace(0, 1, len(x)))  # -1 left .. +1 right
    return np.stack([x * np.sqrt((1 - p) / 2), x * np.sqrt((1 + p) / 2)], 1)


def save(name, x):
    x = np.asarray(x, float)
    if x.ndim == 1: x = stereo(x)
    fade = min(len(x) // 10, int(0.01 * SR)); x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.708
    wav.write(os.path.join(OUT, name + ".wav"), SR, (x * 32767).astype(np.int16))


os.makedirs(OUT, exist_ok=True)
bell = lambda u: np.sin(np.pi * np.clip(u, 0, 1)) ** 2

# transitions
save("whoosh", stereo(verb(shaped_noise(0.55, lambda u: 300 * 2 ** (4 * bell(u)), lambda u: 0.9 + 0 * u, lambda u: bell(u) ** 1.3), 0.5, 0.15), lambda u: -0.8 + 1.6 * u))
save("whoosh_short", stereo(shaped_noise(0.3, lambda u: 600 * 2 ** (3 * u), lambda u: 0.7 + 0 * u, lambda u: np.sin(np.pi * u) ** 1.5), lambda u: 0.7 - 1.4 * u))
save("swish_up", shaped_noise(0.25, lambda u: 1500 * 2 ** (2.5 * u), lambda u: 0.5 + 0 * u, lambda u: u ** 1.5 * (1 - u) ** 0.3 * 2))
t = t_(2.0)
rise = shaped_noise(2.0, lambda u: 250 * 2 ** (5 * u ** 1.6), lambda u: 0.6 + 0 * u, lambda u: u ** 2.2)
rise += 0.35 * np.sin(2 * np.pi * np.cumsum(180 + 900 * (t / 2.0) ** 2) / SR) * (t / 2.0) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * (4 + 14 * t / 2.0) * t))
save("riser", verb(rise, 1.2, 0.3))
t = t_(1.8)
boom = np.sin(2 * np.pi * np.cumsum(34 + 70 * np.exp(-t / 0.07)) / SR) * np.exp(-t / 0.45)
crack = hp(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.35) * 0.35 + bp(rng.standard_normal(len(t)), 200, 1200) * np.exp(-t / 0.05) * 0.6
save("impact", verb(np.tanh(1.8 * (boom + crack)), 1.5, 0.35))
t = t_(0.9)
save("glitch", np.concatenate([np.sign(np.sin(2 * np.pi * f * t_(0.04))) * 0.4 * hp(rng.standard_normal(int(0.04 * SR)), 1500) for f in (1200, 600, 2400, 300, 1800)]))

# UI / sticker
t = t_(0.14)
save("pop", np.sin(2 * np.pi * np.cumsum(1100 * np.exp(-t / 0.03) + 280) / SR) * np.exp(-t / 0.04) + 0.15 * hp(rng.standard_normal(len(t)), 3000) * np.exp(-t / 0.004))
t = t_(0.18)
save("bubble", np.sin(2 * np.pi * np.cumsum(300 + 1500 * (t / 0.18) ** 1.5) / SR) * np.sin(np.pi * t / 0.18) ** 0.6)
t = t_(0.3)
click = lambda d: hp(rng.standard_normal(len(t)), 2000) * np.exp(-np.maximum(t - d, 0) / 0.008) * (t >= d)
save("shutter", click(0.0) + 0.7 * click(0.075) + 0.25 * bp(rng.standard_normal(len(t)), 400, 2000) * np.exp(-t / 0.05))
t = t_(1.2); sp = np.zeros(len(t))
for k, (d, f) in enumerate([(0, 2637), (0.06, 3136), (0.12, 3951), (0.19, 5274), (0.27, 4699)]):
    m = t >= d; sp[m] += np.sin(2 * np.pi * f * (t[m] - d)) * np.exp(-(t[m] - d) / 0.25) * (0.9 - 0.12 * k)
save("sparkle", verb(sp, 1.0, 0.4))
t = t_(0.05); save("tick", hp(rng.standard_normal(len(t)), 3000) * np.exp(-t / 0.006))

# contextual
t = t_(1.6)
f0 = 210 + 18 * np.sin(2 * np.pi * 0.9 * t) + 6 * np.sin(2 * np.pi * 7 * t)
saw = 2 * ((np.cumsum(f0) / SR) % 1) - 1
buzz = bp(saw * (0.75 + 0.25 * np.sin(2 * np.pi * 28 * t)), 250, 3500) * np.sin(np.pi * t / 1.6) ** 0.7
save("bee", stereo(buzz, lambda u: np.sin(2 * np.pi * 0.8 * u)))
t = t_(2.0)
crackle = np.zeros(len(t)); idx = rng.integers(0, len(t), 900); crackle[idx] = rng.standard_normal(900) * rng.random(900) ** 3
save("sizzle", hp(crackle, 2500) * 1.5 + 0.25 * bp(rng.standard_normal(len(t)), 4000, 12000) * (0.8 + 0.2 * np.sin(2 * np.pi * 3 * t)))
t = t_(1.3)
spl = lp(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.18) + 0.4 * bp(rng.standard_normal(len(t)), 600, 5000) * np.exp(-t / 0.45)
for d in rng.uniform(0.1, 0.9, 10):
    m = t >= d; spl[m] += 0.12 * np.sin(2 * np.pi * np.cumsum(np.full(m.sum(), rng.uniform(500, 1400)) * (1 + (t[m] - d) * 3)) / SR) * np.exp(-(t[m] - d) / 0.03)
save("splash", verb(spl, 0.7, 0.2))
t = t_(1.4)
horn = sum(a * (2 * ((f * t) % 1) - 1) for f, a in ((110, 1), (110.8, 0.8), (165, 0.6), (220, 0.3)))
save("horn", verb(lp(horn, 900) * np.minimum(1, t / 0.08) * np.minimum(1, (1.4 - t) / 0.25), 1.2, 0.4))
t = t_(1.0)
ka = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, d in ((2093, 0.5), (3520, 0.35), (5274, 0.2), (2637, 0.6)))
save("kaching", verb(np.concatenate([0.5 * hp(rng.standard_normal(int(0.08 * SR)), 2000) * np.exp(-t_(0.08) / 0.02), ka]), 0.8, 0.3))
t = t_(0.7)
save("heart", sum(np.sin(2 * np.pi * f * t) * np.exp(-t / 0.3) for f in (1046, 1318, 1568)) * np.minimum(1, t / 0.01))
print("sfx:", sorted(os.listdir(OUT)))
