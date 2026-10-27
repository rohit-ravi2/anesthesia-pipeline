# Addendum — hibernation scored, coarsening run, half the headline broken

**Date:** 2026-09-21. Amends `PE5_FINAL_REPORT.md`, which stays as frozen at 10 rows.
`validate_v2.py` exit 0 · `validate_pe5_completion.py` exit 0 (now 12 rows / 144 cells) ·
measured internal retrieval recall **1.00, 120/120** · ledger **162 verified PMIDs, 0 unresolved**.

---

## 1. Why hibernation was scored

`PE5_FINAL_REPORT.md` §21 named it: *"hibernation is exactly the state where an endogenous system
does something anaesthesia-like on purpose"*, and §22 ranked it the second-highest debt, ahead of
everything except the coarsening. It was scored to try to break the headline. **It broke half of it.**

## 2. The result

| `state_production` | rows | PRODUCES | ENTRY | MAINTAINS | PROTECTS | BUILDS | **EXIT** |
|---|---|---|---|---|---|---|---|
| ENDOGENOUS | **7** | **17** | 20 | 17 | 4 | 5 | **2** |
| PHYSICALLY_IMPOSED | 1 | 0 | 2 | 0 | 2 | 1 | 0 |
| EXOGENOUS_AGENT | 4 | **0** | 18 | 3 | 3 | 0 | **5** |

**The production zero survives and is stronger** — still exactly 0 across four anaesthesia rows,
now against 17 in seven endogenous rows.

**The exit zero is broken.** It was 0 across five endogenous rows. It is 2, and both are in
hibernation/torpor.

## 3. What broke it

**PMID:11893609** — intracerebroventricular prostaglandin E₂ **provokes arousal from an established
hibernation bout** in ground squirrels, with an internal negative control: LPS alone induced neither
fever nor arousal in hibernating animals. Scored `ENABLES_EXIT`.

**PMID:22785425** — aminophylline infused into an already-torpid mouse reverses the hypometabolism,
hypothermia, bradycardia and hypoactivity of torpor; the BBB-impermeant antagonist 8-SPT works
intracerebroventricularly and not subcutaneously. Scored `CONTROLS_ENTRY` + `MAINTAINS_STATE` +
`ENABLES_EXIT`.

The second one is scored `ENABLES_EXIT` for **exact consistency** with `S5_ga_volatile_hsap` c6,
where caffeine — also central adenosine antagonism, also delivered during the maintained state —
was scored the same way. Scoring identical pharmacology differently in two rows would be
indefensible, and doing so would have preserved the zero.

## 4. The claim that replaces it, and it is better

The exit literature is absent from all five sleep and worm-arrest rows and present in both
hibernation rows. The difference between those groups is not production mode — all seven are
`ENDOGENOUS`. It is **how expensive and how puzzling exit is**:

> Interbout arousals consume **60–80% of a ground squirrel's entire winter energy budget**, and
> PMID:11893609 states plainly that "their functional significance is unknown and disputed."

So the refined statement is sharper than the one it replaces:

> **Exit is studied where exit is costly. Production is studied where production is not already
> explained by the intervention.** Anaesthesia has an exit literature because emergence is a
> clinical problem; hibernation has one because arousal is an energetic problem; sleep has none
> because waking up is taken for granted. Nothing produces the anaesthetised state because the drug
> already answers "what produces it?".

This keeps the original thesis — the shape of the literature follows the shape of the question —
and now has a **natural experiment inside it**: two groups matched on production mode, differing in
whether exit is expensive, and differing in exactly the predicted way.

## 5. A convergence that was not looked for

Two states, two sufficiency tests, both producing a partial state that failed on the defining
criterion:

| state | manipulation | produced | failed to produce |
|---|---|---|---|
| mouse daily torpor | central A1 agonist CHA (PMID:28378088) | profound hypothermia | **not torpor** — different Tb kinetics, heart-rate trajectory, shivering, arrhythmia, recovery rate, and transcriptional signature (Txnip vs c-Fos/Egr-1) |
| mouse volatile anaesthesia | chemogenetic reactivation of anaesthesia-activated ensembles (PMID:41573848) | immobility, discoordination, anti-nociception, raised anaesthetic sensitivity | **not loss of consciousness** — righting reflex preserved |

Independent literatures, independent methods, same structure: **the components of a reduced-activity
state can be produced separately, and producing some of them does not assemble the state.** Neither
paper cites the other.

## 6. Other hibernation findings

- **PMID:40593766** — ventrolateral-medulla catecholaminergic neurons: inhibition impairs torpor,
  activation drives it, and heart-rate decline *precedes* body-temperature decline, matching natural
  torpor. Necessity and sufficiency in one paper. `PRODUCES_STATE` + `CONTROLS_ENTRY`.
- **PMID:2762331** — septal vasopressin infusion *prevents* hibernation in European hamster, matching
  the seasonal disappearance of endogenous septal vasopressin. `CONTROLS_ENTRY`, opposing.
- **PMID:41280034** (preprint, E-C) — preoptic activation elicits a torpor-like hypometabolic state.
  Same region as this table's VLPO galanin sleep entries; recorded at `SAME_PATHWAY_MODULE` because
  neither paper resolves whether the same subpopulation does both.
- **PMID:34739575** — CO₂ chemosensitivity is blunted on entrance and elevated on arousal, a
  significant hysteresis at matched body temperature. Observational, graded E-D, recorded because
  entrance and arousal differ at the same body temperature.

## 7. Coverage, and a gap that deepens

Hibernation rows are thin: 3/12 (daily) and 2/12 (seasonal). That is not under-searching — both pass
Gate C at recall 1.00. Both are `NOT_TESTED` across the entire merged membrane-excitability block.

**So the single most confident claim in the dormancy literature — that these states reduce neural
excitability — is unexamined at the mechanism level in dauer, cryptobiosis AND both hibernation
rows.** That is pre-registered prediction P2, now confirmed on four deep states instead of two.

## 8. The coarsening debt is discharged

`COARSENING_1_4.md`. Classes 1–4 merged into one excitability class and every class-dependent
statement re-derived.

- **Unchanged:** every role count; the production/exit asymmetry (roles are orthogonal to classes
  by construction, verified not assumed); every `overlap_resolution`, because resolution is declared
  per molecule pair and never inferred from a class label; P2; the discipline-tracking pattern.
- **Changed:** per-row coverage denominators only — 72/144 fine becomes 60/108 coarse, collapsing 17
  fine positives into 5. Any statement of the form "positive in N classes" was always
  partition-dependent.
- **No conclusion in the final report is reversed.**

The honest gloss: the class partition was carrying less weight than the contamination disclosure
feared, because the load-bearing claims were deliberately placed on the role axis and on per-pair
molecular resolution rather than on class counts.

**What it does not license:** it tests one partition choice, the one the criterion named. The other
eight boundaries are untested, and inter-rater reliability on role assignment remains unmeasured and
is now the most serious open methodological question in the project.

## 9. Status of the debts listed in `PE5_FINAL_REPORT.md` §22

| # | debt | status |
|---|---|---|
| 1 | class 1–4 coarsening | **DONE** — `COARSENING_1_4.md`, nothing reversed |
| 2 | hibernation/torpor row | **DONE** — both rows scored; broke the exit zero |
| 3 | inter-rater reliability on roles | **OPEN — now the top methodological debt** |
| 4 | `A_therm` axis amendment | OPEN, and hibernation strengthens it further |
| 5 | stress-induced-sleep row | OPEN, three papers waiting |
| 6 | `PERMISSIVE_BACKGROUND` | OPEN, correctly blocked on its named trigger |
| 7 | replace the preprint at `S6_starv_L1_cele` c9 | OPEN; a second preprint now at `S9_hib_daily_mmus` c7 |
| 8 | remaining committed rows | 12 of 19 scored |
