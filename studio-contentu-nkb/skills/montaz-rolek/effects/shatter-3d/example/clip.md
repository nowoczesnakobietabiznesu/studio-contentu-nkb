# Pękające szkło: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/shatter-3d.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 3.8 s (114 frames).
Spoken line in the slot: "zdanie. To AI jest jakieś głupie."

The CLIP block it was built with:
```
T_BREAK =  'AI'      # the picture fractures on this word: a word from words.json ('absolutely', or 'so#2' for its 2nd
                      # time), seconds (3.29), or 'auto' (a word 0.5 to 1.6 s before T_HIT). Re-measured on the audio
T_HIT =  'głupie.'        # the hard jolt lands on this word (the punch word): word, seconds, or 'auto' (the last long word
                      # that leaves 1.5 s of slot after it). Read the printout and set both words for a real edit
ENDING = 'glass'      # 'glass' = v2, cracks and breaks like glass (the default look); 'heal' = v1, the tiles snap back
HOLD = 11             # frames the fractured picture holds after the hit before it cracks (glass) or heals; 6 to 16
SHOT = 'auto'         # 'auto' (measured from the cutout), or 'wide' / 'medium' / 'tight' / 'none' (no speaker: plain grid)
FACE_BOX = None       # override the measured face (x0, y0, x1, y1) in 1080x1920 px, only if the printout is wrong
CLOSEUPS = 'auto'     # how many close-ups fly out: 'auto' (eyes and hands where there is room), 0, 1 (eyes) or 2
IMPACT = 'auto'       # where the glass is hit (x, y) in 1080x1920 px; 'auto' = the hands, else under the chin, never
                      # on the face
ACCENT =  (255, 240, 74)   # edge colour of the close-up shards (r, g, b): butter yellow; use the buyer's accent colour
GROUND = (20, 22, 28)      # the dark ground seen in the gaps between tiles (r, g, b); keep it near black
SEED = 11             # tile split, depths and tilts. Change it for another arrangement
GLASS_SEED = 4        # crack pattern and how each glass shard flies
```
Everything not in the block was left at the effect's default unless the block says otherwise.
