# Journey and Cellar: spec (draft 2, 24 Oct 2026)

Decisions made on 24 Oct are in section 10; section 11 covers the expanded Explore.

Builds on `data-model.md`. This covers two things and one change of principle.

**The change of principle: the first screen depends on where you are.** At home you are not buying or discovering. You want something you already own. So at home, the first thing Claret shows is a bottle from your cellar. When you're in a shop it shows Scan; in a restaurant, the list reader. Discovery is always one swipe away, never the default at home.

**Cellar** is what you own and what is open. **Journey** is where your tasting has taken you.

---

## 1. Where you are

A new field in the context snapshot (`ctx.where`) with three values.

| Value | When | First screen leads with |
|---|---|---|
| `home` | Default, especially from 16:30 and at weekends | **From your cellar**: one pick from bottles you own, then "or something new" |
| `shop` | You start a label or compare scan, or tap "In a shop" | Scan, with the gaps in your cellar above it ("You're short of: a fresh white, a light red") |
| `out` | You start a wine-list scan, or tap "Out tonight" | The list reader, with your limits and moment applied |

**Detecting it.** The page has no location, so this is a light-touch choice, never a guess shown as fact:
- Default is `home`.
- A chip on the Tonight hero reads **At home ▾**. One tap switches to In a shop or Out.
- Starting a scan switches to `shop` or `out`, for the next three hours, then it falls back to `home`.
- The native app can do better later: a geofence on your home address (arriving home brings up the cellar) and a Focus filter.

**If you own nothing.** An empty cellar is a designed state, not a dead end: "Your cellar is empty. Scan a bottle you own, or take a photo of a delivery note", with Tonight's discovery picks below.

---

## 2. Navigation

Five destinations is the most an iPhone tab bar should carry, and Scan is already its own button, so:

**Tonight · Cellar · Explore · Journey**, plus **Scan**.

- **Tonight** at home leads with the cellar pick; elsewhere it's the discovery screen we have now.
- **Cellar** is the full list of what you own, how it's drinking, and what's open.
- **Explore** is unchanged.
- **Journey** replaces Log and You: your history, your trail and passport, palate, limits and settings. Settings sit behind a profile button at the top of Journey.

---

## 3. Cellar: data

A cellar is bottles you own. Tracking each bottle as its own record is heavy and rarely useful, since a case of six is one decision. So the unit is a **lot**.

### Lot (a node, type `lot`)
```js
{ schema: 1, id: "lot:01J…", type: "lot",
  links: { vintage: "vintage:isabel-estate/bbr-new-zealand-sauvignon-blanc/2023", venue: "venue:uk/bbr", location: "place-in-home:rack-a" },
  qty: 6, left: 4, size: 750,
  paid: 1595,                // pence per bottle; null if a gift
  boughtAt: "2026-10-12",
  gift: false,
  tier: "everyday",          // everyday | good | treat | special; derived from paid, overridable
  note: "Case deal, free delivery" }
```
**Individual bottles.** A lot is counted by default. For special bottles, a lot can be switched to **track each bottle** (offered automatically when the tier is `special` or a bottle cost £80 or more; always available from the lot). Each bottle then becomes its own node:
```js
{ id: "bottle:01J…", type: "bottle", links: { lot: "lot:01J…", vintage: "…" },
  n: 3, of: 6,                  // "bottle 3 of 6"
  note: "From the left-hand end of the case; the 2010 vertical",
  photo: "<asset id>",          // your photo of this bottle, not the label
  location: "rack-a/row-2",
  status: "cellar" | "open" | "finished" | "gifted",
  gift: null }
```
Opening, notes, photos and the drinking window all attach to the bottle, so two bottles from one case can have different stories. The lot keeps the shared facts (price, date, merchant).

**Gifts.** A lot or a bottle can be a gift in either direction.
```js
gift: { from: "person:sam", occasion: "40th birthday", at: "2025-03-14" }     // given to you
gift: { to: "person:alex", occasion: "housewarming", at: "2026-08-02" }       // you gave it away
```
A gift received has `paid: null`, shows "From Sam" in the cellar and on the wine page, and the tasting remembers it ("Opened the bottle from Sam"). People are the same `person` nodes used for "with". Giving a bottle away writes a `gifted` event that takes it out of the cellar.

Where it was kept is free text with a suggested list: Rack, Fridge, Wine fridge, Garage, Under the stairs. Moving a lot writes a `bottle` event; the lot's `location` updates.

### Open bottle (a node, type `open`)
A bottle you've opened and not finished. This is the most useful thing a home screen can know.
```js
{ id: "open:01J…", type: "open", links: { lot: "lot:01J…", vintage: "…" },
  openedAt: "2026-10-14T19:50", left: 0.5,        // fraction left, set by you in thirds or halves
  keep: "fridge" | "cellar" | "preserver",        // how it's being kept
  fadesBy: "2026-10-17" }                         // derived from style
```
**How much is left?** Claret asks, and never guesses. Tapping **Open it** only records that it's open. The question comes at the end of the evening or on next opening of the app: the home screen shows "Last night's Chinon: how much is left?" with **Finished · A quarter · Half · Three quarters**. The answer sets `left` and, if finished, offers to log it. An open bottle that has not been answered after a day shows the prompt again on the "Still open" row.

`fadesBy` comes from the style: sparkling 1–2 days, light white or rosé 3 days, red 3–5 days, Fino 5–7 days, fortified weeks. It's a suggestion, labelled as one.

### Events (kind `bottle`, in the monthly docs)
`bought`, `opened`, `finished`, `gifted`, `moved`, `adjusted` (a count correction). Each carries `lot`, `n`, `at`. `left` on a lot is derived from them. A `finished` event can carry a rating and becomes a tasting in one tap.

### Derived views
| Doc | Built from | Holds |
|---|---|---|
| `cellar` | lots + bottle events | Bottles now, by status, colour and place; spend; average price |
| `forecast` | lots + drinking windows | How many bottles reach their window each year; what falls out of it next |
| `gaps` | cellar vs moments | The styles you have none of, for the shop header |

### Adding bottles
1. **Scan a label → "Add to cellar"** with a quantity stepper.
2. **From a tasting:** "I have another" on the wine page.
3. **A photo of a delivery note or receipt:** Claude reads the lines, you tick what to add. (Later: a Gmail or merchant order feed through the artifact's connectors.)
4. **By hand.**

Nothing is estimated silently: a lot's paid price is only what you entered or the receipt shows.

---

## 4. Cellar: choosing from it

The existing Tonight engine scores **styles**. At home it also scores **your lots** and shows the best one.

```
score = styleFit            // moment, season, weather, food, mood: the engine we have
      + urgency             // see below
      + palateFit           // your ratings of this grape, place and style
      + occasionFit         // does the bottle's tier suit tonight?
      - recency             // you drank this style or this wine in the last few days
      ± explore             // the Safe bets ↔ Surprise me dial: pushes towards unfamiliar lots
```

### Urgency (the reason to open it now)
In this order of weight:
1. An **open** bottle past 50% of its `fadesBy` window.
2. A lot **past its drinking window**.
3. A lot in the **last year** of its window.
4. A lot **ready now** with no end date set.
5. A lot **not ready yet**, only shown if you ask.

### Occasion fit
A Tuesday supper shouldn't suggest the £90 Barolo. Each lot has a tier; each moment has a ceiling:

| Moment | Ceiling | Notes |
|---|---|---|
| Today, weeknight | `good` | |
| Weekend, Tonight | `treat` | |
| Celebrating (mood) | `special` | Boosts `treat` and `special` |
| Nightcap | `good` | |

Tiers are adjustable per lot ("this is my Sunday bottle"), and the ceiling applies only as a penalty, never a block.

### Limits and the cellar
Hard limits are of two kinds, which the data model now says:
```js
{ field: "price", …, applies: "buy" }       // never stops you opening what you own
{ field: "colour" | "grape" | "place" | "abv" | "sweetness", …, applies: "both" }   // taste rules, always respected
```
Price limits apply to buying; taste limits apply to drinking too.

### What the home screen shows
1. **From your cellar tonight:** one lot, with the reason in one line ("Ready now, and the Chinon you opened Tuesday is fading, so this stays shut"), serve temperature and glass, and **Open it**.
2. **Still open:** bottles on the go, with days left.
3. **Or something new:** the discovery pick we have today, and a button to find one.

**Open it** writes an `opened` event, creates the `open` node, starts the fridge timer if the style needs chilling, and later offers **Log it**.

---

## 5. Cellar: the screen

- A header line: "38 bottles · 14 ready now · 6 ending soon · £1,120 paid".
- **Ready now / Hold / Ending soon / Open** as a segmented control. Rows show colour glass, the name in the house naming convention, quantity left, where it is, and a mini drinking-window bar with "now" marked.
- **Forecast:** a small bar chart of bottles reaching their window by year.
- **Gaps:** "No crisp white, no light red." Tapping one opens Scan in shop mode, or Explore filtered to that style.
- **Restock:** a finished lot you rated 4 or more shows "Buy again?", and passes to Explore with the bottle open.
- Swipe on a row to open, move or mark finished.

Valuation is paid-price only. Claret does not show market values, which would need a live source.

---

## 6. Journey: data

### What gets recorded at the moment it happens
Two small additions make the trail possible without guessing later.

**1. `lead` events.** When you open a wine from a recommendation, Claret records where it came from:
```js
{ kind: "lead", from: "vintage:…", to: "vintage:…",
  role: "sideways" | "same-grape" | "next-step" | "trade-up" | "trade-down" | "style" | "region" | "famous" | "search",
  at: "…" }
```
A tasting of `to` within 30 days of a `lead` stores it as `tasting.from`. If there is none, `from` is `manual`, `scan`, `cellar` or `suggestion`.

**2. `firsts` on each tasting,** written when it's logged and never recomputed, so a milestone is permanent:
```js
tasting.firsts = ["grape:albarino", "place:es/rias-baixas", "producer:martin-codax"]
```
It lists the grapes, places (at country, region and appellation level), producers and styles that are new to you at that moment.

### Derived: the `journey` doc (rebuilt from events)
| Part | Holds |
|---|---|
| `trail` | Ordered tastings with their `from` link, so each can draw an edge |
| `passport` | For each country, region, grape, producer and style: state, first date, count, average rating |
| `firsts` | The dated list of firsts |
| `rhythm` | By month: tastings, share that were new ground, average rating |
| `year` | The yearly review figures |

### Passport states
Each place, grape or style is in one of four states, from your own tastings:

| State | Rule |
|---|---|
| Not yet | No tastings |
| Tried | 1 tasting |
| Known | 3 or more tastings, or 2 or more producers |
| Loved | 3 or more tastings averaging 4 or above |

The denominators come from the atlas, so the numbers improve as the atlas grows ("17 of 150 grapes"). The atlas build (Wikidata and the EU appellation register) is a separate piece of work; Journey works with the atlas we have and gets richer with it.

---

## 7. Journey: the screen

- **Top line:** "17 grapes · 6 countries · 41 bottles" in large serif figures. Quiet, not a scoreboard.
- **Your trail.** A vertical path of glass-coloured dots, newest at the top. A ringed dot is new ground. A short label on each link says why you went there: "next step", "same grape elsewhere", "trade up". Tap a dot to open that wine. The trail reads like a route: Marlborough Sauvignon → Sancerre → Grüner Veltliner → Assyrtiko.
- **Passport.** Segmented: Grapes · Places · Producers · Styles. Each is a grid or map of stamps in the four states. Places show a map; tapping a country opens its region page in its own lettering.
- **Firsts.** "First Nerello Mascalese, 12 Nov, Brasserie, 4★". A short dated list; the newest is also shown as a one-off line on Tonight ("Your first Etna Rosso is in the cellar").
- **Comfort and new ground.** A line for the last ten tastings: familiar or new. If it has been all familiar for six weeks, one gentle prompt: "Six weeks in familiar territory. Try a step sideways?", with a button that nudges the explore dial. It can be switched off.
- **Your palate** in one sentence and a few chips: best-rated grapes, regions, styles.
- **Year in the glass.** From December: top regions, best bottle, biggest leap, bottles opened from the cellar versus bought on the day, what you spent.
- **Profile button:** limits, discovery dial, moment times, home city, export.

No streaks, badges or points. The point is a record that you want to look at.

---

## 8. Changes to `data-model.md`

| Section | Change |
|---|---|
| 2 (collections) | Add `store/nodes` types `lot` and `open`; `cellar` doc is derived, not hand-edited |
| 6 (events) | `bottle` kinds defined; new kind `lead`; `tasting` gains `from` and `firsts` |
| 7 (context) | `ctx.where`: `home`, `shop`, `out` |
| 8 (limits) | Each limit gains `applies`: `buy`, `drink` or `both` |
| 9 (derived) | `cellar`, `forecast`, `gaps`, `journey` |

Capacity: lots are hundreds of small docs; the heaviest growth stays in the monthly event docs. A cellar of 500 lots and ten years of tastings is well inside the 25,000-document limit.

---

## 9. Build order

1. **Where you are** and the home-screen split (cellar pick, still open, something new).
2. **Cellar:** lots, adding by scan and by hand, open bottles, the Cellar screen, the drink-next logic.
3. **Journey v1:** `lead` and `firsts` recording (do this first, as it can't be reconstructed later), the trail, and the passport with the current atlas.
4. Delivery-note reading, forecast chart and gaps in Scan.
5. Year in the glass, comfort prompts, map.

The `lead` and `firsts` recording should ship before anything else on this list, even with no Journey screen yet, because every tasting logged before then loses its history.

---

## 10. Decisions (24 Oct 2026)

1. **Per-bottle tracking for special ones.** Lots are counted by default; a lot can track each bottle (section 3).
2. **Ask how much is left.** After opening, never assume (section 3).
3. **Where you are:** Home, In a shop, Out. Three values, no more.
4. **Gifts, with who gave it.** Received and given, both recorded against a person (section 3).

---

## 11. Explore: browse by region, producer and grape

Explore becomes the place to wander. It is built from three kinds of card, each opening a full page laid out the same way (a hero, three round buttons, then what to drink and where to learn more).

### Layout
- **Search** across wines, regions, producers and grapes.
- A segmented control: **Regions · Producers · Grapes**, remembered between visits. Each is a two-column grid of cards.
- **Saved** (regions, producers, grapes and wines) and **The catalogue** below the grid.
- While searching, every kind that matches is shown under its own heading.

### Cards
| Kind | Card | Page hero |
|---|---|---|
| **Region** | Photo with the name in its own lettering. Regions without a photo get a tone and the lettering | Photo, lettering, the region's style, wines from here, grapes, photo credit |
| **Producer** | Photo of the estate (or its region) with the name | Photo, name and place; wines from them; the region it's in; a short note |
| **Grape** | A glass in the grape's own colour, with the name in italic and a line on how it tastes; a dot if you've logged it | The glass at large size on a deep tone, the name, how it tastes; classic places as region cards; next steps; trade up and down; your wines |

### The three round buttons (same on every page)
- **Info:** jumps to the About section.
- **Find bottles:** asks Claude for real UK-buyable wines for this region, producer or grape, with your limits applied. Results become wine pages marked as suggestions.
- **Save:** stars it; it appears under Saved in Explore and counts towards Journey.

### Producers
Producers come from the famous-names list with photos, plus every producer in your graph (catalogue, scans, suggestions). A producer without its own photo borrows its region's photo.

### Grapes
Each grape has a colour from the tasting scale, a one-line description, classic places that link to region cards, and "next step" grapes that link on to their own pages. This is where Journey's passport and Explore meet: a grape you have logged shows a dot, and the page shows your rating.

### Navigation
Detail pages keep a back stack, so region → grape → region → wine → back returns step by step, and tapping a bottom tab resets it.

---

## 12. Built so far (24 Oct 2026)

**Where you are.** A chip on Tonight (At home / In a shop / Out) switches the first screen. Shop and Out last three hours and are also set by starting a scan.

**Cellar.**
- Tab bar is now Tonight · Cellar · Explore · Journey, plus Scan. Journey holds the log; limits and settings sit behind a link at the top of it.
- Add bottles by typing a wine in, or from any wine page ("Add to cellar"), or from a scan result. A lot has a quantity, size, price paid, where it's kept, a tier (set from the price and changeable), an optional drinking window, a note, and optionally **Track each bottle** (switched on automatically for the Special tier or £80 and over).
- **Gifts:** switch "It was a gift" and say who gave it and why; it is stored against a person and shows as "From Sam, Birthday". **Give it away** records who got it.
- **Open it** reduces the count, creates an open bottle, and starts the fridge timer when the style needs chilling. **Still open** asks how much is left (Finished, a quarter, half, three quarters); Finished offers to log it.
- **Tonight at home** picks a style from the moment, weather and food as before, then leads with the best bottle you own for that style: open bottles that are fading first, then lots past or at the end of their window, then your palate, with a penalty when the tier is too grand for the occasion and for anything drunk in the last three days. Price limits never stop you opening what you own; taste limits always apply.
- **Cellar tab:** counts, paid total (gifts excluded), Ready / Hold / Ending / Open, a drinking-window bar per lot, and "Short of" styles that nothing in the cellar covers. In a shop, Scan shows the same gaps.

**Journey recording (the part that cannot be rebuilt later).** Every tasting now stores `firsts` (the grapes, places, producer and style that were new to you at that moment) and `from` (what led to it: a recommendation, a suggestion, a scan, the cellar, or manual). Opening a wine from "More like this" records a `lead` event with its role.

**Not built yet.** The Journey screens (trail, passport, firsts, year in the glass), the forecast chart, delivery-note reading, and Journey's "comfort vs new ground" prompt.

Also in this round: the maturity vocabulary is *Not ready yet · Ready – youthful · Ready – at best · Ready – mature · Past its best* (thirds of the window), and a wine whose name already contains its producer no longer repeats it in the "by" line. See `catalogue-learnings.md`.
