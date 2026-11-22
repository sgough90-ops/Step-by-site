"""Y is for Yacht (dx_yacht_y), Vehicles A to Z, slot Y (22 Nov 2026).
From his pick "Y1 Sleek yacht, open top deck" (Claude's sketches, claude/step-by-draw-vehicles-capitals-round2.md).

A motor yacht, bow to the left, with an open top deck under a sun roof. The Y is the forked post that holds the roof
up. In the sketch the post was a bare black Y; here it is a thin yellow post and the Y is one edge of each of its
three arms (his rule from the food letters: a letter line on a pole is the edge of a thin coloured band).
Written in the sketch's numbers; the Pic moves it onto the paper.

    python3 build_yacht.py
"""
import math
from vkit import *

YX, YTOP, YJ, YBOT, HALF, TH = 61.6, 21.4, 30.6, 40.2, 9.2, 2.0    # the Y: stem, top, joint, foot, half its width; how thick the post is
p = Pic(s=0.95, dx=1.9, dy=2.43)
K = 11 / (64 - 45 - 1.6)                              # the lean of the cabin's front

# ---- behind: the rail on the front deck, the flag pole ----
rail_y = lambda x: 49.4 + (x - 5.6) * 0.21
p.stroke('rail', Seg((5.6, rail_y(5.6)), (31, rail_y(31))), step=7)
for i, x in enumerate((8, 15, 22)):
    p.stroke('rpost%d' % i, Seg((x, rail_y(x)), (x, 61)), step=7)
p.stroke('pole', Seg((92.6, 50.6), (92.6, 64.5)), step=7)
p.stroke('flag', poly((92.6, 50.6), (99.2, 52.6), (92.6, 54.6)), step=7)

# ---- the open top deck: windscreen, seat, low wall ----
p.shape('screen', poly((43.76, 41.6), (49.2, 31.4), (53.2, 31.4), (49.57, 41.6), closed=True), step=4)
p.shape('seat', one("M69.6,41.6 L69.6,36.7 Q69.6,35 71.3,35 L77.9,35 Q79.6,35 79.6,36.7 L79.6,41.6 Z"), step=4)
p.shape('wall', poly((40.4, 46.5), (43, YBOT), (80.6, YBOT), (81.9, 46.5), closed=True), step=4)

# ---- the sun roof, its dome and aerial ----
p.shape('roof', one(f"M49.4,{YTOP} Q44.6,{YTOP} 46.2,19.2 Q47.6,17.6 50.6,17.6 L79.4,17.6 Q84.6,17.6 84.6,{YTOP} Z"), step=3)
p.stroke('dome', arc(58, 17.6, 3.2, 3.05, 180, 360, start=P(54.8, 17.6), end=P(61.2, 17.6)), step=3)
p.stroke('aerial', Seg((74, 17.6), (74, 10.6)), step=3)

# ---- the cabin and its long window ----
p.shape('cabin', one("M23,64 L34,46.6 Q34.9,45 37,45 L83.6,45 Q85.6,45 86,47 L89,64 Z"), step=5)
G0, G1 = 48.5, 57.0
p.shape('glass', poly((27.2 + (64 - G1) * K, G1), (27.2 + (64 - G0) * K, G0), (83.8, G0), (84.6, G1), closed=True), step=5)
for i, px in enumerate((47, 59, 71)):
    p.stroke('bar%d' % i, Seg((px, G0), (px - (G1 - G0) * K, G1)), step=5, deco=True)

# ---- the boat, its stripe, the sea ----
p.shape('hull', one("M2,53 C22,58.5 60,62 96.5,62.5 L94.6,85 L27,85 C16,78 7,66 2,53 Z"), step=6)
p.stroke('stripe', one("M0.5,56.5 C22,62.6 60,66 98.6,66.65"), step=6)
p.shape('sea', blob(5, 96, 81.4, 7.6), step=8)

# ---- the Y and the rest of its post (in front of everything, nothing hides them) ----
r2 = TH * math.sqrt(2)
p.stroke('Y1', poly((YX - HALF, YTOP), (YX, YJ), (YX + HALF, YTOP)), step=1)
p.stroke('Y2', Seg((YX, YJ), (YX, YBOT)), step=1)
# the far edge of the right arm, carried on down the far side of the stem
p.stroke('post_r', poly((YX + YJ + r2 - YTOP, YTOP), (YX + TH, YX + YJ + r2 - (YX + TH)), (YX + TH, YBOT)), step=2)
# the far edge of the left arm: it ends on the right arm
xm = ((YX + YJ) + (YX - YJ + r2)) / 2
p.stroke('post_l', Seg((YX - YJ + r2 + YTOP, YTOP), (xm, YX + YJ - xm)), step=2)

p.build(keep=[(n, 'sea') for n in ('stripe',)])
p.net.keep_in('stripe', 'hull')

dots3 = [dot(*p.pt(x, 71.4), w=3.0, upright=False) for x in (30, 37.5, 45)]
steps = [
    step('Start with a Y', 'Draw a capital Y: a V shape first, then a straight line down from its point. This Y is hiding on top of the yacht.', p.step(1)),
    step('The post', 'Make the Y into a thick post. Draw a line close beside its right arm and on down beside its stem. Draw one more beside its left arm, inside the V.', p.step(2)),
    step('The sun roof', 'Draw a long thin roof with round ends across the two tops of the Y. Add a little dome and a thin aerial on top.', p.step(3)),
    step('The top deck', "Draw a long low wall that touches the foot of the Y. Above it, draw a sloping windscreen on the left and a seat with round corners on the right.", p.step(4)),
    step('The cabin', 'Under the wall, draw the cabin: a flat roof, a long sloping front and a steep back. Draw a long window in it with three slanted bars.', p.step(5)),
    step('The boat', 'Draw a long line from a point on the left, under the cabin, to the back. Go down at the back. Curve down and in from the point. Add a stripe and three dots.',
         p.step(6) + dots3),
    step('Rail and flag', 'On the front deck, draw a sloping rail on three short posts. At the back, draw a little flag on a pole.', p.step(7)),
    step('The sea', 'Draw a long wavy line across the bottom of the boat. Carry it round underneath to make a puddle of sea.', p.step(8)),
    step('Colour yellow', 'Colour the boat below the stripe yellow. Colour the sun roof and the thick post yellow too.',
         [p.face('yellow', (60, 74)), p.ring('yellow', 'roof'), p.face('yellow', (YX + TH / 2, 36)), p.face('yellow', (57.7, 25.3))], use='yellow'),
    step('Colour blue', 'Colour the long cabin window and the windscreen blue.', [p.ring('blue', 'glass'), p.face('blue', (48.6, 36))], use='blue'),
    step('Colour red', 'Colour the seat and the little flag red.', [p.face('red', (74.6, 38)), p.face('red', (94.6, 52.6))], use='red'),
    step('Colour light blue', 'Colour the sea light blue. Leave the cabin, the low wall and the stripe white.', [p.ring('lblue', 'sea')], use='lblue'),
]

D = drawing('dx_yacht_y', 'Y is for Yacht', 3, 18, 'vehicles', ['Letters', 'Vehicles'],
            'A yellow yacht with a long cabin window, an open top deck and a sun roof. The capital Y is hiding on top: '
            'it is the forked post that holds up the roof.',
            steps, ['yellow', 'blue', 'red', 'lblue'])
save('yacht', D, {'set': 'vehicles-AZ', 'slot': 'Y', 'kind': 'sail', 'age_from': 5})
save_white('yacht', p.white)
if __name__ == '__main__':
    preview(D, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'yacht-look.png'))
