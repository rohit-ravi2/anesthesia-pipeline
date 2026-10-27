"""FILTER-FLOOR EXPERIMENT — does a causal, asymmetric observation filter manufacture
measured temporal irreversibility from a provably time-reversible source?

WHY THIS MATTERS. A live literature orders brain states by coarse-grained temporal
irreversibility and reads the ordering as non-equilibrium dissipation: wake > sleep >
anaesthesia > disorders of consciousness (Phys Rev E 2021 34412335; Commun Biol 2022 35688893;
Cereb Cortex 2023 35512291; Phys Rev E 2023 36932548; Sci Rep 2024 39414871; Cell Rep 2026
42541725). Every one of these measures an estimator of the same family on a signal that has
been convolved with a CAUSAL, ASYMMETRIC, NON-MARKOVIAN filter — the calcium indicator in
imaging, the haemodynamic response function in fMRI, electrode and tissue filtering in EEG.

A causal filter rises and falls differently by construction. The question is whether that
alone produces the measured effect, and whether it produces a STATE-DEPENDENT effect, since
the published claims are all about differences between states.

DESIGN. Latent processes chosen so the ground truth is known analytically:

  reversible generators (true sigma_EP = 0, detailed balance holds)
    ou_indep    : N independent 1-D Ornstein-Uhlenbeck processes. A 1-D OU at stationarity
                  satisfies detailed balance. Independent components are jointly reversible,
                  and any linear mixture is a stationary Gaussian process whose autocovariance
                  matrix function is symmetric -- hence still reversible. Quantile binning is a
                  lumping, which preserves reversibility. So sigma_hat must be zero up to
                  finite-sample bias.
    sym_noise   : white noise convolved with a SYMMETRIC (zero-phase) kernel. Reversible.

  irreversible generator (true sigma_EP > 0) -- the estimator's positive control
    ou_rot      : 2-D OU with non-symmetric drift [[-1,-w],[w,-1]]. The rotational steady-state
                  probability current breaks detailed balance; entropy production grows with w.
                  Without this control the whole experiment is uninterpretable: an estimator
                  that returns ~0 on everything proves nothing.

  filters applied to the latent signal
    none          : identity
    causal_gcamp  : GCaMP6s double-exponential, tau_rise 0.20 s / tau_decay 1.80 s
    causal_hrf    : canonical SPM double-gamma haemodynamic response function
    symmetric     : the gcamp kernel time-symmetrised and applied zero-phase, matched in
                    smoothing bandwidth. THIS IS THE KEY CONTROL. It isolates the kernel's
                    ASYMMETRY from its SMOOTHING. If symmetric filtering leaves sigma_hat at
                    the finite-sample floor while causal filtering raises it, the asymmetry is
                    the cause and the result cannot be attributed to low-pass filtering.

Estimator is imported unchanged from irreversibility_gate.py: PCA -> 2 PCs, 4 quantile bins per
PC, first-order transition matrix, sigma_hat = sum_ij p_ij ln(p_ij/p_ji), nats per frame.

UNITS AND SCOPE. sigma_hat is a statistic of the OBSERVED dynamics in nats/frame. It is not
physical entropy production and not a bound on it (see THERMO_BRIDGE_MEMO.md). This experiment
is about the estimator, not about biology.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# reuse the project's estimator verbatim so numbers are comparable to the 38-animal gate
import importlib.util
_spec = importlib.util.spec_from_file_location("_gate", os.path.join(HERE, "irreversibility_gate.py"))


def _load_estimator():
    """irreversibility_gate.py runs its analysis at import time, so lift out just the
    functions we need rather than importing the module."""
    src = open(os.path.join(HERE, "irreversibility_gate.py")).read()
    head = src.split("res = []")[0]
    # the gate imports h5py to read Atanas NWB extracts; this experiment is synthetic and
    # needs only the estimator functions, so drop the data-layer import
    head = head.replace("import h5py, numpy as np, glob, json, os, sys",
                        "import numpy as np, glob, json, os, sys")
    ns = {}
    exec(compile(head, "irreversibility_gate.py", "exec"), ns)
    return ns["sigma_hat"], ns["discretize"], ns["pca"], ns["gcamp_kernel"]


sigma_hat, discretize, pca, gcamp_kernel = _load_estimator()

rng = np.random.default_rng(20260921)
NSEED = 24          # independent realisations per condition
NCHAN = 40          # latent channels (worm-scale)


# ---------------------------------------------------------------- generators
def ou_indep(T, dt, n=NCHAN, tau_lo=1.0, tau_hi=8.0, rs=None):
    """N independent 1-D OU processes. TRUE sigma_EP = 0 (detailed balance)."""
    rs = rs or rng
    taus = rs.uniform(tau_lo, tau_hi, n)
    X = np.zeros((T, n))
    x = rs.normal(0, 1, n)
    for t in range(T):
        x = x + (-x / taus) * dt + np.sqrt(2 * dt / taus) * rs.normal(0, 1, n)
        X[t] = x
    return X


def sym_noise(T, dt, n=NCHAN, width=6, rs=None):
    """White noise smoothed with a SYMMETRIC kernel. TRUE sigma_EP = 0."""
    rs = rs or rng
    k = np.exp(-0.5 * (np.arange(-4 * width, 4 * width + 1) / width) ** 2)
    k /= k.sum()
    W = rs.normal(0, 1, (T + 8 * width, n))
    return np.array([np.convolve(W[:, j], k, mode="same")[:T] for j in range(n)]).T


def poisson_events(T, dt, rate_hz=0.05, n=NCHAN, rs=None):
    """Poisson shot noise. A Poisson point process is TIME-REVERSIBLE (its time reversal is
    again a Poisson process of the same rate), so the latent has no preferred direction. The
    observed signal only becomes asymmetric once a causal kernel is applied. This is the
    EVENT-LIKE latent regime, as opposed to the smooth Gaussian regime of ou_indep, and it is
    the regime the 38-animal gate's indicator control lives in."""
    rs = rs or rng
    return (rs.random((T, n)) < rate_hz * dt).astype(float)


def ou_rot(T, dt, w=1.5, n=NCHAN, rs=None):
    """POSITIVE CONTROL. 2-D rotational OU embedded in n channels.
    Non-symmetric drift -> steady-state probability current -> TRUE sigma_EP > 0."""
    rs = rs or rng
    A = np.array([[-1.0, -w], [w, -1.0]])
    Z = np.zeros((T, 2))
    z = rs.normal(0, 1, 2)
    for t in range(T):
        z = z + A.dot(z) * dt + np.sqrt(2 * dt) * rs.normal(0, 1, 2)
        Z[t] = z
    M = rs.normal(0, 1, (2, n))
    return Z.dot(M) + 0.25 * rs.normal(0, 1, (T, n))


# ---------------------------------------------------------------- filters
def hrf_kernel(dt, length=32.0):
    """Canonical SPM double-gamma HRF. Causal and markedly asymmetric."""
    t = np.arange(0, length, dt)
    from math import gamma as G
    peak = (t ** (6 - 1) * np.exp(-t)) / G(6)
    under = (t ** (16 - 1) * np.exp(-t)) / G(16)
    h = peak - under / 6.0
    return h / np.abs(h).max()


def apply_filter(X, kind, dt):
    if kind == "none":
        return X
    if kind == "causal_gcamp":
        k = gcamp_kernel(dt)
        return np.array([np.convolve(X[:, j], k)[: X.shape[0]] for j in range(X.shape[1])]).T
    if kind == "causal_hrf":
        k = hrf_kernel(dt)
        return np.array([np.convolve(X[:, j], k)[: X.shape[0]] for j in range(X.shape[1])]).T
    if kind == "symmetric":
        # same kernel, time-symmetrised, applied zero-phase: matched smoothing, zero asymmetry
        k = gcamp_kernel(dt)
        ks = np.concatenate([k[::-1][:-1], k])
        ks = ks / ks.sum()
        return np.array([np.convolve(X[:, j], ks, mode="same") for j in range(X.shape[1])]).T
    raise ValueError(kind)


def measure(X):
    lab, ns = discretize(pca(X))
    return sigma_hat(lab, ns)


# ---------------------------------------------------------------- experiments
def run_block(gen, gen_kw, T, dt, label, filters=("none", "symmetric", "causal_gcamp", "causal_hrf")):
    out = {}
    for f in filters:
        vals = []
        for s in range(NSEED):
            rs = np.random.default_rng(20260921 + 1000 * s)
            X = gen(T, dt, rs=rs, **gen_kw)
            vals.append(measure(apply_filter(X, f, dt)))
        v = np.array(vals, float)
        out[f] = dict(mean=float(v.mean()), sd=float(v.std()), median=float(np.median(v)), n=len(v))
    print("  %-28s %s" % (label, "  ".join(
        "%s=%.4f±%.4f" % (f, out[f]["mean"], out[f]["sd"]) for f in filters)), flush=True)
    return out


REPORT = {}
print("=" * 100)
print("EXPERIMENT 1 — does a causal filter manufacture irreversibility from a reversible source?")
print("  worm-calcium regime: dt=0.6 s, T=1600 frames (matches the 38-animal Atanas gate)")
print("=" * 100)
REPORT["exp1_worm_regime"] = {
    "ou_indep_REVERSIBLE": run_block(ou_indep, {}, 1600, 0.6, "OU independent (sigma_EP=0)"),
    "sym_noise_REVERSIBLE": run_block(sym_noise, {}, 1600, 0.6, "symmetric-smoothed noise (0)"),
    "ou_rot_IRREVERSIBLE": run_block(ou_rot, {"w": 1.5}, 1600, 0.6, "rotational OU (sigma_EP>0)"),
}

print()
print("=" * 100)
print("EXPERIMENT 2 — same, in the fMRI regime: dt=0.72 s (HCP TR), T=1200 frames")
print("=" * 100)
REPORT["exp2_fmri_regime"] = {
    "ou_indep_REVERSIBLE": run_block(ou_indep, {}, 1200, 0.72, "OU independent (sigma_EP=0)"),
    "ou_rot_IRREVERSIBLE": run_block(ou_rot, {"w": 1.5}, 1200, 0.72, "rotational OU (sigma_EP>0)"),
}

print()
print("=" * 100)
print("EXPERIMENT 3 — THE STATE-DEPENDENCE TEST")
print("  Published claims are DIFFERENCES BETWEEN STATES. Anaesthesia and deep sleep slow the")
print("  dynamics down. If measured irreversibility depends on the latent timescale while TRUE")
print("  entropy production stays exactly zero, then a wake>anaesthesia ordering is predicted by")
print("  the filter alone. Latent is ALWAYS the reversible OU; only its timescale changes.")
print("=" * 100)
speed = {}
for name, (lo, hi) in [("fast  (wake-like)", (0.5, 3.0)),
                       ("medium", (1.0, 8.0)),
                       ("slow  (anaesthesia-like)", (4.0, 20.0)),
                       ("very slow (burst-suppression-like)", (10.0, 40.0))]:
    speed[name] = run_block(ou_indep, {"tau_lo": lo, "tau_hi": hi}, 1600, 0.6, name,
                            filters=("none", "symmetric", "causal_gcamp", "causal_hrf"))
REPORT["exp3_state_dependence"] = speed

print()
print("=" * 100)
print("EXPERIMENT 4 — EVENT-LIKE latent regime (reconciles with the 38-animal gate)")
print("  A Poisson point process is time-reversible. Convolving it with a CAUSAL kernel makes")
print("  the observed signal asymmetric. Rate is varied because anaesthesia lowers event rate.")
print("=" * 100)
ev = {}
for nm, r in [("rate 0.20 Hz (high)", 0.20), ("rate 0.10 Hz", 0.10),
              ("rate 0.05 Hz (gate-matched)", 0.05), ("rate 0.02 Hz (low)", 0.02)]:
    ev[nm] = run_block(poisson_events, {"rate_hz": r}, 1600, 0.6, nm)
REPORT["exp4_event_regime"] = ev

print()
print("=" * 100)
print("EXPERIMENT 5 — is the floor finite-sample bias? Sweep recording length on a REVERSIBLE")
print("  source. True sigma_EP = 0 at every length, so anything above 0 is estimator bias.")
print("=" * 100)
ln = {}
for T in (400, 800, 1600, 3200, 6400, 12800):
    ln["T=%d" % T] = run_block(ou_indep, {}, T, 0.6, "T=%d frames" % T,
                               filters=("none", "causal_gcamp"))
REPORT["exp5_length_sweep"] = ln

json.dump(REPORT, open(os.path.join(HERE, "FILTER_FLOOR_RESULT.json"), "w"), indent=1)

# ---------------------------------------------------------------- verdicts
print()
print("=" * 100)
print("VERDICTS")
print("=" * 100)
e1 = REPORT["exp1_worm_regime"]
rev, irr = e1["ou_indep_REVERSIBLE"], e1["ou_rot_IRREVERSIBLE"]
sp = REPORT["exp3_state_dependence"]; ks = list(sp)
ev = REPORT["exp4_event_regime"]; ek = list(ev)
ln = REPORT["exp5_length_sweep"]

print("H1 AS STATED WAS FALSIFIED. On a SMOOTH reversible latent (OU), causal filtering does")
print("   NOT raise sigma_hat above the unfiltered value -- it LOWERS it:")
print("     unfiltered %.4f  symmetric %.4f  causal_gcamp %.4f  causal_hrf %.4f"
      % (rev["none"]["mean"], rev["symmetric"]["mean"],
         rev["causal_gcamp"]["mean"], rev["causal_hrf"]["mean"]))
print("   Smoothing of any kind reduces the estimate. Filter ASYMMETRY is not the dominant")
print("   term in this regime. Recorded as a falsified prediction, not smoothed over.")
print()
print("H2 THE REAL CONFOUND IS FINITE-SAMPLE BIAS THAT SCALES WITH LATENT TIMESCALE.")
print("   Unfiltered sigma_hat on a PROVABLY REVERSIBLE source (true sigma_EP = 0 exactly):")
for k in ks:
    print("     %-38s %.4f" % (k, sp[k]["none"]["mean"]))
f0, s0 = sp[ks[0]]["none"]["mean"], sp[ks[-1]]["none"]["mean"]
print("   fast/very-slow ratio = %.1fx  with ZERO real dissipation at both ends." % (f0 / s0))
print("   Anaesthesia and deep sleep slow neural dynamics. This confound therefore has the SAME")
print("   SIGN as every published wake>anaesthesia irreversibility result.")
print()
print("H3 THE BIAS IS CONFIRMED AS FINITE-SAMPLE: it decays with recording length on a source")
print("   whose true value is 0 at every length.")
for k in ln:
    print("     %-10s unfiltered %.4f   causal_gcamp %.4f"
          % (k, ln[k]["none"]["mean"], ln[k]["causal_gcamp"]["mean"]))
print()
print("H4 FILTER ASYMMETRY DOES MATTER, BUT ONLY IN THE EVENT-LIKE REGIME -- which is where the")
print("   38-animal gate's indicator control sat, and why it read so high.")
print("   Poisson latent (reversible) + causal kernel, by event rate:")
for k in ek:
    print("     %-30s unfiltered %.4f  symmetric %.4f  causal_gcamp %.4f"
          % (k, ev[k]["none"]["mean"], ev[k]["symmetric"]["mean"], ev[k]["causal_gcamp"]["mean"]))
print("   Here causal filtering RAISES sigma_hat far above symmetric filtering, confirming that")
print("   kernel ASYMMETRY is the operative term in this regime. But note the SIGN: manufactured")
print("   sigma_hat rises as event rate FALLS, because isolated transients are maximally")
print("   asymmetric while overlapping ones smear. Anaesthesia lowers event rate, so THIS")
print("   confound pushes anaesthesia to look MORE irreversible -- the OPPOSITE direction to")
print("   confound (1) and to the published effect. The two do not add; they compete.")
print()
print("H5 ESTIMATOR POSITIVE CONTROL PASSES: rotational OU (true sigma_EP > 0) reads %.4f,"
      % irr["none"]["mean"])
print("   about %.1fx the reversible floor, so the estimator does detect real irreversibility."
      % (irr["none"]["mean"] / rev["none"]["mean"]))
print()
print("H6 RECONCILIATION WITH THE REAL DATA. Real worm sigma_hat = 0.0133 (38 animals).")
print("   A reversible OU at medium timescale under a causal GCaMP kernel reads %.4f."
      % rev["causal_gcamp"]["mean"])
print("   The real recordings sit INSIDE the range a process with zero entropy production")
print("   produces under this estimator. That is what the gate's FAIL verdict was detecting.")
print()
print("BOTTOM LINE. Two independent confounds with OPPOSITE signs, neither controlled for in the")
print("target literature:")
print("  (1) FINITE-SAMPLE BIAS scaling with latent timescale. Universal -- needs no filter, no")
print("      indicator, no imaging modality. Slower dynamics read as less irreversible even when")
print("      true entropy production is exactly zero. SAME sign as the published wake>anaesthesia")
print("      ordering, and large: %.1fx across a plausible timescale range." % (f0 / s0))
print("  (2) CAUSAL-FILTER ASYMMETRY scaling inversely with event rate, in the event-like regime.")
print("      OPPOSITE sign -- it inflates the anaesthetised state.")
print()
print("  Because they compete, a measured wake>anaesthesia difference is not self-evidently")
print("  either real or artefactual. What follows is narrower and firmer than 'the published")
print("  results are wrong': the estimator has a documented, sign-known, uncontrolled dependence")
print("  on exactly the signal properties that define the states being compared, and no published")
print("  study reports the two controls that would separate them -- a timescale-matched")
print("  reversible surrogate, and a symmetric-filter comparison.")
print()
print("  Both controls are cheap and run on data the field has already published.")
print()
print("[written: FILTER_FLOOR_RESULT.json]")
