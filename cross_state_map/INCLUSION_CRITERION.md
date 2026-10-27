# FROZEN INCLUSION CRITERION — reduced-activity states

**Frozen 2026-09-16T12:45:24Z, BEFORE any state was scored and before any mechanism was
entered into the table.** Applied mechanically thereafter. No criterion, threshold, axis
definition, or row in this file was altered after any cell was populated. Changes require a
new versioned file plus an entry in `AMENDMENTS.md`; this file is never edited in place.

---

## 0. What this criterion is for

The table this criterion governs asks, for each reduced-activity state, **which mechanisms that
state acts on**. It does not assume, require, or test that the states share mechanisms. Whether
mechanism classes recur across states is a measured property of the completed table, not a
hypothesis this criterion is built to support.

Consequently this criterion must admit states on grounds that are independent of what mechanisms
they turn out to use. Every clause below is stated in terms of *phenotype and reversibility only*.
No clause references a channel, gene, pathway, drug, or mechanism class.

---

## 1. The scoring unit

The unit of the table is the ordered pair **(state, species)**, never the state alone.

C. elegans dauer and ground-squirrel hibernation are both deep dormancy; they are different rows.
Human NREM N2 and C. elegans lethargus are both the organism's ordinary recurrent sleep; they are
different rows. No cell in the table is ever filled by transferring a finding from one species to
another. (Transfer *is* recordable, but only at evidence grade E-F, which cannot support a positive
claim — see `REPERTOIRE.md` §4.)

---

## 2. Entry criterion

A (state, species) pair is **eligible** iff it satisfies all four of E1–E4.

- **E1 — Reversibility.** Return to the organism's active baseline is documented, either
  spontaneously or under a defined terminating intervention. States from which recovery is not
  documented are excluded regardless of how closely they resemble an included state.

- **E2 — Bounded episode.** The state has an identifiable onset and offset in time, such that an
  animal can be classified as in-state or out-of-state at a given moment by a stated operational
  rule. This excludes chronic or developmental trends that reduce activity without episode
  structure.

- **E3 — Reduced behavioural output relative to the organism's own active baseline.** Documented as
  reduced spontaneous locomotion, reduced responsiveness to a standard stimulus, or elevated arousal
  threshold, by the standard operational definition used in that state's own field.

  *E3 is deliberately behavioural and deliberately the only activity-related gate.* Behaviour is the
  one axis measurable in every organism on the list, from tardigrade to human. Using neural or
  metabolic reduction as an entry gate would prejudge exactly the question the table exists to
  measure, and would exclude REM by fiat. See §4.

- **E4 — Mechanism-attributable.** At least one published intervention — genetic, pharmacological,
  lesion, or environmental — is documented to alter the state's entry, depth, or exit in that
  species. A state satisfying E1–E3 but not E4 is recorded in `WAITLIST.md` and is not scored; it is
  a state the table cannot yet speak about, which is different from a state with no mechanisms.

---

## 3. Exclusion criterion

Excluded even if E1–E4 appear satisfied:

- **X1 — Irreversible or terminal states.** Death, brain death, and states classified as permanent
  in the source literature. Boundary cases (persistent vegetative state, prolonged disorders of
  consciousness) are excluded under E1 and recorded in `WAITLIST.md` with the reason, because their
  inclusion would make the reversibility axis unmeasurable rather than merely hard.

- **X2 — States individuated solely by stimulus absence.** Dark adaptation, sensory deprivation,
  quiescence attributable only to the removal of a driving stimulus. The organism must be doing
  something, not merely not being driven.

- **X3 — Acute pathology without a physiological entry programme.** Post-ictal depression, syncope,
  hypoxic suppression, anaphylaxis. These are reductions in activity that the organism undergoes
  rather than enters. Recorded in `WAITLIST.md`; several are informative contrast cases and may be
  admitted later by amendment as explicitly-labelled controls.

- **X4 — Anaesthetic states not reaching the surgical endpoint**, when scored under the state name
  "strong general anaesthesia". Sedation and anxiolysis are distinct states; if scored later they
  enter as their own rows, not as shallow instances of this one.

---

## 4. The three axes, and why they are never collapsed

Every eligible (state, species) row carries **three independently scored axes**. They are recorded
separately, reported separately, and are never averaged, summed, or reduced to a single "depth".

| axis | what it measures | typical measurement |
|---|---|---|
| `A_beh` | behavioural output reduction vs the organism's own active baseline | spontaneous locomotion, arousal threshold, response latency to a standard stimulus |
| `A_neu` | neural activity reduction vs the organism's own wake baseline | population firing rate, whole-brain Ca²⁺ event rate, EEG band redistribution, evoked-response amplitude |
| `A_met` | whole-organism metabolic rate reduction | O₂ consumption, CO₂ production, calorimetry, ATP turnover |

Each axis is scored as **direction** (`decreased` / `unchanged` / `increased` / `not_measured`),
**magnitude with units where published**, and **evidence grade** (`REPERTOIRE.md` §4).

**This separation is the load-bearing decision in the whole design.** The three axes are routinely
conflated in every field on the list — "reduced activity" is used to mean behavioural quiescence in
sleep research, cortical suppression in anaesthesiology, and metabolic depression in hibernation and
anhydrobiosis. A table that collapses them cannot distinguish a state that suppresses behaviour
without suppressing metabolism from one that does both, which is a distinction the table exists to
draw.

**REM is the deliberate stress case.** It enters under E3 (atonia reduces behavioural output) and is
expected to show `A_beh: decreased` with `A_neu` and `A_met` not decreased. It is included *as the
dissociation case*, not despite being one. If the axes were collapsed, REM would either be excluded
by fiat or would corrupt the ordering. Under this criterion it is the most informative row.

---

## 5. The committed state list

Nine state names, fixed by Rohit 2026-09-16 and not to be changed without amendment. Each is
instantiated as one or more (state, species) rows. **Instantiation is a mapping of the committed
names onto scoreable units; it is not an addition to the list.**

| # | committed state name | species instantiations (rows) |
|---|---|---|
| 1 | nap | human |
| 2 | core sleep | human (NREM N2), mouse (NREM), *C. elegans* (lethargus) |
| 3 | REM sleep | human, mouse |
| 4 | deep sleep | human (NREM N3 / SWS), mouse (SWS) |
| 5 | strong general anaesthesia | human (volatile), human (propofol), mouse (volatile), *C. elegans* (volatile) |
| 6 | starvation quiescence | *C. elegans* (L1 arrest), *C. elegans* (adult starvation-induced sleep) |
| 7 | dauer | *C. elegans* |
| 8 | cryptobiosis | tardigrade (anhydrobiosis), *C. elegans* dauer (anhydrobiosis) |
| 9 | hibernation | ground squirrel (seasonal torpor bout), mouse (daily torpor) |

Total: **19 rows** across 5 species, giving a 19 × 11 = **209-cell** grid.

Two instantiation decisions are recorded here because they are judgement calls, made before scoring:

- **Lethargus is entered as the *C. elegans* instantiation of "core sleep."** It is the organism's
  ordinary recurrent sleep and satisfies E1–E4. It is developmentally timed rather than homeostatic
  on the mammalian pattern, which is a difference the row will record, not a reason to exclude it.
- **Volatile anaesthesia and propofol are separate rows.** Their behavioural endpoint is
  indistinguishable and their molecular action is not. Merging them would destroy the table's
  ability to show that one endpoint is reachable by more than one mechanism suite, which is the
  single most likely useful output of the anaesthesia rows.

Candidate extensions, **not committed and not to be scored** unless added by amendment: *Drosophila*
sleep, ketamine dissociative anaesthesia, *C. elegans* stress-induced sleep and satiety quiescence,
*Artemia* encystment, hypothermia, sedation short of surgical endpoint.

---

## 6. Contamination disclosure

Recorded here, before population, not discovered afterwards.

The author of this criterion had prior exposure, within the same working period and via earlier
project notes, to:

- the AnestheticSimulator / WCM line, whose head result frames anaesthetic action as a single
  per-cell lever `r = P_Na/P_K` set by NALCN against K2P;
- the frozen anaesthetic target list from the 2026-09-10 dauer gate (`gas-1`; `unc-64`/`unc-13`/
  `unc-31`; `unc-79`/`unc-80`/`nca-1`/`nca-2`; `twk-40`; `unc-49`);
- a hypothesis, generated by the author earlier in the same working period and **explicitly rejected by
  Rohit as a misreading of his proposal**, that reduced-activity states converge on a shared leak-
  ratio effector.

**Consequence.** The mechanism classes in `REPERTOIRE.md` — in particular classes 1 (cation leak)
and 2 (K⁺ conductance) — were written by an author primed toward a leak-ratio account. The class
list is stated in state-independent physical terms and contains no term that can be tuned toward any
particular state's positives, but the *choice to resolve membrane conductance into three separate
classes* while, for example, leaving transcriptional reprogramming as a single class, reflects that
priming and is not a neutral partition of mechanism space.

**Mitigation, committed here:** the completed table must be re-scored once under a coarsened
partition that merges classes 1–4 into a single "membrane conductance" class, and the qualitative
conclusions reported under both partitions. If any conclusion holds only under the fine partition,
it is reported as partition-dependent.

This is a real limitation of the design, not a formality.

---

## 7. Amendment rule

This file is frozen by SHA-256 in `SHA256SUMS.txt`. Any change to a criterion, axis, row, or
exclusion after scoring begins requires: a new file `INCLUSION_CRITERION_v2.md`, an entry in
`AMENDMENTS.md` stating what changed and what had already been scored at the time, and a re-score of
every cell whose value could have been affected. Amendments made after seeing a result must say so
in that entry.
