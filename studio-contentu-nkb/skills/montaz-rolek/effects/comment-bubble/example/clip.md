# Komentarz: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/comment-bubble.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: close-up shot, camera still, 1080x1920, 30 fps. Slot: 4.6 s (138 frames).
Spoken line in the slot: "Skomentuj NKB, a wyślę Ci szczegóły."

The CLIP block it was built with:
```
# -- on-screen text (no em dashes, never "free" / "course", nothing the speaker does not say or imply in the clip)
KEYWORD =  'NKB'                    # the word the speaker asks people to comment, in caps
REPLY_TEXT =   'Już wysłane'   # creator reply; keep it under ~20 characters
CHIP_TEXT =  'Szczegóły'            # label on the yellow link chip; under ~14 characters
USER_NAME =  'ty'                  # generic commenter name, never a real person
# -- times in seconds from the slot start. Run measure.py: it prints Whisper's start and the audio onset for every
#    word. Use the audio onset minus one frame (0.03) so the visual leads the voice by a frame.
T_IN =  0.05       # field slides up: about 0.4s before "comment" (on the words leading into it)
T_FOCUS =  0.13    # onset of "comment": field focuses, caret appears
T_TYPE =  1.07     # onset of the keyword minus 0.03: first letter
KEY_GAP =  0.11    # seconds per letter. (keyword end - T_TYPE - 0.1) / (letters - 1), between 0.05 and 0.11
T_SEND =  1.5     # send tap: the end of the keyword (first breath after it)
T_DOTS =  1.79     # onset of the next phrase ("I'll"): creator typing dots. At least 0.15s before T_REPLY
T_REPLY =  2.11    # onset of "send" (the s, not the vowel): reply bubble lands
T_LINK =  2.24     # onset of the thing the speaker sends ("link", "guide"...) minus 0.03: chip resolves
T_OUT = None      # None = thread holds to the last frame (slot ends on a cut). A time = thread leaves and the plate
                  # settles back so the slot's last frame matches the a-roll again (use when the reel keeps the shot)
# -- size and place. Everything is placed from the measured chin (work/measure.json), nothing is a fixed y.
SCALE =  1.2       # thread size, 1.0 = the original demo. Shrinks by itself if the band under the chin is too small
CHIN_Y =    1390     # None = measured from the cutout (95th percentile while the thread is up). Or a y in frame px:
                  # the lowest the speaker's chin gets in the slot, read off work/measure_check.jpg
CHIN_GAP = 20     # clear px between chin and thread, never less
DROP = 'auto'     # 'auto' = as low as the safe zone allows (bottom edge 1456): on wide shots the speaker's torso and hands stay
                  # visible, on close-ups this equals hugging the chin. A number = px from chin to the thread top
X_CENTER = None   # None = centred under the speaker's head (measured), clamped to the safe zone. Or an x in frame px
PUSH =    1     # 'auto' = lift the plate (scale from the bottom edge) only as much as the thread needs, up to
PUSH_MAX =  1.2   # PUSH_MAX; 1 = never touch the plate (the thread shrinks instead). Close-ups need the lift.
# -- look
AVATAR_FRAME = None   # frame for the creator avatar crop: pick one from work/avatar_check.jpg (eyes open). None = last frame
AVATAR_BOX = None     # (x, y, size) square crop in frame px if the automatic head crop is off. None = measured
GRADE =  'contrast(1.06) saturate(1.04)'        # css filter on the plate. Set it to the reel's own grade so the slot matches its neighbours
SEAT = 1.0            # strength of the soft dark gradient that seats the thread on the footage (0 = off)
# -- style. The buyer's style wins: in a reel, set these from the reel's caption style (SKILL.md "The buyer's style
#    wins", effects/INDEX.md "Restyling an effect's own words"). Each font is (css family, weight, file in
#    assets/fonts): the slot holds every font the caption styles use, assets/fonts/fonts.css lists them.
#    A wide heavy look, for example: WORD_FONT = TEXT_FONT = ('Archivo', 900, 'Archivo-900-normal.woff2'), UPPER = True.
#    A wider typeface makes the thread wider: build.py shrinks it to the safe zone, lower SCALE if it gets small.
WORD_FONT =  ('Inter Tight', 800, 'InterTight-800-normal.woff2')   # the keyword (typed and posted) and the chip label
TEXT_FONT =  ('Inter Tight', 800, 'InterTight-800-normal.woff2')              # the reply line and the commenter name
UPPER = False         # True = reply line, chip label and name in capitals (the keyword is in capitals already)
ACCENT_COL, LIGHT_COL, DARK_COL =  '#FFF04A', '#FFFFFF', '#14161C'   # accent (ring, caret, chip), light (bubble, words), dark (words on light)
```
Everything not in the block was left at the effect's default unless the block says otherwise.
