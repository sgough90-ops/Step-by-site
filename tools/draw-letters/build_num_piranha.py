"""5 is for Piranha (Animals 1 to 9, slot 5). From his shark screenshot, 21 Nov 2026.
The 5: flat hat = top of the head, short line down = front of the top jaw, belly = the inside of the open mouth.
Faces left. Grey back, red tummy, red eye.
"""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'); os.makedirs(OUT, exist_ok=True)

# ---- the 5 ----
HAT_R, CORNER, STEM_B = P(42, 30), P(21, 30), P(21, 47)
belly1 = Seg(STEM_B, (28, 42.5), (45, 43.5), (46, 57))      # top jaw underside and back of the mouth
belly2 = Seg((46, 57), (46, 67.5), (35, 73), (23, 70))       # bottom of the mouth, ending at the bottom lip
five = poly(HAT_R, CORNER, STEM_B) + [belly1, belly2]
LIP = belly2.b

# ---- back and tail ----
back = Seg(HAT_R, (54, 23), (70, 27), (79, 44))
TJ_TOP, TJ_BOT = back.b, P(79, 58)
tail = curve(TJ_TOP, (83, 39), (88, 34), (94, 31), (91, 40), (88, 46), (88, 51), (88, 56), (91, 62), (94, 71), (88, 68), (83, 63), TJ_BOT)

# ---- tummy (bottom of the body and the chin) ----
under = curve(TJ_BOT, (71, 77), (45, 83), (30, 77.5), (26, 76), (23.5, 73.5), LIP)

# ---- teeth: two hanging from the top jaw, two standing on the bottom jaw ----
def teeth(seg, ts, down):
    """One line per tooth, each starting and ending on the jaw."""
    pts = [P(*seg.at(t)) for t in ts]
    out = []
    for a, b in zip(pts, pts[1:]):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        out.append(poly(a, P(mx, my + (5.5 if down else -5.5)), b))
    return out
top_teeth = teeth(belly1, [0.07, 0.2, 0.33], True)
bot_teeth = teeth(belly2, [0.62, 0.76, 0.9], False)

# ---- eye ----
EYE = (33, 37.5)
eye = circle(EYE[0], EYE[1], 3.6)
pupil = circle(EYE[0] - 0.8, EYE[1], 1.5)

# ---- fins ----
b1, rest = back.split(0.42)
fin_base_a = b1.b
mid, b3 = rest.split(0.45)
fin_base_b = mid.b
fin_top = curve(fin_base_a, (61, 20), (66, 17), (70, 15.5), (69, 21), (69.5, 25), fin_base_b)
side_fin = poly((60, 48), (53, 52), (60, 56))
u1, urest = under[0].split(0.3)
afin_a = u1.b
umid, u3 = urest.split(0.3)
afin_b = umid.b
bottom_fin = curve(afin_a, (68, 77), (67, 81), (69, 85), (63, 83), (59, 81), afin_b)

# ---- the line between the grey back and the red tummy ----
m1, m2 = belly2.split(0.28)
D = m1.b
divider = curve(D, (54, 69), (68, 66), TJ_BOT)

# ---- bubbles ----
bub1 = circle(11, 44, 2.4)
bub2 = circle(8, 36, 1.5)

# ---- colours ----
eye_d = d_fill(*eye); pupil_d = d_fill(*pupil)
grey_path = [back] + tail + rev(divider) + rev([belly1, m1]) + poly(STEM_B, CORNER, HAT_R)
# tummy: D -> divider -> TJ_BOT -> under -> LIP -> back along belly2 (m2 reversed) -> D
red_path = divider + under + rev([m2])
fin_grey = fin_top + rev([mid])
fin_red = bottom_fin + rev([umid])

steps = [
    step('Start with a 5', 'Draw a number 5: a flat line across the top, a short line down, then a big round belly. This 5 is hiding in the piranha.',
         [line(*five)]),
    step('The back and tail', 'From the right end of the 5, draw a curved back. Then draw a big tail with two points.',
         [line(back), line(*tail)]),
    step('The tummy', 'From the bottom of the tail, draw a round tummy all the way to the bottom of the 5.', [line(*under)]),
    step('Sharp teeth', 'Draw two pointy teeth hanging down from the top jaw and two pointing up from the bottom jaw.',
         [line(*t) for t in top_teeth + bot_teeth]),
    step('The eye', 'Draw a round eye just under the top of the 5, with a smaller circle inside it.',
         [ring(*eye), ring(*pupil)]),
    step('Fins', 'Draw a pointy fin on its back, a small fin under its tummy, and a little fin on its side.',
         [line(*fin_top), line(*bottom_fin), line(*side_fin)]),
    step('The red tummy', 'Draw a curved line from the bottom of the mouth to the tail. Below it is the red tummy.', [line(*divider)]),
    step('Bubbles', 'Draw two bubbles in front of its mouth.', [ring(*bub1), ring(*bub2)]),
    step('Colour grey', 'Colour its back, its tail and the fin on its back grey. Leave the eye.',
         [fill(FILL['grey'], *grey_path, cut=[eye_d]), fill(FILL['grey'], *fin_grey)], use='grey'),
    step('Colour red', 'Colour the tummy, the fin under it and the eye red.',
         [fill(FILL['red'], *red_path), fill(FILL['red'], *fin_red), fill(FILL['red'], *eye, cut=[pupil_d])], use='red'),
    step('Colour black', 'Colour the middle of the eye black.', [fill(FILL['black'], *pupil)], use='black'),
]
D_ = drawing('dx_piranha_5', '5 is for Piranha', 2, 10, 'animals', ['Numbers', 'Animals'],
             'A piranha with its mouth wide open and sharp teeth. The number 5 is hiding in it: the top of its head, the front of its jaw and the inside of its open mouth.',
             steps, ['grey', 'red', 'black'])
json.dump(D_, open(os.path.join(OUT, 'num5piranha.json'), 'w'))
json.dump({'set': 'animals-09', 'slot': '5', 'kind': 'swim', 'age_from': 5}, open(os.path.join(OUT, 'num5piranha.place.json'), 'w'))
print('steps', len(steps), 'bytes', len(json.dumps(D_, separators=(',', ':'))))
