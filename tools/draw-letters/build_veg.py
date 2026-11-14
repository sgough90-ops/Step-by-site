"""v is for vegetables (Around the house a to z, slot v). A carrot growing, with a tomato and some broccoli.
The v: the two sides of the carrot, down to its point. The soil starts at each side of the v and
never goes across it: nothing crosses the v."""
import json, math, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

VA, VP, VB = (38.0, 30.0), (50.0, 88.0), (62.0, 30.0)
# ---- 1: the v ----
V_ = poly(VA, VP, VB)

# ---- 2: the top of the carrot ----
top = Seg(VA, (40.0, 24.5), (60.0, 24.5), VB)

# ---- 3: the leaves (three fronds, each one a closed shape that starts and ends at one spot on the carrot) ----
fl = [Seg((0, 0), (-0.8, -3.0), (-1.4, -5.0), (-1.4, -7.5)),
      Seg((-1.4, -7.5), (-6.5, -6.5), (-7.0, -12.5), (-2.6, -12.8)),
      Seg((-2.6, -12.8), (-6.8, -13.6), (-6.0, -19.0), (-2.0, -18.2)),
      Seg((-2.0, -18.2), (-3.0, -22.0), (-0.6, -23.5), (0, -23.5))]
frond = fl + rev(mirror(fl, cx=0.0))
def leaf(t, deg, scale=1.0):
    b = top.at(t)
    return shift(rot(xf(frond, lambda x, y: (x * scale, y * scale)), deg), b[0], b[1])
leaves = [leaf(0.22, -40, 0.9), leaf(0.5, 0, 1.0), leaf(0.78, 40, 0.9)]

# ---- 4: lines on the carrot ----
marks = [Seg((43.5, 44.0), (49.0, 44.0)), Seg((50.5, 57.0), (54.5, 57.0))]

# ---- 5: the soil ----
SY = 76.0
CL = P(VA[0] + (VP[0] - VA[0]) * (SY - VA[1]) / (VP[1] - VA[1]), SY); CR = P(100 - CL[0], SY)
E0, E1 = (6.0, 80.0), (94.0, 80.0)
J1, J2, J3, J4 = (12.5, 76.0), (31.5, 76.0), (70.5, 77.0), (76.0, 77.0)
b0 = Seg(E0, (7.5, 76.5), (10.5, 75.0), J1)
b1 = Seg(J1, (17.0, 72.4), (27.0, 72.4), J2)
b2 = Seg(J2, (35.0, 72.2), (42.5, 72.6), CL)
b3 = Seg(CR, (57.0, 72.4), (65.0, 73.0), J3)
b4 = Seg(J3, (72.0, 75.4), (74.5, 75.4), J4)
b5 = Seg(J4, (81.0, 72.6), (90.0, 74.0), E1)
under = [Seg(E0, (6.0, 90.0), (22.0, 94.0), (50.0, 94.0)), Seg((50.0, 94.0), (78.0, 94.0), (94.0, 90.0), E1)]

# ---- 6: the tomato ----
TC = (22.0, 70.5); TR_ = math.dist(TC, J1)
tomato = arc_to(TC[0], TC[1], TR_, TR_, J1, J2, True)
def star(cx, cy, ro, ri, n=5):
    pts = []
    for k in range(2 * n):
        r = ro if k % 2 == 0 else ri; a = math.radians(-90 + 180 * k / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(*pts, closed=True)
calyx = star(22.0, 65.2, 4.6, 2.0)

# ---- 7: the broccoli ----
cs = [(65.5, 60.0, 5.5), (67.0, 51.5, 6.0), (73.5, 47.5, 6.5), (80.0, 51.5, 6.0), (81.5, 60.0, 5.5)]
sTL = on(cs[0][0], cs[0][1], cs[0][2], cs[0][2], 40); sTR = on(cs[4][0], cs[4][1], cs[4][2], cs[4][2], 140)
crown = cloud(cs, sTL, sTR, (73.5, 58.0))
crown_base = Seg(sTL, (71.5, 65.6), (75.5, 65.6), sTR)
stalkL = Seg(sTL, J3); stalkR = Seg(sTR, J4)

steps = [
    step('Start with a v', 'Draw a big letter v: two straight lines that meet in a point at the bottom. This v is hiding in the carrot.',
         [line(*V_)]),
    step('The top of the carrot', 'Join the two tops of the v with a curved line, like a little hill.',
         [line(top)]),
    step('The leaves', 'Draw three bumpy leaves growing out of the top of the carrot: one straight up and one leaning out each side.',
         [ring(*l) for l in leaves]),
    step('Lines on the carrot', 'Draw two short lines across the carrot.',
         [line(m) for m in marks]),
    step('The soil', 'Draw three bumps of soil on each side of the carrot, starting at the v. Then draw a big curve under it all.',
         [line(b2.rev(), b1.rev(), b0.rev()), line(b3, b4, b5), line(*under)]),
    step('A tomato', 'Draw a round tomato sitting behind the soil on the left. Draw a little star on it.',
         [line(*tomato), ring(*calyx)]),
    step('Some broccoli', 'On the right, draw a stalk coming up out of the soil. Draw a curved line across its top and a big bumpy cloud above it.',
         [line(stalkL), line(stalkR), line(crown_base), line(*crown)]),
    step('Colour the carrot', 'Colour the carrot orange, right down to the point.',
         [fill(FILL['orange'], *(V_ + [top.rev()]))], use='orange'),
    step('Colour green', 'Colour the three leaves, the star, and the broccoli and its stalk green.',
         [fill(FILL['green'], *l) for l in leaves] + [fill(FILL['green'], *calyx),
          fill(FILL['green'], *(crown + [crown_base.rev()])),
          fill(FILL['green'], *([stalkL, b4, stalkR.rev(), crown_base.rev()]))], use='green'),
    step('Colour the tomato', 'Colour the tomato red, round the star.',
         [fill(FILL['red'], *(tomato + [b1.rev()]), cut=[d_fill(*calyx)])], use='red'),
    step('Colour the soil', 'Colour the soil brown. Go round the point of the carrot.',
         [fill(FILL['brown'], *([b0, b1, b2, Seg(CL, VP), Seg(VP, CR), b3, b4, b5] + rev(under)))], use='brown'),
]

D = drawing('dx_vegetables_v', 'v is for vegetables', 3, 15, 'things', ['Letters', 'Around the house'],
            'A carrot growing in the soil, with a tomato and some broccoli beside it. The small letter v is hiding in it: the v is the two sides of the carrot.',
            steps, ['orange', 'green', 'red', 'brown'])
json.dump(D, open(os.path.join(OUT, 'veg.json'), 'w'))
json.dump({'set': 'house-az', 'slot': 'v', 'kind': 'key', 'age_from': 5}, open(os.path.join(OUT, 'veg.place.json'), 'w'))
print('veg: %d steps' % len(steps))
