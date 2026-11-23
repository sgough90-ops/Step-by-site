"""8 is for Fried eggs (dx_friedeggs_8), Food and drink 1 to 9, slot 8 (23 Nov 2026).
From his pick "8: 3 Fried egg" (claude/step-by-draw-food-numbers-1-to-9-36-sketches.md).

Two fried eggs in a frying pan. The 8 is the two yolks: a round loop on a bigger round loop, just touching.
The pan is a little smaller than in the sketch so that its handle fits on the paper.
Written in the sketch's numbers.

    python3 build_num_eggs.py
"""
from ncommon import *

p = Pic(s=0.8333, dx=4.33, dy=4.33)
H = 5 / math.sqrt(2)                                # the handle is 10 wide and slants at 45 degrees

# ---- the handle (behind the pan, which hides where it joins) ----
p.stroke('handle', Seg((70 + H, 70 - H), (104 + H, 104 - H)), arc(104, 104, 5, 5, -45, 135, start=P(104 + H, 104 - H), end=P(104 - H, 104 + H)),
         Seg((104 - H, 104 + H), (70 - H, 70 + H)), step=4)

# ---- the pan and the white of the eggs ----
p.shape('pan', circle(50, 50, 47), step=3)
p.shape('white', smooth([(50, 9), (67, 12), (77, 25), (73, 43), (82, 60), (75, 80), (58, 90), (40, 88), (25, 80), (20, 62), (27, 46), (19, 30), (31, 14)], closed=True), step=2)

# ---- the 8, in front of everything: two round yolks, just touching. It is one line, as an 8 is written: from the
#      middle round the top loop and back, then round the bottom loop (two separate rings would be flagged as one line
#      running along another where they touch) ----
TOUCH = P(50, 47)
p.stroke('eight', arc(50, 32, 15, 15, 90, 450, start=TOUCH, end=TOUCH), arc(50, 65, 18, 18, -90, -450, start=TOUCH, end=TOUCH), step=1)
p.build()
p.stay_white('white')

steps = [
    step('Start with an 8', 'Draw a number 8: a round loop on top and a bigger round loop under it, just touching. These are two egg yolks.', p.step(1)),
    step('The egg white', 'Draw a big wobbly shape all the way round the 8. This is the white of the eggs.', p.step(2)),
    step('The pan', 'Draw a big circle round the eggs. This is the frying pan.', p.step(3)),
    step('The handle', 'Draw the handle sticking out at the bottom right: two lines side by side, joined with a round end.', p.step(4)),
    step('Colour yellow', 'Colour the two yolks yellow.', [p.face('yellow', (50, 32)), p.face('yellow', (50, 65))], use='yellow'),
    step('Colour black', 'Colour the pan black, all round the eggs. The egg white stays white.', [p.ring('black', 'pan', holes=('white',))], use='black'),
    step('Colour brown', 'Colour the handle brown.', [p.face('brown', (95, 95))], use='brown'),
]
D = drawing('dx_friedeggs_8', '8 is for Fried eggs', 1, 8, 'things', TAGS,
            'Two fried eggs in a frying pan. The number 8 is hiding in them: the two round yolks.',
            steps, ['yellow', 'black', 'brown'])
ok = finish('num8eggs', D, {'set': SET, 'slot': '8', 'kind': 'key', 'age_from': 4}, p)
