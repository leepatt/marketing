#!/usr/bin/env python3
"""make-v2.py — derive the v2 timeline from the cut's words and write cues-v2.json + fw-reel2/index.html."""
import json, re, sys
W = json.load(open(sys.argv[1])); OUT = sys.argv[2]
norm = lambda s: re.sub(r"[^a-z0-9' ]", "", s.lower().replace('-', ' ')).strip()
toks = [norm(w['w']) for w in W]
def at(phrase, start=0, nth=1):
    p = norm(phrase).split(); hits = 0
    for i in range(start, len(toks) - len(p) + 1):
        if toks[i:i+len(p)] == p:
            hits += 1
            if hits == nth: return W[i]['s'], i
    raise SystemExit('not found: ' + phrase)
T_fw, i_fw = at('formwork builder')          # cut to the hero card on "Formwork"
T_shape, i_sh = at('you choose')             # cut to the builder
T_end = W[-1]['e']
rel = lambda t: round(t - T_shape, 2)
c = {}
c['s00-load'] = 0.0
c['s01-ushape'] = rel(at('u shape', i_sh)[0])
c['s02-circle'] = c['s01-ushape'] + 1.3
t_dims = at('change', i_sh)[0]
c['s03-thickness'] = rel(t_dims); c['s04-radius'] = rel(t_dims) + 0.9; c['s05-height'] = rel(t_dims) + 1.8; c['s06-angle'] = rel(t_dims) + 2.7
c['s07-backrest-on'] = rel(at('backrest', i_sh)[0])
c['s08-br-height'] = rel(at('height', i_sh)[0])
c['s09-br-width'] = rel(at('width', i_sh)[0])
c['s10-cantilever-on'] = rel(at('cantilever', i_sh)[0])
c['s11-scroll-formwork'] = rel(at('scroll', i_sh)[0])
c['s12-plates'] = rel(at('plates', i_sh)[0])
c['s13-shutters'] = rel(at('shutters', i_sh)[0])
c['s14-endcaps'] = rel(at('end caps', i_sh)[0]) - 0.2
c['s15-summary'] = rel(at('spending', i_sh)[0])
c['s16-model'] = rel(at("don't", i_sh)[0])
c['s17-summary-bottom'] = rel(at('add to cart', i_sh)[0])
json.dump(c, open(OUT + '/cues-v2.json', 'w'), indent=1)
demo_len = round(T_end - T_shape + 0.6, 2); total = round(T_end + 4.4, 2); T_endcard = round(T_end - 0.2, 2)
print(json.dumps({'T_fw': T_fw, 'T_shape': T_shape, 'T_end': T_end, 'demo_len': demo_len, 'total': total}))
print(c)
html = open(OUT + '/index.template.html').read()
for k, v in {'T_FW': T_fw, 'T_HERO_DUR': round(T_shape - T_fw, 3), 'T_SHAPE': T_shape, 'DEMO_LEN': demo_len, 'T_END': round(T_end, 3), 'T_ENDCARD': T_endcard, 'TOTAL': total,
             'P_DIMS': c['s03-thickness'], 'P_DIMS_OUT': c['s07-backrest-on'] - 0.6, 'P_BR': c['s08-br-height'], 'P_BR_OUT': c['s11-scroll-formwork'] - 0.3,
             'P_FW': c['s12-plates'], 'P_FW_OUT': c['s15-summary'], 'P_MODEL': c['s16-model'], 'P_MODEL_OUT': c['s17-summary-bottom']}.items():
    html = html.replace('{{' + k + '}}', str(v))
assert '{{' not in html, 'unreplaced placeholder'
open(OUT + '/index.html', 'w').write(html); print('index.html written')
