"""v is for van (dx_van_v), Vehicles a to z, slot v (22 Nov 2026).
From his pick "v 4 Two colours on the side" (claude/step-by-draw-vehicles-small-12-ideas-4-versions.md).

A van facing left. The v is where the two colours meet on its side: the top colour dips down in a V.
Written in the sketch's numbers; the Pic moves it onto the paper.

    python3 build_van.py [yellow]     (with "yellow" the top is coloured yellow; without, it stays white)
"""
import sys
from bcommon import *

TOP = 'yellow' if 'yellow' in sys.argv[1:] else None
p = Pic(s=1.06, dx=-3.4, dy=-9.6)

SIL = "M8,74 L8,58 C8,52 12,50 18,48 L26,32 Q28,28 32,28 L86,28 Q92,28 92,34 L92,70 Q92,74 88,74 Z"
p.shape('body', one(SIL), step=4)
p.stroke('side_l', Seg((20.5, 43), (47, 43)), step=2)
p.stroke('side_r', Seg((77, 43), (92, 43)), step=2)
p.shape('win0', one("M26.4,40 L30,32.6 L40,32.6 L40,40 Z"), step=5)
p.shape('win1', rrect(49, 32.6, 61, 40, 1.5), step=5)
p.shape('win2', rrect(66, 32.6, 78, 40, 1.5), step=5)
p.shape('lamp', rrect(7, 60, 10.6, 66, 1), step=4)
for i, x in enumerate((26, 78)):
    p.shape('tyre%d' % i, circle(x, 76, 9.6), step=3)
    p.shape('hub%d' % i, circle(x, 76, 4.2), step=3)
p.stroke('v', poly((47, 43), (62, 70), (77, 43)), step=1)
p.build()

steps = [
    step('Start with a v', 'Draw a small letter v: a slanting line down to a point, then a slanting line back up.', p.step(1)),
    step('Out to the sides', 'From the top of the v draw a long line out to the left and a shorter line out to the right.', p.step(2)),
    step('Two wheels', 'Under the v draw two big circles, one each side. Draw a small circle inside each one.', p.step(3)),
    step('The van', 'Join the wheels along the bottom. Go up the back, along the roof, down the sloping front and round the nose. Draw a little light on the nose.', p.step(4)),
    step('Three windows', 'Draw a sloping window at the front and two more windows behind it.', p.step(5)),
    step('Colour green', 'Colour the bottom of the van green, up to the v and the two lines.', [p.face('green', (30, 60))], use='green'),
]
if TOP:
    steps.append(step('Colour yellow', 'Colour the top of the van yellow, down into the v. Colour the little light too.',
                      [p.face('yellow', (62, 50), holes=('win0', 'win1', 'win2')), p.ring('yellow', 'lamp')], use='yellow'))
else:
    steps.append(step('Colour yellow', 'Colour the little light on the nose yellow. The top of the van stays white.', [p.ring('yellow', 'lamp')], use='yellow'))
steps += [
    step('Colour light blue', 'Colour the three windows light blue.', [p.ring('lblue', 'win%d' % i) for i in range(3)], use='lblue'),
    step('Colour black', 'Colour the two tyres black, round the small circles.', [p.ring('black', 'tyre%d' % i, holes=('hub%d' % i,)) for i in range(2)], use='black'),
    step('Colour grey', 'Colour the middle of each wheel grey.', [p.ring('grey', 'hub%d' % i) for i in range(2)], use='grey'),
]
D = drawing('dx_van_v', 'v is for van', 2, 12, 'vehicles', ['Letters', 'Vehicles'],
            'A van in two colours. The small letter v is hiding on its side, where the two colours meet.',
            steps, ['green', 'yellow', 'lblue', 'black', 'grey'])
name = 'van-yellow' if TOP else 'van'
ok = finish(name, D, {'set': 'vehicles-az', 'slot': 'v', 'kind': 'drive', 'age_from': 5}, p)
