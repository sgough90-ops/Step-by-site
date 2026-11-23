"""b is for Blueberries (dx_blueberries_b), Food and drink a to z, slot b (23 Nov 2026).
From his pick, round 2 number 1 "Three on the twig" (Claude's sketches, claude/step-by-draw-food-small-round2-and-five-builds.md):
"do the steps for [blueberry] number one".

A twig with a big blueberry against it at the bottom, two smaller berries on little stalks on the other side, and
two leaves. The b is the right edge of the twig (its tall line) and the big berry (its round). The round goes just
past the line (as the g of the gingerbread does), so the two meet cleanly. Written in the sketch's numbers.

    python3 build_blueberry.py
"""
import qcheck                                    # the quicker crossing test (the same 9 checks)
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=3.0)
X, TOP, BOT, R = 48.0, 8.0, 92.0, 21.0           # the b's line, and the size of its round (the big berry)
BCX, BCY = X + R - 0.35, BOT - R                 # the middle of the big berry
XL = X - 5.0                                     # the twig's other edge
B1, B2 = (21.5, 28.0, 11.5), (29.5, 51.0, 9.5)   # the two smaller berries
LA, LB = ((46, 12), (64, 1.5), 9), ((44, 76), (25, 86), 10)   # the leaves: where they start (behind the twig), their tip, their width


def leaf(base, tip, w):
    (bx, by), (tx, ty) = base, tip
    dx, dy = tx - bx, ty - by; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L; h = w * 0.67
    at = lambda t, s: (bx + dx * t + nx * s, by + dy * t + ny * s)
    return [Seg(base, at(0.18, h), at(0.68, h), tip), Seg(tip, at(0.68, -h), at(0.18, -h), base)]


def middle(base, tip, w=None, t0=0.2, t1=0.8):
    return Seg((base[0] + (tip[0] - base[0]) * t0, base[1] + (tip[1] - base[1]) * t0), (base[0] + (tip[0] - base[0]) * t1, base[1] + (tip[1] - base[1]) * t1))


# ---- behind the twig: the leaves and the little stalks (their ends run on behind it and are trimmed) ----
p.shape('leafA', leaf(*LA), step=4)
p.stroke('midA', middle(*LA), step=4, deco=True, w=1.2)
p.shape('leafB', leaf(*LB), step=4)
p.stroke('midB', middle(*LB), step=4, deco=True, w=1.2)
p.stroke('stalk1', Seg((43.5, 19), (38, 16.5), (33, 17), (28.6, 21)), step=3)
p.stroke('stalk2', Seg((43.5, 42), (40.5, 40.5), (38, 41), (34.6, 45)), step=3)

# ---- the twig (its right edge is the b's line), then the berries in front ----
p.region('twigR', box(XL, TOP, X, BOT))
p.stroke('twig', Seg((X, TOP), (XL, TOP)), Seg((XL, TOP), (XL, BOT)), Seg((XL, BOT), (X, BOT)), step=2)
p.shape('berry1', circle(*B1), step=3)
p.shape('berry2', circle(*B2), step=3)
p.shape('b_round', circle(BCX, BCY, R), step=1)
for k, (cx, cy, r, ox, oy, sr) in enumerate(((BCX, BCY, R, 0.36, 0.1, 6.3), (B1[0], B1[1], B1[2], -0.25, 0.3, 3.5), (B2[0], B2[1], B2[2], 0.2, 0.35, 3.0))):
    p.stroke('star%d' % k, star5(cx + ox * r, cy + oy * r, sr, 0.43), step=5, deco=True, w=1.2)
    p.stroke('shine%d' % k, arc(cx, cy, r * 0.72, r * 0.72, 196, 236), step=5, deco=True, w=1.2)

# ---- the b's line, in front of everything ----
p.stroke('b_stick', Seg((X, TOP), (X, BOT)), step=1)
p.build()

steps = [
    step('Start with a b', 'Draw a small letter b: a tall line down, then a big round shape on its right, at the bottom.', p.step(1)),
    step('The twig', 'The tall line is a twig. Go across its top, draw a second line down beside it, and join them at the bottom.', p.step(2)),
    step('Two more berries', 'On the other side of the twig, draw two short curved stalks. Draw a round berry on the end of each one.', p.step(3)),
    step('The leaves', 'Draw a pointed leaf at the top of the twig and another near the bottom. Add a line down the middle of each.', p.step(4)),
    step('Stars and shine', 'Draw a little star on each berry. Add a short curved line on each one to make it shine.', p.step(5)),
    step('Colour blue', 'Colour the three blueberries blue.', [p.ring('blue', 'b_round'), p.ring('blue', 'berry1'), p.ring('blue', 'berry2')], use='blue'),
    step('Colour green', 'Colour the two leaves green.', [p.face('green', (56, 7)), p.face('green', (34.5, 81))], use='green'),
    step('Colour the twig', 'Colour the twig brown.', [p.face('brown', (45.5, 50))], use='brown'),
]
D = drawing('dx_blueberries_b', 'b is for Blueberries', 2, 10, 'things', ['Letters', 'Around the house'],
            'Three blueberries on a twig. The small letter b is hiding in them: it is the edge of the twig and the big berry.',
            steps, ['blue', 'green', 'brown'])
ok = finish('blueberry', D, {'set': 'house-az', 'slot': 'b', 'kind': 'key', 'age_from': 4}, p)
