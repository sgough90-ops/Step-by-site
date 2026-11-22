"""m is for Mushrooms (dx_mushrooms_m), Food and drink a to z, slot m (22 Nov 2026).
From his pick "m4 Growing in the woods" (Claude's sketches, claude/step-by-draw-food-small-11-ideas-4-versions.md).

Two tall mushrooms growing side by side on the ground, with a little one on each side. The m is the tops of the two
big caps: its two humps.

    python3 build_mushrooms.py
"""
import math
from fkit import *

BROWN, GREEN = FILL['brown'], FILL['green']
X0, XM, X1, TOP, RIM = 20.0, 50.0, 80.0, 14.0, 52.0
R = (XM - X0) / 2; SH = TOP + R                       # the humps' radius, and where the straight sides start


def hump(xa, xb):
    return arc((xa + xb) / 2, SH, R, R, 180, 360, start=P(xa, SH), end=P(xb, SH))


def lip(xa, xb, rim, dip, inset):
    """under a cap, from its right corner round to its left corner"""
    return [Seg((xb, rim), (xb - 0.4, rim + dip * 0.7), (xb - inset * 0.4, rim + dip), (xb - inset, rim + dip)),
            Seg((xb - inset, rim + dip), (xa + inset, rim + dip)),
            Seg((xa + inset, rim + dip), (xa + inset * 0.4, rim + dip), (xa + 0.4, rim + dip * 0.7), (xa, rim))]


def stem_sides(xc, y0, y1, w):
    a, b = xc - w / 2, xc + w / 2; m = (y0 + y1) / 2
    return (Seg((a, y0), (a - w * 0.1, m), (a - w * 0.2, y1 - 5), (a - w * 0.1, y1)),
            Seg((b, y0), (b + w * 0.1, m), (b + w * 0.2, y1 - 5), (b + w * 0.1, y1)))


def small_cap(xa, xb, top, rim):
    r = (xb - xa) / 2; sh = top + r
    return [Seg((xa, rim), (xa, sh))] + arc((xa + xb) / 2, sh, r, r, 180, 360, start=P(xa, sh), end=P(xb, sh)) + [Seg((xb, sh), (xb, rim))]


net = Net()
net.add('m1', Seg((X0, RIM), (X0, SH)), hump(X0, XM), Seg((XM, SH), (XM, RIM)))      # 1: the m
net.add('m2', hump(XM, X1), Seg((X1, SH), (X1, RIM)))
net.add('lipL', lip(X0, XM, RIM, 4.5, 6))                                           # 2: under the caps
net.add('lipR', lip(XM, X1, RIM, 4.5, 6))
SB = 90.0
for nm, xc in (('sL', 35.0), ('sR', 65.0)):                                         # 3: the stems
    a, b = stem_sides(xc, 55, SB, 15)
    net.add(nm + 'a', a); net.add(nm + 'b', b)
    net.region('st' + nm, a, Seg(a.b, b.b), b.rev(), Seg(b.a, a.a))
capL = small_cap(3.5, 16.5, 62, 72); capR = small_cap(85.5, 96.5, 68, 76.5)       # 4: the little mushrooms
net.add('cL', capL, lip(3.5, 16.5, 72, 3, 2.5)); net.add('cR', capR, lip(85.5, 96.5, 76.5, 3, 2.5))
for nm, (xc, y0, w) in (('tL', (10, 74, 5)), ('tR', (91, 78, 4.4))):
    a, b = stem_sides(xc, y0, SB, w); net.add(nm + 'a', a); net.add(nm + 'b', b)
gtop = [Seg((2, 92), (6, 84), (30, 85), (50, 85.5)), Seg((50, 85.5), (70, 85), (94, 84), (98, 92))]
ground = gtop + [Seg((98, 92), (98, 96), (2, 96), (2, 92))]
net.add('ground', ground)                                                           # 5: the ground


def gy(x):
    s = gtop[0] if x < 50 else gtop[1]; t = seg_x(s, x); return P(*s.at(t))


def tuft(x, h=5.5):
    xs = [x - 4.2, x - 2.8, x - 1.4, x, x + 1.4, x + 2.8, x + 4.2]
    pts = [gy(xs[0])] + [(xx, gy(xx)[1] - (h if k % 2 == 0 else 1.8) * (0.8 if k in (0, 4) else 1)) for k, xx in enumerate(xs[1:-1])] + [gy(xs[-1])]
    return [Seg(a, b) for a, b in zip(pts, pts[1:])]


TUFTS = []
for k, x in enumerate((19.6, 50.0, 80.4)):
    net.add('g%d' % k, tuft(x)); TUFTS.append('g%d' % k)
net.region('capLR', net.all('m1')[:-1], Seg((XM, SH), (XM, RIM)), lip(X0, XM, RIM, 4.5, 6))
net.region('capRR', Seg((XM, RIM), (XM, SH)), hump(XM, X1), Seg((X1, SH), (X1, RIM)), lip(XM, X1, RIM, 4.5, 6))
net.region('cLR', capL, lip(3.5, 16.5, 72, 3, 2.5)); net.region('cRR', capR, lip(85.5, 96.5, 76.5, 3, 2.5))
net.region('gR', ground)
net.node()
for nm in ('sLa', 'sLb'): net.hide(nm, 'capLR', 'gR')
for nm in ('sRa', 'sRb'): net.hide(nm, 'capRR', 'gR')
for nm in ('tLa', 'tLb'): net.hide(nm, 'cLR', 'gR')
for nm in ('tRa', 'tRb'): net.hide(nm, 'cRR', 'gR')
shine = [line(*arc(35, SH, R * 0.68, R * 0.68, 205, 245)), line(*arc(65, SH, R * 0.68, R * 0.68, 205, 245))]
STEMS = ['sLa', 'sLb', 'sRa', 'sRb']

steps = [
    step('Start with an m', 'Draw a small letter m: a line down, then two round humps. This m is hiding in the mushrooms.', net.lines('m1', 'm2')),
    step('Under the caps', 'Under each hump, draw a curved line from one side to the other. Now they are two mushroom caps.', net.lines('lipL', 'lipR')),
    step('The stems', 'Under each cap, draw two lines going down for a fat stem.', net.lines(*STEMS)),
    step('Two little ones', 'Draw a tiny mushroom on each side: a little round cap and a thin stem.', net.lines('cL', 'cR', 'tLa', 'tLb', 'tRa', 'tRb')),
    step('The ground', 'Draw the ground across the bottom of all the stems. Add three little tufts of grass.', net.lines('ground', *TUFTS)),
    step('The shine', 'Draw a little curved line near the top of each big cap, to make it shine.', shine),
    step('Colour brown', 'Colour all four mushroom caps brown.',
         [net.fill(BROWN, (35, 40), names=['m1', 'lipL']), net.fill(BROWN, (65, 40), names=['m1', 'm2', 'lipR']),
          net.fill(BROWN, (10, 69), names=['cL']), net.fill(BROWN, (91, 73), names=['cR'])], use='brown'),
    step('Colour green', 'Colour the ground and the grass green.',
         [net.fill(GREEN, (50, 92), names=['ground'] + STEMS + ['tLa', 'tLb', 'tRa', 'tRb'])] +
         [net.fill(GREEN, (x, gy(x)[1] - 1.0), names=['ground', 'g%d' % k]) for k, x in enumerate((19.6, 50.0, 80.4))], use='green'),
]

D = drawing('dx_mushrooms_m', 'm is for Mushrooms', 2, 10, 'things', ['Letters', 'Around the house'],
            'Two big mushrooms and two little ones growing in the woods. The small letter m is hiding in them: it is the tops of the two big caps.',
            steps, ['brown', 'green'])
save('mushrooms', D, {'set': 'house-az', 'slot': 'm', 'kind': 'key', 'age_from': 4})
