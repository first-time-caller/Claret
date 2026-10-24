# Outline "Claret" in Newsreader (OFL) at display optical size, weight 500, with HarfBuzz kerning.
import uharfbuzz as hb, io, json
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
src = '/tmp/claude-0/-home-user-westbourne/18b472fb-4b13-5a1d-9f28-c98ddb041701/scratchpad/mocks/fonts/f4.woff2'
f = TTFont(src); f.flavor = None
inst = instantiateVariableFont(f, {'wght': 500, 'opsz': 72})
buf = io.BytesIO(); inst.save(buf); data = buf.getvalue()
face = hb.Face(data); font = hb.Font(face)
b = hb.Buffer(); b.add_str('Claret'); b.guess_segment_properties(); hb.shape(font, b, {'kern': True, 'liga': True})
gs = inst.getGlyphSet(); order = inst.getGlyphOrder(); upm = inst['head'].unitsPerEm
pen = SVGPathPen(gs); x = 0
for info, pos in zip(b.glyph_infos, b.glyph_positions):
    name = order[info.codepoint]
    gs[name].draw(TransformPen(pen, (1, 0, 0, -1, x + pos.x_offset, 0)))
    x += pos.x_advance
d = pen.getCommands()
# bounds
from fontTools.pens.boundsPen import BoundsPen
bp = BoundsPen(gs); x2 = 0
for info, pos in zip(b.glyph_infos, b.glyph_positions):
    gs[order[info.codepoint]].draw(TransformPen(bp, (1, 0, 0, 1, x2, 0))); x2 += pos.x_advance
xmin, ymin, xmax, ymax = bp.bounds
json.dump({'d': d, 'xmin': xmin, 'xmax': xmax, 'top': -ymax, 'bottom': -ymin, 'upm': upm}, open('/tmp/claude-0/-home-user/18b472fb-4b13-5a1d-9f28-c98ddb041701/scratchpad/logos/word.json', 'w'))
print(round(xmin), round(xmax), round(-ymax), round(-ymin), len(d))
