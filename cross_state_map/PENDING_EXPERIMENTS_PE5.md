# Pending experiments — PE-5 completion revision

**Date:** 2026-09-17. Supersedes `PENDING_EXPERIMENTS.md` for all entries listed here.

**Every entry carries a `HAS THIS ALREADY BEEN DONE?` line answered by running the v3 protocol at
production depth against the specific question.** That check is meaningful for the first time, because
the instrument now has measured internal recall 1.00. Two entries were re-scoped by it and one produced
a scoreable result on the spot.

I do no wet-lab work. Every entry is framed as an experiment this project PROPOSES to
collaborators or to the field, which is the only terminus available and is not a blocker.

---

## PE-A — Produce the anaesthetised state without an anaesthetic  **[HIGHEST PRIORITY]**

**Gap.** Zero `PRODUCES_STATE` across four anaesthesia rows and 29 populated cells, including the
table's most completely scored row (mouse volatile, 11/12). Claim D2.

**HAS THIS ALREADY BEEN DONE? — PARTIALLY, AND IT FAILED INFORMATIVELY.**
`PMID:41573848` (bioRxiv 2025) captured isoflurane-activated neurons brain-wide with a Fos-driven
DREADD system and reactivated them without anaesthetic. Result: **immobility, discoordination,
anti-nociception and significantly increased anaesthetic sensitivity — but NOT loss of consciousness
as measured by the righting reflex.** Scored this run at `S5_ga_volatile_mmus` c7 as a positive on
entry and a **measured null on `PRODUCES_STATE`**.

Also relevant and not yet scored: `PMID:41333446` / `41279860` (Res Sq / bioRxiv 2025), "Convergent
Control of NREM Sleep and Anesthesia by Prefrontal Layer 5 Extratelencephalic Neurons."

**RE-SCOPED EXPERIMENT.** An immediate-early-gene-captured ensemble is not a cell type — it is
whatever was metabolically active under the drug. The residue is the cell-type-specific test:

> In mouse, chemogenetically or optogenetically **activate** the parafacial-zone GABAergic population
> whose **ablation** already confers durable resistance to isoflurane and sevoflurane hypnosis
> (PMID:40240218), and score the resulting state on all three frozen axes independently — `A_beh`
> (righting **and** immobility, kept separate per the EAAT3 dissociation), `A_neu` (EEG signature),
> `A_met`.

**Why this node.** The ablation arm is done and is strong (dose-graded against surviving neuron
count). The sufficiency arm has not been run. The same paper shows the behavioural and EEG endpoints
already dissociate for this population, so the three-axis scoring is not decorative.

**Either outcome is publishable.** A positive is the first `PRODUCES_STATE` entry in any anaesthesia
row. A negative, added to PMID:41573848, converts D2 from a literature-shape claim into a biological
one: the anaesthetised state may not be producible from within, and that would be a real dissociation
from sleep.

---

## PE-B — Accelerate exit from natural sleep at fixed sleep pressure

**Gap.** Zero `ENABLES_EXIT` across five endogenous rows and 35 populated cells, against five in the
anaesthesia rows. Claim D2, complementary half.

**HAS THIS ALREADY BEEN DONE? — NOT IN THE FORM THAT DISCRIMINATES.** Arousal from sleep has been
driven optogenetically many times, and caffeine's effect on sleep EEG is heavily studied. What is
absent is the controlled comparison: exit latency **at matched homeostatic drive**, so that "woke up
sooner" cannot be explained by "had less sleep pressure."

**Experiment.** The human anaesthesia caffeine study (PMID:30044241) is the exact template and the
reason it worked is the control: emergence occurred at a **higher** expired isoflurane concentration,
which excludes faster washout. The sleep analogue:

> Deliver an arousal-promoting manipulation during established NREM at a **quantified** sleep-pressure
> level (delta power, or time since deprivation), and measure exit latency against a matched-pressure
> control. The discriminating readout is exit at matched drive, not exit per se.

**Why it matters beyond bookkeeping.** If nothing accelerates exit from sleep at fixed pressure while
several agents accelerate emergence from anaesthesia, the two states differ in how they are
terminated, not only in how they are entered — and the `ENABLES_EXIT` zero becomes biology rather than
a fact about the question set.

---

## PE-C — Ask a channel question of cryptobiosis

**Gap.** Nine of twelve classes empty in `S8_crypto_cele`, at recall 1.00. Claim I1: the classes
interrogated track the discipline, not the biology.

**HAS THIS ALREADY BEEN DONE? — NO. ZERO HITS.** The query
`(nematode OR C. elegans OR tardigrade) AND (anhydrobiosis OR desiccation OR cryptobiosis) AND (gap
junction OR innexin OR electrical coupling OR connexin OR pannexin)` returns **nothing**.

**Experiment.**

> Does electrical coupling remodel during anhydrobiotic entry in *C. elegans* dauer larvae?

**Why this is the right first channel question.** The two literatures are already adjacent and have
never been joined: dauer-specific innexin remodelling is a scored positive in this table
(`S7_dauer_cele` c12), and desiccation is imposed on dauers, so the preparation exists. It is
cheap, it is in a tractable organism, and a positive would be the first non-biochemical mechanism
recorded for any cryptobiotic state.

---

## PE-D — Prospective human complex I anaesthetic risk

**Basis.** Three species, three complex I subunits, one direction (§8 of the final report), with a
clean and clinically actionable agent dissociation: volatile agents yes, intravenous no.

**HAS THIS ALREADY BEEN DONE? — NO. The human arm is observational only.** `PMID:42117732`
(Anesthesiology 2026) is seven patients plus fibroblast and cybrid work. No prospective cohort,
registry or guideline study was found.

**Experiment.** A prospective genotype-stratified perioperative cohort: mtDNA haplotype and nuclear
complex I variant status against anaesthetic requirement and perioperative neurologic outcome,
stratified by volatile versus total intravenous anaesthesia.

**A named intervention already exists**, which is unusual for a proposal at this stage: in the mouse
Leigh model the isoflurane toxicity is macrophage-dependent and is rescued by the CSF1R inhibitor
pexidartinib (PMID:37770252). The same paper also shows the routine 100% O₂ carrier gas is itself
harmful — a laboratory convention confounding the measurement.

---

## PE-3b — RIS necessity under worm volatile anaesthesia  **[CHEAPEST DECISIVE TEST IN THE SET]**

**HAS THIS ALREADY BEEN DONE? — NO. ZERO HITS.** The query
`(C. elegans) AND (RIS OR aptf-1 OR flp-11) AND (isoflurane OR halothane OR anesthetic) AND (ablation
OR mutant OR required)` returns **nothing**.

**Why it is still open and still matters.** `S5_ga_volatile_cele` c7 is `TESTED_NEGATIVE` on the basis
of an **imaging** study (Chang 2025: isoflurane immobility does not recruit ALA/RIS/AVE/AVA). Absence
of recruitment is not absence of requirement. The ablation experiment — is isoflurane immobility
altered in RIS-ablated or `aptf-1` animals? — has never been run, and it is the direct worm analogue
of the mouse PZGABA result that is the single most informative finding of this run.

---

## PE-2 — Energetic demand during maintained anaesthesia by complex I genotype

**HAS THIS ALREADY BEEN DONE? — NO, THOUGH THE SURROUNDING GROUND IS WELL COVERED.** Isoflurane
inhibition of complex I is established in vitro and ex vivo (`PMID:29661379`, `41417580`,
`36385685`), and the Leigh model's hyperoxia sensitivity is mapped (`PMID:31402314`). The specific
measurement — **whole-animal energetic demand during maintained anaesthesia, compared by complex I
genotype** — was not found.

**Status: OPEN.** Directly tests claim G4 and is the only current bridge from the mechanism table to
the σ_EP strand of the wider program.

---

## PE-4 — Presynaptic-release knock-in mouse, MAC and loss of righting

**HAS THIS ALREADY BEEN DONE? — NO.** Query returned nothing on point.

**Status: OPEN, and better motivated than before.** Class 5 now carries two independent mouse results
with a sharp dissociation — the N-type Ca²⁺ channel knockout is *more* halothane-sensitive and *less*
propofol-sensitive (PMID:12962913), and the Ndufs4 effect routes through presynaptic excitatory
transmission (PMID:27498564). A syntaxin-1A or SNAP-25 knock-in would test whether the release step
itself, rather than calcium entry into it, sets potency.

---

## PE-6 — Mouse propofol row

**Status: COMMITTED, UNSCORED.** Now clearly justified: three separate mouse studies scored this run
report propofol arms alongside volatile arms (Ndufs4, connexin36, N-type Ca²⁺), and in two of them
propofol behaves *differently* from the volatiles. Those data are currently recorded only as scope
notes inside volatile-row cells, which is the wrong place for them.

---

## PE-7 — Thermal axis amendment, then torpor / hibernation

**Status: the case is now strong enough to act on.** Class 11 carries both causal directions (§15) and
neither the DMH result nor the anaesthetic-thermoregulation result can be given a role, because no
axis can hold "body temperature changed." **`A_therm` is the best-supported outstanding amendment in
the project.** Scoring hibernation without it would immediately produce role-less mechanisms.

**Hibernation is also the state most likely to break the headline claim** (§21 of the final report):
it is the one endogenous state where an animal does something anaesthesia-like on purpose, and it is
committed but unscored.

---

## PE-8 — Neural irreversibility across states

**Status: unchanged. The instrument verdict stands.** The gate executed on 38 Atanas animals and
failed. That is a statement about the estimator at that sample size, not about the direction, and it
is recorded as such in `irreversibility_gate_result.json`.

---

## PE-9 — Inter-rater reliability on role assignment  *(new, procedural)*

**The most obvious reviewer objection to the headline claim, and it is unmeasured.** Role assignment
is interpretive; two careful scorers could plausibly differ on `CONTROLS_ENTRY` versus
`MAINTAINS_STATE` in perhaps a fifth of cells.

**Proposal.** Have a second scorer independently assign roles to a random 30 populated cells from the
raw perturbation statements alone, blind to the current assignment, and report Cohen's κ.

**Prediction, stated in advance:** κ will be moderate on the entry/maintenance boundary and high on
`PRODUCES_STATE`, because production requires an explicit sufficiency or abolition demonstration.
**The headline claim is robust either way**, since no plausible re-reading turns an anaesthesia cell
into `PRODUCES_STATE` — no experiment in those rows produced the state without the drug.

---

## PE-10 — Class 1–4 coarsening re-score  *(mandated, never run)*

Required by `INCLUSION_CRITERION.md` §6. Until it is run, the boundaries between cation-leak
reduction, K⁺ conductance increase, Cl⁻ shunt and excitatory-receptor block are a scorer's judgement.
**This is the largest known methodological debt in the project** and it is purely computational —
no new data, no collaborator, no wet lab.
