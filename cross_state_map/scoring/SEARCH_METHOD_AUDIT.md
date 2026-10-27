# Search-method audit — MEASURED, v3

**Date:** 2026-09-17. Supersedes the v2 audit of the same day, which reported the protocol at
measured recall 0.56–0.90. Supersedes the 2026-09-16 version, which was qualitative.

---

## 1. The calibration curve

Internal protocol recall, measured by holding out every PMID currently load-bearing for a scored
cell and running ONLY the standardized generic battery for that row:

| protocol | depth (cele / mmus / hsap) | overall recall | rows at 1.00 |
|---|---|---|---|
| v1 — space-separated concatenation | 10 | **0.05** (2/41) | 0 |
| v2 — boolean OR-groups | 15 | 0.56 (23/41) | 0 |
| v2 — boolean OR-groups | 120 / 200 / 200 | 0.90 (71/79) | 5 of 10 |
| v3 — repaired vocabulary | 120 / 200 / 400 | 0.92 (73/79) | 6 of 10 |
| v3 — repaired vocabulary | 150 / 500 / 800 | 0.98 (103/105) | 8 of 10 |
| **v3 — repaired vocabulary** | **150 / 1200 / 1600** | **1.00 (111/111)** | **10 of 10** |

The denominator grows across rows because the battery kept finding new load-bearing papers, which
were then added to the table and became part of the next round's hold-out set. **The final figure is
not 1.00 on a fixed target; it is 1.00 on a target that grew by 170% during the calibration.**

---

## 2. What the control actually measures, and what it does not

It measures **internal protocol sensitivity**: given a row whose mechanism set is already known, how
much of that known set does the blind generic battery return. It is NOT an estimate of literature-wide
recall, and no claim of completeness follows from it. What DOES follow is narrower and is the only
thing it is used for here: **a `NOT_TESTED` cell in a row at recall 1.00 is interpretable as
"nothing found by an instrument demonstrated to retrieve what it is pointed at", whereas the same
cell at recall 0.05 was uninterpretable.** That is the entire warrant for Gate B.

---

## 3. Five failure modes, each with a measured instance

1. **Query malformation — the dominant one, and it was invisible for three working rounds.**
   eutils ANDs bare terms, so a concatenated multi-concept string demands every term appear.
   *Instance:* Sedensky 1987, the founding worm anaesthesia-genetics paper, returns **zero hits**
   under v1 and is recovered immediately under v2. **Fix:** boolean OR-groups, plus a recall control.

2. **Vocabulary gap in a class synonym list.** Seven of the eight v2 residual misses.
   *Instances:* class 6 lacked cholinesterase inhibitors, so both physostigmine papers were
   unreachable; class 6 lacked `caffeine`, so the only human ENABLES_EXIT result in the table was
   unreachable; class 7 lacked sensory-neuron terms, so the AWC/ASI dauer paper was unreachable;
   the volatile-agent group lacked `enflurane`; the REM and NREM state groups lacked bare `sleep`,
   so Funato 2016 and the galanin VLPO paper were unreachable.
   **Fix:** attribute every residual miss to a component by direct diagnostic before changing anything.

3. **Retrieval depth.** *Instance:* PMID:22540145 (CD73 knockout) matched species, state AND class
   individually but sat below rank 500 in the mouse class-6 set.

4. **Paper framed by phenotype or field rather than mechanism.** *Instance:* Funato 2016, an
   EEG-screen paper, carries both the mouse NALCN and the SIK3 results.

5. **Finding indexed by clinical endpoint or by intervention name.** *Instances:* Plourde 2003
   (BIS/ASSR) hid the human sevoflurane cholinergic reversal; Fong 2018 is indexed as *caffeine*, a
   drug name that appears in no mechanism-class vocabulary anyone would write a priori.

---

## 4. The non-obvious methodological result

**Broadening the vocabulary at fixed depth COSTS recall.** Moving from the v2 to the v3 vocabulary at
unchanged depth dropped `S5_ga_volatile_mmus` from 0.89 to 0.83: the extra OR-terms enlarge the
candidate pool, so known papers fall past the retrieval cut. Breadth and depth are coupled and must
be raised together.

The corollary bit twice, and both times the diagnostic was what settled it: **a residual miss must be
attributed to vocabulary or to depth before either is changed.** PMID:30044241 looked like a depth
problem and was not — the complete class-6 human set is 1085 records, below the 1600 cap, and the
paper is simply not in it, because its abstract says *caffeine* and never says *adenosine*. Raising
depth would have cost thousands of records and fixed nothing.

---

## 5. Mandatory protocol

1. **Boolean OR-groups only.** `(species) AND (state OR endpoint) AND (class synonyms OR'd)`.
   Never concatenate concepts.
2. **Retrieval depth is a measured parameter, not a convention.** Current calibration:
   C. elegans 150, mouse 1200, human 1600. The human anaesthesia literature is the binding
   constraint and is roughly an order of magnitude larger than the worm literatures.
3. **Five routes**, all executed, all logged per cell: class-first · molecule/system-first including
   paralogues and accessory subunits · citation-chain via `elink` in both directions ·
   negative-result · species × state × endpoint.
4. **Run the recall control before trusting any null**, and re-run it after every vocabulary or
   depth change. A protocol without a measured recall figure produces uninterpretable nulls.
5. **Attribute every residual miss by component diagnostic** (`<component> AND <pmid>[uid]`) before
   changing vocabulary or depth.
6. **Record `discovery_route` per cell** so the yield-by-route statistic keeps accumulating.

---

## 6. A caching defect found along the way

`lit.py` keyed its disk cache on Python's builtin `hash()`, which is salted per process. The cache
therefore never hit across runs and every re-run re-fetched everything. Fixed by keying on SHA-256.
Noted because it silently tripled the cost of every calibration round before it was found, and
because a cache that appears to work while never hitting is the kind of defect that survives review.
