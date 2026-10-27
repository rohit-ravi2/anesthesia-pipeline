"""PE-5 Route 3 — CITATION_CHAIN, executed systematically rather than opportunistically.

Every prior run marked this route PENDING because it was done by hand on a few papers. This does it
properly: for each row, seed on the PMIDs already load-bearing for that row, expand one hop in both
directions via eutils elink (what cites them, what they cite), drop everything already in the ledger,
and rank the remainder with the same prefilter used by the retrieval pipeline.

Rationale for a citation route at all: the four documented failure modes of keyword retrieval
(malformation, phenotype-framing, paralogue-in-adjacent-literature, clinical-endpoint indexing) are
all failures of VOCABULARY. A citation edge does not depend on vocabulary, so this route is the one
independent check on the keyword battery.
"""
import json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lit
from pe5_vocab_v3 import STATE
from pe5_pipeline import CAUSAL, STATEWORD, WRONGPREP
from pe5_recovery_v3 import known_pmids

LED = set(json.load(open(os.path.join(HERE, "ledger.json"))).keys())


def chain(rid):
    seeds = sorted(known_pmids(rid))
    if not seeds:
        return dict(row_id=rid, n_seeds=0, status='NO_SEEDS', candidates=[])
    edges = collections.defaultdict(lambda: dict(citedin=[], refs=[]))
    for s in seeds:                      # one seed at a time so edges stay attributable
        for ln, k in (('pubmed_pubmed_citedin', 'citedin'), ('pubmed_pubmed_refs', 'refs')):
            try:
                for p in lit.elink([s], ln):
                    edges[p][k].append(s)
            except Exception:
                pass
    cand = [p for p in edges if p not in seeds and ('PMID:' + p) not in LED]
    meta = {}
    for i in range(0, len(cand), 180):
        try:
            meta.update(lit.esummary(cand[i:i + 180]))
        except Exception:
            pass
    ranked = []
    for p in cand:
        d = meta.get(p)
        if not d:
            continue
        t, e = d['title'], edges[p]
        score = 2 * (len(e['citedin']) + len(e['refs']) - 1)   # multi-seed edges rank first
        if CAUSAL.search(t):
            score += 3
        if re.search(STATEWORD[rid], t, re.I):
            score += 2
        if WRONGPREP.search(t):
            score -= 3
        if any(x.lower().startswith('review') for x in d.get('pubtype', [])):
            score -= 3
        ranked.append(dict(pmid=p, score=score, year=d['year'], journal=d['journal'], title=t,
                           cited_seeds=e['citedin'], ref_seeds=e['refs']))
    ranked.sort(key=lambda x: -x['score'])
    return dict(row_id=rid, n_seeds=len(seeds), seeds=seeds, n_linked=len(edges),
                n_candidates=len(ranked), status='COMPLETE', candidates=ranked)


def main(rows=None):
    rows = rows or list(STATE)
    out = {}
    for rid in rows:
        r = chain(rid)
        out[rid] = r
        print('%-24s seeds=%2d linked=%4d new_candidates=%4d top_score=%s'
              % (rid, r['n_seeds'], r.get('n_linked', 0), r.get('n_candidates', 0),
                 r['candidates'][0]['score'] if r['candidates'] else '-'), flush=True)
    json.dump(out, open(os.path.join(HERE, 'pe5_citation_chain.json'), 'w'), indent=1)
    return out


if __name__ == '__main__':
    main(sys.argv[1:] or None)
