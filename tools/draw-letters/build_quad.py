"""Q is for Quad bike (Vehicles A to Z, slot Q). Side view, facing left.
The Q: its circle is the big back wheel and its tail is the dust kicked up behind it.
Nothing crosses the Q: the spokes stay clear of the tail, the mudguard goes round the wheel with a gap."""
import json, math, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

BC = (68.0, 69.0); BR = 15.0          # back wheel = the Q
FC = (25.0, 72.5); FR = 11.5          # front wheel
TAIL_A = 45.0

def at(c, r, a):
    return P(c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))

# ---- 1: the Q ----
Qc = circle(BC[0], BC[1], BR)
tail = Seg(at(BC, 9.0, TAIL_A), at(BC, 22.5, TAIL_A))

# ---- 2: the back wheel's middle: a hub and five spokes that keep clear of the tail ----
HR = 4.0
hubB = circle(BC[0], BC[1], HR)
SP = [TAIL_A + 36 + 72 * k for k in range(5)]          # 81, 153, 225, 297, 369
spokesB = [Seg(at(BC, HR, a), at(BC, BR, a)) for a in SP]

# ---- 3: the front wheel, the same way ----
fw = circle(FC[0], FC[1], FR)
hubF = circle(FC[0], FC[1], 3.2)
spokesF = [Seg(at(FC, 3.2, a), at(FC, FR, a)) for a in (-90 + 72 * k for k in range(5))]

# ---- 4: the body: mudguards over both wheels, the seat-top line, the bump at the front ----
FG = 15.0; RG = 18.5
f0, f1 = at(FC, FG, 195), at(FC, FG, 345)
r0, r1 = at(BC, RG, 200), at(BC, RG, 340)
body = arc(FC[0], FC[1], FG, FG, 195, 345, start=f0, end=f1) + [Seg(f1, r0)] + \
       arc(BC[0], BC[1], RG, RG, 200, 340, start=r0, end=r1) + \
       [Seg(r1, (88.4, 59.2), (89.2, 52.0), (89.2, 48.2)),
        Seg((89.2, 48.2), (89.2, 46.3), (87.9, 45.0), (86.0, 45.0)),
        Seg((86.0, 45.0), (46.0, 45.0)),
        Seg((46.0, 45.0), (43.0, 45.0), (41.0, 38.5), (36.0, 38.5)),
        Seg((36.0, 38.5), (29.0, 38.5)),
        Seg((29.0, 38.5), (24.0, 38.5), (16.0, 46.0), (12.0, 52.0)),
        Seg((12.0, 52.0), (9.6, 55.6), (9.2, 63.0), f0)]

# ---- 5: the seat ----
seat = [Seg((48.0, 45.0), (48.0, 41.6), (49.8, 40.0), (53.0, 40.0)), Seg((53.0, 40.0), (66.0, 40.0)),
        Seg((66.0, 40.0), (69.2, 40.0), (71.0, 41.8), (71.0, 45.0))]

# ---- 6: the handlebars: a post and a bar ----
BAR = rrect(23.0, 25.0, 40.0, 29.0, 2.0)
postL = Seg((31.0, 38.5), (31.0, 29.0)); postR = Seg((33.6, 38.5), (33.6, 29.0))

# ---- 7: the rack on the back ----
rack = poly((73.0, 45.0), (75.4, 37.0), (88.0, 37.0), (85.6, 45.0))
def slat(x):
    return Seg((x, 45.0), (x + 2.4, 37.0))
slats = [slat(76.6), slat(79.6), slat(82.6)]

# ---- 8: the headlight ----
lamp = circle(21.2, 48.0, 2.4)

# ---- 9: dust puffs at the end of the tail ----
T = tail.b
puff = [Seg(T, (T[0] + 0.2, T[1] + 2.6), (T[0] + 3.0, T[1] + 4.0), (T[0] + 5.0, T[1] + 2.4)),
        Seg((T[0] + 5.0, T[1] + 2.4), (T[0] + 7.6, T[1] + 3.6), (T[0] + 10.0, T[1] + 0.4), (T[0] + 7.6, T[1] - 1.8)),
        Seg((T[0] + 7.6, T[1] - 1.8), (T[0] + 7.0, T[1] - 5.2), (T[0] + 2.6, T[1] - 5.4), P(*tail.at(0.84)))]

steps = [
    step('Start with a Q', 'Draw a big capital Q: a round circle with a short tail sticking out at the bottom. This Q is hiding in the quad bike.',
         [ring(*Qc), line(tail)]),
    step('The back wheel', 'Draw a small circle in the middle of the Q. Draw five spokes out to the edge. Keep them away from the tail.',
         [ring(*hubB)] + [line(s) for s in spokesB]),
    step('The front wheel', 'Draw a smaller wheel on the left, in the same way: a circle, a little circle in the middle and five spokes.',
         [ring(*fw), ring(*hubF)] + [line(s) for s in spokesF]),
    step('The body', 'Draw a curved mudguard over each wheel and join them. Go up the back, along the top, over a bump and down the front.',
         [ring(*body)]),
    step('The seat', 'Draw a long seat on the top of the body.',
         [line(*seat)]),
    step('The handlebars', 'Draw a short post up from the bump at the front. Put a long bar on top of it.',
         [line(postL), line(postR), ring(*BAR)]),
    step('The rack', 'Draw a rack on the back: a sloping box on the top, with three lines in it.',
         [line(*rack)] + [line(s) for s in slats]),
    step('The light', 'Draw a round light on the front of the body.',
         [ring(*lamp)]),
    step('Dust', 'Draw a puff of dust at the end of the tail. The quad bike is going fast!',
         [line(*puff)]),
    step('Colour red', 'Colour the body red. Go round the light.',
         [fill(FILL['red'], *body, cut=[d_fill(*lamp)])], use='red'),
    step('Colour grey', 'Colour both wheels grey, round the little circles in the middle. Colour the rack and the post grey too.',
         [fill(FILL['grey'], *Qc, cut=[d_fill(*hubB)]), fill(FILL['grey'], *fw, cut=[d_fill(*hubF)]),
          fill(FILL['grey'], *close(rack)), fill(FILL['grey'], *poly((31.0, 38.5), (31.0, 29.0), (33.6, 29.0), (33.6, 38.5), closed=True))], use='grey'),
    step('Colour black', 'Colour the seat and the handlebars black. Colour the middles of the wheels black too.',
         [fill(FILL['black'], *close(seat)), fill(FILL['black'], *BAR), fill(FILL['black'], *hubB), fill(FILL['black'], *hubF)], use='black'),
    step('Colour the light', 'Colour the light yellow.',
         [fill(FILL['yellow'], *lamp)], use='yellow'),
]

D = drawing('dx_quadbike_q', 'Q is for Quad bike', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
            'A red quad bike racing along with dust flying behind it. The capital Q is hiding in it: the circle is the big back wheel and the tail is the dust.',
            steps, ['red', 'grey', 'black', 'yellow'])
json.dump(D, open(os.path.join(OUT, 'quad.json'), 'w'))
json.dump({'set': 'vehicles-AZ', 'slot': 'Q', 'kind': 'drive', 'age_from': 5}, open(os.path.join(OUT, 'quad.place.json'), 'w'))
print('quad: %d steps' % len(steps))
