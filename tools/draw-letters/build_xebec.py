"""x is for xebec (dx_xebec_x), Vehicles a to z, slot x (22 Nov 2026).
From his pick "x 2 Ropes between the masts" (claude/step-by-draw-vehicles-small-12-ideas-4-versions.md).

A xebec: an old sailing ship with three-cornered sails. The x is the two ropes that cross between its two masts,
from the top of each mast to the foot of the other. The masts are a little wider apart than in the sketch so the x
has a normal shape. Written in the sketch's numbers.

    python3 build_xebec.py
"""
from bcommon import *

p = Pic(s=0.97, dx=0.9, dy=5.0)
ML0, ML1, MR0, MR1 = 29.8, 32.2, 67.8, 70.2     # the two masts (thin boxes)
DECK, MTOP, XTOP = 66, 11, 24

# ---- behind the hull: the cabin at the back, sails, masts, flags, the pole at the front ----
p.stroke('cabin', one("M6,66 L6,57 Q6,55 8,55 L20,55 Q22,55 22,57 L22,66"), step=5)
p.shape('cwin', rrect(10.5, 58, 17.5, 63, 1), step=5)
p.stroke('sail_l', poly((ML0, 19), (11, 46), (ML0, 57)), step=4)
p.stroke('sail_r', poly((MR1, 19), (90, 49), (MR1, 57)), step=4)
p.stroke('mast_l', poly((ML0, DECK), (ML0, MTOP), (ML1, MTOP), (ML1, DECK)), step=2)
p.stroke('mast_r', poly((MR0, DECK), (MR0, MTOP), (MR1, MTOP), (MR1, DECK)), step=2)
p.stroke('flag_l', poly((ML1, MTOP), (40, 13.7), (ML1, 16.4)), step=4)
p.stroke('flag_r', poly((MR1, MTOP), (78, 13.7), (MR1, 16.4)), step=4)
p.stroke('pole', Seg((96, 66), (99.2, 62.2)), step=3)

# ---- the hull, the plank line along it, the water in front ----
p.shape('hull', one("M4,66 L96,66 C95,74 89,82 80,82 L18,82 C11,82 6,75 4,66 Z"), step=3)
p.stroke('plank', Seg((1, 72), (99, 72)), step=3, deco=True)
p.shape('sea', blob(5, 95, 78.6, depth=9), step=3)

# ---- the x, in front of everything ----
p.stroke('x1', Seg((ML1, XTOP), (MR0, DECK)), step=1)
p.stroke('x2', Seg((MR0, XTOP), (ML1, DECK)), step=1)
p.build()
p.net.keep_in('plank', 'hull')

steps = [
    step('Start with an x', 'Draw a small letter x: two slanting lines that cross in the middle.', p.step(1)),
    step('Two masts', 'Draw a tall thin mast up each side of the x. Each one is a long thin box that goes up past the top of the x.', p.step(2)),
    step('The ship and the sea', 'Draw a long line under it all. Curve down at each end, with a line along the side and a little pole at the front. Draw wavy water.', p.step(3)),
    step('Sails and flags', 'Draw a pointed sail on the outside of each mast. Draw a little pointed flag at the top of each mast.', p.step(4)),
    step('The cabin', 'At the back of the ship draw a little cabin with round corners and a window.', p.step(5)),
    step('Colour brown', 'Colour the ship and the two masts brown.',
         [p.face('brown', (50, 69)), p.face('brown', (31, 40)), p.face('brown', (69, 40))], use='brown'),
    step('Colour light brown', 'Colour the cabin light brown, round its window.', [p.face('lbrown', (14, 56.5), holes=('cwin',))], use='lbrown'),
    step('Colour red', 'Colour the two flags red.', [p.face('red', (35, 13.7)), p.face('red', (73, 13.7))], use='red'),
    step('Colour light blue', 'Colour the water and the cabin window light blue. The sails stay white.', [p.ring('lblue', 'sea'), p.ring('lblue', 'cwin')], use='lblue'),
]
D = drawing('dx_xebec_x', 'x is for xebec', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A xebec is an old sailing ship. The small letter x is hiding in it: the two ropes that cross between the masts.',
            steps, ['brown', 'lbrown', 'red', 'lblue'])
ok = finish('xebec', D, {'set': 'vehicles-az', 'slot': 'x', 'kind': 'sail', 'age_from': 5}, p)
