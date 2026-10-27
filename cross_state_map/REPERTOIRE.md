# FROZEN REPERTOIRE AND MAPPING RULE — mechanism classes

**Frozen 2026-09-16T12:45:24Z, BEFORE any state was scored.** Companion to
`INCLUSION_CRITERION.md`. Same amendment rule: never edited in place.

---

## 1. What the repertoire is a repertoire *of*

The organism possesses machinery capable of reversibly reducing its own activity. The classes below
partition that machinery **by what it physically does**, not by what kind of molecule implements it
and not by which field described it.

This is the central mapping decision and the reason the table can compare states at all. Anaesthesia
is described in its literature at the drug-target level, dauer at the transcription-factor level,
sleep at the circuit level, hibernation at the endocrine and thermoregulatory level, anhydrobiosis
at the biophysical level. Those are different *descriptions*, not different *kinds of mechanism*, and
a table that inherits each field's preferred level cannot be read across rows. Every entry is
therefore normalised onto the eleven classes below before it is scored.

---

## 2. The eleven classes

| # | class | physical action | representative implementations |
|---|---|---|---|
| 1 | cation-leak reduction | decreases resting Na⁺/nonselective cation permeability | NALCN / `nca-1`, `nca-2`, `unc-79`, `unc-80`, `unc-77`; TRP leak |
| 2 | K⁺ conductance increase | increases resting or evoked K⁺ permeability | K2P (TWK/TREK/TASK), GIRK, BK, Kv, SK |
| 3 | Cl⁻ / shunting inhibition | increases Cl⁻ or shunt conductance | GABA-A, glycine receptors, `unc-49`, glutamate-gated Cl⁻ |
| 4 | excitatory receptor block | reduces ionotropic excitatory drive | NMDA, AMPA/kainate receptor antagonism or modulation |
| 5 | synaptic release machinery | reduces transmitter or peptide release at the terminal | SNARE (`unc-64`, `unc-13`), dense-core release (`unc-31`), presynaptic Ca_v |
| 6 | neuromodulatory / peptidergic drive | a released signalling molecule acts on receptors to impose the state | FLP-11, adenosine→A1, galanin, orexin withdrawal, insulin/IGF signalling |
| 7 | circuit-level switch | a dedicated sleep- or dormancy-active neuronal population drives the state | RIS, ALA, VLPO, hypothalamic torpor-inducing populations |
| 8 | mitochondrial / metabolic | reduces ATP production or shifts metabolic mode | Complex I (`gas-1`), oxidative→anaerobic shift, ATP availability, pump capacity |
| 9 | transcriptional / developmental reprogramming | changes the expressed protein complement of the state | DAF-16/FOXO, DAF-12, HIF, torpor transcriptional programmes |
| 10 | structural / biophysical | alters the physical state of cells or the organism's barriers | trehalose vitrification, intrinsically disordered proteins, cuticle and permeability barriers, desiccation tolerance |
| 11 | thermal / rate effects | changes the temperature at which the system runs, hence all rates | regulated hypothermia, Q₁₀ effects, active cooling |

Classes are physical, not exclusive: a state may act on any number of them, and a single molecular
event may be recorded under two classes if it does two physical things (see §3.2).

---

## 3. Mapping rules

### 3.1 Assignment is by proximal physical effect

A mechanism is assigned to the class describing **what it does to the cell or organism**, never to
the class describing what sort of entity it is.

- A volatile anaesthetic that binds a K2P channel and increases K⁺ conductance is **class 2**, not a
  separate "drug" class.
- A transcription factor is **class 9** only in respect of the reprogramming itself. What the
  reprogramming *produces* is scored under its own class.
- Adenosine acting through A1 receptors to open GIRK channels is **class 6 proximal-to class 2**.

### 3.2 Chains are recorded, not flattened

Many mechanisms are causal chains that cross classes. Every entry records:

- `chain` — the ordered causal sequence as documented, in the source's own terms;
- `proximal_class` — the class of the most membrane- or metabolism-proximal step **that has direct
  evidence in this (state, species)**;
- `upstream_classes` — every earlier step with direct evidence in this (state, species), each with
  `role: upstream`.

A cell (state, species, class) scores **positive** if that class appears in a documented chain
either as `proximal_class` or as a documented-necessary `upstream_class`. The two are always
distinguishable in the record and are reported separately, because "dauer acts on K⁺ conductance"
means something different if the K⁺ change is the proximal effector than if it is three steps
downstream of a transcription factor and inferred.

**Chain steps without direct evidence in this (state, species) are not scored at all.** They are
recorded in the chain as `inferred: true` and contribute nothing to any cell. This is the specific
rule that prevents a well-studied pathway in one state from silently populating cells in another.

### 3.3 No transfer across rows

A mechanism documented in (state X, species A) never scores a cell in (state X, species B) or
(state Y, species A). Cross-species and cross-state inference is recordable only at grade E-F, which
cannot support a positive cell (§4).

### 3.4 No gene identity claims across species

Orthology is recorded at the class level with the ortholog relation named and sourced. The table
never asserts that a worm gene and a mammalian gene are the same gene, and no cell is scored on
orthology alone.

---

## 4. Evidence grades

Committed before scoring. Every cell carries the grade of its **strongest** supporting evidence, and
the full grade list of all supporting evidence.

| grade | definition |
|---|---|
| **E-A** | unbiased forward genetic or chemical screen hit for this state, in this species |
| **E-B** | targeted loss- or gain-of-function alters entry, depth, or exit of this state, in vivo, in this species |
| **E-C** | pharmacological manipulation alters this state, with a named target **and** a reported specificity control |
| **E-D** | direct physiological measurement of the mechanism during this state (recorded conductance, flux, metabolite, or rate change) |
| **E-E** | expression or transcriptomic change during this state, no functional test |
| **E-F** | inference from another state or another species; no direct evidence in this (state, species) |

**A cell whose strongest evidence is E-E or E-F is marked `SUGGESTED` and may not be reported as a
positive.** Suggested cells are carried in the table because they are the highest-value targets for
the follow-up work, not because they are findings.

Pharmacological evidence without a specificity control is **E-F**, not E-C. This demotion is
committed here because it will bite hardest on the anaesthesia and hibernation rows, which is
exactly why it is stated before those rows are scored.

---

## 5. Coverage accounting

Every cell in the 19 × 11 grid takes one of three values, and the third is not a variant of the
second:

- `TESTED_POSITIVE` — an assay capable of detecting this class was applied to this (state, species)
  and detected it.
- `TESTED_NEGATIVE` — an assay capable of detecting this class was applied and did not detect it.
  Requires a citation to the negative result and a statement of what the assay could have detected.
- `NOT_TESTED` — no such assay has been applied. **Absence of evidence. Never reported as absence of
  the mechanism.**

Each row additionally carries a **coverage denominator**: the number of the eleven classes for which
any capable assay has ever been applied to that (state, species). Every count, proportion, or
comparison computed from the table is reported against its coverage denominator, never against 11.

This is the control for the ascertainment problem. Human NREM and *C. elegans* dauer differ in study
volume by orders of magnitude; without denominators, any cross-row count measures publication
history rather than biology. The 2026-09-10 dauer gate failed on precisely this class of confound —
degree-matching controlled for how much a gene had been studied but never for study-in-that-context
— and the fix there is not available here, so the fix used here is to report the denominator rather
than to model it away.

---

## 6. Prohibitions

Binding on every use of this table.

1. **No enrichment claim may be computed from this table.** It is an incidence map with unequal and
   unmodelled ascertainment. Statements of the form "class C is enriched across states" are
   forbidden regardless of what null is proposed.
2. **Literature co-occurrence is never evidence.** A cell is scored from a documented experimental
   result in that (state, species), never from two entities appearing in the same paper, database
   edge, or review.
3. **`NOT_TESTED` is never reported as negative**, in text, figure, or summary statistic.
4. **The three axes are never collapsed** into a single depth score, ordering, or ranking.
5. **No cross-species gene identity claims** (§3.4).
6. **Every citation passes the verification harness** (the earlier
   dauer-gate harness; reimplemented here as `scoring/lit.py`) before its cell is
   scored. Title-and-content verification, not PMID resolution alone. This is mandatory because the
   author's citation reliability is documented as poor on both axes.
7. **The completed table is re-scored under the coarsened partition** merging classes 1–4, per the
   contamination disclosure in `INCLUSION_CRITERION.md` §6, and any conclusion holding under only
   one partition is reported as partition-dependent.

---

## 7. What the completed table is permitted to say

Stated in advance so the output is not retrofitted to whatever the scoring produces.

Permitted:
- the mechanism suite documented for each (state, species), at a common physical level, with grades;
- the three-axis profile of each row, with the axes separate;
- the coverage denominator of each row, and the list of `NOT_TESTED` cells;
- the set of untested cells, as a ranked list of proposed experiments with named assays;
- qualitative statements about which classes recur, **always paired with the denominators**, and
  always as description rather than as an enrichment claim.

Not permitted without further work outside this table:
- any statistical claim about convergence;
- any ordering of states by depth, suppression, or distance from equilibrium;
- any claim that a state lacks a mechanism class.
