# Claret: project notes for Claude Code

Claret is a UK, iPhone-first wine companion ("what are we drinking?"). It is a single-page app in one file, `index.html`, first delivered as a private Claude artifact. Specs are in `docs/`.

## Layout
- `index.html`: the whole app (HTML, CSS, JS). Views: Today, Explore, Cellar, Journey (`#v-log`), scan, wine/place pages, You.
- `data/`: all content (places, producers, country defaults, map frames). **Add detail here, not in code.** See `docs/data-files.md`.
- `img/`: photos (`credits.json` holds each photo's credit), `logos/` (producer logos + `index.json`), `maps.json` (generated).
- `images/logos/raw/`: raw logo files; `tools/build_logos.py` turns them into masks.
- `tools/`: `validate_data.py`, `build_maps.py`, `build_logos.py`.
- `docs/`: `data-model.md`, `journey-and-cellar.md`, `catalogue-learnings.md`, `roadmap.md`, `data-files.md`, `france-model.md` (draft).
- `design/`: mocks and logo sources.

## Run and check
- Serve from the repo root: `python3 -m http.server 8765`. The app expects `window.claude` (artifact runtime) but falls back to localStorage, so it runs in a plain browser. AI features (scan, find bottles, fill-in) need the Claude app, so they say so offline.
- Syntax check: extract the `<script>` block and run `node --check`.
- Browser checks: Playwright with a 390x844 viewport. Wrap `index.html` in a minimal page (see `.gitignore`: `_preview.html`), stub `Date` for time-of-day behaviour.
- Before publishing content changes: `python3 tools/validate_data.py`; after map spec changes: `python3 tools/build_maps.py`.

## Publishing
The artifact is at https://claude.ai/artifact/6izvLmehzezMkiPD9rkjYL (private). Publish `index.html` with the Artifact tool, passing the same URL, `root` set to a staging folder, and a `files` map for `data/**` and `img/**` (only changed files need listing; others are kept). The page fetches `data/*.json`, `img/credits.json`, `img/producers.json`, `img/maps.json` and `img/logos/index.json` relative to itself.

## Design rules (decided with the owner)
- Neat, squarer tiles (4px radii), "less iOS". Classical serif headings. Claret brand colour is fixed (never theme-switched).
- Keep names whole (no mid-word wraps); use `words()`/`setTitle`/`fitLetters`.
- Wine naming: `{vintage} {wine} by {producer}, {region}`; drop "by" when the name already holds the producer.
- Cards drop the country label when the whole view is in that country; producer cards show only name or logo.
- Hard limits (colour, price, origin) are enforced in code (`breaks()`), never only suggested.
- Estates named like their appellation are producers, separate from the place (Château Margaux vs Margaux).
- Open bottles count as tried (pending tastings); Journey, Cellar and Explore marks (Tried/Known/Loved) read the same maps (`maps()`).

## Data model in brief
Places have `level` (Country, Island/State, Region, Appellation) and `parent`; wines roll up to every ancestor. Explore shows top-level places; search shows matching places with their children as grouped tiles; wines only on a tap unless nothing else matches. See `docs/data-model.md`.

## Open items
- France: bespoke model per `docs/france-model.md` (needs owner's answers and region tables).
- Logos still missing: Vega Sicilia (and the Yarra Valley estates). Photos still missing for many regions (country stand-ins are used).
- Photo credits for owner-supplied images read "attribution to be added" in `img/credits.json`.
- Update `docs/journey-and-cellar.md` and README for Journey, Cellar decomposition and open-bottle behaviour.
- Producer entries for Pétrus, Lafite and similar; descriptions for the Australian and Hawke's Bay additions were written from general knowledge and need owner review.
