# AMENDMENTS

Append-only. One entry per post-freeze change to any hashed file.

Each entry must state: what changed, why, **what had already been scored at the time**, whether the
change was made after seeing a result, and which cells were re-scored as a consequence.

A change to a criterion, axis definition, class, row, or evidence grade requires a new versioned
file (`INCLUSION_CRITERION_v2.md`, etc.). Hashed files are never edited in place.

---

*No amendments. Criterion and repertoire frozen 2026-09-16T12:45:24Z; scoring not yet begun.*

## 2026-09-16 — Entry 1. README row-count error (unhashed file), no frozen file changed

`README.md` §Phase plan said "score the four *C. elegans* rows" while listing five instantiations in
the same sentence. The hashed `states.json` specifies **six** rows with `species: cele`
(S2_core_cele, S5_ga_volatile_cele, S6_starv_L1_cele, S6_starv_adult_cele, S7_dauer_cele,
S8_crypto_cele). The hashed file is authoritative; the README sentence was a drafting error.

Already scored at time of entry: S2_core_cele, S5_ga_volatile_cele, S6_starv_L1_cele.
Made after seeing a result: no. No hashed file altered. No cell re-scored.

## 2026-09-16 — Entry 2. S6_starv_adult_cele moved to WAITLIST on E4 failure

**What changed:** the committed row `S6_starv_adult_cele` ("adult starvation-induced sleep") is
recorded as WAITLIST / E4_fail and is not scored. Scoreable worm rows therefore number five, not six.

**Why:** systematic search returned no primary study of starvation-induced behavioural quiescence in
ADULT *C. elegans*. Every located worm starvation-sleep study concerns arrested larvae — Skora 2018
(PMID:29386137), Koutsoumparis 2023 (PMID:37682641), Wu 2018 (PMID:30416057). Queries run:
"Caenorhabditis elegans starvation sleep adult stage", "adult Caenorhabditis starvation quiescence
fasting sleep", "food deprivation quiescence adult nematode sleep", "elegans adult fasting
behavioral quiescence", "elegans sleep adult starvation RIS quiescence food". The row fails frozen
criterion E4 (no published intervention altering entry, depth, or exit) and plausibly E2.

**Provenance of the error:** this instantiation was created by the author during Step 1 and was not
checked against the literature before being frozen. It is an error in the frozen instantiation, not
a finding about worm biology.

**Adjacent state that is NOT a substitute:** satiety quiescence (post-feeding; You 2008 lineage,
Makino 2021 PMID:34335159) is a documented adult worm quiescent state, but it is a different state
and already sits on the non-committed candidate-extensions list in `states.json`. Admitting it would
require its own amendment and its own row; it is not used to fill this one.

Already scored at time of entry: S2_core_cele, S5_ga_volatile_cele, S6_starv_L1_cele.
Made after seeing a result: no — this is a state-existence finding, not a mechanism result.
No hashed file altered. No cell re-scored. Denominators for worm-level reporting use 5 scoreable rows.

## 2026-09-16 — Entry 3. v2 ontology: role axis, perturbation direction, class 12, neural sub-axes

**What changed.** A versioned successor ontology was created. **No v1 file was altered.** New files:
`REPERTOIRE_v2.md`, `SCHEMA_v2.json`, `states_v2.json`, `SHA256SUMS_v2.txt`. v1 scoring in
`scoring/rows/` is preserved; v2 scoring goes to `scoring/rows_v2/`.

**Already scored at time of entry:** all five scoreable worm rows under v1 (55 cells), audited in
`scoring/WORM_AUDIT.md`. **Made after seeing a result: YES** — this amendment is a response to the
v1 worm scoring and that is its entire justification. Every change traces to a documented v1 failure;
none was introduced to make any hypothesis look better. The classes 1–11 definitions, the entry
criterion, the three axes, the three-valued evidence logic, the evidence grades and every prohibition
are unchanged.

**Four repairs, each with its triggering failure:**

1. **Mechanism role axis** — triggered by cryptobiosis (WORM_AUDIT §E.2). v1 implicitly assumed every
   mechanism produces the suppression. In anhydrobiosis the state is physically imposed and all
   documented machinery is protective.
2. **Perturbation records + derived `state_polarity`** — triggered by the sign problem
   (WORM_AUDIT §F.1): three best-evidenced positives run opposite to naive suppression.
   `TESTED_POSITIVE` means participation and nothing more.
3. **Class 12, electrical coupling** — triggered by Bhattacharya 2019 (dauer innexin remodelling
   causally altering behaviour) being force-assigned to class 10, plus `unc-9` and UNC-1 in the
   anaesthesia row.
4. **Neural sub-measures + `measurability` + `condition`** — triggered by Awal 2020 (decorrelation
   without reduced activity) and Skora 2018 (robust while awake, downregulated only in sleep bouts).

**Role vocabulary was validated against evidence before freezing, not invented.** All 24 populated v1
mechanisms were assigned a role by hand; the vocabulary is the minimum that covered them:

- `PRODUCES_STATE` — RIS, FLP-11, NLP-22, dgk-1, innexin remodelling, sphingolipid/metabolic requirement
- `CONTROLS_ENTRY` — insulin/TGF-β (dauer), KIN-29/SIK, PVC/RIM switching RIS on, and the entire
  volatile-anaesthesia row (unc-79/unc-80, unc-64, slo-1, gas-1, stomatin, Goα/Gqα, acy-1)
- `MAINTAINS_STATE` — NALCN complex in lethargus, DAF-16 sleep homeostasis, CEPsh glia, dach-1
- `PROTECTS_THROUGH_STATE` — trehalose/IDPs in anhydrobiosis, reduced cuticle permeability in dauer
- `BUILDS_MACHINERY` — LIM-6/APTF-1 specifying RIS and FLP-11

`ENABLES_EXIT` and `PERMISSIVE_BACKGROUND` were considered and **deliberately NOT instantiated**: no
v1 cell required either. They are named as reserved so a future scorer adds them by amendment rather
than coining a synonym. Using them requires a further amendment.

**Prediction status is preserved, not rewritten.** `PREDICTIONS.md` is unchanged and remains hashed
under `SHA256SUMS.txt`. P2 partly falsified, P5 not met, P6 falsified — recorded in
`scoring/WORM_AUDIT.md` §F.6 and carried forward to the v2 audit.

**Cells expected to change under v2** (verified during re-scoring, reported in `WORM_V2_AUDIT.md`):
S7 class 10 → class 12 for the innexin mechanism; S5 class 8 gains a role-scoped negative; S2 class 3
gains an explicit ambiguity record; S8 gains `state_production: PHYSICALLY_IMPOSED` with no
`PRODUCES_STATE` role; A_neu records in S5 and S6 gain sub-measures.

## 2026-09-16 — Entry 4. v2 worm re-scoring completed

Five scoreable worm rows re-scored under v2 into `scoring/rows_v2/`; v1 rows untouched and verifying.
`validate_v2.py` exit 0. Grid 5x12 = 60 cells: 24 POSITIVE, 2 SUGGESTED, 1 TESTED_NEGATIVE,
33 NOT_TESTED. Comparative audit in `scoring/WORM_V2_AUDIT.md`.

**Scorer error caught by the validator and logged, not silently fixed:** the first v2 draft of
`S7_dauer_cele.json` omitted the class-7 cell entirely. `validate_v2.py` flagged "missing classes
[7]" and it was restored with its v1 content. Four `n_distinct_sources` values were also hand-counted
wrong and were recomputed programmatically. No evidence or interpretation was affected.

**No new literature was searched for v2.** All v2 cells derive from v1's 54-entry verified ledger.
Gene-name lookups for the CeNGEN follow-up produced no scoring.

**Reserved roles remained unused**, as required; the validator enforces this.

## 2026-09-16 — Entry 5. Mammalian v2 stress test (four rows), stopped as required

Four mammalian rows scored under v2 into `scoring/rows_v2/`: `S3_rem_mmus`, `S4_deep_mmus`,
`S5_ga_volatile_hsap` (sevoflurane), `S5_ga_propofol_hsap`. `validate_v2.py` exit 0 across all nine
scored rows (108 cells). Ledger 80 verified citations, 26 added this stage, 0 unresolved. **No frozen
file was modified.** Audit: `scoring/MAMMAL_V2_STRESS_TEST.md`. Scoring STOPPED after four rows.

**Row selection.** Species-matched pairs (mouse sleep, human anaesthesia) so the two within-domain
comparisons are not species-confounded; the cost is that the cross-domain comparison is, and it is
treated as weak.

**`state_production` provenance.** All four were assigned on 2026-09-16 in `states_v2.json` (hashed in
`SHA256SUMS_v2.txt`) BEFORE any mammalian mechanism search, satisfying the anti-post-hoc requirement.
Operational justifications and ambiguities were recorded per row at scoring time.

**Vocabulary note.** The task brief named a role `BUILDS_CAPACITY`; the frozen vocabulary is
`BUILDS_MACHINERY`. The frozen term was used. Reserved roles remained unused.

**Non-scoring annotation added.** `proximal_physical_effect` was added to mechanism records as an
explicitly non-scoring field, per the task's future-physical-bridge instruction. It carries no
thermodynamic sign and the validator ignores it.

**Two frozen rules found to be in conflict, NOT resolved here:** REPERTOIRE_v2 §3.3 (cross-species
evidence never scores a cell) and evidence grade E-F (defined as inference from another state or
another species, which would yield SUGGESTED). §3.3 was applied as the more conservative reading and
cross-species evidence scored nothing. This determines the content of whole mammalian rows and is
flagged for v3 resolution by amendment.

**Recommendation recorded:** minimal v3 (thermal phenotype axis; resolve the species-rule/E-F
conflict; `causal_status` orthogonal to evidence grade), then score `S5_ga_volatile_mmus` first to
test the method-determines-role hypothesis raised in the audit §G.

## 2026-09-16 — Entry 6. Two mammalian rows amended during the mechanism-overlap audit

**What changed.** Two cells moved from NOT_TESTED to TESTED_POSITIVE (E-A), both from Funato 2016
(PMID:27806374), an unbiased EEG/EMG-based mutagenesis screen in mice:

- `S3_rem_mmus` class 1 (cation leak): NALCN missense gain-of-function reduces REM amount and episode
  duration. Roles CONTROLS_ENTRY + MAINTAINS_STATE; polarity OPPOSES_STATE.
- `S4_deep_mmus` class 8 (mitochondrial/metabolic): SIK3 splicing mutation increases inherent sleep
  need. Role MAINTAINS_STATE; polarity PROMOTES_STATE. **Class assignment flagged as arguable** —
  class 9 is the live alternative (SIK-family kinases act via HDAC/CRTC; the worm kin-29 chain already
  records hda-4 as a class-9 upstream step). Not resolved; flagged for v3.

**Why — this is new evidence, not migration.** Both are genuine misses from the first mammalian pass.
They were found because this stage searched by CROSS-STATE MOLECULAR SYSTEM rather than by mechanism
class. The class-first protocol has a systematic blind spot for molecules whose state-relevance was
established in another state's literature. Recorded as a methodological lesson in the audit §11.

**Made after seeing a result: yes, in the sense that the cross-state question prompted the search.**
No frozen definition was altered. Row summaries recomputed programmatically; `validate_v2.py` exit 0.

**Consequence for the audit.** These two additions create the only two cross-species exact/orthologous
molecular overlaps in the table (NALCN, SIK), and the SIK one does not rest on my own orthology
inference — Funato 2016 state in the abstract that Sik3 orthologues regulate sleep in roundworms, and
the worm cell's own source describes KIN-29 as the C. elegans SIK homolog.

**Three mammalian findings identified and deliberately NOT scored**, because they are in species with
no scored row (frozen rule 3.3): Ndufs4 Complex-I anaesthetic hypersensitivity in mice; propofol's
direct inhibition of the release machinery with syntaxin md130A abolishing it (rat/PC12, Herring 2011
PMID:21173083); and TREK-1/TREK-2 knockout mice NOT resistant to halothane or isoflurane (Spencer 2023
PMID:37027798), which would be a TESTED_NEGATIVE. These are recorded in MECHANISM_OVERLAP_AUDIT.md §10
and are the reason `S5_ga_volatile_mmus` is the recommended next row.

## 2026-09-17 — Entry 7. Ontology v2.1: ENABLES_EXIT instantiated; mouse volatile row scored

**What changed.** The reserved role `ENABLES_EXIT` was instantiated. New file `states_v2_1.json`;
`states_v2.json` preserved unchanged and still hashed. `validate_v2.py` repointed to the successor.
`REPERTOIRE_v2.md`, `SCHEMA_v2.json`, `INCLUSION_CRITERION.md` and all class/axis/row definitions are
UNCHANGED. Reserved list now holds only `PERMISSIVE_BACKGROUND`.

**Why this is not a v3.** `REPERTOIRE_v2.md` §2 reserved the role precisely so a future scorer would
"add them by amendment with evidence, rather than inventing a synonym." Three cells in
`S5_ga_volatile_mmus` require it, each with induction explicitly measured and unchanged while
emergence is specifically altered:
- class 8: astrocyte-specific Ndufs4 KO — induction EC50 unchanged, emergence EC50 halved for both
  isoflurane and halothane (PMID:30707122);
- class 6: orexin neuron ablation and OX1R antagonism delay emergence without changing induction
  (PMID:18195361);
- class 11: cooling prolongs emergence 4.9→12.4 min with induction unaffected (PMID:23477964).
Scoring these as MAINTAINS_STATE would have distorted all three.

**Row scored.** `S5_ga_volatile_mmus`: 7/12 classes populated, 7 POSITIVE, 0 SUGGESTED, 0
TESTED_NEGATIVE at cell level, 5 NOT_TESTED, 15 distinct verified sources. Roles: CONTROLS_ENTRY ×3,
ENABLES_EXIT ×4. Two role-scoped negatives (TREK-1/2 for class 2; glycine α1 for class 3). One
role-less cell (class 4). `validate_v2.py` exit 0 across 10 rows. Ledger 101 verified, 0 unresolved.

**Agent specificity preserved** per the frozen agent-general instantiation: agent recorded per
perturbation (isoflurane, halothane, sevoflurane, enflurane), never collapsed.

**Discovery route recorded per cell** as methodological metadata. Class-first search would have found
2 of 7 positives and would have missed mitochondrial Complex I entirely. Second consecutive stage in
which molecule-first search recovered mechanisms class-first missed.

**Matrices regenerated from row files**, not edited by hand. Overlap re-evaluation in
`scoring/MOUSE_VOLATILE_OVERLAP_AUDIT.md`. The derived `overlap_resolution` annotation was sufficient;
no schema primitive was added.

## 2026-09-17 — Entry 8. Collaborator spec filed; pending-experiment register created

**No row, class, axis, criterion or hashed definition was changed.** No cell was scored.

Filed `collaborator_specs/NALCN_MOUSE_VOLATILE_SPEC.md` — Rohit's specification for the mouse
NALCN × volatile-anaesthesia experiment, preserved as authored (§§1–13), with a separately marked
addendum (§14) added on filing. Created `PENDING_EXPERIMENTS.md` registering PE-1 (this spec) plus
three previously identified but unregistered experiments: PE-2 energetic demand in Ndufs4/NDi1 mice,
PE-3 RIS in worm anaesthesia and dauer, PE-4 syntaxin/SNAP-25 knock-in mouse MAC.

**Substantive correction in the addendum, verified against the primary source before filing:** the
spec lists constitutive `Nalcn` as the first-priority target, but NALCN mutant mice "die within 24
hours of birth" (Lu 2007, Cell 129:371-83, PMID:17448995). A constitutive null cannot enter an adult
loss-of-righting assay. The addendum recommends the Funato 2016 Dreamless gain-of-function allele
instead — viable, adult-testable, already sleep-phenotyped, and the exact allele behind the mouse REM
cell, which converts the design from cross-species orthology to same-allele cross-state.

Three further additions: circadian control (the row already contains a circadian emergence effect,
PMID:32807382); a pre-specified MDE of >=15% EC50 shift anchored on the row's own positive control
(Ndufs4, ~2-fold) and noise floor (TREK null, ~2% at P=0.268); and recording wake state before
exposure, since the candidate genotype is defined by altered sleep.

Four citations added to the ledger (105 total, 0 unresolved): PMID:17448995, 32620897, 21040849,
19092807.

## 2026-09-17 — Entry 9. Comprehensive execution run: two cells changed, one gate executed and failed

**Cells changed (both by new evidence, not migration):**
- `S5_ga_volatile_mmus` class 1: NOT_TESTED -> TESTED_POSITIVE (E-B), Unc79/Lightweight heterozygous
  mice show an altered isoflurane response (Speca 2010, PMID:20714347). Row now 8/12. NALCN-complex
  machinery now has causal evidence in FOUR states across two species.
- `S5_ga_volatile_cele` class 7: NOT_TESTED -> TESTED_NEGATIVE (E-D), isoflurane does not recruit the
  worm sleep-atonia circuit; the ALA-AVE correlation INVERTS from -0.286 to +0.229, p=0.003
  (Chang 2025, PMID:40446059). Only the second cell-level negative in 120 cells.
- `S5_ga_volatile_mmus` A_met: NOT_YET_MEASURED -> MEASURED (E-D), mouse CMRO2 falls dose-dependently
  under isoflurane (Wei 2024, PMID:39254055), with the authors' respiration-rate caveat recorded.
- 32 mechanisms in earlier rows backfilled with `proximal_physical_effect` (non-scoring annotation).

**No frozen definition, class, criterion, axis or role vocabulary was changed.** validate_v2.py exit 0.
Ledger 115 verified citations, 0 unresolved.

**Branch P executed: indicator-floor gate FAILED.** 38 animals, awake Atanas. sigma_real 0.0133 vs
indicator-only 0.0552, real above floor in 0/38; real indistinguishable from phase-randomised surrogate
(mean excess 0.2 SD). All measured asymmetry is explained by the power spectrum. This labels the
instrument, not the biology. Claim G2 now has empirical as well as theoretical refutation; new claim
G2b added. Consequence: acquiring a state-comparison dataset would not by itself rescue the analysis.

**Thermal axis: decision taken (yes, required), amendment DRAFTED NOT IMPLEMENTED** in
COMPREHENSIVE_EXECUTION_AUDIT.md section 6. It is a criterion-level change requiring a versioned
successor and an axis re-score of every row.

**Search protocol rewritten to five routes** after Unc79 was missed by BOTH class-first and
molecule-first. PE-5 (re-search all existing rows) is now the top-ranked action in the project.

## 2026-09-17 — Entry 10. PE-5 five-route re-audit, PARTIAL

**Integrity check first:** PENDING_EXPERIMENTS.md was inspected for the suspected duplication and is
CLEAN — 9 unique PE headers, no duplicate IDs, PE-1 correctly described as re-scoped. No repair needed.

**Cells changed (all by newly discovered literature, none by re-interpretation):**
- `S5_ga_volatile_hsap` c6: SUGGESTED -> POSITIVE (E-C), role MAINTAINS_STATE. Physostigmine at
  constant end-tidal sevoflurane; 5/8 regained consciousness (Plourde 2003, PMID:14504163). Scoped:
  3/8 no change, BIS NS, authors state it is less reliable than with propofol.
- `S5_ga_volatile_hsap` c11: NOT_TESTED -> POSITIVE (E-C), role CONTROLS_ENTRY. Isoflurane MAC
  1.69/1.47/1.22% at 37/34/31 degC in children (Liu 2001, PMID:11374601). First human class-11 cell.
- `S5_ga_propofol_hsap` c6: role CONTROLS_ENTRY added alongside MAINTAINS_STATE. Physostigmine raises
  propofol induction dose 2.0->2.4 mg/kg, randomised double-blind n=40 (Fassoulaki 1997, PMID:9398952).
- `S5_ga_volatile_hsap` agent_scope widened sevoflurane-only -> agent-general, logged in-row. The frozen
  states_v2 instantiation is agent-general; the narrowing was a scoring decision and was inconsistent
  with the mouse volatile row.
- Five worm rows, class 11: applicability NOT_APPLICABLE -> APPLICABLE. Poikilothermy removes the
  regulated-thermoregulation sub-sense but NOT Q10 / temperature-mediated kinetics, which the frozen
  class-11 definition also covers. Coverage unchanged at NOT_TESTED; queries recorded in-cell.
- `S5_ga_propofol_hsap` A_neu enriched with Zelmann 2023 (PMID:37659409), a within-species
  sleep-vs-anaesthesia intracranial contrast. NOT scored as a mechanism: stimulation used as a probe.

**No frozen definition, class, criterion, axis or role vocabulary changed.** validate_v2.py exit 0.
Ledger 115 -> 120 verified citations, 0 unresolved.

**Counts:** populated 48 -> 49; POSITIVE 43 -> 45; SUGGESTED 3 -> 2; NOT_TESTED 72 -> 71.

**PE-5 IS NOT COMPLETE.** Route 4 (negative-result search) was never run systematically; the control
test was not performed; five of ten rows were not re-audited. Enumerated in FIVE_ROUTE_REAUDIT.md
sect. F. Comparative conclusions remain provisional until it is finished.

**Claim changes:** D1 (maintenance gap) WEAKENED - maintenance manipulations exist but live in macaque
and intracranial-human preparations outside the scored rows. E1 (thermal) strengthened with human
quantitative data. F1 (search bias) gains a THIRD failure mode: findings indexed by clinical endpoint
rather than mechanism.

## 2026-09-17 — Entry 11. PE-5 continuation: search protocol found defective, fixed, measured

**THE PRIMARY RESULT IS METHODOLOGICAL AND IT INVALIDATES PRIOR NULLS.** The mandatory protocol
sensitivity control (deferred twice) was executed. The query battery used in ALL prior runs has a
measured recall of 0.05 (2/41 known load-bearing papers) — 0.13 on worm volatile, 0.00 on mouse
volatile. Cause: eutils ANDs bare terms, so concatenated multi-concept queries demanded every term be
present. Sedensky 1987 returns ZERO hits under it.

Corrected protocol v2 (boolean OR-groups): recall 0.56 at depth 15; 0.93 worm volatile; 1.00 worm
lethargus at depth 100. Artefacts: scoring/pe5_search_v2.py, pe5_recovery_test.json,
pe5_recovery_test_v2.json, pe5_candidates.tsv (v1, VOID), pe5_search_log*.json.

**CONSEQUENCE: every prior "no qualifying evidence identified under the standardized search"
statement is downgraded from evidence-of-absence to NOT ADEQUATELY SEARCHED.** This includes the
mouse sleep nulls for NALCN/SNARE/complex I/gap junctions and the worm thermal nulls recorded earlier
today. The 720-query v1 sweep run at the start of this round is void.

**Cells changed (all new literature, corrected protocol):**
- S3_rem_mmus c4 NOT_TESTED -> POSITIVE (E-B), PRODUCES_STATE. GluN1 deletion in lateral preoptic
  abolishes REM generation (PMID:35649726).
- S4_deep_mmus c4 NOT_TESTED -> POSITIVE (E-B), MAINTAINS_STATE. Same deletion, same paper, NREM
  fragmented with normal total sleep. SAME MOLECULE, DIFFERENT ROLE IN TWO STATES.
- S4_deep_mmus c3 NOT_TESTED -> POSITIVE (E-B), MAINTAINS_STATE. PV-interneuron Gabrd cKO alters sleep
  EEG; viral rescue restores REM phenotype (PMID:40204438).
- S5_ga_volatile_mmus c1 second mechanism added, PROTECTS_THROUGH_STATE. Volatile anaesthetics directly
  activate NALCN conductance in retrotrapezoid nucleus; required for CO2 response during anaesthesia;
  propofol does NOT activate it (PMID:32773689). Endpoint is respiratory, not the state.
- S5_ga_volatile_hsap c11 second mechanism added, role-less. Isoflurane lowers vasoconstriction and
  shivering thresholds ~4.6 degC at 1% (PMID:8712437). Thermal coupling is BIDIRECTIONAL.

**Bug caught and fixed:** a first application pass lost all five edits because the recompute helper
re-read rows from disk before the in-memory updates were saved. Detected by direct file inspection,
re-applied via a persistent idempotent script (pe5_apply_findings.py), verified on disk.

**Counts:** populated 49->52; POSITIVE 45->48; NOT_TESTED 71->68; citations 120->127; role
assignments 57->61. No frozen definition, class, criterion, axis or role vocabulary changed.
validate_v2.py exit 0. All hashes regenerated.

**Ledgers:** PE5_EXECUTION_LEDGER.json (87 COMPLETE / 73 PENDING), PE5_CELL_LEDGER.json (48 POSITIVE,
45 NOT_TESTED_AFTER_FULL_SEARCH, 2 NEGATIVE, 2 SUGGESTED, 23 PENDING), PE5_PRE_COMPLETION_SNAPSHOT.json.

---

## Entry 12 — 2026-09-17 — PE-5 completion run: protocol v3, schema amendment, twelve new sources

### 12a. Search protocol v3 (`scoring/pe5_vocab_v3.py`)

The v2 recall control (Entry 11) raised measured internal recall 0.05 -> 0.90 and then named the
eight known papers the battery still could not reach. Each miss was attributed to a specific query
component by a direct diagnostic (`<component> AND <pmid>[uid]`), which is decisive rather than
inferential:

| PMID | row | failing component | gap |
|---|---|---|---|
| 27806374 | S3_rem_mmus | STATE | REM group lacked bare `sleep` |
| 30297727 | S4_deep_mmus | STATE | NREM group lacked bare `sleep` |
| 11020764 | S5_ga_volatile_mmus | STATE | volatile group lacked `enflurane` |
| 9398952 | S5_ga_propofol_hsap | CLASS 6 | no cholinesterase-inhibitor terms |
| 14504163 | S5_ga_volatile_hsap | CLASS 6 | no cholinesterase-inhibitor terms |
| 32807382 | S5_ga_volatile_mmus | CLASS 6 | no monoaminergic-arousal terms |
| 33712439 | S7_dauer_cele | CLASS 7 | no sensory-neuron terms |
| 11374601 | S5_ga_volatile_hsap | **none — all three matched** | **retrieval depth** |

Seven were vocabulary; one was depth. v3 repairs all eight.

**A second, non-obvious result came out of the repair.** Broadening the vocabulary at FIXED depth
*cost* recall on the two largest literatures (S5_ga_volatile_mmus 0.89 -> 0.83): extra OR-terms pull
in more records, so known papers fall past the retrieval cut. **Vocabulary breadth and retrieval
depth are coupled and must be raised together.** Depth is therefore recorded as a measured,
calibrated parameter, not a convention: cele 150 / mmus 500 / hsap 800.

**SCOPE: this changes the SEARCH INSTRUMENT only.** No frozen mechanism-class definition, criterion,
axis or role was touched. `REPERTOIRE.md`, `REPERTOIRE_v2.md` and `INCLUSION_CRITERION.md` hashes are
unchanged.

### 12b. Route 3 made real (`scoring/pe5_citation_chain.py`)

CITATION_CHAIN had been `PENDING` in every prior run because it was done by hand on a few papers.
It is now systematic: for each row, seed on that row's load-bearing PMIDs and expand one hop in both
directions via eutils `elink` (`pubmed_pubmed_citedin`, `pubmed_pubmed_refs`). All ten rows are
`COMPLETE`. The justification for keeping a citation route at all is that all four documented
failure modes of keyword retrieval are failures of VOCABULARY, and a citation edge does not depend
on vocabulary — it is the one independent check on the keyword battery.

### 12c. SCHEMA AMENDMENT — `SCHEMA_v2_2.json`, new polarity `NO_ESTABLISHED_EFFECT`

`SCHEMA_v2.json` is hash-frozen and was NOT edited; the amendment is a separate file.

The ontology already admitted `coverage = TESTED_NEGATIVE` at cell level but offered no polarity
value for the mechanism carrying the null, so a measured negative had to be written as
`UNDETERMINED` — which means something entirely different (a real effect whose direction the records
do not fix). Three tested-negative mechanisms added in this round forced the issue.

`NO_ESTABLISHED_EFFECT` is legal **only** on a mechanism whose record carries an explicit
`negative_assay_statement` or an internal positive control. Consequential rule, now enforced in
`validate_v2.py`: **the roles of a `NO_ESTABLISHED_EFFECT` mechanism are roles TESTED AND FOUND
ABSENT.** They must appear in `roles_tested_negative` and must NOT enter `roles_present` or the role
counts. Without this, a measured null would have silently inflated the role tallies — the exact
error the three-valued evidence logic exists to prevent.

### 12d. Twelve new sources, all retrieved by the corrected battery

| PMID | applied to | verdict |
|---|---|---|
| 22912761 | S5_ga_volatile_mmus c8 | Ndufs4 KO 2.5-3x hypersensitive to isoflurane/halothane, 2x propofol, **resistant to ketamine** |
| 27498564 | S5_ga_volatile_mmus c4, c8 | same lesion restricted to glutamatergic neurons recapitulates it; GABAergic and cholinergic do NOT |
| 16931982 | S5_ga_volatile_mmus c10 | **TESTED_NEGATIVE** — stomatin KO: +12% ether sensitivity, no change for halothane or isoflurane |
| 40240218 | S5_ga_volatile_mmus c7 | PZGABA ablation -> behavioural resistance to isoflurane and sevoflurane, faster emergence |
| 40240218 | S4_deep_mmus c7 | **TESTED_NEGATIVE, same animals** — no change in sleep amount or homeostatic drive |
| 33942407 | S3_rem_mmus c3, S4_deep_mmus c3 | GABA-A beta1 KO: spectral content changes, sleep amount does not (`STRUCTURE_ONLY`) |
| 25548191 | S3_rem_mmus c6 | optogenetic PPT/LDT cholinergic activation **sufficient** to induce REM; episode NUMBER up, DURATION unchanged |
| 12797957 | S3_rem_mmus c6, S4_deep_mmus c6 | OX2R vs orexin null dissociation across REM and NREM |
| 22540145 | S4_deep_mmus c6 | CD73 KO: no homeostatic NREM rebound, baseline NREM higher, IL1beta response intact |
| 37682636 | S2_core_cele c5 | dgk-1 from an unbiased forward screen; cholinergic rescue; pkc-1 counterbalance |
| 38371321 | S2_core_cele c6 | nlp-22/nlp-23 required for developmentally timed sleep, **dispensable** for stress-induced sleep |
| 33712439 | S7_dauer_cele c7 | ASI/AWC chemosensation via EXP-1 and STR-2 modulates dauer entry |
| 41279428 | S6_starv_L1_cele c9 | HLH-30/TFEB maintains L1 arrest — **PREPRINT, graded E-C on that ground, flagged for revisit** |

### 12e. The single most important result of the round, and it is a negative

**PMID:40240218.** The same neurons, the same caspase ablation, the same animals, the same paper:
**required for volatile-anaesthetic hypnosis, dispensable for the amount and homeostasis of natural
NREM sleep.** Recorded as `EXACT_MOLECULE` overlap between `S5_ga_volatile_mmus c7` (POSITIVE) and
`S4_deep_mmus c7` (the null mechanism on a cell that stays POSITIVE on other evidence).

This constrains the "anaesthesia co-opts sleep circuitry" hypothesis harder than any positive in the
table: **co-option is not symmetric.** A shared node can be load-bearing in one direction only. It
also carries an axis dissociation the authors state explicitly — the behavioural (righting) endpoint
moved, the EEG signature did not. A_beh moved, A_neu did not. A single collapsed "anaesthetic depth"
score would have erased both findings.

**SCOPE:** one node, not the circuit class. Nothing here licenses a general claim that sleep
circuitry is dispensable for NREM.

### 12f. Counts

Ledger 127 -> **137 verified citations, 0 unresolved**. `validate_v2.py` exit 0.

---

## Entry 13 — 2026-09-17 — PE-5 COMPLETION. Validator exits 0.

### 13a. Gates

`scoring/validate_pe5_completion.py` exits 0. Three gates, all ten rows:

- **Gate A** — five search routes executed per row, derived from the pipeline log and the
  citation-chain record, not asserted. CITATION_CHAIN, `PENDING` in every prior run, is now
  systematic via eutils `elink` in both directions.
- **Gate B** — 120/120 cells terminally disposed. `NOT_TESTED_AFTER_FULL_SEARCH` is accepted only
  from a row that also passes Gate C, because a null from a battery of unmeasured recall is
  uninterpretable.
- **Gate C** — measured internal retrieval recall **1.00, 111/111**, every row.

### 13b. Search protocol calibration, complete

| protocol | depth cele/mmus/hsap | recall | rows at 1.00 |
|---|---|---|---|
| v1 concatenated | 10 | 0.05 (2/41) | 0 |
| v2 boolean | 15 | 0.56 | 0 |
| v2 | 120/200/200 | 0.90 | 5 |
| v3 vocabulary | 120/200/400 | 0.92 | 6 |
| v3 | 150/500/800 | 0.98 | 8 |
| **v3** | **150/1200/1600** | **1.00 (111/111)** | **10** |

The hold-out denominator grew 41 -> 111 during calibration because the battery kept finding new
load-bearing papers which then joined the target set. **The final 1.00 is on a target that grew 170%.**

Two portable method results, both established by measurement rather than argument:
**(i)** broadening vocabulary at fixed depth COSTS recall (mouse volatile 0.89 -> 0.83); breadth and
depth are coupled. **(ii)** every residual miss must be attributed to vocabulary or depth by direct
diagnostic (`<component> AND <pmid>[uid]`) before either is changed — two misses looked identical and
were not.

Defect found and fixed: `lit.py` keyed its disk cache on Python's builtin `hash()`, which is salted
per process, so the cache never hit across runs. Now SHA-256.

### 13c. Cells changed, rounds 3-7 (21 new sources; see `pe5_apply_r2.py` ... `pe5_apply_r7.py`)

Populated 52 -> **67 of 120**. Ledger 127 -> **153 verified citations, 0 unresolved**.
Roles: CONTROLS_ENTRY 36, MAINTAINS_STATE 19, PRODUCES_STATE 16, PROTECTS_THROUGH_STATE 9,
BUILDS_MACHINERY 5, ENABLES_EXIT 5. Mechanisms recorded: 94.

New rows reaching high coverage: `S5_ga_volatile_mmus` 8/12 -> **11/12**, `S4_deep_mmus` 7/12 ->
**10/12**, `S2_core_cele` 6/12 -> **9/12**.

### 13d. SCHEMA AMENDMENT — `SCHEMA_v2_2.json`, polarity `NO_ESTABLISHED_EFFECT`

`SCHEMA_v2.json` hash unchanged; the amendment is a separate file. The ontology admitted
`coverage = TESTED_NEGATIVE` at cell level but had no polarity for the mechanism carrying the null,
forcing measured negatives to be written as `UNDETERMINED`, which means something else.

Enforced consequence: **the roles of a `NO_ESTABLISHED_EFFECT` mechanism are roles TESTED AND FOUND
ABSENT** — they belong in `roles_tested_negative` and must not enter `roles_present` or the role
counts. Without this every measured null would have silently inflated the role tallies.

### 13e. The result of the run

**No mechanism has ever been shown to PRODUCE the anaesthetised state (0 across 4 rows, 29 populated
cells), and no mechanism has ever been shown to ENABLE EXIT from an endogenous one (0 across 5 rows,
35 populated cells).** Both zeros are exact and complementary. Not a coverage artefact: the
best-scored row in the table (mouse volatile, 11/12) carries one of them.

The shape follows `state_production`, a field frozen into the schema before any of this was visible.
Falsifiable as stated: one manipulation producing anaesthesia without an anaesthetic, or accelerating
waking from natural sleep at fixed sleep pressure, breaks it.

Single most informative individual result, and it is a negative: **PMID:40240218**, parafacial GABA
ablation — required for volatile-anaesthetic hypnosis, dispensable for natural NREM amount and
homeostasis, same neurons, same animals, same paper. Co-option of sleep circuitry by anaesthesia is
**not symmetric**.

### 13f. Refusals recorded

- **PMID:42161335** (glr-5 in stress-induced sleep) NOT applied. SIS is not a committed row; scoring
  it under lethargus would be a state-substitution error.
- **PMID:27806374** (Funato 2016) NOT used to create a `TESTED_NEGATIVE` at `S4_deep_mmus` c1. Its
  "NREMS and REMS, respectively" is a dissociation by emphasis, not a measured null.
- **`PERMISSIVE_BACKGROUND`** NOT instantiated despite the best candidate yet (DMH GABAergic neurons,
  required but not sufficient). One paper is not enough to open a frozen role. Named trigger recorded.

### 13g. Deliverables

`PE5_FINAL_REPORT.md` (23 sections), `PE5_MATRICES.md` (A-E), `PE5_STRUCTURAL_ANALYSES.md`,
`scoring/SEARCH_METHOD_AUDIT.md` (v3), `scoring/PE5_CELL_LEDGER.json`,
`scoring/PE5_EXECUTION_LEDGER.json`, `scoring/PE5_RECOVERY_SUMMARY.json`,
`scoring/pe5_recovery/*.json`. `validate_v2.py` exit 0; `validate_pe5_completion.py` exit 0.

---

## Entry 14 — 2026-09-21 — Hibernation scored; coarsening run; the exit zero breaks

### 14a. Hibernation, and it did what §21 predicted

`PE5_FINAL_REPORT.md` §21 named hibernation as the state most likely to break the headline. Both
committed rows were scored under the same frozen ontology and the same v3 protocol (species group
`isp` = seasonal obligate hibernators as a clade, depth 600; `S9_hib_daily_mmus` at mouse depth).

**The production zero survives and strengthens: 0 across four anaesthesia rows, against 17 across
seven endogenous rows. The exit zero is broken: 0 -> 2, both in hibernation.**

- **PMID:11893609** — ICV prostaglandin E2 provokes arousal from an established bout, with LPS-alone
  as an internal negative control. `ENABLES_EXIT`.
- **PMID:22785425** — aminophylline into an already-torpid mouse reverses hypometabolism,
  hypothermia, bradycardia and hypoactivity; ICV but not subcutaneous 8-SPT returns animals to
  euthermia. Scored `ENABLES_EXIT` **for exact consistency with the caffeine entry at
  `S5_ga_volatile_hsap` c6** — identical pharmacology, identical delivery-during-maintained-state
  design. Scoring them differently would have preserved the zero and been indefensible.

### 14b. The replacement claim is better than the one it replaces

All seven endogenous rows share a production mode; only hibernation has an exit literature. The
discriminating variable is **cost of exit**: interbout arousals consume 60-80% of the winter energy
budget and their function is, in the source's own words, "unknown and disputed".

> **Exit is studied where exit is costly. Production is studied where production is not already
> explained by the intervention.**

This retains the literature-shape thesis and supplies a natural experiment inside it — two groups
matched on production mode, differing in exit cost, differing in exactly the predicted direction.

### 14c. An unlooked-for convergence

Two independent literatures, two sufficiency tests, same structure: **PMID:28378088** (A1 agonist
produces hypothermia that is "largely different" from torpor on six measures) and **PMID:41573848**
(ensemble reactivation produces immobility, discoordination and anti-nociception but not loss of
righting). Components of a reduced-activity state can be produced separately; producing some does
not assemble the state. Neither paper cites the other.

### 14d. Coarsening debt discharged — `COARSENING_1_4.md`

Mandated by `INCLUSION_CRITERION.md` §6 and outstanding since the freeze. Classes 1-4 merged.
Role counts, the production/exit asymmetry, all `overlap_resolution` values, P2 and the
discipline-tracking pattern are **unchanged**. Only coverage denominators move (72/144 -> 60/108,
collapsing 17 fine positives into 5). **No conclusion is reversed.** Scope: one partition choice,
the one the criterion named; the other eight boundaries remain untested and inter-rater reliability
on role assignment is now the top methodological debt.

### 14e. P2 deepens

Both hibernation rows are `NOT_TESTED` across the entire merged excitability block. Pre-registered
P2 now holds on **four** deep states, not two: the most confident claim in the dormancy literature —
that these states reduce neural excitability — is unexamined at the mechanism level in dauer,
cryptobiosis and both hibernation rows.

### 14f. Counts

12 rows · 144 cells · 72 populated · ledger 154 -> **162 verified PMIDs, 0 unresolved** ·
recall **1.00 (120/120)** on every row · both validators exit 0. Completion validator updated from
10 to 12 expected rows.

### 14g. Separately — two confounds found in the neural-irreversibility estimator

`IRREVERSIBILITY_CONFOUND_MEMO.md`, `scoring/filter_floor_experiment.py`. The prediction that a
causal asymmetric filter manufactures irreversibility was **falsified** — on smooth reversible
latents, causal filtering lowers the estimate. What was found instead: **finite-sample bias scaling
with latent timescale**, 17.2x across a plausible range on a source with true entropy production of
exactly zero, decaying with recording length; same sign as every published wake>anaesthesia result.
A second confound, causal-filter asymmetry in the event-like regime, has the **opposite** sign. The
estimator's positive control passes (~8x floor on a genuinely irreversible process). Real worm data
(0.0133) sits inside the range a zero-dissipation process produces. Claim stated narrowly: the
estimator has a sign-known uncontrolled dependence on the very signal properties that define the
states being compared, and neither required control appears in the target literature.
