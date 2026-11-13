# Klony: the demo clip

The demo of this effect is the clip the buyer sees on the catalog page (`picker/previews/effects/clone.mp4`): a
Polish talking-head reel recorded for Studio Contentu NKB and edited in the Studio's style "Wyrazisty" (Inter Tight
800 white captions, key word in DM Serif Display yellow #FFF04A). Use it as a worked example of the settings, never
as the buyer's own result.

Footage: wide shot, camera still, 1080x1920, 30 fps. Slot: 7.4 s (222 frames).
Spoken line in the slot: "Jedna ja nagrywa, druga montuje, trzecia publikuje. A tak naprawdę robi to Claude."

The CLIP block it was built with:
```
# Run prep.py first. It prints the speaker's head anchor, the widest pose and the word hits, and saves grid frames in
# work/prep/ to read pixel positions from. The values below are the demo's (example/clip.md): replace every one.

CLONES = [
    # One line per clone, in the order they appear.
    #   id      letter used in file and element names
    #   word_f  frame the VOWEL of the trigger word lands on ("hit" in work/onsets.txt). The pop starts 4 frames earlier.
    #   x       x of the clone's head centre, px. A spot where the wall above the furniture is free (no red tint in
    #           the grid frames). bake.py prints each clone's visible x range: keep it inside 6..1074.
    #   top     y of the clone's head top, px. Set it so the furniture edge (or the real speaker) crosses the clone
    #           between shoulders and hips: furniture edge y at that x, minus 1.5 to 2.5 clone head heights
    #           (clone head height = scale x prep.py "head ... x H"). Sitting upright: the speaker's own head top + 60 to 120.
    #   scale   size vs the real speaker, 0.5 to 0.7 = (camera to the speaker) / (camera to the spot behind the furniture).
    #   lag     frames the clone runs behind the speaker (6 = 0.2 s). Give each clone a different lag.
    dict(id='L', word_f=53, x=172, top=890, scale=.5, lag=6),
    dict(id='R', word_f=85, x=915, top=810, scale=.5, lag=9),
]

# Payoff frame: every lag snaps to 0, the clones flash-pop together, the stage punches in. The vowel of the payoff
# word (work/onsets.txt). None = no payoff, the clones just stay in canon.
SYNC_F = 166

# Frame the clones drop back behind the furniture. None = they stay to the last frame (fine for a stand-alone clip).
# In a reel slot set it ~14 frames before the end so the slot hands back to the plain a-roll.
EXIT_F = None

# Top edge of the furniture the clones stand behind, as rough points (x, y) left to right across the WHOLE frame
# width, read from work/prep/grid_000.jpg (within ~10 px is enough: bake.py snaps every column to the real edge).
# Where the speaker covers the edge, continue the line straight through the speaker.
OCCLUDER_LINE = [(0, 1212), (300, 1212), (760, 1120), (1000, 1112), (1080, 1100)]

# Side the key light comes from, 'left' or 'right' (the brighter side of the speaker's face). Shadows fall the other way.
LIGHT_FROM = 'right'

# Caption groups: (top y px, [(word, onset frame, 'y' = accent colour or '')], frame the group clears or None).
# Chest band, in front of the speaker, never over the speaker's face. Dropped with CAPTIONS=0.
CAP_X = 540                  # x the captions are centred on (the speaker's chest centre)
CAPS = [
    (1078, [('Jedna', 1, ''), ('ja', 23, ''), ('nagrywa,', 28, 'y')], 52),
    (1078, [('druga', 53, ''), ('montuje,', 63, 'y')], 81),
    (1078, [('trzecia', 82, ''), ('publikuje.', 91, 'y')], 135),
    (1052, [('A', 107, ''), ('tak', 136, ''), ('naprawdę', 142, ''), ('robi', 152, ''), ('to', 160, '')], None),
]
# Big accent word on the payoff: (word, frame, top y px, frame it clears or None). None instead of the tuple = no word.
PUNCH = ('Claude.', 164, 1118, None)

ACCENT = '#FFF04A'           # butter yellow (accent words, flash tint)
VIGNETTE = 0.0               # 0 for a reel slot (the slot must match the a-roll around it); 0.22 for a stand-alone clip
```
Everything not in the block was left at the effect's default unless the block says otherwise.
