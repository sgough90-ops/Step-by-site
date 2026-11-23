"""m is for mail van (dx_mailvan_m), Vehicles a to z, slot m (23 Nov 2026).
From his pick "m4 Little red post van", with the m made less tall as he asked ("don't make it quite as tall the letter m")
(Claude's second-go sketches, claude/step-by-draw-food-capitals-vehicles-small-14x4.md).

A small red mail van facing left, with two back wheels close together. The m is the bottom edge of the van going up and
over those two wheels. In the sketch the m was 38 wide and 24.5 tall; here it is 38 wide and 21 tall.

    python3 build_mailvan.py
"""
from bcommon import *

p = Pic(s=1.0, dx=1.4, dy=2.0)
X0, X1, X2, BOT, TOP, RY = 50, 69, 88, 83, 71.5, 9.5            # the m: its three lines, their bottom, where the arches start, how high they go
R, WY, FX, FA = 7.6, 80.4, 22, 9.6                             # wheels, their middle height, the front wheel and its arch
S0, S1 = 54, 58.4                                              # the stripe

M1 = [Seg((X0, BOT), (X0, TOP))] + arc((X0 + X1) / 2, TOP, (X1 - X0) / 2, RY, 180, 360, start=P(X0, TOP), end=P(X1, TOP)) + [Seg((X1, TOP), (X1, BOT))]
M2 = arc((X1 + X2) / 2, TOP, (X2 - X1) / 2, RY, 180, 360, start=P(X1, TOP), end=P(X2, TOP)) + [Seg((X2, TOP), (X2, BOT))]
BODY = (one("M88,83 L94,83 L94,24 Q94,14 84,14 L42,14 C32,14 28,19 24.6,27 L17,45.5 L9,48.6 Q6,49.6 6,53.6 L6,83") +
        [Seg((6, BOT), (FX - FA, BOT)), Seg((FX - FA, BOT), (FX - FA, WY))] +
        arc(FX, WY, FA, FA, 180, 360, start=P(FX - FA, WY), end=P(FX + FA, WY)) +
        [Seg((FX + FA, WY), (FX + FA, BOT)), Seg((FX + FA, BOT), (X0, BOT))])

p.stroke('body', BODY, step=3)
p.stroke('stripe0', Seg((6, S0), (94, S0)), step=4)
p.stroke('stripe1', Seg((6, S1), (94, S1)), step=4)
p.stroke('door_u', Seg((45, 14), (45, S0)), step=5, deco=True)
p.stroke('door_l', Seg((45, S1), (45, BOT)), step=5, deco=True)
p.shape('win', one("M21.6,45 L27.2,31.4 Q28.2,29.5 30.6,29.5 L42,29.5 L42,45 Z"), step=5)
p.shape('env', box(58, 24, 82, 41), step=5)
p.stroke('flap', poly((58, 24), (70, 33.6), (82, 24)), step=5, deco=True)
p.shape('lamp', rrect(4.4, 60.4, 8.4, 66.4, 1.2), step=3)
p.shape('bumper', rrect(2.8, 76, 9.8, 81.6, 2), step=3)
WHEELS = ((X0 + X1) / 2, (X1 + X2) / 2, FX)
for i, x in enumerate(WHEELS):
    p.shape('tyre%d' % i, circle(x, WY, R), step=2)
    p.shape('hub%d' % i, circle(x, WY, 3.4), step=2)
p.stroke('m1', M1, step=1)
p.stroke('m2', M2, step=1)
p.build()

steps = [
    step('Start with an m', 'Draw a small letter m: a short line up, a round hump down to the bottom, then a second hump just the same.', p.step(1)),
    step('Three wheels', 'Draw a wheel under each hump of the m: a circle with a small circle inside. Draw one more wheel far over on the left.', p.step(2)),
    step('The van', 'From the right of the m go up the back, along the roof, down the sloping front and the nose, and over the front wheel to the m. Add a light and a bumper.', p.step(3)),
    step('The stripe', 'Draw two long lines along the side of the van, close together, from the nose to the back.', p.step(4)),
    step('Window, door and letter', 'Draw a window at the front, and a line down for the door, above and below the stripe. Draw a box with a V in it: a letter to post.', p.step(5)),
    step('Colour red', 'Colour the van red, above and below the stripe. Leave the window, the letter and the wheels.',
         [p.face('red', (70, 48), holes=('win', 'env')), p.face('red', (40, 66))], use='red'),
    step('Colour yellow', 'Colour the stripe yellow. Colour the letter and the little light on the nose yellow too.',
         [p.face('yellow', (50, (S0 + S1) / 2)), p.ring('yellow', 'env'), p.ring('yellow', 'lamp')], use='yellow'),
    step('Colour light blue', 'Colour the window light blue.', [p.ring('lblue', 'win')], use='lblue'),
    step('Colour black', 'Colour the three tyres black, round the small circles.', [p.ring('black', 'tyre%d' % i, holes=('hub%d' % i,)) for i in range(3)], use='black'),
    step('Colour grey', 'Colour the middle of each wheel grey. Colour the bumper grey too.', [p.ring('grey', 'hub%d' % i) for i in range(3)] + [p.ring('grey', 'bumper')], use='grey'),
]
D = drawing('dx_mailvan_m', 'm is for mail van', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A little red mail van with a letter on its side. The small letter m is hiding at the back: the edge of the van going over its two back wheels.',
            steps, ['red', 'yellow', 'lblue', 'black', 'grey'])
ok = finish('mailvan', D, {'set': 'vehicles-az', 'slot': 'm', 'kind': 'drive', 'age_from': 5}, p)
