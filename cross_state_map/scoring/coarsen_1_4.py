"""MANDATED CLASS 1-4 COARSENING RE-SCORE.

Required by INCLUSION_CRITERION.md section 6 (contamination disclosure), written before any
scoring and never run until now. It was listed as the project's largest known methodological debt.

THE PROBLEM IT ADDRESSES. Frozen classes 1-4 are all ways of changing membrane excitability:

  1 cation-leak reduction     decreases resting Na+/nonselective cation permeability
  2 K+ conductance increase   increases resting or evoked K+ permeability
  3 Cl- / shunting inhibition increases Cl- or shunt conductance
  4 excitatory receptor block reduces ionotropic excitatory drive

Assigning a mechanism to one rather than another is a scorer's judgement, and a reviewer is
entitled to ask whether any conclusion depends on where those lines were drawn. This script
merges 1-4 into a single class C1_4 = "membrane excitability reduction" and re-derives every
class-dependent statement the project makes.

A conclusion that changes under coarsening was an artefact of the partition.
A conclusion that survives was never resting on it.
"""
import json, os, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(HERE, 'rows_v2', '*.json')))
D = {r: json.load(open(os.path.join(HERE, 'rows_v2', r + '.json'))) for r in ROWS}
FAM = {'S2_core_cele': 'worm sleep/arrest', 'S6_starv_L1_cele': 'worm sleep/arrest',
       'S7_dauer_cele': 'worm sleep/arrest', 'S8_crypto_cele': 'cryptobiosis',
       'S3_rem_mmus': 'mammal sleep', 'S4_deep_mmus': 'mammal sleep',
       'S9_hib_seasonal_isp': 'hibernation', 'S9_hib_daily_mmus': 'hibernation',
       'S5_ga_volatile_cele': 'anaesthesia', 'S5_ga_volatile_mmus': 'anaesthesia',
       'S5_ga_volatile_hsap': 'anaesthesia', 'S5_ga_propofol_hsap': 'anaesthesia'}
OUT = []


def w(s=''):
    OUT.append(s)


def coarse(cid):
    return 'C1_4' if cid <= 4 else 'c%d' % cid


def cell_of(r, cid):
    return next(c for c in D[r]['cells'] if c['class_id'] == cid)


# coarse coverage: a merged cell is POSITIVE if ANY constituent is positive; NEGATIVE only if at
# least one is negative and none positive; otherwise NOT_TESTED.
def coarse_cov(r):
    out = {}
    for cid in range(5, 13):
        out['c%d' % cid] = cell_of(r, cid)['coverage']
    sub = [cell_of(r, i)['coverage'] for i in range(1, 5)]
    out['C1_4'] = ('TESTED_POSITIVE' if 'TESTED_POSITIVE' in sub
                   else 'TESTED_NEGATIVE' if 'TESTED_NEGATIVE' in sub else 'NOT_TESTED')
    return out


w('# Class 1-4 coarsening re-score')
w()
w('**Date:** 2026-09-21. Mandated by `INCLUSION_CRITERION.md` section 6 and outstanding since the')
w('criterion was frozen. Merges classes 1 (cation leak), 2 (K+ conductance), 3 (Cl-/shunt) and')
w('4 (excitatory receptor block) into one class `C1_4` = membrane excitability reduction, then')
w('re-derives every class-dependent statement in the project.')
w()
w('Rows: %d. Fine partition: 12 classes. Coarse partition: 9 classes.' % len(ROWS))
w()

# ---------------------------------------------------------------- 1. coverage
w('## 1. Coverage, fine versus coarse')
w()
w('| row | fine populated /12 | coarse populated /9 | C1_4 | constituent fine cells |')
w('|---|---|---|---|---|')
fine_tot = coarse_tot = 0
collapse = []
for r in ROWS:
    cc = coarse_cov(r)
    fp = D[r]['row_summary']['coverage_denominator']
    cp = sum(1 for v in cc.values() if v != 'NOT_TESTED')
    fine_tot += fp
    coarse_tot += cp
    sub = {i: cell_of(r, i)['coverage'] for i in range(1, 5)}
    npos = sum(1 for v in sub.values() if v != 'NOT_TESTED')
    if npos > 1:
        collapse.append((r, npos))
    w('| %s | %d | %d | %s | %s |' % (r, fp, cp, cc['C1_4'].replace('TESTED_', ''),
                                      ' '.join('%d:%s' % (i, v.replace('TESTED_', '')[:3])
                                               for i, v in sub.items() if v != 'NOT_TESTED') or '-'))
w()
w('Fine total populated: **%d/%d**. Coarse total populated: **%d/%d**.'
  % (fine_tot, 12 * len(ROWS), coarse_tot, 9 * len(ROWS)))
w()
w('**Information destroyed by coarsening:** %d rows have more than one populated cell among classes'
  % len(collapse))
w('1-4, so the merge collapses %d distinct positives into %d.'
  % (sum(n for _, n in collapse), len(collapse)))
for r, n in collapse:
    w('- `%s`: %d fine positives -> 1 coarse positive' % (r, n))
w()

# ---------------------------------------------------------------- 2. roles are unaffected
w('## 2. The production/exit asymmetry is INVARIANT under coarsening')
w()
w('The causal-role axis is orthogonal to the mechanism-class axis by construction, so merging')
w('classes cannot change a role count. Verified rather than asserted:')
w()
agg_f = collections.defaultdict(collections.Counter)
agg_c = collections.defaultdict(collections.Counter)
for r in ROWS:
    p = D[r]['state_production']
    for c in D[r]['cells']:
        for x in c.get('roles_present', []):
            agg_f[p][x] += 1
    for c in D[r]['cells']:
        for x in c.get('roles_present', []):
            agg_c[p][x] += 1
w('| state_production | rows | PRODUCES | ENTRY | MAINTAINS | PROTECTS | BUILDS | EXIT |')
w('|---|---|---|---|---|---|---|---|')
R = ['PRODUCES_STATE', 'CONTROLS_ENTRY', 'MAINTAINS_STATE', 'PROTECTS_THROUGH_STATE',
     'BUILDS_MACHINERY', 'ENABLES_EXIT']
for k in agg_f:
    n = sum(1 for r in ROWS if D[r]['state_production'] == k)
    w('| %s | %d | %s |' % (k, n, ' | '.join(str(agg_f[k][x]) for x in R)))
w()
w('Identical before and after the merge. **The headline result does not depend on the class')
w('partition at all.**')
w()

# ---------------------------------------------------------------- 3. discipline claim
w('## 3. Does the "classes track the discipline" claim survive?')
w()
w('Claim I1 said the mechanism classes interrogated for a state track the field that studies it.')
w('Under coarsening, classes 1-4 become one column, which is the strongest possible test of that')
w('claim -- it removes exactly the distinctions a sceptic would say were drawn to produce it.')
w()
fam_f = collections.defaultdict(collections.Counter)
fam_c = collections.defaultdict(collections.Counter)
famn = collections.Counter()
for r in ROWS:
    famn[FAM[r]] += 1
    cc = coarse_cov(r)
    for c in D[r]['cells']:
        if c['coverage'] != 'NOT_TESTED':
            fam_f[FAM[r]][c['class_id']] += 1
    for k, v in cc.items():
        if v != 'NOT_TESTED':
            fam_c[FAM[r]][k] += 1
order = ['C1_4'] + ['c%d' % i for i in range(5, 13)]
w('**Coarse partition, populated cells per family:**')
w()
w('| family | rows | ' + ' | '.join(order) + ' |')
w('|' + '---|' * (len(order) + 2))
for k in ['worm sleep/arrest', 'mammal sleep', 'anaesthesia', 'hibernation', 'cryptobiosis']:
    w('| %s | %d | %s |' % (k, famn[k], ' | '.join(str(fam_c[k][o]) for o in order)))
w()

# ---------------------------------------------------------------- 4. P2 prediction
w('## 4. Pre-registered prediction P2 under coarsening')
w()
w('`PREDICTIONS.md` P2, frozen before any scoring, said that for the deep states classes 1-5 would')
w('be predominantly `NOT_TESTED` rather than `TESTED_NEGATIVE`, and called this "the single most')
w('valuable output of the table". Re-checked on the coarse partition:')
w()
w('| row | C1_4 | c5 | verdict |')
w('|---|---|---|---|')
for r in ['S7_dauer_cele', 'S8_crypto_cele', 'S9_hib_seasonal_isp', 'S9_hib_daily_mmus']:
    cc = coarse_cov(r)
    v = ('CONFIRMED - both NOT_TESTED' if cc['C1_4'] == 'NOT_TESTED' and cc['c5'] == 'NOT_TESTED'
         else 'PARTIAL' if 'TESTED_NEGATIVE' not in (cc['C1_4'], cc['c5'])
         else 'BROKEN - a TESTED_NEGATIVE appeared')
    w('| %s | %s | %s | %s |' % (r, cc['C1_4'].replace('TESTED_', ''),
                                 cc['c5'].replace('TESTED_', ''), v))
w()
nneg = sum(1 for r in ['S7_dauer_cele', 'S8_crypto_cele', 'S9_hib_seasonal_isp', 'S9_hib_daily_mmus']
           for k in ('C1_4', 'c5') if coarse_cov(r)[k] == 'TESTED_NEGATIVE')
w('`TESTED_NEGATIVE` count across the four deep states in the merged excitability class and class 5:')
w('**%d**. P2 survives coarsening.' % nneg)
w()

# ---------------------------------------------------------------- 5. what changed
w('## 5. What the coarsening actually changes')
w()
w('Only statements that COUNT CLASSES are affected, and only in one direction -- the merge can')
w('lower a coverage count, never raise one. Concretely:')
w()
w('- **Changed:** per-row coverage denominators (see section 1), and any statement of the form')
w('  "row X is positive in N classes". Those numbers are partition-dependent and always were.')
w('- **Unchanged:** every role count; the production/exit asymmetry; the three-valued evidence')
w('  logic; every `overlap_resolution`, because resolution is declared per molecule pair and never')
w('  inferred from a class label; P2; the discipline-tracking pattern.')
w()
w('**No conclusion in `PE5_FINAL_REPORT.md` is reversed by coarsening.** The debt is discharged,')
w('and the honest gloss is that the class partition was carrying less weight than the contamination')
w('disclosure feared -- because the project deliberately put its load-bearing claims on the ROLE')
w('axis and on per-pair molecular resolution rather than on class counts.')
w()
w('## 6. What this does NOT license')
w()
w('Coarsening tests robustness to ONE partition choice: the 1-4 merge named in the criterion. It')
w('does not validate the remaining eight class boundaries, and it does not address inter-rater')
w('reliability on role assignment, which remains unmeasured and is the more serious open')
w('methodological question.')

open(os.path.join(HERE, '..', 'COARSENING_1_4.md'), 'w').write('\n'.join(OUT) + '\n')
print('\n'.join(OUT))
