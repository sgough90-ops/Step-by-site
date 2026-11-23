"""z is for zipline car (dx_ziplinecar_z), Vehicles a to z, slot z (22 Nov 2026).
From his pick "z 1 Slanting arm" (claude/step-by-draw-vehicles-small-12-ideas-4-versions.md).

A red car hanging from a wire. The z is the bottom of the grey trolley on the wire, the slanting arm, and the top of
the bar on the car's roof. Written in the sketch's numbers; the Pic moves it onto the paper.

    python3 build_ziplinecar.py
"""
from bcommon import *

p = Pic(s=0.94, dx=3.0, dy=2.6)
ZX0, ZX1, ZT, ZB = 36, 62, 24, 46

# ---- behind: two clouds, the wire ----
p.shape('cloud1', cloud(8, 41, 0.95), step=6)
p.shape('cloud2', cloud(77, 36, 0.85), step=6)
p.stroke('wire', Seg((0, 17), (100, 17)), step=3)

# ---- the trolley on the wire (its bottom edge is the top of the z) and its two wheels ----
TR = "M36,24 L36,14 Q36,11 39,11 L59,11 Q62,11 62,14 L62,24"
p.region('trolleyR', one(TR + " Z"))
p.stroke('trolley', one(TR), step=2)
p.shape('wheel1', circle(42.5, 16.6, 2.8), step=2)
p.shape('wheel2', circle(55.5, 16.6, 2.8), step=2)

# ---- the bar on the roof (its top edge is the bottom of the z), the car and its windows ----
p.stroke('bar_l', Seg((ZX0, ZB), (ZX0, 50)), step=4)
p.stroke('bar_r', Seg((ZX1, ZB), (ZX1, 50)), step=4)
p.shape('car', rrect(20, 50, 80, 88, 10), step=4)
for i, x in enumerate((25.5, 43, 60.5)):
    p.shape('win%d' % i, rrect(x, 57, x + 14, 72, 3), step=5)

# ---- the z, in front of everything ----
p.stroke('z', poly((ZX0, ZT), (ZX1, ZT), (ZX0, ZB), (ZX1, ZB)), step=1)
p.build()

steps = [
    step('Start with a z', 'Draw a small letter z: a line across the top, a slanting line down to the left, and a line across the bottom.', p.step(1)),
    step('The trolley', 'From the left end of the top line go up, across with round corners, and down to the right end. Draw two little wheels inside.', p.step(2)),
    step('The wire', 'Draw a long straight line out from each side of the trolley. This is the wire it rides along.', p.step(3)),
    step('The car', 'Draw a short line down from each end of the bottom line. Under them draw a big box with very round corners.', p.step(4)),
    step('Three windows', 'Draw three windows with round corners in a row across the car.', p.step(5)),
    step('Clouds', 'Draw a little cloud on each side.', p.step(6)),
    step('Colour red', 'Colour the car red, round the three windows.', [p.ring('red', 'car', holes=('win0', 'win1', 'win2'))], use='red'),
    step('Colour light blue', 'Colour the three windows light blue.', [p.ring('lblue', 'win%d' % i) for i in range(3)], use='lblue'),
    step('Colour grey', 'Colour the trolley grey, round its two wheels.', [p.face('grey', (49, 21.5), holes=('wheel1', 'wheel2'))], use='grey'),
    step('Colour black', 'Colour the two little wheels and the bar on the roof black.',
         [p.ring('black', 'wheel1'), p.ring('black', 'wheel2'), p.face('black', (49, 48))], use='black'),
]
D = drawing('dx_ziplinecar_z', 'z is for zipline car', 2, 12, 'vehicles', ['Letters', 'Vehicles'],
            'A red car hanging from a wire. The small letter z is hiding above it: the bottom of the trolley, '
            'the slanting arm and the bar on the roof.',
            steps, ['red', 'lblue', 'grey', 'black'])
ok = finish('ziplinecar', D, {'set': 'vehicles-az', 'slot': 'z', 'kind': 'drive', 'age_from': 5}, p)
