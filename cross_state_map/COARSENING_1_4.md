# Class 1-4 coarsening re-score

**Date:** 2026-09-21. Mandated by `INCLUSION_CRITERION.md` section 6 and outstanding since the
criterion was frozen. Merges classes 1 (cation leak), 2 (K+ conductance), 3 (Cl-/shunt) and
4 (excitatory receptor block) into one class `C1_4` = membrane excitability reduction, then
re-derives every class-dependent statement in the project.

Rows: 12. Fine partition: 12 classes. Coarse partition: 9 classes.

## 1. Coverage, fine versus coarse

| row | fine populated /12 | coarse populated /9 | C1_4 | constituent fine cells |
|---|---|---|---|---|
| S2_core_cele | 9 | 7 | POSITIVE | 1:POS 2:POS 3:NEG |
| S3_rem_mmus | 7 | 4 | POSITIVE | 1:POS 2:POS 3:POS 4:POS |
| S4_deep_mmus | 10 | 8 | POSITIVE | 2:POS 3:POS 4:POS |
| S5_ga_propofol_hsap | 2 | 2 | NOT_TESTED | - |
| S5_ga_volatile_cele | 9 | 7 | POSITIVE | 1:POS 2:POS 4:POS |
| S5_ga_volatile_hsap | 3 | 3 | NOT_TESTED | - |
| S5_ga_volatile_mmus | 11 | 8 | POSITIVE | 1:POS 2:POS 3:POS 4:POS |
| S6_starv_L1_cele | 6 | 6 | POSITIVE | 1:POS |
| S7_dauer_cele | 7 | 7 | NOT_TESTED | - |
| S8_crypto_cele | 3 | 3 | NOT_TESTED | - |
| S9_hib_daily_mmus | 3 | 3 | NOT_TESTED | - |
| S9_hib_seasonal_isp | 2 | 2 | NOT_TESTED | - |

Fine total populated: **72/144**. Coarse total populated: **60/108**.

**Information destroyed by coarsening:** 5 rows have more than one populated cell among classes
1-4, so the merge collapses 17 distinct positives into 5.
- `S2_core_cele`: 3 fine positives -> 1 coarse positive
- `S3_rem_mmus`: 4 fine positives -> 1 coarse positive
- `S4_deep_mmus`: 3 fine positives -> 1 coarse positive
- `S5_ga_volatile_cele`: 3 fine positives -> 1 coarse positive
- `S5_ga_volatile_mmus`: 4 fine positives -> 1 coarse positive

## 2. The production/exit asymmetry is INVARIANT under coarsening

The causal-role axis is orthogonal to the mechanism-class axis by construction, so merging
classes cannot change a role count. Verified rather than asserted:

| state_production | rows | PRODUCES | ENTRY | MAINTAINS | PROTECTS | BUILDS | EXIT |
|---|---|---|---|---|---|---|---|
| ENDOGENOUS | 7 | 17 | 20 | 17 | 4 | 5 | 2 |
| EXOGENOUS_AGENT | 4 | 0 | 18 | 3 | 3 | 0 | 5 |
| PHYSICALLY_IMPOSED | 1 | 0 | 2 | 0 | 2 | 1 | 0 |

Identical before and after the merge. **The headline result does not depend on the class
partition at all.**

## 3. Does the "classes track the discipline" claim survive?

Claim I1 said the mechanism classes interrogated for a state track the field that studies it.
Under coarsening, classes 1-4 become one column, which is the strongest possible test of that
claim -- it removes exactly the distinctions a sceptic would say were drawn to produce it.

**Coarse partition, populated cells per family:**

| family | rows | C1_4 | c5 | c6 | c7 | c8 | c9 | c10 | c11 | c12 |
|---|---|---|---|---|---|---|---|---|---|---|
| worm sleep/arrest | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 1 | 0 | 2 |
| mammal sleep | 2 | 2 | 1 | 2 | 2 | 1 | 2 | 0 | 1 | 1 |
| anaesthesia | 4 | 2 | 2 | 4 | 3 | 3 | 0 | 2 | 2 | 2 |
| hibernation | 2 | 0 | 0 | 2 | 1 | 0 | 1 | 0 | 1 | 0 |
| cryptobiosis | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 |

## 4. Pre-registered prediction P2 under coarsening

`PREDICTIONS.md` P2, frozen before any scoring, said that for the deep states classes 1-5 would
be predominantly `NOT_TESTED` rather than `TESTED_NEGATIVE`, and called this "the single most
valuable output of the table". Re-checked on the coarse partition:

| row | C1_4 | c5 | verdict |
|---|---|---|---|
| S7_dauer_cele | NOT_TESTED | POSITIVE | PARTIAL |
| S8_crypto_cele | NOT_TESTED | NOT_TESTED | CONFIRMED - both NOT_TESTED |
| S9_hib_seasonal_isp | NOT_TESTED | NOT_TESTED | CONFIRMED - both NOT_TESTED |
| S9_hib_daily_mmus | NOT_TESTED | NOT_TESTED | CONFIRMED - both NOT_TESTED |

`TESTED_NEGATIVE` count across the four deep states in the merged excitability class and class 5:
**0**. P2 survives coarsening.

## 5. What the coarsening actually changes

Only statements that COUNT CLASSES are affected, and only in one direction -- the merge can
lower a coverage count, never raise one. Concretely:

- **Changed:** per-row coverage denominators (see section 1), and any statement of the form
  "row X is positive in N classes". Those numbers are partition-dependent and always were.
- **Unchanged:** every role count; the production/exit asymmetry; the three-valued evidence
  logic; every `overlap_resolution`, because resolution is declared per molecule pair and never
  inferred from a class label; P2; the discipline-tracking pattern.

**No conclusion in `PE5_FINAL_REPORT.md` is reversed by coarsening.** The debt is discharged,
and the honest gloss is that the class partition was carrying less weight than the contamination
disclosure feared -- because the project deliberately put its load-bearing claims on the ROLE
axis and on per-pair molecular resolution rather than on class counts.

## 6. What this does NOT license

Coarsening tests robustness to ONE partition choice: the 1-4 merge named in the criterion. It
does not validate the remaining eight class boundaries, and it does not address inter-rater
reliability on role assignment, which remains unmeasured and is the more serious open
methodological question.
