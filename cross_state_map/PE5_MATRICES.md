# PE-5 final matrices

Generated from `rows_v2/*.json` only. Ten scored (state, species) rows x twelve frozen mechanism
classes = 120 cells.

**Read this first.** These are INCIDENCE maps over cells that have been searched to a measured
but unequal degree. A blank means the standardized battery found no qualifying evidence at the
recall recorded for that row; it does NOT mean the mechanism is absent. Prohibition 1 of
`REPERTOIRE.md` forbids computing any enrichment claim from these tables, and none is computed.

## Matrix A - coverage

| state | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 | c10 | c11 | c12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| worm lethargus     | **+** | **+** | **–** | . | **+** | **+** | **+** | **+** | **+** | . | . | **+** |
| worm L1 arrest     | **+** | . | . | . | **+** | **+** | **+** | **+** | **+** | . | . | . |
| worm dauer         | . | . | . | . | **+** | **+** | **+** | **+** | **+** | **+** | . | **+** |
| worm cryptobiosis  | . | . | . | . | . | . | . | **+** | **+** | **+** | . | . |
| mouse REM          | **+** | **+** | **+** | **+** | . | **+** | **+** | . | **+** | . | . | . |
| mouse NREM         | . | **+** | **+** | **+** | **+** | **+** | **+** | **+** | **+** | . | **+** | **+** |
| worm volatile      | **+** | **+** | . | **+** | **+** | **+** | **–** | **+** | . | **+** | . | **+** |
| mouse volatile     | **+** | **+** | **+** | **+** | **+** | **+** | **+** | **+** | . | **–** | **+** | **+** |
| human volatile     | . | . | . | . | . | **+** | . | **+** | . | . | **+** | . |
| human propofol     | . | . | . | . | . | **+** | **+** | . | . | . | . | . |

`+` tested positive - `–` tested negative - `.` not tested - `n/a` class not applicable to this state

## Matrix B - causal role

| state | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 | c10 | c11 | c12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| worm lethargus     | M | MP | (P) | . | PE | P | PEM | E | MB | . | . | PME |
| worm L1 arrest     | T | . | . | . | PT | E | P | P | MT | . | . | . |
| worm dauer         | . | . | . | . | M | E | E | E | EB | T | . | P |
| worm cryptobiosis  | . | . | . | . | . | . | . | TEB | E | T | . | . |
| mouse REM          | EM | E | PM | P | . | EP | P(P) | . | BM | . | . | . |
| mouse NREM         | . | E | M(M) | M | M | PME | P(M) | M | BM | . | PE | E(M) |
| worm volatile      | E | E | . | E | E | E | (P) | E(P) | . | E | . | E |
| mouse volatile     | ET | E(E) | E(E) | E | E | X | XE(P) | EXT | . | (E) | X | EM |
| human volatile     | . | . | . | . | . | MX | . | T | . | . | E | . |
| human propofol     | . | . | . | . | . | ME | . | . | . | . | . | . |

P produces - E controls entry - M maintains - T protects through - B builds machinery - X enables exit. Roles in parentheses were TESTED AND FOUND ABSENT.

## Matrix C - state polarity

| state | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 | c10 | c11 | c12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| worm lethargus     | ~ | + | ~ | . | + | + | +-~ | + | +s | . | . | + |
| worm L1 arrest     | - | . | . | . | +- | - | + | + | + | . | . | . |
| worm dauer         | . | . | . | . | ? | - | - | ? | + | +? | . | ? |
| worm cryptobiosis  | . | . | . | . | . | . | . | +? | ? | +? | . | . |
| mouse REM          | - | + | +s | + | . | +- | + | . | + | . | . | . |
| mouse NREM         | . | + | 0s | s | + | +- | 0~ | + | + | . | +~ | + |
| worm volatile      | -? | + | . | + | - | ~ | ? | ? | . | ? | . | ~ |
| mouse volatile     | ? | + | + | -? | ~ | - | +-0~ | +-? | . | 0 | ~ | - |
| human volatile     | . | . | . | . | . | - | . | ? | . | . | +? | . |
| human propofol     | . | . | . | . | . | - | ? | . | . | . | . | . |

`+` promotes - `–` opposes - `s` structure only - `~` context dependent - `?` undetermined - `0` measured null. Several cells carry more than one symbol because a class can hold mechanisms of opposite sign.

## Matrix E - strongest evidence grade

| state | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 | c10 | c11 | c12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| worm lethargus     | E-B | E-B | E-B | . | E-A | E-B | E-B | E-B | E-B | . | . | E-A |
| worm L1 arrest     | E-A | . | . | . | E-A | E-B | E-B | E-A | E-C | . | . | . |
| worm dauer         | . | . | . | . | E-A | E-B | E-C | E-B | E-B | E-D | . | E-B |
| worm cryptobiosis  | . | . | . | . | . | . | . | E-B | E-E | E-B | . | . |
| mouse REM          | E-A | E-C | E-B | E-B | . | E-B | E-B | . | E-B | . | . | . |
| mouse NREM         | . | E-C | E-B | E-B | E-B | E-C | E-B | E-A | E-B | . | E-B | E-B |
| worm volatile      | E-A | E-B | . | E-F | E-A | E-B | E-D | E-B | . | E-B | . | E-A |
| mouse volatile     | E-B | E-B | E-B | E-D | E-A | E-B | E-C | E-B | . | E-A | E-B | E-A |
| human volatile     | . | . | . | . | . | E-C | . | E-C | . | . | E-C | . |
| human propofol     | . | . | . | . | . | E-C | E-D | . | . | . | . | . |

E-A strongest through E-F weakest.

## Matrix D - declared cross-row mechanism correspondences

Every `overlap_resolution` recorded on any mechanism, at the resolution the scorer declared.
Resolution is recorded PER PAIR and never inferred from a shared class label.

| resolution | row / class | partner | molecule |
|---|---|---|---|
| EXACT_MOLECULE | mouse NREM c4 | (free text) | Grin1 / GluN1 |
| EXACT_MOLECULE | mouse NREM c7 | S5_ga_volatile_mmus c7 (same paper, POSITIVE) | parafacial zone GABAergic neurons (PZGABA) |
| EXACT_MOLECULE | mouse REM c4 | (free text) | Grin1 / GluN1 NMDA receptor subunit |
| EXACT_MOLECULE | mouse volatile c1 | (free text) | Nalcn (retrotrapezoid nucleus, Phox2b neurons) |
| EXACT_MOLECULE | mouse volatile c7 | S4_deep_mmus c7 (same paper, NEGATIVE) | parafacial zone GABAergic neurons (PZGABA) |
| EXACT_MOLECULE | worm lethargus c12 | S5_ga_volatile_cele c12 (unc-9) | UNC-7 and UNC-9 innexins |
| EXACT_MOLECULE | worm lethargus c2 | S5_ga_volatile_cele c2 (slo-1) | SLO-1 (BK, calcium-activated potassium channel); PCDR-1 melato |
| ORTHOLOGOUS_MOLECULE | mouse NREM c12 | S7_dauer_cele c12 / S5_ga_volatile_cele c12 (innexins) | Pannexin1 (Panx1) |
| ORTHOLOGOUS_MOLECULE | mouse NREM c9 | S2_core_cele c9 (APTF-1) | Tfap2b (AP-2beta) |
| ORTHOLOGOUS_MOLECULE | mouse REM c9 | S2_core_cele c9 (APTF-1) | Tfap2b (AP-2beta) |
| ORTHOLOGOUS_MOLECULE | mouse volatile c10 | S5_ga_volatile_cele (unc-1) | Stomatin (Stom) |
| SAME_COMPLEX | human volatile c8 | S5_ga_volatile_cele c8 (gas-1); S5_ga_volatile_mmus c8 (Ndufs4) | MT-ND4 (complex I subunit), m.11232T>C / L158P |
| SAME_PATHWAY_MODULE | mouse volatile c5 | S5_ga_volatile_cele c5 (unc-64 syntaxin) | N-type Ca2+ channel (Cacna1b / Cav2.2) |
| SAME_PATHWAY_MODULE | worm cryptobiosis c8 | S8_crypto_cele c10 (trehalose) | glyoxylate shunt (isocitrate lyase / malate synthase, gei-7/ic |
| SAME_PHYSICAL_CLASS | mouse NREM c3 | (free text) | Gabrd (GABA-A delta subunit) on PV+ interneurons |
| SAME_PHYSICAL_CLASS | mouse volatile c12 | S5_ga_volatile_cele c12 (unc-9 innexin) | Connexin36 (Gjd2) |
| UNSTRUCTURED_NOTE | human volatile c11 | (free text) |  |

Counts: EXACT_MOLECULE 7 - ORTHOLOGOUS_MOLECULE 4 - SAME_COMPLEX 1 - SAME_PATHWAY_MODULE 2 - SAME_PHYSICAL_CLASS 2

## Totals

- cells: 120 across 10 rows x 12 classes
- coverage: NOT_TESTED 53, TESTED_NEGATIVE 3, TESTED_POSITIVE 64
- mechanisms recorded: 96
- distinct load-bearing sources: 103
- cell-level roles present: CONTROLS_ENTRY 36, MAINTAINS_STATE 19, PRODUCES_STATE 16, PROTECTS_THROUGH_STATE 9, BUILDS_MACHINERY 5, ENABLES_EXIT 5
- cell-level roles TESTED NEGATIVE: PRODUCES_STATE 5, MAINTAINS_STATE 3, CONTROLS_ENTRY 3
- mechanism polarity: PROMOTES_STATE 39, OPPOSES_STATE 20, UNDETERMINED 18, CONTEXT_DEPENDENT 10, STRUCTURE_ONLY 5, NO_ESTABLISHED_EFFECT 4

## Per-row summary

| row | populated | positive | negative | roles present | strongest |
|---|---|---|---|---|---|
| worm lethargus | 9/12 | 8 | 1 | B1 E4 M5 P5 | E-A |
| worm L1 arrest | 6/12 | 6 | 0 | E1 M1 P3 T3 | E-A |
| worm dauer | 7/12 | 7 | 0 | B1 E4 M1 P1 T1 | E-A |
| worm cryptobiosis | 3/12 | 2 | 0 | B1 E2 T2 | E-B |
| mouse REM | 7/12 | 7 | 0 | B1 E3 M3 P4 | E-A |
| mouse NREM | 10/12 | 10 | 0 | B1 E4 M6 P3 | E-A |
| worm volatile | 9/12 | 7 | 1 | E8 | E-A |
| mouse volatile | 11/12 | 10 | 1 | E8 X4 M1 T2 | E-A |
| human volatile | 3/12 | 3 | 0 | E1 X1 M1 T1 | E-C |
| human propofol | 2/12 | 2 | 0 | E1 M1 | E-C |

