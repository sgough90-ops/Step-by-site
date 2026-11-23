"""q is for Quinoa (dx_quinoa_q), Food and drink a to z, slot q (23 Nov 2026).
From his pick "q1 With a spoon" (Claude's sketches, claude/step-by-draw-food-small-12-ideas-4-versions.md), with
his two changes: "you seem to have the vertical bottom part too low, lift it up, and also make it look more like
a spoon".

A bowl of quinoa seen from above, with peas and bits of red pepper, and a spoon lying beside it. The q is the edge
of the bowl (its round) and the left edge of the spoon's handle (its line), with the round end of the handle as
its flick. The line now ends 11.5 below the bowl (it was 19): any shorter and it starts to read as an a.
The round goes just past the line (as the g of the gingerbread does), so the two meet cleanly.
Written in the sketch's numbers.

    python3 build_quinoa.py
"""
import random
import qcheck                                    # the quicker crossing test (the same 9 checks)
from bcommon import *

p = Pic(s=1.0, dx=4.0, dy=11.0)
CX, CY, R, RIN = 40.35, 44, 30, 24.5             # the bowl: the q's round, and the inside of its edge
X = 70.0                                         # the q's line (the left edge of the spoon's handle)
OX, OY, ORX, ORY = 72.8, 3.2, 8.2, 11.5          # the round end of the spoon
TOPY = OY + ORY * math.sqrt(1 - ((X - OX) / ORX) ** 2)   # where the handle leaves it (level with the top of the bowl)
XR0, XR1, YR1 = 2 * OX - X, 77.4, 78.0           # the handle's other edge: top, bottom
SB, FB, FX = 80.5, 85.5, 73.7                    # the q's line ends, the flick's lowest point



def square(x, y, half, deg):
    """a little square turned by deg degrees"""
    a = math.radians(deg); c, s_ = math.cos(a), math.sin(a)
    return poly(*[(x + u * half * c - v * half * s_, y + u * half * s_ + v * half * c) for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))], closed=True)


flick = Seg((X, SB), (X, SB + 3.1), (X + 1.6, FB), (FX, FB))
end = Seg((FX, FB), (FX + 2.3, FB), (XR1, YR1 + 4.6), (XR1, YR1))
side = Seg((XR0, TOPY), (XR1, YR1))

# ---- the spoon: its round end, then the handle in front of it (so the two join up) ----
p.shape('spoon', circle(OX, OY, ORX, ry=ORY), step=3)
p.stroke('hollow', arc(OX, OY, 4.8, 8.0, 115, 245), step=3, deco=True, w=1.2)
p.region('handleR', Seg((X, TOPY), (XR0, TOPY)), side, end.rev(), flick.rev(), Seg((X, SB), (X, TOPY)))
p.stroke('handle', side, end.rev(), step=2)

# ---- the bowl: the q's round, the inside of its edge, the peas and the peppers ----
p.shape('q_round', circle(CX, CY, R), step=1)
p.shape('inner', circle(CX, CY, RIN), step=4)
PEAS = [(34, 29), (56, 46), (31, 57)]
PEPS = [(49, 31, 20), (24.5, 43, -15), (46, 60, 35)]
for i, (x, y) in enumerate(PEAS):
    p.shape('pea%d' % i, circle(x, y, 2.9), step=5)
for i, (x, y, deg) in enumerate(PEPS):
    p.shape('pep%d' % i, square(x, y, 2.7, deg), step=5)

# ---- the q's line, in front of everything ----
p.stroke('q_stick', Seg((X, TOPY), (X, SB)), flick, step=1)
p.build()

# ---- the quinoa: lots of little dots, clear of the peas, the peppers and the edge ----
rnd = random.Random(11)
grains = []
while len(grains) < 14:                           # 14 is the most new lines the app's own checker allows in one step
    a, rr = rnd.uniform(0, 2 * math.pi), (RIN - 3.4) * math.sqrt(rnd.uniform(0, 1))
    g = (CX + rr * math.cos(a), CY + rr * math.sin(a))
    if all(math.dist(g, (x, y)) > 6.2 for x, y in PEAS) and all(math.dist(g, (x, y)) > 7.0 for x, y, _ in PEPS) and all(math.dist(g, h) > 8.2 for h in grains):
        grains.append(g)
dots = [dot(*p.pt(x, y), w=2.8) for x, y in grains]
VEG = tuple('pea%d' % i for i in range(3)) + tuple('pep%d' % i for i in range(3))

steps = [
    step('Start with a q', 'Draw a small letter q: a big round shape, a straight line down its right side, and a little flick at the bottom.', p.step(1)),
    step('The handle', 'The line of the q is the handle of a spoon. Draw a second line beside it, and join them at the bottom with a round end.', p.step(2)),
    step('The spoon', 'On top of the handle, draw a big oval for the round end of the spoon. Add a curved line inside it.', p.step(3)),
    step('The bowl', 'The round part of the q is a bowl, seen from above. Draw a smaller circle inside it.', p.step(4)),
    step('Peas and peppers', 'In the bowl, draw three little circles for peas and three little squares for bits of red pepper.', p.step(5)),
    step('The quinoa', 'Dot the rest of the bowl with little dots. That is the quinoa.', dots),
    step('Colour the bowl', 'Colour the edge of the bowl blue.', [p.face('blue', (CX, CY - R + 2.7), holes=('inner',))], use='blue'),
    step('Colour the quinoa', 'Colour the quinoa light brown, all round the peas and the peppers.', [p.ring('lbrown', 'inner', holes=VEG)], use='lbrown'),
    step('Colour the spoon', 'Colour the spoon grey.', [p.face('grey', (OX, OY - 4))], use='grey'),
    step('Colour the peas', 'Colour the three peas green.', [p.ring('green', 'pea%d' % i) for i in range(3)], use='green'),
    step('Colour the peppers', 'Colour the three bits of pepper red.', [p.ring('red', 'pep%d' % i) for i in range(3)], use='red'),
]
D = drawing('dx_quinoa_q', 'q is for Quinoa', 2, 12, 'things', ['Letters', 'Around the house'],
            'A bowl of quinoa with peas and peppers, and a spoon beside it. The small letter q is hiding in it: the edge of the bowl and the handle of the spoon.',
            steps, ['blue', 'lbrown', 'grey', 'green', 'red'])
ok = finish('quinoa', D, {'set': 'house-az', 'slot': 'q', 'kind': 'key', 'age_from': 4}, p)
