"""M is for Monster truck (Vehicles A to Z, slot M). Front view.
The M: its two tall lines are the inside edges of the two giant tyres; its V is the pointed bottom of the truck."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

XL, XR = 33.0, 67.0
YT, YB = 47.0, 87.0
VX, VY = 50.0, 72.0

M_ = poly((XL, YB), (XL, YT), (VX, VY), (XR, YT), (XR, YB))

side_a, side_b = (26.6, 43.2), (34.9, 21.4)
ux, uy = (side_b[0] - side_a[0]), (side_b[1] - side_a[1]); L_ = (ux * ux + uy * uy) ** .5; ux, uy = ux / L_, uy / L_
left = [Seg((XL, YT), (29.6, YT)),
        Seg((29.6, YT), (27.4, YT), (side_a[0] - 2.2 * ux, side_a[1] - 2.2 * uy), side_a),
        Seg(side_a, side_b),
        Seg(side_b, (side_b[0] + 1.9 * ux, side_b[1] + 1.9 * uy), (36.4, 18.5), (38.2, 18.5)),
        Seg((38.2, 18.5), (50, 18.5))]
cab = left + rev(mirror(left))
ROOF = 18.5

screen = rrect(38.5, 23, 61.5, 33.5, 2.2)
shine1 = Seg((42.2, 30.6), (45.2, 25.8))
shine2 = Seg((45.6, 30.6), (47.4, 27.7))

def light(x0, x1, h=5.0, r=1.7):
    y0 = ROOF - h
    return [Seg((x0, ROOF), (x0, y0 + r))] + arc(x0 + r, y0 + r, r, r, 180, 270, start=P(x0, y0 + r), end=P(x0 + r, y0)) + \
           [Seg((x0 + r, y0), (x1 - r, y0))] + arc(x1 - r, y0 + r, r, r, 270, 360, start=P(x1 - r, y0), end=P(x1, y0 + r)) + \
           [Seg((x1, y0 + r), (x1, ROOF))]
lights = [light(39.6, 45.6), light(47, 53), light(54.4, 60.4)]

hl = [circle(34.2, 39.6, 3.0), circle(65.8, 39.6, 3.0)]
grille = rrect(43.5, 37.6, 56.5, 43.2, 1.6)

TY = 51.0
tyreL = [Seg((XL, TY), (19.5, TY))] + arc(19.5, TY + 5.5, 5.5, 5.5, 270, 180, start=P(19.5, TY), end=P(14, TY + 5.5)) + \
        [Seg((14, TY + 5.5), (14, YB - 5.5))] + arc(19.5, YB - 5.5, 5.5, 5.5, 180, 90, start=P(14, YB - 5.5), end=P(19.5, YB)) + \
        [Seg((19.5, YB), (XL, YB))]
tyreR = mirror(tyreL)

treadL = [Seg((18.8, y), (28.4, y)) for y in (60.0, 69.0, 78.0)]
treadR = [mirror([s])[0] for s in treadL]

steps = [
    step('Start with an M', 'Draw a big capital M: two tall straight lines, with a V between their tops. This M is hiding in the truck.',
         [line(*M_)]),
    step('The cab', 'Start at the top of the M on the left. Go out a little, up a sloping side, along the flat roof and down the other side to the top of the M again.',
         [line(*cab)]),
    step('The windscreen', 'Draw a wide window near the top of the cab, with round corners. Add two little slanting lines in it for the shine.',
         [ring(*screen), line(shine1), line(shine2)]),
    step('Lights on the roof', 'Draw three little lights in a row on top of the roof.',
         [line(*l) for l in lights]),
    step('The headlights', 'Draw a round headlight in each bottom corner of the cab.',
         [ring(*c) for c in hl]),
    step('The grille', 'Draw a small box with round corners between the two headlights.',
         [ring(*grille)]),
    step('Giant tyres', 'Draw a giant tyre on the outside of each tall line of the M. Start just under the cab. Go out, down and back in to the bottom of the line.',
         [line(*tyreL), line(*tyreR)]),
    step('The tread', 'Draw three short lines across each tyre.',
         [line(s) for s in treadL + treadR]),
    step('Colour red', 'Colour the truck red, down to the point of the V. Go round the windscreen, the headlights and the grille.',
         [fill(FILL['red'], *(cab + [Seg((XR, YT), (VX, VY)), Seg((VX, VY), (XL, YT))]),
               cut=[d_fill(*screen), d_fill(*hl[0]), d_fill(*hl[1]), d_fill(*grille)])], use='red'),
    step('Colour the windscreen', 'Colour the windscreen light blue.',
         [fill(FILL['lblue'], *screen)], use='lblue'),
    step('Colour yellow', 'Colour the three lights on the roof yellow. Colour the two headlights yellow too.',
         [fill(FILL['yellow'], *(l + [Seg(l[-1].b, l[0].a)])) for l in lights] + [fill(FILL['yellow'], *c) for c in hl], use='yellow'),
    step('Colour black', 'Colour the two giant tyres black. Colour the grille black too.',
         [fill(FILL['black'], *(tyreL + [Seg((XL, YB), (XL, TY))])), fill(FILL['black'], *(tyreR + [Seg((XR, YB), (XR, TY))])),
          fill(FILL['black'], *grille)], use='black'),
]

D = drawing('dx_monstertruck_m', 'M is for Monster truck', 2, 12, 'vehicles', ['Letters', 'Vehicles'],
            'A monster truck seen from the front, with giant tyres. The capital M is hiding in it: its two tall lines are the inside edges of the tyres and its V is the pointed bottom of the truck.',
            steps, ['red', 'lblue', 'yellow', 'black'])
json.dump(D, open(os.path.join(OUT, 'truck.json'), 'w'))
json.dump({'set': 'vehicles-AZ', 'slot': 'M', 'kind': 'drive', 'age_from': 5}, open(os.path.join(OUT, 'truck.place.json'), 'w'))
print('truck: %d steps' % len(steps))
