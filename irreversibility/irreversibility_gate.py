"""BRANCH P - indicator-floor gate for coarse-grained neural irreversibility.

THE QUESTION THIS ANSWERS (and it is a gate, not a result about biology):
Does a forward-vs-reverse transition asymmetry computed on GCaMP traces exceed what the
INDICATOR KERNEL ALONE manufactures? GCaMP rises fast and decays slow, so every calcium
transient is time-asymmetric by construction, and the injected asymmetry scales with event
rate. If sigma_hat(real) is not clearly above sigma_hat(indicator-only), the measure is
reading the sensor, not the brain, and every downstream irreversibility claim is dead.

Data: Atanas 2023 freely-moving whole-brain GCaMP6s, AWAKE ONLY (38 animals on disk).
This cannot compare states - no lethargus/anaesthesia/starvation recordings are local.
It can only decide whether the instrument is usable at all.

Estimator: PCA -> 2D, quantile-binned into B bins/dim, first-order transition matrix,
sigma_hat = sum_ij p_ij * ln(p_ij / p_ji)  (Schnakenberg-style coarse-grained KL rate).
Units: nats per frame. This is a LOWER BOUND on coarse-grained entropy production of the
observed process and is NOT physical entropy production. See THERMO_BRIDGE_MEMO.md.

Controls, all rate- and length-matched:
  shuffle    : random permutation of frames        -> destroys all temporal structure
  circshift  : independent circular shift per PC   -> preserves each marginal + autocorr, breaks joint dynamics
  phaserand  : phase randomisation per PC          -> preserves power spectrum exactly, destroys higher-order structure
  indicator  : synthetic Poisson events at matched rate convolved with a GCaMP6s kernel
"""
import h5py, numpy as np, glob, json, os, sys

rng = np.random.default_rng(20260917)
# Directory of per-animal .h5 extracts (datasets 'traces' (T, N) and 'trace_timestamps') from the
# Atanas et al. 2023 NWB files. Set ATANAS_H5_DIR or place them in data/external/atanas2023_h5/.
DATA_DIR = os.environ.get('ATANAS_H5_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'external', 'atanas2023_h5'))
FILES = sorted(glob.glob(os.path.join(DATA_DIR, '*.h5')))
B = 4          # bins per PC
NPC = 2
NSUR = 20      # surrogates per animal per control


def sigma_hat(labels, nstates):
    """Coarse-grained forward/reverse KL rate, nats per transition."""
    T = np.zeros((nstates, nstates))
    np.add.at(T, (labels[:-1], labels[1:]), 1.0)
    tot = T.sum()
    if tot == 0:
        return np.nan
    P = T / tot
    s = 0.0
    for i in range(nstates):
        for j in range(nstates):
            if P[i, j] > 0 and P[j, i] > 0:
                s += P[i, j] * np.log(P[i, j] / P[j, i])
    return s


def discretize(X, b=B):
    """Quantile-bin each column independently, then combine into a joint state index."""
    lab = np.zeros(X.shape[0], dtype=int)
    for k in range(X.shape[1]):
        edges = np.quantile(X[:, k], np.linspace(0, 1, b + 1)[1:-1])
        lab = lab * b + np.digitize(X[:, k], edges)
    return lab, b ** X.shape[1]


def pca(Y, npc=NPC):
    Y = Y - Y.mean(0)
    U, S, Vt = np.linalg.svd(Y, full_matrices=False)
    return U[:, :npc] * S[:npc]


def gcamp_kernel(dt, tau_r=0.20, tau_d=1.8):
    t = np.arange(0, 10 * tau_d, dt)
    k = (1 - np.exp(-t / tau_r)) * np.exp(-t / tau_d)
    return k / k.max()


def phase_randomize(x):
    F = np.fft.rfft(x)
    ph = rng.uniform(0, 2 * np.pi, len(F))
    ph[0] = 0
    if len(x) % 2 == 0:
        ph[-1] = 0
    return np.fft.irfft(np.abs(F) * np.exp(1j * ph), n=len(x))


res = []
for f in FILES:
    with h5py.File(f, 'r') as h:
        tr = np.array(h['traces'])              # (T, N)
        ts = np.array(h['trace_timestamps'])
    if tr.shape[0] < 400:
        continue
    tr = np.nan_to_num(tr, nan=0.0)
    keep = tr.std(0) > 1e-9
    tr = tr[:, keep]
    if tr.shape[1] < 10:
        continue
    dt = float(np.median(np.diff(ts)))
    Z = (tr - tr.mean(0)) / tr.std(0)
    T, N = Z.shape

    # --- real ---
    Xr = pca(Z)
    lab, ns = discretize(Xr)
    s_real = sigma_hat(lab, ns)

    # --- surrogate controls on the same PCs ---
    s_shuf, s_circ, s_phase = [], [], []
    for _ in range(NSUR):
        Xs = Xr[rng.permutation(T)]
        l, n = discretize(Xs); s_shuf.append(sigma_hat(l, n))
        Xc = np.column_stack([np.roll(Xr[:, k], rng.integers(50, T - 50)) for k in range(Xr.shape[1])])
        l, n = discretize(Xc); s_circ.append(sigma_hat(l, n))
        Xp = np.column_stack([phase_randomize(Xr[:, k]) for k in range(Xr.shape[1])])
        l, n = discretize(Xp); s_phase.append(sigma_hat(l, n))

    # --- indicator-only synthetic, rate-matched per neuron ---
    k = gcamp_kernel(dt)
    dZ = np.diff(Z, axis=0)
    thr = 2.0 * dZ.std(0)
    rate = (dZ > thr).sum(0) / (T * dt)          # events/s per neuron, from the real data
    s_ind = []
    for _ in range(NSUR):
        syn = np.zeros((T, N))
        for j in range(N):
            lam = max(rate[j], 1e-4)
            ev = rng.poisson(lam * dt, T)
            syn[:, j] = np.convolve(ev.astype(float), k, mode='full')[:T]
        syn += rng.normal(0, 0.05, syn.shape)
        sd = syn.std(0); sd[sd < 1e-9] = 1
        Xi = pca((syn - syn.mean(0)) / sd)
        l, n = discretize(Xi); s_ind.append(sigma_hat(l, n))

    res.append(dict(animal=os.path.basename(f), T=T, N=int(N), dt=round(dt, 3),
                    sigma_real=s_real,
                    sigma_shuffle=float(np.mean(s_shuf)),
                    sigma_circshift=float(np.mean(s_circ)),
                    sigma_phaserand=float(np.mean(s_phase)),
                    sigma_indicator=float(np.mean(s_ind)),
                    sigma_indicator_sd=float(np.std(s_ind)),
                    mean_event_rate_hz=float(np.mean(rate))))
    print("%-34s T=%d N=%3d  real=%.4f  shuf=%.4f  circ=%.4f  phase=%.4f  indicator=%.4f"
          % (res[-1]['animal'][:34], T, N, s_real, res[-1]['sigma_shuffle'],
             res[-1]['sigma_circshift'], res[-1]['sigma_phaserand'], res[-1]['sigma_indicator']))

arr = {k: np.array([r[k] for r in res]) for k in
       ['sigma_real', 'sigma_shuffle', 'sigma_circshift', 'sigma_phaserand', 'sigma_indicator', 'mean_event_rate_hz']}
print("\n" + "=" * 92)
print("N animals = %d" % len(res))
for k in ['sigma_real', 'sigma_shuffle', 'sigma_circshift', 'sigma_phaserand', 'sigma_indicator']:
    print("  %-18s mean=%.4f  sd=%.4f  median=%.4f" % (k, arr[k].mean(), arr[k].std(), np.median(arr[k])))

d_ind = arr['sigma_real'] - arr['sigma_indicator']
d_ph = arr['sigma_real'] - arr['sigma_phaserand']
n_above_ind = int((d_ind > 0).sum())
n_above_ph = int((d_ph > 0).sum())
print("\n  real > indicator-floor in %d/%d animals; mean excess = %.4f (sd %.4f)"
      % (n_above_ind, len(res), d_ind.mean(), d_ind.std()))
print("  real > phase-randomised in %d/%d animals; mean excess = %.4f (sd %.4f)"
      % (n_above_ph, len(res), d_ph.mean(), d_ph.std()))
r = np.corrcoef(arr['mean_event_rate_hz'], arr['sigma_real'])[0, 1]
print("  corr(mean event rate, sigma_real) = %.3f   <-- if high, the measure largely tracks EVENT RATE" % r)

verdict = ("PASS - real exceeds the indicator floor in the large majority of animals"
           if n_above_ind >= 0.8 * len(res) and d_ind.mean() > 0 else
           "FAIL / AMBIGUOUS - real does not clearly exceed the indicator floor")
print("\n  GATE VERDICT: %s" % verdict)
json.dump(dict(per_animal=res, n=len(res),
               summary={k: dict(mean=float(arr[k].mean()), sd=float(arr[k].std()), median=float(np.median(arr[k]))) for k in arr},
               n_above_indicator=n_above_ind, n_above_phaserand=n_above_ph,
               mean_excess_over_indicator=float(d_ind.mean()),
               corr_rate_sigma=float(r), verdict=verdict,
               estimator="coarse-grained forward/reverse KL, 2 PCs, 4 quantile bins/PC, first-order transitions, nats/frame",
               caveat="AWAKE DATA ONLY. No state comparison possible with local data. Lower bound on coarse-grained EP of the observed process; NOT physical entropy production."),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'irreversibility_gate_result.json'), 'w'), indent=1)
print("\n[written: irreversibility_gate_result.json]")
