"""Small things the Food and drink number builds share (23 Nov 2026).
Like bcommon.py for the vehicle letters: finish() saves a drawing, runs the nine checks and draws the quick look."""
import json, os, re, sys
from vkit import *
import check as CK

HERE = os.path.dirname(os.path.abspath(__file__))
TAGS = ['Numbers', 'Around the house']          # the Food and drink sets still carry the old tag name
SET = 'house-09'


def extent(D):
    """how far the drawing reaches on the paper: x0, y0, x1, y1"""
    pts = [q for st in D['steps'] for it in st['add'] for sub, _ in CK.parse(it['d'], step=0.5) for q in sub]
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    return min(xs), min(ys), max(xs), max(ys)


def pdot(p, x, y, w=2.6):
    """a dot at a point given in the sketch's numbers"""
    return dot(*p.pt(x, y), w=w)


def finish(name, D, place, pic, letter_steps=1, allow=()):
    """save, run the checks, draw the quick look; returns True when every check passes"""
    save(name, D, place)
    save_white(name, pic.white)
    r, info = CK.check(D, verbose=False, letter_steps=letter_steps, allow_cross=allow, white=tuple(pic.white))
    good = all(g for _, g, _ in r)
    for n, g, dtl in r:
        if not g: print('   FAIL', n, '->', dtl)
    for i in info: print('   ', i)
    x0, y0, x1, y1 = extent(D)
    print('    on the paper: x %.1f to %.1f, y %.1f to %.1f (middle %.1f, %.1f)' % (x0, x1, y0, y1, (x0 + x1) / 2, (y0 + y1) / 2))
    print('    longest step text %d, bytes %d' % (max(len(st['text']) for st in D['steps']), len(json.dumps(D, separators=(',', ':')))))
    print('   %s: %d steps, %s' % (name, len(D['steps']), 'ALL 9 CHECKS PASS' if good else 'CHECKS FAILED'))
    preview(D, os.path.join(HERE, 'out', name + '-look.png'), px=700)
    return good
