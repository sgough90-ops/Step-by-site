"""U is for UFO (Vehicles A to Z, slot U).
The U: the round bottom half of the spaceship. The wide ring sits across its two tops and the three legs
start on its curve: nothing crosses the U. (The little alien in the dome is an extra.)"""
import json, math, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

UX0, UX1, UT = 32.0, 68.0, 44.0
UC = (50.0, 62.0); UR = 18.0

def up(a): return on(UC[0], UC[1], UR, UR, a)

# ---- 1: the U (its curve is in pieces, so the legs and colours can use the same pieces) ----
LA = [180, 141, 127, 97, 83, 53, 39, 0]            # where the three legs join the curve
upts = [P(UX0, UC[1])] + [up(a) for a in LA[1:-1]] + [P(UX1, UC[1])]
ucurve = [arc_to(UC[0], UC[1], UR, UR, upts[i], upts[i + 1], False) for i in range(7)]
U_ = [Seg((UX0, UT), (UX0, UC[1]))] + [s for piece in ucurve for s in piece] + [Seg((UX1, UC[1]), (UX1, UT))]

# ---- 2: the ring ----
RT, RB = 34.0, 44.0
ring_ = rrect(14.0, RT, 86.0, RB, 5.0)

# ---- 3: the dome ----
DX0, DX1 = 33.0, 67.0
dome = arc(50.0, RT, 17.0, 19.0, 180, 360, start=P(DX0, RT), end=P(DX1, RT))

# ---- 4: the aerial ----
aer = Seg((50.0, 15.0), (50.0, 9.4))
ball = circle(50.0, 6.6, 2.8, start_deg=90)

# ---- 5: lights ----
lights = [circle(x, 39.0, 2.7) for x in (26.0, 50.0, 74.0)]
window = circle(50.0, 60.0, 7.0)

# ---- 6: three legs with feet ----
FY = 92.0; FRX, FRY = 6.0, 4.6
def foot(cx, a0, a1):
    """A foot (a little dome with a flat bottom); a0, a1 are where the two leg lines land on it."""
    L_, R_ = P(cx - FRX, FY), P(cx + FRX, FY)
    p0, p1 = on(cx, FY, FRX, FRY, a0), on(cx, FY, FRX, FRY, a1)
    top = [arc_to(cx, FY, FRX, FRY, L_, p0, True), arc_to(cx, FY, FRX, FRY, p0, p1, True), arc_to(cx, FY, FRX, FRY, p1, R_, True)]
    return top, Seg(R_, L_), p0, p1
feet = [foot(22.0, 248, 292), foot(50.0, 250, 290), foot(78.0, 248, 292)]
# leg lines: (point on the U, point on the foot); for each leg the outer line first
legs = []
for k, (fi, ia, ib) in enumerate(((0, 1, 2), (1, 3, 4), (2, 5, 6))):
    top, base, p0, p1 = feet[fi]
    if k == 2:      # the right leg: its left line starts nearer the middle of the U
        legs.append((Seg(upts[ia], p0), Seg(upts[ib], p1), ucurve[ia], top[1]))
    else:
        legs.append((Seg(upts[ia], p0), Seg(upts[ib], p1), ucurve[ia], top[1]))

# ---- 7: a little alien in the dome ----
AX0, AX1 = 41.5, 58.5
alien = arc(50.0, RT, 8.5, 12.5, 180, 360, start=P(AX0, RT), end=P(AX1, RT))
eyes = [dot(46.6, 28.6, w=4.4), dot(53.4, 28.6, w=4.4)]
smile = Seg((47.6, 31.2), (48.8, 32.6), (51.2, 32.6), (52.4, 31.2))

def leg_fill(lg):
    a, b, upiece, fpiece = lg
    return [a] + fpiece + [b.rev()] + rev(upiece)

steps = [
    step('Start with a U', 'Draw a big capital U: straight down, round the bottom and straight back up. This U is hiding in the spaceship.',
         [line(*U_)]),
    step('The ring', 'Draw a long bar with round ends across the top of the U. It sticks out a long way on both sides.',
         [ring(*ring_)]),
    step('The dome', 'Draw a tall round dome on top of the bar.',
         [line(*dome)]),
    step('The aerial', 'Draw a short line on top of the dome, with a little ball on the end.',
         [line(aer), ring(*ball)]),
    step('The lights', 'Draw three round lights in a row on the bar. Draw one big round light on the U.',
         [ring(*c) for c in lights] + [ring(*window)]),
    step('Three legs', 'Draw three legs under the U: two lines each. The outside ones slope out. Give each leg a round foot with a flat bottom.',
         [it for lg in legs for it in (line(lg[0]), line(lg[1]))] +
         [line(*([s for piece in f[0] for s in piece] + [f[1]])) for f in feet]),
    step('An alien', 'Draw a little alien looking out of the dome: a round head, two dots for eyes and a smile.',
         [line(*alien)] + eyes + [line(smile)]),
    step('Colour grey', 'Colour the U, the bar, the legs and the feet grey. Go round all the lights.',
         [fill(FILL['grey'], *(U_ + [Seg((UX1, UT), (UX0, UT))]), cut=[d_fill(*window)]),
          fill(FILL['grey'], *ring_, cut=[d_fill(*c) for c in lights])] +
         [fill(FILL['grey'], *leg_fill(lg)) for lg in legs] +
         [fill(FILL['grey'], *([s for piece in f[0] for s in piece] + [f[1]])) for f in feet], use='grey'),
    step('Colour the dome', 'Colour the dome light blue, round the alien.',
         [fill(FILL['lblue'], *(dome + [Seg((DX1, RT), (AX1, RT))] + rev(alien) + [Seg((AX0, RT), (DX0, RT))]))], use='lblue'),
    step('Colour yellow', 'Colour all four lights yellow.',
         [fill(FILL['yellow'], *c) for c in lights] + [fill(FILL['yellow'], *window)], use='yellow'),
    step('Colour the alien', 'Colour the alien green.',
         [fill(FILL['green'], *(alien + [Seg((AX1, RT), (AX0, RT))]))], use='green'),
    step('Colour red', 'Colour the little ball on the aerial red.',
         [fill(FILL['red'], *ball)], use='red'),
]

D = drawing('dx_ufo_u', 'U is for UFO', 2, 12, 'vehicles', ['Letters', 'Vehicles'],
            'A flying saucer with a glass dome, lights and three legs, and a little alien looking out. The capital U is hiding in it: the U is the round bottom of the spaceship.',
            steps, ['grey', 'lblue', 'yellow', 'green', 'red'])
json.dump(D, open(os.path.join(OUT, 'ufo.json'), 'w'))
json.dump({'set': 'vehicles-AZ', 'slot': 'U', 'kind': 'fly', 'age_from': 4}, open(os.path.join(OUT, 'ufo.place.json'), 'w'))
print('ufo: %d steps' % len(steps))
