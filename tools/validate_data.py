#!/usr/bin/env python3
"""Check data/*.json before publishing:  python3 tools/validate_data.py
Exits non-zero if anything is wrong, so a typo shows up here instead of as a broken page."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = os.path.join(ROOT, 'data')
idx = json.load(open(os.path.join(data, 'index.json')))
LEVELS = {'Country', 'Island', 'State', 'Region', 'Appellation'}
errors, warns = [], []
def err(m): errors.append(m)

places = {}
for f in idx['places']:
    for p in json.load(open(os.path.join(data, f))):
        if p['id'] in places: err(f'duplicate place id {p["id"]} ({f})')
        places[p['id']] = (p, f)
windows = json.load(open(os.path.join(data, idx['windows'])))
credits = {}
for c in ('credits.json', 'producers.json'):
    fp = os.path.join(ROOT, 'img', c)
    if os.path.exists(fp): credits.update(json.load(open(fp)))
place_ids = {}
for k, (p, f) in places.items():
    for req in ('name', 'country', 'blurb'):
        if not p.get(req): err(f'{k}: missing {req}')
    if p.get('level') and p['level'] not in LEVELS: err(f'{k}: unknown level {p["level"]}')
    if p.get('parent') and p['parent'] not in places: err(f'{k}: parent {p["parent"]} not found')
    seen, x = set(), k
    while x and places.get(x, ({},))[0].get('parent'):
        x = places[x][0]['parent']
        if x in seen or x == k: err(f'{k}: parent loop'); break
        seen.add(x)
    lt = p.get('lettering')
    if lt:
        for req in ('t', 'f', 'size', 'card', 'tone'):
            if req not in lt: err(f'{k}: lettering missing {req}')
    m = p.get('map')
    if not m: warns.append(f'{k}: no map')
    else:
        if m.get('window') not in windows: err(f'{k}: unknown map window {m.get("window")}')
        if not ('admin1' in m or 'blob' in m): err(f'{k}: map needs admin1 or blob')
        if 'blob' in m and len(m['blob']) != 5: err(f'{k}: blob needs [lon, lat, long, short, angle]')
    if p.get('photo') and p['photo'] not in credits and p['photo'] not in places: warns.append(f'{k}: photo alias {p["photo"]} has no credit entry')
    for pid in p.get('places', []):
        if not pid.startswith('place:'): err(f'{k}: place id {pid} should start with place:')
        if pid in place_ids and place_ids[pid] != k: err(f'{pid} maps to both {place_ids[pid]} and {k}')
        place_ids[pid] = k

prods = json.load(open(os.path.join(data, idx['producers'])))
names = set()
logos = set()
lp = os.path.join(ROOT, 'img', 'logos', 'index.json')
if os.path.exists(lp): logos = set(json.load(open(lp)))
for p in prods:
    for req in ('name', 'place', 'blurb'):
        if not p.get(req): err(f'producer {p.get("name")}: missing {req}')
    if p['name'] in names: err(f'duplicate producer {p["name"]}')
    names.add(p['name'])
    if p.get('region') and p['region'] not in places: err(f'producer {p["name"]}: region {p["region"]} not found')
    if not p.get('region'): warns.append(f'producer {p["name"]}: no region')
    if p.get('photo') and p['photo'] not in credits and not p.get('photoFrom'): warns.append(f'producer {p["name"]}: photo {p["photo"]} not in credits')
for w in warns: print('warning:', w)
for e in errors: print('ERROR:', e)
print(f'{len(places)} places, {len(prods)} producers, {len(logos)} logos: {len(errors)} errors, {len(warns)} warnings')
sys.exit(1 if errors else 0)
