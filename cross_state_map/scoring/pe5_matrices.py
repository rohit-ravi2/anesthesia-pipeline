"""PE-5 final analysis matrices A-E, derived from the row files only.

A  coverage        state x class, disposition
B  role            state x class, roles present
C  polarity        state x class, mechanism polarity
D  overlap         molecule-level correspondences between rows, at declared resolution
E  evidence grade  state x class, strongest grade

Every matrix is an INCIDENCE map over unequally-searched cells. Prohibition 1 of REPERTOIRE.md
forbids computing any enrichment claim from it, and nothing here does.
"""
import json, os, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = ['S2_core_cele', 'S6_starv_L1_cele', 'S7_dauer_cele', 'S8_crypto_cele',
        'S3_rem_mmus', 'S4_deep_mmus',
        'S5_ga_volatile_cele', 'S5_ga_volatile_mmus', 'S5_ga_volatile_hsap', 'S5_ga_propofol_hsap']
SHORT = {'S2_core_cele': 'worm lethargus', 'S6_starv_L1_cele': 'worm L1 arrest',
         'S7_dauer_cele': 'worm dauer', 'S8_crypto_cele': 'worm cryptobiosis',
         'S3_rem_mmus': 'mouse REM', 'S4_deep_mmus': 'mouse NREM',
         'S5_ga_volatile_cele': 'worm volatile', 'S5_ga_volatile_mmus': 'mouse volatile',
         'S5_ga_volatile_hsap': 'human volatile', 'S5_ga_propofol_hsap': 'human propofol'}
RSYM = {'PRODUCES_STATE': 'P', 'CONTROLS_ENTRY': 'E', 'MAINTAINS_STATE': 'M',
        'PROTECTS_THROUGH_STATE': 'T', 'BUILDS_MACHINERY': 'B', 'ENABLES_EXIT': 'X'}
PSYM = {'PROMOTES_STATE': '+', 'OPPOSES_STATE': '-', 'STRUCTURE_ONLY': 's',
        'CONTEXT_DEPENDENT': '~', 'UNDETERMINED': '?', 'NO_ESTABLISHED_EFFECT': '0'}

D = {r: json.load(open(os.path.join(HERE, 'rows_v2', r + '.json'))) for r in ROWS}
CELL = {(r, c['class_id']): c for r in ROWS for c in D[r]['cells']}
OUT = []


def w(s=''):
    OUT.append(s)


def table(title, fn, legend):
    w('## ' + title)
    w()
    w('| state | ' + ' | '.join('c%d' % i for i in range(1, 13)) + ' |')
    w('|' + '---|' * 13)
    for r in ROWS:
        w('| %-18s | %s |' % (SHORT[r], ' | '.join(fn(r, i) for i in range(1, 13))))
    w()
    w(legend)
    w()


def a(r, i):
    c = CELL[(r, i)]
    if c['applicability'] == 'NOT_APPLICABLE':
        return 'n/a'
    return {'TESTED_POSITIVE': '**+**', 'TESTED_NEGATIVE': '**–**',
            'NOT_TESTED': '.'}.get(c['coverage'], c['coverage'])


def b(r, i):
    c = CELL[(r, i)]
    s = ''.join(RSYM.get(x, '?') for x in c.get('roles_present', []))
    n = ''.join(RSYM.get(x, '?') for x in c.get('roles_tested_negative', []))
    return (s + ('(' + n + ')' if n else '')) or '.'


def p(r, i):
    c = CELL[(r, i)]
    s = ''.join(sorted({PSYM.get(m.get('state_polarity'), '?') for m in c['mechanisms']}))
    return s or '.'


def e(r, i):
    return CELL[(r, i)].get('strongest_grade') or '.'


w('# PE-5 final matrices')
w()
w('Generated from `rows_v2/*.json` only. Ten scored (state, species) rows x twelve frozen mechanism')
w('classes = 120 cells.')
w()
w('**Read this first.** These are INCIDENCE maps over cells that have been searched to a measured')
w('but unequal degree. A blank means the standardized battery found no qualifying evidence at the')
w('recall recorded for that row; it does NOT mean the mechanism is absent. Prohibition 1 of')
w('`REPERTOIRE.md` forbids computing any enrichment claim from these tables, and none is computed.')
w()

table('Matrix A - coverage', a,
      '`+` tested positive - `–` tested negative - `.` not tested - `n/a` class not applicable to this state')
table('Matrix B - causal role', b,
      'P produces - E controls entry - M maintains - T protects through - B builds machinery - '
      'X enables exit. Roles in parentheses were TESTED AND FOUND ABSENT.')
table('Matrix C - state polarity', p,
      '`+` promotes - `–` opposes - `s` structure only - `~` context dependent - `?` undetermined - '
      '`0` measured null. Several cells carry more than one symbol because a class can hold mechanisms '
      'of opposite sign.')
table('Matrix E - strongest evidence grade', e, 'E-A strongest through E-F weakest.')

# ---------------------------------------------------------------- Matrix D, overlaps
w('## Matrix D - declared cross-row mechanism correspondences')
w()
w('Every `overlap_resolution` recorded on any mechanism, at the resolution the scorer declared.')
w('Resolution is recorded PER PAIR and never inferred from a shared class label.')
w()
w('| resolution | row / class | partner | molecule |')
w('|---|---|---|---|')
order = ['EXACT_MOLECULE', 'ORTHOLOGOUS_MOLECULE', 'SAME_COMPLEX', 'SAME_PATHWAY_MODULE',
         'SAME_PHYSICAL_CLASS', 'NO_ESTABLISHED_OVERLAP']
ov = []
for (r, i), c in CELL.items():
    for m in c['mechanisms']:
        o = m.get('overlap_resolution')
        if not o:
            continue
        # Earlier rounds wrote this field as a free-text string; later rounds write a dict with
        # level/partner/justification. Both are read, and the free-text ones are labelled as such
        # rather than silently parsed into a level they never declared.
        if isinstance(o, str):
            lev = next((k for k in order if k in o), 'UNSTRUCTURED_NOTE')
            partner, note = '(free text)', o
        else:
            lev, partner, note = o['level'], o.get('partner', ''), ''
        ov.append((order.index(lev) if lev in order else 9, lev,
                   '%s c%d' % (SHORT[r], i), partner or note[:70],
                   (m['molecules'][0]['name'] if m.get('molecules') else '')))
for _, lev, cell, partner, mol in sorted(ov):
    w('| %s | %s | %s | %s |' % (lev, cell, partner, mol[:62]))
w()

lc = collections.Counter(x[1] for x in ov)
w('Counts: ' + ' - '.join('%s %d' % (k, lc[k]) for k in order if lc[k]))
w()

# ---------------------------------------------------------------- totals
w('## Totals')
w()
tot = collections.Counter(c['coverage'] for c in CELL.values())
rol = collections.Counter()
neg = collections.Counter()
pol = collections.Counter()
grd = collections.Counter()
srcs = set()
nmech = 0
for c in CELL.values():
    for x in c.get('roles_present', []):
        rol[x] += 1
    for x in c.get('roles_tested_negative', []):
        neg[x] += 1
    for m in c['mechanisms']:
        nmech += 1
        pol[m.get('state_polarity')] += 1
        srcs.update(m.get('citation_ids', []))
        for pp in m['perturbations']:
            srcs.update(pp.get('citation_ids', []))
w('- cells: 120 across 10 rows x 12 classes')
w('- coverage: ' + ', '.join('%s %d' % (k, v) for k, v in sorted(tot.items())))
w('- mechanisms recorded: %d' % nmech)
w('- distinct load-bearing sources: %d' % len(srcs))
w('- cell-level roles present: ' + ', '.join('%s %d' % (k, v) for k, v in rol.most_common()))
w('- cell-level roles TESTED NEGATIVE: ' + (', '.join('%s %d' % (k, v) for k, v in neg.most_common())
                                            or 'none'))
w('- mechanism polarity: ' + ', '.join('%s %d' % (k, v) for k, v in pol.most_common()))
w()

# ---------------------------------------------------------------- per-row
w('## Per-row summary')
w()
w('| row | populated | positive | negative | roles present | strongest |')
w('|---|---|---|---|---|---|')
for r in ROWS:
    s = D[r]['row_summary']
    rr = collections.Counter()
    for c in D[r]['cells']:
        for x in c.get('roles_present', []):
            rr[x] += 1
    w('| %s | %d/12 | %d | %d | %s | %s |'
      % (SHORT[r], s['coverage_denominator'], s['n_positive'], s['n_negative'],
         ' '.join('%s%d' % (RSYM[k], v) for k, v in sorted(rr.items())) or '-',
         min((c.get('strongest_grade') or 'E-Z') for c in D[r]['cells'])))
w()

open(os.path.join(HERE, '..', 'PE5_MATRICES.md'), 'w').write('\n'.join(OUT) + '\n')
print('\n'.join(OUT[:120]))
print('\n[written: PE5_MATRICES.md, %d lines]' % len(OUT))
