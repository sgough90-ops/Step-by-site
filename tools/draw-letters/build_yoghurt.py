"""y is for Yoghurt (dx_yoghurt_y), Food and drink a to z, slot y (23 Nov 2026).
From his pick "yogurt 1" (19:31), design 1 "Like your photo" on the sheet y-yoghurt-like-photo (Claude's sketches,
after his ChatGPT card of a blue bowl of yoghurt with half a strawberry, two blueberries, a raspberry and mint).

A wide, shallow bowl of yoghurt seen from above the front, with a small pile of fruit and three mint leaves.
The y is the straight kind and it is the three middle lines of the leaves: the long line runs down the middle of the
top right leaf and on down the leaf that lies on the fruit; the short line is the middle of the top left leaf.
Each leaf starts a little way along its line (a short stalk), so only the y's own three lines meet at its join.
The sprig is in front of everything, so nothing covers the y. The rim and the yoghurt stay white (plain paper).
Written in the sketch's numbers.

    python3 build_yoghurt.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=-4.0)
SX, SY = 0.0, 2.0                                                      # where the sprig sits on the sketch
A, B, M, C = (41 + SX, 25 + SY), (63 + SX, 25 + SY), (52 + SX, 40 + SY), (41 + SX, 55 + SY)   # the y: A to M, and B through M to C
STALK, LEAFW = 2.8, 8.0                                                # how far along its line a leaf starts, how wide it is
OUT, INN = (50, 50, 46, 17), (50, 50.6, 42, 13.4)                      # the bowl's rim: outside edge and inside edge
SC, SS, SD = (32.5, 50.0), 11.5, -20                                   # the half strawberry: middle, size, lean
BLUE1, BLUE2 = (57.0, 55.5, 6.0), (67.5, 53.0, 5.6)                    # the blueberries (the first is in front)
RASP = (79.5, 46.5, 6.2)                                               # the raspberry


def along(a, b, d):
    L = math.dist(a, b)
    return (a[0] + (b[0] - a[0]) * d / L, a[1] + (b[1] - a[1]) * d / L)


def leaf(name, tip, w, step):
    """a mint leaf round one line of the y: it starts a little way along the line and ends at the line's end"""
    (bx, by), (tx, ty) = along(M, tip, STALK), tip
    dx, dy = tx - bx, ty - by; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L; h = w * 0.67
    at = lambda t, s: (bx + dx * t + nx * s, by + dy * t + ny * s)
    e1 = Seg((bx, by), at(0.18, h), at(0.68, h), tip); e2 = Seg((bx, by), at(0.18, -h), at(0.68, -h), tip)
    p.region(name + 'R', [e1], rev([e2]))
    p.stroke(name + '1', e1, step=step); p.stroke(name + '2', e2, step=step)


def rot(pt, c, deg):
    a = math.radians(deg); x, y = pt[0] - c[0], pt[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


HEART = [(0, -1), (0.62, -0.92), (0.95, -0.4), (0.8, 0.3), (0.38, 0.86), (0, 1.05), (-0.38, 0.86), (-0.8, 0.3), (-0.95, -0.4), (-0.62, -0.92)]


def berry_shape(kx, ky, oy):
    return smooth([rot((SC[0] + x * SS * kx, SC[1] + y * SS * ky + SS * oy), SC, SD) for x, y in HEART], closed=True)


def flat_star(c, r_out, r_in, squash, deg):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(-90 + deg + 36 * i)
        pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a) * squash))
    return poly(*pts, closed=True)


def bumpy(cx, cy, r, k=8, amp=0.1, turn=10):
    pts = []
    for i in range(2 * k):
        rr = r * (1 + amp) if i % 2 == 0 else r * (1 - amp)
        a = math.radians(turn + 180.0 * i / k)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return smooth(pts, closed=True)


# ---- the bowl (at the back) ----
p.shape('rim', ell(*OUT), step=6)
p.stroke('bowl', one("M4,50 C2.6,62 18,83 50,83 C82,83 97.4,62 96,50"), step=7)   # it leaves the rim leaning out a little, so it does not run along the oval
p.shape('inner', ell(*INN), step=6)

# ---- the fruit ----
p.shape('straw', berry_shape(1.0, 1.0, 0.0), step=3)
p.shape('straw_in', berry_shape(0.56, 0.56, 0.08), step=3)
p.shape('calyx', flat_star(rot((SC[0], SC[1] - SS * 0.95), SC, SD), SS * 0.42, SS * 0.18, 0.62, SD), step=3)
p.shape('rasp', bumpy(*RASP), step=5)
for i in range(7):
    a = math.radians(20 + 60 * i)
    c = (RASP[0], RASP[1]) if i == 6 else (RASP[0] + RASP[2] * 0.54 * math.cos(a), RASP[1] + RASP[2] * 0.54 * math.sin(a))
    p.stroke('ring%d' % i, circle(c[0], c[1], RASP[2] * 0.2), step=5, deco=True, w=1.2)
p.shape('blue2', circle(*BLUE2), step=4)
p.shape('blue1', circle(*BLUE1), step=4)
for k, (cx, cy, r) in enumerate((BLUE1, BLUE2)):
    p.stroke('star%d' % k, star5(cx + r * 0.2, cy - r * 0.2, r * 0.4, 0.43), step=4, deco=True, w=1.2)

# ---- the mint, in front of everything; then the y itself ----
leaf('lc', C, LEAFW * 0.92, 2)
leaf('la', A, LEAFW, 2)
leaf('lb', B, LEAFW, 2)
p.stroke('y_long', Seg(B, C), step=1)
p.stroke('y_short', Seg(A, M), step=1)
p.build()

n = lambda a, b, t, s: (a[0] + (b[0] - a[0]) * t - (b[1] - a[1]) / math.dist(a, b) * s, a[1] + (b[1] - a[1]) * t + (b[0] - a[0]) / math.dist(a, b) * s)
green = [p.face('green', n(M, tip, 0.6, sg * 1.6)) for tip in (A, B, C) for sg in (-1, 1)]
green.append(p.ring('green', 'calyx'))

steps = [
    step('Start with a y', 'Draw a small letter y: a short line sloping down to the right, then a long line from the top right, down past its end.', p.step(1)),
    step('Three leaves', 'Draw a leaf round each of the three ends of the y. Each line of the y is the line down the middle of a leaf.', p.step(2)),
    step('Half a strawberry', 'Behind the bottom leaf draw half a strawberry: a fat heart shape. Draw a smaller one inside it and a spiky star on its top.', p.step(3)),
    step('Two blueberries', 'On the other side of the leaf draw two round blueberries. Draw a tiny star on each one.', p.step(4)),
    step('A raspberry', 'Next to them draw a raspberry: a round shape with a bumpy edge. Draw little rings all over it.', p.step(5)),
    step('The top of the bowl', 'Draw a long flat oval round all the fruit. It goes behind the two top leaves. Draw another oval just inside it.', p.step(6)),
    step('The bowl', 'From one end of the big oval, draw a deep curve down and round to the other end. The fruit is in a bowl of yoghurt!', p.step(7)),
    step('Colour yellow', 'Colour the bowl yellow, under the ovals.', [p.face('yellow', (50, 76))], use='yellow'),
    step('Colour blue', 'Colour the two blueberries blue.', [p.ring('blue', 'blue1'), p.face('blue', (BLUE2[0] + 2, BLUE2[1] + 2))], use='blue'),
    step('Colour red', 'Colour the strawberry red, all round its middle.', [p.face('red', (SC[0] - 8.6, SC[1] + 1), holes=['straw_in'])], use='red'),
    step('Colour pink', 'Colour the middle of the strawberry pink. Colour the raspberry pink too.',
         [p.ring('pink', 'straw_in'), p.ring('pink', 'rasp')], use='pink'),
    step('Colour green', 'Colour the three mint leaves green. Colour the star on the strawberry green. The yoghurt stays white.', green, use='green'),
]
D = drawing('dx_yoghurt_y', 'y is for Yoghurt', 3, 15, 'things', ['Letters', 'Around the house'],
            'A bowl of yoghurt with fruit and a sprig of mint. The small letter y is hiding in the mint: it is the lines down the middle of the three leaves.',
            steps, ['yellow', 'blue', 'red', 'pink', 'green'])
ok = finish('yoghurt', D, {'set': 'house-az', 'slot': 'y', 'kind': 'key', 'age_from': 5}, p)
