"""p is for pear (Around the house a to z, slot p).
The p: its straight line is the pear's stalk (one line, as written) and its bowl is the leaf.
The stalk ends on the top of the pear: nothing crosses the p."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

SX = 50.0; ST = 10.0; SB = 40.0; LB = 27.0

# ---- 1: the p ----
stick = Seg((SX, ST), (SX, SB))
bowl = [Seg((SX, ST), (SX + 9, ST), (SX + 16.5, 12.6), (SX + 20, 18.5)),
        Seg((SX + 20, 18.5), (SX + 16.5, 24.4), (SX + 9, LB), (SX, LB))]

# ---- 2: the pear ----
half = [Seg((SX, SB), (55.6, SB), (58.6, 43.6), (59.6, 49.6)),
        Seg((59.6, 49.6), (60.8, 56.6), (69.0, 60.6), (69.0, 72.0)),
        Seg((69.0, 72.0), (69.0, 84.6), (60.6, 91.0), (SX, 91.0))]
pear = half + rev(mirror(half))

# ---- 3: a line down the middle of the leaf ----
vein = Seg((SX, 18.5), (56.0, 17.4), (62.0, 17.4), (66.0, 18.5))

# ---- 4: a shine ----
shine = [Seg((38.0, 70.0), (36.6, 76.0), (38.6, 82.2), (43.6, 84.8))]

steps = [
    step('Start with a p', 'Draw a small letter p: a straight line down, then a round bowl at the top. This p is hiding in the pear.',
         [line(stick), line(*bowl)]),
    step('The pear', 'From the bottom of the p, draw a pear: narrow at the top and big and round at the bottom.',
         [ring(*pear)]),
    step('The leaf', 'The bowl of the p is a leaf. Draw a curved line along the middle of it.',
         [line(vein)]),
    step('The shine', 'Draw a little curved line near the bottom of the pear, to make it shine.',
         [line(*shine)]),
    step('Colour the leaf', 'Colour the leaf green.',
         [fill(FILL['green'], *(bowl + [Seg((SX, LB), (SX, ST))]))], use='green'),
    step('Colour the pear', 'Colour the pear yellow. You can colour over the shine line, it will still show.',
         [fill(FILL['yellow'], *pear)], use='yellow'),
]

D = drawing('dx_pear_p', 'p is for pear', 1, 6, 'things', ['Letters', 'Around the house'],
            'A juicy pear with a green leaf. The small letter p is hiding in it: its straight line is the stalk and its round bowl is the leaf.',
            steps, ['green', 'yellow'])
json.dump(D, open(os.path.join(OUT, 'pear.json'), 'w'))
json.dump({'set': 'house-az', 'slot': 'p', 'kind': 'key', 'age_from': 3}, open(os.path.join(OUT, 'pear.place.json'), 'w'))
print('pear: %d steps' % len(steps))
