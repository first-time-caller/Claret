# Claret: roadmap

## v1 (this build)
- Tonight with moments, season, weather tap, mood, food, company; local style engine; sideways alternatives; serving guide.
- Find bottles (Claude), with hard limits enforced in code and a suggestion event recording what you took.
- Scan: label, compare, wine list. Nodes, scan events and sightings written per the data model.
- Log with tasting colours, structure, tags, half-step ratings.
- You: palate summary, hard limits, discovery dial, moment times, export.
- Private sync through the artifact `db`, local fallback.

## Next
- Cellar: bottles you own, drinking windows, "open this before it fades".
- Palate passport: coverage map by grape and place, "never tried, near what you like".
- Group mode: several people's limits merged into one pick.
- Price view per wine from sightings; restaurant markup against shop prices you've seen.
- Store label photos with `assets` and link them from scan events.
- Derived docs (palate, passport, prices) with a logic version, rebuilt from events.
- Bigger atlas: appellations for the main regions, ~150 grapes, UK merchants.
- Test set of real label and wine-list photos with expected results, run whenever a prompt changes.
- Playwright tests: Tonight engine, limits checks, log round trip, export.

## Later
- The second app: UK retailer prices and stock, feeding Tonight with "available near you".
- Native SwiftUI app; the storage adapter is the only module that changes.
