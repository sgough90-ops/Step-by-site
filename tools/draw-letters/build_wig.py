"""w is for wig (Around the house a to z, slot w). A wig on a stand.
The w: the zigzag fringe of the wig (a true w: down, up, down, up). The face hangs from its two top ends
and the hair goes over the top: nothing crosses the w."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

WL_, WR_ = (36.0, 40.0), (64.0, 40.0)
# ---- 1: the w ----
W_ = poly(WL_, (43.0, 52.0), (50.0, 40.0), (57.0, 52.0), WR_)

# ---- 2: the face ----
faceL = Seg(WL_, (36.0, 56.0), (40.0, 69.0), (50.0, 69.0))
faceR = rev(mirror([faceL]))[0]                       # from the chin up to the top of the w on the right

# ---- 3: the hair ----
TL = (14.0, 66.0)
outL = [Seg(TL, (20.0, 62.0), (22.0, 52.0), (24.0, 40.0)), Seg((24.0, 40.0), (26.0, 22.0), (36.0, 10.0), (50.0, 10.0))]
outer = outL + rev(mirror(outL))

# ---- 4: the ends of the hair ----
tC = 0.5
sideL = sub(faceL, 0, tC); CL = sideL.b               # the side of the face that the hair covers
scalL = [Seg(TL, (17.0, 71.5), (23.5, 72.0), (26.5, 67.0)), Seg((26.5, 67.0), (29.5, 71.5), (35.5, 70.5), CL)]
scalR = mirror(scalL); sideR = mirror([sideL])[0]

# ---- 5: a shine on the hair, and a little face ----
shine = Seg((30.0, 31.0), (31.5, 23.0), (36.0, 17.0), (42.5, 15.2))
eyes = [dot(44.6, 58.4, w=3.2), dot(55.4, 58.4, w=3.2)]
smile = Seg((46.6, 62.6), (48.0, 64.6), (52.0, 64.6), (53.4, 62.6))

# ---- 6: the stand ----
tN = seg_line_cross_x(faceL, 46.0, 0.5, 1.0)
chinL = sub(faceL, tN, 1); pL = chinL.a; chinR = mirror([chinL])[0]; pR = chinR.a
BY = 82.0
neckL = Seg(pL, (pL[0], BY)); neckR = Seg(pR, (pR[0], BY))
base = rrect(34.0, BY, 66.0, 89.0, 3.5)

SKIN = '#f8dcae'
steps = [
    step('Start with a w', 'Draw a small letter w: down, up, down, up. Four straight lines with sharp points. This w is hiding in the wig.',
         [line(*W_)]),
    step('The face', 'From the top of the w on the left, draw down, round a chin and back up to the top of the w on the right.',
         [line(faceL, faceR)]),
    step('The hair', 'Draw a big round shape over the top, from one side to the other. Flick the ends out at the bottom.',
         [line(*outer)]),
    step('The ends of the hair', 'From each flick, draw two round bumps back in to the side of the face.',
         [line(*scalL), line(*scalR)]),
    step('Shine and a face', 'Draw a curved line on the hair to make it shine. Draw two dots and a smile on the face.',
         [line(shine)] + eyes + [line(smile)]),
    step('The stand', 'Draw two lines down from the chin. Draw a flat box with round corners under them. The wig sits on this stand.',
         [line(neckL), line(neckR), ring(*base)]),
    step('Colour the wig', 'Colour the hair pink, all the way round the face and down to the points of the w.',
         [fill(FILL['pink'], *(outer + scalR + [sideR.rev()] + rev(W_) + [sideL] + rev(scalL)))], use='pink'),
    step('Colour the stand', 'Colour the face, the neck and the flat box light brown.',
         [fill(SKIN, *(W_ + [faceR.rev(), faceL.rev()])),
          fill(SKIN, *([neckL, Seg((pL[0], BY), (pR[0], BY)), neckR.rev(), chinR, chinL.rev()])),
          fill(SKIN, *base)], use='lbrown'),
]

D = drawing('dx_wig_w', 'w is for wig', 2, 10, 'things', ['Letters', 'Around the house'],
            'A pink wig on a stand with a smiling face, and a zigzag fringe. The small letter w is hiding in it: the w is the fringe.',
            steps, ['pink', 'lbrown'])
json.dump(D, open(os.path.join(OUT, 'wig.json'), 'w'))
json.dump({'set': 'house-az', 'slot': 'w', 'kind': 'key', 'age_from': 4}, open(os.path.join(OUT, 'wig.place.json'), 'w'))
print('wig: %d steps' % len(steps))
