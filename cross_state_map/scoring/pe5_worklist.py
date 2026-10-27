"""PE-5 stage 5 — turn 11k ranked candidates into a per-cell scoring worklist.

Each (row, class) cell gets the top-ranked candidates that were retrieved *for that cell* by the
production battery, restricted to candidates whose title carries both a causal-manipulation signal
and the row's state vocabulary. Those are the only ones worth an abstract fetch; the rest of the
retrieval set is recorded as screened-and-rejected-at-title, which is what makes a null defensible.
"""
import json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lit
from pe5_pipeline import CAUSAL, STATEWORD, WRONGPREP

N_PER_CELL = int(os.environ.get('PE5_N_PER_CELL', '6'))


def build(min_score=4):
    ranked = json.load(open(os.path.join(HERE, 'pe5_ranked_candidates.json')))
    chain = {}
    cp = os.path.join(HERE, 'pe5_citation_chain.json')
    if os.path.exists(cp):
        chain = json.load(open(cp))

    per = collections.defaultdict(list)
    for x in ranked:
        if x['score'] < min_score:
            continue
        for rid in x['rows']:
            if not re.search(STATEWORD[rid], x['title'], re.I):
                continue                      # title does not even mention this row's state
            for cid in x['classes']:
                per[(rid, cid)].append(dict(x, src='RETRIEVAL'))

    for rid, rec in chain.items():
        for x in rec.get('candidates', [])[:120]:
            if x['score'] < 4 or not re.search(STATEWORD[rid], x['title'], re.I):
                continue
            per[(rid, 0)].append(dict(x, src='CITATION_CHAIN', classes=[0], rows=[rid]))

    work = {}
    for (rid, cid), v in per.items():
        v.sort(key=lambda d: -d['score'])
        seen, keep = set(), []
        for d in v:
            if d['pmid'] in seen:
                continue
            seen.add(d['pmid'])
            keep.append(d)
        work['%s|c%d' % (rid, cid)] = dict(n_screened=len(v), candidates=keep[:N_PER_CELL])

    json.dump(work, open(os.path.join(HERE, 'PE5_WORKLIST.json'), 'w'), indent=1)
    tot = sum(len(v['candidates']) for v in work.values())
    print('cells with candidates: %d ; abstracts to read: %d' % (len(work), tot))
    return work


def show(prefix=''):
    work = json.load(open(os.path.join(HERE, 'PE5_WORKLIST.json')))
    for k in sorted(work):
        if not k.startswith(prefix):
            continue
        print('== %s (screened %d)' % (k, work[k]['n_screened']))
        for c in work[k]['candidates']:
            print('   %2d %s %s %s | %s' % (c['score'], c['pmid'], c['year'],
                                            c.get('src', '')[:4], c['title'][:118]))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        show(sys.argv[2] if len(sys.argv) > 2 else '')
    else:
        build()
