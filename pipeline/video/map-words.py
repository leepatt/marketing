#!/usr/bin/env python3
"""map-words.py — map source-time words through a cut sheet onto the cut's timeline (no re-transcription).
Usage: map-words.py source-words.json cut-sheet.txt out-words.json"""
import json, sys
words = json.load(open(sys.argv[1]))
ranges = [(float(o), float(i), float(e)) for o, i, e, d in (l.split() for l in open(sys.argv[2]) if not l.startswith('#'))]
out = []
for w in words:
    dur = max(0.02, w['e'] - w['s'])
    for o, i, e in ranges:
        if (min(e, w['e']) - max(i, w['s'])) / dur >= 0.6:
            out.append({'w': w['w'], 's': round(max(o, o + w['s'] - i), 3), 'e': round(min(o + (e - i), o + w['e'] - i), 3), 'p': w.get('p', 1)}); break
json.dump(out, open(sys.argv[3], 'w'))
print(f"{len(out)} of {len(words)} words kept; last ends {out[-1]['e']}s"); print(''.join(x['w'] for x in out).strip())
