"""o is for octopus (Animals a to z, slot o).
The o: the octopus's whole round head, drawn first and complete. Each of the eight arms starts on the o and comes back
to it, so the arms only touch the letter: nothing covers it or crosses it.  (--gaps prints how close the arms come.)"""
import json, math, os, sys
from kit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

C = (50.0, 31.0); R = 18.0
A_TOP = 170.0
STEP = (A_TOP - 90.0) / 4

O_ = circle(C[0], C[1], R)

def on_o(a):
    return P(C[0] + R * math.cos(math.radians(a)), C[1] + R * math.sin(math.radians(a)))


def arm(k, M, head, l0, l1, turn, r0, r1, w_end=1.6, power=1.1, n_main=4, n_curl=8, skip=2.0, smooth=2.2):
    a_hi = A_TOP - STEP * k; a_lo = a_hi - STEP; a_mid = (a_hi + a_lo) / 2
    Qhi, Qlo = on_o(a_hi), on_o(a_lo)
    od = (math.cos(math.radians(a_mid)), math.sin(math.radians(a_mid)))
    B = (C[0] + R * od[0], C[1] + R * od[1])
    hd = (math.cos(math.radians(head)), math.sin(math.radians(head)))
    main = Seg.__new__(Seg); main.p = [B, (B[0] + od[0] * l0, B[1] + od[1] * l0), (M[0] - hd[0] * l1, M[1] - hd[1] * l1), M]
    samp = [main.at(i / 80) for i in range(81)]
    n_main_s = len(samp)
    N = 90; x, y = M
    for i in range(N):
        f = (i + 0.5) / N; psi = math.radians(head + turn * f); r = r0 * (r1 / r0) ** f
        ds = r * math.radians(turn) / N
        x += ds * math.cos(psi); y += ds * math.sin(psi); samp.append((x, y))
    cum = [0.0]
    for i in range(1, len(samp)): cum.append(cum[-1] + math.dist(samp[i], samp[i - 1]))
    L = cum[-1]; Lm0 = cum[n_main_s - 1]; ds = 0.2; n = int(L / ds)
    def at_len(s):
        j = max(1, min(len(cum) - 1, next((q for q in range(1, len(cum)) if cum[q] >= s), len(cum) - 1)))
        f = (s - cum[j - 1]) / max(1e-9, cum[j] - cum[j - 1]); a, b_ = samp[j - 1], samp[j]
        return (a[0] + (b_[0] - a[0]) * f, a[1] + (b_[1] - a[1]) * f)
    pts = [at_len(i * ds) for i in range(n + 1)]
    psi = []
    for i in range(n):
        psi.append(math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0]))
    for i in range(1, n):
        while psi[i] - psi[i - 1] > math.pi: psi[i] -= 2 * math.pi
        while psi[i] - psi[i - 1] < -math.pi: psi[i] += 2 * math.pi
    sig = smooth / ds; half = int(3 * sig); ker = [math.exp(-0.5 * (j / sig) ** 2) for j in range(-half, half + 1)]; ks_ = sum(ker)
    ext = [psi[0]] * half + psi + [psi[-1] + (psi[-1] - psi[-2]) * (j + 1) for j in range(half)]
    sm = [sum(ker[j] * ext[i + j] for j in range(2 * half + 1)) / ks_ for i in range(n)]
    samp = [B]
    for i in range(n):
        samp.append((samp[-1][0] + ds * math.cos(sm[i]), samp[-1][1] + ds * math.sin(sm[i])))
    cum = [i * ds for i in range(n + 1)]; L = cum[-1]; Lm = min(Lm0, L - 1)
    w0 = math.dist(Qhi, Qlo) / 2
    hi, lo, thi, tlo = [], [], [], []
    for i, p in enumerate(samp):
        a_ = sm[0] if i == 0 else (sm[n - 1] if i == n else (sm[i - 1] + sm[i]) / 2)
        kap = 0.0 if i == 0 or i == n else (sm[i] - sm[i - 1]) / ds
        tx, ty = math.cos(a_), math.sin(a_); nx, ny = -ty, tx
        u = cum[i] / L
        w = w0 + (w_end - w0) * u ** power
        dw = (w_end - w0) * power * max(u, 1e-3) ** (power - 1) / L
        hi.append((p[0] + nx * w, p[1] + ny * w)); lo.append((p[0] - nx * w, p[1] - ny * w))
        a1 = (tx * (1 - w * kap) + nx * dw, ty * (1 - w * kap) + ny * dw); a2 = (tx * (1 + w * kap) - nx * dw, ty * (1 + w * kap) - ny * dw)
        thi.append((a1[0] / math.hypot(*a1), a1[1] / math.hypot(*a1))); tlo.append((a2[0] / math.hypot(*a2), a2[1] / math.hypot(*a2)))
    end_ang = math.degrees(sm[-1])
    ks = [skip + (Lm - skip) * j / n_main for j in range(n_main)] + [Lm + (L - Lm) * j / n_curl for j in range(n_curl + 1)]
    idx = [min(range(len(samp)), key=lambda i: abs(cum[i] - s)) for s in ks]; idx[-1] = len(samp) - 1
    def edge(q, pos, tan):
        P_ = [q] + [pos[i] for i in idx]
        d0 = (P_[1][0] - q[0], P_[1][1] - q[1]); l0_ = math.hypot(*d0)
        T_ = [(d0[0] / l0_, d0[1] / l0_)] + [tan[i] for i in idx]
        out = []
        for j in range(len(P_) - 1):
            d = math.dist(P_[j], P_[j + 1]) / 3
            out.append(Seg(P_[j], (P_[j][0] + T_[j][0] * d, P_[j][1] + T_[j][1] * d), (P_[j + 1][0] - T_[j + 1][0] * d, P_[j + 1][1] - T_[j + 1][1] * d), P_[j + 1]))
        return out
    e_hi = edge(Qhi, hi, thi); e_lo = edge(Qlo, lo, tlo)
    ang = end_ang
    cap = arc(samp[-1][0], samp[-1][1], w_end, w_end, ang + 90, ang - 90, start=e_hi[-1].b, end=e_lo[-1].b)
    outline = e_hi + cap + rev(e_lo)
    base = arc(C[0], C[1], R, R, a_lo, a_hi, start=Qlo, end=Qhi)
    return outline, base, samp


ARMS = [
    arm(0, (17.0, 44.0), 215, 6.0, 7.0, 250, 9.0, 2.2),
    arm(1, (14.5, 63.0), 190, 7.0, 7.0, 250, 9.0, 2.2),
    arm(2, (25.5, 79.0), 150, 8.0, 8.0, 245, 8.5, 2.2),
    arm(3, (40.5, 84.5), 115, 8.0, 9.0, 240, 8.0, 2.2),
]

EY = 30.0
eyeL = circle(43.0, EY, 3.0); eyeR = circle(57.0, EY, 3.0)
shL = circle(44.0, EY - 1.0, 1.05); shR = circle(58.0, EY - 1.0, 1.05)
smile = [Seg((45.6, 36.6), (47.3, 40.2), (52.7, 40.2), (54.4, 36.6))]

def arm_lines(k):
    o, b, _ = ARMS[k]
    return [line(*o), line(*mirror(o))]

def arm_fills(k):
    o, b, _ = ARMS[k]
    return [fill(FILL['pink'], *(o + b)), fill(FILL['pink'], *(mirror(o) + mirror(b)))]

steps = [
    step('Start with an o', 'Draw a letter o near the top of your paper: one round shape, nice and big. This o is hiding in the octopus.',
         [ring(*O_)]),
    step('Two arms', 'Draw two long arms under the o. Each one starts on the o, wiggles down, curls round at the end and comes back to the o.',
         arm_lines(3)),
    step('Two more arms', 'Draw one more arm on each side. Start where the last arm joined the o. Go out, curl up at the end and come back to the o.',
         arm_lines(2)),
    step('And two more', 'Draw another arm on each side, in the same way. These two go out to the sides.',
         arm_lines(1)),
    step('The last two arms', 'Draw the last two arms, one on each side of the o. Curl them up. Now the octopus has eight arms.',
         arm_lines(0)),
    step('The eyes', 'Draw two round eyes in the middle of the o. Draw a tiny circle in each one for the shine.',
         [ring(*eyeL), ring(*eyeR), ring(*shL), ring(*shR)]),
    step('The smile', 'Draw a happy smile under the eyes.',
         [line(*smile)]),
    step('Colour pink', 'Colour the octopus pink: the round head and all eight arms. Go round the eyes.',
         [fill(FILL['pink'], *O_, cut=[d_fill(*eyeL), d_fill(*eyeR)])] + arm_fills(3) + arm_fills(2) + arm_fills(1) + arm_fills(0), use='pink'),
    step('Colour the eyes', 'Colour the eyes black. Leave the shine white.',
         [fill(FILL['black'], *eyeL, cut=[d_fill(*shL)]), fill(FILL['black'], *eyeR, cut=[d_fill(*shR)])], use='black'),
]

D = drawing('dx_octopus_o', 'o is for octopus', 3, 15, 'animals', ['Letters', 'Animals'],
            'A happy pink octopus with eight curly arms. The small letter o is hiding in it: the o is the octopus\'s round head.',
            steps, ['pink', 'black'])
json.dump(D, open(os.path.join(OUT, 'octopus.json'), 'w'))
json.dump([d_fill(*shL), d_fill(*shR)], open(os.path.join(OUT, 'octopus.white.json'), 'w'))
json.dump({'set': 'animals-az', 'slot': 'o', 'kind': 'swim', 'age_from': 5}, open(os.path.join(OUT, 'octopus.place.json'), 'w'))
print('octopus: %d steps' % len(steps))
