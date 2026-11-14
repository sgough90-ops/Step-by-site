"""m is for mittens (Around the house a to z, slot m).
The m: its two arches are the round tops of the two mittens and its three straight lines are their sides.
Everything else hangs from the m or touches it: nothing covers it or crosses it."""
import json, math, os, sys
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
ZIG = '--plain' not in sys.argv

X0, X1, X2 = 29.0, 50.0, 71.0
YS, YB = 29.0, 58.0
RY = 11.0

stick0 = Seg((X0, YS), (X0, YB))
arch1 = arc((X0 + X1) / 2, YS, (X1 - X0) / 2, RY, 180, 360, start=P(X0, YS), end=P(X1, YS))
stick1 = Seg((X1, YS), (X1, YB))
arch2 = arc((X1 + X2) / 2, YS, (X2 - X1) / 2, RY, 180, 360, start=P(X1, YS), end=P(X2, YS))
stick2 = Seg((X2, YS), (X2, YB))

bottom = Seg((X0, YB), (X2, YB))

TA, TB = 33.0, 43.6
thumbL = [Seg((X0, TB), (23.4, 45.2), (16.6, 38.6), (18.3, 32.4)),
          Seg((18.3, 32.4), (19.6, 27.6), (25.6, 27.6), (X0, TA))]
thumbR = mirror(thumbL)

def cloud(circles, start, end):
    """Outline along the undersides of overlapping circles, from start (on the first) to end (on the last)."""
    def ang(c, p): return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
    def lower(c1, c2):
        (x1, y1, r1), (x2, y2, r2) = c1, c2
        d = math.hypot(x2 - x1, y2 - y1); a = (r1 * r1 - r2 * r2 + d * d) / (2 * d); h = math.sqrt(r1 * r1 - a * a)
        ux, uy = (x2 - x1) / d, (y2 - y1) / d; px, py = x1 + a * ux, y1 + a * uy
        q1 = (px - h * uy, py + h * ux); q2 = (px + h * uy, py - h * ux)
        return P(*(q1 if q1[1] > q2[1] else q2))
    pts = [P(*start)] + [lower(circles[i], circles[i + 1]) for i in range(len(circles) - 1)] + [P(*end)]
    segs = []
    for i, (cx, cy, r) in enumerate(circles):
        a0 = ang((cx, cy), pts[i]); a1 = ang((cx, cy), pts[i + 1])
        if i == 0:
            while a0 < a1 + 1e-9: a0 += 360
        if i == len(circles) - 1:
            while a1 > a0 - 1e-9: a1 -= 360
        if a0 < a1: a0, a1 = a0, a1 - 360
        segs += arc(cx, cy, r, r, a0, a1, start=pts[i], end=pts[i + 1])
    return segs

EIN = 45.9
cL = [(30.1, 61.95, math.hypot(30.1 - X0, 61.95 - YB)), (37.45, 62.9, 4.1), (44.8, 61.95, math.hypot(44.8 - EIN, 61.95 - YB))]
cuffL = cloud(cL, (X0, YB), (EIN, YB))
cuffR = rev(mirror(cuffL))
cuffR_fwd = mirror(cuffL)

S1, S2 = 47.0, 53.6
stripes = [Seg((X0, S1), (X1, S1)), Seg((X0, S2), (X1, S2)), Seg((X1, S1), (X2, S1)), Seg((X1, S2), (X2, S2))]

def zig(xa, xb, n=6, lo=48.6, hi=52.0):
    pts = []
    for i in range(n + 1):
        pts.append((xa + (xb - xa) * i / n, hi if i % 2 == 0 else lo))
    return poly(*pts)
zigL = zig(32.0, 47.0); zigR = mirror(zigL)

sa = (37.45, 62.9 + 4.1)
string = [Seg(sa, (39.0, 87.5), (61.0, 87.5), (100 - sa[0], sa[1]))]

def red_parts(side):
    if side == 'L':
        top = [Seg((X0, S1), (X0, YS))] + arch1 + [Seg((X1, YS), (X1, S1)), Seg((X1, S1), (X0, S1))]
        th = thumbL + [Seg((X0, TA), (X0, TB))]
        strip = poly((X0, S2), (X1, S2), (X1, YB), (X0, YB), closed=True)
    else:
        top = [Seg((X1, S1), (X1, YS))] + arch2 + [Seg((X2, YS), (X2, S1)), Seg((X2, S1), (X1, S1))]
        th = thumbR + [Seg((X2, TA), (X2, TB))]
        strip = poly((X1, S2), (X2, S2), (X2, YB), (X1, YB), closed=True)
    return [fill(FILL['red'], *top), fill(FILL['red'], *th), fill(FILL['red'], *strip)]

steps = [
    step('Start with an m', 'Draw a small letter m: a short straight line down, then two arches side by side. Each arch comes straight down to the bottom.',
         [line(stick0), line(*arch1, stick1), line(*arch2, stick2)]),
    step('The bottoms', 'Draw a straight line along the bottom, from the first line of the m to the last. Now you have two mittens.',
         [line(bottom)]),
    step('The thumbs', 'Draw a thumb on the outside of each mitten. It sticks out and points up.',
         [line(*thumbL), line(*thumbR)]),
    step('Fluffy cuffs', 'Draw a fluffy cuff under each mitten: three round bumps, like a little cloud. Leave a small gap between the two cuffs.',
         [line(*cuffL), line(*cuffR_fwd)]),
    step('A stripe', 'Draw two lines across each mitten, low down. They make a stripe on each one.',
         [line(s) for s in stripes]),
]
if ZIG:
    steps.append(step('A zigzag', 'Draw a zigzag line inside each stripe.', [line(*zigL), line(*zigR)]))
steps += [
    step('The string', 'Draw a long string hanging down from one cuff and back up to the other. It keeps the two mittens together.',
         [line(*string)]),
    step('Colour red', 'Colour the mittens and the thumbs red, above and below the stripe. Leave the stripe and the fluffy cuffs white.',
         red_parts('L') + red_parts('R'), use='red'),
]

D = drawing('dx_mittens_m', 'm is for mittens', 1, 8, 'things', ['Letters', 'Around the house'],
            'A pair of red mittens with fluffy cuffs, joined by a string. The small letter m is hiding in them: its two arches are the tops of the mittens and its three lines are their sides.',
            steps, ['red'])
name = 'mittens' if ZIG else 'mittens-plain'
json.dump(D, open(os.path.join(OUT, name + '.json'), 'w'))
json.dump({'set': 'house-az', 'slot': 'm', 'kind': 'key', 'age_from': 4}, open(os.path.join(OUT, name + '.place.json'), 'w'))
print('%s: %d steps' % (name, len(steps)))
