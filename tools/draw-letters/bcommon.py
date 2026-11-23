"""Small things the seven vehicle builds share (22 Nov 2026)."""
import json, os, subprocess, sys
from vkit import *
import check as CK

HERE = os.path.dirname(os.path.abspath(__file__))


def cloud(x, y, s=1.0):
    """a little cloud with a flat bottom; (x, y) is its bottom-left corner"""
    pts = [(0, 0), (-2.6, -2.4), (-1.2, -6), (2.6, -6.4), (5.2, -9.2), (9.2, -7.6), (10.4, -4.2), (13.2, -2.6), (11.8, 0)]
    return smooth([(x + a * s, y + b * s) for a, b in pts], closed=True, k=0.9)


def star5(cx, cy, r, k=0.46):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * k
        a = math.radians(-90 + 36 * i)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(*pts, closed=True)


def wavy(x0, x1, y, amp=1.2, wl=11.0):
    k = max(2, int(round((x1 - x0) / (wl / 2))))
    pts = [(x0 + (x1 - x0) * i / k, y + (amp if i % 2 else -amp)) for i in range(k + 1)]
    return smooth(pts)


def finish(name, D, place, pic, letter_steps=1, allow=()):
    """save, run the checks, draw the quick look; returns True when every check passes"""
    save(name, D, place)
    save_white(name, pic.white)
    r, info = CK.check(D, verbose=False, letter_steps=letter_steps, allow_cross=allow, white=tuple(pic.white))
    good = all(g for _, g, _ in r)
    for n, g, dtl in r:
        if not g: print('   FAIL', n, '->', dtl)
    for i in info: print('   ', i)
    xs = []
    for st in D['steps']:
        for it in st['add']:
            xs += [float(v) for v in re.findall(r'-?\d*\.?\d+', it['d'])]
    print('   %s: %d steps, %s' % (name, len(D['steps']), 'ALL 9 CHECKS PASS' if good else 'CHECKS FAILED'))
    preview(D, os.path.join(HERE, 'out', name + '-look.png'))
    return good
