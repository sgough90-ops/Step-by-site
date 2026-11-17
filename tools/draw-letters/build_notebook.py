"""N is for Notebook (dx_notebook_n), Around the house A to Z, slot N. Built from Claude's sketch "Notebook 1" (16 Nov 2026).
The N is the two long sides of the cover and the stretchy band that goes from corner to corner."""
from kit15 import *
import json, os

BLUE, RED = FILL['blue'], FILL['red']
XL, XR, YT, YB = 27, 73, 12, 84
n_l, n_d, n_r = Seg((XL, YB), (XL, YT)), Seg((XL, YT), (XR, YB)), Seg((XR, YB), (XR, YT))
top, bot = Seg((XL, YT), (XR, YT)), Seg((XL, YB), (XR, YB))

label = rrect(48, 20, 68, 31, 2)
lines_ = [Seg((51.5, 24), (64.5, 24)), Seg((51.5, 27.4), (61.5, 27.4))]

RL, RR, RB, RV = 50.5, 56.5, 93, 90
ribbon = poly((RL, YB), (RL, RB), ((RL + RR) / 2, RV), (RR, RB), (RR, YB))
PY = 86.8
pages_l = poly((28.5, YB), (28.5, PY), (RL, PY))
pages_r = poly((RR, PY), (71.5, PY), (71.5, YB))

steps = [
    step('Start with an N', 'Draw a big capital N: a tall line up, a slanting line down to the right, and a tall line back up.', [line(n_l, n_d, n_r)]),
    step('The cover', 'Draw a line across the top and a line across the bottom to finish the cover.', [line(top), line(bot)]),
    step('The label', 'Draw a small box with round corners near the top right.', [ring(*label)]),
    step('The lines', 'Draw two short lines inside the label.', [line(l) for l in lines_]),
    step('The bookmark', 'Draw a ribbon hanging down from the bottom, with a V cut in its end.', [line(*ribbon)]),
    step('The pages', 'Draw a thin strip of pages under the cover, on each side of the ribbon.', [line(*pages_l), line(*pages_r)]),
]
tri_lo = fill(BLUE, n_l, n_d, bot.rev())
tri_hi = fill(BLUE, top, n_r.rev(), n_d.rev(), cut=[d_fill(*label)])
steps += [
    step('Colour blue', 'Colour the cover blue. Leave the label white.', [tri_lo, tri_hi], use='blue'),
    step('Colour red', 'Colour the ribbon red.', [fill(RED, *ribbon, Seg((RR, YB), (RL, YB)))], use='red'),
]
P_ = drawing('dx_notebook_n', 'N is for Notebook', 1, 8, 'things', ['Letters', 'Around the house'],
             'A blue notebook with a stretchy band across it and a red ribbon bookmark. The capital N is hiding in it: '
             'the two sides of the cover are the tall lines, and the band from corner to corner is the slanting line.',
             steps, ['blue', 'red'])
save('notebook', P_, {'set': 'house-AZ', 'slot': 'N', 'kind': 'key', 'age_from': 4})
HERE = os.path.dirname(os.path.abspath(__file__))
json.dump([d_fill(*label)], open(os.path.join(HERE, 'out', 'notebook.white.json'), 'w'))
