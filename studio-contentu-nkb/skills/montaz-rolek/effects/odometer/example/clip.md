# Licznik: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/odometer.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 5.9 s (177 frames).
Spoken line in the slot: "Rolka zmontowana przez Claude przyniosła mi 141 nowych obserwujących."

The CLIP block it was built with:
```
COUNTERS = [
    dict(
        text='+141',
        say='141',
        lock=None,
        label=[('NOWYCH', 'nowych'), ('OBSERWUJĄCYCH', 'obserwujących.')],
        label2=None,
        sit='auto',
        size='auto',
        then='dock',
    ),
]
ROLL = 0.44        # seconds the drums spin before the lock (0.35 to 0.5; shorter for a number the speaker says fast)
OUT = None         # seconds: every panel leaves by this time. None = they hold to the last frame (end the slot on a cut, or set this ~0.25 s before the slot ends)
DOCK_CORNER = 'auto'   # where a docked chip goes: 'auto' (top corner away from the next panel), 'top-left', 'top-right', or (x, y)
GRADE =  'none'    # light grade on the footage (plate + cutout). 'none' when the main reel grades it
```
Everything not in the block was left at the effect's default unless the block says otherwise.
