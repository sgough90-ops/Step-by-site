"""n is for narrowboat (dx_narrowboat_n), Vehicles a to z, slot n (22 Nov 2026).
From his pick "n 3 From the front" (claude/step-by-draw-vehicles-small-12-ideas-4-versions.md).

A narrowboat seen from the front. The n is the end of the cabin: up the left side, over the round roof and down
the right side. Written in the sketch's numbers.

    python3 build_narrowboat.py
"""
from bcommon import *

p = Pic(s=1.0, dx=0.0, dy=0.5)
NX0, NX1, NT, NB, NRY = 35, 65, 42, 66, 11      # the n: legs from the deck up to 42, then the arch

# ---- on the roof, behind the cabin end: chimney and smoke, plant and pot ----
p.shape('smoke', circle(59.5, 12.5, 3.2), step=5)
p.stroke('chimney', one("M57,40 L57,19 Q57,18 58,18 L61,18 Q62,18 62,19 L62,40"), step=5)
p.shape('plant', circle(41, 24.6, 3.6), step=5)
p.region('potR', box(37.5, 27.5, 44.5, 40))
p.stroke('pot', one("M37.5,40 L37.5,28.5 Q37.5,27.5 38.5,27.5 L43.5,27.5 Q44.5,27.5 44.5,28.5 L44.5,40"), step=5)

# ---- the hull, the fender on its nose, the water in front ----
p.shape('hull', one("M27,66 L73,66 C72,78 62,90 50,92 C38,90 28,78 27,66 Z"), step=2)
p.shape('fender', circle(50, 71.2, 3.4, ry=2.3), step=4)
p.shape('sea', blob(13, 87, 84.5, depth=9.5), step=2)

# ---- the cabin end (hides the bottoms of the chimney and the pot), doors, windows, lamp ----
p.region('cabinR', Seg((NX0, 65.8), (NX0, NT)), arc(50, NT, 15, NRY, 180, 360), Seg((NX1, NT), (NX1, 65.8)), Seg((NX1, 65.8), (NX0, 65.8)))
p.stroke('doors', one("M40.6,66 L40.6,48.5 Q40.6,47 42.1,47 L57.9,47 Q59.4,47 59.4,48.5 L59.4,66"), step=3)
p.stroke('doormid', Seg((50, 47), (50, 66)), step=3)
p.shape('dwin0', rrect(42.3, 50.4, 47.7, 56.4, 1), step=3)
p.shape('dwin1', rrect(52.3, 50.4, 57.7, 56.4, 1), step=3)
p.shape('lamp', circle(50, 38.6, 2.7), step=4)

# ---- the n, in front of everything ----
p.stroke('n', Seg((NX0, NB), (NX0, NT)), arc(50, NT, 15, NRY, 180, 360), Seg((NX1, NT), (NX1, NB)), step=1)
p.build()

steps = [
    step('Start with an n', 'Draw a small letter n: a straight line up, over the top in a round arch, and straight down the other side.', p.step(1)),
    step('The boat and the water', 'Draw a line under the n, a bit wider than it. From each end curve down and in. Draw a long wavy puddle of water across the bottom.', p.step(2)),
    step('Two doors', 'Inside the n draw a big door shape with a line down the middle. Draw a little window in each door.', p.step(3)),
    step('Lamp and bumper', 'Draw a round lamp above the doors. Draw a little oval on the front of the boat.', p.step(4)),
    step('On the roof', 'On the roof draw a tall chimney with a puff of smoke above it. Draw a plant pot with a round bush in it.', p.step(5)),
    step('Colour green', 'Colour the cabin green, round the doors and the lamp. Colour the bush green too.',
         [p.face('green', (50, 44.4), holes=('lamp',)), p.face('green', (41, 23))], use='green'),
    step('Colour red', 'Colour the two doors red, round their windows. Colour the plant pot red.',
         [p.face('red', (45, 60), holes=('dwin0',)), p.face('red', (55, 60), holes=('dwin1',)), p.face('red', (41, 30))], use='red'),
    step('Colour black', 'Colour the boat black, down to the water and round the little oval. Colour the chimney black.',
         [p.face('black', (40, 74), holes=('fender',)), p.face('black', (59.5, 26))], use='black'),
    step('Colour light blue', 'Colour the water and the two door windows light blue.',
         [p.ring('lblue', 'sea'), p.ring('lblue', 'dwin0'), p.ring('lblue', 'dwin1')], use='lblue'),
    step('Colour yellow', 'Colour the lamp and the little oval yellow.', [p.ring('yellow', 'lamp'), p.ring('yellow', 'fender')], use='yellow'),
]
D = drawing('dx_narrowboat_n', 'n is for narrowboat', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A narrowboat coming towards you on the canal. The small letter n is hiding in it: the round end of the cabin.',
            steps, ['green', 'red', 'black', 'lblue', 'yellow'])
ok = finish('narrowboat', D, {'set': 'vehicles-az', 'slot': 'n', 'kind': 'sail', 'age_from': 5}, p)
