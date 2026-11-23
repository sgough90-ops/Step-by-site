"""d is for Dim sum (dx_dimsum_d), Food and drink a to z, slot d (23 Nov 2026).
From his pick, "four more" number 3 "With chopsticks" (Claude's sketches,
claude/step-by-draw-snowmobile-round4-dimsum-nuts-waffle-sketches.py).

A steamed bun with a red dot, two chopsticks beside it and a little dish of sauce.
The d is the round bun (its round) and the left edge of the chopstick that touches it (its stick).
  The bun meets the chopstick at two points and is cut off flat by it, so the two lines do not run along each other
  (a full circle that only touches the stick fails "no line runs along another").
  Step 1 draws a normal d: its stick is twice as tall as its round (19 to 87). Step 3 carries that line on up to the top
  of the chopstick (9), because a chopstick is longer than the stick of a d.
The bun stays white. The sketch's grey table line is left out, like in the other food drawings.
Written in the sketch's numbers.

    python3 build_dimsum.py
"""
from bcommon import *

p = Pic(s=1.0, dx=-5.4, dy=-1.0)
X, BOT, TOP1, CTOP, CW = 50, 87, 19, 9, 3.2                    # the d's stick, its bottom, its top in step 1, the top of the chopstick, how wide a chopstick is
R, OFF, CY = 17, 16.2, 70                                      # the bun: how big, how far its middle is from the stick, its height
CX = X - OFF
H = math.sqrt(R * R - OFF * OFF); ANG = math.degrees(math.atan2(H, OFF))
FOLD = (CX, CY - R * 0.5)                                      # where the folds on top of the bun meet

D_ROUND = arc(CX, CY, R, R, -ANG, -360 + ANG, start=P(X, CY - H), end=P(X, CY + H))
D_STICK = Seg((X, TOP1), (X, BOT))

for i, a in enumerate((205, 238, 270, 302, 335)):
    t = math.radians(a)
    p.stroke('fold%d' % i, Seg(FOLD, (FOLD[0] + R * 0.34 * math.cos(t), FOLD[1] + R * 0.34 * math.sin(t))), step=2, deco=True)
p.shape('dot', circle(CX, CY + R * 0.08, R * 0.13), step=2)
p.stroke('chop0', poly((X, TOP1), (X, CTOP), (X + CW, CTOP), (X + CW, BOT), (X, BOT)), step=3)
p.shape('chop1', rrect(56.6, 12, 56.6 + CW, 85, 1), step=3)
p.shape('pot', one("M66,80 L94,80 C93,89 87,93 80,93 C73,93 67,89 66,80 Z"), step=4)
p.shape('rim', ell(80, 80, 14, 3.4), step=4)
p.shape('sauce', ell(80, 80.3, 11.4, 2.2), step=4)
p.stroke('d_round', D_ROUND, step=1)
p.stroke('d_stick', D_STICK, step=1)
p.build()

steps = [
    step('Start with a d', 'Draw a small letter d: a big round shape, then a tall straight line down its right side.', p.step(1)),
    step('A steamed bun', 'The round of the d is a bun. Near the top draw five short lines that meet at the bottom, like a little fan. Draw a small circle in the middle.', p.step(2)),
    step('Chopsticks', 'Carry the tall line of the d on up. Go across a little, all the way down and back to the d: a chopstick. Draw another long thin one beside it.', p.step(3)),
    step('A dish of sauce', 'On the right draw a flat oval with a smaller oval inside it. Under it draw the round bottom of the dish.', p.step(4)),
    step('Colour red', 'Colour the small circle on the bun red. Leave the bun white.', [p.ring('red', 'dot')], use='red'),
    step('Colour light brown', 'Colour the two chopsticks light brown.', [p.face('lbrown', (X + CW / 2, 40)), p.ring('lbrown', 'chop1')], use='lbrown'),
    step('Colour blue', 'Colour the dish blue, round the sauce.', [p.face('blue', (80, 88)), p.ring('blue', 'rim', holes=('sauce',))], use='blue'),
    step('Colour brown', 'Colour the sauce brown.', [p.ring('brown', 'sauce')], use='brown'),
]
D = drawing('dx_dimsum_d', 'd is for Dim sum', 2, 10, 'things', ['Letters', 'Around the house'],
            'A steamed bun with chopsticks and a dish of sauce. The small letter d is hiding in them: the round bun and the edge of a chopstick.',
            steps, ['red', 'lbrown', 'blue', 'brown'])
ok = finish('dimsum', D, {'set': 'house-az', 'slot': 'd', 'kind': 'key', 'age_from': 4}, p)
