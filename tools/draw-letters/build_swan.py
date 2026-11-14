"""s is for swan (Animals a to z, slot s). Side view, facing right.
The s: its top curl is the underside of the swan's arched neck, and its bottom curl is the breast and the tummy.
The head, the back of the neck, the back and the tail are added outside the s; the wing sits inside the body.
Nothing crosses the s."""
import json, math, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

C1 = (58.0, 30.0); R1 = 10.0            # the top curl of the s
C2 = (58.0, 61.0); R2 = 21.0            # the bottom curl
PC = (44.0, 81.0); PRX, PRY = 40.0, 8.5  # the pond

A = on(C1[0], C1[1], R1, R1, 315)       # where the s starts (the swan's chin)
J = P(C1[0], C1[1] + R1)                # where the two curls join
B = on(C2[0], C2[1], R2, R2, 115)       # where the s ends

def pond_f(p):
    return ((p[0] - PC[0]) / PRX) ** 2 + ((p[1] - PC[1]) / PRY) ** 2 - 1

# where the bottom curl of the s meets the pond
lo, hi = 20.0, 80.0
for _ in range(60):
    m = (lo + hi) / 2
    if pond_f((C2[0] + R2 * math.cos(math.radians(m)), C2[1] + R2 * math.sin(math.radians(m)))) > 0: lo = m
    else: hi = m
WR = on(C2[0], C2[1], R2, R2, lo)

# ---- 1: the s ----
s_top = arc_to(C1[0], C1[1], R1, R1, A, J, False)
s_low1 = arc_to(C2[0], C2[1], R2, R2, J, WR, True)
s_low2 = arc_to(C2[0], C2[1], R2, R2, WR, B, True)
S_ = s_top + s_low1 + s_low2

# ---- 2: the head and the back of the neck ----
M = ((A[0] + C1[0] + 19.5 * math.cos(math.radians(315))) / 2, (A[1] + C1[1] + 19.5 * math.sin(math.radians(315))) / 2)
HR_ = 4.75
HO = on(M[0], M[1], HR_, HR_, 315)
p2 = on(M[0], M[1], HR_, HR_, 70); p1 = on(M[0], M[1], HR_, HR_, 20)
cap = [arc_to(M[0], M[1], HR_, HR_, A, p2, False), arc_to(M[0], M[1], HR_, HR_, p2, p1, False), arc_to(M[0], M[1], HR_, HR_, p1, HO, False)]
NR = 17.5
over = [Seg(HO, (HO[0] - 3.5, HO[1] - 3.5), (C1[0] + 5.5, C1[1] - NR), (C1[0], C1[1] - NR))] + \
       arc(C1[0], C1[1], NR, NR, 270, 180, start=P(C1[0], C1[1] - NR), end=P(C1[0] - NR, C1[1]))
N = (38.0, 47.5)
down = [Seg((C1[0] - NR, C1[1]), (C1[0] - NR, 37.5), (41.5, 44.0), N)]
neck = cap[0] + cap[1] + cap[2] + over + down

# ---- 3: the beak ----
TIP = P(M[0] + 13.5 * math.cos(math.radians(45)), M[1] + 13.5 * math.sin(math.radians(45)))
beak = [Seg(p1, TIP), Seg(TIP, p2)]

# ---- 4: the eye ----
eye = dot(M[0] - 0.9, M[1] - 1.1, w=3.4)

# ---- 5: the back, the tail and the tummy ----
T = (8.0, 56.0)
back = Seg(N, (33.1, 52.4), (20.0, 47.0), T)
belly = Seg(B, (B[0] - 9.06, B[1] - 4.23), (13.0, 76.5), T)
lo, hi = 0.0, 1.0
for _ in range(60):
    m = (lo + hi) / 2
    if pond_f(belly.at(m)) < 0: lo = m
    else: hi = m
tL = lo
belly_a, belly_b = belly.split(tL)       # B..WL (in the water) and WL..T
WL = belly_a.b

# ---- 6: the wing ----
wing = [Seg((56.0, 55.0), (48.0, 48.5), (32.0, 50.0), (19.0, 58.5)),
        Seg((19.0, 58.5), (22.0, 64.0), (28.0, 65.5), (31.0, 63.5)),
        Seg((31.0, 63.5), (33.0, 68.5), (39.0, 69.5), (42.0, 67.0)),
        Seg((42.0, 67.0), (46.0, 70.0), (54.0, 66.0), (56.0, 55.0))]

# ---- 7: the water ----
water = arc_to(PC[0], PC[1], PRX, PRY, WR, WL, True)

steps = [
    step('Start with an s', 'Draw a letter s with a small curl at the top and a big curl at the bottom. This s is hiding in the swan.',
         [line(*S_)]),
    step('Head and neck', 'Start at the top end of the s. Draw a round head, then follow the s over the top and down its side. Carry on down and curve away.',
         [line(*neck)]),
    step('The beak', 'Draw a pointed beak on the head, pointing down.',
         [line(*beak)]),
    step('The eye', 'Draw a dot on the head for the eye.',
         [eye]),
    step('Back and tail', 'From the bottom of the neck, draw the back along to a pointed tail. Then curve back under to the bottom end of the s.',
         [line(back, belly_b.rev(), belly_a.rev())]),
    step('The wing', 'Draw a big wing on the body: a long curve along the top, then three round feathers along the bottom.',
         [ring(*wing)]),
    step('The water', 'Draw a pond under the swan: start at its front, go round under it and come back up to its tail end.',
         [line(*water)]),
    step('Colour the beak', 'Colour the beak orange.',
         [fill(FILL['orange'], *(beak + cap[1]))], use='orange'),
    step('Colour the water', 'Colour the pond light blue. Leave the swan white.',
         [fill(FILL['lblue'], *(water + [belly_a.rev()] + rev(s_low2)))], use='lblue'),
]

D = drawing('dx_swan_s', 's is for swan', 2, 10, 'animals', ['Letters', 'Animals'],
            'A white swan gliding on a pond, with its neck curved over. The small letter s is hiding in it: its top curl is the underside of the neck and its bottom curl is the breast and tummy.',
            steps, ['orange', 'lblue'])
json.dump(D, open(os.path.join(OUT, 'swan.json'), 'w'))
json.dump({'set': 'animals-az', 'slot': 's', 'kind': 'swim', 'age_from': 5}, open(os.path.join(OUT, 'swan.place.json'), 'w'))
print('swan: %d steps' % len(steps))
