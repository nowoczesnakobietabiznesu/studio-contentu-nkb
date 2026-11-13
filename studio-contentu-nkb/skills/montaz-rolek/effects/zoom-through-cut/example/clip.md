# Przejście przez Ciebie: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/zoom-through-cut.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 1.0 s (30 frames), across a cut at 0.50 s.
Spoken line in the slot: "zyskujesz."

The CLIP block it was built with:
```
CUT = None            # first frame of shot B. None = clip.json "cut_frames"[0] (two_shot.py writes it)
HALF = 9              # transition frames on EACH side of the cut (9 = 18 in total). Shorter shots: lower it
POINT_A = None        # (x, y) px the camera dives into, on the LAST frame of shot A. None = measured by prep.py
                      #   (darkest flat patch on the speaker's torso or lap, clear of the speaker's hands). Check work/measure.jpg
POINT_B = None        # (x, y) px shot B opens out from, on the FIRST frame of shot B. None = measured by prep.py
DEPTH = 80.0          # total zoom travelled. A reaches ~sqrt(DEPTH)x on the cut. 40 = gentler, 150 = harder
SHARP = 2.4           # ease steepness: higher = longer creep at both ends, faster through the cut
ROLL = 5.0            # degrees of camera roll through the move (0 = none, negative = the other way)
CREEP_A = 1.03        # slow push-in on shot A before the dive (scale reached when the dive starts). 1 = off
CREEP_B = 1.04        # slow push-in on shot B after landing (scale reached on the last frame). 1 = off
GRADE_A = None        # optional light look baked into shot A: None, 'girl' (warm, soft) or 'dude' (dark, cool)
GRADE_B = None        # same for shot B. None when the main reel grades the footage itself
# Captions: one block per shot, or None. Times are seconds in THIS slot (words.json; confirm onsets on the audio).
#   style  'girl' (small Inter + yellow serif italic), 'dude' (tracked caps + DM Serif), 'plain' (Inter Tight)
#   top    y of the block top. None = measured by prep.py (just under the speaker's chin); the block is dropped if no room
#   lead / punch / tail   [(time, 'word'), ...]: small line above, the big word(s), small line below
CAP_A = None
CAP_B = {'style': 'plain', 'top': None,
         'lead': [],
         'lead_rides': True,      # True = the whole lead line arrives with the picture, spreading out of the point
         'punch': [(0.55, 'zyskujesz.')],
         'tail': []}
WHOOSH_VOL = 0.30     # template volume of the one whoosh (x0.75 is applied below). Its peak lands on the cut
```
Everything not in the block was left at the effect's default unless the block says otherwise.
