"""H is for Hot dog (dx_hotdog_h), Food and drink A to Z, slot H (23 Nov 2026).
From his pick "H3 In a paper sleeve" (Claude's second-go sketches, claude/step-by-draw-food-capitals-vehicles-small-14x4.md).

A hot dog standing up in a stripy paper sleeve. The H is the two outside edges (the bun above, the paper below) and the
top edge of the paper. The bun leaves the top of each line at a slant, so it does not carry the line on.

    python3 build_hotdog.py
"""
from bcommon import *

p = Pic(s=1.08, dx=-4.0, dy=-3.9)
X0, X1, TOP, BOT, BAR = 29, 71, 26, 84, 55                     # the H
SL, SR, SY, SRAD = 42.5, 57.5, 16.5, 7.5                       # the sausage: its two sides, where its round top starts

p.stroke('sausage', Seg((SL, BAR), (SL, SY)), arc(50, SY, SRAD, SRAD, 180, 360, start=P(SL, SY), end=P(SR, SY)), Seg((SR, SY), (SR, BAR)), step=2)
bunL = one("M29,26 C32,20 34.5,17 37.6,17 C40.4,17 42.3,19 42.5,22.4")
p.stroke('bunL', bunL, step=3)
p.stroke('bunR', mirror(bunL), step=3)
p.stroke('mustard', poly((46, 21), (54, 26), (46, 31), (54, 36), (46, 41), (54, 46), (46, 51)), step=4, deco=True)
p.stroke('paper', one("M29,84 Q29,89 34,89 L66,89 Q71,89 71,84"), step=5)
STR = (37.4, 45.8, 54.2, 62.6)
for i, x in enumerate(STR):
    p.stroke('str%d' % i, Seg((x, BAR), (x, 89)), step=5)
p.stroke('h_l', Seg((X0, TOP), (X0, BOT)), step=1)
p.stroke('h_r', Seg((X1, TOP), (X1, BOT)), step=1)
p.stroke('h_bar', Seg((X0, BAR), (X1, BAR)), step=1)
p.build()

steps = [
    step('Start with an H', 'Draw a capital H: two tall lines down, and a line across the middle to join them.', p.step(1)),
    step('The sausage', 'In the top half of the H, draw a tall sausage with a round top. It stands on the middle line and pokes out above the H.', p.step(2)),
    step('The bun', 'From the top of each tall line, draw a round curve in to the sausage. Now there is a piece of bun on each side.', p.step(3)),
    step('Mustard', 'Draw a zigzag line down the sausage.', p.step(4)),
    step('The paper', 'Join the bottoms of the H with a line that curves round each corner. Then draw four lines down the paper for its stripes.', p.step(5)),
    step('Colour red', 'Colour the sausage red. Colour three stripes on the paper red: the two at the sides and the one in the middle.',
         [p.face('red', (50, 30)), p.face('red', (33, 70)), p.face('red', (50, 70)), p.face('red', (67, 70))], use='red'),
    step('Colour light brown', 'Colour the two pieces of bun light brown.', [p.face('lbrown', (35.5, 40)), p.face('lbrown', (64.5, 40))], use='lbrown'),
]
D = drawing('dx_hotdog_h', 'H is for Hot dog', 2, 10, 'things', ['Letters', 'Around the house'],
            'A hot dog in a stripy paper sleeve. The capital H is hiding in it: the two sides, and the top edge of the paper.',
            steps, ['red', 'lbrown'])
ok = finish('hotdog', D, {'set': 'house-AZ', 'slot': 'H', 'kind': 'key', 'age_from': 4}, p)
