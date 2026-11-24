"""y is for yellow motorbike (dx_yellowmotorbike_y), Vehicles a to z, slot y (24 Nov 2026).
His pick (07:09): number 1, "Smaller y", on the second sketch sheet (y-yellow-motorbike-round2.png, 24 Nov).

A sports motorbike facing left. Under the seat there is a black panel with a pointed bottom. The y is the panel's
two bottom edges; its long line carries straight on down as the back edge of the yellow bodywork, and stops where the
yellow meets the black part underneath. Behind the long line is the grey frame. Only the y's own lines meet at its join.
Things in front are drawn in earlier steps, so nothing ever has to be rubbed out: the frame before the exhaust, the
exhaust before the back wheel, the bodywork before the windscreen and the fork. Written in the sketch's numbers.

    python3 build_yellowmotorbike.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=-8.0)
S, T, J, B = (52, 50), (68, 50), (60, 60), (52, 70)        # the y: short arm S to J, long line T through J to B
TR = (77, 53.6)                                            # where the frame meets the underside of the tail
F, R, TYRE, RIM = (19.5, 74.4), (80.5, 74.4), 13.6, 7.5


def sausage(a, b, w):
    """a bar with round ends from a to b, w wide, as a closed chain of pieces"""
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); r = w / 2
    nx, ny = -dy / L * r, dx / L * r
    ang = math.degrees(math.atan2(ny, nx))
    a1, b1, b2, a2 = P(a[0] + nx, a[1] + ny), P(b[0] + nx, b[1] + ny), P(b[0] - nx, b[1] - ny), P(a[0] - nx, a[1] - ny)
    return ([Seg(a1, b1)] + arc(b[0], b[1], r, r, ang, ang - 180, start=b1, end=b2)
            + [Seg(b2, a2)] + arc(a[0], a[1], r, r, ang - 180, ang - 360, start=a2, end=a1))


# ---- front wheel: the fork is behind it, the mudguard sits over its top ----
fx, fy = 9.7 / 27.56, -25.8 / 27.56                        # the way the fork leans
for nm, sg in (('fork_a', 1), ('fork_b', -1)):
    ox, oy = -fy * 1.6 * sg, fx * 1.6 * sg
    p.stroke(nm, Seg((F[0] + ox, F[1] + oy), (29.2 + ox, 48.6 + oy)), step=9)
p.shape('tyre_f', circle(F[0], F[1], TYRE), step=9)
p.shape('rim_f', circle(F[0], F[1], RIM), step=9)
go, gi = arc(F[0], F[1], 16.4, 16.4, 208, 316), arc(F[0], F[1], 12.2, 12.2, 316, 208)
p.shape('guard', go + [Seg(go[-1].b, gi[0].a)] + gi + [Seg(gi[-1].b, go[0].a)], step=9)

# ---- back wheel, with the exhaust in front of it ----
p.shape('tyre_r', circle(R[0], R[1], TYRE), step=8)
p.shape('rim_r', circle(R[0], R[1], RIM), step=8)
p.shape('pipe', sausage((64.5, 69), (90, 55), 5), step=8)

# ---- the frame: behind the y's long line ----
p.region('frameR', poly(T, B, (51, 77.4), (61, 78.4), (66.5, 68), TR, closed=True))
p.stroke('frame', poly(B, (51, 77.4), (61, 78.4), (66.5, 68), TR), step=4)

# ---- the tail, and the line across its tip for the light ----
TAIL = "M68,45.2 C76,43.6 86,41 94,38.6 L95,41.8 L77,53.6 L68,50"
p.region('tailR', one(TAIL + " Z"))
p.stroke('tail', one(TAIL), step=3)
p.stroke('light', Seg((92, 38), (93.3, 44)), step=3)

# ---- windscreen and handlebar: the bodywork hides their bottoms ----
p.shape('screen', one("M17.5,42.6 C19.5,35 25,30.6 31.5,30.2 L36,37.5 L19,43.5 Z"), step=7)
p.shape('bar', sausage((38.2, 36.6), (42.8, 32.4), 2.2), step=7)

# ---- the yellow bodywork: side panel, nose (held up clear of the front wheel) and tank. Its back edge is the y ----
BODY = ("M52,70 L37.2,70 C37,66.6 36.4,62 35,57.6 C33.8,53.4 31.4,50 27.5,50.2 L19,50.8 C15.6,50.8 13.2,49.4 13.4,46.4 "
        "C13.8,43.4 17,41.2 21,40.2 L34.5,37.2 C38.5,34.8 46.5,35 50.2,39.4 L52,44.6")
p.region('bodyR', one(BODY + " L52,50 L60,60 Z"))
p.stroke('body', one(BODY), step=5)
p.stroke('belly', one("M37.2,70 C37.3,73 38,75.6 39.6,77.4 L51,77.4"), step=6)

# ---- the seat, and the line across the top of the y that closes the black panel ----
p.stroke('seat', one("M52,50 L52,44.6 Q60,47.6 68,45.2 L68,50"), step=2)
p.stroke('panel', Seg(S, T), step=2)
p.shape('lamp', one("M15.6,45.4 L21.6,43.2 Q22.6,45.2 22.2,47.2 L16.6,49 Q15.2,47.6 15.6,45.4 Z"), step=7)

# ---- the y, in front of everything ----
p.stroke('y_short', Seg(S, J), step=1)
p.stroke('y_long', Seg(T, B), step=1)
p.build()
p.net.keep_in('light', 'tailR')

steps = [
    step('Start with a y', 'Draw a small letter y: a short line sloping down to the right, then a long line sloping down to the left that passes its end.', p.step(1)),
    step('The seat', 'Join the two tops of the y with a line. Draw the seat on top of it: up a little, across with a dip, and down again.', p.step(2)),
    step('The tail', 'From the back of the seat draw a tail that rises to the right. Come back under it to the top of the y. Draw a line across its tip for the light.', p.step(3)),
    step('The frame', 'From the bottom of the y go down, along to the right, then up in two slopes to meet the underside of the tail.', p.step(4)),
    step('The bodywork', 'From the bottom of the y go left, up and round a small nose. Come back along the top, over a round tank, and down to the front of the seat.', p.step(5)),
    step('Underneath', 'Draw the part underneath: curve down from the front corner of the bodywork, then go along to the bottom corner of the frame.', p.step(6)),
    step('Screen, light and handlebar', 'Draw a curved windscreen on top of the nose, a headlight on the side of the nose and a short handlebar on the tank.', p.step(7)),
    step('Exhaust and back wheel', 'Draw a long exhaust sloping up from the frame. Behind it draw a big circle for the back wheel, with a smaller circle inside.', p.step(8)),
    step('Front wheel', 'Draw the front wheel the same size. Draw a curved mudguard over its top, and two lines up from the mudguard to the nose.', p.step(9)),
    step('Colour yellow', 'Colour the bodywork, the tail and the mudguard yellow.',
         [p.face('yellow', (44, 52)), p.face('yellow', (80, 47)), p.ring('yellow', 'guard')], use='yellow'),
    step('Colour black', 'Colour the seat, the panel in the top of the y, the part underneath, the two tyres and the handlebar black.',
         [p.face('black', (60, 48.5)), p.face('black', (60, 54)), p.face('black', (45, 74)), p.face('black', (19.5, 85), holes=['rim_f']),
          p.face('black', (80.5, 85.5), holes=['rim_r']), p.face('black', (42.2, 33))], use='black'),
    step('Colour grey', 'Colour the frame, the exhaust, the middle of each wheel and the fork grey.',
         [p.face('grey', (57, 72)), p.face('grey', (80, 60.5)), p.ring('grey', 'rim_f'), p.ring('grey', 'rim_r'), p.face('grey', (26.54, 55.68))], use='grey'),
    step('Colour light blue', 'Colour the windscreen light blue.', [p.face('lblue', (26, 34))], use='lblue'),
    step('Colour red', 'Colour the light at the end of the tail red.', [p.face('red', (93.7, 41))], use='red'),
]
D = drawing('dx_yellowmotorbike_y', 'y is for yellow motorbike', 3, 20, 'vehicles', ['Letters', 'Vehicles'],
            'A fast yellow motorbike. The small letter y is hiding under the seat: the black panel and the back edge of the yellow bodywork.',
            steps, ['yellow', 'black', 'grey', 'lblue', 'red'])
ok = finish('yellowmotorbike', D, {'set': 'vehicles-az', 'slot': 'y', 'kind': 'drive', 'age_from': 5}, p)
