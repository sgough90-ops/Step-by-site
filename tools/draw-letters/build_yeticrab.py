"""y is for yeti crab (dx_yeticrab_y), Animals a to z, slot y (21 Nov 2026).
From Claude's sketch 'yeti crab (claws up)' (round 2 design 1, like the Art Expedition video he sent): a yeti crab seen
from above with its claws up and a curly small y drawn on its shell, as the lines between the shell's plates. The y's
cup is on the left; its stem comes down from the point of the head notch and curls round to the edge of the shell.
Shell, arms and palms light brown; claws pink. Sketch coordinates (200 x 200) go onto the paper by T().
"""
import math, re
from r5kit import *

PA = Paper(0.6, -10, -4.8)
T = PA.T
LB, PNK = FILL['lbrown'], FILL['pink']
CX, CY, RX, RY = 100, 118, 46, 50


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


def edge_x(x, top=True):
    return (x, CY - (1 if top else -1) * RY * math.sqrt(max(0, 1 - ((x - CX) / RX) ** 2)))


def edge_y(y, left=True):
    return (CX - (1 if left else -1) * RX * math.sqrt(max(0, 1 - ((y - CY) / RY) ** 2)), y)


def arc_between(ring_, p, q):
    """the shorter way round a closed ring from p to q"""
    a = ring_piece(ring_, p, q); b = rev(ring_piece(ring_, q, p))
    la = sum(math.dist(s.a, s.b) for s in a); lb = sum(math.dist(s.a, s.b) for s in b)
    return a if la <= lb else b


# ---- 1: the curly y ----
CUP = chain('M76,95 C75,108 86,115 101,114')
FORK = CUP[-1].b
STEM = chain('M102,91 L101,114 L100,124 C98,136 80,143 59.6,142')
assert STEM[0].b == FORK
TOPS = STEM[0].a                                            # the top of the stem: the point of the head notch
C1 = P(*STEM[2].at(0.1))                                    # a shell line leaves the curl here
STEM, ex = cut_at_points(STEM, [C1]); C1 = ex[0]
CURL_END = STEM[-1].b

# ---- the shell: an oval, cut wherever something meets it ----
RING = circle(*T(CX, CY), RX * PA.s, start_deg=-90, ry=RY * PA.s)
pts = {
    'eyeR': edge_x(105), 'antR': edge_x(112), 'notchR': edge_x(122), 'armRi': edge_x(129), 'armRo': edge_x(139),
    'legR1': edge_y(104, False), 'fork': edge_y(114, False), 'legR2': edge_y(126, False), 'legR3': edge_y(146, False),
    'plate': edge_x(132, False), 'legL3': edge_y(152), 'curl': None, 'legL2': edge_y(126), 'legL1': edge_y(104),
    'armLo': edge_x(61), 'armLi': edge_x(71), 'notchL': edge_x(78), 'antL': edge_x(88), 'eyeL': edge_x(95)}
names = [k for k in pts if k != 'curl']
RING, ex = cut_at_points(RING, [T(*pts[k]) for k in names] + [CURL_END])
E = dict(zip(names, ex[:-1]))
assert math.dist(ex[-1], CURL_END) < 0.05, (ex[-1], CURL_END)
# make the y's curl end exactly on the shell
STEM[-1] = Seg(STEM[-1].p[0], STEM[-1].p[1], STEM[-1].p[2], ex[-1]); CURL_END = ex[-1]

# ---- shell lines: the head notch, the line from the fork, the line from the curl ----
notch = [Seg(E['notchL'], TOPS), Seg(TOPS, E['notchR'])]
fork_line = snap(chain('M101,114 C116,112 132,112 145.85,114'), FORK, E['fork'])
plate_line = snap(chain('M98.9,127.4 C110,138 122,150 132,153.9'), C1, E['plate'])

# ---- the arms: a tube in two parts, a round palm and a two-part claw ----
def arm(Ao, Ai, ux, uy, nx, ny):
    """Ao/Ai: outer and inner feet on the shell (paper); u: up the arm; n: towards the outer side (sketch units)"""
    so = ((Ao[0] - PA.ox) / PA.s, (Ao[1] - PA.oy) / PA.s); si = ((Ai[0] - PA.ox) / PA.s, (Ai[1] - PA.oy) / PA.s)
    M0 = ((so[0] + si[0]) / 2, (so[1] + si[1]) / 2)
    at = lambda k, m: (M0[0] + ux * k + nx * m, M0[1] + uy * k + ny * m)
    Jo, Ji = T(*at(16, 7)), T(*at(16, -7))
    pc = at(38, 0)
    Ko, Ki = T(*at(38 - 6.71, 6)), T(*at(38 - 6.71, -6))
    def rot(deg):
        a = math.radians(deg); return (ux * math.cos(a) + nx * math.sin(a), uy * math.cos(a) + ny * math.sin(a))
    def on_palm(deg, r=9):
        d = rot(deg); return T(pc[0] + d[0] * r, pc[1] + d[1] * r)
    Bo, Bm, Bi = on_palm(40), on_palm(0), on_palm(-40)
    to, ti = on_palm(14, 24), on_palm(-14, 24)
    palm = circle(*T(*pc), 9 * PA.s)
    palm, exx = cut_at_points(palm, [Ko, Ki, Bo, Bm, Bi]); Ko, Ki, Bo, Bm, Bi = exx
    outer = [Seg(Ao, Jo), Seg(Jo, Ko)]
    inner = [Seg(Ai, Ji), Seg(Ji, Ki)]
    joint = Seg(Jo, Ji)
    def finger(a, tip, b, bulge_a, bulge_b):
        m1 = ((a[0] + tip[0]) / 2 + nx * PA.s * bulge_a, (a[1] + tip[1]) / 2 + ny * PA.s * bulge_a)
        m2 = ((tip[0] + b[0]) / 2 + nx * PA.s * bulge_b, (tip[1] + b[1]) / 2 + ny * PA.s * bulge_b)
        return [q2c(a, P(*m1), tip), q2c(tip, P(*m2), b)]
    f_out = finger(Bo, to, Bm, 3, -1)
    f_in = finger(Bm, ti, Bi, 1, -3)
    fills = [fill(LB, *([Seg(Ao, Jo), joint, Seg(Ji, Ai)] + arc_between(RING, Ai, Ao))),
             fill(LB, *([Seg(Jo, Ko)] + arc_between(palm, Ko, Ki) + [Seg(Ki, Ji), joint.rev()])),
             fill(LB, *palm)]
    claws = [fill(PNK, *(f_out + arc_between(palm, Bm, Bo))), fill(PNK, *(f_in + arc_between(palm, Bi, Bm)))]
    return dict(lines=[line(*outer), line(*inner), line(joint)], claw_lines=[ring(*palm), line(*f_out), line(*f_in)], fills=fills, claws=claws)
# left arm goes up and a little left, right arm up and a little right
armL = arm(E['armLo'], E['armLi'], -0.174, -0.985, -0.985, 0.174)
armR = arm(E['armRo'], E['armRi'], 0.174, -0.985, 0.985, 0.174)

# ---- legs, with two little hairs each ----
def leg(base, a1, a2, L=16):
    b = ((base[0] - PA.ox) / PA.s, (base[1] - PA.oy) / PA.s)
    p1 = (b[0] + math.cos(math.radians(a1)) * L, b[1] + math.sin(math.radians(a1)) * L)
    p2 = (p1[0] + math.cos(math.radians(a2)) * L, p1[1] + math.sin(math.radians(a2)) * L)
    segs = [Seg(base, T(*p1)), Seg(T(*p1), T(*p2))]
    hairs = []
    for (ax, ay), (bx, by) in [(b, p1), (p1, p2)]:
        dx, dy = bx - ax, by - ay; ln = math.hypot(dx, dy); nx_, ny_ = -dy / ln, dx / ln
        if ny_ > 0: nx_, ny_ = -nx_, -ny_                     # hairs on the upper side
        mx, my = ax + dx * 0.5, ay + dy * 0.5
        s0 = (mx + nx_ * 2.5, my + ny_ * 2.5); s1 = (s0[0] + nx_ * 4 + dx / ln * 2, s0[1] + ny_ * 4 + dy / ln * 2)
        hairs.append(Seg(T(*s0), T(*s1)))
    return segs, hairs
legs = [leg(E['legL1'], 200, 235), leg(E['legL2'], 180, 215), leg(E['legL3'], 160, 195),
        leg(E['legR1'], -20, -55), leg(E['legR2'], 0, -35), leg(E['legR3'], 20, -15)]

# ---- eyes on stalks, and two long feelers ----
stalks = [Seg(E['eyeL'], T(93, 58.5)), Seg(E['eyeR'], T(107, 58.5))]
eyes = [dot(*T(92.7, 56.6), w=3.8), dot(*T(107.3, 56.6), w=3.8)]
feelers = [[q2c(E['antL'], T(86, 46), T(80, 22))], [q2c(E['antR'], T(114, 46), T(120, 20))]]

steps = [
    step('Start with a y', 'Draw a curly small letter y: a curved cup on the left, and a long line that comes down and curls round at the bottom. This y is hiding in the crab.',
         [line(*CUP), line(*STEM)]),
    step('The shell', 'Draw a big oval shell round the y. The curl at the bottom of the y just touches it.', [ring(*RING)]),
    step('Shell lines', 'Draw a pointed notch from the top of the y up to the shell, a line from the middle of the y across, and a curve from the curl down.',
         [line(*notch), line(*fork_line), line(*plate_line)]),
    step('The arms', 'Draw two long arms going up from the top of the shell, each with a line across the middle.', armL['lines'] + armR['lines']),
    step('Claws', 'Draw a round palm at the top of each arm, with a two-part claw on top.', armL['claw_lines'] + armR['claw_lines']),
    step('Legs', 'Draw three bent legs on each side of the shell.', [line(*lg[0]) for lg in legs]),
    step('Hairy legs', 'Give each leg two little hairs. Yeti crabs are hairy!', [line(h) for lg in legs for h in lg[1]]),
    step('Eyes and feelers', 'Draw two eyes on little stalks and two long feelers at the top of the shell.', [line(s) for s in stalks] + eyes + [line(*f) for f in feelers]),
]

# ---- colours ----
stem_down = STEM                                             # top of stem -> fork -> ... -> curl end
i_fork = next(k for k, s in enumerate(STEM) if s.b == FORK)
i_c1 = next(k for k, s in enumerate(STEM) if s.b == C1)
stem_top = STEM[:i_fork + 1]                                 # top -> fork
stem_mid = STEM[i_fork + 1:i_c1 + 1]                         # fork -> C1
stem_curl = STEM[i_c1 + 1:]                                  # C1 -> curl end
R_head = fill(LB, *(ring_piece(RING, E['notchL'], E['notchR']) + rev(notch)))
R_rt = fill(LB, *(ring_piece(RING, E['notchR'], E['fork']) + rev(fork_line) + rev(stem_top) + [notch[1]]))
R_rm = fill(LB, *(ring_piece(RING, E['fork'], E['plate']) + rev(plate_line) + rev(stem_mid) + fork_line))
R_bot = fill(LB, *(ring_piece(RING, E['plate'], CURL_END) + rev(stem_curl) + plate_line))
R_left = fill(LB, *(ring_piece(RING, CURL_END, E['notchL']) + [notch[0]] + STEM))
steps += [
    step('Colour light brown', 'Colour the shell, the arms and the palms light brown.', [R_head, R_rt, R_rm, R_bot, R_left] + armL['fills'] + armR['fills'], use='lbrown'),
    step('Colour pink', 'Colour the claws pink.', armL['claws'] + armR['claws'], use='pink'),
]

D = drawing('dx_yeticrab_y', 'y is for yeti crab', 2, 14, 'animals', ['Letters', 'Animals'],
            'A hairy yeti crab with its claws up. The small y is hiding on its shell: the curly lines between the plates.',
            steps, ['lbrown', 'pink'])
save('yeticrab', D, {'set': 'animals-az', 'slot': 'y', 'kind': 'crawl', 'age_from': 4})
