"""R is for Rocking horse (Around the house A to Z, slot R). Side view, facing left.
The R: its straight line is the front leg, its bowl is the horse's body and its slanting leg is the back leg.
The head and neck sit on top of the R; both legs stand on the rocker. Nothing crosses the R."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

SX = 36.0; BT = 46.0; BBm = 62.0

# ---- the rocker's top edge (worked out first, so both legs end exactly on it) ----
rtop = Seg((12.0, 79.0), (34.0, 89.0), (66.0, 89.0), (88.0, 79.0))
def on_rocker(x):
    return P(*rtop.at(seg_line_cross_x(rtop, x)))
SBOT = on_rocker(SX)
LEG0 = (50.0, BBm); LEGX = 68.0
LEG1 = on_rocker(LEGX)

# ---- 1: the R ----
stick = Seg((SX, BT), SBOT)
bowl = [Seg((SX, BT), (64.0, BT)),
        Seg((64.0, BT), (72.5, BT), (76.0, 50.0), (76.0, 54.0)),
        Seg((76.0, 54.0), (76.0, 58.0), (72.5, BBm), (64.0, BBm)),
        Seg((64.0, BBm), (SX, BBm))]
leg = Seg(LEG0, LEG1)

# ---- 2: the rocker ----
rocker = [rtop,
          Seg((88.0, 79.0), (90.4, 77.9), (92.2, 81.2), (90.4, 82.8)),
          Seg((90.4, 82.8), (67.0, 93.6), (33.0, 93.6), (9.6, 82.8)),
          Seg((9.6, 82.8), (7.8, 81.2), (9.6, 77.9), (12.0, 79.0))]

# ---- 3: the head and neck ----
NB = (44.0, BT)
head = [Seg((SX, BT), (35.0, 40.0), (33.0, 33.0), (31.0, 28.0)),
        Seg((31.0, 28.0), (27.0, 28.6), (20.0, 30.0), (16.5, 29.6)),
        Seg((16.5, 29.6), (13.0, 29.2), (12.4, 24.2), (15.6, 22.6)),
        Seg((15.6, 22.6), (21.0, 19.6), (27.0, 16.6), (31.0, 13.6)),
        Seg((31.0, 13.6), (32.0, 10.2), (33.0, 8.2), (34.2, 8.2)),
        Seg((34.2, 8.2), (36.0, 8.2), (37.6, 11.0), (37.6, 14.0)),
        Seg((37.6, 14.0), (40.0, 22.0), (42.5, 34.0), NB)]

# ---- 4: the mane ----
MB = (48.0, BT)
mane = Seg((37.6, 14.0), (42.0, 16.4), (46.0, 30.0), MB)

# ---- 5: the eye ----
eye = circle(24.0, 22.8, 1.6)

# ---- 6: the saddle (hanging from the top of the body) ----
saddle = [Seg((62.0, BT), (62.0, 52.4)), Seg((62.0, 52.4), (62.0, 53.7), (61.1, 54.6), (59.8, 54.6)),
          Seg((59.8, 54.6), (52.2, 54.6)), Seg((52.2, 54.6), (50.9, 54.6), (50.0, 53.7), (50.0, 52.4)), Seg((50.0, 52.4), (50.0, BT))]

# ---- 7: the tail ----
rs1, rs2 = bowl[1], bowl[2]
ta = P(*rs1.at(0.55)); tb = P(*rs2.at(0.45))
_, rs1b = rs1.split(0.55)
rs2a, _ = rs2.split(0.45)
tail = [Seg(ta, (82.0, 47.0), (87.6, 52.0), (87.6, 61.0)),
        Seg((87.6, 61.0), (87.6, 65.0), (88.4, 68.0), (89.6, 70.4)),
        Seg((89.6, 70.4), (83.0, 68.6), (79.6, 63.0), tb)]
tail_base = [rs2a.rev(), rs1b.rev()]          # tb -> (76,54) -> ta

steps = [
    step('Start with an R', 'Draw a big capital R: a tall straight line, a round bowl at the top, and a slanting leg. This R is hiding in the rocking horse.',
         [line(stick), line(*bowl), line(leg)]),
    step('The rocker', 'Draw a long curved rocker under the R, with round ends. The two legs of the R stand on it.',
         [ring(*rocker)]),
    step('Head and neck', 'From the top of the R, draw up a long neck to a head with a long nose and a pointed ear. Come back down to the R.',
         [line(*head)]),
    step('The mane', 'Draw a line from the ear down to the top of the R, behind the neck. This is the mane.',
         [line(mane)]),
    step('The eye', 'Draw a small round eye on the head.',
         [ring(*eye)]),
    step('The saddle', 'Draw a saddle on the back: a little box hanging down from the top of the bowl.',
         [line(*saddle)]),
    step('The tail', 'Draw a long tail hanging from the back of the horse, with a pointed end.',
         [line(*tail)]),
    step('Colour light brown', 'Colour the horse light brown: the head, the neck and the body. Go round the eye and the saddle.',
         [fill(FILL['lbrown'], *(head + [Seg(NB, (SX, BT))]), cut=[d_fill(*eye)]),
          fill(FILL['lbrown'], *([Seg((SX, BT), (50.0, BT))] + rev(saddle) + [Seg((62.0, BT), (64.0, BT))] + bowl[1:3] + [bowl[3], Seg((SX, BBm), (SX, BT))]))], use='lbrown'),
    step('Colour brown', 'Colour the mane and the tail brown.',
         [fill(FILL['brown'], *([head[-1]] + [Seg(NB, MB)] + [mane.rev()])), fill(FILL['brown'], *(tail + tail_base))], use='brown'),
    step('Colour red', 'Colour the saddle and the rocker red.',
         [fill(FILL['red'], *(saddle + [Seg((50.0, BT), (62.0, BT))])), fill(FILL['red'], *rocker)], use='red'),
    step('Colour the eye', 'Colour the eye black.',
         [fill(FILL['black'], *eye)], use='black'),
]

D = drawing('dx_rockinghorse_r', 'R is for Rocking horse', 3, 15, 'things', ['Letters', 'Around the house'],
            'A wooden rocking horse with a red saddle and rocker. The capital R is hiding in it: its straight line is the front leg, its bowl is the body and its slanting leg is the back leg.',
            steps, ['lbrown', 'brown', 'red', 'black'])
json.dump(D, open(os.path.join(OUT, 'rockinghorse.json'), 'w'))
json.dump({'set': 'house-AZ', 'slot': 'R', 'kind': 'key', 'age_from': 5}, open(os.path.join(OUT, 'rockinghorse.place.json'), 'w'))
print('rocking horse: %d steps' % len(steps))
