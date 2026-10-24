# Claret logo, final

- **Icon:** the rim. A deep claret core with a paler rim, as when you look down into a glass. `claret-icon-light.svg`, `-dark.svg`, `-tinted.svg` (1024 × 1024; iOS applies the corner mask). For Icon Composer, the icon is also split into `claret-icon-layer-background.svg` and `claret-icon-layer-rim.svg`.
- **Mark:** `claret-mark.svg`, the rim on its own.
- **Wordmark:** "Claret" in Newsreader (SIL Open Font License) at weight 500, display optical size, outlined to paths so it renders the same everywhere. `claret-wordmark-poured.svg` is filled with a subtle claret gradient, deeper at the bottom; `-poured-dark.svg` for dark backgrounds; `-ink.svg` in a single ink colour.
- **Lockups:** `claret-lockup.svg`, `claret-lockup-dark.svg`.
- **Colour:** always claret. Light #4E0C1A → #8A2236 for the word; dark #A3304A → #DA6A80.
- **Launch:** the empty wordmark outline fills from the bottom with claret, its surface settling as it rises, then the rim lands beside it. About 1.2 s, once a day, tap to skip, a fade under Reduce Motion.

`wordmark.json` holds the outlined path and its bounds; `build-wordmark.py` regenerates it (needs `fonttools`, `brotli` and `uharfbuzz`). Apple's New York is used in the interface only, not in the logo, because its licence covers app interfaces.
