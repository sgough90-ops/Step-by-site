"""x is for Xantus's hummingbird (dx_hummingbird_x), Animals a to z, slot x (21 Nov 2026).
From Claude's sketch 'Xantus's hummingbird (hovering, from the front)' (design 1 of four, the closest to his picture:
hovering with its wings spread and its beak up to a flower). In his picture the middle of the X was hidden behind the
bird's body; here the whole x stays in view: the top half of the x is the bottom of its body narrowing to a point, the
bottom half is the two sides of its spread tail (an hourglass). Head green, body orange, wings brown, tail red, flower
pink with a green cap. Sketch coordinates (200 x 200) go onto the paper by T().
"""
import math, re
from r5kit import *

PA = Paper(0.58, -15, 3)
T = PA.T
GRN, ORA, BRN, RED, PNK = FILL['green'], FILL['orange'], FILL['brown'], FILL['red'], FILL['pink']


def chain(d):
    toks = re.findall(r'[MCLQ]|-?\d+\.?\d*', d)
    out = []; cur = None; i = 0; cmd = None
    while i < len(toks):
        t = toks[i]
        if t in 'MCLQ':
            cmd = t; i += 1; continue
        if cmd == 'M':
            cur = T(float(toks[i]), float(toks[i + 1])); i += 2
        elif cmd == 'C':
            c1 = T(float(toks[i]), float(toks[i + 1])); c2 = T(float(toks[i + 2]), float(toks[i + 3])); p = T(float(toks[i + 4]), float(toks[i + 5]))
            out.append(Seg(cur, c1, c2, p)); cur = p; i += 6
        elif cmd == 'Q':
            q = T(float(toks[i]), float(toks[i + 1])); p = T(float(toks[i + 2]), float(toks[i + 3]))
            out.append(q2c(cur, q, p)); cur = p; i += 4
        elif cmd == 'L':
            p = T(float(toks[i]), float(toks[i + 1])); out.append(Seg(cur, p)); cur = p; i += 2
    return out


def scallops(pts, bump):
    """bumpy edge through sketch points (quadratic bumps, bump > 0 bulges to the left of travel as seen on screen)"""
    d = 'M%s,%s' % pts[0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        d += ' Q%.2f,%.2f %s,%s' % (mx + nx * bump, my + ny * bump, x1, y1)
    return chain(d)


# ---- 1: the x ----
UL, LR, UR, LL, XC = T(78, 98), T(122, 150), T(122, 98), T(78, 150), T(100, 124)
xa = [Seg(UL, XC), Seg(XC, LR)]
xb = [Seg(UR, XC), Seg(XC, LL)]

# ---- the body and head, over the top of the x ----
BODY = chain('M78,98 C70,86 72,72 84,66 C82,52 90,38 104,38 C118,38 126,50 122,60 C130,68 130,86 122,98')
assert BODY[0].a == UL and BODY[-1].b == UR
N1, N2 = BODY[0].b, BODY[2].b                              # the neck line goes from here to here
LW = [P(*BODY[0].at(t)) for t in (0.3, 0.7)]               # the left wing meets the body
RW = [P(*BODY[3].at(t)) for t in (0.3, 0.7)]               # and the right wing
BK = P(*BODY[2].at(0.62))                                   # the beak starts here
BODY, ex = cut_at_points(BODY, LW + RW + [BK])
LW2, LW1, RW1, RW2, BK = ex
neck = [Seg(N1, T(92, 72), T(112, 72), N2)]

# ---- the tail: a bumpy edge across the bottom of the x, and three lines ----
TP = [(122, 150), (111, 155), (100, 157), (89, 155), (78, 150)]
TAIL = snap(scallops(TP, 3), LR, LL)
R_end = [TAIL[1].b, TAIL[2].b, TAIL[0].b]                  # (100,157), (89,155), (111,155)
RS = T(100, 134)
rays = [Seg(RS, p) for p in R_end]

# ---- the wings ----
def wing(base1, base2, tip, mids, bump):
    t = T(*tip)
    ql = P((base1[0] + t[0]) / 2 + (t[1] - base1[1]) * 0.08, (base1[1] + t[1]) / 2 - (t[0] - base1[0]) * 0.08)
    lead = [q2c(base1, ql, t)]
    # sketch points of the trailing edge, then onto the paper
    b2 = ((base2[0] - PA.ox) / PA.s, (base2[1] - PA.oy) / PA.s)
    trail = snap(scallops([tip] + mids + [b2], bump), t, base2)
    return lead + trail
wingL = wing(LW1, LW2, (36, 36), [(38, 54), (46, 66), (55, 76), (64, 84)], -3)
wingR = wing(RW1, RW2, (182, 62), [(174, 72), (162, 80), (148, 85), (137, 86)], 3)
featL = [Seg(T(44, 54), T(60, 70)), Seg(T(51, 65), T(63, 76))]
featR = [Seg(T(166, 69), T(142, 76)), Seg(T(155, 77), T(139, 80))]

# ---- the flower at the tip of its beak ----
a = math.radians(-40); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
mx, my = 172, 28; Lb, w0, w1 = 18, 6, 2.5
p1 = (mx + nx * w0, my + ny * w0); p2 = (mx - nx * w0, my - ny * w0)
b1 = (mx + ux * Lb + nx * w1, my + uy * Lb + ny * w1); b2 = (mx + ux * Lb - nx * w1, my + uy * Lb - ny * w1)
bell = [Seg(T(*p1), T(mx + ux * 7 + nx * 5, my + uy * 7 + ny * 5), T(b1[0] - ux * 5, b1[1] - uy * 5), T(*b1)),
        Seg(T(*b1), T(*b2)),
        Seg(T(*b2), T(b2[0] - ux * 5, b2[1] - uy * 5), T(mx + ux * 7 - nx * 5, my + uy * 7 - ny * 5), T(*p2))]
lip = q2c(T(*p2), T(mx - ux * 3, my - uy * 3), T(*p1))
BM = P(*lip.at(0.5))                                       # the beak's tip touches the middle of the lip
lip1, lip2 = lip.split(0.5); BM = lip1.b
cap_tip = (mx + ux * (Lb + 5), my + uy * (Lb + 5))
cap = [Seg(T(*b1), T(b1[0] + ux * 3, b1[1] + uy * 3), T(cap_tip[0] + nx * 2, cap_tip[1] + ny * 2), T(*cap_tip)),
       Seg(T(*cap_tip), T(cap_tip[0] - nx * 2, cap_tip[1] - ny * 2), T(b2[0] + ux * 3, b2[1] + uy * 3), T(*b2))]
stem = [Seg(T(*cap_tip), T(cap_tip[0] + 2, cap_tip[1] - 4), T(190, 8), T(192, 6))]
beak = [Seg(BK, BM)]
eye = dot(*T(111, 47), w=3.6)

steps = [
    step('Start with an x', 'Draw a small letter x: two straight lines that cross in the middle. This x is hiding in the hummingbird.', [line(*xa), line(*xb)]),
    step('Body and head', 'From the top of one line, draw its round body and head over the top, down to the top of the other line.', [line(*BODY)]),
    step('Neck and eye', 'Draw a curved line across its neck, and an eye.', [line(*neck), eye]),
    step('The tail', 'Join the bottom of the x with a bumpy line for its tail, and draw three lines on it.', [line(*TAIL)] + [line(r) for r in rays]),
    step('The wings', 'Draw a big wing on each side, with bumpy feather edges and two lines on each.', [line(*wingL), line(*wingR)] + [line(f) for f in featL + featR]),
    step('The beak', 'Draw its long thin beak, from its head up to the right.', [line(*beak)]),
    step('The flower', 'Draw a trumpet flower at the end of its beak, with a little cap and a stem.', [line(*bell), line(lip1, lip2), line(*cap), line(*stem)]),
]

# ---- colours ----
head = fill(GRN, *(piece(BODY, N1, N2) + rev(neck)))
body = fill(ORA, *(piece(BODY, UL, N1) + neck + piece(BODY, N2, UR) + [xb[0], xa[0].rev()]))
tail = fill(RED, *([xa[1]] + TAIL + [xb[1].rev()]))
wings = [fill(BRN, *(wingL + piece(BODY, LW2, LW1))), fill(BRN, *(wingR + rev(piece(BODY, RW1, RW2))))]
flower = fill(PNK, *(bell + [lip1, lip2]))
capf = fill(GRN, *(cap + [bell[1].rev()]))
steps += [
    step('Colour green', 'Colour its head and the cap of the flower green.', [head, capf], use='green'),
    step('Colour orange', 'Colour its body orange.', [body], use='orange'),
    step('Colour brown', 'Colour its wings brown.', wings, use='brown'),
    step('Colour red', 'Colour its tail red.', [tail], use='red'),
    step('Colour pink', 'Colour the flower pink.', [flower], use='pink'),
]

D = drawing('dx_hummingbird_x', "x is for Xantus's hummingbird", 2, 14, 'animals', ['Letters', 'Animals'],
            "A Xantus's hummingbird hovering at a flower. The small x is hiding in it: the bottom of its body and its spread tail.",
            steps, ['green', 'orange', 'brown', 'red', 'pink'])
save('hummingbird', D, {'set': 'animals-az', 'slot': 'x', 'kind': 'fly', 'age_from': 4})
