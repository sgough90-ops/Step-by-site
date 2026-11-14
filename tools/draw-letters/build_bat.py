"""V is for Vampire bat (Animals A to Z, slot V). Front view, wings open.
The V: its two lines are the sides of the bat's body, coming to a point at the feet.
The round head sits on the top of the V and the wings hang from its sides: nothing crosses the V."""
import json, math, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

HC = (50.0, 31.0); HR = 15.0
VL = on(HC[0], HC[1], HR, HR, 140); VR = on(HC[0], HC[1], HR, HR, 40)
VP = (50.0, 80.0)

# ---- 1: the V ----
V_ = [Seg(VL, VP), Seg(VP, VR)]

# ---- 2: the head ----
head = circle(HC[0], HC[1], HR)
chin = arc_to(HC[0], HC[1], HR, HR, VR, VL, True)          # the bottom of the head, between the tops of the V

# ---- 3: the ears ----
e0 = on(HC[0], HC[1], HR, HR, 200); e1 = on(HC[0], HC[1], HR, HR, 252)
earL = [Seg(e0, (31.0, 19.0), (30.6, 11.0), (32.6, 5.6)), Seg((32.6, 5.6), (38.6, 8.4), (43.2, 12.6), e1)]
earR = mirror(earL)
# ---- 4: the insides of the ears ----
i0 = on(HC[0], HC[1], HR, HR, 211); i1 = on(HC[0], HC[1], HR, HR, 241)
inL = [Seg(i0, (34.6, 18.4), (34.2, 14.6), (34.8, 11.2)), Seg((34.8, 11.2), (38.2, 13.0), (40.8, 15.4), i1)]
inR = mirror(inL)

# ---- 5, 6: the wings ----
A = on(HC[0], HC[1], HR, HR, 166)
W_ = (20.0, 21.0); T = (5.0, 47.0); S1 = (19.0, 60.0); S2 = (34.0, 70.0)
wingL = [Seg(A, (31.0, 31.0), (25.0, 24.0), W_),
         Seg(W_, (12.0, 26.0), (6.0, 36.0), T),
         Seg(T, (10.0, 47.5), (17.0, 52.0), S1),
         Seg(S1, (24.0, 58.0), (32.0, 62.0), S2),
         Seg(S2, (39.0, 68.0), (45.0, 73.0), VP)]
wingR = mirror(wingL)
sideL = arc_to(HC[0], HC[1], HR, HR, VL, A, True)           # the bit of the head between the V and the wing

# ---- 7: the feet ----
footL = [Seg(VP, (45.6, 80.6), (41.8, 84.6), (43.2, 88.2)), Seg((43.2, 88.2), (44.6, 91.4), (49.2, 89.4), VP)]
footR = mirror(footL)

# ---- 8: eyes and nose ----
eyeL = circle(44.0, 28.0, 2.3); eyeR = circle(56.0, 28.0, 2.3)

# ---- 9: mouth and fangs ----
MY = 37.0
mouth = [Seg((43.0, 34.4), (44.0, 36.4), (45.0, MY), (46.0, MY)), Seg((46.0, MY), (54.0, MY)), Seg((54.0, MY), (55.0, MY), (56.0, 36.4), (57.0, 34.4))]
fangL = poly((46.6, MY), (48.1, 41.4), (49.6, MY))
fangR = mirror(fangL)
fangL_fill = fangL + [Seg((49.6, MY), (46.6, MY))]
fangR_fill = [Seg((53.4, MY), (51.9, 41.4)), Seg((51.9, 41.4), (50.4, MY)), Seg((50.4, MY), (53.4, MY))]

def ear_fill(ear, inner, mir=False):
    """The outside part of an ear: round the ear, along the head, up and over the inside line, along the head again."""
    if not mir:
        return ear + arc_to(HC[0], HC[1], HR, HR, ear[-1].b, inner[-1].b, False) + rev(inner) + arc_to(HC[0], HC[1], HR, HR, inner[0].a, ear[0].a, False)
    return ear + arc_to(HC[0], HC[1], HR, HR, ear[-1].b, inner[-1].b, True) + rev(inner) + arc_to(HC[0], HC[1], HR, HR, inner[0].a, ear[0].a, True)

def in_fill(inner, mir=False):
    return inner + arc_to(HC[0], HC[1], HR, HR, inner[-1].b, inner[0].a, mir)

steps = [
    step('Start with a V', 'Draw a big capital V: two straight lines that meet in a point at the bottom. This V is hiding in the bat.',
         [line(*V_)]),
    step('The head', 'Draw a big round head sitting on the top of the V. The two ends of the V touch it.',
         [ring(*head)]),
    step('The ears', 'Draw two big pointed ears on top of the head.',
         [line(*earL), line(*earR)]),
    step('Inside the ears', 'Draw a smaller pointed shape inside each ear.',
         [line(*inL), line(*inR)]),
    step('The left wing', 'Start at the side of the head. Go up to a point and down to a tip. Come back to the bottom of the V in three curves.',
         [line(*wingL)]),
    step('The right wing', 'Draw the same wing on the other side.',
         [line(*wingR)]),
    step('The feet', 'Draw two little feet hanging from the point of the V.',
         [ring(*footL), ring(*footR)]),
    step('The eyes', 'Draw two round eyes on the head.',
         [ring(*eyeL), ring(*eyeR)]),
    step('Mouth and fangs', 'Draw a smile with a flat middle. Draw two little pointed fangs hanging from it.',
         [line(*mouth), line(*fangL), line(*fangR)]),
    step('Colour purple', 'Colour the head, the body, the ears and the feet purple. Go round the eyes and the fangs. Leave the insides of the ears.',
         [fill(FILL['purple'], *head, cut=[d_fill(*eyeL), d_fill(*eyeR), d_fill(*fangL_fill), d_fill(*fangR_fill)]),
          fill(FILL['purple'], *(V_ + chin)),
          fill(FILL['purple'], *ear_fill(earL, inL)), fill(FILL['purple'], *ear_fill(earR, inR, True)),
          fill(FILL['purple'], *footL), fill(FILL['purple'], *footR)], use='purple'),
    step('Colour black', 'Colour the two wings black. Colour the eyes black too.',
         [fill(FILL['black'], *(wingL + [Seg(VP, VL)] + sideL)), fill(FILL['black'], *(wingR + [Seg(VP, VR)] + mirror(sideL))),
          fill(FILL['black'], *eyeL), fill(FILL['black'], *eyeR)], use='black'),
    step('Colour pink', 'Colour the insides of the ears pink.',
         [fill(FILL['pink'], *in_fill(inL)), fill(FILL['pink'], *in_fill(inR, True))], use='pink'),
]

D = drawing('dx_vampirebat_v', 'V is for Vampire bat', 3, 15, 'animals', ['Letters', 'Animals'],
            'A friendly bat with big ears, wide wings and two little fangs. The capital V is hiding in it: its two lines are the sides of the bat\'s body.',
            steps, ['purple', 'black', 'pink'])
json.dump(D, open(os.path.join(OUT, 'bat.json'), 'w'))
json.dump([d_fill(*fangL_fill), d_fill(*fangR_fill)], open(os.path.join(OUT, 'bat.white.json'), 'w'))
json.dump({'set': 'animals-AZ', 'slot': 'V', 'kind': 'fly', 'age_from': 5}, open(os.path.join(OUT, 'bat.place.json'), 'w'))
print('bat: %d steps' % len(steps))
