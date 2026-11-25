"""h is for helicopter (dx_helicopter_h), Vehicles a to z, slot h. A new helicopter, 25 Nov 2026.

He sent step 1 from the live app: "Do a better helicopter and better h". Claude sketched one (/home/claude/fix/boatheli.py),
he said "the helicopter is better, but the back part can you not bring that down in line with the other part?", so the
tail was brought down to come straight out of the middle of the cabin (/home/claude/fix/r2.py heli2), and then
"yes, you can make live the helicopter".

The h: its tall stick is the mast under the rotor, the back of the cabin and the back strut of the skid; its hump is the
top and front of the window, and comes down to the skid as the front strut. Written in the sketch's numbers; the Pic moves it
to the middle of the paper (and low enough that the rotor stays clear of the step number).

    python3 build_helicopter.py
"""
from bcommon import *
import ncommon

p = Pic(s=1.0, dx=10.2, dy=4.0)
SX, LX, TOP, FLOOR, FOOT = 40.0, 67.0, 16.0, 72.0, 84.0

p.shape('rotor', circle(SX, 13.3, 37.0, ry=2.7), step=2)
p.stroke('wline', Seg((SX, 60.0), (LX, 60.0)), step=3)
p.stroke('floor', Seg((SX, FLOOR), (LX, FLOOR)), step=3)
p.stroke('shine', one("M57.5,44.6 C60.4,45.8 62.4,48.6 62.9,52.2"), step=3, deco=True)
# the tail, then the tail rotor in front of its end
p.stroke('tail', one("M40,48 C34,48.2 28,49.6 22,51.4 L10.5,53 L10.5,58 L21,59.4 C28,60.6 34.6,66.4 40,72"), step=5)
p.shape('trotor', circle(8.0, 55.5, 6.2), step=4)
p.stroke('tx1', Seg((8.0, 49.3), (8.0, 61.7)), step=4, deco=True)
p.stroke('tx2', Seg((1.8, 55.5), (14.2, 55.5)), step=4, deco=True)
p.stroke('skid', one("M30.5,81.2 C31,83 32.4,84 34.5,84 L72,84 C75.4,84 77.4,82.4 77.8,79.6"), step=6)
# the h, in front of everything
p.stroke('arch', one("M40,48 C40,43 47,40 54,40 C62,40 67,46 67,54 L67,84"), step=1)
p.stroke('h', Seg((SX, TOP), (SX, FOOT)), step=1)
p.build()

steps = [
    step('Start with an h', 'Draw a small letter h: a tall stick, then a hump that comes back down as far as the stick. This h is hiding in the helicopter.', p.step(1)),
    step('The rotor', 'On top of the stick, draw a long flat oval for the spinning blades.', p.step(2)),
    step('Window and floor', 'Draw a line across the h for the bottom of the window, and another lower down for the floor. Draw a little curve in the window for a shine.', p.step(3)),
    step('The tail rotor', 'Far out to the left, draw a small circle with a cross in it.', p.step(4)),
    step('The tail', 'From where the hump starts, draw a line out to the small circle. Draw another line from the circle back to the floor.', p.step(5)),
    step('The skid', 'Draw a long skid under the helicopter. It touches the bottom of both lines of the h and curls up at each end.', p.step(6)),
    step('Colour grey', 'Colour the long blades and the small circle grey.', [p.ring('grey', 'rotor'), p.ring('grey', 'trotor')], use='grey'),
    step('Colour red', 'Colour the tail red. Colour the bottom of the cabin red too, under the window.', [p.face('red', (28.0, 56.0)), p.face('red', (53.0, 66.0))], use='red'),
    step('Colour the window', 'Colour the window light blue.', [p.face('lblue', (50.0, 50.0))], use='lblue'),
]
D = drawing('dx_helicopter_h', 'h is for helicopter', 2, 10, 'vehicles', ['Letters', 'Vehicles'],
            'A red helicopter with a big window. The small letter h is hiding in it: its tall stick is the mast and the back of the '
            'cabin, and its hump is the top and front of the window.',
            steps, ['grey', 'red', 'lblue'])
ok = finish('helicopter', D, {'set': 'vehicles-az', 'slot': 'h', 'kind': 'fly', 'age_from': 5}, p, allow=('4',))   # the cross in the tail rotor is meant
