"""X is for X-15 rocket plane (dx_x15_x), Vehicles A to Z, slot X (24 Nov 2026).
His pick (06:49): number 2, "From above", on the sheet X-x-15 (Claude's sketches, after his ask for the X-15).

The X-15 was a real rocket plane of the 1960s: a long black dart with stubby wings, small tail wings and a rocket.
Here it is seen from above, flying up to the right. On a solid plane two edges never truly cross, so the X is the
plane's back corner, where four real edges meet: one line is the back edge of the near tail wing carrying straight on
as the end of the body; the other is the side of the body carrying straight on as the side of the fire.
Step 1 draws that X. The body's side and the far tail wing's back edge are then carried on from its ends.

The fire leans a little: on the far side its edge turns in at the corner, so the same corner over there is not a
second X. No marks, flags or wording: it is the shape of the plane only.
Written along the plane: u runs up the body from its back end, v runs across it (v under 0 is the near, left side).

    python3 build_x15.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=0.0)
K = math.sqrt(0.5) * 1.12
M = lambda u, v: (27 + (u + v) * K, 71 + (-u + v) * K)          # from along and across the plane to the paper
HW, ARM, TAIL = 5.0, 10.5, 15.5                                 # half the body's width; an arm of the X; the tail wing's tip

# ---- the body: from the top right end of the X, up to the nose and back down to the bottom right end of the X ----
p.stroke('body', Seg(M(ARM, -HW), M(50, -HW)), Seg(M(50, -HW), M(60, -HW), M(66, -2.6), M(70, 0)),
         Seg(M(70, 0), M(66, 2.6), M(60, HW), M(50, HW)), Seg(M(50, HW), M(0, HW)), step=2)
# ---- the fire: from the bottom left end of the X round to a point and back to the bottom right end; it leans, see above ----
p.stroke('fire', Seg(M(-ARM, -HW), M(-16, -HW), M(-21, -4.4), M(-24.5, -2)), Seg(M(-24.5, -2), M(-17, -0.2), M(-4.5, 1.6), M(0, HW)), step=3)
# ---- tail wings: the near one starts at the top left end of the X; the far one carries the X's line on ----
p.stroke('tail_n', poly(M(0, -TAIL), M(4.2, -TAIL), M(13, -HW)), step=4)
p.stroke('tail_f', poly(M(0, HW), M(0, TAIL), M(4.2, TAIL), M(13, HW)), step=4)
# ---- wings ----
for nm, sg in (('wing_n', -1), ('wing_f', 1)):
    p.stroke(nm, poly(M(40, HW * sg), M(31.5, 17 * sg), M(26.2, 17 * sg), M(27, HW * sg)), step=5)
# ---- window, band, tail fin (seen from above it is a long thin triangle) ----
p.shape('window', smooth([M(57 + 1.7 * math.cos(math.radians(a)), 3.1 * math.sin(math.radians(a))) for a in range(0, 360, 45)], closed=True), step=6)
p.stroke('band_a', Seg(M(44, -HW), M(44, HW)), step=6); p.stroke('band_b', Seg(M(48, -HW), M(48, HW)), step=6)
p.shape('fin', poly(M(24, 0), M(4, 2.3), M(4, -2.3), closed=True), step=6)
# ---- clouds ----
p.shape('cloud1', cloud(14, 33, 0.95), step=7)
p.shape('cloud2', cloud(60, 87, 0.95), step=7)
# ---- the X ----
p.stroke('x1', Seg(M(0, -TAIL), M(0, HW)), step=1)
p.stroke('x2', Seg(M(ARM, -HW), M(-ARM, -HW)), step=1)
p.build()

steps = [
    step('Start with an X', 'Draw a capital X: a line sloping down to the right, then a line sloping down to the left across it.', p.step(1)),
    step('The body', 'From the top right end of the X, draw a long line up to a pointed nose. Come back down the other side to the bottom right end of the X.', p.step(2)),
    step('The fire', 'From the bottom left end of the X, curve round to a point. Then curve back up to the bottom right end of the X.', p.step(3)),
    step('Tail wings', 'At the top left end of the X draw a short edge, then slope back to the body. Draw the same little wing on the other side of the body.', p.step(4)),
    step('Wings', 'Half way up the body draw a wing on each side: a sloping front, a short tip and a straight back.', p.step(5)),
    step('Window, band and fin', 'Draw an oval window near the nose. Draw two lines across the body for a band. Draw a long thin triangle near the back: the tail fin.', p.step(6)),
    step('Clouds', 'Draw two fluffy clouds in the sky.', p.step(7)),
    step('Colour black', 'Colour the body black, on both sides of the band. The band stays white.',
         [p.face('black', M(33, 0), holes=['fin']), p.face('black', M(64, 0), holes=['window'])], use='black'),
    step('Colour grey', 'Colour the two wings, the two tail wings and the tail fin grey.',
         [p.face('grey', M(32, -10)), p.face('grey', M(32, 10)), p.face('grey', M(4, -9)), p.face('grey', M(4, 9)), p.ring('grey', 'fin')], use='grey'),
    step('Colour orange', 'Colour the fire orange.', [p.face('orange', M(-8, -1.5))], use='orange'),
    step('Colour light blue', 'Colour the window light blue.', [p.ring('lblue', 'window')], use='lblue'),
]
D = drawing('dx_x15_x', 'X is for X-15 rocket plane', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'The X-15 was a real rocket plane, one of the fastest ever flown. The capital letter X is hiding at its back corner: where the tail wing, the body and the fire meet.',
            steps, ['black', 'grey', 'orange', 'lblue'])
ok = finish('x15', D, {'set': 'vehicles-AZ', 'slot': 'X', 'kind': 'fly', 'age_from': 5}, p)
