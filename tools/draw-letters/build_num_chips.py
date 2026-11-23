"""1 is for Chips (dx_chips_1), Food and drink 1 to 9, slot 1 (23 Nov 2026).
From his pick "1: 1 Chips" (claude/step-by-draw-food-numbers-1-to-9-36-sketches.md).

A carton of chips. The 1 is the tallest chip: its slanted top is the flick of the 1 and its right side is the long
line down, which stops at the front edge of the carton. Written in the sketch's numbers.

    python3 build_num_chips.py
"""
from ncommon import *

p = Pic(s=1.0, dx=0.0, dy=-1.5)
RIM = Seg((22, 56), (34, 62), (66, 62), (78, 56))          # the front edge of the carton: a smile


def ry(x):
    return RIM.at(seg_x(RIM, x))[1]


def side_x(y, right):
    k = (y - 56) / 38 * 8
    return 78 - k if right else 22 + k


# ---- the chips (behind the carton): up one side, across a slanted top and down the other side ----
p.stroke('chipA', poly((26, 64), (21.5, 33.5), (28.5, 29.5), (33.2, 64)), step=4)
p.stroke('chipB', poly((35.5, 66), (35.5, 24.5), (42.5, 29.5), (42.5, 66)), step=4)
p.stroke('chipD', poly((56.5, 66), (56.5, 27), (63.5, 21.5), (63.5, 66)), step=5)
p.stroke('chipE', poly((66.8, 64), (71.5, 33), (78.5, 37.5), (74, 64)), step=5)
p.stroke('tall_l', Seg((45, 17), (45, 66)), step=2)

# ---- the carton (hides the bottoms of the chips) and its stripe ----
p.shape('carton', RIM, poly((78, 56), (70, 94), (30, 94), (22, 56)), step=3)
p.stroke('stripe1', Seg((side_x(72, False), 72), (36, 77.6), (64, 77.6), (side_x(72, True), 72)), step=6)
p.stroke('stripe2', Seg((side_x(81, False), 81), (37, 86.6), (63, 86.6), (side_x(81, True), 81)), step=6)

# ---- the 1, in front of everything: the flick, then the long line down to the carton ----
p.stroke('one', poly((45, 17), (54, 9), (54, ry(54))), step=1)
p.build()

steps = [
    step('Start with a 1', 'Draw a number 1: a short slanted line going up, then a long straight line down. This 1 is hiding in the chips.', p.step(1)),
    step('The tallest chip', 'From the bottom of the short slanted line, draw a straight line down. Stop level with the bottom of the 1.', p.step(2)),
    step('The carton', 'Under the chip draw a curved line like a smile. From its ends draw two lines sloping in, and join them along the bottom.', p.step(3)),
    step('Two chips on the left', 'Draw two more chips on the left. Each one is a line up from the carton, a slanted top and a line back down.', p.step(4)),
    step('Two chips on the right', 'Draw two more chips on the right, the same way.', p.step(5)),
    step('A stripe', 'Draw two curved lines across the carton to make a stripe.', p.step(6)),
    step('Colour yellow', 'Colour all five chips yellow.',
         [p.face('yellow', s) for s in ((49.5, 40), (27, 45), (39, 45), (60, 45), (72.5, 48))], use='yellow'),
    step('Colour blue', 'Colour the carton blue, above and below the stripe. The stripe stays white.',
         [p.face('blue', (50, 68)), p.face('blue', (50, 90))], use='blue'),
]
D = drawing('dx_chips_1', '1 is for Chips', 1, 8, 'things', TAGS,
            'A carton of chips. The number 1 is hiding in it: the tallest chip, with its slanted top.',
            steps, ['yellow', 'blue'])
ok = finish('num1chips', D, {'set': SET, 'slot': '1', 'kind': 'key', 'age_from': 4}, p)
