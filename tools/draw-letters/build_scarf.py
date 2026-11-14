"""S is for Scarf (Around the house A to Z, slot S).
The S: one edge of the scarf (its inside edge at the top, its outside edge at the bottom). The other edge is a second
line beside it, the same shape. Stripes and tassels only touch the S: nothing crosses it."""
import json, math, os
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

CX = 50.0; Y1 = 32.5
R_S1, R_S2 = 12.0, 20.0            # the S: top curl, bottom curl
WID = 8.5
R_O1, R_O2 = R_S1 + WID, R_S2 - WID  # the second line: outside at the top, inside at the bottom
C1 = (CX, Y1); C2 = (CX, Y1 + R_S1 + R_S2)
A0, NSEG = 325.0, 6
UA = [A0 - (A0 - 90.0) * i / NSEG for i in range(NSEG + 1)]              # top curl: 325 down to 90
LA = [270.0 + (A0 - 90.0) * i / NSEG for i in range(NSEG + 1)]           # bottom curl: 270 up to 505

s_up = [on(C1[0], C1[1], R_S1, R_S1, a) for a in UA]; o_up = [on(C1[0], C1[1], R_O1, R_O1, a) for a in UA]
s_lo = [on(C2[0], C2[1], R_S2, R_S2, a) for a in LA]; o_lo = [on(C2[0], C2[1], R_O2, R_O2, a) for a in LA]
assert s_up[-1] == s_lo[0] and o_up[-1] == o_lo[0]

S_up = [arc_to(C1[0], C1[1], R_S1, R_S1, s_up[i], s_up[i + 1], False) for i in range(NSEG)]
S_lo = [arc_to(C2[0], C2[1], R_S2, R_S2, s_lo[i], s_lo[i + 1], True) for i in range(NSEG)]
O_up = [arc_to(C1[0], C1[1], R_O1, R_O1, o_up[i], o_up[i + 1], False) for i in range(NSEG)]
O_lo = [arc_to(C2[0], C2[1], R_O2, R_O2, o_lo[i], o_lo[i + 1], True) for i in range(NSEG)]
flat = lambda pieces: [s for p in pieces for s in p]

# ---- 1: the S ----
S_ = flat(S_up) + flat(S_lo)
# ---- 2: the second line ----
O_ = flat(O_up) + flat(O_lo)
# ---- 3: the ends and the tassels ----
end_top = Seg(s_up[0], o_up[0]); end_bot = Seg(s_lo[-1], o_lo[-1])
def tassels(p, q, ang, n=4, length=5.6):
    dx, dy = -math.sin(math.radians(ang)), math.cos(math.radians(ang))     # the way the scarf is going
    out = []
    for k in range(n):
        x = p[0] + (q[0] - p[0]) * k / (n - 1); y = p[1] + (q[1] - p[1]) * k / (n - 1)
        out.append(Seg((x, y), (x + dx * length, y + dy * length)))
    return out
# at the top end the scarf "goes on" backwards along the curl (towards bigger angles); at the bottom end forwards
tas_top = tassels(s_up[0], o_up[0], UA[0]); tas_bot = tassels(s_lo[-1], o_lo[-1], LA[-1])
# ---- 4: the stripes ----
str_up = [Seg(s_up[i], o_up[i]) for i in range(1, NSEG + 1)]     # the last one is where the two curls join
str_lo = [Seg(s_lo[i], o_lo[i]) for i in range(1, NSEG)]

def band(Sp, Op, sp, op, i):
    """One stripe of the scarf, between cross lines i and i + 1."""
    return Sp[i] + [Seg(sp[i + 1], op[i + 1])] + rev(Op[i]) + [Seg(op[i], sp[i])]
reds = [band(S_up, O_up, s_up, o_up, i) for i in (0, 2, 4)] + [band(S_lo, O_lo, s_lo, o_lo, i) for i in (0, 2, 4)]

steps = [
    step('Start with an S', 'Draw a big capital S with a small curl at the top and a bigger curl at the bottom. This S is hiding in the scarf.',
         [line(*S_)]),
    step('A second line', 'Draw another line beside the S, the same shape. Keep it outside the S at the top and inside the S at the bottom.',
         [line(*O_)]),
    step('The ends', 'Join the two lines at each end with a short line. Then draw four little lines sticking out of each end for the tassels.',
         [line(end_top), line(end_bot)] + [line(t) for t in tas_top + tas_bot]),
    step('Stripes at the top', 'Draw six lines across the top half of the scarf, from one edge to the other.',
         [line(s) for s in str_up]),
    step('Stripes at the bottom', 'Draw five lines across the bottom half of the scarf.',
         [line(s) for s in str_lo]),
    step('Colour red', 'Colour every other stripe red, starting at the top end. Leave the stripes in between white.',
         [fill(FILL['red'], *r) for r in reds], use='red'),
]

D = drawing('dx_scarf_s', 'S is for Scarf', 2, 10, 'things', ['Letters', 'Around the house'],
            'A long stripy scarf with tassels at both ends. The capital S is hiding in it: the S is one edge of the scarf, all the way along.',
            steps, ['red'])
json.dump(D, open(os.path.join(OUT, 'scarf.json'), 'w'))
json.dump({'set': 'house-AZ', 'slot': 'S', 'kind': 'key', 'age_from': 5}, open(os.path.join(OUT, 'scarf.place.json'), 'w'))
print('scarf: %d steps' % len(steps))
