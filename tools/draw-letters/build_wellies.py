"""W is for Wellies (dx_wellies_w), Around the house A to Z, slot W. Rebuilt from his ChatGPT sheet (15 Nov 2026).
The W is the tops of the two boots: each V is the yellow lining you can see inside a boot."""
from kit15 import *
import math

GREEN, YELLOW, BLACK, LBLUE = FILL['green'], FILL['yellow'], FILL['black'], FILL['lblue']
CX = 50.0

W1, Wb1, WM, Wb2, W2 = P(24, 18), P(36, 40), P(CX, 18), P(64, 40), P(76, 18)
wsegs = poly(W1, Wb1, WM, Wb2, W2)
topL, topR = Seg(W1, WM), Seg(WM, W2)

SY = 76.5   # top of the soles
sideL = Seg(W1, (24, 58))
toeL = Seg((24, 58), (24, 65.5), (13.5, 67.5), (13.5, SY))
cornL = Seg((13.5, SY), (13.5, 81.6), (16.8, 84), (21.5, 84))
botL = Seg((21.5, 84), (45.5, 84))
notL = Seg((45.5, 84), (48, 84), (49.4, 82.8), (CX, 81))
left_out = [sideL, toeL, cornL, botL, notL]
right_out = rev(mirror(left_out, CX))          # from the bump in the middle, round the right boot, up to the W's top-right end
sideR, toeR, cornR, botR, notR = right_out[4], right_out[3], right_out[2], right_out[1], right_out[0]
divider = [Seg(WM, (CX, SY)), Seg((CX, SY), (CX, 81))]
soleL, soleR = Seg((13.5, SY), (CX, SY)), Seg((CX, SY), (86.5, SY))

# the puddle: part of a wide oval, from the corner of one boot round underneath to the corner of the other
cL1, cL2 = cornL.split(0.5)
Q = cL1.b
Q2 = P(2 * CX - Q[0], Q[1])
cRa = mirror([cL2], CX)[0].rev()     # (78.5,84) -> Q2
pcx, pcy, prx = CX, 86.5, 45
c = (Q[0] - pcx) / prx
pry = abs(Q[1] - pcy) / math.sqrt(1 - c * c)
th = math.degrees(math.atan2((Q[1] - pcy) / pry, c)) % 360
puddle = arc(pcx, pcy, prx, pry, th, 180 - th, start=Q, end=Q2)

steps = [
    step('Start with a W', 'Draw a big capital W near the top. Make its three top points the same height.', [line(*wsegs)]),
    step('Close the tops', 'Draw a line across the top of each V. These are the tops of the two boots.', [line(topL), line(topR)]),
    step('The boots', 'From the left top corner go down, round the toe, along the bottom and up a little bump in the middle. Do the same on the other side.',
         [line(*left_out, *right_out)]),
    step('The middle line', 'Draw a straight line from the middle point of the W down to the little bump.', [line(*divider)]),
    step('The soles', 'Draw a line across each boot, near the bottom, from the toe to the middle line.', [line(soleL), line(soleR)]),
    step('A puddle', 'Draw a big flat puddle under the boots, from one toe round to the other.', [line(*puddle)]),
]
bootL = fill(GREEN, sideL, toeL, soleL, divider[0].rev(), Seg(WM, Wb1), Seg(Wb1, W1))
bootR = fill(GREEN, divider[0], soleR, toeR, sideR, Seg(W2, Wb2), Seg(Wb2, WM))
linL = fill(YELLOW, topL, Seg(WM, Wb1), Seg(Wb1, W1))
linR = fill(YELLOW, topR, Seg(W2, Wb2), Seg(Wb2, WM))
sL = fill(BLACK, cornL, botL, notL, divider[1].rev(), soleL.rev())
sR = fill(BLACK, soleR.rev(), divider[1], notR, botR, cornR)
steps += [
    step('Colour green', 'Colour the two boots green.', [bootL, bootR], use='green'),
    step('Colour yellow', 'Colour inside the tops of the boots yellow.', [linL, linR], use='yellow'),
    step('Colour black', 'Colour the soles black.', [sL, sR], use='black'),
]
pud = fill(LBLUE, *puddle, cRa.rev(), botR.rev(), notR.rev(), notL.rev(), botL.rev(), cL2.rev())
steps.append(step('Colour light blue', 'Colour the puddle light blue.', [pud], use='lblue'))
P_ = drawing('dx_wellies_w', 'W is for Wellies', 2, 10, 'things', ['Letters', 'Around the house'],
             'A pair of green wellies standing in a puddle. The capital W is hiding in them: its two V shapes are the yellow insides of the boots.',
             steps, ['green', 'yellow', 'black', 'lblue'])
save('wellies', P_, {'set': 'house-AZ', 'slot': 'W', 'kind': 'key', 'age_from': 5})
