"""A is for Avocado (dx_avocado_a), Food and drink A to Z, slot A (23 Nov 2026).
From his pick "A1 Half with its stone" (Claude's second-go sketches, claude/step-by-draw-food-capitals-vehicles-small-14x4.md).

Half an avocado with its stone. The top of the inside comes to a point: the A is that point (its two slanting lines)
and one cut across it (its bar). The round bottom of the inside carries the A's lines on. Written in the sketch's numbers.

    python3 build_avocado.py
"""
from bcommon import *

p = Pic(s=0.97, dx=1.5, dy=0.4)
AP, AL, AR, BAR = (50, 16), (35, 48), (65, 48), 36.5          # the A: its point, its two feet, how high its bar is
K = (BAR - AP[1]) / (AL[1] - AP[1]) * (AR[0] - AP[0])          # half the length of the bar
SKIN = ("M50,8.6 C51.5,8.6 53,10.8 54.2,14.05 L69.2,46.05 C73.6,55.5 85.2,61 85.2,73 C85.2,88 69.5,97.6 50,97.6 "
        "C30.5,97.6 14.8,88 14.8,73 C14.8,61 26.4,55.5 30.8,46.05 L45.8,14.05 C47,10.8 48.5,8.6 50,8.6 Z")
INSIDE = "M65,48 C69,57 80.5,62 80.5,73 C80.5,85.5 66.5,93 50,93 C33.5,93 19.5,85.5 19.5,73 C19.5,62 31,57 35,48"

p.shape('skin', one(SKIN), step=3)
p.stroke('inside', one(INSIDE), step=2)
p.shape('stone', circle(50, 73, 13.5), step=4)
p.stroke('shine', arc(50, 73, 8.6, 8.6, 200, 255), step=4, deco=True)
p.stroke('a_legs', poly(AL, AP, AR), step=1)
p.stroke('a_bar', Seg((50 - K, BAR), (50 + K, BAR)), step=1)
p.build()

flesh = p.net.all('a_legs') + p.net.all('inside')              # the edge of the inside: the A's two lines, then the round curve
steps = [
    step('Start with an A', 'Draw a capital A: a slanting line up to a point, a slanting line back down, and a line across the middle.', p.step(1)),
    step('The inside', 'From the bottom of each slanting line, carry on down and round in one big curve, like a fat pear.', p.step(2)),
    step('The skin', 'Draw the same shape again, a little bigger, all the way round the outside. Start just above the point of the A.', p.step(3)),
    step('The stone', 'Draw a big circle in the fat part for the stone. Add a little curved line inside it for the shine.', p.step(4)),
    step('Colour green', 'Colour the skin green: the thin band all the way round the outside.',
         [fill(FILL['green'], *p.net.all('skin'), cut=[d_fill(*flesh)])], use='green'),
    step('Colour yellow', 'Colour the inside yellow, round the stone.', [fill(FILL['yellow'], *flesh, cut=[d_fill(*p.net.all('stone'))])], use='yellow'),
    step('Colour brown', 'Colour the stone brown.', [p.ring('brown', 'stone')], use='brown'),
]
D = drawing('dx_avocado_a', 'A is for Avocado', 2, 10, 'things', ['Letters', 'Around the house'],
            'Half an avocado with its big brown stone. The capital A is hiding at the top: the pointed tip and one cut across it.',
            steps, ['green', 'yellow', 'brown'])
ok = finish('avocado', D, {'set': 'house-AZ', 'slot': 'A', 'kind': 'key', 'age_from': 4}, p)
