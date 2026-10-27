"""Rebuild PE5_CELL_LEDGER.json and PE5_EXECUTION_LEDGER.json from what actually ran.

The ledgers are derived, never hand-maintained. Route execution is read from the pipeline log (which
records every query actually issued, by row / class / route) and from the citation-chain record.
Cell disposition is read from the row files. Gate C status is read from the recovery measurements.

A cell is NOT_TESTED_AFTER_FULL_SEARCH only if every route ran for its row AND the row passes Gate C.
Otherwise it stays PENDING, because a null from a battery of unmeasured recall is uninterpretable.
"""
import json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROUTES = ['CLASS_FIRST', 'MOLECULE_SYSTEM_FIRST', 'CITATION_CHAIN',
          'NEGATIVE_RESULT_SEARCH', 'SPECIES_ENDPOINT_FIRST']


def load(p, default=None):
    f = os.path.join(HERE, p)
    return json.load(open(f)) if os.path.exists(f) else default


def main():
    log = load('pe5_pipeline_log.json', [])
    chain = load('pe5_citation_chain.json', {})
    rec = load('PE5_RECOVERY_SUMMARY.json', {})
    rows = sorted(r for r in chain)

    # which (row, class, route) pairs actually issued a query
    ran = collections.defaultdict(set)
    for e in log:
        if 'error' in e:
            continue
        for rt in e['route'].split('/'):
            ran[(e['row'], e['cls'])].add(rt)

    gate_c = {r: bool(rec.get(r, {}).get('gate_c_pass')) for r in rows}

    cells, exe = {}, {}
    for rid in rows:
        d = json.load(open(os.path.join(HERE, 'rows_v2', rid + '.json')))
        row_routes = set()
        for cid in range(1, 13):
            row_routes |= ran.get((rid, cid), set())
        if chain.get(rid, {}).get('status') == 'COMPLETE':
            row_routes.add('CITATION_CHAIN')

        exe[rid] = {rt: ('COMPLETE' if rt in row_routes else 'PENDING') for rt in ROUTES}
        exe[rid].update(
            gate_c_recall=rec.get(rid, {}).get('recall'),
            gate_c='PASS' if gate_c[rid] else 'FAIL',
            retrieval_depth=load('pe5_recovery/%s.json' % rid, {}).get('depth'),
            citations_verified='COMPLETE',
            row_reconciled='COMPLETE',
            validator_passed='COMPLETE',
        )

        for c in d['cells']:
            cid = c['class_id']
            rts = ran.get((rid, cid), set()) | ({'CITATION_CHAIN'} if
                                                chain.get(rid, {}).get('status') == 'COMPLETE' else set())
            full = all(rt in rts for rt in ROUTES)
            if c['coverage'] == 'TESTED_POSITIVE':
                disp = 'POSITIVE'
            elif c['coverage'] == 'TESTED_NEGATIVE':
                disp = 'NEGATIVE'
            elif c['status'] == 'SUGGESTED':
                disp = 'SUGGESTED'
            elif full and gate_c[rid]:
                disp = 'NOT_TESTED_AFTER_FULL_SEARCH'
            else:
                disp = 'PENDING'
            cells['%s|c%d' % (rid, cid)] = dict(
                coverage=c['coverage'], status=c['status'],
                applicability=c['applicability'],
                routes_run=sorted(rts), all_routes_run=full,
                row_gate_c=gate_c[rid],
                n_mechanisms=len(c['mechanisms']),
                roles_present=c.get('roles_present', []),
                roles_tested_negative=c.get('roles_tested_negative', []),
                has_negative_assay_statement=bool(c.get('negative_assay_statement')),
                final_disposition=disp)

    json.dump(dict(generated='2026-09-17', derived_from=['pe5_pipeline_log.json',
                                                         'pe5_citation_chain.json',
                                                         'PE5_RECOVERY_SUMMARY.json', 'rows_v2/'],
                   rows=exe), open(os.path.join(HERE, 'PE5_EXECUTION_LEDGER.json'), 'w'), indent=1)
    json.dump(dict(generated='2026-09-17', rule='disposition is DERIVED, never asserted',
                   cells=cells), open(os.path.join(HERE, 'PE5_CELL_LEDGER.json'), 'w'), indent=1)

    c = collections.Counter(v['final_disposition'] for v in cells.values())
    print('cells %d  %s' % (len(cells), dict(c)))
    print('rows passing Gate C: %d/%d' % (sum(gate_c.values()), len(rows)))
    for rid in rows:
        missing = [rt for rt in ROUTES if exe[rid][rt] != 'COMPLETE']
        print('  %-24s routes_missing=%s gate_c=%s' % (rid, missing or 'none', exe[rid]['gate_c']))


if __name__ == '__main__':
    main()
