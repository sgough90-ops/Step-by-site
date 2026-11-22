"""A tall step sheet that reads well on a phone: the letter in red and the finished picture on top, then every step,
two across (new lines red, earlier lines dark). Drawn by Chrome, like sheet.py.

    python3 sheet_phone.py out/<name>.json out/<name>-phone.png ["a note under the title"]
"""
import json, sys, html
from sheet import svg_for, _shot, INK, NEW


def red_letter(svg, P):
    for it in P['steps'][0]['add']:
        svg = svg.replace('d="%s" fill="none" stroke="%s"' % (html.escape(it['d']), INK), 'd="%s" fill="none" stroke="%s"' % (html.escape(it['d']), NEW))
    return svg


def phone(P, out, cols=2, size=260, note=None):
    last_line = max(i for i, st in enumerate(P['steps']) if any('fill' not in a for a in st['add']))
    a = red_letter(svg_for(P, last_line, size, final=True), P)
    b_ = svg_for(P, len(P['steps']) - 1, size, final=True)
    cells = []
    for i in range(len(P['steps'])):
        cells.append('<div class="c"><div class="n">%d</div>%s<div class="t">%s</div></div>' % (i + 1, svg_for(P, i, size), html.escape(P['steps'][i]['title'])))
    doc = '''<!doctype html><html><head><meta charset="utf-8"><style>
    body{margin:0;background:#f1f3f5;font-family:Arial,Helvetica,sans-serif}
    h1{font-size:30px;text-align:center;margin:16px 0 4px}
    h2{font-size:17px;font-weight:normal;color:#495057;text-align:center;margin:0 0 10px}
    .g{display:grid;grid-template-columns:repeat(%d,%dpx);gap:10px;padding:0 14px 14px;justify-content:center}
    .c{position:relative;background:#fff;border:2px solid #ced4da;border-radius:14px;overflow:hidden;padding-bottom:6px}
    .c svg{display:block}
    .n{position:absolute;left:10px;top:6px;font-weight:bold;font-size:24px}
    .t{text-align:center;font-size:15px;color:#495057}
    .k{text-align:center;font-size:15px;color:#495057;padding:4px 0 2px}
    </style></head><body><h1>%s</h1><h2>%s</h2>
    <div class="g"><div class="c">%s<div class="k">The hidden letter, in red</div></div><div class="c">%s<div class="k">Finished</div></div></div>
    <h2>The steps</h2><div class="g">%s</div></body></html>''' % (cols, size, html.escape(P['title']), html.escape(note or ('%d steps' % len(P['steps']))), a, b_, ''.join(cells))
    _shot(doc, out, cols * (size + 14) + 34, 800, True)


if __name__ == '__main__':
    P = json.load(open(sys.argv[1]))
    phone(P, sys.argv[2], note=sys.argv[3] if len(sys.argv) > 3 else None)
