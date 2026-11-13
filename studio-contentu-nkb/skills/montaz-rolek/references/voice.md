# Voice cleaning

Phone recordings sound different from clip to clip: the phone's own noise suppression gates some pauses to silence
and leaves room hum in others, and loud speakers clip. `clean_voice.py` treats the whole cut the same way, so the
reel sounds like one recording.

```
PY "SK/scripts/clean_voice.py" "<project>"              after assemble.py, before the build
PY "SK/scripts/clean_voice.py" "<project>" --model cb   the voice sounds thin or robotic: the other RNNoise model
```

- It writes `assets/voice_clean.wav`. `build_reel.py` plays it instead of the a-roll's own sound, but only while it
  belongs to the current cut (newer than `aroll.mp4`, same length). After a new `assemble.py` (a notes round that
  changes takes, a hook trial) run it again; until then the build uses the a-roll sound and prints a NOTE.
- Hook trials (`variations.py make`) clean their own new cut by themselves when the reel was cleaned.
- Loudness lands at about -14 LUFS, peaks under -1.5 dB: the level Instagram plays at, so the reel is neither quieter
  nor louder than the ones around it. `check_cuts.py` prints the final level as its last line.
- The latency of the denoisers (about 35 ms) is measured and removed, so lips and voice stay together. The STATUS line
  says how much was removed and what is left (a residual under 5 ms is fine).
- A `NOTE` that RNNoise is missing means this computer's ffmpeg has no neural denoise. The rest of the chain still ran;
  the voice is cleaner than the original, only a little less so.
- She says "bez czyszczenia", "zostaw oryginalny dźwięk": do not run it. If it already ran on this reel, rename the
  project's `assets/voice_clean.wav` to `voice_clean.off.wav` (a project file, never one of her originals) and
  rebuild: the build goes back to the a-roll sound.
- Sound effects are mixed on top of the cleaned voice at their usual levels, never louder than the voice.
