"""W is for Woodpecker (Animals A to Z, slot W). Side view, holding on to a tree trunk.
The W: the two pointed tail feathers at the bottom of the bird. The body grows up from its two top ends,
so the W is the bottom edge of the bird: nothing crosses it."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

WA, WB = (34.0, 72.0), (54.0, 72.0)
# ---- 1: the W ----
W_ = poly(WA, (39.0, 92.0), (44.0, 72.0), (49.0, 92.0), WB)

# ---- 3: the head (worked out first so the body can end on it) ----
HC = (44.0, 28.0); HR = 11.0
head = circle(HC[0], HC[1], HR)
nL = on(HC[0], HC[1], HR, HR, 135); nR = on(HC[0], HC[1], HR, HR, 45)

# ---- 2: the body ----
sideL = Seg(WA, (25.0, 60.0), (25.0, 44.0), nL)
sideR = Seg(WB, (63.0, 60.0), (63.0, 44.0), nR)

# ---- 4: the beak ----
TX = 72.0
bkT = on(HC[0], HC[1], HR, HR, 352); bkB = on(HC[0], HC[1], HR, HR, 22)
TIP = (TX, 29.6)
beak = [Seg(bkT, TIP), Seg(TIP, bkB)]

# ---- 5: the cap and the eye ----
hL = on(HC[0], HC[1], HR, HR, 200); hR_ = on(HC[0], HC[1], HR, HR, 340)
capline = Seg(hL, (40.0, 21.0), (48.0, 21.0), hR_)
eye = circle(48.4, 29.6, 2.6)
pupil = dot(48.9, 29.6, w=2.6)

# ---- 6: the tummy ----
tT = 0.86
side_top = sub(sideR, tT, 1); pT = side_top.a           # the top bit of the right side, above the tummy
tummy = Seg(pT, (47.0, 50.0), (45.0, 64.0), WB)

# ---- 7: the tree ----
trunk = poly((TX, 6.0), (90.0, 6.0), (90.0, 94.0), (TX, 94.0), closed=True)
bark = [Seg((78.0, 14.0), (80.2, 17.0), (80.2, 21.0), (78.0, 24.0)), Seg((84.0, 36.0), (86.2, 39.0), (86.2, 43.0), (84.0, 46.0)),
        Seg((79.0, 68.0), (81.2, 71.0), (81.2, 75.0), (79.0, 78.0)), Seg((84.0, 80.0), (86.2, 83.0), (86.2, 87.0), (84.0, 90.0))]

# ---- 8: the feet ----
f1 = P(*sideR.at(0.5)); f2 = P(*sideR.at(0.3))
feet = [Seg(f1, (TX, f1[1])), Seg(f2, (TX, f2[1]))]

steps = [
    step('Start with a W', 'Draw a capital W near the bottom of your paper: down, up, down, up, with sharp points. This W is hiding in the woodpecker.',
         [line(*W_)]),
    step('The body', 'From the top of the W on the left, draw a curved line up and in. Do the same on the right. Leave a gap between the two tops.',
         [line(sideL), line(sideR)]),
    step('The head', 'Draw a round head sitting on top of the body. It touches the tops of both lines.',
         [ring(*head)]),
    step('The beak', 'Draw a long pointed beak on the right side of the head.',
         [line(*beak)]),
    step('Cap and eye', 'Draw a curved line across the top of the head for a cap. Draw a round eye with a dot in it.',
         [line(capline), ring(*eye), pupil]),
    step('The tummy', 'Draw a curved line inside the body, from just under the head down to the top of the W on the right.',
         [line(tummy)]),
    step('The tree', 'Draw a tall tree trunk on the right: a long box. Its side touches the tip of the beak. Add four little curved lines for bark.',
         [ring(*trunk)] + [line(b) for b in bark]),
    step('The feet', 'Draw two short lines from the tummy across to the tree. The woodpecker is holding on.',
         [line(f) for f in feet]),
    step('Colour the cap', 'Colour the cap on top of the head red.',
         [fill(FILL['red'], *(arc_to(HC[0], HC[1], HR, HR, hL, hR_, True) + [capline.rev()]))], use='red'),
    step('Colour black', 'Colour the back and the two pointed tail feathers black. Leave the tummy and the face white. Colour the beak black too.',
         [fill(FILL['black'], *([sideL] + arc_to(HC[0], HC[1], HR, HR, nL, nR, False) + [side_top.rev(), tummy] + rev(W_))),
          fill(FILL['black'], *(beak + arc_to(HC[0], HC[1], HR, HR, bkB, bkT, False)))], use='black'),
    step('Colour the tree', 'Colour the tree trunk brown.',
         [fill(FILL['brown'], *trunk)], use='brown'),
]

D = drawing('dx_woodpecker_w', 'W is for Woodpecker', 3, 15, 'animals', ['Letters', 'Animals'],
            'A woodpecker with a red cap, tapping on a tree trunk. The capital W is hiding in it: the W is its two pointed tail feathers.',
            steps, ['red', 'black', 'brown'])
json.dump(D, open(os.path.join(OUT, 'woodpecker.json'), 'w'))
json.dump({'set': 'animals-AZ', 'slot': 'W', 'kind': 'fly', 'age_from': 5}, open(os.path.join(OUT, 'woodpecker.place.json'), 'w'))
print('woodpecker: %d steps' % len(steps))
