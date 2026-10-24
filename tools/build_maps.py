#!/usr/bin/env python3
"""Build img/maps.json (the region maps) from the map specs in data/places/*.json.

  python3 tools/build_maps.py

Each place may carry  "map": {"window": "FR", "admin1": ["Gironde"]}  (highlight these political areas)
or                    "map": {"window": "BDX", "blob": [lon, lat, long_half, short_half, angle]}  (a rough ellipse)
and optionally        "ctx": ["South Australia"]  (an outline drawn around the highlight for context).
Windows (the map frame) are defined in data/map-windows.json. Boundaries come from Natural Earth
(public domain), downloaded to tools/.cache on first run."""
import json, math, os, sys, glob, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'tools', '.cache'); os.makedirs(CACHE, exist_ok=True)
NE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'
def ne(name):
    f = os.path.join(CACHE, name)
    if not os.path.exists(f):
        print('downloading', name); urllib.request.urlretrieve(NE + name, f)
    return json.load(open(f))['features']
a1 = ne('ne_10m_admin_1_states_provinces.geojson'); a0 = ne('ne_50m_admin_0_countries.geojson')
W = 300
def ellipse(c):
    lon,lat,a,b,ang=c; th=math.radians(ang); pts=[]
    for i in range(24):
        t=2*math.pi*i/24; x=a*math.cos(t); y=b*math.sin(t)
        xr=x*math.cos(th)-y*math.sin(th); yr=x*math.sin(th)+y*math.cos(th)
        pts.append((lon+xr/math.cos(math.radians(lat)),lat+yr))
    return {'type':'Polygon','coordinates':[pts]}
def proj(win):
    lon0,lat0,lon1,lat1=win; k=math.cos(math.radians((lat0+lat1)/2)); wd=(lon1-lon0)*k; ht=(lat1-lat0); s=W/wd
    return (lambda lon,lat:((lon-lon0)*k*s,(lat1-lat)*s)), round(ht*s)
def clip(poly,w,h):
    def edge(pts,inside,inter):
        out=[]
        for i,p in enumerate(pts):
            q=pts[i-1]
            if inside(p):
                if not inside(q): out.append(inter(q,p))
                out.append(p)
            elif inside(q): out.append(inter(q,p))
        return out
    pts=poly
    for ins,it in [(lambda p:p[0]>=0,lambda a,b:(0,a[1]+(b[1]-a[1])*(0-a[0])/(b[0]-a[0]))),(lambda p:p[0]<=w,lambda a,b:(w,a[1]+(b[1]-a[1])*(w-a[0])/(b[0]-a[0]))),(lambda p:p[1]>=0,lambda a,b:(a[0]+(b[0]-a[0])*(0-a[1])/(b[1]-a[1]),0)),(lambda p:p[1]<=h,lambda a,b:(a[0]+(b[0]-a[0])*(h-a[1])/(b[1]-a[1]),h))]:
        if not pts: return []
        pts=edge(pts,ins,it)
    return pts
def dp(pts,t):
    if len(pts)<3: return pts
    def d(p,a,b):
        dx,dy=b[0]-a[0],b[1]-a[1]; L=dx*dx+dy*dy
        if L==0: return math.hypot(p[0]-a[0],p[1]-a[1])
        u=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/L)); return math.hypot(p[0]-(a[0]+u*dx),p[1]-(a[1]+u*dy))
    st=[(0,len(pts)-1)]; keep=[False]*len(pts); keep[0]=keep[-1]=True
    while st:
        i,j=st.pop(); m=-1;idx=-1
        for k in range(i+1,j):
            dd=d(pts[k],pts[i],pts[j])
            if dd>m: m=dd;idx=k
        if m>t: keep[idx]=True; st.append((i,idx)); st.append((idx,j))
    return [p for p,k in zip(pts,keep) if k]
def rings(geom):
    if geom['type']=='Polygon': return [geom['coordinates'][0]]
    if geom['type']=='MultiPolygon': return [p[0] for p in geom['coordinates']]
    return []
def path(geoms,win,tol):
    P,H=proj(win); out=[]; lon0,lat0,lon1,lat1=win; pad=1
    for g in geoms:
        for r in rings(g):
            lons=[p[0] for p in r]; lats=[p[1] for p in r]
            if max(lons)<lon0 or min(lons)>lon1 or max(lats)<lat0 or min(lats)>lat1: continue
            pts=[P(x,y) for x,y in r]; pts=clip(pts,W,H)
            if len(pts)<3: continue
            pts=dp(pts,tol)
            if len(pts)<3: continue
            # skip specks
            xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
            if (max(xs)-min(xs))<2.5 and (max(ys)-min(ys))<2.5: continue
            out.append('M'+'L'.join('%g %g'%(round(x,1),round(y,1)) for x,y in pts)+'Z')
    return ''.join(out),H

data = os.path.join(ROOT, 'data')
idx = json.load(open(os.path.join(data, 'index.json')))
WIN = {k: tuple(v['bbox']) for k, v in json.load(open(os.path.join(data, idx['windows']))).items()}
WINDEF = json.load(open(os.path.join(data, idx['windows'])))
res = {'win': {}, 'reg': {}}
def admin1(iso, names):
    out = [f['geometry'] for f in a1 if f['properties']['iso_a2'] == iso and f['properties']['name'] in names]
    if len(out) != len(names): print('  warning: some admin1 names not found:', iso, names)
    return out
for f in idx['places']:
    for p in json.load(open(os.path.join(data, f))):
        m = p.get('map')
        if not m: continue
        w = m['window']; win = WIN[w]; iso = f.split('/')[-1][:2].upper()
        if w not in res['win']:
            land, H = path([x['geometry'] for x in a0], win, 0.5 if WINDEF[w].get('ctx') else 1.0)
            res['win'][w] = {'h': H, 'land': land}
            c = WINDEF[w].get('ctx')
            if c: res['win'][w]['ctx'] = path(admin1(c['iso'], c['admin1']), win, .5)[0]
        if 'admin1' in m: gs, tol = admin1(iso, m['admin1']), .6
        else:
            lon, lat, a, b, ang = m['blob']; gs, tol = [ellipse((lon, lat, a, b, ang))], .15
        hi, _ = path(gs, win, tol); res['reg'][p['id']] = {'w': w, 'hi': hi}
        if m.get('ctx'): res['reg'][p['id']]['ctx'] = path(admin1(iso, m['ctx']), win, .5)[0]
out = os.path.join(ROOT, 'img', 'maps.json')
js = json.dumps(res, separators=(',', ':'), ensure_ascii=False)
open(out, 'w').write(js); print('wrote', out, len(js), 'bytes;', len(res['reg']), 'places')
