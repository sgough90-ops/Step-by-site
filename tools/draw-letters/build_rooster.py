"""r is for rooster (Animals a to z, slot r). Side view, facing left.
The r: its straight line is the back of the rooster, where the tail feathers grow, and its arch is the bottom edge of
the top tail feather. The body starts at the top of the r and ends at its bottom: nothing crosses the r."""
import json, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

SX = 56.0; ST = 44.0; SB = 78.0

# ---- 1: the r ----
stick = Seg((SX, SB), (SX, ST + 4.5))
archS = (SX, ST + 4.5)
arch = [Seg(archS, (SX, 43.0), (63.0, 40.6), (71.0, 40.6))]
stick_full = Seg((SX, SB), (SX, ST))

# ---- 2: the body (from the top of the r round the head and chest to the bottom of the r) ----
neckB = Seg((SX, ST), (50.0, 40.0), (48.0, 32.0), (48.0, 26.0))
headB = Seg((48.0, 26.0), (48.0, 19.0), (43.0, 15.0), (38.0, 15.0))
headF = Seg((38.0, 15.0), (32.0, 15.0), (29.0, 20.0), (29.0, 26.0))
throat = Seg((29.0, 26.0), (29.0, 33.0), (33.0, 36.0), (33.0, 42.0))
chest = Seg((33.0, 42.0), (26.0, 48.0), (24.0, 56.0), (26.0, 64.0))
belly = Seg((26.0, 64.0), (29.0, 74.0), (38.0, 79.0), (46.0, 79.0))
under = Seg((46.0, 79.0), (51.0, 79.0), (54.0, 78.6), (SX, SB))
body = [neckB, headB, headF, throat, chest, belly, under]

# ---- 3: the comb, three bumps on top of the head ----
c0 = P(*headB.at(0.55)); c1 = P(*headF.at(0.35))
hb_a, hb_b = headB.split(0.55)
hf_a, hf_b = headF.split(0.35)
mx1, mx2 = 41.0, 36.0
comb = [Seg(c0, (46.0, 9.0), (42.0, 7.6), (41.2, 12.2)),
        Seg((41.2, 12.2), (40.0, 6.6), (35.4, 6.6), (35.6, 12.4)),
        Seg((35.6, 12.4), (33.2, 9.0), (29.2, 11.4), c1)]
comb_base = [hf_a.rev(), hb_b.rev()]        # c1 -> (38,15) -> c0

# ---- 4: the beak and the wattle ----
b0 = P(*headF.at(0.78)); b1 = P(*throat.at(0.12))
beak = [Seg(b0, (21.0, 25.4)), Seg((21.0, 25.4), b1)]
hf2a, hf2b = headF.split(0.78)
th_a, th_b = throat.split(0.12)
beak_base = [th_a.rev(), hf2b.rev()]         # b1 -> (29,26) -> b0
w0 = P(*throat.at(0.2)); w1 = P(*throat.at(0.62))
wattle = [Seg(w0, (24.6, 29.6), (23.4, 36.4), (27.2, 37.0)), Seg((27.2, 37.0), (29.4, 37.3), (30.2, 35.6), w1)]
t1, rest = throat.split(0.2)
mid_t = (0.62 - 0.2) / 0.8
t2, _ = rest.split(mid_t)
wattle_base = [t2.rev()]                     # w1 -> w0

# ---- 5: the eye ----
eye = circle(37.0, 23.0, 1.9)

# ---- 6: the wing ----
wing = [Seg((34.0, 60.0), (39.0, 53.0), (49.0, 52.5), (53.0, 58.0)), Seg((53.0, 58.0), (48.0, 64.0), (39.0, 65.0), (34.0, 60.0))]

# ---- 7: three tail feathers ----
top_low = Seg((71.0, 40.6), (78.0, 40.6), (84.0, 44.0), (87.0, 49.0))
top_up = [Seg((SX, ST), (57.0, 33.0), (72.0, 25.0), (84.0, 32.0)), Seg((84.0, 32.0), (89.0, 35.0), (91.0, 43.0), (87.0, 49.0))]
midF = [Seg((SX, 54.0), (66.0, 49.0), (80.0, 49.0), (90.0, 57.0)), Seg((90.0, 57.0), (80.0, 63.0), (66.0, 63.5), (SX, 61.0))]
lowF = [Seg((SX, 65.0), (65.0, 65.0), (75.0, 69.0), (79.0, 78.0)), Seg((79.0, 78.0), (69.0, 79.0), (61.0, 75.0), (SX, 71.0))]

# ---- 8: legs and feet ----
l1 = P(*belly.at(0.62)); l2 = P(*under.at(0.1))
def leg(top):
    x = top[0]; yb = 89.0
    return [line(Seg(top, (x, yb))), line(*poly((x - 5.0, yb + 2.0), (x, yb), (x + 4.0, yb + 2.0))), line(Seg((x, yb), (x - 2.0, yb + 3.0)))]

steps = [
    step('Start with an r', 'Draw a small letter r: a straight line down, then a little arch at the top going over to the right. This r is hiding in the rooster.',
         [line(stick_full), line(*arch)]),
    step('The body', 'From the top of the r, draw up the neck, round a head, down the front and round a big tummy to the bottom of the r.',
         [line(*body)]),
    step('The comb', 'Draw three round bumps on top of the head.',
         [line(*comb)]),
    step('Beak and wattle', 'Draw a pointed beak on the front of the head. Draw a little round wattle hanging under it.',
         [line(*beak), line(*wattle)]),
    step('The eye', 'Draw a small round eye on the head.',
         [ring(*eye)]),
    step('The wing', 'Draw a wing on the body: a long leaf shape.',
         [ring(*wing)]),
    step('Tail feathers', 'The arch of the r is a feather. Finish it with a big curve over the top. Then draw two more feathers under it.',
         [line(top_low), line(*top_up), line(*midF), line(*lowF)]),
    step('Legs and feet', 'Draw two straight legs under the tummy, with three toes on each foot.',
         leg(l1) + leg(l2)),
    step('Colour orange', 'Colour the body orange. Go round the wing and the eye.',
         [fill(FILL['orange'], *(body + [Seg((SX, SB), (SX, ST))]), cut=[d_fill(*wing), d_fill(*eye)])], use='orange'),
    step('Colour brown', 'Colour the wing brown.',
         [fill(FILL['brown'], *wing)], use='brown'),
    step('Colour red', 'Colour the comb and the wattle red.',
         [fill(FILL['red'], *(comb + comb_base)), fill(FILL['red'], *(wattle + wattle_base))], use='red'),
    step('Colour yellow', 'Colour the beak yellow. Colour the middle tail feather yellow too.',
         [fill(FILL['yellow'], *(beak + beak_base)), fill(FILL['yellow'], *(midF + [Seg((SX, 61.0), (SX, 54.0))]))], use='yellow'),
    step('Colour blue', 'Colour the top tail feather blue.',
         [fill(FILL['blue'], *(top_up + [top_low.rev()] + rev(arch) + [Seg(archS, (SX, ST))]))], use='blue'),
    step('Colour green', 'Colour the bottom tail feather green.',
         [fill(FILL['green'], *(lowF + [Seg((SX, 71.0), (SX, 65.0))]))], use='green'),
    step('Colour the eye', 'Colour the eye black.',
         [fill(FILL['black'], *eye)], use='black'),
]

D = drawing('dx_rooster_r', 'r is for rooster', 3, 15, 'animals', ['Letters', 'Animals'],
            'A proud rooster with a red comb and a bright tail. The small letter r is hiding in it: its straight line is the rooster\'s back and its arch is the bottom of the top tail feather.',
            steps, ['orange', 'brown', 'red', 'yellow', 'blue', 'green', 'black'])
json.dump(D, open(os.path.join(OUT, 'rooster.json'), 'w'))
json.dump({'set': 'animals-az', 'slot': 'r', 'kind': 'hop', 'age_from': 5}, open(os.path.join(OUT, 'rooster.place.json'), 'w'))
print('rooster: %d steps' % len(steps))
