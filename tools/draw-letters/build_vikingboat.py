"""V is for Viking boat (dx_vikingboat_v), Vehicles A to Z, slot V (22 Nov 2026).
From his pick "V1 Pointed stripe on the sail" (Claude's sketches, claude/step-by-draw-vehicles-capitals-round2.md).

A Viking longship from the side, dragon head to the right, five round shields along its side. The V is the two edges
of the red pointed stripe in the middle of the sail (a pattern on the sail: he was told and picked it).
The mast ends behind the sail, so no line runs down from the V's point (that would read as a Y).

    python3 build_vikingboat.py
"""
from vkit import *

TOPY, PTY = 20.0, 57.5                             # the top of the V (the bottom edge of the pole) and its point
VX0, VXM, VX1 = 35.5, 50.0, 64.5
TIPY = 62.5                                        # the two ends of the boat
p = Pic(s=1.0, dx=-1.5, dy=0.0)


def gun_y(x):
    t = (x - 14) / 72.0
    return TIPY + 21 * t * (1 - t)


# ---- the mast top, flag, pole and sail ----
p.shape('stub', box(48.4, 10.4, 51.6, 18.2), step=4)
p.stroke('flag', poly((51.6, 11.0), (59.4, 13.2), (51.6, 15.4)), step=4)
p.shape('yard', rrect(26.5, 16.6, 73.5, TOPY, 1.4), step=2)
p.stroke('sail_l', poly((29.5, TOPY), (29.5, PTY), (VXM, PTY)), step=3)
p.stroke('sail_r', poly((70.5, TOPY), (70.5, PTY), (VXM, PTY)), step=3)
p.stroke('V', poly((VX0, TOPY), (VXM, PTY), (VX1, TOPY)), step=1)

# ---- the two posts (behind the boat, the head and the curl) ----
back = [*curve((14, TIPY), (10, 57.5), (8.8, 51), (8.6, 43.6)), Seg((8.6, 43.6), (12.4, 43.6)),
        *curve((12.4, 43.6), (12.6, 52), (13.8, 60), (19.5, 66)), Seg((19.5, 66), (14, TIPY))]
front = [*curve((86, TIPY), (90, 57.5), (91, 51), (89.0, 44.8)), Seg((89.0, 44.8), (86.0, 44.6)),
         *curve((86.0, 44.6), (86.6, 52), (85.6, 60), (80.5, 66)), Seg((80.5, 66), (86, TIPY))]
p.shape('post_b', back, step=7)
p.shape('post_f', front, step=7)

# ---- the boat ----
hull = one(f"M14,{TIPY} C31,{TIPY + 7} 69,{TIPY + 7} 86,{TIPY} C83,80.5 68,88.5 50,88.5 C32,88.5 17,80.5 14,{TIPY} Z")
p.shape('hull', hull, step=6)
p.stroke('plank', one("M18.2,71.6 C33,77.6 67,77.6 81.8,71.6"), step=6, deco=True)
SH = [(x, gun_y(x) - 1.4) for x in (30, 40, 50, 60, 70)]
for i, (x, y) in enumerate(SH):
    p.shape('shield%d' % i, ell(x, y, 4.3), step=5)

# ---- the tail curl and the dragon's head ----
p.shape('curl', ell(10.3, 41.2, 3.9), step=8)
p.shape('head', one("M85.2,45.6 C83.4,39.5 86.2,34.4 91,34.4 C95,34.4 98.2,36.4 98.5,39.2 C98.7,41.2 96.8,42.3 94.8,42.3 L92.4,43 C91.8,44.6 90.6,45.8 89.2,46 Z"), step=8)
p.stroke('mouth', one("M96.9,40.3 Q95,41.1 93.1,40.3"), step=8, deco=True)

p.shape('sea', blob(7, 94, 84.6, 8.0), step=9)
p.build()

dots5 = [dot(*p.pt(x, y), w=2.6) for x, y in SH]
steps = [
    step('Start with a V', 'Draw a big capital V in the middle of your paper. This V is hiding in the sail of the boat.', p.step(1)),
    step('The pole', 'Draw a long thin pole across the top of the V, with round ends. Its bottom edge touches the two tops of the V.', p.step(2)),
    step('The sail', 'From the pole, draw a line down on each side of the V. Join each one along the bottom to the point of the V.', p.step(3)),
    step('Mast and flag', 'On top of the pole, in the middle, draw a little box for the top of the mast. Add a pointed flag.', p.step(4)),
    step('Five shields', 'Under the sail, draw five round shields in a row that dips in the middle. Put a dot in the middle of each one.', p.step(5) + dots5),
    step('The boat', 'Join the shields with a curved line that goes a little past each end. Curve down and in at both ends. Add a curved line along the side.', p.step(6)),
    step('The two posts', 'From each end of the boat, draw a tall thick post that curves up: a neck at the front and a tail at the back.', p.step(7)),
    step('Dragon head and tail', "On the front post, draw a dragon's head with a long nose, an eye, a nostril and a smile. On the back post, draw a circle with a dot.",
         p.step(8) + [dot(*p.pt(90.4, 38.5), w=2.6), dot(*p.pt(96.5, 38.7), w=1.6), dot(*p.pt(10.3, 41.2), w=2.2)]),
    step('The sea', 'Draw a long wavy line across the bottom of the boat. Carry it round underneath to make a puddle of sea.', p.step(9)),
    step('Colour brown', 'Colour the boat, the two posts, the pole and the top of the mast brown. Leave the shields.',
         [p.face('brown', (50, 80)), p.face('brown', (11.7, 54.5)), p.face('brown', (87.6, 54.8)), p.ring('brown', 'yard'), p.face('brown', (50, 13.5))], use='brown'),
    step('Colour red', 'Colour the pointed stripe inside the V red. Colour the flag and the first, third and fifth shields red too.',
         [p.face('red', (50, 35)), p.face('red', (53.5, 13.2))] + [p.ring('red', 'shield%d' % i) for i in (0, 2, 4)], use='red'),
    step('Colour yellow', "Colour the dragon's head, the circle on the tail and the other two shields yellow.",
         [p.ring('yellow', 'head'), p.ring('yellow', 'curl')] + [p.ring('yellow', 'shield%d' % i) for i in (1, 3)], use='yellow'),
    step('Colour blue', 'Colour the sea blue. Leave the two sides of the sail white.', [p.ring('blue', 'sea')], use='blue'),
]

D = drawing('dx_vikingboat_v', 'V is for Viking boat', 3, 18, 'vehicles', ['Letters', 'Vehicles'],
            "A Viking boat with a dragon's head, five round shields and a big striped sail. The capital V is hiding in the sail: "
            'it is the two edges of the red pointed stripe.',
            steps, ['brown', 'red', 'yellow', 'blue'])
save('vikingboat', D, {'set': 'vehicles-AZ', 'slot': 'V', 'kind': 'sail', 'age_from': 5})
save_white('vikingboat', p.white)
if __name__ == '__main__':
    preview(D, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'vikingboat-look.png'))
