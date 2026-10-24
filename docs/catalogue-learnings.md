# What two UK merchants' bestsellers say about building a catalogue

Source: the Berry Bros. & Rudd "All wines" page (its filters, and 24 best-selling listings) and Hedonism's wine listing (7,048 wines, its filters and facet counts, and the top 20 by "Best Selling"), pasted by the owner on 24 Oct 2026. Counts below are from that paste. Nothing here is live data.

## What the numbers show

| Finding | BBR | Hedonism |
|---|---|---|
| **Price sits in a narrow band** | 20 of 24 bestsellers are under £30; 15 are £13.95–£19.95; the median is £17.50 | Only 459 of 7,048 wines (6.5%) are under £30, yet the top-20 NV Champagnes cluster around £42–£60 |
| **A few categories dominate** | Own-label "style by producer" wines: all 24 titles begin "Berry Bros. & Rudd" | 17 of the top 20 are Champagne; the rest are Prosecco, Franciacorta and Tignanello |
| **Geography is lopsided** | | France 54% of the range; Burgundy 21%, Bordeaux 16%, Champagne 8%; California 11% |
| **Recent vintages lead** | 2023–2025 on nearly every card | NV for most Champagne; a few old vintages (Dom Pérignon 2009, 2010) |
| **Every card says how ready it is** | "Ready – youthful / at best / mature" on every one | Not shown; critic scores take its place |
| **One wine, several formats** | 75 cl, 37.5 cl half, 150 cl magnum, 300 cl, each with its own price, under one listing | Half and Magnum are separate listings ("Ruinart Blanc de Blancs Half") |

## What we should take

**1. Name the wine the way a person asks for it.** BBR sells "White Burgundy by Collovray & Terrier", "Sancerre by Domaine David Sautereau", "Good Ordinary Claret by Dourthe". The buyer chooses the style or appellation first and the producer second. We already show `{vintage} {wine}, by {producer}, {region}`. One refinement: when the wine's name already contains the producer (Pol Roger Brut Réserve, Dom Pérignon 2010), drop the "by" line and show the region instead.

**2. One maturity vocabulary, on every card.** BBR's three "Ready" states are enough to turn a drinking window into a decision. We use: *Not ready yet · Ready – youthful · Ready – at best · Ready – mature · Past its best*, worked out by dividing the window into thirds. The Cellar uses it for sorting and for "ending soon".

**3. Separate colour from type.** Hedonism filters by **Colour** (Red 4,563 · White 2,485 · Rosé 224 · Other 4) *and* by **Wine Type** (Still 6,065 · Sparkling 674 · Sweet 166 · Fortified 143). Champagne is a white wine and a sparkling wine, and a rosé Champagne is the same type in a different colour. Our `family` field mixes the two. The fix is two claims, `colour` and `type`, with `family` derived for the interface. This matters for hard limits too: "no sparkling" and "no white" are different rules.

**4. A wine has formats and prices, not copies.** BBR lists bottle, half, magnum and double magnum under one wine. We should do the same: `offers: [{ size, price, source }]`. For home drinking this unlocks a useful suggestion: **a half bottle for a weeknight**, a magnum for a gathering. Cellar lots already carry `size`.

**5. Filters and limits are the same thing.** Both sites filter by colour, country, region, grape, vintage, price, size and alcohol. Those are, nearly one for one, our hard limits (colour, price, place, grape, ABV, size, sweetness). So Explore filters should use the limits schema, and "Save this filter as a limit" should be one tap. Show counts beside each value, as Hedonism does ("Burgundy 1,511"), so the user can see what's there.

**6. Build the first catalogue from what people actually buy.** The top of both lists is dull and valuable: well-known Champagne houses, everyday own-label bottles, a handful of famous reds. A catalogue seeded from fine-wine lists would be wrong for the curious regular. Seed from UK bestsellers at £10–£60, then let scans and sightings widen it. The atlas must be deepest where the stock is: Burgundy, Bordeaux, Champagne, Tuscany, California and Napa, and below region level for Bordeaux (Pauillac 174, Saint-Émilion Grand Cru 174, Pomerol 139, Margaux 119).

**7. Blends need their own class.** Hedonism's grape field says "Champagne Blend" and "Cabernet – Sangiovese". "Champagne Blend" is not a grape, it's an archetype where the label does not name the grapes. We should keep `blend` as a structured list and add **blend archetypes** (Bordeaux blend, Champagne blend, Rhône blend, Port blend, Super Tuscan) as browsable pages next to grapes. They are among the most-bought wines.

**8. The grape list has a very long tail.** Hedonism's grape facet runs from Albariño (20) to Albillo (2) and Alicante Bouschet (1). A handful of grapes carry most wines. Explore should lead with the classics and keep the long tail one tap away, as it does now.

**9. Card anatomy.** What both sites put on a card, in order of importance:
1. Name in the house naming convention, with a bottle or label image.
2. A one-line identity: **colour · ABV · region, country · grape(s)**.
3. Maturity status (BBR) or critic scores (Hedonism).
4. Price **and** size together ("£17.50 · 75 cl").
5. A small set of badges: *Organic, Capsule-free, Bestseller, New*.
6. Availability: "326 left" is a trust signal. Hedonism shows it on every card.

We have 1, 3 (both), and 4. Adding the identity line, ABV and size to wine rows is a small change.

**10. Critic scores need a key and a scale.** Hedonism shows up to four per wine, abbreviated, on two scales: Robert Parker / Wine Advocate (RP) and Vinous (Vin) out of 100, Jancis Robinson (JR) out of 20 (16–18.5). Show the two or three most relevant on the card and all of them on the page, with the critic and scale always spelled out on tap. Some of the other single-letter codes need a key before use.

## What we should leave

- **En primeur, case size, price per case, stock origin, in bond, BBX.** These serve people buying fine wine to hold. They matter only if Claret grows a collector side. Case deals do matter as a *lot quantity*.
- **Gift box** and **New to BBX**: merchant-specific.
- **Sort by "Best selling".** For us the default sort is "Best for tonight".

## Changes this drives

| Area | Change |
|---|---|
| Naming | Drop "by {producer}" when the name contains the producer |
| Maturity | Thirds-based status vocabulary (done) |
| Data model | `colour` and `type` as separate claims; `offers` with sizes; blend archetypes |
| Catalogue | Seed from UK bestsellers £10–£60; atlas depth follows stock |
| Explore | Filters use the limits schema, with counts; "Save as limit" |
| Wine rows | Identity line, ABV, size beside price, badges |
| Cellar | A lot has a size; half bottles and magnums are first-class |
