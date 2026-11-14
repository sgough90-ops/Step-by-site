"""Line and picture checks for a Step by Draw drawing (stepby/1 data).

    python3 check.py out/<name>.json [steps whose lines may cross] [number of letter steps]

Reads out/<name>.white.json (a JSON list of hole paths meant to stay white) if it is there.
Reads the path text exactly as the app will (M L C Q A Z, absolute), so the checks see what the app draws.
"""
import json, math, os, re, sys
import numpy as np
from scipy.spatial import cKDTree
from skimage.draw import polygon as skpoly
from scipy.ndimage import binary_erosion

TOK = re.compile(r'[MLCQAZ]|-?\d*\.?\d+(?:e-?\d+)?')


def arc_pts(x1, y1, rx, ry, phi, fa, fs, x2, y2, n):
    phi = math.radians(phi); c, s = math.cos(phi), math.sin(phi)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = c * dx + s * dy, -s * dx + c * dy
    rx, ry = abs(rx), abs(ry)
    lam = x1p ** 2 / rx ** 2 + y1p ** 2 / ry ** 2
    if lam > 1: rx *= math.sqrt(lam); ry *= math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    co = math.sqrt(max(0, num / den)) * (-1 if fa == fs else 1)
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx = c * cxp - s * cyp + (x1 + x2) / 2; cy = s * cxp + c * cyp + (y1 + y2) / 2
    ang = lambda ux, uy, vx, vy: math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not fs and dt > 0: dt -= 2 * math.pi
    if fs and dt < 0: dt += 2 * math.pi
    out = []
    for i in range(1, n + 1):
        t = t1 + dt * i / n
        out.append((cx + rx * math.cos(t) * c - ry * math.sin(t) * s, cy + rx * math.cos(t) * s + ry * math.sin(t) * c))
    return out


def parse(d, step=0.02):
    """List of subpaths; each is (points, closed). Points are dense samples."""
    t = TOK.findall(d); i = 0; subs = []; cur = None; start = None; pts = []
    def num():
        nonlocal i
        v = float(t[i]); i += 1; return v
    def dens(p0, p1):
        L = math.dist(p0, p1); return max(2, int(L / step) + 2)
    cmd = None
    while i < len(t):
        if t[i] in 'MLCQAZ':
            cmd = t[i]; i += 1
            if cmd == 'Z':
                if pts:
                    if math.dist(pts[-1], start) > 1e-9:
                        n = dens(pts[-1], start)
                        pts += [(pts[-1][0] + (start[0] - pts[-1][0]) * k / (n - 1), pts[-1][1] + (start[1] - pts[-1][1]) * k / (n - 1)) for k in range(1, n)]
                    subs.append((pts, True)); pts = []; cur = start
                continue
        if cmd == 'M':
            if pts: subs.append((pts, False))
            cur = (num(), num()); start = cur; pts = [cur]; cmd = 'L'
        elif cmd == 'L':
            p = (num(), num()); n = dens(cur, p)
            pts += [(cur[0] + (p[0] - cur[0]) * k / (n - 1), cur[1] + (p[1] - cur[1]) * k / (n - 1)) for k in range(1, n)]; cur = p
        elif cmd == 'C':
            c1 = (num(), num()); c2 = (num(), num()); p = (num(), num())
            L = math.dist(cur, c1) + math.dist(c1, c2) + math.dist(c2, p); n = max(3, int(L / step) + 2)
            for k in range(1, n):
                u = k / (n - 1); v = 1 - u
                pts.append((v*v*v*cur[0] + 3*v*v*u*c1[0] + 3*v*u*u*c2[0] + u*u*u*p[0], v*v*v*cur[1] + 3*v*v*u*c1[1] + 3*v*u*u*c2[1] + u*u*u*p[1]))
            cur = p
        elif cmd == 'Q':
            c1 = (num(), num()); p = (num(), num())
            L = math.dist(cur, c1) + math.dist(c1, p); n = max(3, int(L / step) + 2)
            for k in range(1, n):
                u = k / (n - 1); v = 1 - u
                pts.append((v*v*cur[0] + 2*v*u*c1[0] + u*u*p[0], v*v*cur[1] + 2*v*u*c1[1] + u*u*p[1]))
            cur = p
        elif cmd == 'A':
            rx, ry, ph, fa, fs, x, y = num(), num(), num(), num(), num(), num(), num()
            L = math.pi * max(rx, ry); n = max(8, int(L / step) + 2)
            pts += arc_pts(cur[0], cur[1], rx, ry, ph, int(fa), int(fs), x, y, n); cur = (x, y)
    if pts: subs.append((pts, False))
    return subs


def run_len(mask, pts):
    best = cur = 0.0
    for k in range(1, len(pts)):
        if mask[k] and mask[k - 1]:
            cur += math.dist(pts[k], pts[k - 1]); best = max(best, cur)
        else:
            cur = 0.0
    return best


def seg_inter(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    if abs(d) < 1e-12: return None
    u = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    v = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d
    if 0 <= u <= 1 and 0 <= v <= 1: return (p1[0] + u * (p2[0] - p1[0]), p1[1] + u * (p2[1] - p1[1]))
    return None


def crossings(A, B, stepA=4, stepB=4):
    """Rough crossing points between two dense polylines (thinned for speed)."""
    a = A[::stepA] + [A[-1]]; b = B[::stepB] + [B[-1]]
    out = []
    ba = np.array(b)
    for k in range(len(a) - 1):
        p1, p2 = a[k], a[k + 1]
        lo = np.minimum(p1, p2) - 0.5; hi = np.maximum(p1, p2) + 0.5
        idx = np.where((ba[:, 0] >= lo[0]) & (ba[:, 0] <= hi[0]) & (ba[:, 1] >= lo[1]) & (ba[:, 1] <= hi[1]))[0]
        for j in idx:
            for jj in (j - 1, j):
                if 0 <= jj < len(b) - 1:
                    q = seg_inter(p1, p2, b[jj], b[jj + 1])
                    if q and all(math.dist(q, o) > 0.3 for o in out): out.append(q)
    return out


def check(P, verbose=True, letter_steps=1, allow_cross=(), white=()):
    S = P['steps']; res = []; info = []
    def ok(name, good, detail=''):
        res.append((name, good, detail))
    lines = []
    fills = []
    for si, st in enumerate(S):
        for ii, it in enumerate(st['add']):
            subs = parse(it['d'])
            if 'fill' in it:
                cuts = [parse(c) for c in it.get('cut', [])]
                fills.append((si, ii, it, subs, cuts))
            else:
                lines.append((si, ii, it, subs))
    allp = [p for _, _, _, subs in lines for pts, _ in subs for p in pts] + [p for f in fills for pts, _ in f[3] for p in pts]
    a = np.array(allp)
    ok('Everything inside 2 to 98', bool((a.min() >= 2).all() and (a.max() <= 98).all()), 'min %.2f max %.2f' % (a.min(), a.max()))
    corner = a[(a[:, 0] < 16) & (a[:, 1] < 16)]
    ok('Nothing under the step number (x and y both under 16)', len(corner) == 0, '%d points' % len(corner))
    lp = np.array([p for _, _, _, subs in lines for pts, _ in subs for p in pts]); tree = cKDTree(lp)
    worst = []
    for si, ii, it, subs, cuts in fills:
        for pts, _ in subs + [s for c in cuts for s in c]:
            d, _ = tree.query(np.array(pts[::5]))
            if d.max() > 0.06: worst.append('%d.%d %.3f at %s' % (si + 1, ii + 1, d.max(), tuple(np.round(np.array(pts[::5])[d.argmax()], 2))))
    ok('Every colour edge is on a drawn line (within 0.06)', not worst, '; '.join(worst[:6]))
    R = 20
    masks = []
    for si, ii, it, subs, cuts in fills:
        m = np.zeros((100 * R, 100 * R), bool)
        for pts, _ in subs + [s for c in cuts for s in c]:
            q = np.array(pts) * R
            rr, cc = skpoly(q[:, 1], q[:, 0], m.shape); t = np.zeros_like(m); t[rr, cc] = True; m ^= t
        masks.append(binary_erosion(m, iterations=2))
    over = []
    for x in range(len(masks)):
        for y in range(x + 1, len(masks)):
            n = int((masks[x] & masks[y]).sum())
            if n: over.append('%d.%d/%d.%d (%d px)' % (fills[x][0] + 1, fills[x][1] + 1, fills[y][0] + 1, fills[y][1] + 1, n))
    ok('No two colours overlap', not over, '; '.join(over[:6]))
    alld = set(f[2]['d'] for f in fills); bad = []; kept_white = []
    for si, ii, it, subs, cuts in fills:
        for c in it.get('cut', []):
            if c not in alld:
                if c in white: kept_white.append('%d.%d' % (si + 1, ii + 1))
                else: bad.append('%d.%d hole not filled' % (si + 1, ii + 1))
        ot = cKDTree(np.array([p for pts, _ in subs for p in pts]))
        for cs in cuts:
            for pts, _ in cs:
                dd, _ = ot.query(np.array(pts))
                if dd.min() < 0.3: bad.append('%d.%d hole touches its edge (%.2f)' % (si + 1, ii + 1, dd.min()))
    ok('Every hole is filled by another colour (or meant to stay white) and does not touch its edge', not bad, '; '.join(bad))
    if kept_white: info.append('Holes meant to stay white: ' + ', '.join(kept_white))
    along = []
    for x in range(len(lines)):
        for y in range(len(lines)):
            if x == y: continue
            A = [p for pts, _ in lines[x][3] for p in pts]; B = np.array([p for pts, _ in lines[y][3] for p in pts])
            t = cKDTree(B); d, _ = t.query(np.array(A)); L = run_len(d < 0.1, A)
            if L > 1.8: along.append('%d.%d along %d.%d for %.1f' % (lines[x][0] + 1, lines[x][1] + 1, lines[y][0] + 1, lines[y][1] + 1, L))
    ok('No line runs along another for more than 1.8', not along, '; '.join(along[:8]))
    letter = [l for l in lines if l[0] < letter_steps]
    cross = []; other_cross = []
    ends = lambda subs: [subs[0][0][0], subs[-1][0][-1]] + [e for pts, cl in subs for e in ((pts[0], pts[-1]) if not cl else ())]
    for l in lines:
        if l[0] < letter_steps: continue
        B = [p for pts, _ in l[3] for p in pts]; be = ends(l[3])
        for lt in letter:
            A = [p for pts, _ in lt[3] for p in pts]; ae = ends(lt[3])
            for q in crossings(B, A):
                if min(math.dist(q, e) for e in be) < 0.4 or min(math.dist(q, e) for e in ae) < 0.4: continue
                cross.append('%d.%d crosses the letter at %s' % (l[0] + 1, l[1] + 1, tuple(round(v, 2) for v in q)))
    ok('Nothing crosses the letter (lines may only touch it)', not cross, '; '.join(cross[:6]))
    for x in range(len(lines)):
        for y in range(x + 1, len(lines)):
            if lines[x][0] < letter_steps or lines[y][0] < letter_steps: continue
            A = [p for pts, _ in lines[x][3] for p in pts]; B = [p for pts, _ in lines[y][3] for p in pts]
            ae, be = ends(lines[x][3]), ends(lines[y][3])
            for q in crossings(A, B):
                if min(math.dist(q, e) for e in ae) < 0.4 or min(math.dist(q, e) for e in be) < 0.4: continue
                tag = '%d.%d x %d.%d' % (lines[x][0] + 1, lines[x][1] + 1, lines[y][0] + 1, lines[y][1] + 1)
                if tag.split(' x ')[0].split('.')[0] in allow_cross or tag.split(' x ')[1].split('.')[0] in allow_cross: continue
                other_cross.append(tag + ' at %s' % (tuple(round(v, 1) for v in q),))
    ok('Lines only cross where meant', not other_cross, '; '.join(other_cross[:8]))
    mats = [m['id'] for m in P['materials'] if m['kind'] == 'pencil' and m['id'] != 'pencil']
    used = set(); probs = []
    first_fill = min([i for i, st in enumerate(S) if any('fill' in a for a in st['add'])] or [99])
    last_line = max([i for i, st in enumerate(S) if any('fill' not in a for a in st['add'])] or [-1])
    for i, st in enumerate(S):
        if len(st['use']) != 1: probs.append('step %d uses %d pencils' % (i + 1, len(st['use'])))
        isf = any('fill' in a for a in st['add']); isl = any('fill' not in a for a in st['add'])
        if isf and isl: probs.append('step %d mixes lines and colour' % (i + 1))
        if isl and st['use'] != ['pencil']: probs.append('line step %d not pencil' % (i + 1))
        if isf: used |= set(st['use'])
        if not st['add']: probs.append('step %d adds nothing' % (i + 1))
    if set(mats) - used: probs.append('pencils never used: %s' % (set(mats) - used))
    if last_line > first_fill: probs.append('a line step comes after colouring starts')
    ok('One pencil a step, lines first, every pencil used', not probs, '; '.join(probs))
    loose = []
    for x, l in enumerate(lines):
        for pts, cl in l[3]:
            if cl or math.dist(pts[0], pts[-1]) < 0.05: continue
            for e in (pts[0], pts[-1]):
                near = False
                for y, m in enumerate(lines):
                    if y == x: continue
                    for q, _ in m[3]:
                        if min(math.dist(e, z) for z in q[::3]) < 0.3: near = True; break
                    if near: break
                if not near and not (len(pts) < 20 and math.dist(pts[0], pts[-1]) < 0.5):
                    loose.append('%d.%d %s' % (l[0] + 1, l[1] + 1, tuple(round(v, 1) for v in e)))
    info.append('Loose line ends (check they are meant): ' + (', '.join(loose) if loose else 'none'))
    if verbose:
        for n, g, dtl in res: print(('PASS ' if g else 'FAIL ') + n + ('' if g or not dtl else '  -> ' + dtl))
        for i in info: print('     ' + i)
    return res, info


if __name__ == '__main__':
    f = sys.argv[1]
    P = json.load(open(f))
    allow = tuple(x for x in sys.argv[2].split(',') if x) if len(sys.argv) > 2 else ()
    ls = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    wf = f[:-5] + '.white.json'
    white = json.load(open(wf)) if os.path.exists(wf) else ()
    r, _ = check(P, allow_cross=allow, letter_steps=ls, white=white)
    sys.exit(0 if all(g for _, g, _ in r) else 1)
