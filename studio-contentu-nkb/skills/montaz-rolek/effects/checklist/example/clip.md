# Lista kroków: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/checklist.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 11.7 s (351 frames).
Spoken line in the slot: "Kim jesteś i jak mówisz? Kim jest Twoja klientka i jakimi słowami opisuje swoje problemy? Twoją ofertę i ceny? Przykłady materiałów, z których jesteś dumna?"

The CLIP block it was built with:
```
# Frames are 30 fps frames of assets/aroll.mp4 (frame 0 = first frame of the slot). Get them from `python3 onsets.py`.
TITLE =  'Musisz mu dać'       # eyebrow line, shown in caps. Use words the speaker says in the clip. Keep it under ~22 characters.
ROWS = [
    ('Kim *jesteś*', 4, 28),
    ('Twoja *klientka*', 93, 117),
    ('*Oferta* i ceny', 215, 251),
    ('*Przykłady* materiałów', 271, 291),
]
F_IN = 2            # frame the card starts building. First frame of speech, or ~20 frames before the first f_say.
F_DONE =  329        # frame the card completes (pill, sheen, glow). A stressed word 8+ frames after the last tick, or None = last tick + 10.
F_OUT = None        # frame the card leaves (whips off in ~7 frames), or None = it stays to the end of the slot.
CARD_BOX = 'auto'   # 'auto' = largest room the speaker leaves free while the card is up (work/prep.json), or (x, y, w, h) px the card must fit inside.
LAYER = 'auto'      # 'behind' = between the room and the speaker's cutout (the speaker overlaps it), 'front' = over the speaker, 'auto' = behind unless front is clearly larger.
OVERLAP = 40        # px the card may tuck behind the top of the speaker's head when it sits above the speaker ('behind' only). 0 = keep clear.
GLASS = 'auto'      # 'auto' = glass when prep.py says the camera is steady, else opaque. Or force 'glass' / 'opaque'.
ACCENT =  '#FFF04A'  # tick, bar and accent-word colour (the house butter yellow). Never orange.
GRADE = ''          # CSS filter on the footage. '' = leave it (the main reel grades the slot). Standalone clip: 'contrast(1.05) saturate(.95) brightness(.99)'
VIGNETTE = 0        # 0 to .4 edge darkening. 0 inside a reel that has its own vignette. Standalone clip: .30
PUSH = 1.0          # slow push-in across the slot (1.0 = none). Only above 1.0 (demo: 1.03) on a locked-off shot that does not cut back to plain a-roll.
KEEP_OUT = []       # [(x0, y0, x1, y1), ...] px rects the main reel uses (its label pill, its caption band): the card never enters them.
```
Everything not in the block was left at the effect's default unless the block says otherwise.
