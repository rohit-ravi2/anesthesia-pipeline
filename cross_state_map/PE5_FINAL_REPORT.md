# The mechanism repertoire of reversible reduced-activity states

### PE-5 final report — 2026-09-17

**Completion validator `scoring/validate_pe5_completion.py` exits 0.** Three gates pass on all ten
scored rows: five search routes executed per row (A), 120 of 120 cells terminally disposed (B),
measured internal retrieval recall 1.00 (C). `scoring/validate_v2.py` reports zero schema violations.
Citation ledger: **154 verified PMIDs, 0 unresolved**, every title fetched in-run and never recalled.

---

## 1. What this project asked

Not *do reduced-activity states share a mechanism?* That question was explicitly set aside early and
is not the premise here.

The premise is: **these states are possible because the machinery that can implement them already
exists in the organism.** Sleep, anaesthesia, dauer, L1 arrest and cryptobiosis are not each built
from bespoke parts; each is an *affordance* of a repertoire the animal already has for other reasons.
The question the table answers is therefore per-state and not comparative: **for each state, which
parts of the repertoire has anyone actually shown it acts on, and in what causal role?**

Convergence, if it appears, is a result. It is not the search criterion, and nothing in the method
rewards finding it.

---

## 2. What was built

A frozen mechanism-repertoire × state map.

- **12 mechanism classes**, defined by *physical action* rather than by molecule
  (`REPERTOIRE.md`, `REPERTOIRE_v2.md`, SHA-256 frozen).
- **10 scored (state, species) rows** out of 19 committed. The scoring unit is (state, species),
  never a state alone — the same state in two species is two rows.
- **120 cells**, each carrying three-valued evidence logic: `TESTED_POSITIVE` / `TESTED_NEGATIVE` /
  `NOT_TESTED`, never collapsed to a binary.
- **An orthogonal causal-role axis**: `PRODUCES_STATE`, `CONTROLS_ENTRY`, `MAINTAINS_STATE`,
  `PROTECTS_THROUGH_STATE`, `BUILDS_MACHINERY`, `ENABLES_EXIT`.
- **Three phenotype axes** never collapsed into one depth score: behavioural `A_beh`, neural `A_neu`,
  metabolic `A_met`.
- **A per-pair molecular-resolution hierarchy**: `EXACT_MOLECULE` → `ORTHOLOGOUS_MOLECULE` →
  `SAME_COMPLEX` → `SAME_PATHWAY_MODULE` → `SAME_PHYSICAL_CLASS` → `NO_ESTABLISHED_OVERLAP`.
  Resolution is declared per pair and never inferred from a shared class label.

Every modification since the freeze is amendment-only and logged in `AMENDMENTS.md` (13 entries).
No hashed file has been edited in place.

---

## 3. Headline result

**Across 120 cells, 96 recorded mechanisms and 154 verified sources, no mechanism has ever been shown
to PRODUCE the anaesthetised state, and no mechanism has ever been shown to ENABLE EXIT from an
endogenous one.**

| `state_production` | rows | PRODUCES | ENTRY | MAINTAINS | PROTECTS | BUILDS | **EXIT** |
|---|---|---|---|---|---|---|---|
| ENDOGENOUS (sleep, dauer, L1 arrest) | 5 | **16** | 16 | 16 | 4 | 4 | **0** |
| PHYSICALLY_IMPOSED (cryptobiosis) | 1 | 0 | 2 | 0 | 2 | 1 | **0** |
| EXOGENOUS_AGENT (anaesthesia) | 4 | **0** | 18 | 3 | 3 | 0 | **5** |

Both zeros are exact, and they are complementary. This is not a coverage artefact: the most
completely scored row in the entire table is `S5_ga_volatile_mmus` at 11/12 cells, and it still
carries zero `PRODUCES_STATE`. The two most completely scored sleep rows carry zero `ENABLES_EXIT`.

---

## 4. Why the zeros are there

The honest reading is that **this is a fact about the literature's question set before it is a fact
about biology**, and the table can say which because `state_production` was frozen into the schema
before any of this was visible.

For a state imposed by a drug, "what produces it?" has a trivially available answer — the drug — so
nobody asks what *in the animal* produces it. What is worth an experiment is why one animal needs
more drug than another (entry) and why some wake up slowly (exit). For a state the animal generates
itself, "what produces it?" is the whole question, and exit is handed to the circadian clock and the
homeostat, so nobody manipulates it.

The literature's shape follows from the mode of state production. That is a structural prediction the
table makes about its own source material, and it is falsifiable: **find one manipulation that
produces the anaesthetised state without an anaesthetic, or one that accelerates waking from natural
sleep at fixed sleep pressure, and this pattern breaks.**

It also converts directly into the two highest-value experiments in §18.

---

## 5. The single most informative result, and it is a negative

**PMID:40240218.** Caspase ablation of parafacial-zone GABAergic neurons in mouse:

- **volatile anaesthesia** — durable behavioural resistance to *both* isoflurane and sevoflurane,
  ~50% higher likelihood of intact righting, resistance inversely correlated with surviving neuron
  count, faster emergence with purposeful movement. Scored `CONTROLS_ENTRY` + `ENABLES_EXIT`.
- **natural NREM sleep** — *in the same animals, in the same paper*: no change in sleep amount, no
  change in wakefulness, no change in homeostatic drive after deprivation, with 70–80% of the
  population destroyed. Scored as a measured null with `MAINTAINS_STATE` in `roles_tested_negative`.

A node of the sleep-promoting circuitry is **required for the drug-induced state and dispensable for
the endogenous one.** The anaesthesia field's central hypothesis — that general anaesthetics co-opt
endogenous sleep circuitry — survives, but with a constraint it did not have before: **co-option is
not symmetric.** A shared node can be load-bearing in one direction only.

The same paper carries a second dissociation the authors state explicitly: the *behavioural* endpoint
moved and the *EEG signature* did not. `A_beh` moved, `A_neu` did not. A single collapsed
"anaesthetic depth" score would have erased both findings. This is the clearest vindication in the
project of the frozen three-axis rule.

**Scope:** one node, not the circuit class. Nothing here licenses a general claim that sleep
circuitry is dispensable for NREM.

---

## 6. Causal role is a property of the state, not of the molecule

Four independent demonstrations, in increasing order of tightness:

| molecule | state A | role | state B | role |
|---|---|---|---|---|
| GluN1 (LPO) | mouse REM | `PRODUCES_STATE` — REM cannot be generated | mouse NREM | `MAINTAINS_STATE` — fragmented, normal total |
| SLO-1 / BK | worm lethargus | `MAINTAINS_STATE` — sleep duration shortened | worm volatile | `CONTROLS_ENTRY` — anaesthetic resistance |
| UNC-9 innexin | worm lethargus | `PRODUCES` + `MAINTAINS` + `ENTRY` | worm volatile | `CONTROLS_ENTRY`, opposite sign |
| PZGABA neurons | mouse volatile | `CONTROLS_ENTRY` + `ENABLES_EXIT` | mouse NREM | **tested and absent** |

The last is the strongest: same neurons, same manipulation, same animals, same paper. The rows differ
only in which state was assayed. Before this run, this claim rested on cross-species comparisons in
which allele, preparation and endpoint all differed simultaneously.

---

## 7. NALCN, five contexts, five role/polarity combinations

| state | molecule | manipulation | endpoint | role | polarity |
|---|---|---|---|---|---|
| worm lethargus | nca-1/2, unc-79, unc-80 | LOF | quiescence, fragmentation | MAINTAINS | CONTEXT_DEPENDENT |
| worm volatile | unc-79, unc-80 | LOF | immobility EC50 | CONTROLS_ENTRY | OPPOSES |
| mouse REM | Nalcn | dominant GOF | REM amount + episode duration | ENTRY + MAINTAINS | OPPOSES |
| mouse volatile | Unc79 (Lwt/+) | LOF het | "altered isoflurane response" | CONTROLS_ENTRY | UNDETERMINED |
| mouse volatile | Nalcn (RTN) | drug activation + silencing | CO₂ ventilatory response | PROTECTS_THROUGH | UNDETERMINED |

Four states, two species, five contexts. The molecular recurrence is real, at
`ORTHOLOGOUS_MOLECULE`/`SAME_COMPLEX`. **The function is not conserved.** The fifth entry is not even
about the anaesthetised state — it is about preserving breathing *through* it.

This is the pattern the whole project predicts: shared machinery, unshared function. It is the
opposite of a convergence result, and it is what an affordance account looks like when it is right.

---

## 8. Complex I: the widest correspondence in the table, across three species

| species | molecule | manipulation | result |
|---|---|---|---|
| C. elegans | gas-1 (49 kDa subunit) | LOF | volatile hypersensitivity |
| mouse | Ndufs4 (accessory subunit) | KO | **2.5–3× hypersensitive** to isoflurane and halothane, 2× to propofol, **resistant to ketamine** — the largest anaesthetic-sensitivity change recorded in a mammal |
| human | MT-ND4 m.11232T>C (L158P) | natural variant | severe perioperative neurologic deterioration after volatile anaesthesia; **no adverse events in the same individuals under intravenous-only anaesthesia** |

Three species, three different subunits of one respiratory complex, one agent class, one direction.
Recorded at `SAME_COMPLEX`, and the endpoints are deliberately *not* merged: immobility EC₅₀ in worm,
loss of response in mouse, neurologic injury in human. It is a correspondence of mechanism, not of
phenotype.

Two further results sharpen it. **The lesion is routed through excitatory neurons specifically**:
restricting NDUFS4 loss to glutamatergic neurons reproduces the hypersensitivity while GABAergic and
cholinergic restriction do not, baseline CA1 electrophysiology is normal, and at 0.6% isoflurane
sEPSC frequency falls only in the knockout while sIPSCs are unaffected. And **potency and tolerance
are different quantities**: the same Ndufs4 animals are hypersensitive *and* are killed by prolonged
low-dose isoflurane — a toxicity that is macrophage-dependent and pharmacologically rescued by a
CSF1R inhibitor, making it a target rather than an inevitability.

---

## 9. Agent specificity is now established four times over

Anaesthetics are routinely discussed as a class. The table's evidence says they are not one.

| manipulation | hypersensitive to | resistant to / unchanged |
|---|---|---|
| Ndufs4 KO | isoflurane, halothane, propofol | **ketamine** |
| Stomatin KO | diethyl ether (+12%) | halothane, isoflurane (**measured null, positive internal control**) |
| EAAT3 KO | isoflurane *hypnosis* | isoflurane *immobility*; ketamine hypnosis |
| N-type Ca²⁺ channel KO | **halothane** | **propofol — oppositely affected** |
| NALCN in RTN | isoflurane, sevoflurane activate it | **propofol does not** |
| MT-ND4 variant | volatile agents | intravenous agents |

The N-type calcium channel result is the sharpest: not "less affected" but *oppositely* affected, in
one genotype, with a matched hippocampal field-potential correlate. The authors' own conclusion is
the claim: inhibition of the N-type channel "underlies mechanisms of halothane anesthesia but
counteracts propofol anesthesia."

**Consequence for the field:** "anaesthetic sensitivity" is not one quantity. It is at least
agent-specific and, per EAAT3, endpoint-specific within a single agent — immobility (spinal) and
hypnosis (supraspinal) come apart under one lesion in one animal.

---

## 10. AP-2: the only correspondence where the role is conserved too

`Tfap2b` acts embryonically in mouse GABAergic neurons; deletion shortens both NREM and REM and
weakens delta and theta power, at baseline and in rebound. Its direct orthologue **APTF-1** already
carried this table's worm lethargus class-9 entry as the transcriptional specifier of the RIS sleep
neuron.

Both are assigned `BUILDS_MACHINERY`. Both act developmentally. Both act on the GABAergic
sleep-promoting population. The species are separated by roughly 600 Myr, and the authors state
directly that AP-2 transcription factors control sleep in *C. elegans*, *Drosophila* and mice.

This is the deepest correspondence in the table, and the **only one where molecule and role are both
conserved**. It is also the first mammalian `BUILDS_MACHINERY` assignment; the only two before it
were in *C. elegans*, and one of them is this one's orthologue.

---

## 11. Gap junctions: convergent proteins, opposite signs

| row | protein | manipulation | effect |
|---|---|---|---|
| worm lethargus | UNC-7 + UNC-9 innexin | LOF; joint overexpression | sleep reduced and arousal threshold lowered; **overexpression sufficient to induce anachronistic adult sleep** |
| worm volatile | UNC-9 innexin | LOF | **suppresses** unc-79/unc-80 halothane hypersensitivity |
| mouse volatile | Connexin36 | KO | **causes** hypersensitivity (EC₅₀ 0.37% vs 0.49%) and prolongs propofol anaesthesia in young animals |
| mouse NREM | Pannexin1 | KO | less slow-wave sleep, more waking; **homeostatic rebound intact** |

Connexins and innexins are **convergently evolved, not homologous** — recorded at
`SAME_PHYSICAL_CLASS`, which is exactly what that level exists to express. Pannexins *are* innexin
superfamily members, so `ORTHOLOGOUS_MOLECULE` applies there — but the worm entries act as electrical
synapses while Panx1 is proposed to act as a metabolite conduit. **Same superfamily, different
physical function.** Had resolution been inferred from the class label instead of declared per pair,
all four would have been collapsed into one spurious "gap junctions matter" claim with contradictory
signs inside it.

The worm lethargus entry is independently notable as one of very few **necessity *and* sufficiency**
demonstrations anywhere in the table, with epistasis placing gap junctions downstream of both EGL-4
and the NCA/NALCN channels, and an explicit internal negative (PDFR-1 loss does not suppress).

---

## 12. Entry and maintenance come apart, and so do state and controller

Manipulations that separate these are rare and each one is load-bearing.

- **Entry without maintenance.** Optogenetic activation of cholinergic PPT/LDT neurons during NREM
  increased the *number* of REM episodes and did not change episode *duration*; activation was
  *sufficient* to induce REM. `PRODUCES_STATE` + `CONTROLS_ENTRY`, with `MAINTAINS_STATE` tested and
  negative.
- **State without its controller.** CD73-knockout mice sleep *more* at baseline yet show *no* NREM
  rebound after deprivation, while IL-1β still increases their NREM. Entry machinery intact,
  homeostatic drive lost — and the IL-1β arm is the positive control that makes the null interpretable.
- **The exact mirror, in the same row.** Panx1-knockout mice sleep *less* at baseline and their
  rebound is *intact*. Two manipulations of one adenosine pathway dissociate baseline amount from
  homeostatic drive in opposite directions.
- **Oscillation without amount.** GABA-A β1 knockout changes delta power in NREM and theta power in
  REM with *no* change in sleep-wake architecture. Scored `STRUCTURE_ONLY`: positive on `A_neu`,
  negative on state amount.
- **Required but not sufficient.** DMH GABAergic ablation removes the coupling from ambient
  temperature to NREM, while chemogenetic activation *or* inhibition of the same neurons changes
  nothing about the sleep-wake cycle on its own (see §16).
- **Ligand and receptor dissociate.** Deleting orexin is worse than deleting OX2R for REM intrusion
  and equivalent for NREM attacks, so "orexin signalling" is not one class-6 entry but two.

---

## 13. Cryptobiosis, and what the table's holes actually mean

The cryptobiosis row is populated in classes 8, 9 and 10 only — metabolism, transcription, structural
biophysics — and empty in every channel, receptor, circuit and neuromodulator class. After a search
demonstrated at recall 1.00, that hole is not an artefact.

**The mechanism classes interrogated for a state track the discipline that studies the state, not the
biology of the state.** Anaesthesia is studied by pharmacologists, so it is dense in channels and
receptors. Sleep is studied by systems neuroscientists, so it is dense in circuits and
neuromodulators. Cryptobiosis is studied by biochemists, so it is dense in metabolites and proteins.
Nobody has asked whether a *C. elegans* dauer entering anhydrobiosis changes its electrical coupling,
and there is no reason from the biology to think the question is uninteresting.

Two cryptobiosis findings also mark the limit of any pan-organism account. **The glyoxylate shunt**
is required during *preconditioning* — before the state — and builds the trehalose pool the animal
will need; it is the table's cleanest `BUILDS_MACHINERY` case. **LEA-1**, a disordered protein, is
required in vivo for desiccation survival, and short defined motifs are sufficient to replace it.
Neither the glyoxylate shunt nor LEA proteins exist in mammals.

**Some affordances are simply unavailable to us.** That is the correct form of the project's thesis:
not that all animals converge on one solution, but that each state is built from whatever repertoire
that lineage happens to have.

---

## 14. The human rows, and a limit that is not a search failure

Human volatile 3/12; human propofol 2/12. Both rows pass Gate C at recall 1.00, so this is not
under-searching.

**It is a design limit.** The mechanism classes are defined by physical action and the evidence
standard is causal manipulation. In humans you cannot delete a channel. What exists is exactly what
is ethically available:

- pharmacological antagonism at fixed drug concentration — physostigmine restoring consciousness at
  constant end-tidal sevoflurane (5/8 volunteers), and raising the propofol induction dose 2.0 → 2.4
  mg/kg in an RCT;
- **caffeine accelerating emergence from isoflurane in a randomised double-blind crossover**, 16.5 →
  9.6 min, a 42% reduction — and emergence occurred at a *higher* expired isoflurane concentration,
  so this is not faster washout: the same brain concentration no longer sustained the state;
- applied physical variables — hypothermia lowering isoflurane MAC 5.1%/°C, and isoflurane lowering
  vasoconstriction and shivering thresholds ~4.6 °C;
- natural genetic variants read observationally — the MT-ND4 haplotype of §8.

The caffeine result deserves emphasis out of proportion to its size (n=8, one agent, one dose): it is
the cleanest human evidence that **the anaesthetised state is actively held rather than passively
imposed**, and a direct instance of the project's thesis — the state is afforded by machinery the
organism already has, and that machinery can be pushed the other way.

---

## 15. Thermal coupling runs in both directions

Class 11 now carries both directions and they are not confounds of each other.

- **Temperature → state**: hypothermia reduces isoflurane MAC dose-dependently in humans (5.1%/°C);
  in mice, cold exposure increases waking and decreases NREM while warm exposure does the reverse,
  and DMH GABAergic ablation removes that coupling.
- **State → temperature**: isoflurane lowers vasoconstriction and shivering thresholds ~4.6 °C at 1%
  end-tidal; sleep-active preoptic neurons causally drive heat loss.

The reverse direction still has to be stored as a role-less mechanism, because **there is no thermal
phenotype axis**. `A_beh`, `A_neu` and `A_met` cannot hold "body temperature fell." This is now the
best-supported outstanding amendment in the project (§17).

---

## 16. One reserved role, deliberately not opened

DMH GABAergic neurons are **required** for ambient temperature to modulate NREM and **not sufficient**
to drive sleep — demonstrated in one paper by two manipulations pointing opposite ways.

None of the six instantiated roles fits. It is neither production, maintenance, unconditional entry
control, protection, construction, nor exit. It is the strongest candidate so far for instantiating
the reserved role `PERMISSIVE_BACKGROUND`.

**It was not instantiated.** One paper is not enough to open a frozen role, and doing so on a single
result is exactly the ontology drift the freeze discipline exists to prevent. It is scored meanwhile
as `CONTROLS_ENTRY` with `context_dependence: thermal_challenge_dependent`, which is accurate and
under-describes it, and logged as a pending decision with a named trigger: **instantiate when a
second independent required-but-not-sufficient result appears in any row.**

---

## 17. Ontology changes made this run

**`SCHEMA_v2_2.json` — new polarity `NO_ESTABLISHED_EFFECT`.** The ontology admitted
`coverage = TESTED_NEGATIVE` at cell level but offered no polarity for the *mechanism* carrying the
null, so a measured negative had to be written as `UNDETERMINED` — which means something else
entirely. Legal only on a mechanism with an explicit `negative_assay_statement` or an internal
positive control.

The consequential rule, now enforced: **the roles of a `NO_ESTABLISHED_EFFECT` mechanism are roles
tested and found absent.** They go in `roles_tested_negative` and must never enter `roles_present` or
the role counts. Without this, every measured null would have silently inflated the role tallies —
the precise error three-valued evidence logic exists to prevent. `SCHEMA_v2.json` was not edited; the
amendment is a separate file and the original hash is unchanged.

**Still deferred, with the case now stronger:** an `A_therm` phenotype axis (§15);
`PERMISSIVE_BACKGROUND` (§16); a **stress-induced-sleep row** — three independent papers this run
(nlp-2/22/23 dispensable for SIS but required for DTS; dgk-1 required for both; a glr-5 screen in
SIS) had findings that could not be scored because the state is not committed. One of them,
PMID:42161335, was found and deliberately *not* applied, because scoring SIS under the lethargus row
would be exactly the state-substitution error the inclusion criterion forbids.

---

## 18. What to do next — the four experiments the table now demands

Each is named by a hole that is *demonstrated*, not merely unfilled, because the row it sits in
passes Gate C at recall 1.00.

**PE-A. Produce the anaesthetised state without an anaesthetic.** The entire `PRODUCES_STATE` column
is empty for four rows across three species (§3–4).

**The prior-art check found this partially attempted, and the result is now scored.** PMID:41573848
captured isoflurane-activated neurons brain-wide with a Fos-driven DREADD system and reactivated them
without anaesthetic: **immobility, discoordination, anti-nociception and significantly increased
anaesthetic sensitivity appeared — loss of consciousness, measured by righting, did not.** That is
recorded at `S5_ga_volatile_mmus` c7 as a positive on entry and a **measured null on
`PRODUCES_STATE`**, and it upgrades §3–4 from "nobody has attempted it" to "it has been attempted at
ensemble level and the components of the anaesthetic state came apart under the attempt."

**Re-scoped residue.** A Fos-captured ensemble is not a cell type; it is whatever was metabolically
active under the drug. The test that remains is cell-type-specific: in mouse, **activate** the
parafacial GABA population whose **ablation** already confers durable resistance to isoflurane and
sevoflurane hypnosis (§5), and score the resulting state on all three axes independently — with
righting and immobility kept separate, per the EAAT3 dissociation in §9. The ablation arm is done and
is dose-graded; the sufficiency arm is not. A positive would be the first entry in that column. A
negative, on top of PMID:41573848, would convert §4 from a claim about the literature into a claim
about biology: the anaesthetised state may not be producible from within.

**PE-B. Accelerate exit from natural sleep at fixed sleep pressure.** `ENABLES_EXIT` is empty for all
five endogenous rows while anaesthesia has five. Caffeine's human anaesthesia result (§14) is the
template: the discriminating measurement is exit *at matched drive*, not exit *per se*.

**PE-C. Ask a channel question of cryptobiosis.** Nine of twelve classes are empty (§13) and the
hole is disciplinary. Concretely: does electrical coupling change during anhydrobiotic entry in dauer
larvae? Innexin remodelling is already a scored positive in the dauer row, and desiccation is imposed
on dauers — the two literatures are adjacent and have never been joined.

**PE-D. Test complex I anaesthetic hypersensitivity prospectively in humans.** §8 gives a
three-species mechanism and a human variant currently supported only observationally, with a clean
agent dissociation (volatile yes, intravenous no) that is directly actionable perioperatively. The
mouse arm further shows the injury is macrophage-dependent and rescued by a CSF1R inhibitor, so there
is a named intervention as well as a named risk.

A fifth is procedural rather than biological: **commit a stress-induced-sleep row** (§17). Three
papers this run already had findings for it.

---

## 19. Method, and the part of it worth reusing

The finding that reframed this entire program is not about biology.

**The search protocol used for every prior run had a measured recall of 0.05.** NCBI eutils ANDs bare
terms, so the concatenated multi-concept queries used throughout demanded that *every* term appear.
Sedensky 1987 — the founding worm anaesthesia-genetics paper — returned **zero hits**. Every earlier
statement of the form "no qualifying evidence identified under the standardized search" was therefore
void, and a 720-query sweep whose near-empty worm yield had looked like saturation was an artefact.

The repair and its calibration:

| protocol | depth (cele/mmus/hsap) | recall | rows at 1.00 |
|---|---|---|---|
| v1 concatenated | 10 | **0.05** | 0 |
| v2 boolean OR-groups | 15 | 0.56 | 0 |
| v2 | 120/200/200 | 0.90 | 5 |
| v3 repaired vocabulary | 120/200/400 | 0.92 | 6 |
| v3 | 150/500/800 | 0.98 | 8 |
| **v3** | **150/1200/1600** | **1.00 (111/111)** | **10** |

The hold-out denominator grew from 41 to 111 during calibration, because the battery kept finding new
load-bearing papers that then joined the target set. **The final 1.00 is on a target that grew by
170%.**

Three method results are portable beyond this project:

1. **Broadening vocabulary at fixed depth costs recall.** Moving to the v3 vocabulary at unchanged
   depth dropped the mouse volatile row from 0.89 to 0.83 — extra OR-terms enlarge the pool, so known
   papers fall past the cut. Breadth and depth are coupled.
2. **Attribute every residual miss to a component before changing anything.** The diagnostic
   `<component> AND <pmid>[uid]` settles it. Two misses looked identical and were not: one was depth,
   one was a vocabulary gap in a set of 1085 records that was already below the retrieval cap.
   Raising depth for the second would have cost thousands of records and fixed nothing.
3. **A null is only as interpretable as the instrument's measured recall.** This is why Gate B refuses
   to accept `NOT_TESTED_AFTER_FULL_SEARCH` from any row that fails Gate C.

A quieter defect is worth recording because it survived three working rounds: `lit.py` keyed its disk cache
on Python's builtin `hash()`, which is salted per process, so the cache never hit across runs and
every calibration round silently re-fetched everything.

---

## 20. What this table cannot be used for

Stated as prohibitions because they are enforced by the validator and by `REPERTOIRE.md`, not left to
the reader's discretion.

1. **No enrichment claim.** The cells are searched to measured but *unequal* completeness, and the
   classes are of unequal size and unequal literature history. Counting positives per class and
   calling one "enriched" is invalid.
2. **Literature co-occurrence is never evidence.** Every cell is scored from a documented
   experimental manipulation with a named endpoint.
3. **`NOT_TESTED` is never reported as negative** — in text, in a figure, or in a summary statistic.
   53 of 120 cells are `NOT_TESTED_AFTER_FULL_SEARCH`; that is a statement about the literature.
4. **The three axes are never collapsed** into a depth score or an ordering. §5 is what that rule
   buys.
5. **No cross-species identity claim** beyond the resolution declared for that specific pair.
6. **Every citation passes the verification harness.** 154 PMIDs, every title fetched in-run.
7. **The completed table must be re-scored under the coarsened partition** merging classes 1–4, per
   the contamination disclosure in `INCLUSION_CRITERION.md` §6. *This remains outstanding* and is the
   largest known methodological debt (§22).

---

## 21. Honest grading

**What is solid.** The three-valued logic and role axis are doing real work and repeatedly caught
errors that a binary table would have absorbed. The measured-recall gate is the strongest
methodological feature and is portable. The 154-PMID verified ledger is a durable asset. §5, §6, §8,
§9 and §10 are results that would survive review as stated.

**What is weak, and would be attacked.**

- **Ten of nineteen committed rows are scored.** Hibernation, torpor, Drosophila sleep, zebrafish
  sleep and several others are committed and empty. Nothing in §3–4 is safe from a hibernation row
  that behaves differently, and hibernation is exactly the state where an endogenous system does
  something anaesthesia-like on purpose.
- **Coverage is deeply uneven**: 11/12 for mouse volatile, 2/12 for human propofol. Any statement
  comparing rows inherits that unevenness, and §3's zeros are stated the way they are precisely
  because the *best-covered* row carries one of them.
- **One row rests partly on a preprint.** `S6_starv_L1_cele` c9 (HLH-30/TFEB) is bioRxiv, graded E-C
  on that ground and flagged for revisit.
- **The class-1–4 coarsening has not been run.** Until it is, the class boundaries between cation
  leak, K⁺ conductance, Cl⁻ shunt and excitatory block are a scorer's judgement, and the
  contamination disclosure says so.
- **Role assignment is interpretive.** It is made from the perturbation record and the raw statement
  is authoritative, but two careful scorers could differ on `CONTROLS_ENTRY` vs `MAINTAINS_STATE` in
  perhaps a fifth of cells. No inter-rater measurement has been made. That is the most obvious
  reviewer objection to §3, and the honest answer is that §3's zeros are robust to it: no plausible
  re-reading turns any anaesthesia cell into `PRODUCES_STATE`, because no experiment in those rows
  produced the state without the drug.

**Is it publication grade?** The method section is, and would stand alone as a short methods paper on
retrieval calibration for structured literature synthesis. The biology is a strong, well-instrumented
*negative-space map* — it says with unusual precision what has not been asked. It is not yet a
findings paper, because the headline is about the literature's question set. Scoring hibernation and
running the coarsening are what would convert it.

---

## 22. Outstanding debts, in priority order

1. **Class 1–4 coarsening re-score** — mandated by the frozen inclusion criterion, never run.
2. **Hibernation/torpor row** — the state most likely to break §3, and committed but unscored.
3. **Inter-rater reliability on role assignment** — the most obvious reviewer objection, unmeasured.
4. **`A_therm` axis amendment** (§15) — now well-supported.
5. **Stress-induced-sleep row** (§17) — three papers already waiting.
6. **`PERMISSIVE_BACKGROUND`** (§16) — blocked on a named trigger, correctly.
7. **Replace the preprint** at `S6_starv_L1_cele` c9 when peer-reviewed.
8. **Nine remaining committed rows.**

---

## 23. Files

**Frozen (SHA-256, never edited in place):** `INCLUSION_CRITERION.md`, `REPERTOIRE.md`,
`REPERTOIRE_v2.md`, `SCHEMA.json`, `SCHEMA_v2.json`, `states.json`, `states_v2.json`,
`states_v2_1.json`.

**Amendments:** `AMENDMENTS.md` (12 entries), `SCHEMA_v2_2.json`.

**Scored data:** `scoring/rows_v2/*.json` (10 rows × 12 cells), `scoring/ledger.json` (154 verified).

**Search instrument:** `scoring/lit.py`, `scoring/pe5_vocab_v3.py`, `scoring/pe5_pipeline.py`,
`scoring/pe5_citation_chain.py`, `scoring/pe5_recovery_v3.py`, `scoring/pe5_worklist.py`.

**Application scripts (idempotent, re-runnable):** `scoring/pe5_apply_findings.py`,
`scoring/pe5_apply_r2.py` … `pe5_apply_r7.py`, `scoring/pe5_ledger_sync.py`.

**Validators:** `scoring/validate_v2.py` (schema, exit 0), `scoring/validate_pe5_completion.py`
(three gates, exit 0).

**Derived:** `PE5_MATRICES.md` (A–E), `PE5_STRUCTURAL_ANALYSES.md`,
`scoring/PE5_RECOVERY_SUMMARY.json`, `scoring/pe5_recovery/*.json`,
`scoring/PE5_CELL_LEDGER.json`, `scoring/PE5_EXECUTION_LEDGER.json`,
`scoring/SEARCH_METHOD_AUDIT.md`.

**Audits:** `scoring/WORM_AUDIT.md`, `WORM_V2_AUDIT.md`, `MAMMAL_V2_STRESS_TEST.md`,
`MECHANISM_OVERLAP_AUDIT.md`, `MOUSE_VOLATILE_OVERLAP_AUDIT.md`, `THERMO_BRIDGE_MEMO.md`.
