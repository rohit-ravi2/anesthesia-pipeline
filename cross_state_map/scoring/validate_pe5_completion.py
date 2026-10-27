"""PE-5 completion validator. Exit 0 iff all three gates pass for all ten scored rows.

GATE A — route completeness.  Every row must have all five routes executed to COMPLETE (or
         BLOCKED_EXTERNAL with a named unavailable resource). CITATION_CHAIN counts only if
         pe5_citation_chain.json records status COMPLETE for that row.
GATE B — cell disposition.  All 12 cells of every row carry a terminal disposition. PENDING is not
         terminal. NOT_TESTED_AFTER_FULL_SEARCH is terminal only if the row passes Gate C, because
         a null from a battery with unmeasured recall is uninterpretable.
GATE C — retrieval adequacy.  Per-row internal recall >= 0.90 under the production protocol, or
         every miss individually explained in pe5_miss_explanations.json.

The validator reads state from disk only. It never recomputes or repairs.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ROUTES = ['CLASS_FIRST', 'MOLECULE_SYSTEM_FIRST', 'CITATION_CHAIN',
          'NEGATIVE_RESULT_SEARCH', 'SPECIES_ENDPOINT_FIRST']
TERMINAL = {'POSITIVE', 'NEGATIVE', 'SUGGESTED', 'NOT_TESTED_AFTER_FULL_SEARCH'}


def load(p, default=None):
    f = os.path.join(HERE, p)
    return json.load(open(f)) if os.path.exists(f) else default


def main():
    fail = []
    exe = load('PE5_EXECUTION_LEDGER.json', {}).get('rows', {})
    cells = load('PE5_CELL_LEDGER.json', {}).get('cells', {})
    chain = load('pe5_citation_chain.json', {})
    rec = load('PE5_RECOVERY_SUMMARY.json', {})
    rows = sorted(r for r in exe)

    # 12 rows since the hibernation extension (2026-09-21); was 10 at PE-5 completion
    if len(rows) != 12:
        fail.append('GATE_A: execution ledger has %d rows, expected 12' % len(rows))

    # ---- Gate C first: its verdict feeds Gate B ----
    gate_c = {}
    for rid in rows:
        r = rec.get(rid)
        if not r:
            gate_c[rid] = False
            fail.append('GATE_C %s: no recovery measurement on disk' % rid)
            continue
        gate_c[rid] = bool(r.get('gate_c_pass'))
        if not gate_c[rid]:
            fail.append('GATE_C %s: recall %s, unexplained misses %s'
                        % (rid, r.get('recall'), r.get('missed_unexplained')))

    # ---- Gate A ----
    for rid in rows:
        for rt in ROUTES:
            st = exe[rid].get(rt)
            if st == 'BLOCKED_EXTERNAL':
                continue
            if st != 'COMPLETE':
                fail.append('GATE_A %s/%s: %s' % (rid, rt, st))
        if chain.get(rid, {}).get('status') != 'COMPLETE':
            fail.append('GATE_A %s/CITATION_CHAIN: no systematic chain record on disk' % rid)

    # ---- Gate B ----
    for rid in rows:
        got = [k for k in cells if k.startswith(rid + '|')]
        if len(got) != 12:
            fail.append('GATE_B %s: %d cells in ledger, expected 12' % (rid, len(got)))
        for k in got:
            d = cells[k]['final_disposition']
            if d not in TERMINAL:
                fail.append('GATE_B %s: disposition %s' % (k, d))
            elif d == 'NOT_TESTED_AFTER_FULL_SEARCH' and not gate_c.get(rid):
                fail.append('GATE_B %s: null asserted but row fails Gate C '
                            '(null is uninterpretable)' % k)

    # ---- report ----
    print('PE-5 COMPLETION VALIDATOR')
    print('rows=%d  cells_in_ledger=%d  gate_c_passing_rows=%d/%d'
          % (len(rows), len(cells), sum(gate_c.values()), len(rows)))
    if fail:
        print('\nFAILURES (%d):' % len(fail))
        for f in fail[:80]:
            print('  ' + f)
        if len(fail) > 80:
            print('  ... %d more' % (len(fail) - 80))
        return 1
    print('\nALL GATES PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
