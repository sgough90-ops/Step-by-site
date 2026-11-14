"""Draws a numbered step sheet for a drawing (new lines red, earlier lines dark), using Chrome so curves are drawn
exactly as a browser draws the app's path text.

    python3 sheet.py out/<name>.json out/<name>-steps.png ["Title"]
    python3 sheet.py out/<name>.json out/<name>-pair.png --pair
"""
import json, sys, html
from playwright.sync_api import sync_playwright

INK = '#343a40'; NEW = '#e03131'


def svg_for(P, upto, size=300, final=False):
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="%d" height="%d">' % (size, size),
             '<rect width="100" height="100" fill="#ffffff"/>']
    fills, lines = [], []
    for si, st in enumerate(P['steps'][:upto + 1]):
        for it in st['add']:
            if 'fill' in it:
                d = it['d'] + ''.join(' ' + c for c in it.get('cut', []))
                fills.append('<path d="%s" fill="%s" fill-rule="evenodd"/>' % (html.escape(d), it['fill']))
            else:
                col = NEW if (si == upto and not final) else INK
                lines.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.3f" stroke-linecap="round" stroke-linejoin="round"/>' % (html.escape(it['d']), col, it.get('w', 1.8) * 0.6))
    parts += fills + lines + ['</svg>']
    return ''.join(parts)


def _shot(doc, out, w, h, full=False):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.set_content(doc); pg.wait_for_timeout(100)
        pg.screenshot(path=out, full_page=full); b.close()


def sheet(P, out, title=None, cols=4, size=300):
    n = len(P['steps'])
    cells = []
    for i in range(n):
        cells.append('<div class="c"><div class="n">%d</div>%s<div class="t">%s</div></div>' % (i + 1, svg_for(P, i, size), html.escape(P['steps'][i]['title'])))
    doc = '''<!doctype html><html><head><meta charset="utf-8"><style>
    body{margin:0;background:#f1f3f5;font-family:Arial,Helvetica,sans-serif}
    h1{font-size:30px;text-align:center;margin:18px 0 10px}
    .g{display:grid;grid-template-columns:repeat(%d,%dpx);gap:12px;padding:0 16px 18px;justify-content:center}
    .c{position:relative;background:#fff;border:2px solid #ced4da;border-radius:14px;overflow:hidden;padding-bottom:6px}
    .c svg{display:block}
    .n{position:absolute;left:10px;top:6px;font-weight:bold;font-size:26px}
    .t{text-align:center;font-size:16px;color:#495057}
    </style></head><body><h1>%s</h1><div class="g">%s</div></body></html>''' % (cols, size, html.escape(title or P['title']), ''.join(cells))
    _shot(doc, out, cols * (size + 16) + 40, 800, True)


def pair(P, out, size=560):
    """Lines only (letter in red) beside the finished coloured picture: for a close look."""
    last_line = max(i for i, st in enumerate(P['steps']) if any('fill' not in a for a in st['add']))
    a = svg_for(P, last_line, size, final=True)
    for it in P['steps'][0]['add']:
        a = a.replace('d="%s" fill="none" stroke="%s"' % (html.escape(it['d']), INK), 'd="%s" fill="none" stroke="%s"' % (html.escape(it['d']), NEW))
    b_ = svg_for(P, len(P['steps']) - 1, size, final=True)
    _shot('<html><body style="margin:10px;background:#dee2e6;display:flex;gap:10px">%s%s</body></html>' % (a, b_), out, size * 2 + 30, size + 20)


if __name__ == '__main__':
    P = json.load(open(sys.argv[1]))
    if len(sys.argv) > 3 and sys.argv[3] == '--pair':
        pair(P, sys.argv[2])
    else:
        sheet(P, sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
