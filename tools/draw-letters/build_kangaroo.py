"""K is for kangaroo (dx_kangaroo_k), Animals A to Z, slot K, in place of K is for Koala (21 Nov 2026).
From Claude's round-3 sketch 'Kangaroo (with a baby in its pouch)' (claude/step-by-draw-kangaroo-k-sketches.py), which
follows the shape of his kangaroo picture (a capital K hidden in its back legs), drawn with our own lines.

The K: the line down is the front of its near back leg; the top slanting line is the edge of its far thigh, under its
tummy; the bottom slanting line is the top of its far leg, which kicks down to its foot. The far leg is coloured brown,
the rest light brown, inside the ears pink. The eye stays white (out/kangaroo.white.json). The baby in the pouch is
drawn in lines on mum's tummy and coloured with her.
Sketch coordinates (200 x 200) are put on the app's paper by T() (0.48 scale), so the long tail fits inside.
"""
import json, os, re
from r5kit import *

PA = Paper(0.48, 2.6, 2.5)
T = PA.T


def chain(d):
    """pieces on the paper from a sketch path made of M, C and L (absolute)"""
    toks = re.findall(r'[MCL]|-?\d+\.?\d*', d)
    out = []; cur = None; i = 0; cmd = None
    while i < len(toks):
        t = toks[i]
        if t in 'MCL':
            cmd = t; i += 1; continue
        if cmd == 'M':
            cur = T(float(toks[i]), float(toks[i + 1])); i += 2
        elif cmd == 'C':
            c1 = T(float(toks[i]), float(toks[i + 1])); c2 = T(float(toks[i + 2]), float(toks[i + 3])); p = T(float(toks[i + 4]), float(toks[i + 5]))
            out.append(Seg(cur, c1, c2, p)); cur = p; i += 6
        elif cmd == 'L':
            p = T(float(toks[i]), float(toks[i + 1])); out.append(Seg(cur, p)); cur = p; i += 2
    return out


LB, BRN, PNK = FILL['lbrown'], FILL['brown'], FILL['pink']

# ---- 1: the K (line down 60 tall on the sketch, arms meeting half-way, 31 wide) ----
ST, UA, J, SB, LA, FS = T(107, 106), T(137, 107), T(107, 136), T(107, 166), T(138, 166), T(107, 154)
k_stem = Seg(ST, SB)
k_arms = [Seg(UA, J), Seg(J, LA)]

# ---- the outline, in the order it is drawn ----
feet_near = chain('M107,166 C113,174 120,182 125,189 C128,194 123,197 119,194 C112,188 103,178 96,170')
feet_far = chain('M138,166 C141,170 143,174 144,178 C145,182 141,184 139,181 C129,172 117,163 107,154')
toe = chain('M113,185 C115.5,186.5 117.5,189 118.5,192')
belly = chain('M107,106 C116,108 128,108.5 137,107 C140,106.5 143,104 145,100 C145,95 147,90 150,86')
neck_face = chain('M150,86 C158,79 170,72 177.5,67 C179.5,64 182,62 186.5,62 C192.5,62 197.5,59 197.5,53.5 '
                  'C197.5,48 193.5,45 192.5,41 C191,33 189,26 185,22')
ears_head = chain('M185,22 C187.5,16 188,10.5 186.5,5 C182.5,8.5 180,14 178.5,21 C177.5,21 176.5,21 175.5,21 '
                  'C176.5,15 175.5,9 173,4.5 C169.5,8 167.5,14 167,21.5 C163,22 160,25 159,30')
back_tail = chain('M159,30 C157,38 154,46 148,50 C130,53 100,51 86,51 C78,52 72,55 68,60 '
                  'C50,65 28,66 12,62 C6,60.5 3.5,64 6.5,66.5 C20,72 44,77 70,76')
rear = chain('M70,76 C66,84 66,98 70,108 C75,122 84,140 90,158 C91,163 93,166 96,170')
assert feet_near[0].a == SB and feet_far[0].a == LA and feet_far[-1].b == FS
assert belly[0].a == ST and belly[0].b == UA
assert neck_face[0].a == belly[-1].b and ears_head[0].a == neck_face[-1].b and back_tail[0].a == ears_head[-1].b
assert rear[0].a == back_tail[-1].b and rear[-1].b == feet_near[-1].b

# ---- where the arms and the pouch meet the outline (cut there so colour edges match exactly) ----
neck_face, (NF, FR1, FR2) = cut_at_points(neck_face, [T(151.5, 85.2), T(159, 79.4), T(164.4, 76.4)])
belly, (PE, NB) = cut_at_points(belly, [T(145.3, 97), T(146.3, 93)])

# ---- the arms: thin, hanging down in front, three little claws on each paw ----
far_arm = snap(chain('M159,79.4 C162,90 165,103 166,116 C166,121 172.4,121 172.4,116 C171.4,102 168.4,89 164.4,76.4'), FR1, FR2)
near_arm = snap(chain('M146.4,93 C148,104 150,115 151,124 C151.5,129 157.8,129 157.8,124 C157,112 155,99 151.2,86'), NB, NF)

def claws(paw):
    out = []
    for t, dx in ((.25, -.35), (.5, 0), (.75, .35)):
        p = P(*paw.at(t))
        out.append(line(Seg(p, P(p[0] + dx, p[1] + 1.75)), w=1.3))
    return out

# ---- the face ----
EYE_C, EYE_R = T(176, 36), 4.6 * 0.48
eye = circle(*EYE_C, EYE_R)
pupil = dot(*T(177.2, 36.6), w=1.9)
brow = chain('M172,29.4 C174.4,27.9 177.9,27.9 180.4,29.2')
nose = dot(*T(193.8, 50.2), w=2.6)
smile = chain('M180,52.5 C182,57 187,59.6 192,58')
ear_in = [chain('M169.5,19 C170,13.5 171.2,9.6 173,7.4 C174.4,10.6 174.6,15 174,19 L169.5,19'),
          chain('M180.3,19.5 C181.4,14.4 183.2,10.4 185.6,8 C186,12 185.4,16 183.8,19.5 L180.3,19.5')]

# ---- the pouch and the baby ----
pouch = [Seg(T(120, 97), T(128, 102.4), T(139, 102.4), PE)]
pouch, (JD1, JD2) = cut_at_points(pouch, [T(125, 100.2), T(140.5, 100.2)])
dome = [Seg(JD1, T(123.6, 91.4), T(127.2, 86), T(132.8, 86)), Seg(T(132.8, 86), T(138.4, 86), T(142, 91.4), JD2)]
dome, (E1a, E1b, E2a, E2b) = cut_at_points(dome, [T(127, 87.6), T(130.6, 86.4), T(135.6, 86.4), T(139.6, 87.8)])
joey_ear1 = [Seg(E1a, T(125, 80.6), T(125, 75.6), T(127.4, 72.4)), Seg(T(127.4, 72.4), T(130.4, 75.4), T(131.2, 79.8), E1b)]
joey_ear2 = [Seg(E2a, T(136.6, 79.4), T(138.8, 75.2), T(142, 73.4)), Seg(T(142, 73.4), T(142.8, 77.4), T(142, 81.6), E2b)]
joey_dots = [dot(*T(130, 92.6), w=1.6), dot(*T(136, 92.6), w=1.6), dot(*T(133, 96), w=1.7)]

# ---- the colours ----
body_edge = [k_stem] + feet_near + rev(rear) + rev(back_tail) + rev(ears_head) + rev(neck_face) + rev(belly)
eye_hole = d_fill(*eye)
ear_holes = [d_fill(*e) for e in ear_in]
body = fill(LB, *body_edge, cut=[eye_hole] + ear_holes)
far_arm_fill = fill(LB, *(far_arm + rev(piece(neck_face, FR1, FR2))))
near_arm_fill = fill(LB, *(near_arm + rev(piece(belly, NB, belly[-1].b) + piece(neck_face, neck_face[0].a, NF))))
far_thigh = fill(BRN, belly[0], Seg(UA, J), Seg(J, ST))
far_foot = fill(BRN, *([Seg(J, LA)] + feet_far + [Seg(FS, J)]))
ear_fills = [fill(PNK, *e) for e in ear_in]

steps = [
    step('Start with a K', 'Draw a capital K: a straight line down, then two slanting lines from its middle, one up and one down. This K is hiding in the kangaroo.',
         [line(k_stem), line(*k_arms)]),
    step('The feet', 'From the bottom of the line down, draw a long foot with a round toe. From the end of the bottom slanting line, draw a small foot back to the line down.',
         [line(*feet_near), line(*feet_far), line(*toe)]),
    step('The tummy', 'From the top of the line down, draw under its tummy, past the end of the top slanting line, and up to its chest.',
         [line(*belly)]),
    step('Neck and face', 'Carry on up the front of its neck, round its chin and its nose, and up the front of its face.',
         [line(*neck_face)]),
    step('The ears', 'Draw two tall pointy ears on top of its head, then come down the back of its head.',
         [line(*ears_head)]),
    step('Back and tail', 'Draw down its neck and along its back, then a long thin tail. Go round the end of the tail and back underneath.',
         [line(*back_tail)]),
    step('The back leg', 'From under the tail, draw the back of its long leg, all the way down to its heel.',
         [line(*rear)]),
    step('The arms', 'Draw two thin arms hanging down from its chest, with three little claws on each paw.',
         [line(*far_arm), line(*near_arm)] + claws(far_arm[1]) + claws(near_arm[1])),
    step('The face', 'Draw an eye with a dot in it, an eyebrow, a nose at the end of its face and a big grin.',
         [ring(*eye), pupil, line(*brow), nose, line(*smile)]),
    step('Inside the ears', 'Draw a thin shape inside each ear.',
         [ring(*e) for e in ear_in]),
    step('The baby', 'Draw a curved line on its tummy for the pouch, and a baby peeping out: a round head, two ears, two eyes and a nose.',
         [line(*pouch), line(*dome), line(*joey_ear1), line(*joey_ear2)] + joey_dots),
    step('Colour light brown', 'Colour the kangaroo light brown, and the baby too. Leave its eye white and the far leg for later.',
         [body, far_arm_fill, near_arm_fill], use='lbrown'),
    step('Colour brown', 'Colour the far leg brown: the little triangle under its tummy and the small foot.',
         [far_thigh, far_foot], use='brown'),
    step('Colour pink', 'Colour inside its ears pink.', ear_fills, use='pink'),
]

D = drawing('dx_kangaroo_k', 'K is for kangaroo', 3, 15, 'animals', ['Letters', 'Animals'],
            'A kangaroo hopping along with a baby in its pouch. The capital K is hiding in its back legs.',
            steps, ['lbrown', 'brown', 'pink'])
save('kangaroo', D, {'set': 'animals-AZ', 'slot': 'K', 'kind': 'hop', 'age_from': 5})
json.dump([eye_hole], open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'kangaroo.white.json'), 'w'))
