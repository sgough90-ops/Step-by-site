"""Z is for Zeppelin (dx_zeppelin_z), Vehicles A to Z, slot Z. Rebuilt from his ChatGPT sheet (15 Nov 2026).
The Z is the tail: its top line is the top of the upper fin, its slanted line is the back of the balloon, its bottom line is the bottom of the lower fin."""
from kit15 import *

GREY, RED, YELLOW, LBLUE = FILL['grey'], FILL['red'], FILL['yellow'], FILL['lblue']

# ---- the Z ----
A, B, C, D = P(66, 26), P(90, 26), P(64, 58), P(88, 58)
M = P((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
sF = 0.6
F = P(M[0] + (C[0] - M[0]) * sF, M[1] + (C[1] - M[1]) * sF)
G = P(A[0] + (M[0] - A[0]) * 0.3, A[1] + (M[1] - A[1]) * 0.3)
diag = [Seg(B, M), Seg(M, F), Seg(F, C)]
top, botbar = Seg(A, B), Seg(C, D)

# ---- the fins: join the free ends of the Z's lines to the middle of the slanted line ----
finA = [Seg(A, G), Seg(G, M)]
finD = Seg(D, M)
mid = Seg(M, (93, 42))

# ---- the balloon ----
etop = Seg(G, (57, 22.2), (24.5, 21.6), (12.5, 32.6))
enose = Seg((12.5, 32.6), (8.6, 36.4), (8.6, 47.6), (12.5, 51.4))
ebot = Seg((12.5, 51.4), (24.5, 62.2), (57, 61.6), F)
env = [etop, enose, ebot]

# seams
S1 = P(A[0] + (M[0] - A[0]) * 0.62, A[1] + (M[1] - A[1]) * 0.62)
S2 = P(M[0] + (C[0] - M[0]) * 0.35, M[1] + (C[1] - M[1]) * 0.35)
n1, n2 = enose.split(0.27)
n2, n3 = n2.split(0.62)
N1, N2 = n1.b, n2.b
seam1 = Seg(N1, (30, 32.6), (55, 32.2), S1)
seam2 = Seg(N2, (30, 51.8), (55, 52.4), S2)
# the seam ends must sit on the fin line / slanted line: split those lines there
finA = [Seg(A, G), Seg(G, S1), Seg(S1, M)]
diag = [Seg(B, M), Seg(M, S2), Seg(S2, F), Seg(F, C)]

# ---- the cabin under the balloon ----
b1, rest = cut_chain_x([ebot], 30)
b2, b3 = cut_chain_x(rest, 50)
PL, PR = b1[-1].b, b2[-1].b
cab = [Seg(PL, (30, 68.4)), *arc(32.6, 68.4, 2.6, 2.6, 180, 90, start=P(30, 68.4), end=P(32.6, 71)), Seg((32.6, 71), (47.4, 71)),
       *arc(47.4, 68.4, 2.6, 2.6, 90, 0, start=P(47.4, 71), end=P(50, 68.4)), Seg((50, 68.4), PR)]
wins = [rrect(x, 63.2, x + 4.2, 67.2, 1.1) for x in (32.1, 37.9, 43.7)]

# ---- two clouds ----
cl1 = cloud(10, 33, 89, 10)
cl2 = cloud(61, 86, 84, 10)

steps = [
    step('Start with a Z', 'Draw a big capital Z on the right of your paper.', [line(top), line(*diag), line(botbar)]),
    step('The tail fins', 'Join the left end of the top line to the middle of the slanted line. Join the right end of the bottom line to the middle too.',
         [line(*finA), line(finD)]),
    step('The middle fin', 'From the middle of the slanted line, draw a short line straight out to the right.', [line(mid)]),
    step('The balloon', 'Start on the line you just drew at the top. Draw a long round balloon to the left and back to the slanted line.',
         [line(*env)]),
    step('The seams', 'Draw two long curved lines along the balloon, one near the top and one near the bottom.', [line(seam1), line(seam2)]),
    step('The cabin', 'Draw a box with round corners hanging under the balloon.', [line(*cab)]),
    step('The windows', 'Draw three little windows in the cabin.', [ring(w) for w in wins]),
    step('A cloud', 'Draw a fluffy cloud under the balloon, on the left.', [ring(cl1)]),
    step('Another cloud', 'Draw another cloud on the right, under the tail.', [ring(cl2)]),
]
# colour outlines
e_fill = fill(GREY, etop, enose, b1, b2, b3, rev(diag[1:3]), rev(finA[1:]))
# the cabin is under the balloon: balloon fill stops at the balloon's bottom line, cabin fill uses the same piece
cab_fill = fill(YELLOW, *cab, rev(b2), cut=[d_fill(*w) for w in wins])
fin_up = fill(RED, top, diag[0], rev(finA))
fin_lo = fill(RED, *diag[1:], botbar, finD)
steps += [
    step('Colour grey', 'Colour the balloon grey.', [e_fill], use='grey'),
    step('Colour red', 'Colour the two tail fins red.', [fin_up, fin_lo], use='red'),
    step('Colour yellow', 'Colour the cabin yellow, round the windows.', [cab_fill], use='yellow'),
    step('Colour light blue', 'Colour the windows light blue.', [fill(LBLUE, *w) for w in wins], use='lblue'),
]
P_ = drawing('dx_zeppelin_z', 'Z is for Zeppelin', 3, 15, 'vehicles', ['Letters', 'Vehicles'],
             'A zeppelin, a long round airship, floating past two clouds. The capital Z is hiding in its tail: '
             'the top and bottom lines are the edges of the red fins and the slanted line is the back of the balloon.',
             steps, ['grey', 'red', 'yellow', 'lblue'])
save('zeppelin', P_, {'set': 'vehicles-AZ', 'slot': 'Z', 'kind': 'fly', 'age_from': 5})
