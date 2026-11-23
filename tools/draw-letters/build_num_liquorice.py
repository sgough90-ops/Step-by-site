"""9 is for Liquorice wheel (dx_liquorice_9), Food and drink 1 to 9, slot 9 (23 Nov 2026).
From his pick "9: 4 Liquorice wheel" (claude/step-by-draw-food-numbers-1-to-9-36-sketches.md).

A coiled liquorice wheel with its loose end hanging straight down. The 9 is the outside of the wheel and the outside
edge of the loose end. It is drawn as one line (round the loop, then straight down), as a 9 is written.
Written in the sketch's numbers.

    python3 build_num_liquorice.py
"""
from ncommon import *

p = Pic(s=1.05, dx=5.9, dy=-5.6)
CX, CY, R, Y1, WD, SWEET = 42, 36, 24, 94, 5.4, 6.6
XI = CX + R - WD                                           # the inside edge of the loose end
J = (XI, CY + math.sqrt(R * R - (XI - CX) ** 2))           # where that edge meets the wheel


def swirl_pt(deg):
    """the swirl: starts 5.4 inside the wheel on the right and comes in by 5.4 every time round (anticlockwise)"""
    r = (R - WD) - WD * deg / 360
    return (CX + r * math.cos(math.radians(-deg)), CY + r * math.sin(math.radians(-deg)))


TURN = (R - WD - SWEET) / WD * 360                         # how far round the swirl goes before it reaches the sweet
swirl = smooth([J, (XI, CY + 8)] + [swirl_pt(d) for d in range(0, int(TURN), 30)] + [swirl_pt(TURN)])

# ---- the loose end's inside edge and bottom, the swirl, the little sweet in the middle ----
p.stroke('tail_in', Seg(J, (XI, Y1)), Seg((XI, Y1), (CX + R, Y1)), step=2)
p.stroke('swirl', swirl, step=4, deco=True)
p.shape('sweet', circle(CX, CY, SWEET), step=3)

# ---- the 9, in front of everything: one line, round the loop and then straight down ----
p.stroke('nine', arc(CX, CY, R, R, 0, -360, start=P(CX + R, CY), end=P(CX + R, CY)), Seg((CX + R, CY), (CX + R, Y1)), step=1)
p.build()

steps = [
    step('Start with a 9', 'Draw a number 9: a big round loop, then a straight line down from its right side. This 9 is hiding in the liquorice wheel.', p.step(1)),
    step('The loose end', 'Draw a second line down, just inside the first, from the loop to the bottom. Join the two lines at the bottom.', p.step(2)),
    step('The middle', 'Draw a small circle in the middle of the loop. This is a little sweet.', p.step(3)),
    step('The swirl', 'From the top of the second line, carry on up inside the loop. Swirl round and round until you reach the small circle.', p.step(4)),
    step('Colour black', 'Colour the liquorice black: the wheel, round the little sweet, and the loose end.',
         [p.face('black', (CX, CY - 15), holes=('sweet',)), p.face('black', (XI + WD / 2, 75))], use='black'),
    step('Colour pink', 'Colour the little sweet in the middle pink.', [p.ring('pink', 'sweet')], use='pink'),
]
D = drawing('dx_liquorice_9', '9 is for Liquorice wheel', 2, 10, 'things', TAGS,
            'A liquorice wheel with its loose end hanging down. The number 9 is hiding in it: the round wheel and the straight end.',
            steps, ['black', 'pink'])
ok = finish('num9liquorice', D, {'set': SET, 'slot': '9', 'kind': 'key', 'age_from': 5}, p)
