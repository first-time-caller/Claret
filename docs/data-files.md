# Data files: adding detail without touching the code

Places, producers and country defaults live in `data/*.json`. `index.html` only loads and draws them. To add a region, an appellation, or fifty producers, edit JSON, run two checks, and republish.

```
data/index.json          which files to load
data/places/<cc>.json    one file per country (fr, it, nz, au, ...): an array of places
data/producers.json      estates and famous producers
data/countries.json      per-country defaults (card lettering font, fallback photo)
data/map-windows.json    the map frames (bounding boxes) used by the maps
img/logos/               producer logos (+ index.json), built by tools/build_logos.py
```

## A place

```json
{
  "id": "hawkes-bay",
  "name": "Hawke’s Bay",
  "level": "Region",
  "parent": "north-island",
  "country": "New Zealand",
  "grapes": "Merlot, Cabernet Sauvignon, Syrah, Chardonnay",
  "blurb": "A warmer, sun-drenched region… (terroir and style)",
  "lettering": { "t": "Hawke’s Bay", "f": "\"Dancing Script\",cursive", "w": 500, "size": 56, "card": 34, "tone": "#4A3A2A" },
  "places": ["place:nz/hawke-s-bay", "place:nz/hawkes-bay"],
  "keywords": "hawkes bay",
  "photo": "sancerre",
  "map": { "window": "NZ", "admin1": ["Hawke's Bay"] }
}
```

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Short unique slug. Also the photo key: a photo at `img/<id>.jpg` with an entry in `img/credits.json` shows on its card |
| `name`, `country`, `blurb` | yes | Display name; country text (the last comma part is the country); terroir and style |
| `level` | no | `Country`, `Island`, `State`, `Region` or `Appellation`. Shown as a badge and used for the page layout |
| `parent` | no | `id` of the place above it. Gives the breadcrumb, the tiles on the parent's page, and "counts toward" roll-ups |
| `grapes` | no | Key varieties, most important first. They become the Grapes strip and the tile subtitle |
| `lettering` | no | Title style: `t` text, `f` CSS font-family, `w` weight, `size` page size, `card` card size, `tone` fallback colour, `ls` letter-spacing |
| `places` | no | Place ids that mean this region. A wine recorded as `place:nz/waiheke` is filed here |
| `keywords` | no | Extra words search should match (old names, nearby towns) |
| `photo` | no | Borrow another key's photo (e.g. the Margaux appellation reuses `bordeaux`) |
| `map` | no | `window` (from `map-windows.json`), then either `admin1` (political areas to highlight) or `blob` `[lon, lat, long-half-axis, short-half-axis, angle]` (a rough ellipse); optional `ctx` outlines a surrounding area |

## A producer

```json
{ "name": "Trinity Hill", "place": "Hawke’s Bay, New Zealand", "region": "hawkes-bay",
  "blurb": "A Gimblett Gravels pioneer…", "country": "nz" }
```

`region` must be a place `id`. `country` (`nz` or `au` so far) sets the fallback photo. Famous houses with their own photo add `"photo": "<credits key>"` and optionally `"bottle"`, `"photoFrom"`, and `"lettering"` (used when there is no logo). A logo is picked up automatically if `img/logos/<slug-of-name>.png` exists.

## Workflow

1. Edit the JSON (a spreadsheet table converts straight to it).
2. `python3 tools/validate_data.py` — catches missing parents, unknown regions, bad map windows, duplicate ids.
3. If you changed any `map`: `python3 tools/build_maps.py` (downloads Natural Earth boundaries once into `tools/.cache`).
4. If you added logos: drop them in `images/logos/raw/` and run `python3 tools/build_logos.py`.
5. Publish `index.html`, `data/` and `img/`.

Code is only needed for things that are logic rather than content: how Tonight scores a wine, how pages are laid out, and (for France) how classification rules are read. See `docs/france-model.md`.
