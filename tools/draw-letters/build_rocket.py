"""r is for rocket (dx_rocket_small_r), Vehicles a to z, slot r (22 Nov 2026).
From his pick "r 1 Side and nose" (claude/step-by-draw-vehicles-small-12-ideas-4-versions.md).
The key dx_rocket_r is already used by the capital R rocket, so this one has its own key.

The r is the left side of the rocket and the curve up to the ball on its tip. The ball sits on the end of the r,
so the r's line stops there and does not carry on. Written in the sketch's numbers.

Step 1 draws a normal-looking r: only the top part of the straight side (down to RCUT) and the curve. Step 2 carries
the straight line on down to the bottom of the rocket (23 Nov 2026: with the whole side in step 1 the r was 58 tall
and 12 wide, stretched tall like the heron's H and the dumper's d were before their step 1 was fixed).

25 Nov 2026: he asked for the little extras to come out of the final pictures and for each picture to sit in the
middle of the paper. The four stars round the rocket are gone (their step, and their yellow), and the rocket is 6
higher (dy was -1.5), so its middle is the middle of the paper. See noextras.py.

    python3 build_rocket.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=-7.5)
CX, NY, RX, RY = 50, 42, 14, 20            # the nose is half an oval on top of the body
BX, BY, BR = 50, 20.4, 3.0                 # the ball on the tip
L, R, BOT = 36, 64, 80
RCUT = 64                                  # step 1's r stops here; step 2 carries its straight line on down


def meet():
    """how many degrees before the top the nose curve meets the ball"""
    lo, hi = 0.0, 40.0
    for _ in range(60):
        m = (lo + hi) / 2; a = math.radians(270 - m)
        d = math.hypot(CX + RX * math.cos(a) - BX, NY + RY * math.sin(a) - BY)
        if d < BR: lo = m
        else: hi = m
    return (lo + hi) / 2


DL = meet()

# ---- behind: flames, fins ----
p.stroke('flame', one("M42,80 C40,88 44,94 50,98 C56,94 60,88 58,80"), step=5)
p.stroke('flame_in', one("M46,80 C45,85 47,89 50,92 C53,89 55,85 54,80"), step=5)
p.stroke('fin_l', one("M36,60 C27,62 21,72 20,87 L36,80"), step=4)
p.stroke('fin_r', one("M64,60 C73,62 79,72 80,87 L64,80"), step=4)

# ---- the rest of the body: from the ball down the right side and along the bottom ----
p.stroke('body_r', arc(CX, NY, RX, RY, 270 + DL, 360), Seg((R, NY), (R, BOT)), Seg((R, BOT), (L, BOT)), step=2)
p.stroke('noseline', Seg((L, NY), (R, NY)), step=3)
p.shape('port', circle(50, 54, 7.6), step=3)
p.shape('glass', circle(50, 54, 5), step=3)
leaf = one("M50,78.5 C45.6,74.5 45.6,68.5 50,65 C54.4,68.5 54.4,74.5 50,78.5 Z")
p.shape('fin_c', leaf, step=4)
p.shape('ball', circle(BX, BY, BR), step=2)

# ---- the r, in front of everything: the straight side, then the curve up to the ball ----
p.stroke('r_down', Seg((L, RCUT), (L, BOT)), step=2)
p.stroke('r', Seg((L, RCUT), (L, NY)), arc(CX, NY, RX, RY, 180, 270 - DL), step=1)
p.build()

steps = [
    step('Start with an r', 'Draw a small letter r: a straight line going up, then a curve over to the right. Stop before the top.', p.step(1)),
    step('Make it a rocket', 'Make the straight line of the r longer, going down. Draw a little ball on the end of the r. From the ball curve down the other side and join the bottom.', p.step(2)),
    step('Nose and window', 'Draw a line across under the nose. Draw a round window with a smaller circle inside it.', p.step(3)),
    step('Three fins', 'Draw a curved fin on each side of the rocket. Draw a leaf shape in the middle near the bottom.', p.step(4)),
    step('Flames', 'Draw a big pointed flame under the rocket and a smaller flame inside it.', p.step(5)),
    step('Colour red', 'Colour the nose, the two side fins and the leaf shape red.',
         [p.face('red', (50, 34)), p.face('red', (29, 72)), p.face('red', (71, 72)), p.ring('red', 'fin_c')], use='red'),
    step('Colour orange', 'Colour the big flame orange, round the small flame.', [p.face('orange', (43.6, 84))], use='orange'),
    step('Colour yellow', 'Colour the small flame and the ball on the tip yellow.', [p.face('yellow', (50, 86)), p.ring('yellow', 'ball')], use='yellow'),
    step('Colour light blue', 'Colour the middle of the window light blue.', [p.ring('lblue', 'glass')], use='lblue'),
]
D = drawing('dx_rocket_small_r', 'r is for rocket', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A rocket blasting off. The small letter r is hiding in it: the straight left side and the curve up to the ball on the tip.',
            steps, ['red', 'orange', 'yellow', 'lblue'])
ok = finish('rocket', D, {'set': 'vehicles-az', 'slot': 'r', 'kind': 'fly', 'age_from': 5}, p)
