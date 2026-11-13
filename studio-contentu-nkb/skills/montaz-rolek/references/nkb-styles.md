# NKB ready styles (the catalog)

The Studio ships the NKB catalog as ready styles in `SK/nkb-styles/<key>/` (`style.json` + `style.md`), in the same
format as the buyer's saved styles (`references/my-styles.md`). The catalog page (the Studio Picker) shows them on
the NKB sample clip. A buyer who picks one gets a COPY in their own styles, so their notes and brand colour change
their copy, never the shipped one.

```
PY "SK/scripts/my_styles.py" save "<name>" --from-nkb <key> [--accent "#hex"] [--with-picks]
```
`<name>`: what the buyer calls it (default: the style's own name, e.g. "Viral"). `--accent`: their brand colour
instead of the NKB gold #CD9F38 (ask once at setup: "Jaki jest kolor Twojej marki?"). `--with-picks`: the effects
they picked in the Picker go with it.

## Two ways (the catalog switch)

**Wybieram gotowy styl** (overall styles, kind "overall"): colour, captions, graphics, pace and sound together.

| Key | Name | Needs | Per reel (style.md "Graphic elements") |
|---|---|---|---|
| `salon` | Salon | | pinned title from the hook |
| `viral` | Viral | clean cutout | the punch word BEHIND the head on its emph / cta word |
| `redakcja` | Redakcja | | masthead with the buyer's brand name |
| `lekcja` | Lekcja | | step label + progress, only from steps she names |
| `tempo` | Tempo | | none: punch-ins every other cut in edl.json |
| `pokaz` | Pokaz | clean cutout | UI cards in the top band, one per named thing |
| `kulisy` | Kulisy | the buyer's b-roll clips | full-frame b-roll layers over the whole reel |
| `notatnik` | Notatnik | | sparkles and a handwritten note on key words |
| `elegancki` | Elegancki | | one light sweep at the start |
| `yapping` | Yapping | clean cutout | title behind the head, typed caps, cards, brush, notes |

**Stwórz swój styl** (caption styles, kind "captions"): only the captions; the footage stays as it is.
Spokojne: `kinowe`, `szept`, `cytat`, `szklo`, `kadr`. Wyraziste: `zlota-nic`, `pieczatka`, `obrys`, `marker`,
`etykieta`. Dynamiczne: `jedno-slowo`, `schody`, `echo`, `naglowek`, `maszynopis`. Edytorskie: `gabinet`, `duet`,
`liczby`, `notatki`, `wstega`.

## Rules every NKB style keeps
- Captions at the bottom of the Reels safe zone (`"position": 1470`), as far from the face as the safe zone allows.
  When a two-line style has no room under the chin, the engine keeps it inside the safe zone and says so in a NOTE:
  look at the snapshot, and use one line or a smaller size for that reel if it covers the chin.
- No picture lift: with these styles set `"lift": 0` in `layout.json` after `layout.py` (the captions do not need
  the collar band, and the lifted strip at the bottom looks like a border).
- Every face the skill ships has Polish and German letters (only Rubik Mono One lacks "ß"). A face fetched with
  `get_font.py` comes as one file with all its letters, and the script prints `MISSING LETTERS pl: ...` when the
  family has none (Permanent Marker, Lobster Two, Elsie Swash Caps): then pick the nearest face that has them and tell
  the buyer which face stands in.
- The accent is `var(--acc)` in every style's css and layers: changing `caption.accent` recolours all of it.
- Text on screen is only the buyer's own words or a generic placeholder. No invented step counts, issue numbers,
  logos or data.
- Styles that need the clean cutout: run `rvm_cut.py` before the build (`references/checks.md`).

## Changing the catalog
Edit `nkb-styles/_make_captions.py` or `_make_overall.py` and run it; Viral and Złota nić are edited in their own
`style.json`. Then build the test reel on the sample clip and look at the snapshots.
