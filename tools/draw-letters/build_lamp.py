"""r is for reading lamp (Around the house a to z, slot r).
The r: its straight line is the lamp's pole and its arch is the arm that bends over to hold the shade.
The pole stands on the base and the arm ends on the knob of the shade: nothing crosses the r."""
import json, math, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

SX = 26.0; SB = 82.0; ST = 30.0

KC = (65.0, 22.6); KR = 2.6
kp = P(KC[0] + KR * math.cos(math.radians(225)), KC[1] + KR * math.sin(math.radians(225)))

# ---- 1: the r (one line: up the pole and over the arm) ----
r_ = [Seg((SX, SB), (SX, ST)), Seg((SX, ST), (SX, 18.0), (34.0, 12.0), (44.0, 12.0)), Seg((44.0, 12.0), (52.0, 12.0), (58.6, 15.4), kp)]

# ---- 2: the base ----
base = rrect(12.0, SB, 40.0, 90.0, 3.0)

# ---- 3: the shade and its knob ----
k0, k1 = P(KC[0] - KR, KC[1]), P(KC[0] + KR, KC[1])
shade = [Seg((52.0, 34.0), (52.0, 27.6), (56.0, 22.6), (61.6, 22.6)), Seg((61.6, 22.6), k0), Seg(k0, k1),
         Seg(k1, (68.4, 22.6)), Seg((68.4, 22.6), (74.0, 22.6), (78.0, 27.6), (78.0, 34.0)), Seg((78.0, 34.0), (52.0, 34.0))]
knob = arc(KC[0], KC[1], KR, KR, 180, 360, start=k0, end=k1)

# ---- 4: the bulb ----
BC = (65.0, 34.0); BR = 4.0
bulb = arc(BC[0], BC[1], BR, BR, 180, 0, start=P(61.0, 34.0), end=P(69.0, 34.0))

# ---- 5: an open book ----
pgL = Seg((45.0, 88.0), (45.0, 80.4), (55.0, 77.0), (66.0, 82.6))
pgR = Seg((66.0, 82.6), (77.0, 77.0), (87.0, 80.4), (87.0, 88.0))
spine = Seg((66.0, 82.6), (66.0, 88.0))
cover = rrect(43.0, 88.0, 89.0, 91.4, 1.4)

# ---- 6: the light ----
tL, tR = 0.16, 0.84
Lp = P(*pgL.at(tL)); Rp = P(*pgR.at(tR))
beamL = Seg((56.0, 34.0), Lp); beamR = Seg((74.0, 34.0), Rp)
_, pgL_b = pgL.split(tL)
pgR_a, _ = pgR.split(tR)

steps = [
    step('Start with an r', 'Draw a small letter r: a tall straight line, with its top bending over to the right like an arch. This r is hiding in the lamp.',
         [line(*r_)]),
    step('The base', 'Draw a box with round corners at the bottom of the r for the lamp to stand on.',
         [ring(*base)]),
    step('The shade', 'Draw a little round knob at the end of the arch. Draw a big round shade under it, flat at the bottom.',
         [ring(*shade), line(*knob)]),
    step('The bulb', 'Draw a round bulb peeping out under the shade.',
         [line(*bulb)]),
    step('A book', 'Draw an open book on the table: two curved pages and a line down the middle, on a long thin cover.',
         [line(pgL, pgR), line(spine), ring(*cover)]),
    step('The light', 'Draw two straight lines from the shade down to the book. This is the light shining on it.',
         [line(beamL), line(beamR)]),
    step('Colour the shade', 'Colour the shade green.',
         [fill(FILL['green'], *shade)], use='green'),
    step('Colour the light', 'Colour the bulb yellow. Colour the light shining down yellow too, very softly.',
         [fill(FILL['yellow'], *(bulb + [Seg((69.0, 34.0), (61.0, 34.0))])),
          fill('#fff1a8', *([beamL, pgL_b, pgR_a, beamR.rev(), Seg((74.0, 34.0), (69.0, 34.0))] + rev(bulb) + [Seg((61.0, 34.0), (56.0, 34.0))]))], use='yellow'),
    step('Colour the cover', 'Colour the cover of the book red.',
         [fill(FILL['red'], *cover)], use='red'),
    step('Colour grey', 'Colour the base and the knob grey.',
         [fill(FILL['grey'], *base), fill(FILL['grey'], *(knob + [Seg(k1, k0)]))], use='grey'),
]

D = drawing('dx_readinglamp_r', 'r is for reading lamp', 2, 12, 'things', ['Letters', 'Around the house'],
            'A reading lamp shining on an open book. The small letter r is hiding in it: its straight line is the pole and its arch is the arm that holds the shade.',
            steps, ['green', 'yellow', 'red', 'grey'])
json.dump(D, open(os.path.join(OUT, 'lamp.json'), 'w'))
json.dump({'set': 'house-az', 'slot': 'r', 'kind': 'key', 'age_from': 4}, open(os.path.join(OUT, 'lamp.place.json'), 'w'))
print('lamp: %d steps' % len(steps))
