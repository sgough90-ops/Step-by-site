"""X is for Xylophone (Around the house A to Z, slot X).
The X: the two beaters, lying crossed in front of the xylophone (two straight lines, as the X is written).
A ball goes on each top end. Nothing else touches the X."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

HY, HRAD = 66.0, 4.0
hcL, hcR = (35.5, HY), (64.5, HY)
aL = on(hcL[0], hcL[1], HRAD, HRAD, 45); aR = on(hcR[0], hcR[1], HRAD, HRAD, 135)
# ---- 1: the X ----
X_ = [Seg(aL, (62.0, 92.5)), Seg(aR, (38.0, 92.5))]
# ---- 2: a ball on each beater ----
ballL = circle(hcL[0], hcL[1], HRAD, start_deg=45); ballR = circle(hcR[0], hcR[1], HRAD, start_deg=135)
# ---- 3: the two ends of the frame ----
postL = rrect(11.5, 16.5, 17.5, 63.5, 3.0); postR = rrect(82.5, 26.5, 88.5, 53.5, 3.0)
# ---- 4, 5: six bars, each a little shorter than the last ----
BW, GAP = 8.4, 1.92
def bar(i):
    x0 = 20.0 + i * (BW + GAP)
    return rrect(x0, 20.0 + 2 * i, x0 + BW, 60.0 - 2 * i, 1.8)
bars = [bar(i) for i in range(6)]
# ---- 6: pins ----
pins = []
for i in range(6):
    cx = 20.0 + i * (BW + GAP) + BW / 2
    pins += [dot(cx, 20.0 + 2 * i + 4.2, w=2.8), dot(cx, 60.0 - 2 * i - 4.2, w=2.8)]

steps = [
    step('Start with an X', 'Draw a capital X near the bottom of your paper: two straight lines that cross in the middle. This X is hiding in the picture.',
         [line(X_[0]), line(X_[1])]),
    step('Two beaters', 'Draw a ball on each top end of the X. Now the X is two beaters for hitting the notes.',
         [ring(*ballL), ring(*ballR)]),
    step('The frame', 'Draw a tall thin bar with round ends on the left. Draw a shorter one on the right.',
         [ring(*postL), ring(*postR)]),
    step('Three bars', 'Draw three bars side by side next to the tall end. Make each one a little shorter than the last. Leave small gaps.',
         [ring(*b) for b in bars[:3]]),
    step('Three more bars', 'Draw three more bars, each one a little shorter, up to the short end.',
         [ring(*b) for b in bars[3:]]),
    step('The pins', 'Draw a dot near the top and a dot near the bottom of every bar.',
         pins),
    step('Colour red', 'Colour the first bar red. Colour the ball on the left red too.',
         [fill(FILL['red'], *bars[0]), fill(FILL['red'], *ballL)], use='red'),
    step('Colour orange', 'Colour the second bar orange.', [fill(FILL['orange'], *bars[1])], use='orange'),
    step('Colour yellow', 'Colour the third bar yellow.', [fill(FILL['yellow'], *bars[2])], use='yellow'),
    step('Colour green', 'Colour the fourth bar green.', [fill(FILL['green'], *bars[3])], use='green'),
    step('Colour blue', 'Colour the fifth bar blue. Colour the ball on the right blue too.',
         [fill(FILL['blue'], *bars[4]), fill(FILL['blue'], *ballR)], use='blue'),
    step('Colour purple', 'Colour the last bar purple.', [fill(FILL['purple'], *bars[5])], use='purple'),
    step('Colour the frame', 'Colour the two ends of the frame light brown.',
         [fill(FILL['lbrown'], *postL), fill(FILL['lbrown'], *postR)], use='lbrown'),
]

D = drawing('dx_xylophone_x', 'X is for Xylophone', 2, 15, 'things', ['Letters', 'Around the house'],
            'A rainbow xylophone with two beaters. The capital X is hiding in it: the X is the two beaters, lying crossed.',
            steps, ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'lbrown'])
json.dump(D, open(os.path.join(OUT, 'xylophone.json'), 'w'))
json.dump({'set': 'house-AZ', 'slot': 'X', 'kind': 'key', 'age_from': 4}, open(os.path.join(OUT, 'xylophone.place.json'), 'w'))
print('xylophone: %d steps' % len(steps))
