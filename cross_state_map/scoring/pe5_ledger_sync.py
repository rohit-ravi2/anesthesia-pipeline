"""Verify every citation now load-bearing in a row and append it to ledger.json.

A PMID enters the ledger only after its title has been FETCHED from eutils in this run (never
recalled) and recorded verbatim. Anything that fails to resolve is written to the unresolved list
and must be removed from the row or replaced.
"""
import json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lit

LEDF = os.path.join(HERE, 'ledger.json')
led = json.load(open(LEDF))

used = set()
for f in glob.glob(os.path.join(HERE, 'rows_v2', '*.json')):
    d = json.load(open(f))
    for c in d['cells']:
        for m in c['mechanisms']:
            used.update(m.get('citation_ids', []))
            for p in m['perturbations']:
                used.update(p.get('citation_ids', []))
            for r in m.get('roles', []):
                used.update(r.get('citation_ids', []))
            for s in m.get('chain', []):
                used.update(s.get('citation_ids', []))

new = sorted(x for x in used if x not in led and x.startswith('PMID:'))
print('load-bearing citations: %d ; already in ledger: %d ; to verify: %d'
      % (len(used), len(used) - len(new), len(new)))

unresolved = []
for i in range(0, len(new), 100):
    chunk = new[i:i + 100]
    meta, missing = lit.verify([x.split(':')[1] for x in chunk])
    for x in chunk:
        p = x.split(':')[1]
        if p in meta:
            m = meta[p]
            led[x] = dict(pmid=p, title=m['title'], journal=m['journal'], year=m['year'],
                          first_author=(m['authors'][0] if m['authors'] else None), doi=m['doi'],
                          verified_utc='2026-09-17', verification='title fetched from eutils esummary '
                                                                 'in the PE-5 round-2 run')
            print('  VERIFIED %s  %s' % (p, m['title'][:96]))
        else:
            unresolved.append(x)
            print('  UNRESOLVED %s' % p)

json.dump(led, open(LEDF, 'w'), indent=1)
print('ledger now %d entries; unresolved %d' % (len(led), len(unresolved)))
if unresolved:
    json.dump(unresolved, open(os.path.join(HERE, 'UNRESOLVED_CITATIONS.json'), 'w'), indent=1)
