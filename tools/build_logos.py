#!/usr/bin/env python3
"""Turn raw logo files into the transparent masks Claret draws in white.

  python3 tools/build_logos.py [raw_dir] [out_dir]

Name each raw file after the producer's slug, e.g. church-road.png, trinity-hill.jpg.
Anything with a transparent background keeps its alpha; a logo on white or any light
background is converted by how far each pixel is from the background. Output: one PNG per
logo in img/logos plus img/logos/index.json ({slug: width/height}) which the app reads."""
import sys, json, glob, os
import numpy as np
from PIL import Image

raw = sys.argv[1] if len(sys.argv) > 1 else 'images/logos/raw'
out = sys.argv[2] if len(sys.argv) > 2 else 'img/logos'
os.makedirs(out, exist_ok=True)
idx_path = os.path.join(out, 'index.json')
index = json.load(open(idx_path)) if os.path.exists(idx_path) else {}

def alpha_of(a):
    if (a[..., 3] < 250).mean() > 0.1:               # already has a transparent background
        return a[..., 3] / 255
    bg = np.median(np.concatenate([a[0, :, :3], a[-1, :, :3], a[:, 0, :3], a[:, -1, :3]]), axis=0)
    dist = np.abs(a[..., :3] - bg).max(axis=2)       # distance from the background colour
    al = np.clip(dist * 1.8 / 255, 0, 1)
    return np.where(al < 0.06, 0, al)

for f in sorted(glob.glob(os.path.join(raw, '*'))):
    slug, ext = os.path.splitext(os.path.basename(f))
    if ext.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
        continue
    a = np.array(Image.open(f).convert('RGBA')).astype(float)
    arr = np.zeros(a.shape, np.uint8); arr[..., 3] = (alpha_of(a) * 255).astype(np.uint8)
    im = Image.fromarray(arr)
    im = im.crop(im.split()[3].point(lambda v: 255 if v > 25 else 0).getbbox())
    if im.width > 900:
        im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    im.save(os.path.join(out, slug + '.png'), optimize=True)
    index[slug] = round(im.width / im.height, 3)
    print(slug, im.size)
for f in glob.glob(os.path.join(out, '*.png')):         # keep every logo already in the folder listed
    slug = os.path.splitext(os.path.basename(f))[0]
    if slug not in index:
        w, h = Image.open(f).size; index[slug] = round(w / h, 3)
json.dump(dict(sorted(index.items())), open(idx_path, 'w'), indent=1)
