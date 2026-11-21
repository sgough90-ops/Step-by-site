"""m is for monkey (dx_monkey_m), Animals a to z, slot m. From Claude's round 5 sketch 'Monkey (hanging from a branch)'
(21 Nov 2026), drawn with the idea of Art Expedition's video (a small m in a monkey's face), with the branch taken away as
he asked: both arms up in the air, legs dangling. The arms bend out a little so they clear its ears.

The small m is its face: the two humps are its brow, one over each eye; the outside lines are the sides of its face;
the middle line runs down between its eyes to its nose. Below the m its face goes out to its cheeks and chin.
Sketch coordinates (200 x 200) go onto the app's 100 x 100 paper by T().
"""
import os, json
from r5kit import *

pp = Paper(0.48, 1.0, 1.0)
T, S = pp.T, pp.s
BROWN, LB = FILL['brown'], FILL['lbrown']

def ring_mid_out(ch, c, r):
    """is the middle of a run of pieces outside the circle (c, r)?"""
    seg = ch[len(ch) // 2]; m = seg.at(.5)
    return math.dist(m, c) > r

def short_piece(ring, p, q):
    """pieces of a closed ring from p to q, the shorter way round (reversed if that is against the ring's direction)"""
    a = ring_piece(ring, p, q); b = ring_piece(ring, q, p)
    return a if chain_len(a) <= chain_len(b) else rev(b)

def cut_ring(ring, raw_pts, exact=None):
    """cut a ring at points; if exact points are given, the cut points are moved onto them exactly"""
    new, ex = cut_at_points(ring, raw_pts)
    if exact:
        exact = [e1 if e1 is not None else e0 for e0, e1 in zip(ex, exact)]
        fix = {}
        for e0, e1 in zip(ex, exact): fix[e0] = e1
        out = []
        for s in new:
            n = Seg.__new__(Seg); n.p = [fix.get(s.p[0], s.p[0])] + s.p[1:-1] + [fix.get(s.p[-1], s.p[-1])]; out.append(n)
        new, ex = out, list(exact)
    chain_ok(new)
    return new, ex

# ---------- the m: lines at x 75, 100, 125; humps spring at y 80 (14 high); bottoms at y 100 ----------
A0, A1, A2 = T(75, 100), T(75, 80), T(100, 80)
B1, B2, C1 = T(100, 100), T(125, 80), T(125, 100)
hump1 = arc(87.5 * S + 1, 80 * S + 1, 12.5 * S, 14 * S, 180, 360, start=A1, end=A2)
hump2 = arc(112.5 * S + 1, 80 * S + 1, 12.5 * S, 14 * S, 180, 360, start=A2, end=B2)
m_first = [Seg(A0, A1)] + hump1 + [Seg(A2, B1)]
m_second = hump2 + [Seg(B2, C1)]

# ---------- head, ears, body (rings), and where they meet ----------
HC, HR = T(100, 88), 42 * S
head = circle(HC[0], HC[1], HR)
ear_l = circle(*T(56, 88), 12 * S); ear_r = circle(*T(144, 88), 12 * S)
torso = circle(*T(100, 150), 25 * S, ry=27 * S)

cheek_l_raw = [Seg(A0, T(72, 104), T(67.5, 107.2), T(60.5, 108.7))]
cheek_r_raw = [Seg(C1, T(128, 104), T(132.5, 107.2), T(139.5, 108.7))]
cl, ql = trim_to(cheek_l_raw, head, 'start'); cr_, qr = trim_to(cheek_r_raw, head, 'start')
xe_l = [x[4] for x in crossings(ear_l, head)]; xe_r = [x[4] for x in crossings(ear_r, head)]
xt = [x[4] for x in crossings(torso, head)]
assert len(xe_l) == 2 and len(xe_r) == 2 and len(xt) == 2, (len(xe_l), len(xe_r), len(xt))
head, ex = cut_ring(head, [ql, qr] + xe_l + xe_r + xt)
QL, QR, EL1, EL2, ER1, ER2, TJ1, TJ2 = ex
cheek_l = snap(cl, end=QL); cheek_r = snap(cr_, end=QR)
ear_l, _ = cut_ring(ear_l, xe_l, [EL1, EL2]); ear_r, _ = cut_ring(ear_r, xe_r, [ER1, ER2])
ear_l_arc = ring_piece(ear_l, EL1, EL2)
if not ring_mid_out(ear_l_arc, HC, HR): ear_l_arc = ring_piece(ear_l, EL2, EL1)
ear_r_arc = ring_piece(ear_r, ER1, ER2)
if not ring_mid_out(ear_r_arc, HC, HR): ear_r_arc = ring_piece(ear_r, ER2, ER1)

# ---------- arms, hands, legs, feet, tail: edges trimmed where they come out of the body and where they reach a hand or foot ----------
hand_l = circle(*T(33, 45), 8.5 * S); hand_r = circle(*T(167, 45), 8.5 * S)
foot_l = circle(*T(80, 189.5), 10 * S, ry=5.5 * S); foot_r = circle(*T(120, 189.5), 10 * S, ry=5.5 * S)

def limb_edges(centre, w0, w1, end_ring):
    """the two edges of an arm or leg: from where they come out of the body to where they reach a hand or foot"""
    Lq, Rq, _ = band_edges(centre, w0, w1)
    out = []
    for q in (Lq, Rq):
        ch = pp.smooth(q)
        xs = crossings(ch, torso)
        assert len(xs) == 1, ('edge should come out of the body once', len(xs))
        ia, ta, _, _, p0 = xs[0]
        a, b = ch[ia].split(ta); ch = [b] + ch[ia + 1:]
        ch, p1 = trim_to(ch, end_ring, 'start')
        assert not crossings(ch, head), 'edge runs behind the head'
        out.append((ch, p0, p1))
    return out

ARM_L = [(90, 146), (76, 140), (47, 124), (30, 94), (33, 47)]
ARM_R = [(200 - x, y) for x, y in ARM_L]
LEG_L = [(90, 160), (88, 168), (84, 179), (82, 188)]
LEG_R = [(200 - x, y) for x, y in LEG_L]
arms = [limb_edges(ARM_L, 13, 11, hand_l), limb_edges(ARM_R, 13, 11, hand_r)]
legs = [limb_edges(LEG_L, 13, 11, foot_l), limb_edges(LEG_R, 13, 11, foot_r)]

# tail: one line out of the body, round its curly tip and back into the body
TAIL = [(112, 156), (124, 160), (146, 176), (166, 168), (172, 150), (162, 140), (152, 146), (156, 156)]
Lq, Rq, c = band_edges(TAIL, 8, 6)
tip = c[-1]; wt = 3.0
a0 = math.degrees(math.atan2(Lq[-1][1] - tip[1], Lq[-1][0] - tip[0]))
cap = [(tip[0] + wt * math.cos(math.radians(a0 + 180 * k / 6)), tip[1] + wt * math.sin(math.radians(a0 + 180 * k / 6))) for k in range(1, 6)]
tail_ch = pp.smooth(Lq + cap + Rq[::-1])
xs = sorted(crossings(tail_ch, torso), key=lambda r: (r[0], r[1]))
assert len(xs) == 2, len(xs)
(i1, t1, _, _, tq1), (i2, t2, _, _, tq2) = xs
a, b = tail_ch[i2].split(t2); tail_ch = tail_ch[:i2] + [a]
a, b = tail_ch[i1].split(t1); tail_ch = [b] + tail_ch[i1 + 1:]

# cut the body ring where the arms, legs and tail come out, and where it meets the head
body_raw = [TJ1, TJ2] + [e[1] for arm in arms for e in arm] + [e[1] for leg in legs for e in leg] + [tq1, tq2]
torso, bx = cut_ring(torso, body_raw, [TJ1, TJ2] + [None] * (len(body_raw) - 2))
TB = bx[2:]
arm_e = []; k = 0
for arm in arms:
    arm_e.append([snap(ch, start=TB[k + j]) for j, (ch, _, _) in enumerate(arm)]); k += 2
leg_e = []
for leg in legs:
    leg_e.append([snap(ch, start=TB[k + j]) for j, (ch, _, _) in enumerate(leg)]); k += 2
tail_line = snap(tail_ch, start=TB[k], end=TB[k + 1])
TA1, TA2 = TB[k], TB[k + 1]

def ends_on(ring, edges):
    ring, ex = cut_ring(ring, [e[-1].b for e in edges])
    return ring, [snap(e, end=x) for e, x in zip(edges, ex)], ex

hand_l, arm_e[0], HL = ends_on(hand_l, arm_e[0]); hand_r, arm_e[1], HRr = ends_on(hand_r, arm_e[1])
foot_l, leg_e[0], FL = ends_on(foot_l, leg_e[0]); foot_r, leg_e[1], FR = ends_on(foot_r, leg_e[1])

body_vis = ring_piece(torso, TJ1, TJ2)
if not ring_mid_out(body_vis, HC, HR): body_vis = ring_piece(torso, TJ2, TJ1)

# ---------- face ----------
EYE_L, EYE_R = T(87.5, 84), T(112.5, 84)
NRX, NRY = 6.4 * S, 3.6 * S
nose = circle(B1[0], B1[1] + NRY, NRX, start_deg=-90, ry=NRY)
nose = snap(nose, start=B1); nose[-1] = snap([nose[-1]], end=B1)[0]
smile = [q2c(T(87, 113), T(100, 124), T(113, 113))]
tummy = circle(*T(100, 156), 15 * S, ry=16 * S)

steps = [
    step('Start with an m', 'Draw a small letter m: a short straight line, then two humps side by side, each coming straight down.',
         [line(*m_first), line(*m_second)]),
    step('The head', 'Draw a big circle all the way round the m.', [ring(*head)]),
    step('The face', 'From the bottom of each outside line, draw a short line out to the circle.', [line(*cheek_l), line(*cheek_r)]),
    step('Eyes, nose and smile', 'Draw an eye dot under each hump, a nose at the bottom of the middle line, and a big smile.',
         [dot(*EYE_L, w=4.0), dot(*EYE_R, w=4.0), ring(*nose), line(*smile)]),
    step('The ears', 'Draw a round ear on each side of the head.', [line(*ear_l_arc), line(*ear_r_arc)]),
    step('The body', 'Draw its round body under the head.', [line(*body_vis)]),
    step('The tummy', 'Draw a circle for its tummy.', [ring(*tummy)]),
    step('Arms up', 'Draw two round hands up high, then two long arms from the body up to them.',
         [ring(*hand_l), ring(*hand_r)] + [line(*e) for arm in arm_e for e in arm]),
    step('Legs and feet', 'Draw two feet at the bottom, then two short legs from the body down to them.',
         [ring(*foot_l), ring(*foot_r)] + [line(*e) for leg in leg_e for e in leg]),
    step('The tail', 'Draw a long curly tail coming out of its side.', [line(*tail_line)]),
]

# ---------- colours ----------
hole = lambda segs: d_fill(*segs)
top = ring_piece(head, QL, QR)                                   # over the top of the head, from cheek to cheek
assert top[len(top) // 2].at(.5)[1] < HC[1]
low = ring_piece(head, QR, QL)                                   # under the face
brown_head = fill(BROWN, *(top + rev(cheek_r) + [Seg(C1, B2)] + rev(hump2) + rev(hump1) + [Seg(A1, A0)] + cheek_l))
face = fill(LB, *([Seg(A0, A1)] + hump1 + hump2 + [Seg(B2, C1)] + cheek_r + low + rev(cheek_l)), cut=[hole(nose)])
def ear_fill(arc_, a, b):
    inside = short_piece(head, arc_[-1].b, arc_[0].a)
    return fill(LB, *(arc_ + inside))
under_head = short_piece(head, body_vis[-1].b, body_vis[0].a)
body_fill = fill(BROWN, *(body_vis + under_head), cut=[hole(tummy)])
def limb_fill(edges, ring_):
    e1, e2 = edges
    end_piece = short_piece(ring_, e1[-1].b, e2[-1].b)
    base = short_piece(torso, e2[0].a, e1[0].a)
    return fill(BROWN, *(e1 + end_piece + rev(e2) + base))
tail_fill = fill(BROWN, *(tail_line + short_piece(torso, TA2, TA1)))
browns = [brown_head, fill(BROWN, *nose), body_fill, limb_fill(arm_e[0], hand_l), limb_fill(arm_e[1], hand_r),
          fill(BROWN, *hand_l), fill(BROWN, *hand_r), limb_fill(leg_e[0], foot_l), limb_fill(leg_e[1], foot_r), tail_fill]
lights = [face, ear_fill(ear_l_arc, EL1, EL2), ear_fill(ear_r_arc, ER1, ER2), fill(LB, *tummy), fill(LB, *foot_l), fill(LB, *foot_r)]
steps += [step('Colour brown', 'Colour the monkey brown, but leave its face, ears, tummy and feet.', browns, use='brown'),
          step('Colour light brown', 'Colour its face, ears, tummy and feet light brown.', lights, use='lbrown')]

Pd = drawing('dx_monkey_m', 'm is for monkey', 2, 12, 'animals', ['Letters', 'Animals'],
             'A happy monkey with its arms up. The small m is its face: its brow over each eye, the sides of its face and a line down to its nose.',
             steps, ['brown', 'lbrown'])
save('monkey', Pd, {'set': 'animals-az', 'slot': 'm', 'kind': 'hop', 'age_from': 4})
