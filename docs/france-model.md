# France: a bespoke place model (draft for discussion)

New Zealand and Australia fit the simple model: country > island or state > region, with key varieties and a terroir blurb. France does not, for four reasons: far more places (roughly 360 appellations), several overlapping classification systems, a hierarchy that changes by region, and the estate/négociant split. This draft sets out what the model needs. Nothing here is built yet.

## 1. The place hierarchy is not one ladder

Levels the app needs, with examples:

| Level | Examples | Notes |
|---|---|---|
| Country | France | |
| Wine region | Bordeaux, Burgundy, Champagne, Rhône, Loire, Alsace, Languedoc-Roussillon, Provence, South West, Jura & Savoie, Beaujolais, Corsica | Roughly a dozen; what Explore shows |
| Sub-region | Médoc, Côte d'Or (Côte de Nuits, Côte de Beaune), Northern and Southern Rhône, Anjou-Saumur, Touraine | Optional step; not every region has one |
| Appellation | Margaux, Pauillac, Chablis, Meursault, Hermitage, Sancerre | The unit people buy by |
| Classified vineyard tier | Premier Cru, Grand Cru (Burgundy, Chablis, Alsace, Champagne villages) | A tier of an appellation, not a separate place |
| Named vineyard (climat, lieu-dit) | Clos de Vougeot, Les Amoureuses, Montrachet | Burgundy has about 640 climats; a place in its own right |

Decision needed: model Premier/Grand Cru as a **level**, a **tier property** on a place, or both. Proposal: both. Montrachet is a place (a Grand Cru vineyard) with `tier: Grand Cru`, and the app can filter by tier.

## 2. Classification is a separate axis

Quality systems cut across geography and differ by region. They should be their own records, attached to estates or places, not baked into the hierarchy:

- **Bordeaux Left Bank, 1855:** five growths for estates (Château Margaux is a Premier Cru Classé). Applies to producers, not places.
- **Saint-Émilion:** Grand Cru Classé, revised periodically. Estates again.
- **Burgundy:** four tiers (regional, village, Premier Cru, Grand Cru), applied to vineyards. Places.
- **Champagne:** village ratings (Grand Cru and Premier Cru villages) plus house styles (NV, vintage, prestige cuvée).
- **Alsace:** Grand Cru vineyards; **Beaujolais:** ten named crus; **Cru Bourgeois, Cru Artisan** for Médoc.

Proposal: a `classification` record `{system, tier, applies_to, year}` so a wine card can say "Premier Grand Cru Classé (1855)" without a special case per region.

## 3. Producers: estate, négociant, grower, co-operative

France needs a `producer_type`: estate, négociant, grower-producer (Champagne), co-operative, domaine with many parcels. It matters most in Burgundy, where one producer may own parcels in 20 appellations. Rule from earlier stands: an estate named after its appellation (Château Margaux, Château Pétrus) is a producer row, separate from the appellation.

## 4. Data volume and how it loads

About 360 appellations plus Burgundy climats is far larger than the current inline data. Proposals:

- Move place data out of `index.html` into `img/france.json` (and similar per country), loaded lazily when France is opened.
- Keep Explore's top level to the dozen regions; everything below loads on demand.
- Maps: départements are good for regions, but appellation boundaries are not available freely at useful detail. Use rough ellipses as now, and add real shapes only where open data exists (INAO publishes appellation boundaries; licence to confirm).

## 5. What we show on a place page

Same sections as New Zealand (breadcrumb, map, key varieties, terroir, top producers) plus, for France:

- **Classification** panel (which systems apply, with a short plain-English explanation).
- **Appellation ladder** in Burgundy, shown as the four tiers rather than a flat list.
- **Style by colour** (Bordeaux: red appellations vs sweet vs dry white), since appellations often allow only one colour.

## Open questions for you

1. Level of detail for launch: all of Bordeaux and Burgundy first, then the rest at region level only?
2. Do you want a Burgundy tier ladder (Bourgogne > village > Premier Cru > Grand Cru) as a dedicated view?
3. Is a classification panel useful on every page, or only where a system exists?
4. Source of truth: can you supply tables like the New Zealand one (region, key varieties, terroir and style) per French region? That gives wording in your voice.
5. Producers: how many to seed per region, and are négociants (Louis Jadot, Bouchard) welcome alongside estates?
