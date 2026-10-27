# Thermodynamic bridge memo

**Date:** 2026-09-17. Covers Branch O (mechanism → physics) and Branch Q (what the irreversibility
estimator is and is not).

---

## Part 1 — Branch Q: what a forward/reverse KL rate actually is

The project has repeatedly been tempted by the identification

> neural temporal irreversibility = physical entropy production.

This is the audit of that identification. **It does not hold in the form the project would need.**

### 1.1 The one true statement

For a **Markov jump process on the true microstates**, at **stationarity**, with each transition
`i→j` having a physical reverse `j→i`, the Schnakenberg entropy production rate is

```
    σ_EP = k_B · Σ_ij  J_ij · ln( w_ij p_i / w_ji p_j )        [J K⁻¹ s⁻¹]
```

and the dimensionless quantity we can estimate from data,

```
    σ̂ = Σ_ij  p_ij · ln( p_ij / p_ji )                          [nats per transition]
```

relates to it by `σ_EP = k_B · σ̂ / Δt` **only under all of the following**:

1. **Markov on the observed variable.** The coarse-grained state must itself be Markov.
2. **Stationarity.**
3. **Microscopic reversibility of the observable** — every observed forward transition has an
   observable reverse.
4. **The coarse-graining is a lumping that preserves the transition structure.**
5. **No hidden driving** that injects asymmetry not attributable to the system's own dissipation.

### 1.2 Which of these fail for calcium imaging of a nervous system

| assumption | status for whole-brain GCaMP | consequence |
|---|---|---|
| Markov on observed state | **fails.** Calcium is a slow low-pass filter of voltage; the indicator carries its own memory (τ_decay ≈ 1–2 s ≫ frame interval) | observed process is non-Markov; σ̂ is not the EP of a Markov chain |
| stationarity | **fails in general.** Behaving animals switch states | σ̂ picks up non-stationarity as asymmetry |
| reversibility of observable | **fails structurally.** GCaMP rise ≠ decay. Every transient is asymmetric *by construction* | asymmetry exists with zero neural dissipation difference |
| lumping preserves structure | **fails.** PCA + binning is not a lumping | coarse-graining can create *or* destroy apparent asymmetry |
| no hidden drive | **fails.** Sensory input, motor feedback | external work appears as internal dissipation |

### 1.3 What survives

**Only the inequality, and only in a restricted sense.** Coarse-graining a genuinely Markov process
can only *reduce* measured EP, giving `σ̂_observed ≤ σ_EP` — the standard lower-bound statement. But
that bound requires the observed process to be a coarse-graining *of* the dissipative process, which
the indicator kinetics break: **the indicator adds asymmetry that is not a coarse-graining of neural
dissipation at all.** With an additive non-neural asymmetry term the inequality is no longer signed.

**Therefore:** σ̂ from calcium imaging is a *statistic of the observed dynamics with units of
nats/frame*. It is not entropy production, not a bound on entropy production, and not convertible to
W/K without a biophysical model that is not currently in hand.

### 1.4 What would be needed to make the claim

1. A measurement whose forward/reverse asymmetry is not dominated by indicator kinetics — voltage
   imaging with symmetric kinetics, or electrophysiology, or deconvolved event trains with the
   deconvolution error characterised.
2. A demonstration that the coarse-grained variable is approximately Markov at the chosen Δt.
3. A biophysical model converting coarse-grained transitions into ion fluxes and pump turnover, which
   is where physical units enter (`σ = Σ J_ion·(V−E_ion)·zF` plus ATP hydrolysis per pump cycle).
4. Stationary epochs, or an explicitly non-stationary formalism.

**Until (1)–(4), the correct language is "temporal irreversibility of the recorded signal", and the
project should not write "entropy production" in a manuscript.**

### 1.5 Consequence for the empirical gate

This is why the indicator-floor test (Branch P, `irreversibility_gate.py`) is a *gate* and not a
result: it asks only whether the statistic carries any information beyond the sensor. Even a clean
PASS would license "the recorded dynamics are more time-asymmetric than indicator kinetics alone
explain" — nothing thermodynamic.

---

## Part 2 — Branch O: mechanism → proximal physics → measurable quantity

53 scored mechanisms now carry a `proximal_physical_effect` annotation
(`physical_effect_matrix.csv`). Below, each mechanism family is classified by whether its physics is
direct enough to sign an energetic consequence.

**Categories used:** `SIGN_DERIVABLE` (physics fixes the sign given stated assumptions) ·
`SIGN_AMBIGUOUS` (competing terms) · `NO_DIRECT_ENERGETIC_INFERENCE`.

### O1 — NALCN / cation leak → `SIGN_DERIVABLE` (for the pump-load term only)

Chain: NALCN conductance → resting Na⁺ influx → Na⁺/K⁺-ATPase turnover → ATP hydrolysis.

At steady state the pump must extrude the Na⁺ that leaks in, so pump turnover ∝ Na⁺ influx, and ATP
cost per Na⁺ is fixed (3 Na⁺ per ATP). **Reducing Na⁺ leak reduces resting pump ATP demand. The sign
of this term is unambiguous.**

**Three caveats that stop it being a whole-cell claim.** (i) It signs the *resting leak* term only,
not total cellular ATP demand. (ii) Hyperpolarisation *increases* the electrochemical driving force on
Na⁺, partially opposing the conductance reduction — the net flux change requires the actual V_m and
E_Na. (iii) Changed excitability changes spiking and synaptic cost, which can dominate.

**Critically, the map now shows why presence cannot be used to sign anything:** NALCN appears in four
states with three different role/polarity combinations. *Direction of the manipulation*, not
involvement, sets the energetic sign.

### O2 — K⁺ conductance → `SIGN_AMBIGUOUS`

Increasing g_K hyperpolarises toward E_K, which *reduces* the K⁺ driving force even as conductance
rises; the product J_K·(V−E_K) can move either way. Meanwhile hyperpolarisation reduces spiking
(lowering cost) but increases Na⁺ driving force (raising leak influx).

**Do not assume "more K⁺ conductance = less energy."** The project's own data reinforce this: the
mouse K⁺ current is *downstream of complex I inhibition*, so its energetic consequence is entangled
with a supply-side change.

### O3 — Synaptic release / SNARE → `SIGN_DERIVABLE` (reduced synaptic cost) but **compartment-specific**

Vesicle cycling, transmitter loading and postsynaptic current reversal are major ATP consumers.
Reducing release probability reduces this cost. **But it barely touches resting pump load**, which is
set by leak. So a release-machinery manipulation should reduce *activity-dependent* energy use while
leaving resting demand near-unchanged — a **dissociation the map can exploit**: NALCN and SNARE act
on different energetic compartments.

### O4 — Mitochondrial complex I → **supply, not demand.** `NO_DIRECT_ENERGETIC_INFERENCE` for demand

`Ndufs4` changes respiratory *capacity*. Capacity, realised flux, and demand are three different
things. A capacity reduction may produce: unchanged flux with reduced reserve; reduced flux with
compensation; or reduced ATP with downstream consequences. **The sign of *demand* cannot be inferred
from a capacity lesion.** This is precisely why PE-2 exists.

The `Ndufs4` → K⁺ leak → hyperpolarisation chain is a *demand-side* consequence of a *supply-side*
lesion, which is what makes this pair the most informative available intervention: **complex I and
NALCN perturb opposite sides of the same ledger.**

### O5 — Temperature → `SIGN_DERIVABLE`, and the strongest physics in the project

All rate constants scale with temperature (Q₁₀ ≈ 2–3 for enzymatic processes). Lower T lowers pump
turnover, channel kinetics, metabolic rate, and hence dissipation, with a known functional form.

**And the empirical result is unusually clean:** MAC falls rectilinearly with temperature and at
≈20 °C no isoflurane is required at all (Antognini 1993, goats). Temperature is not a modulator of
the anaesthetic state — **at sufficient depth it substitutes for it.** Any energetic ordering of
reduced-activity states that does not control temperature is partly measuring a thermostat.

### O6 — Structural/protective (trehalose, vitrification) → `NO_DIRECT_ENERGETIC_INFERENCE`

These act on survival through a state whose energetics are set by water availability, not by the
protective machinery. Cryptobiosis energetics are governed by the imposed physical condition.

### Summary table

| mechanism family | proximal physics | energetic sign |
|---|---|---|
| NALCN / cation leak | Na⁺ leak → pump turnover | `SIGN_DERIVABLE` (resting term) |
| K⁺ conductance | g_K ↑, driving force ↓ | `SIGN_AMBIGUOUS` |
| Cl⁻ / shunt | shunt conductance | `SIGN_AMBIGUOUS` |
| SNARE / release | vesicle cycling cost | `SIGN_DERIVABLE`, synaptic compartment only |
| complex I | ETC capacity (supply) | `NO_DIRECT_ENERGETIC_INFERENCE` for demand |
| circuit / neuromodulator | network firing | `NO_DIRECT_ENERGETIC_INFERENCE` |
| temperature | Q₁₀ on all rates | `SIGN_DERIVABLE` |
| structural / protective | none during the state | `NO_DIRECT_ENERGETIC_INFERENCE` |

---

## Part 3 — What should actually be measured

**The single best experiment remains PE-2**, now sharper. Measure, in WT vs `Ndufs4` vs `NDi1`,
during *maintained* isoflurane at matched MAC-multiples **and matched core temperature**:

1. **CMRO₂** — mouse-feasible by noncontrast MRI (Wei 2024 did it in WT under graded isoflurane and
   found dose-dependent suppression). Closest available proxy for realised metabolic flux.
2. **ATP / ADP:ATP** by genetically encoded sensor — separates demand from supply.
3. **NADH/FAD redox** — reports ETC operating point directly.
4. **Whole-organism indirect calorimetry** — the only true whole-body dissipation measure, and the
   only one convertible toward W.

**Matched temperature is non-negotiable** (Part 2, O5), and **matched MAC-multiple rather than matched
%** is required because the genotypes differ in MAC by up to two-fold — comparing at equal delivered
concentration would compare different anaesthetic depths.

### What each measurement would and would not license

| measurement | licenses | does NOT license |
|---|---|---|
| CMRO₂ | brain O₂ consumption rate changed | whole-body dissipation; entropy production |
| ATP/ADP | demand-supply balance shifted | absolute ATP turnover |
| NADH/FAD | ETC operating point moved | flux magnitude |
| calorimetry | whole-organism heat output, → W | *neural* dissipation specifically |
| σ̂ from imaging | recorded dynamics more/less time-asymmetric | anything thermodynamic (Part 1) |

**None of these, alone or together, yields physical entropy production of the nervous system.** The
honest target is **metabolic rate and its compartmental allocation**, which is a real physical
quantity, measurable, and sufficient for every comparative claim the project actually needs.

---

## Part 4 — Bottom line

1. The forward/reverse KL statistic is **not** entropy production and should not be called it.
2. Of eight mechanism families, **three** have derivable energetic signs (cation leak, release
   machinery, temperature); one is explicitly supply-side (complex I); four are ambiguous or
   non-inferential.
3. **Mechanism presence never signs an energetic consequence** — NALCN in four states with three
   role/polarity combinations is the proof.
4. The original monotone ladder is **not** recoverable from mechanism data. What replaces it is a
   **two-sided ledger** — supply (complex I, temperature) versus demand (leak, release, firing) —
   with states occupying different positions on *both*, not one scalar.
5. Temperature is not a confound to control away. It is a **first-class axis**: at 20 °C it replaces
   the anaesthetic entirely.
