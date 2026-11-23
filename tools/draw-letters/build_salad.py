"""S is for Salad (dx_salad_s), Food and drink A to Z, slot S (23 Nov 2026).
From his pick "S3 Big lettuce leaf" (Claude's second-go sketches, claude/step-by-draw-food-capitals-vehicles-small-14x4.md).

A bowl of salad with one big lettuce leaf at the front. The S is the wavy left edge of that leaf; a little tomato sits
in the bottom curve of the S. Written in the sketch's numbers.

    python3 build_salad.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=0.0)
SX, SY, SW, SH = 30, 11, 27, 46                                # the S: left, top, how wide, how tall
RIM = 62


def S(u, v):
    return (SX + u * SW, SY + v * SH)


S_SEGS = curve(S(0.95, 0.16), S(0.88, 0.06), S(0.72, 0), S(0.5, 0), S(0.2, 0), S(0.02, 0.11), S(0.02, 0.25), S(0.02, 0.4), S(0.24, 0.46), S(0.5, 0.5),
               S(0.76, 0.54), S(0.98, 0.6), S(0.98, 0.75), S(0.98, 0.89), S(0.8, 1), S(0.5, 1), S(0.28, 1), S(0.12, 0.94), S(0.05, 0.84))
S_TOP, S_END = S_SEGS[0].a, S_SEGS[-1].b
LEAF_R = smooth([S_TOP, (62, 9), (69, 6.5), (75, 12), (75.5, 21), (83, 24.5), (84.5, 34), (79.5, 41), (87, 48), (85, 56), (82, RIM)])
LEAF_L = Seg(S_END, (S_END[0] + 1, RIM))



def stick(a, b, w):
    """a carrot stick: a thin shape with round ends, from a to b"""
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); r = w / 2; th = math.degrees(math.atan2(dy, dx))
    nx, ny = -dy / L * r, dx / L * r
    p1, p2, p3, p4 = P(a[0] + nx, a[1] + ny), P(b[0] + nx, b[1] + ny), P(b[0] - nx, b[1] - ny), P(a[0] - nx, a[1] - ny)
    return [Seg(p1, p2)] + arc(b[0], b[1], r, r, th + 90, th - 90, start=p2, end=p3) + [Seg(p3, p4)] + arc(a[0], a[1], r, r, th - 90, th - 270, start=p4, end=p1)


# ---- at the back: the other leaves ----
p.stroke('moundL', smooth([(9, RIM), (5.5, 51), (10, 40), (19, 36), (22, 27), (31, 23), (38, 27)]), step=5)
p.stroke('moundR', smooth([(78, 36), (86, 41.5), (92.5, 50), (91, RIM)]), step=5)
# ---- carrot sticks and tomatoes, in front of those leaves ----
p.shape('carrot0', stick((12, 45), (27, 38), 3.6), step=4)
p.shape('carrot1', stick((12, 52), (29, 45), 3.6), step=4)
p.shape('wedge', circle(20, 63, 8.2), step=4)
p.shape('tom', circle(43, 47.6, 5.6), step=4)
# ---- the big leaf (its left edge is the S) ----
p.region('leafR', S_SEGS, LEAF_L, Seg((S_END[0] + 1, RIM), (82, RIM)), rev(LEAF_R))
p.stroke('leaf', LEAF_R, step=2)
p.stroke('leafl', LEAF_L, step=2)
RIB = Seg((62, RIM), (62, 46), (64.5, 31), (68.5, 17))
p.stroke('rib', RIB, step=6, deco=True)
for i, (t, c1, c2, e) in enumerate(((0.2, (67, 46.5), (72, 45.5), (78, 46.5)), (0.48, (68, 34.5), (73, 32.5), (78, 31.5)), (0.74, (64.4, 23.6), (62.4, 20.4), (60.4, 18)))):
    p.stroke('vein%d' % i, Seg(RIB.at(t), c1, c2, e), step=6, deco=True)
# ---- the bowl, in front of everything ----
p.shape('foot', rrect(37.4, 89.5, 62.6, 95.5, 2), step=3)
p.shape('bowl', one("M8,62 L92,62 C91,80.6 71.84,92 50,92 C28.16,92 9,80.6 8,62 Z"), step=3)
p.stroke('band0', Seg((6, 69), (94, 69)), step=3)
p.stroke('band1', Seg((6, 74.5), (94, 74.5)), step=3)
# ---- the S ----
p.stroke('s', S_SEGS, step=1)
p.build()
p.net.keep_in('band0', 'bowl'); p.net.keep_in('band1', 'bowl')

steps = [
    step('Start with an S', 'Draw a capital S: a curve one way at the top, then a curve the other way at the bottom.', p.step(1)),
    step('The big leaf', 'From the top end of the S, draw a wavy line up, round and down the right side. From the bottom end of the S draw a short line down.', p.step(2)),
    step('The bowl', 'Draw a line across under the leaf. Draw a big round bowl below it, with a little foot. Add two lines across the bowl.', p.step(3)),
    step('Tomatoes and carrot', 'Draw a small round tomato in the bottom curve of the S. On the left draw half a tomato on the bowl, and two carrot sticks above it.', p.step(4)),
    step('More leaves', 'On the left draw a bumpy line from the bowl up to the S. On the right draw a curved line from the big leaf down to the bowl.', p.step(5)),
    step('Leaf lines', 'Draw a line up the middle of the big leaf, and three little lines going out from it.', p.step(6)),
    step('Colour green', 'Colour the big leaf green. Colour the leaves behind it green too, round the tomatoes and the carrot sticks.',
         [p.face('green', (73, 26)), p.face('green', (14, 57), holes=('carrot0', 'carrot1', 'tom')), p.face('green', (88.5, 56))], use='green'),
    step('Colour red', 'Colour the little tomato and the half tomato red.', [p.ring('red', 'tom'), p.face('red', (20, 58.5))], use='red'),
    step('Colour orange', 'Colour the two carrot sticks orange.', [p.ring('orange', 'carrot0'), p.ring('orange', 'carrot1')], use='orange'),
    step('Colour light blue', 'Colour the stripe on the bowl light blue.', [p.face('lblue', (50, 71.7))], use='lblue'),
]
D = drawing('dx_salad_s', 'S is for Salad', 3, 15, 'things', ['Letters', 'Around the house'],
            'A bowl of salad with one big lettuce leaf. The capital S is hiding in it: the wavy edge of the big leaf.',
            steps, ['green', 'red', 'orange', 'lblue'])
ok = finish('salad', D, {'set': 'house-AZ', 'slot': 'S', 'kind': 'key', 'age_from': 4}, p)
