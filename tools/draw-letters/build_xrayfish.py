"""X is for X-ray fish (dx_xrayfish_x), Animals A to Z, slot X. Rebuilt from his ChatGPT sheet (15 Nov 2026).
The X is where the tail crosses: its left half is the tail, its right half is the start of the body."""
from kit15 import *

LBLUE, YELLOW, PINK = FILL['lblue'], FILL['yellow'], FILL['pink']

XC = P(32, 50)
UL, LR, UR, LL = P(18, 36), P(46, 64), P(46, 36), P(18, 64)
x1, x2 = Seg(UL, LR), Seg(UR, LL)

top = Seg(UR, (54, 28), (76, 27.4), (88, 45.6))
nose = Seg((88, 45.6), (90.2, 48.2), (90.2, 51.8), (88, 54.4))
bot = Seg((88, 54.4), (76, 72.6), (54, 72), LR)
tp = split_many(top, [0.3, 0.5, 0.8])          # fin base, fin base, gill
bp = split_many(bot, [0.2, 0.5, 0.7])          # gill, fin base, fin base
TF1, TF2, G1 = tp[0].b, tp[1].b, tp[2].b
G2, BF1, BF2 = bp[0].b, bp[1].b, bp[2].b

notch = poly(UL, (25, 50), LL)
finT = [Seg(TF1, (51.4, 22), (52.6, 17.6), (53.8, 15.6)), Seg((53.8, 15.6), (58.6, 19.4), (61.6, 23.2), TF2)]
finB = [Seg(BF2, (51.4, 78), (52.6, 82.4), (53.8, 84.4)), Seg((53.8, 84.4), (58.6, 80.6), (61.6, 76.8), BF1)]
gill = Seg(G1, (77.6, 38), (77.6, 62), G2)
eye = circle(82.4, 45.6, 2.5)
n1, n2 = nose.split(0.62)
mouth = Seg(n1.b, (88.4, 52.6), (87.2, 53), (85.6, 52.8))

spine = Seg((37.5, 50), (73.6, 50))
ribs = []
for x in (45, 52, 59, 66):
    ribs.append(Seg((x, 50), (x - 0.8, 46.4), (x - 2.4, 43.2), (x - 4.6, 41.4)))
    ribs.append(Seg((x, 50), (x - 0.8, 53.6), (x - 2.4, 56.8), (x - 4.6, 58.6)))
bubbles = [circle(84.6, 31.4, 1.7), circle(89.4, 24.6, 2.1), circle(84.2, 17.6, 1.5)]

# the backbone must end on the gill line: snap it there
import math
hits = line_hits_seg((37.5, 50), (73.6, 50), gill)
gt, gpt = hits[0]
ga, gb = gill.split(gt)
spine = Seg((37.5, 50), ga.b)

steps = [
    step('Start with an X', 'Draw a big capital X on the left of your paper.', [line(x1), line(x2)]),
    step('The body', 'From the top right end of the X, curve up and over to a round nose, then back round to the bottom right end.',
         [line(top, nose, bot)]),
    step('The tail', 'Join the two left ends of the X with a line that points in, like a V on its side.', [line(*notch)]),
    step('The top fin', 'Draw a pointy fin on top of the body.', [line(*finT)]),
    step('The bottom fin', 'Draw another fin underneath.', [line(*finB)]),
    step('The head', 'Draw a curved line from the top to the bottom, near the nose.', [line(gill)]),
    step('Eye and mouth', 'Draw an eye with a dot in it, and a little line for the mouth.', [ring(eye), dot(82.8, 45.6, 2.2), line(mouth)]),
    step('The backbone', 'Now you can see inside! Draw a long straight line along the middle, from near the tail to the head.', [line(spine)]),
    step('The bones', 'Draw four curved bones going up from the backbone and four going down.', [line(r) for r in ribs]),
    step('Bubbles', 'Draw three bubbles coming from the fish.', [ring(b) for b in bubbles]),
]
body = fill(LBLUE, Seg(XC, UR), *tp, nose, *bp, Seg(LR, XC), cut=[d_fill(*eye)])
tail = fill(PINK, Seg(XC, UL), *notch, Seg(LL, XC))
fT = fill(YELLOW, *finT, tp[1].rev())
fB = fill(YELLOW, *finB, bp[2])
steps += [
    step('Colour light blue', 'Colour the body light blue, so it glows like an X-ray.', [body], use='lblue'),
    step('Colour yellow', 'Colour the fins and the eye yellow.', [fT, fB, fill(YELLOW, *eye)], use='yellow'),
    step('Colour pink', 'Colour the tail pink.', [tail], use='pink'),
]
P_ = drawing('dx_xrayfish_x', 'X is for X-ray fish', 3, 15, 'animals', ['Letters', 'Animals'],
             'An X-ray fish: a little see-through fish where you can see its bones. The capital X is hiding in it: '
             'the left half of the X is the tail and the right half is the start of the body.',
             steps, ['lblue', 'yellow', 'pink'])
save('xrayfish', P_, {'set': 'animals-AZ', 'slot': 'X', 'kind': 'swim', 'age_from': 5})
