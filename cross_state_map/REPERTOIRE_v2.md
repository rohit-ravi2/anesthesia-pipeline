# FROZEN REPERTOIRE v2 — mechanism classes, roles, and perturbation direction

**Frozen 2026-09-16, after the v1 worm scoring (55 cells, 5 rows) and before any v2 cell was scored.**

**v1 is preserved unchanged and remains the record of what was scored under it.** This file does not
supersede `REPERTOIRE.md`; it is a versioned successor. Every change below traces to a specific,
documented failure in `scoring/WORM_AUDIT.md`. Nothing is added speculatively.

Governed by the same `INCLUSION_CRITERION.md` (unchanged: entry gate, exclusions, three axes, the
19 committed rows, the contamination disclosure). v2 changes the *mechanism representation only*.

---

## 0. What is unchanged from v1

Stated first, because most of v1 survived contact with the evidence.

- **The three-valued evidence logic is unchanged in meaning.** `TESTED_POSITIVE` /
  `TESTED_NEGATIVE` / `NOT_TESTED` answer exactly one question: *was this mechanism class
  experimentally implicated in this state?* The v1 worm result — 30 `NOT_TESTED` against 1
  `TESTED_NEGATIVE` in 55 cells — is the strongest argument for keeping it.
- **Evidence grades E-A … E-F are unchanged**, including the rule that E-E or E-F alone yields
  `SUGGESTED` and cannot support a positive.
- **Coverage denominators are unchanged and still mandatory.**
- **All prohibitions are unchanged**, in particular: no enrichment statistic over the table under any
  null; `NOT_TESTED` never reported as negative; no cross-species gene identity claims; citations
  title-and-content verified before scoring.
- **Causal chains are still recorded, not flattened**, and inferred steps still score no cell.
- **Assignment is still by proximal physical effect.**

## 0.1 What v1 got wrong, and what each repair answers

| v1 failure (from WORM_AUDIT.md) | v2 repair |
|---|---|
| `TESTED_POSITIVE` read as "this mechanism is suppressed in this state", when 3 of the best-evidenced positives run the other way | §3 perturbation records + derived `state_polarity` |
| Cryptobiosis: classes 1–7 presuppose the organism produces its own suppression; in anhydrobiosis suppression is physically imposed and all machinery is protective | §2 mechanism roles + §4 row-level `state_production` |
| Class 9 conflated state-responsive regulation with developmental specification of the machinery | §2 role `BUILDS_MACHINERY` |
| Demonstrated causal gap-junction mechanism in dauer force-assigned to class 10 | §1 class 12 |
| A_neu could not express "decorrelated but not less active" | §5 neural sub-axes |
| No way to hold conflicting evidence across readouts in one cell | §3 multiple perturbation records + `ambiguity` |
| No agent field inside the anaesthesia row | §3 `agent` on perturbation records |
| `NOT_TESTED` could not be distinguished from `NOT_APPLICABLE` | §6 `applicability`, orthogonal to coverage |
| Axis could not distinguish not-yet-measured from not-currently-definable | §5 `measurability` |
| A row could look well covered while resting on one paper | §6 computed `n_distinct_sources` |

---

## 1. Mechanism classes — class 12 added, 1–11 unchanged

Classes 1–11 keep their v1 definitions verbatim. One class is added.

### Class 12 — electrical coupling / gap-junction regulation and remodelling

**Proximal physical effect:** a change in the *electrical (and small-molecule) coupling between
cells* mediated by gap junctions — innexin/connexin channel composition, expression, localisation,
conductance, or the making and breaking of electrical synapses.

**Belongs in class 12:**
- neuron-type-specific change in innexin expression that alters coupling;
- remodelling, addition or removal of electrical synapses between identified cells;
- genetic manipulation of an innexin that alters the state or its behavioural output;
- pharmacological or genetic change in junctional conductance.

**Does NOT belong in class 12:**
- **chemical** synaptic transmission, vesicle fusion, or transmitter release → class 5;
- conductances carried by channels in the plasma membrane facing the *extracellular* space
  (leak, K⁺, Cl⁻, ionotropic receptors) → classes 1–4. The distinguishing feature is that a gap
  junction couples the cytoplasm of two cells rather than a cytoplasm to the bath;
- generic structural or biophysical change with no coupling readout (cuticle, vitrification,
  membrane lipid packing) → class 10;
- a transcription factor that *causes* an innexin expression change → class 9, recorded as an
  upstream step in the chain (see below).

**Canonical chain representation.** A transcriptional programme driving coupling change is recorded
as two steps, not one:

```
DAF-16/terminal selector TF   → class 9,  role BUILDS_MACHINERY,   upstream
innexin expression change → coupling change → class 12, role PRODUCES_STATE, proximal
altered behaviour             → class null (an outcome, not a mechanism)
```

The cell scored is class 12 (proximal) **and** class 9 (documented upstream), exactly as the v1
chain rule already required.

**Boundary case, recorded now so it is not decided ad hoc later:** a stomatin-family protein that
regulates both a degenerin channel and gap junctions (UNC-1) occupies classes 1, 10 and 12 by
separate evidence. v2 permits a molecule to appear in several classes when *separate* experiments
support each; it does not permit one experiment to populate several classes.

---

## 2. Mechanism role — the new orthogonal axis

Every mechanism record carries one or more **roles**. A role answers a different question from the
class: the class says *what the mechanism physically does*, the role says *what causal job it does
with respect to the state*.

Five roles, each instantiated by actual worm evidence (the check is recorded in
`AMENDMENTS.md` Entry 3):

| role | definition | test it must pass | worm instance |
|---|---|---|---|
| `PRODUCES_STATE` | the mechanism's activity brings the reduced-activity state about; manipulating it creates or abolishes the state itself | would the state fail to occur, or occur when it otherwise would not, on manipulating this? | RIS/FLP-11 in lethargus (ablation abolishes, optogenetic activation induces) |
| `CONTROLS_ENTRY` | sets the threshold, probability, or timing of entering the state without itself being the thing that produces it | does manipulation shift *when* or *at what dose* the state occurs, rather than whether the machinery exists? | insulin/TGF-β in dauer; `unc-79`/`unc-80` and `gas-1` setting anaesthetic dose–response |
| `MAINTAINS_STATE` | sustains, stabilises, consolidates or homeostatically regulates the state once entered | does manipulation change duration, fragmentation, depth or rebound rather than occurrence? | NALCN complex in lethargus (loss → fragmentation); DAF-16 sleep homeostasis; CEPsh glia limiting sleep duration |
| `PROTECTS_THROUGH_STATE` | preserves cells or the organism during the state without contributing to producing it | if abolished, does the animal fail to *survive* or fail to *recover*, while the state itself still occurs? | trehalose in anhydrobiosis; reduced cuticle permeability in dauer |
| `BUILDS_MACHINERY` | developmental specification that constructs the apparatus a state later uses; constitutive, not deployed on entry | is it required for the effector to exist at all, on a developmental rather than state timescale? | LIM-6/APTF-1 specifying RIS and FLP-11 expression |

**Reserved but NOT instantiated:** `ENABLES_EXIT` (recovery/resumption machinery) and
`PERMISSIVE_BACKGROUND`. No worm cell in the v1 scoring required either. They are named here so that
a future scorer adds them by amendment with evidence, rather than inventing a synonym. **Do not use
them until a cell requires one.**

**Roles are not exclusive.** A mechanism with separate evidence for two jobs carries two roles, each
with its own evidence grade and citations. A mechanism with one experiment gets one role.

**Roles apply to negative cells too.** A `TESTED_NEGATIVE` cell records `role_tested` — which job was
looked for and not found. This matters: v1 could not express that Complex I *modulates anaesthetic
sensitivity* (positive, `CONTROLS_ENTRY`) while *not controlling immobility in wild type* (negative,
`PRODUCES_STATE`). In v2 that is one cell with a positive role and a negative role.

---

## 3. Perturbation records — the authoritative representation of direction

**The raw experimental statement is authoritative. The compact sign is derived and secondary.**

Every mechanism carries one or more `perturbations`, each recording what was done and what happened:

- `manipulation` — `loss_of_function` | `gain_of_function` | `ablation` | `optogenetic_activation` |
  `optogenetic_inhibition` | `pharmacological_block` | `pharmacological_activation` |
  `expression_change` | `environmental` | `other`
- `direction_of_manipulation` — `decrease` | `increase` | `remove` | `not_applicable`
- `agent` — for drug states, the specific agent (halothane, isoflurane, diethyl ether, N₂O). Null
  otherwise. Added because worm anaesthetic sensitivities dissociate *by agent* (Morgan 1990) and v1
  could not hold that.
- `observed_effect` — an object with independent fields, each
  `increase` | `decrease` | `unchanged` | `not_reported`:
  - `total_quiescence` — amount of the state
  - `state_structure` — fragmentation / consolidation / duration / latency
  - `entry_threshold` — for states induced by a gradable stimulus: `hypersensitive` | `resistant` |
    `unchanged` | `not_reported`
  - `survival_recovery` — survival of, or recovery from, the state
  - `other` — free text
- `context_dependence` — `none_reported` | `dose_dependent` | `timing_dependent` |
  `readout_dependent` | `cell_type_dependent`
- `statement` — the experimental result in the source's own terms. **This field is authoritative and
  must be populated.** If the compact fields and the statement ever disagree, the statement governs.
- `evidence_grade`, `citation_ids`

### Derived `state_polarity` (convenience only, never authoritative)

| value | meaning |
|---|---|
| `PROMOTES_STATE` | more mechanism activity → more of the state; less → less |
| `OPPOSES_STATE` | more mechanism activity → less of the state |
| `STRUCTURE_ONLY` | manipulation changes organisation/duration/fragmentation without a clean change in total amount |
| `CONTEXT_DEPENDENT` | sign differs by dose, timing, readout, or cell type |
| `UNDETERMINED` | the experiment does not support a sign |

**Rule: never assign a polarity the experiment does not support.** `UNDETERMINED` and
`STRUCTURE_ONLY` are correct answers, not failures. A derived polarity may not be computed from a
mechanism's *name* or from expectation; only from its perturbation records.

---

## 4. Row-level `state_production`

One field per (state, species) row, forced by cryptobiosis:

- `ENDOGENOUS` — the organism's own machinery brings the state about (lethargus, L1-arrest sleep, dauer)
- `EXOGENOUS_AGENT` — an external agent produces it; organismal mechanisms modulate susceptibility
  (volatile anaesthesia)
- `PHYSICALLY_IMPOSED` — the state follows from a physical condition and no organismal mechanism
  produces it (anhydrobiosis: water removal halts the chemistry)

This makes explicit what v1 assumed universally and what was true only for some rows. It also
predicts, checkably, where `PRODUCES_STATE` cells can exist at all: a `PHYSICALLY_IMPOSED` row
should have none.

---

## 5. Neural axis — minimal decomposition

v1's single `A_neu` direction could not express the two best neural measurements in the worm set
(isoflurane decorrelation without reduced activity; starvation robustness while awake). The smallest
faithful repair keeps one axis and decomposes its *measurement*:

`A_neu` carries three independent sub-measures, each with its own direction, grade and citations:

- `rate_amplitude` — population firing rate, event rate, response or dynamic-range amplitude
- `coordination` — inter-neuronal correlation, synchrony, integration, dimensionality of shared structure
- `dynamical_organization` — spectral content, state structure, trajectory organisation, repertoire

`A_beh` and `A_met` remain single-valued; no worm evidence required decomposing them.

Additional axis fields, all three axes:

- `scope` — `whole_brain` | `population_subset` | `single_cells` | `whole_organism` | `not_applicable`
- `condition` — a within-state sub-phase label, so a row can carry more than one record per axis
  (e.g. `starved_awake` vs `starved_asleep`). Axis records are keyed by (axis, condition).
- `measurability` — `MEASURED` | `NOT_YET_MEASURED` | `NOT_CURRENTLY_DEFINABLE`. The last is for
  cases like neural activity in a desiccated animal, where there is no aqueous phase in which the
  measurement is defined — categorically different from nobody having tried.

**Binding rule, carried forward and strengthened:** do not record `rate_amplitude: decrease` unless
the experiment measured a reduction in activity. Decorrelation, randomisation, loss of
low-dimensional structure, and spectral shift are `coordination` and `dynamical_organization`
findings and must be recorded as such.

---

## 6. Two further fields

- `applicability` on each cell — `APPLICABLE` | `QUESTIONABLE` | `NOT_APPLICABLE`, **orthogonal to
  coverage**, so the three-valued evidence logic is untouched. Class 11 (thermal/rate) in a
  poikilotherm is `NOT_APPLICABLE`, which is not the same claim as `NOT_TESTED`.
- `n_distinct_sources` computed per row in `row_summary`, so a row resting on one paper is visible.

---

## 7. What v2 still cannot do

Recorded honestly, so the next version has a target list.

1. No quantitative effect sizes. Perturbation records are directional only. Any later energetic or
   dynamical work will need magnitudes and will not find them here.
2. No representation of *interaction* between mechanisms (epistasis, redundancy, parallel pathways).
   `unc-9` suppressing `unc-79`/`unc-80` is a suppression relationship that v2 records as two
   separate mechanisms, losing the interaction.
3. No time-resolved representation within a state beyond the `condition` label.
4. `state_polarity` collapses a multi-field observation into one token and will be wrong at the
   edges; this is why the raw statement is authoritative.
5. The classes 1–4 coarsening sensitivity analysis committed in `INCLUSION_CRITERION.md` §6 is
   **still owed** and is not performed by this version.
