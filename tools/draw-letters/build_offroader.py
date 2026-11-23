"""o is for off-roader (dx_offroader_o), Vehicles a to z, slot o (23 Nov 2026).
From his pick "o4 Over the rocks" (Claude's second-go sketches, claude/step-by-draw-food-capitals-vehicles-small-14x4.md).

An open-top off-road truck climbing over rocks, facing left. Its back wheel is behind a big rock, so there is only one
round wheel to see: the o is that front wheel. The truck is written facing right and level (the sketch's numbers);
F() turns it to face left and tips its nose up by 7 degrees.

    python3 build_offroader.py
"""
from bcommon import *

p = Pic(s=0.96, dx=2.0, dy=-7.0)
OX, OY, DEG = 105.9, 7.7, 7
C7, S7 = math.cos(math.radians(DEG)), math.sin(math.radians(DEG))


def tf(q):
    """where a point of the level, right-facing truck lands on the page"""
    x, y = -q[0], q[1]
    return (OX + x * C7 - y * S7, OY + x * S7 + y * C7)


def F(*segs):
    return [Seg(*[tf(q) for q in s.p]) for s in flat(segs)]


def stick(a, b, w):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); r = w / 2; th = math.degrees(math.atan2(dy, dx))
    nx, ny = -dy / L * r, dx / L * r
    p1, p2, p3, p4 = P(a[0] + nx, a[1] + ny), P(b[0] + nx, b[1] + ny), P(b[0] - nx, b[1] - ny), P(a[0] - nx, a[1] - ny)
    return [Seg(p1, p2)] + arc(b[0], b[1], r, r, th + 90, th - 90, start=p2, end=p3) + [Seg(p3, p4)] + arc(a[0], a[1], r, r, th - 90, th - 270, start=p4, end=p1)


def lam(A, T, B, w):
    """a roll bar: one shape like an upside-down V, from foot A up to the top T and down to foot B, w thick"""
    r = w / 2

    def unit(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy)
        return dx / L, dy / L
    d1, d2 = unit(A, T), unit(T, B)
    n1, n2 = (d1[1], -d1[0]), (d2[1], -d2[0])                  # the outside of each leg
    Ao, To1, To2, Bo = (A[0] + n1[0] * r, A[1] + n1[1] * r), (T[0] + n1[0] * r, T[1] + n1[1] * r), (T[0] + n2[0] * r, T[1] + n2[1] * r), (B[0] + n2[0] * r, B[1] + n2[1] * r)
    Ai, Bi = (A[0] - n1[0] * r, A[1] - n1[1] * r), (B[0] - n2[0] * r, B[1] - n2[1] * r)
    den = d1[0] * (-d2[1]) - d1[1] * (-d2[0])                  # where the two inside edges meet
    a = ((Bi[0] - Ai[0]) * (-d2[1]) - (Bi[1] - Ai[1]) * (-d2[0])) / den
    K = (Ai[0] + d1[0] * a, Ai[1] + d1[1] * a)
    a1, a2 = math.degrees(math.atan2(n1[1], n1[0])) % 360, math.degrees(math.atan2(n2[1], n2[0])) % 360
    if a2 < a1: a2 += 360
    return ([Seg(Ao, To1)] + arc(T[0], T[1], r, r, a1, a2, start=P(*To1), end=P(*To2)) + [Seg(To2, Bo), Seg(Bo, Bi), Seg(Bi, K), Seg(K, Ai), Seg(Ai, Ao)])


WX, WY, WR = 75, 75, 12.8                                      # the front wheel (the o), in the truck's own numbers
TOPY = lambda x: 44 + (x - 57) / (86 - 57) * 1.6               # the top edge of the bonnet

# ---- behind the body: seat, roll bar, windscreen, spare wheel ----
p.shape('seat', F(rrect(34, 31, 41.4, 59, 3)), step=4)
p.shape('bar', F(lam((21, 47), (24.4, 25.4), (32.5, 58), 3.4)), step=4)
p.shape('screen', F(poly((55.6, 45.4), (59.4, 45.4), (55.4, 24), (51.6, 24), closed=True)), step=4)
p.shape('spare', F(rrect(2.4, 42, 9, 59, 2.6)), step=4)
# ---- the body, with a scooped doorway; then the bar along the bottom ----
p.shape('body', F(one("M8,68 L8,47 Q8,44 11,44 L28,44 C32,44 32,55 37,55 L49,55 C54,55 53,44 57,44 L86,45.6 Q93,46.2 93,51 L93,68 Z")), step=3)
p.stroke('door', F(Seg((66, TOPY(66)), (66, 62.6))), step=5, deco=True)
p.shape('lamp', F(rrect(90.6, 49.6, 95.2, 55.6, 1.3)), step=5)
p.shape('sill', F(rrect(5.6, 62.6, 96.6, 70.6, 2.8)), step=3)
# ---- a little rock under the front wheel; then the wheel, which is the o ----
p.shape('rockS', poly((3, 93), (7, 85.5), (16, 83), (29, 83.6), (39, 87), (44, 93), closed=True), step=2)
OC = tf((WX, WY))
p.shape('o', circle(OC[0], OC[1], WR), step=1)
p.shape('hub', circle(OC[0], OC[1], 5), step=2)
# ---- the big rock in front of the back wheel ----
p.shape('rockB', poly((52, 93), (55, 77), (61, 65.4), (72, 59), (84, 61.4), (92, 71), (97, 93), closed=True), step=2)
p.stroke('facet0', poly((61, 65.4), (76, 70), (84, 61.4)), step=2, deco=True)
p.stroke('facet1', Seg((76, 70), (72, 93)), step=2, deco=True)
p.build()

sd = lambda x, y: tf((x, y))                                   # a colour's starting point, given in the truck's own numbers
steps = [
    step('Start with an o', 'Draw a small letter o: a big round circle. This o is hiding in the truck.', p.step(1)),
    step('Wheel and rocks', 'Draw a small circle in the middle of the o. Draw a low rock under it. Far over on the right draw a big rock with three lines on it.', p.step(2)),
    step('The truck', 'Draw a long thin bar from the big rock to the o, and its end on the other side of the o. Above it draw the truck, with a dip for the doorway.', p.step(3)),
    step('Seat, bars and glass', 'Draw a seat in the doorway and a bar like an upside-down V behind it. Draw a thin sloping windscreen in front, and a spare wheel on the back.', p.step(4)),
    step('Door and light', 'Draw a line down for the door. Draw a little light on the front of the truck.', p.step(5)),
    step('Colour orange', 'Colour the truck orange.', [p.face('orange', sd(76, 54))], use='orange'),
    step('Colour black', 'Colour the tyre black, round the small circle. Colour the seat, the bar and the spare wheel black too.',
         [p.ring('black', 'o', holes=('hub',)), p.face('black', sd(37.7, 38)), p.face('black', sd(22.8, 35.7)), p.face('black', sd(5, 50))], use='black'),
    step('Colour grey', 'Colour the middle of the wheel, the long bar and the two rocks grey.',
         [p.ring('grey', 'hub'), p.face('grey', sd(55, 66.6)), p.face('grey', sd(92.5, 66.6)), p.ring('grey', 'rockB'), p.face('grey', (22, 90))], use='grey'),
    step('Colour light blue', 'Colour the windscreen light blue.', [p.face('lblue', sd(55.5, 34))], use='lblue'),
    step('Colour yellow', 'Colour the little light yellow.', [p.ring('yellow', 'lamp')], use='yellow'),
]
D = drawing('dx_offroader_o', 'o is for off-roader', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'An open-top off-roader climbing over rocks. The small letter o is hiding in it: the big front wheel.',
            steps, ['orange', 'black', 'grey', 'lblue', 'yellow'])
ok = finish('offroader', D, {'set': 'vehicles-az', 'slot': 'o', 'kind': 'drive', 'age_from': 5}, p)
