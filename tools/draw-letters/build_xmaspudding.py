"""x is for Xmas pudding (dx_xmaspudding_x), Food and drink a to z, slot x (22 Nov 2026).
From his pick "x1 Holly on top" (Claude's sketches, claude/step-by-draw-food-small-11-ideas-4-versions.md).

A round Christmas pudding with white icing, on a plate. On top are four holly leaves and three red berries.
The x is the middle lines of the four holly leaves.

    python3 build_xmaspudding.py
"""
import math
from fkit import *

GREEN, RED, BROWN, LBLUE = FILL['green'], FILL['red'], FILL['brown'], FILL['lblue']
CX, CY, H = 50.0, 35.0, 12.0                     # the x: its middle, and half its height
PX, BASE, RX, RY = 50.0, 90.0, 36.0, 46.0        # the pudding: middle, bottom, half its width, its height


def holly(ang):
    """a holly leaf from near the middle of the x out to the end of one of its lines (its middle is the line)"""
    d = (math.cos(math.radians(ang)), math.sin(math.radians(ang))); n = (-d[1], d[0])
    tip = P(CX + H * (1 if d[0] > 0 else -1), CY + H * (1 if d[1] > 0 else -1))
    L = math.dist((CX, CY), tip); b0 = 1.4
    at = lambda u, v: (CX + d[0] * (b0 + u) + n[0] * v, CY + d[1] * (b0 + u) + n[1] * v)
    Lu = L - b0
    side = [(0, 0), (0.33 * Lu, 0.27 * Lu), (0.66 * Lu, 0.40 * Lu), (Lu, 0)]
    pts = side + [(u, -v) for u, v in side[-2::-1]]
    pts = [at(u, v) for u, v in pts]; pts[0] = pts[-1] = P(*pts[0]); pts[3] = tip
    mid = at(Lu / 2, 0); out = []
    for a, b in zip(pts, pts[1:]):
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2); k = 0.22 * math.dist(a, b)
        g = (mid[0] - m[0], mid[1] - m[1]); gl = math.hypot(*g); g = (g[0] / gl * k, g[1] / gl * k)
        out.append(Seg(a, (a[0] + (b[0] - a[0]) / 3 + g[0], a[1] + (b[1] - a[1]) / 3 + g[1]),
                       (a[0] + 2 * (b[0] - a[0]) / 3 + g[0], a[1] + 2 * (b[1] - a[1]) / 3 + g[1]), b))
    return out


net = Net()
net.add('x1', Seg((CX - H, CY - H), (CX + H, CY + H)))                  # 1: the x
net.add('x2', Seg((CX + H, CY - H), (CX - H, CY + H)))
LEAVES = []
for k, ang in enumerate((225, 315, 45, 135)):                           # 2: the holly leaves
    net.add('leaf%d' % k, holly(ang)); LEAVES.append('leaf%d' % k)
BER = [(50, 22.4, 'b0'), (45.4, 17.2, 'b1'), (54.6, 17.2, 'b2')]       # 3: the berries (the front one first)
for x, y, nm in BER: net.add(nm, ell(x, y, 3.7))
dome = arc(PX, BASE, RX, RY, 180, 360) + [Seg((PX + RX, BASE), (PX - RX, BASE))]
dome[0] = Seg(P(PX - RX, BASE), *dome[0].p[1:]); dome[-2] = Seg(*dome[-2].p[:3], P(PX + RX, BASE))
net.add('pud', dome)                                                    # 4: the pudding
wave = [(-0.84, 0)] + [(-0.84 + 0.168 * i, (0.31, 0.36, 0.27, 0.35, 0.30)[(i - 1) // 2] if i % 2 else 0.56) for i in range(1, 10)] + [(0.84, 0)]
pts = []
for u, v in wave:
    if v == 0:
        a = math.acos(u); pts.append(P(PX + RX * math.cos(a), BASE - RY * math.sin(a)))
    else:
        pts.append((PX + RX * u, BASE - RY * v))
net.add('icing', smooth(pts))                                           # 5: the icing
net.add('plate', ell(PX, BASE, 44, 7, start=180))                       # 6: the plate
net.region('pudR', dome)
for i, nm in enumerate(LEAVES):
    net.region('L' + nm, holly((225, 315, 45, 135)[i]))
net.region('frontB', ell(50, 22.4, 3.7))
net.node()
for nm in ('pud', 'icing'):
    net.hide(nm, *['L' + l for l in LEAVES])
net.hide('b1', 'frontB'); net.hide('b2', 'frontB')
net.hide('plate', 'pudR')
CURR = [(PX - RX * 0.62, 84.5), (PX - RX * 0.24, 86.6), (PX + RX * 0.06, 83.6), (PX + RX * 0.34, 86.2), (PX + RX * 0.64, 84.0), (PX - RX * 0.4, 81.4), (PX + RX * 0.5, 80.2)]
dots = [dot(x, y, w=2.6) for x, y in CURR]


def leaf_fills():
    out = []
    for i, ang in enumerate((225, 315, 45, 135)):
        d = (math.cos(math.radians(ang)), math.sin(math.radians(ang))); n = (-d[1], d[0])
        for s in (1, -1):
            seed = (CX + d[0] * 10 + n[0] * 2.6 * s, CY + d[1] * 10 + n[1] * 2.6 * s)
            out.append(net.fill(GREEN, seed, names=['x1', 'x2', 'leaf%d' % i]))
    return out


steps = [
    step('Start with an x', 'Draw a small letter x: two straight lines that cross in the middle. This x is hiding in the holly.', net.lines('x1', 'x2')),
    step('The holly', 'Draw a spiky holly leaf round each line of the x, from near the middle out to the end.', net.lines(*LEAVES)),
    step('The berries', 'Above the holly, draw three little round berries.', net.lines('b0', 'b1', 'b2')),
    step('The pudding', 'Under the holly, draw a big round pudding with a flat bottom.', net.lines('pud')),
    step('The icing', 'Draw a wavy line across the top of the pudding, with drips going down. That is the icing.', net.lines('icing')),
    step('The plate', 'Draw a flat plate under the pudding. Add some dots on the pudding.', net.lines('plate') + dots),
    step('Colour green', 'Colour the holly leaves green, on both sides of each line.', leaf_fills(), use='green'),
    step('Colour red', 'Colour the berries red.',
         [net.fill(RED, (50, 22.4), names=['b0']), net.fill(RED, (44.2, 16.4), names=['b1', 'b0']), net.fill(RED, (55.8, 16.4), names=['b2', 'b0'])], use='red'),
    step('Colour brown', 'Colour the pudding brown, under the icing.', [net.fill(BROWN, (PX, 87), names=['pud', 'icing'])], use='brown'),
    step('Colour the plate', 'Colour the plate light blue.', [net.fill(LBLUE, (PX, 94), names=['pud', 'plate'])], use='lblue'),
]

D = drawing('dx_xmaspudding_x', 'x is for Xmas pudding', 2, 10, 'things', ['Letters', 'Around the house'],
            'A Christmas pudding with icing and holly. The small letter x is hiding in it: it is the middle lines of the holly leaves.',
            steps, ['green', 'red', 'brown', 'lblue'])
save('xmaspudding', D, {'set': 'house-az', 'slot': 'x', 'kind': 'key', 'age_from': 4})
