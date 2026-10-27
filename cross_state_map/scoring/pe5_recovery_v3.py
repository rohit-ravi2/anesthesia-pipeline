"""PE-5 Gate C — per-row retrieval adequacy under the PRODUCTION protocol.

Runs the exact query battery used by pe5_pipeline.py (same boolean OR-groups, same depth) and
measures what fraction of each row's already-known load-bearing PMIDs the battery recovers.

A row passes Gate C at recall >= 0.90, or at lower recall if EVERY miss is individually explained
and the explanation is recorded in pe5_recovery/<row_id>.json. An unexplained miss means the row's
NOT_TESTED cells are uninterpretable, because the battery demonstrably cannot retrieve material it
is pointed at.

Queries are cached on disk by lit.py, so re-running after the pipeline is nearly free.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lit
from pe5_pipeline import build, DEPTH, ROWSP
from pe5_vocab_v3 import STATE

OUT = os.path.join(HERE, 'pe5_recovery')
os.makedirs(OUT, exist_ok=True)

# Misses that are explained rather than defects. Keyed by pmid; the explanation must say why the
# paper is unreachable by a generic mechanism-class battery, not merely that it was not returned.
EXPLAINED = json.load(open(os.path.join(HERE, 'pe5_miss_explanations.json'))) \
    if os.path.exists(os.path.join(HERE, 'pe5_miss_explanations.json')) else {}


def known_pmids(rid):
    """Every PMID currently load-bearing for a scored cell in this row."""
    d = json.load(open(os.path.join(HERE, 'rows_v2', rid + '.json')))
    s = set()
    for c in d['cells']:
        if c['coverage'] == 'NOT_TESTED':
            continue
        for m in c['mechanisms']:
            s.update(m.get('citation_ids', []))
            for p in m['perturbations']:
                s.update(p.get('citation_ids', []))
    return {x.split(':')[1] for x in s if x.startswith('PMID:')}


def measure(rid):
    d = DEPTH[ROWSP[rid]]
    retrieved, byq = set(), []
    for cid, route, q in build(rid):
        try:
            ids = lit.esearch(q, n=d)
        except Exception as e:
            byq.append(dict(cls=cid, route=route, error=str(e))); continue
        retrieved.update(ids)
        byq.append(dict(cls=cid, route=route, n=len(ids)))
    known = known_pmids(rid)
    hit = sorted(known & retrieved)
    miss = sorted(known - retrieved)
    unexplained = [p for p in miss if p not in EXPLAINED]
    recall = round(len(hit) / max(len(known), 1), 3)
    rec = dict(
        row_id=rid, protocol='v3_boolean_or_groups_repaired_vocabulary', depth=d,
        n_queries=len(byq), n_retrieved_unique=len(retrieved),
        n_known=len(known), n_recovered=len(hit), recall=recall,
        recovered=hit, missed=miss,
        missed_explained={p: EXPLAINED[p] for p in miss if p in EXPLAINED},
        missed_unexplained=unexplained,
        gate_c_pass=bool(known) and (recall >= 0.90 or not unexplained),
        per_query=byq,
    )
    json.dump(rec, open(os.path.join(OUT, rid + '.json'), 'w'), indent=1)
    return rec


def main(rows=None):
    rows = rows or list(STATE)
    summary, tk, th = {}, 0, 0
    for rid in rows:
        r = measure(rid)
        tk += r['n_known']; th += r['n_recovered']
        summary[rid] = {k: r[k] for k in
                        ('recall', 'n_known', 'n_recovered', 'missed_unexplained', 'gate_c_pass')}
        print('%-24s known=%2d recovered=%2d recall=%.2f unexplained=%d %s'
              % (rid, r['n_known'], r['n_recovered'], r['recall'],
                 len(r['missed_unexplained']), 'PASS' if r['gate_c_pass'] else 'FAIL'), flush=True)
    summary['_overall'] = dict(n_known=tk, n_recovered=th,
                               recall=round(th / max(tk, 1), 3),
                               rows_passing=sum(1 for k, v in summary.items() if v.get('gate_c_pass')),
                               interpretation='internal protocol sensitivity on already-scored rows; '
                                              'NOT an estimate of literature-wide recall')
    json.dump(summary, open(os.path.join(HERE, 'PE5_RECOVERY_SUMMARY.json'), 'w'), indent=1)
    print('\nOVERALL %d/%d = %.2f' % (th, tk, summary['_overall']['recall']))
    return summary


if __name__ == '__main__':
    main(sys.argv[1:] or None)
