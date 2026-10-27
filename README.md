# anesthesia-pipeline

Code and result files for my work on anesthesia as a reduced-activity state. The main piece is a
network-state validator: literature Hill curves for each anesthetic's targets are applied to a
spiking network, and a single scalar fitted on halothane predicts the held-out isoflurane EC50
within 1.002x in worm, 1.11x in fly larva and 1.06x in mouse, where a Meyer-Overton baseline
calibrated the same way is about 2.9x off in all three. Alongside it are a literature map of
mechanisms across 12 reduced-activity states (144 cells, 162 PubMed-verified sources) and an audit
of the irreversibility estimator used to compare brain states.

Project page: https://www.rohitravi.com/projects/anesthesia-pipeline

## Results

### 1. Held-out EC50 prediction (worm, fly, mouse)

Each anesthetic gets a perturbation profile built from primary-literature EC50/IC50 values across
mechanism classes (GABA-A potentiation, K2P potentiation, Complex I block, SNARE cooperativity, NCA
leak block, nAChR antagonism, GluCl potentiation). The profile is applied to a Brian2 LIF network
and the readout is the quiescent fraction of the locomotion command neurons. One scalar (alpha) per
organism is fitted on wild-type halothane; nothing is refit afterwards.

| organism, substrate | halothane (calibration) | isoflurane (held out) | Meyer-Overton, isoflurane | alpha |
|---|---|---|---|---|
| worm, Cook 2019 connectome (300 neurons) | 317 uM vs 340 (1.07x) | **291 uM vs 290 (1.002x)** | 837 uM (2.89x) | 0.13 |
| fly larva, Winding 2023 connectome (2,952 neurons) | 361 uM vs 340 (1.06x) | **323 uM vs 290 (1.11x)** | 837 uM (2.89x) | 0.060 |
| mouse, random LIF graph (3,000 neurons) | 297 uM vs 350 (1.18x) | **273 uM vs 290 (1.06x)** | 862 uM (2.97x) | 0.10 |

Sources: `AnestheticSimulator/artifacts/state_validation/v3_ensemble/ec50_predictions.csv`,
`AnestheticSimulator/artifacts/state_validation_fly/v4_ensemble/ec50_predictions.csv`,
`AnestheticSimulator/artifacts/state_validation_mouse/v6_ec50_predictions.csv`,
`AnestheticSimulator/artifacts/v5_controls/control2_meyer_overton.json`.

Each prediction is a 5-seed ensemble. Bootstrap 95% intervals (`v5_controls/M5_bootstrap_CIs.json`)
are tight: worm isoflurane [276, 310] uM contains the published 290; the other wild-type intervals
sit just outside their published values (for example fly isoflurane [315, 328]).

The three Eger non-immobilizer controls (cis-1,2-dichloroethylene is an anesthetic;
trans-1,2-dichloroethylene and hexafluoroethane are not, despite Meyer-Overton-appropriate lipid
solubility) are classified correctly in all three organisms. Swapping the calibration anchor to
isoflurane returns the same alpha at grid resolution in all three organisms
(`v7_cross_cal/v7_cross_cal_verdict.json`). Under one-at-a-time +/-50% perturbation of every
parameter, the worst halothane fold-error is 1.44x (`v7_sensitivity/v7_sensitivity_verdict.json`).

### 2. Which mechanism classes are needed

I ran every non-empty subset of the mechanism classes through three staged gates (halothane, then
held-out isoflurane, then the Eger panel): 127 subsets each for worm and fly, 63 for mouse (no GluCl
ortholog). 25 subsets pass all three stages. The smallest passing subset has 5 classes in worm, 6 in
fly and 4 in mouse, and **SNARE cooperativity or Complex I block is present in 25 of 25 passing
subsets**. Source: `AnestheticSimulator/artifacts/v7_subset_search/v7_subset_verdict.json`.

### 3. Controls that narrow the claim

I ran these before writing anything up, and they set the scope of what the validator shows:

- **The operator is rank 2.** Every anesthetic and genotype profile reduces to one uniform current
  plus one global synaptic gain (max per-neuron non-uniformity 2.7e-16,
  `audits/phase0/P18-B/result.json`). The network cannot tell which targets are engaged apart from
  those two coordinates.
- **Magnitude-matched null.** Against 50 random ensembles matched on both coordinates, the
  conserved profile ranks at the 28th (worm), 26th (fly) and 38th (mouse) percentile
  (`v7_match2b/v7_match2b_verdict.json`): a modest advantage in worm and fly, marginal in mouse.
- **Cell-type targeting.** On a rank-lifted substrate using CeNGEN per-class expression, the
  conserved profile's cell-type spread sits at the 46th percentile of surrogates
  (`p1_p2/match3_worm.json`), so I found no cell-type specificity on worm.
- **Connectome permutation.** Worm halothane calibration fails under full random rewiring (6.35x)
  and degree-preserving rewiring (2.02x) but passes under a cell-type block shuffle (1.07x). The fly
  result passes on all three random graphs (`v5_controls/M2_verdict.json`).
- **Mutant direction.** A sign-only baseline with no network gets 32 of 35 mutant directions right,
  the same as the validator (`v5_controls/control1_no_integration.json`). Direction comes from the
  perturbation table, so the network's contribution is in magnitude, not sign.

### 4. Cross-state mechanism map

`cross_state_map/` is a frozen (state, species) by mechanism-class table: 12 scored rows (sleep,
volatile and propofol anesthesia, dauer, L1 arrest, cryptobiosis, seasonal hibernation and daily
torpor across worm, mouse, human and a hibernating ground squirrel) by 12 classes defined by physical action, so
144 cells. Evidence is three-valued (tested positive, tested negative, not tested) and never
collapsed to a binary. Every source in `scoring/ledger.json` (162 PMIDs) had its title fetched from
PubMed rather than recalled. Both validators exit 0 on the files in this repo.

Causal-role counts by how the state is produced (recomputed from `scoring/rows_v2/*.json`):

| state production | rows | produces | entry | maintains | protects | builds | exit |
|---|---|---|---|---|---|---|---|
| endogenous | 7 | 17 | 20 | 17 | 4 | 5 | 2 |
| physically imposed | 1 | 0 | 2 | 0 | 2 | 1 | 0 |
| exogenous agent (anesthesia) | 4 | 0 | 18 | 3 | 3 | 0 | 5 |

No mechanism in the four anesthesia rows met the map's definition of producing the state, against
17 in the endogenous rows; the mouse volatile row, which has 11 of 12 cells populated, is one of the
four. Hibernation was scored specifically to test an earlier zero in the exit column, and it broke
it (both exit entries are hibernation/torpor). The write-ups are `PE5_FINAL_REPORT.md` (10 rows),
`PE5_HIBERNATION_ADDENDUM.md` (12 rows) and `PE5_MATRICES.md`.

**Search recall.** The PubMed protocol I started with had a measured internal recall of 0.05
(2/41): E-utilities ANDs bare terms, so concatenated multi-concept queries required every word, and
the founding worm anesthesia-genetics paper returned zero hits. Rebuilding queries as boolean
OR-groups with retrieval depth treated as a measured parameter took recall to 1.00 (111/111) on the
10-row table, and 1.00 (120/120) on all 12 rows after hibernation was added. Two lessons from the
calibration: widening the vocabulary at fixed depth lowered recall, and every residual miss had to be
attributed to vocabulary or depth by a direct diagnostic before changing either.
`scoring/SEARCH_METHOD_AUDIT.md` has the curve; `scoring/PE5_RECOVERY_SUMMARY.json` has per-row
recall. This measure is the protocol's sensitivity on already-scored rows, not literature-wide recall.

### 5. Irreversibility estimator audit

Papers that rank brain states by "temporal irreversibility" use a coarse-grained forward/reverse KL
rate. On 38 awake whole-brain GCaMP recordings (Atanas et al. 2023), the real value is 0.0133
nats/frame, below a rate-matched indicator-only floor of 0.0552 and barely above phase-randomized
surrogates (0.0120); 0 of 38 animals exceed the floor (`irreversibility/irreversibility_gate_result.json`).

A simulation with known ground truth (`irreversibility/FILTER_FLOOR_RESULT.json`) shows why. On a
provably reversible process the estimator reads 0.1286 for fast dynamics and 0.0075 for very slow
dynamics, a 17x spread with zero true dissipation, and the bias shrinks with recording length.
Anesthesia slows dynamics, so this confound has the same sign as published wake > anesthesia
results. A second confound, causal indicator filtering of sparse events, runs the other way. A
rotational OU process with real broken detailed balance reads 0.2864, so the estimator does detect
genuine irreversibility. `irreversibility/IRREVERSIBILITY_CONFOUND_MEMO.md` states the claim and its
limits: this is simulation plus awake worm data, not a re-analysis of the published datasets.

## Repo layout

```
AnestheticSimulator/
  src/state_validation/   validator, organism substrates, all control and audit scripts
  data/state_validation*/ literature perturbation tables, mutant tables and EC50 anchors (worm, fly, mouse)
  artifacts/              result files: ensembles, verdict JSONs, controls (v5_*, v7_*, p*)
  audits/                 preregistrations, harnesses and results for the rank-2 and follow-up checks
scripts/brain/            worm LIF network (lif_brain.py) and connectome builder
cross_state_map/          frozen criterion, repertoire, schema, reports; scoring/ has rows, ledgers, search code, validators
irreversibility/          indicator-floor gate on real data, ground-truth simulation, memos
```

The `v7_*` result files embed the SHA-256 of the V7 preregistration they were run against. Local
absolute paths inside archived JSON were rewritten to repo-relative ones, so file hashes recorded
inside some verdicts refer to the original copies.

## How to run

Python 3.11. Install with `pip install -r requirements.txt`.

Cross-state map validators (no network access needed):

```
cd cross_state_map/scoring
python validate_v2.py
python validate_pe5_completion.py
python pe5_matrices.py        # regenerates ../PE5_MATRICES.md from rows_v2/
```

`lit.py`, `pe5_pipeline.py` and `pe5_recovery_v3.py` query NCBI E-utilities and cache responses in
`scoring/cache/` (not included).

Simulator: build the worm connectome first (needs the external files listed under Data), then run
the ensemble from its directory.

```
python scripts/brain/build_connectome_matrix.py          # writes scripts/brain/artifacts/connectome.npz
cd AnestheticSimulator/src/state_validation
python parallel_v2_ensemble.py                            # worm gates 1-4, 60 s x 5 seeds per point
python parallel_v4_fly_ensemble.py                        # fly larva
python mouse_m3_sweep_and_v6_ensemble.py                  # mouse
python v5_controls_no_integration_and_meyer_overton.py   # reads the outputs above; no simulation
```

The V7 subset search and nulls are run with `v7_orchestrator.py`. The worm ensemble is 545
simulations and stage 1 of the subset search is 12,680; both use `multiprocessing` and were run on a
single desktop.

Irreversibility: `python irreversibility/filter_floor_experiment.py` is synthetic and needs no data.
`irreversibility_gate.py` reads per-animal `.h5` extracts from `ATANAS_H5_DIR`.

## Data

Third-party data is not redistributed here. Place files under `data/external/` (paths as in the
scripts) or edit the path constants at the top of each script.

- Cook et al. 2019, *Nature*: hermaphrodite connectome, SI 5 adjacency matrices (corrected July
  2020), from the paper's supplement or wormwiring.org.
- Loer and Rand 2022, WormAtlas: neurotransmitter identity tables (`Ce_NTtables_Loer&Rand2022.xlsx`).
- CeNGEN (Taylor et al. 2021, *Cell*): neuron-class expression, cengen.org. The scripts expect a
  class-by-gene mean TPM table at `expression/cengen/derived/expression_neuron_mean.csv`.
- WormBase WS297 gene association file (`c_elegans.PRJNA13758.WS297.gene_association.wb`).
- Winding et al. 2023, *Science*: Drosophila larva connectome, Supplementary Data S1.
- Atanas et al. 2023, *Cell*: whole-brain GCaMP recordings (WormWideWeb / DANDI), used by the
  irreversibility gate and the readout check.
- Kato et al. 2015, *Cell*: whole-brain imaging with labeled states, used by the readout check.
- PubMed via NCBI E-utilities for everything in `cross_state_map/`.

Anesthetic and mutant parameters in `AnestheticSimulator/data/` carry a PMID per row; rows without a
clean primary anchor are marked `DEFERRED` rather than imputed.

## Notes

- The immobilization readout (command-neuron quiescent fraction) is a network statistic. Checked
  against held-out neural and behavioral data it did not validate as behavioral quiescence
  (`artifacts/p17_readout_validity/`), so I do not claim the simulator measures behavior.
- The mouse substrate is a generic random graph and covers immobilization only, not EEG or
  consciousness measures.
- An earlier version of this project used docking (AutoDock Vina) against predicted structures to
  get occupancies. It failed its own diagnostics and was replaced by the literature table; that code
  is not in this repo.
