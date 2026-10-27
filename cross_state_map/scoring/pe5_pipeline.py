"""PE-5 scalable retrieval pipeline: deep boolean retrieval -> global dedup -> prefilter.

Stage 1 broad retrieval at calibrated depth, Stage 2 global dedup, Stage 3 prefilter ranking.
Abstract fetch and scoring happen downstream, only on ranked plausible candidates.
"""
import json, os, sys, collections, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lit
from pe5_vocab_v3 import SPECIES, STATE, ENDPOINT, CLASS, NEG, DEPTH

LED = set(json.load(open(os.path.join(HERE, "ledger.json"))).keys())
def _sp(r):
    for suf in ('cele', 'mmus', 'hsap', 'isp'):
        if r.endswith('_' + suf):
            return suf
    raise ValueError('no species suffix: ' + r)

ROWSP = {r: _sp(r) for r in STATE}

# prefilter vocabulary: causal/organism-level signal vs preparation-only / irrelevant
CAUSAL = re.compile(r'\b(knock|mutant|mutation|deletion|deficient|null|conditional|optogenetic|chemogenetic|'
                    r'ablation|silenc|rescue|overexpress|transgenic|allele|RNAi|antagonist|agonist|'
                    r'required|necessary|sufficient|abolish|restore|reverse|prevent|EC50|MAC|'
                    r'loss of righting|threshold|sensitivity|resistant|hypersensitiv)', re.I)
STATEWORD = {
 'S9_hib_seasonal_isp': r'hibernat|torpor|torpid',
 'S9_hib_daily_mmus': r'torpor|torpid|hibernat',
 'S2_core_cele': r'lethargus|sleep|quiescen',
 'S5_ga_volatile_cele': r'anesthe|anaesthe|halothane|isoflurane|volatile',
 'S6_starv_L1_cele': r'L1|starvation|arrest|sleep|quiescen',
 'S7_dauer_cele': r'dauer|diapause',
 'S8_crypto_cele': r'anhydro|desicca|cryptobio',
 'S3_rem_mmus': r'\bREM\b|paradoxical sleep',
 'S4_deep_mmus': r'NREM|slow.wave|non.REM|sleep',
 'S5_ga_volatile_mmus': r'isoflurane|halothane|sevoflurane|anesthe|anaesthe',
 'S5_ga_volatile_hsap': r'sevoflurane|isoflurane|desflurane|anesthe|anaesthe',
 'S5_ga_propofol_hsap': r'propofol',
}
WRONGPREP = re.compile(r'\b(oocyte|HEK|heterologous|cell line|PC12|in silico|docking|molecular dynamics|'
                       r'crystal structure|review|meta-analysis|systematic review)\b', re.I)

def build(rid):
    sp = ROWSP[rid]
    out = []
    for cid, cq in CLASS.items():
        out.append((cid, 'CLASS_FIRST/MOLECULE_SYSTEM_FIRST', "%s AND %s AND %s" % (SPECIES[sp], STATE[rid], cq)))
        out.append((cid, 'NEGATIVE_RESULT_SEARCH', "%s AND %s AND %s AND %s" % (SPECIES[sp], STATE[rid], cq, NEG)))
        out.append((cid, 'SPECIES_ENDPOINT_FIRST', "%s AND %s AND %s" % (SPECIES[sp], ENDPOINT[rid], cq)))
    return out

def run(rows=None):
    rows = rows or list(STATE)
    hits = collections.defaultdict(lambda: dict(rows=set(), classes=set(), routes=set(), n=0))
    log = []
    nq = 0
    for rid in rows:
        d = DEPTH[ROWSP[rid]]
        for cid, route, q in build(rid):
            nq += 1
            try:
                ids = lit.esearch(q, n=d)
            except Exception as e:
                log.append(dict(row=rid, cls=cid, route=route, error=str(e))); continue
            log.append(dict(row=rid, cls=cid, route=route, depth=d, n=len(ids)))
            for p in ids:
                h = hits[p]; h['rows'].add(rid); h['classes'].add(cid); h['routes'].add(route); h['n'] += 1
        print('  %s done (%d queries so far, %d unique pmids)' % (rid, nq, len(hits)), flush=True)
    new = [p for p in hits if ('PMID:' + p) not in LED]
    print('QUERIES %d | UNIQUE PMIDS %d | NOT IN LEDGER %d' % (nq, len(hits), len(new)), flush=True)

    # Stage 4: batch metadata for new pmids
    meta = {}
    for i in range(0, len(new), 180):
        try: meta.update(lit.esummary(new[i:i+180]))
        except Exception: pass
        if i % 900 == 0: print('   meta %d/%d' % (i, len(new)), flush=True)

    # Stage 3: prefilter ranking
    ranked = []
    for p in new:
        d = meta.get(p)
        if not d: continue
        t = d['title']
        h = hits[p]
        score = 0
        if CAUSAL.search(t): score += 3
        rowmatch = [r for r in h['rows'] if re.search(STATEWORD[r], t, re.I)]
        score += 2 * len(rowmatch)
        if len(h['rows']) > 1: score += 1
        if 'NEGATIVE_RESULT_SEARCH' in h['routes']: score += 1
        if WRONGPREP.search(t): score -= 3
        if any(x.lower().startswith('review') for x in d.get('pubtype', [])): score -= 3
        ranked.append(dict(pmid=p, score=score, year=d['year'], journal=d['journal'], title=t,
                           rows=sorted(h['rows']), classes=sorted(h['classes']),
                           routes=sorted(h['routes']), n_retrievals=h['n'],
                           row_title_match=sorted(rowmatch)))
    ranked.sort(key=lambda x: (-x['score'], -x['n_retrievals']))
    json.dump(ranked, open(os.path.join(HERE, 'pe5_ranked_candidates.json'), 'w'), indent=1)
    json.dump(log, open(os.path.join(HERE, 'pe5_pipeline_log.json'), 'w'), indent=1)
    print('RANKED CANDIDATES: %d ; score>=5: %d ; score>=7: %d'
          % (len(ranked), sum(1 for r in ranked if r['score'] >= 5), sum(1 for r in ranked if r['score'] >= 7)))
    return ranked

if __name__ == '__main__':
    run()
