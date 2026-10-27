# Two uncontrolled confounds in brain-state irreversibility measurement

**Date:** 2026-09-21 · `filter_floor_experiment.py` · `FILTER_FLOOR_RESULT.json`
Estimator imported unchanged from `irreversibility_gate.py`.

---

## 1. The target

A live literature orders brain states by coarse-grained temporal irreversibility and reads the
ordering as non-equilibrium dissipation — wake > sleep > anaesthesia > disorders of consciousness:

| PMID | venue | claim |
|---|---|---|
| 34412335 | Phys Rev E 2021 | "Nonequilibrium brain dynamics as a signature of consciousness" |
| 35688893 | Commun Biol 2022 | INSIDEOUT — intrinsic/extrinsic balance from asymmetry |
| 35512291 | Cereb Cortex 2023 | irreversibility decoded from primate ECoG; wake > sleep, wake > ketamine |
| 36932548 | Phys Rev E 2023 | EP of multivariate OU "correlates with consciousness levels" |
| 39414871 | Sci Rep 2024 | temporal asymmetry of cortical dynamics as a brain-state signature |
| 42541725 | **Cell Rep 2026** | "Thermodynamics of consciousness" — FDT violations fall in anaesthesia and DoC |

This is the same ordering this project arrived at independently as a physical intuition. The
question here is not whether the ordering is real. It is whether the instrument can see it.

## 2. Design

Latent processes with analytically known ground truth, then measured with the *same* estimator
(PCA → 2 PCs, 4 quantile bins/PC, first-order transitions, nats/frame).

- **Reversible** (true σ_EP = 0 exactly): independent 1-D Ornstein–Uhlenbeck processes; a 1-D OU at
  stationarity satisfies detailed balance, independent components are jointly reversible, any linear
  mixture is a stationary Gaussian process with symmetric autocovariance, and quantile binning is a
  lumping that preserves reversibility. Also: symmetric-kernel-smoothed white noise.
- **Reversible, event-like**: Poisson shot noise. A Poisson process reversed is a Poisson process.
- **Irreversible positive control** (true σ_EP > 0): 2-D OU with non-symmetric drift
  `[[-1,-w],[w,-1]]`, whose rotational steady-state current breaks detailed balance.
- **Filters**: none · causal GCaMP6s double-exponential · canonical SPM double-gamma HRF ·
  the same GCaMP kernel **time-symmetrised and applied zero-phase**, matched in smoothing
  bandwidth. That last one is the control that separates kernel *asymmetry* from kernel *smoothing*.

24 realisations per condition.

## 3. The hypothesis I went in with was falsified

**Predicted:** a causal asymmetric filter manufactures irreversibility from a reversible source.

**Found:** on a smooth reversible latent, causal filtering does not raise σ̂ — it *lowers* it.

| | unfiltered | symmetric | causal GCaMP | causal HRF |
|---|---|---|---|---|
| reversible OU, σ_EP = 0 | 0.0367 | 0.0176 | 0.0162 | 0.0180 |

Smoothing of any kind reduces the estimate. Filter asymmetry is not the dominant term here.
Recorded as falsified rather than quietly dropped.

## 4. What is actually going on — confound 1, and it is the bigger one

**Finite-sample bias that scales with the latent timescale.** On a provably reversible source,
unfiltered, true σ_EP = 0 at every row:

| latent timescale | σ̂ |
|---|---|
| fast (wake-like) | **0.1286** |
| medium | 0.0367 |
| slow (anaesthesia-like) | 0.0145 |
| very slow (burst-suppression-like) | **0.0075** |

**17.2× across the range, with zero real dissipation at both ends.**

Confirmed as finite-sample by a length sweep on the same zero-truth source: σ̂ falls monotonically
0.0466 → 0.0138 from T = 400 to T = 12,800 frames.

Anaesthesia and deep sleep unambiguously slow neural dynamics. **This confound therefore has the
same sign as every published wake > anaesthesia result, and is large.**

## 5. Confound 2 — opposite sign

In the **event-like** regime (Poisson latent, reversible), causal filtering *does* dominate, and
this is where the project's 38-animal indicator control sat:

| event rate | unfiltered | symmetric | causal GCaMP |
|---|---|---|---|
| 0.20 Hz | 0.1478 | 0.0425 | 0.0705 |
| 0.05 Hz (gate-matched) | 0.0649 | 0.0418 | **0.1303** |
| 0.02 Hz | 0.0057 | 0.0381 | **0.1757** |

Causal ≫ symmetric confirms asymmetry is the operative term. But σ̂ rises as event rate *falls* —
isolated transients are maximally asymmetric, overlapping ones smear. Anaesthesia lowers event
rate, so **this confound inflates the anaesthetised state: the opposite direction.**

**The two confounds compete rather than add.**

## 6. Controls that did pass

- **Estimator positive control:** rotational OU (true σ_EP > 0) reads 0.2864, ~7.8× the reversible
  floor. The estimator does detect real irreversibility when it is there.
- **Reconciliation with real data:** real worm σ̂ = 0.0133 (38 animals, `irreversibility_gate.py`).
  A reversible OU at medium timescale under a causal GCaMP kernel reads 0.0162. **The real
  recordings sit inside the range a zero-dissipation process produces under this estimator** — which
  is what that gate's FAIL verdict was detecting, now with a mechanism.

## 7. The claim, stated narrowly

Not "the published results are wrong." The defensible claim is:

> This estimator family has a documented, sign-known, uncontrolled dependence on exactly the signal
> properties that *define* the states being compared — dominant timescale and event rate. Two
> confounds of opposite sign are present. No study in the target list reports either of the two
> controls that would separate confound from effect: a **timescale-matched reversible surrogate**,
> and a **symmetric-filter comparison**.

## 8. Scope and limits, stated plainly

- Everything here is simulation. It establishes that the confounds exist and their sign and scale
  under this estimator; it does **not** measure how large they are in any published dataset.
- The real-data arm is calcium imaging in *C. elegans*, awake only — a different modality from the
  BOLD/EEG/ECoG the target papers use.
- Estimator variants differ. Deep-learning decoders (35512291) and FDT-violation measures (42541725)
  are not the binned KL rate used here, and the transfer is an argument, not a measurement.
- A 30-year-old precedent makes the same argument form against chaos metrics in EEG and should be
  cited rather than ignored: **PMID 8983161** (Biol Cybern 1996) — EEG temporal asymmetry attributed
  to nonstationarity, cycles and randomness, with an explicit critique of dimension-based algorithms.

## 9. Next move, and it is cheap

Run both controls on the public data the published claims already use. No wet lab, no new
acquisition. If the published effects survive a timescale-matched reversible surrogate, that is a
service to the field and still worth reporting. If they do not, it is a correction.
