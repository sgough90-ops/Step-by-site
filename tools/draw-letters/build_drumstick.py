"""D is for Drumstick (dx_drumstick_d), Food and drink A to Z, slot D (23 Nov 2026).
From his pick "D1 Dipped in sauce" (Claude's second-go sketches, claude/step-by-draw-food-capitals-vehicles-small-14x4.md).

A chicken drumstick whose fat end has been dipped in sauce, with the pot of sauce beside it. The D is the edge of the
sauce (its straight line) and the round end of the meat (its curve). Written in the sketch's numbers.

    python3 build_drumstick.py
"""
from bcommon import *

p = Pic(s=1.0, dx=2.2, dy=-9.5)
X, TOP, BOT = 58, 27, 73                                       # the D's straight line
BOW = "M58,27 C80,25 92,37 92,50 C92,63 80,75 58,73"            # the D's curve: the round end of the meat
LEFT = "M58,27 C46,28 36,37 30,46 L30,54 C36,63 46,72 58,73"    # the rest of the meat, in to the narrow end
BONE = "M32,46.4 L13,46.4 C12.6,43.6 9.4,41.6 6.6,42.8 C3.6,44 3,47.6 5.6,50 C3,52.4 3.6,56 6.6,57.2 C9.4,58.4 12.6,56.4 13,53.6 L32,53.6 Z"

p.shape('bone', one(BONE), step=3)
p.region('meatR', one(LEFT), rev(one(BOW)))
p.stroke('left', one(LEFT), step=2)
p.shape('pot', one("M62,80 L92,80 L89,95 L65,95 Z"), step=4)
p.shape('rim', ell(77, 80, 15, 3.8), step=4)
p.shape('sauce', ell(77, 80.3, 12.2, 2.4), step=4)
p.stroke('d_stick', Seg((X, TOP), (X, BOT)), step=1)
p.stroke('d_bow', one(BOW), step=1)
p.build()

steps = [
    step('Start with a D', 'Draw a capital D: a straight line down, then a big round curve from the top of the line to the bottom.', p.step(1)),
    step('The meat', 'From the top of the D, curve out to the left and in to a narrow end. Do the same from the bottom. Join the two ends with a short line.', p.step(2)),
    step('The bone', 'From the narrow end draw two lines out to the left. Finish the bone with two round bumps.', p.step(3)),
    step('A pot of sauce', 'Under the D draw a flat oval with a smaller oval inside it. Draw the two sides of the pot going down, and a line across the bottom.', p.step(4)),
    step('Colour red', 'Colour the D red: this end has been dipped in the sauce. Colour the sauce in the pot red too.',
         [p.face('red', (76, 50)), p.ring('red', 'sauce')], use='red'),
    step('Colour brown', 'Colour the rest of the meat brown.', [p.face('brown', (44, 50))], use='brown'),
]
D = drawing('dx_drumstick_d', 'D is for Drumstick', 1, 8, 'things', ['Letters', 'Around the house'],
            'A chicken drumstick dipped in sauce. The capital D is hiding in it: the edge of the sauce and the round end of the meat.',
            steps, ['red', 'brown'])
ok = finish('drumstick', D, {'set': 'house-AZ', 'slot': 'D', 'kind': 'key', 'age_from': 4}, p)
