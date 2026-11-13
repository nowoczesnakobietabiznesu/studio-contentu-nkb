#!/usr/bin/env python3
"""One consistent voice clean-up for the whole a-roll -> <project>/assets/voice_clean.wav (48 kHz stereo).

Usage:  PY clean_voice.py <project_dir> [--model cb]      (run after assemble.py; build_reel.py picks it up by itself)

Why: phone clips arrive with the phone's own, inconsistent noise suppression (some pauses gated to digital silence,
others keep ~-40 dB room rumble), plus 1-4 % clipped samples (recorded too hot). Treating the whole cut the same way
makes every section sound equally clean. Ported from the NKB video-edit skill (tested on Polish phone reels, 2026-10).

Chain (ffmpeg): adeclip -> highpass 80 Hz -> arnndn (RNNoise, neural speech denoise) -> afftdn (residual hiss) ->
gentle compressor -> gate (the same quiet floor in every pause) -> two-pass loudnorm -14 LUFS / -1.5 dBTP ->
latency removed (the denoisers delay the voice ~35 ms; measured against the a-roll and shifted back, same length).
Models: SK/models/std.rnnn (general, default) or cb.rnnn (--model cb: for a voice the default thins out).

Lines to watch for:
    STATUS voice CLEAN <file> (latency removed: x ms, residual y ms)
    NOTE ...      a stage this ffmpeg lacks was left out (the rest still ran); pass it on only if the voice sounds off
"""
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skillenv  # noqa: E402

FF = skillenv.tool('ffmpeg')
MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')


def ff_filter_path(p):
    """a path inside an ffmpeg filter argument: forward slashes, the drive colon escaped (C\\:/...)"""
    return os.path.abspath(p).replace('\\', '/').replace(':', '\\:')


def run(args):
    return subprocess.run([FF, '-v', 'error', '-y'] + args, **skillenv.TEXT)


def pcm(path):
    import numpy as np
    raw = subprocess.run([FF, '-v', 'error', '-i', path, '-vn', '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.float32)


def main():
    skillenv.utf8_stdio()
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    proj = skillenv.path_arg(args[0])
    name = args[args.index('--model') + 1] if '--model' in args else 'std'
    model = os.path.join(MODELS, f'{name}.rnnn')
    src = os.path.join(proj, 'assets', 'aroll.mp4')
    if not os.path.isfile(src):
        sys.exit('assets/aroll.mp4 is missing: run assemble.py first.')
    work = os.path.join(proj, 'work')
    os.makedirs(work, exist_ok=True)
    mid = os.path.join(work, 'voice_stage1.wav')
    norm_wav = os.path.join(work, 'voice_stage2.wav')
    out = os.path.join(proj, 'assets', 'voice_clean.wav')

    # pass 1: repair + denoise (mono speech chain at 48 kHz)
    def chain(rnn):
        return ','.join(x for x in [
            'aresample=48000', 'pan=mono|c0=0.5*c0+0.5*c1',
            'volume=0.7',                                   # headroom before declipping (decoded AAC overshoots)
            'adeclip=window=55:overlap=75:arorder=8:threshold=10',
            'highpass=f=80:poles=2',
            f"arnndn=m='{ff_filter_path(model)}':mix=1" if rnn else '',
            'afftdn=nr=12:nf=-55:tn=1',
            'acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2',
            'agate=threshold=0.018:ratio=4:range=0.08:attack=4:release=180:knee=4',
        ] if x)
    r = run(['-i', src, '-vn', '-af', chain(os.path.isfile(model)), '-c:a', 'pcm_s24le', mid])
    if r.returncode != 0:
        print('NOTE the neural denoise (RNNoise) is not in this ffmpeg; cleaned without it')
        r = run(['-i', src, '-vn', '-af', chain(False), '-c:a', 'pcm_s24le', mid])
        if r.returncode != 0:
            sys.exit('voice cleaning failed: ' + (r.stderr or '')[-300:])

    # pass 2: two-pass loudness normalisation to -14 LUFS
    err = subprocess.run([FF, '-hide_banner', '-i', mid, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json',
                          '-f', 'null', '-'], **skillenv.TEXT).stderr
    m = json.loads(err[err.rindex('{'):err.rindex('}') + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
          f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(['-i', mid, '-af', ln + ',aresample=48000', '-c:a', 'pcm_s16le', norm_wav]).check_returncode()

    # pass 3: undo the filter chain's latency by cross-correlation against the a-roll, same total length
    import numpy as np
    ref, got = pcm(src), pcm(norm_wav)
    n = min(len(ref), len(got), 48000 * 30)
    xc = np.fft.irfft(np.fft.rfft(got[:n], 2 * n) * np.conj(np.fft.rfft(ref[:n], 2 * n)))
    lags = np.r_[np.arange(0, 4800), np.arange(-4800, 0)]
    lag = int(lags[np.argmax(np.r_[xc[:4800], xc[-4800:]])])        # samples; > 0 = the cleaned voice is late
    dur = len(ref) / 48000
    shift = f'atrim=start_sample={lag},asetpts=PTS-STARTPTS,apad' if lag > 0 else f'adelay={-lag}S,asetpts=PTS-STARTPTS'
    run(['-i', norm_wav, '-af', f'{shift},atrim=end={dur:.6f},pan=stereo|c0=c0|c1=c0', '-c:a', 'pcm_s16le', out]
        ).check_returncode()
    chk = pcm(out)
    m2 = min(len(ref), len(chk), 48000 * 30)
    post = 0
    if m2 > 48000 + 2000:
        post = int(np.argmax([np.dot(ref[48000:m2 - 1000], chk[48000 + L:m2 - 1000 + L])
                              for L in range(-240, 241, 12)])) * 12 - 240
    print(f'STATUS voice CLEAN {out} (latency removed: {lag / 48:.1f} ms, residual {post / 48:.1f} ms)')


if __name__ == '__main__':
    main()
