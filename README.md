# Claret

What are we drinking? A UK wine companion for iPhone, built first as a Claude artifact.

Claret opens on an answer. It reads the moment (Today, This afternoon, Tonight or Nightcap), the season, a one-tap weather choice, what you're eating and your mood, and suggests a style with the reason, what to look for and how to serve it. From there it can find specific bottles you can buy in the UK, read a label in the shop, compare two or three labels, or read a restaurant wine list and pick the best fit, the best value and something new. Every suggestion is checked in code against your hard limits (colour, price a bottle and a glass, ABV, countries, grapes) before you see it.

## What's in v1

- **Tonight**: moment-aware style suggestion from a local engine that works with no network, three "sideways" alternatives, serving temperature, glass and prep, and "Find bottles for this" (Claude, limits enforced).
- **Scan**: Label, Compare and Wine list modes. Each read creates wine nodes, a scan event and a price sighting per price, so your own UK price history builds as you go.
- **Log**: producer, wine, vintage, origin, grapes, a rating in half steps, the tasting colour in the glass, structure, tags, notes, food, company, where and what you paid.
- **You**: bottles, grapes and countries so far, best-rated grapes, never-tried countries, hard limits, how adventurous suggestions should be, the Tonight and Nightcap switch times, and export.

## Design

iPhone-first, in Apple's own type: New York (`ui-serif`) for wine names and titles, SF for interface text, SF Mono for prices, vintages and temperatures. Large titles, grouped lists, a frosted tab bar and bottom sheets. The palette is the sommelier's appearance scale, from water-white to brick; every wine is drawn as a glass seen from above in its own colour, and claret is the accent.

## Data

See [`docs/data-model.md`](docs/data-model.md). In short: small nodes with readable ids (`vintage:jamet/cote-rotie/2019`), facts as sourced claims rather than columns, append-only events grouped by month, and views rebuilt from events. Reference knowledge (countries, regions, grapes, styles, tasting colours) ships inside the page.

## Running it

`index.html` is written as a Claude artifact page (no `<html>` or `<head>` of its own; the artifact host wraps it).

- **As a Claude artifact** (the main way): label scanning, wine lists and bottle suggestions use Claude, and your data syncs privately to your Claude account.
- **Anywhere else**: Tonight, the log and limits work fully, and data stays in that browser.

## Specs

- [`docs/data-model.md`](docs/data-model.md): the graph, claims, events and derived views.
- [`docs/journey-and-cellar.md`](docs/journey-and-cellar.md): where you are (home, shop, out), the cellar, and the Journey trail and passport.
- [`docs/roadmap.md`](docs/roadmap.md): what ships next.
