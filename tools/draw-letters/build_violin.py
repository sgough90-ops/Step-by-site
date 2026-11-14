"""V is for Violin (Around the house A to Z, slot V). Front view, standing up.
The V: the tailpiece, the pointed part that holds the bottom of the strings. It is a true V (two lines);
its top is closed later with a new line. The neck is drawn before the body so no line has to cross another."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

VT = 66.0
VL, VP, VR = (43.5, VT), (50.0, 84.0), (56.5, VT)

# ---- 1: the V ----
V_ = poly(VL, VP, VR)

# ---- 2: the neck (a long thin box) ----
NX0, NX1, NT, NB = 45.5, 54.5, 10.0, 50.0
neck = poly((NX0, NT), (NX1, NT), (NX1, NB), (NX0, NB), closed=True)

# ---- 3: the body (from one side of the neck round to the other) ----
BY = 30.0
half = [Seg((NX0, BY), (40.0, BY), (34.0, 33.0), (34.0, 41.0)),
        Seg((34.0, 41.0), (34.0, 46.5), (40.0, 49.5), (40.0, 54.5)),
        Seg((40.0, 54.5), (40.0, 59.0), (30.0, 62.0), (30.0, 73.0)),
        Seg((30.0, 73.0), (30.0, 85.0), (39.0, 93.0), (50.0, 93.0))]
body = half + rev(mirror(half))

# ---- 4: the top of the V, and the bridge ----
vtop = Seg(VL, VR)
BRT, BRB = 59.6, 62.4
bridge = rrect(43.6, BRT, 56.4, BRB, 1.2)

# ---- 5: the strings ----
SXS = (47.4, 50.0, 52.6)
str_up = [Seg((x, NB), (x, BRT)) for x in SXS]
str_dn = [Seg((x, BRB), (x, VT)) for x in SXS]

# ---- 6: the f-holes ----
fL = Seg((41.6, 58.0), (38.8, 61.0), (38.8, 65.6), (41.6, 68.6))
fR = mirror([fL])[0]

# ---- 7: the top of the neck and the pegs ----
dome = arc(50.0, NT, 3.2, 3.6, 180, 360, start=P(46.8, NT), end=P(53.2, NT))
def peg(y, side):
    x0 = NX0 if side < 0 else NX1
    x1 = x0 + side * 3.0; cx = x1 + side * 1.9
    return [line(Seg((x0, y), (x1, y))), ring(*circle(cx, y, 1.9, start_deg=0 if side < 0 else 180))], circle(cx, y, 1.9, start_deg=0 if side < 0 else 180)
pegs = [peg(14.0, -1), peg(19.6, -1), peg(14.0, 1), peg(19.6, 1)]

# ---- 8: the chin rest ----
rest = circle(38.4, 80.2, 4.4, ry=3.2)

steps = [
    step('Start with a V', 'Draw a capital V near the bottom of your paper: two straight lines that meet in a point. This V is hiding in the violin.',
         [line(*V_)]),
    step('The neck', 'Draw a long thin box above the V, going right up near the top of your paper. Leave a gap between the box and the V.',
         [ring(*neck)]),
    step('The body', 'Start at the side of the neck. Go out and round a small bump, in at the waist, round a big bump under the V and back up the other side.',
         [line(*body)]),
    step('The bridge', 'Draw a line across the top of the V to close it. Then draw a thin little box just above it.',
         [line(vtop), ring(*bridge)]),
    step('The strings', 'Draw three lines down from the neck to the little box. Then draw three short lines from the box down to the V.',
         [line(s) for s in str_up + str_dn]),
    step('The sound holes', 'Draw a curved line on each side of the strings, like a pair of brackets.',
         [line(fL), line(fR)]),
    step('The pegs', 'Draw a little round top on the neck. Draw two pegs on each side of it: a short line with a small circle on the end.',
         [line(*dome)] + [it for pg, _ in pegs for it in pg]),
    step('The chin rest', 'Draw a flat oval near the bottom of the violin, on the left of the V.',
         [ring(*rest)]),
    step('Colour brown', 'Colour the body of the violin brown. Go round the V, the little box and the oval. Colour the round top of the neck too.',
         [fill(FILL['brown'], *(body + [Seg((NX1, BY), (NX1, NB)), Seg((NX1, NB), (NX0, NB)), Seg((NX0, NB), (NX0, BY))]),
               cut=[d_fill(*(V_ + [vtop.rev()])), d_fill(*bridge), d_fill(*rest)]),
          fill(FILL['brown'], *(dome + [Seg((53.2, NT), (46.8, NT))]))], use='brown'),
    step('Colour black', 'Colour the neck black. Colour the V, the oval and the four pegs black too.',
         [fill(FILL['black'], *neck), fill(FILL['black'], *(V_ + [vtop.rev()])), fill(FILL['black'], *rest)] +
         [fill(FILL['black'], *c) for _, c in pegs], use='black'),
    step('Colour the bridge', 'Colour the thin little box light brown.',
         [fill(FILL['lbrown'], *bridge)], use='lbrown'),
]

D = drawing('dx_violin_v', 'V is for Violin', 3, 15, 'things', ['Letters', 'Around the house'],
            'A violin with strings, pegs and a chin rest. The capital V is hiding in it: the V is the pointed part that holds the bottom of the strings.',
            steps, ['brown', 'black', 'lbrown'])
json.dump(D, open(os.path.join(OUT, 'violin.json'), 'w'))
json.dump({'set': 'house-AZ', 'slot': 'V', 'kind': 'key', 'age_from': 6}, open(os.path.join(OUT, 'violin.place.json'), 'w'))
print('violin: %d steps' % len(steps))
