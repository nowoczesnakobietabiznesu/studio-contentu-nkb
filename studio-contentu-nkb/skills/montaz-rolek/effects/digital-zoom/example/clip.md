# Najazd: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/digital-zoom.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera moving, 1080x1920, 30 fps. Slot: 2.0 s (60 frames).
Spoken line in the slot: "Serio?"

The CLIP block it was built with:
```
# The values below are the NKB demo clip ("Serio?", 60 frames, close-up). Replace all of them for a new clip.

# The zooms, in order. zoom(t_start, t_land, scale, kind). Frames come from `onsets.py` (audio envelope per frame):
#   creep: t_start = first word of the line, t_land = 2 frames AFTER the vowel of the word it lands on
#   snap : t_land = the vowel of the stressed syllable, t_start = 3 frames before it
#   pull : t_start = onset of the word it leaves on, t_land = about 9 frames later
# Scale: build.py prints the lossless limit for this source and caps anything past MAX_UPSCALE times that.
ZOOMS = [
    zoom(F(2), F(20), 1.06, 'creep'),
    zoom(F(21), F(24), 1.18, 'snap'),
    zoom(F(44), F(53), 1.0, 'pull'),
]
# Where the speaker's eyes sit on screen while the shot is tight (x, y). 540 = centred, 640 = upper third line. On a close-up
# selfie go a little higher (about 620) so the chin leaves room for captions. build.py prints from which scale the frame
# can hold the speaker there ("aim: ..."): start a snap above that scale, or the snap also slides the picture.
EYE = (540, 640)
# How tightly the camera follows the speaker's head: gaussian sigma in frames. 5 = an operator following the speaker. Raise to 8-10 if
# the background swims on a still tripod shot, lower to 3 on handheld footage where the face must stay pinned.
FOLLOW = 5
# Optional manual aim, only if work/track_check.jpg shows the cross off the speaker's eyes: (frame, x, y) of the point between
# the speaker's eyes in that frame of assets/aroll.mp4. None = automatic from the cutout.
AIM = None
# How far past the lossless zoom of the source a scale may go (1.5 = 150% upscale, still clean with the unsharp pass).
MAX_UPSCALE = 1.5
# Captions (dropped with CAPTIONS=0). One tuple per group: (last frame on screen or None, lines).
#   line = (top px, size, words), size 'sm' 84px | 'lg' 190px | 'big' 236px | a number of px, word = (frame it is spoken, text, 'y' yellow or '').
#   Keep every top below the chin: build.py prints "clearance" per group and warns when a group is too close, too low or too wide.
#   A group that ends where a snap starts is pushed through, one that ends where a pull starts is left behind.
CAPS = [
    (None, [(1082, 'big', [(2, 'Serio?', 'y')])]),
]
# Whoosh volume on each snap, relative to the template (0.75 gain is applied on top). 0 = none. Keep it under the speaker's voice.
WHOOSH = 0.26
# Grade on the picture (dropped with GRADE=0). A soft contrast base look, a touch lighter so skin stays natural.
GRADE = 'contrast(1.06) saturate(.93) brightness(.98)'
```
Everything not in the block was left at the effect's default unless the block says otherwise.
