# Ściana słów: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/type-wall.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: medium shot, camera still, 1080x1920, 30 fps. Slot: 2.5 s (75 frames).
Spoken line in the slot: "Claude, przygotowałyśmy do tego gotowego skilla."

The CLIP block it was built with:
```
# PHRASES: what the wall says, in the order the speaker says it. 1 to 3 words per phrase, UPPER CASE.
#   (frame, 'WORD') = the frame that word starts on. Get it from `python3 onsets.py` (column "swap").
#   The first word of the first phrase rides in with the wall at IN_FRAME, whatever its own frame says.
#   A 2 or 3 word phrase builds down the wall: every row says word 1, then every 2nd (or 3rd) row turns to word 2...
#   'hit': True marks the word that matters: all rows snap to it, the wall punches, the row over the speaker's head turns yellow.
#   Skip the small words. Split a word that is wider than the frame (EVERY / BODY'S); build.py tells you which.
PHRASES = [
    {'words': [(2, 'CLAUDE')]},
    {'words': [(60, 'SKILLA')], 'hit': True},
]
IN_FRAME = 0        # frame the wall arrives (hard cut from the room, rows whip in). 0 = it is up from the first frame. Normally the frame of the first wall word
OUT_FRAME = None    # frame the wall is gone and the room is back. None = it stays up to the end of the slot
KEEP = []           # real picture kept in front of the wall (the sofa or desk the speaker sits at). Still camera only. A list of shapes that do not overlap, each a list of (x, y) px read off work/measure.jpg. [] = the wall fills the whole frame
FS =  180            # letter size in px. 205 suits a shot with clear wall above the speaker's head; go down (150 to 180) when prep.py says there is no room above the speaker or build.py says a word is wider than the frame
ACCENT_Y = None     # y px where the letters of the yellow row end. None = measured: just above the highest point the speaker's head reaches
HEAD_GAP = 14       # px between the yellow row and the top of the speaker's head (only used when ACCENT_Y is None)
XC = {}             # {row number: x px} to move the spot where a row's word is centred when it swaps. {} = measured: the widest gap the speaker leaves in that row. Row numbers are printed by build.py
GROUND = ('#22261A', '#14160F', '#0B0C09')    # wall colours: glow behind the speaker's head, middle, corners. Keep it dark and quiet so the letters carry
INK = '#EEEADF'     # letter colour (outlined rows use the same colour at 60%)
ACCENT =  '#FFF04A'  # colour of the row over the speaker's head from the hit word on (from the start when no phrase has 'hit')
VOL_IN, VOL_HIT, VOL_SWAP = .28, .08, .16     # sound levels: whoosh as the wall arrives, low hit on the hit word, soft whoosh on each new phrase. 0 = that sound off
```
Everything not in the block was left at the effect's default unless the block says otherwise.
