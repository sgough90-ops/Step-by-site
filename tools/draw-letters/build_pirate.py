"""P is for Pirate ship (Vehicles A to Z, slot P). Side view.
The P: its stick is the mast (one line, as written) and its bowl is the sail. The mast stands on the deck.
Nothing crosses the P: the skull sits inside the sail, the cabin and flag are beside the mast."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

MX = 52.0; MT = 10.0; DECK = 64.0

# ---- 1: the P ----
stick = Seg((MX, DECK), (MX, MT))
bowl = [Seg((MX, MT), (MX + 13, MT), (MX + 27, 15.5), (MX + 27, 27.5)),
        Seg((MX + 27, 27.5), (MX + 27, 39.5), (MX + 13, 45.0), (MX, 45.0))]

# ---- 2: the hull ----
hull = [Seg((12.0, DECK), (90.0, DECK)),
        Seg((90.0, DECK), (86.0, 74.0), (81.0, 83.0), (73.0, 83.0)),
        Seg((73.0, 83.0), (27.0, 83.0)),
        Seg((27.0, 83.0), (21.0, 83.0), (16.0, 76.0), (12.0, DECK))]

# ---- 3: the cabin (three sides standing on the deck) ----
cab = poly((24.0, DECK), (24.0, 55.0), (41.0, 55.0), (41.0, DECK))

# ---- 4: three round windows ----
ports = [circle(x, 72.5, 3.0) for x in (34.0, 52.0, 70.0)]

# ---- 5: a little flag on the cabin ----
pole = Seg((30.0, 55.0), (30.0, 41.0))
flag = [Seg((30.0, 42.0), (33.0, 40.6), (36.0, 43.4), (40.0, 42.0)), Seg((40.0, 42.0), (40.0, 48.0)),
        Seg((40.0, 48.0), (36.0, 49.4), (33.0, 46.6), (30.0, 48.0))]

# ---- 6: the skull in the sail ----
SC = (66.0, 25.5); SR = 7.0
import math
def at(a): return P(SC[0] + SR * math.cos(math.radians(a)), SC[1] + SR * math.sin(math.radians(a)))
ja, jb = at(140), at(40)
JB = 36.0
skull = arc(SC[0], SC[1], SR, SR, 140, 400, start=ja, end=jb) + \
        [Seg(jb, (69.4, 32.6)), Seg((69.4, 32.6), (69.4, JB - 1.4)),
         Seg((69.4, JB - 1.4), (69.4, JB - 0.4), (68.6, JB), (67.6, JB)), Seg((67.6, JB), (64.4, JB)),
         Seg((64.4, JB), (63.4, JB), (62.6, JB - 0.4), (62.6, JB - 1.4)), Seg((62.6, JB - 1.4), (62.6, 32.6)), Seg((62.6, 32.6), ja)]
teeth = [Seg((64.8, JB), (64.8, 33.4)), Seg((67.2, JB), (67.2, 33.4))]

# ---- 7: eyes and nose ----
eyeL = circle(63.3, 25.6, 2.0); eyeR = circle(68.7, 25.6, 2.0)
nose = poly((66.0, 28.6), (67.2, 30.8), (64.8, 30.8), closed=True)

# ---- 8: the sea: two wavy lines, each one starts at the side of the ship ----
WY = 79.0
def side_x(seg, y):
    return P(*seg.at(seg_line_cross_y(seg, y)))
wl = side_x(hull[3], WY); wr = side_x(hull[1], WY)
waveL = curve((5.0, WY), (7.5, WY - 2.4), (10.0, WY - 2.4), (12.5, WY), (14.0, WY + 1.4), (15.0, WY + 0.8), wl)
waveR = curve(wr, (88.5, WY + 1.4), (90.5, WY + 1.4), (92.0, WY), (93.5, WY - 1.6), (95.0, WY - 1.6), (96.0, WY - 0.6))
seaB = curve((8.0, 89.0), (14.0, 86.6), (20.0, 86.6), (26.0, 89.0), (32.0, 91.4), (38.0, 91.4), (44.0, 89.0),
             (50.0, 86.6), (56.0, 86.6), (62.0, 89.0), (68.0, 91.4), (74.0, 91.4), (80.0, 89.0), (86.0, 86.6), (90.0, 86.6), (93.0, 88.0))

steps = [
    step('Start with a P', 'Draw a big capital P: a tall straight line, with a round bowl at the top. This P is hiding in the pirate ship.',
         [line(stick, *bowl)]),
    step('The ship', 'Draw a long line across the bottom of the P. Then draw the bottom of the ship under it, round at the ends.',
         [ring(*hull)]),
    step('The cabin', 'Draw a box standing on the deck, on the left of the mast.',
         [line(*cab)]),
    step('Round windows', 'Draw three round windows in a row along the side of the ship.',
         [ring(*c) for c in ports]),
    step('A little flag', 'Draw a pole on top of the cabin. Put a little wavy flag on it.',
         [line(pole), line(*flag)]),
    step('A skull', 'Draw a skull in the sail: a round head with a square chin. Draw two little lines in the chin for teeth.',
         [ring(*skull)] + [line(t) for t in teeth]),
    step('Eyes and nose', 'Draw two round eyes in the skull, and a little triangle for the nose.',
         [ring(*eyeL), ring(*eyeR), ring(*nose)]),
    step('The sea', 'Draw a wavy line on each side of the ship, where it sits in the water. Draw one more wavy line under the ship.',
         [line(*waveL), line(*waveR), line(*seaB)]),
    step('Colour black', 'Colour the sail black, round the skull. Colour the little flag, the eyes and the nose black too.',
         [fill(FILL['black'], *([stick.rev()] if False else []), *(bowl + [Seg((MX, 45.0), (MX, MT))]), cut=[d_fill(*skull)]),
          fill(FILL['black'], *(flag + [Seg((30.0, 48.0), (30.0, 42.0))])),
          fill(FILL['black'], *eyeL), fill(FILL['black'], *eyeR), fill(FILL['black'], *nose)], use='black'),
    step('Colour the ship', 'Colour the ship brown. Go round the three windows.',
         [fill(FILL['brown'], *hull, cut=[d_fill(*c) for c in ports])], use='brown'),
    step('Colour the cabin', 'Colour the cabin light brown.',
         [fill(FILL['lbrown'], *close(cab))], use='lbrown'),
    step('Colour the windows', 'Colour the three windows yellow, like lights shining inside.',
         [fill(FILL['yellow'], *c) for c in ports], use='yellow'),
]

D = drawing('dx_pirateship_p', 'P is for Pirate ship', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A pirate ship with a black sail and a skull. The capital P is hiding in it: its straight line is the mast and its round bowl is the sail.',
            steps, ['black', 'brown', 'lbrown', 'yellow'])
json.dump(D, open(os.path.join(OUT, 'pirate.json'), 'w'))
json.dump([d_fill(*skull)], open(os.path.join(OUT, 'pirate.white.json'), 'w'))
json.dump({'set': 'vehicles-AZ', 'slot': 'P', 'kind': 'sail', 'age_from': 5}, open(os.path.join(OUT, 'pirate.place.json'), 'w'))
print('pirate: %d steps' % len(steps))
