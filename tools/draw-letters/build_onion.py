"""o is for Onion (dx_onion_o), Food and drink a to z, slot o (23 Nov 2026).
From his pick "o1 A whole onion" (Claude's sketches, claude/step-by-draw-food-small-12-ideas-4-versions.md),
with the top turned green at his ask ("the part at the top ... is brown, turn that green").

A big round onion with a green shoot on top, little roots underneath, curved lines down its skin and a bit of
skin lying beside it. The o is the onion itself. Written in the sketch's numbers.

    python3 build_onion.py
"""
import qcheck                                    # the quicker crossing test (the same 9 checks)
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=-2.5)
CX, CY, R = 50, 59, 30                           # the o

# ---- behind the onion: the shoot and the roots (their ends run on behind it and are trimmed) ----
p.stroke('shoot', one("M43,35 C45.1,23.8 43,14.2 50,7 C52.1,16.6 57,23.8 57,35"), step=2)
p.stroke('shootmid', one("M50,11.5 C49,17.6 50.6,24.4 50,32"), step=2, deco=True, w=1.2)
for i, dx in enumerate((-9, -5, -1, 3, 7)):
    y, drop = CY + R, 8
    p.stroke('root%d' % i, Seg((CX + dx * 0.7, y - 2), (CX + dx * 0.8 - 1, y + drop * 0.3), (CX + dx + 1.4, y + drop * 0.6), (CX + dx * 1.15, y + drop + (i % 2))),
             step=3, w=1.2)

# ---- the o, in front ----
p.shape('o', circle(CX, CY, R), step=1)

# ---- on the onion: the lines down its skin; beside it: a bit of skin ----
for i, k in enumerate((-0.62, -0.26, 0.26, 0.62)):
    p.stroke('skin%d' % i, one("M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f" % (CX + k * R * 0.34, CY - R + 3, CX + k * R * 1.5, CY, CX + k * R * 0.34, CY + R - 3)),
             step=4, deco=True, w=1.2)
p.shape('flake', one("M80,93 C84,86 92,85 96,90 C91,90 87,92 85,96 Z"), step=4)
p.build()

steps = [
    step('Start with an o', 'Draw a small letter o: one big round shape, as wide as it is tall. This o is hiding in the onion.', p.step(1)),
    step('The shoot', 'On top of the o, draw a tall pointed shoot: up one side to a point and down the other. Add a line down its middle.', p.step(2)),
    step('The roots', 'Under the o, draw five little wiggly lines for the roots.', p.step(3)),
    step('The skin', 'Draw four curved lines down the onion, from near the top to near the bottom. Draw a little bit of skin lying beside it.', p.step(4)),
    step('Colour the onion', 'Colour the onion light brown. Colour the little bit of skin too.', [p.ring('lbrown', 'o'), p.ring('lbrown', 'flake')], use='lbrown'),
    step('Colour the shoot', 'Colour the shoot on top of the onion green.', [p.face('green', (50, 20))], use='green'),
]
D = drawing('dx_onion_o', 'o is for Onion', 1, 8, 'things', ['Letters', 'Around the house'],
            'A big round onion with a green shoot on top. The small letter o is hiding in it: it is the onion itself.',
            steps, ['lbrown', 'green'])
ok = finish('onion', D, {'set': 'house-az', 'slot': 'o', 'kind': 'key', 'age_from': 4}, p)
