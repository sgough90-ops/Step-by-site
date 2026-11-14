"""O is for Oven (Around the house A to Z, slot O).
The O: the round window in the oven door. Nothing touches it; the door goes round it and the bread sits inside it."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

X0, X1 = 23.0, 77.0
YT, YB = 38.0, 88.0
HT = 24.0
HX0, HX1 = 30.0, 70.0

OC = (50.0, 70.6); OR = 12.0
O_ = circle(OC[0], OC[1], OR)

door = rrect(28.5, 50, 71.5, 85.6, 3.0)

r = 3.0
front = [Seg((X0, YT), (X1, YT)), Seg((X1, YT), (X1, YB - r))] + arc(X1 - r, YB - r, r, r, 0, 90, start=P(X1, YB - r), end=P(X1 - r, YB)) + \
        [Seg((X1 - r, YB), (X0 + r, YB))] + arc(X0 + r, YB - r, r, r, 90, 180, start=P(X0 + r, YB), end=P(X0, YB - r)) + [Seg((X0, YB - r), (X0, YT))]

def foot(x0, x1, h=4.0, r=1.6):
    y1 = YB + h
    return [Seg((x0, YB), (x0, y1 - r))] + arc(x0 + r, y1 - r, r, r, 180, 90, start=P(x0, y1 - r), end=P(x0 + r, y1)) + \
           [Seg((x0 + r, y1), (x1 - r, y1))] + arc(x1 - r, y1 - r, r, r, 90, 0, start=P(x1 - r, y1), end=P(x1, y1 - r)) + [Seg((x1, y1 - r), (x1, YB))]
feet = [foot(28.5, 34.5), foot(65.5, 71.5)]

band = Seg((X0, 47), (X1, 47))
knobs = [circle(x, 42.5, 2.5) for x in (31.5, 43.8, 56.2, 68.5)]

handle = rrect(36.5, 52.3, 63.5, 55.5, 1.6)

hob = poly((X0, YT), (HX0, HT), (HX1, HT), (X1, YT))

rings = [circle(38, 33.4, 6.4, ry=2.3), circle(62, 33.4, 6.4, ry=2.3), circle(40.6, 27.6, 4.8, ry=1.7), circle(59.4, 27.6, 4.8, ry=1.7)]

PX0, PX1, PT = 54.5, 68.0, 15.8
pan = poly((PX0, HT), (PX0, PT), (PX1, PT), (PX1, HT))
ph = [Seg((PX0, 17.6), (45.6, 17.6)), Seg((45.6, 17.6), (44.1, 17.6), (44.1, 20.2), (45.6, 20.2)), Seg((45.6, 20.2), (PX0, 20.2))]
steam = [curve((58.6, 12.6), (56.9, 11.2), (60.3, 9.4), (58.6, 8.0), (57.6, 7.2), (57.6, 6.2), (58.6, 5.4)),
         curve((64.4, 12.6), (62.7, 11.2), (66.1, 9.4), (64.4, 8.0), (63.4, 7.2), (63.4, 6.2), (64.4, 5.4))]

loaf = [Seg((43.8, 77.2), (56.2, 77.2)),
        Seg((56.2, 77.2), (58.7, 77.2), (59.2, 73.8), (57.9, 71.2)),
        Seg((57.9, 71.2), (56.4, 68.0), (53.3, 66.3), (50, 66.3)),
        Seg((50, 66.3), (46.7, 66.3), (43.6, 68.0), (42.1, 71.2)),
        Seg((42.1, 71.2), (40.8, 73.8), (41.3, 77.2), (43.8, 77.2))]
slash = [Seg((46.3, 70.0), (48.1, 72.5)), Seg((51.9, 70.0), (53.7, 72.5))]

steps = [
    step('Start with an O', 'Draw a round capital O, a little below the middle of your paper. This O is hiding in the oven.',
         [ring(*O_)]),
    step('The door', 'Draw a box with round corners around the O. Leave more room above the O than below it.',
         [ring(*door)]),
    step('The oven', 'Draw a bigger box around the door. Leave lots of room at the top for the knobs.',
         [ring(*front)]),
    step('The feet', 'Draw two little feet under the oven.',
         [line(*f) for f in feet]),
    step('The knobs', 'Draw a line across the oven, just above the door. Then draw four round knobs in a row above the line.',
         [line(band)] + [ring(*k) for k in knobs]),
    step('The handle', 'Draw a long thin handle across the top of the door.',
         [ring(*handle)]),
    step('The top', 'From each top corner of the oven, draw a sloping line going up and in. Join the two lines with a line across.',
         [line(*hob)]),
    step('The rings', 'Draw four flat ovals on the top: two big ones at the front and two smaller ones behind them.',
         [ring(*c) for c in rings]),
    step('A pan', 'Draw a pan standing on the back of the top. Give it a long handle. Add two wavy lines of steam above it.',
         [line(*pan), line(*ph), line(*steam[0]), line(*steam[1])]),
    step('The bread', 'Draw a loaf of bread inside the O: a flat bottom with a round hill on top. Add two little lines on the loaf.',
         [ring(*loaf), line(slash[0]), line(slash[1])]),
    step('Colour black', 'Colour the inside of the O black, round the bread. Colour the four rings, the handle and the two feet black too.',
         [fill(FILL['black'], *O_, cut=[d_fill(*loaf)])] + [fill(FILL['black'], *c) for c in rings] + [fill(FILL['black'], *handle)] +
         [fill(FILL['black'], *(f + [Seg(f[-1].b, f[0].a)])) for f in feet], use='black'),
    step('Colour the bread', 'Colour the loaf of bread light brown.',
         [fill(FILL['lbrown'], *loaf)], use='lbrown'),
    step('Colour the door', 'Colour the door grey. Go round the O and round the handle.',
         [fill(FILL['grey'], *door, cut=[d_fill(*O_), d_fill(*handle)])], use='grey'),
    step('Colour red', 'Colour the pan and its handle red. Colour the four knobs red too.',
         [fill(FILL['red'], *(pan + [Seg((PX1, HT), (PX0, HT))])), fill(FILL['red'], *(ph + [Seg((PX0, 20.2), (PX0, 17.6))]))] +
         [fill(FILL['red'], *k) for k in knobs], use='red'),
]

D = drawing('dx_oven_o', 'O is for Oven', 3, 15, 'things', ['Letters', 'Around the house'],
            'An oven with bread baking inside and a pan on top. The capital O is hiding in it: the O is the round window in the oven door.',
            steps, ['black', 'lbrown', 'grey', 'red'])
json.dump(D, open(os.path.join(OUT, 'oven.json'), 'w'))
json.dump({'set': 'house-AZ', 'slot': 'O', 'kind': 'key', 'age_from': 5}, open(os.path.join(OUT, 'oven.place.json'), 'w'))
print('oven: %d steps' % len(steps))
