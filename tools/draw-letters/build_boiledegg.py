"""e is for Egg (dx_egg_e), Food and drink a to z, slot e (22 Nov 2026).
From his pick "e2 A boiled egg and a spoon" (Claude's sketches, claude/step-by-draw-food-small-11-ideas-4-versions.md).

A boiled egg in a blue egg cup on a plate, with a spoon standing next to the cup. The e is the egg and the top of the cup:
its straight line is where the egg sits in the cup.

    python3 build_boiledegg.py
"""
import math
from fkit import *

LBROWN, BLUE, GREY, LBLUE = FILL['lbrown'], FILL['blue'], FILL['grey'], FILL['lblue']
EX, EY, ERX, ERY = 50.0, 50.0, 15.0, 16.5
E_END = P(64.8, 55.2)


def rot_segs(segs, c, deg):
    a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
    out = []
    for s in segs:
        out.append(Seg(*[(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in s.p]))
    for i in range(len(out) - 1): set_b(out[i], out[i + 1].a)
    set_b(out[-1], out[0].a)
    return out


def ray(p, q, ext0=0, ext1=0):
    dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    return Seg((p[0] - ux * ext0, p[1] - uy * ext0), (q[0] + ux * ext1, q[1] + uy * ext1))


top = arc(EX, EY, ERX, ERY, 0, -180, start=P(EX + ERX, EY), end=P(EX - ERX, EY))
low = [Seg((EX - ERX, EY), (35, 61.5), (41.5, 70), (50, 70)), Seg((50, 70), (58.5, 70), (64.2, 62.5), E_END)]
net = Net()
net.add('e', Seg((EX - ERX, EY), (EX + ERX, EY)), top, low)                         # 1: the e
closer = Seg(E_END, (65.0, 53.4), (65.0, 51.7), (EX + ERX, EY))
net.add('close', closer)                                                            # 2: close the cup, and its stem
net.add('stemL', Seg((46.3, 66), (44.5, 88))); net.add('stemR', Seg((53.7, 66), (55.5, 88)))
foot = ell(50, 87.5, 15, 3.4, start=180)
net.add('foot', foot)                                                               # 3: the foot
# 4: the spoon, standing beside the cup with its bowl at the top (27 Nov 2026: he could not tell the old one was a spoon)
TH = math.radians(17.0)                                 # leans 17 degrees towards the cup
SA = (84.0, 90.0)                                       # middle of the round end of the handle, on the plate
SU, SN = (-math.sin(TH), -math.cos(TH)), (math.cos(TH), -math.sin(TH))


def W(s, t):
    """s along the spoon from the end of the handle, t across it (plus is away from the cup)"""
    return (round(SA[0] + s * SU[0] + t * SN[0], 3), round(SA[1] + s * SU[1] + t * SN[1], 3))


R0, NK, NW, BW, BS, TIP = 1.7, 29.5, 0.9, 5.6, 39.0, 45.5
spoon = [Seg(W(R0, R0), W(NK, NW)),
         Seg(W(NK, NW), W(NK + 2.6, NW + 0.2), W(BS - 4.2, BW), W(BS, BW)),
         Seg(W(BS, BW), W(BS + 3.9, BW), W(TIP, BW * 0.56), W(TIP, 0)),
         Seg(W(TIP, 0), W(TIP, -BW * 0.56), W(BS + 3.9, -BW), W(BS, -BW)),
         Seg(W(BS, -BW), W(BS - 4.2, -BW), W(NK + 2.6, -NW - 0.2), W(NK, -NW)),
         Seg(W(NK, -NW), W(R0, -R0)),
         Seg(W(R0, -R0), W(R0 - R0 * 4 / 3, -R0), W(R0 - R0 * 4 / 3, R0), W(R0, R0))]
net.add('spoon', *spoon)
sshine = line(Seg(W(BS - 3.2, 1.9), W(BS - 1.6, 3.0), W(BS + 1.8, 3.1), W(BS + 3.4, 2.0)))
plate = ell(55, 91, 36, 6, start=180)
net.add('plate', plate)                                                             # 5: the plate
net.region('cup', Seg((EX - ERX, EY), (EX + ERX, EY)), closer.rev(), rev(low))
net.region('footR', foot); net.region('spoonR', *spoon)
net.node()
for nm in ('stemL', 'stemR'): net.hide(nm, 'cup', 'footR')
net.hide('plate', 'footR', 'spoonR')
shine = line(*arc(EX, EY, 11.0, 12.2, 212, 246))
speck = [dot(x, y, w=2.2) for x, y in ((44, 43.5), (51.5, 39), (57, 45), (48, 46.6), (58.5, 39.6))]

steps = [
    step('Start with an e', 'Draw a small letter e: a straight line across, then go up, round and down to make a curl.', net.lines('e')),
    step('The egg cup', 'Draw a short line to close the e. Under it, draw two lines going down for the stem of the cup.', net.lines('close', 'stemL', 'stemR')),
    step('The foot', 'At the bottom of the stem, draw a flat oval for the foot of the egg cup.', net.lines('foot')),
    step('The spoon', 'Draw a spoon standing next to the cup: a long thin handle with a round end, and a big round bowl at the top. Draw a little curve in the bowl for its shine.', net.lines('spoon') + [sshine]),
    step('The plate', 'Draw a big flat plate under the egg cup and the spoon.', net.lines('plate')),
    step('Speckles', 'The top of the e is the egg. Draw a curved line for the shine and some little speckles on it.', [shine] + speck),
    step('Colour the egg', 'Colour the egg light brown.', [net.fill(LBROWN, (50, 42), names=['e'])], use='lbrown'),
    step('Colour blue', 'Colour the egg cup blue: the cup, the stem and the foot.',
         [net.fill(BLUE, (50, 60), names=['e', 'close']), net.fill(BLUE, (50, 78), names=['e', 'stemL', 'stemR', 'foot']),
          net.fill(BLUE, (50, 88.5), names=['foot'])], use='blue'),
    step('Colour the spoon', 'Colour the spoon grey.',
         [net.fill(GREY, W(BS, 0), names=['spoon'])], use='grey'),
    step('Colour the plate', 'Colour the plate light blue.', [net.fill(LBLUE, (40, 94), names=['plate', 'foot', 'spoon'])], use='lblue'),
]

D0 = drawing('dx_egg_e', 'e is for Egg', 2, 10, 'things', ['Letters', 'Around the house'],
            'A boiled egg in an egg cup, with a spoon. The small letter e is hiding in it: it is the egg and the top of the cup.',
            steps, ['lbrown', 'blue', 'grey', 'lblue'])
D = scale(D0, 1.25, 75.0, 97.0)                     # the whole picture a bit bigger, to fill the paper
save('boiledegg', D, {'set': 'house-az', 'slot': 'e', 'kind': 'key', 'age_from': 4})
