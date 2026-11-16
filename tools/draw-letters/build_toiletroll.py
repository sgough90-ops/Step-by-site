"""t is for toilet roll holder (dx_toiletroll_t), Around the house a to z, slot t. Rebuilt from his ChatGPT sheet (15 Nov 2026).
The t is the holder: the stick is the pole, the bar is the shelf for the spare roll and the curl is the arm that holds the roll."""
from kit15 import *

GREY, LBROWN = FILL['grey'], FILL['lbrown']

STX, TOP = 32, 22
BY, BL, BR = 34, 18, 57
stem = Seg((STX, TOP), (STX, 56))
curl = Seg((STX, 56), (STX, 64), (36.2, 66), (41.8, 66))
arm = Seg((41.8, 66), (46, 66))
bar = Seg((BL, BY), (BR, BY))

# the roll on the arm, seen from the side, with its round end on the right
roll = [Seg((46, 66), (46, 57.5)), *arc(47.5, 57.5, 1.5, 1.5, 180, 270, start=P(46, 57.5), end=P(47.5, 56)), Seg((47.5, 56), (68, 56)),
        *arc(68, 66, 4, 10, -90, 90, start=P(68, 56), end=P(68, 76)), Seg((68, 76), (47.5, 76)),
        *arc(47.5, 74.5, 1.5, 1.5, 90, 180, start=P(47.5, 76), end=P(46, 74.5)), Seg((46, 74.5), (46, 66))]
face = arc(68, 66, 4, 10, -90, -270, start=P(68, 56), end=P(68, 76))
hole1 = circle(68, 66, 1.4, ry=3.4)

# the paper hanging down, with a torn edge
xs = [49 + 2 * i for i in range(8)]
torn = poly(*[(x, 86.5 if i % 2 == 0 else 88) for i, x in enumerate(xs)])
sheet = [Seg((49, 76), (49, 86.5)), *torn, Seg((63, 88), (63, 76))]

plate = rrect(26.5, 12.5, 37.5, TOP, 2.2)

# the spare roll standing on the shelf
spL, spR = Seg((40, BY), (40, 21.4)), Seg((54, BY), (54, 21.4))
sptop = circle(47, 21.4, 7, start_deg=180, ry=2.4)
hole2 = circle(47, 21.4, 2.4, ry=0.9)

steps = [
    step('Start with a t', 'Draw a small letter t with a long bar. At the bottom, curl the stick round to the right.', [line(stem, curl, arm), line(bar)]),
    step('The toilet roll', 'At the end of the curl, draw a long box with a round end. It is the roll, sitting on the holder.', [ring(roll)]),
    step('The end of the roll', 'Draw a curve inside the round end, and a small oval in the middle for the hole.', [line(*face), ring(hole1)]),
    step('The paper', 'Draw a piece of paper hanging down from the roll, with a zigzag edge where it was torn.', [line(*sheet)]),
    step('The wall plate', 'Draw a small box on top of the stick. It is the plate that holds the holder on the wall.', [ring(plate)]),
    step('A spare roll', 'Stand a spare roll on the shelf: two lines up from the bar and an oval on top.', [line(spL), line(spR), ring(sptop)]),
    step('The hole', 'Draw a small oval in the top of the spare roll.', [ring(hole2)]),
    step('Colour grey', 'Colour the wall plate grey.', [fill(GREY, *plate)], use='grey'),
    step('Colour light brown', 'Colour the two holes light brown. That is the cardboard tube inside.', [fill(LBROWN, *hole1), fill(LBROWN, *hole2)], use='lbrown'),
]
P_ = drawing('dx_toiletroll_t', 't is for toilet roll holder', 2, 10, 'things', ['Letters', 'Around the house'],
             'A toilet roll holder with a roll on it and a spare roll on the shelf. The small letter t is hiding in it: '
             'the stick is the pole, the bar is the shelf and the curl is the arm that holds the roll.',
             steps, ['grey', 'lbrown'])
scale(P_, 1.13, 45, 49)
move(P_, 5, 0)
save('toiletroll', P_, {'set': 'house-az', 'slot': 't', 'kind': 'key', 'age_from': 5})
