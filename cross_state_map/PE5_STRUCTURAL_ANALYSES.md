# PE-5 structural analyses

Generated from `rows_v2/*.json` at PE-5 completion. Every row passes Gate C at measured internal
retrieval recall 1.00, so the empty cells below are interpretable.

## 1. Role profile by state production mode

| row | state_production | P | E | M | T | B | X | populated |
|---|---|---|---|---|---|---|---|---|
| S2_core_cele | ENDOGENOUS | 5 | 4 | 5 | 0 | 1 | 0 | 9 |
| S6_starv_L1_cele | ENDOGENOUS | 3 | 1 | 1 | 3 | 0 | 0 | 6 |
| S7_dauer_cele | ENDOGENOUS | 1 | 4 | 1 | 1 | 1 | 0 | 7 |
| S8_crypto_cele | PHYSICALLY_IMPOSED | 0 | 2 | 0 | 2 | 1 | 0 | 3 |
| S3_rem_mmus | ENDOGENOUS | 4 | 3 | 3 | 0 | 1 | 0 | 7 |
| S4_deep_mmus | ENDOGENOUS | 3 | 4 | 6 | 0 | 1 | 0 | 10 |
| S5_ga_volatile_cele | EXOGENOUS_AGENT | 0 | 8 | 0 | 0 | 0 | 0 | 9 |
| S5_ga_volatile_mmus | EXOGENOUS_AGENT | 0 | 8 | 1 | 2 | 0 | 4 | 11 |
| S5_ga_volatile_hsap | EXOGENOUS_AGENT | 0 | 1 | 1 | 1 | 0 | 1 | 3 |
| S5_ga_propofol_hsap | EXOGENOUS_AGENT | 0 | 1 | 1 | 0 | 0 | 0 | 2 |

| state_production | rows | PRODUCES | ENTRY | MAINTAINS | PROTECTS | BUILDS | EXIT |
|---|---|---|---|---|---|---|---|
| ENDOGENOUS | 5 | 16 | 16 | 16 | 4 | 4 | 0 |
| PHYSICALLY_IMPOSED | 1 | 0 | 2 | 0 | 2 | 1 | 0 |
| EXOGENOUS_AGENT | 4 | 0 | 18 | 3 | 3 | 0 | 5 |

**Both zeros are exact.** Endogenous states: 16 PRODUCES, 0 EXIT. Exogenous-agent states: 0
PRODUCES, 5 EXIT. Not a coverage artefact - the best-scored row in the table (mouse volatile,
11/12) carries one of them.

## 2. Class coverage by state family

| family | rows | c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 | c10 | c11 | c12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| worm sleep/arrest | 3 | 2 | 1 | 1 | 0 | 3 | 3 | 3 | 3 | 3 | 1 | 0 | 2 |
| mammal sleep | 2 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 | 2 | 0 | 1 | 1 |
| anaesthesia | 4 | 2 | 2 | 1 | 2 | 2 | 4 | 3 | 3 | 0 | 2 | 2 | 2 |
| cryptobiosis | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 |

Anaesthesia (pharmacology) is dense in channels and receptors and EMPTY in class 9, transcriptional
reprogramming. Cryptobiosis (biochemistry) is populated ONLY in classes 8, 9 and 10. Sleep (systems
neuroscience) is dense in circuits and neuromodulators. At recall 1.00 these holes are not search
artefacts.

## 3. Molecules appearing in more than one row

- **daf-16**
  - S2_core_cele c9 roles=MAINTAINS_STATE polarity=STRUCTURE_ONLY
  - S7_dauer_cele c9 roles=CONTROLS_ENTRY/BUILDS_MACHINERY polarity=PROMOTES_STATE
- **dgk-1**
  - S2_core_cele c5 roles=PRODUCES_STATE/CONTROLS_ENTRY polarity=PROMOTES_STATE
  - S6_starv_L1_cele c5 roles=PRODUCES_STATE polarity=PROMOTES_STATE
- **gabrb1**
  - S3_rem_mmus c3 roles=MAINTAINS_STATE polarity=STRUCTURE_ONLY
  - S4_deep_mmus c3 roles=MAINTAINS_STATE polarity=STRUCTURE_ONLY
- **girk1/2**
  - S3_rem_mmus c2 roles=CONTROLS_ENTRY polarity=PROMOTES_STATE
  - S4_deep_mmus c2 roles=CONTROLS_ENTRY polarity=PROMOTES_STATE
- **lea-1**
  - S7_dauer_cele c10 roles=PROTECTS_THROUGH_STATE polarity=PROMOTES_STATE
  - S8_crypto_cele c10 roles=PROTECTS_THROUGH_STATE polarity=PROMOTES_STATE
- **muscarinic acetylcholine receptors**
  - S5_ga_volatile_hsap c6 roles=MAINTAINS_STATE polarity=OPPOSES_STATE
  - S5_ga_propofol_hsap c6 roles=MAINTAINS_STATE/CONTROLS_ENTRY polarity=OPPOSES_STATE
- **nalcn**
  - S3_rem_mmus c1 roles=CONTROLS_ENTRY/MAINTAINS_STATE polarity=OPPOSES_STATE
  - S5_ga_volatile_mmus c1 roles=PROTECTS_THROUGH_STATE polarity=UNDETERMINED
- **parafacial zone gabaergic neurons**
  - S4_deep_mmus c7 roles=MAINTAINS_STATE polarity=NO_ESTABLISHED_EFFECT
  - S5_ga_volatile_mmus c7 roles=CONTROLS_ENTRY/ENABLES_EXIT polarity=PROMOTES_STATE
- **slo-1**
  - S2_core_cele c2 roles=MAINTAINS_STATE/PRODUCES_STATE polarity=PROMOTES_STATE
  - S5_ga_volatile_cele c2 roles=CONTROLS_ENTRY polarity=PROMOTES_STATE
- **tfap2b**
  - S3_rem_mmus c9 roles=BUILDS_MACHINERY/MAINTAINS_STATE polarity=PROMOTES_STATE
  - S4_deep_mmus c9 roles=BUILDS_MACHINERY/MAINTAINS_STATE polarity=PROMOTES_STATE
- **unc-79**
  - S2_core_cele c1 roles=MAINTAINS_STATE polarity=CONTEXT_DEPENDENT
  - S5_ga_volatile_cele c1 roles=CONTROLS_ENTRY polarity=OPPOSES_STATE
- **unc-80**
  - S2_core_cele c1 roles=MAINTAINS_STATE polarity=CONTEXT_DEPENDENT
  - S5_ga_volatile_cele c1 roles=CONTROLS_ENTRY polarity=OPPOSES_STATE

## 4. Cells carrying a measured null

- **S2_core_cele c3** coverage=TESTED_NEGATIVE roles_tested_negative=['PRODUCES_STATE']
  - power: Turek 2013 assayed RIS-dependent lethargus quiescence with GABA function removed; the assay could have detected a requirement for GABA in RIS-driven quiescence and did not. Turek 2016 independently concluded FLP-11, not GABA, is the major d
- **S4_deep_mmus c3** coverage=TESTED_POSITIVE roles_tested_negative=['MAINTAINS_STATE']
  - power: Chronic EEG was recorded in Gabra3-knockout and wild-type mice (PMID:18485607). No difference was resolved during NREM sleep, at waking-NREM transitions, or in the response to 6 h sleep deprivation. The same recordings DID resolve two chang
- **S4_deep_mmus c7** coverage=TESTED_POSITIVE roles_tested_negative=['MAINTAINS_STATE']
  - power: EEG-defined sleep and the homeostatic sleep drive after sleep deprivation were measured in PZGABA-ablated and mCherry control mice (PMID:40240218). Ablation of up to 70-80% of PZGABA neurones did not alter the amount of endogenous sleep or 
- **S5_ga_volatile_cele c7** coverage=TESTED_NEGATIVE roles_tested_negative=['PRODUCES_STATE']
  - power: Chang 2025 imaged 20 animals with NeuroPAL identification under graded isoflurane by light-sheet microscopy and analysed the identified sleep-atonia pathway (ALA, RIS, AVE, AVA). The assay could have detected recruitment of the quiescence p
- **S5_ga_volatile_mmus c7** coverage=TESTED_POSITIVE roles_tested_negative=['PRODUCES_STATE']
  - power: Chemogenetic reactivation of Fos-captured, isoflurane-activated brain-wide ensembles (PMID:41573848) produced immobility, discoordination and anti-nociception and significantly increased anaesthetic sensitivity, but did NOT produce loss of 
- **S5_ga_volatile_mmus c10** coverage=TESTED_NEGATIVE roles_tested_negative=['CONTROLS_ENTRY']
  - power: EC50 for loss of response to tail clamp was determined in stomatin-knockout and parental mice under continuous flows of diethyl ether, halothane and isoflurane. A 12% sensitivity increase was resolved for diethyl ether; no significant chang

## 5. Evidence grade distribution

E-A 37, E-B 54, E-C 15, E-D 1, E-E 1, E-F 1
