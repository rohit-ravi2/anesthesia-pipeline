"""PE-5 round-2b — findings whose target cells were ALREADY populated.

pe5_apply_r2.py deliberately refuses to overwrite a populated cell. Six of its findings landed on
cells that already carried a different mechanism, so they were skipped rather than lost. This file
appends them as additional mechanisms on those cells, which is the correct representation anyway:
a class can carry several independent mechanisms with different roles and different polarities, and
flattening them would destroy exactly the structure the role axis exists to record.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pe5_apply_findings import mech
from pe5_apply_r2 import (add_mech, ch, APPLIED, SKIPPED,
                          S_NDUFS4_GLU, S_PZ, S_PZ_NEG, S_PPT, S_OX, S_CD73)

APPLIED.clear(); SKIPPED.clear()

# ---------------------------------------------------------------- 1) mouse volatile c4
add_mech('S5_ga_volatile_mmus', 4,
         mech("Excitatory (glutamatergic) neurons are the cell class through which complex I "
              "dysfunction sets volatile-anaesthetic potency",
              [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-B", "citation_ids": ["PMID:27498564"],
                "basis": "Cell-type-restricted metabolic lesion reproduces the whole-animal "
                         "anaesthetic phenotype, with a matched presynaptic excitatory readout and an "
                         "inhibitory-side negative control in the same slices."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
                "agent": "isoflurane",
                "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                    "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                    "other": "glutamatergic-restricted NDUFS4 loss recapitulates VA "
                                             "hypersensitivity; GABAergic and cholinergic restriction "
                                             "do NOT; baseline CA1 electrophysiology unchanged; sEPSC "
                                             "frequency falls at 0.6% isoflurane only in KO; sIPSCs "
                                             "not differentially affected; evoked fEPSP and paired-"
                                             "pulse facilitation similar between genotypes"},
                "context_dependence": "cell_type_dependent", "statement": S_NDUFS4_GLU,
                "evidence_grade": "E-B", "citation_ids": ["PMID:27498564"]}],
              "OPPOSES_STATE",
              [ch("metabolic lesion confined to glutamatergic neurons", 8, "E-B", ["PMID:27498564"]),
               ch("spontaneous excitatory transmission becomes anaesthetic-hypersensitive", 4, "E-B",
                  ["PMID:27498564"]),
               ch("whole-animal volatile-anaesthetic hypersensitivity", None, "E-B", ["PMID:27498564"])],
              4, [{"name": "glutamatergic neurons as the causal cell class (not a receptor)",
                   "species": "mmus", "identifier": None, "ortholog_relation": None}],
              ["PMID:27498564"],
              "anaesthetic-induced failure of excitatory presynaptic release under reduced metabolic reserve",
              None),
         note=("SCOPE. This is NOT evidence that a glutamate receptor is an anaesthetic target. The "
               "manipulation is a METABOLIC lesion targeted to glutamatergic neurons, read out as "
               "sEPSC frequency, with an explicit inhibitory-side negative (sIPSCs not differentially "
               "affected) and two negative cell-type controls (GABAergic, cholinergic). It is "
               "evidence that EXCITATORY TRANSMISSION is the route by which metabolic state sets "
               "anaesthetic potency, and it is the mechanistic bridge between this row's class 4, "
               "class 5 and class 8 entries."),
         extra_roles=["CONTROLS_ENTRY"], grade="E-B")

# ---------------------------------------------------------------- 2) mouse volatile c7
add_mech('S5_ga_volatile_mmus', 7,
         mech("Parafacial-zone GABAergic neurons are required for volatile-anaesthetic hypnosis",
              [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"],
                "basis": "Caspase ablation produces durable behavioural resistance to two agents, "
                         "dose-graded against the number of surviving neurons."},
               {"role": "ENABLES_EXIT", "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"],
                "basis": "Ablated mice emerged from isoflurane significantly faster with purposeful "
                         "movement - exit kinetics measured separately from induction."}],
              [{"manipulation": "ablation", "direction_of_manipulation": "remove",
                "agent": "isoflurane; sevoflurane",
                "observed_effect": {"total_quiescence": "decrease", "state_structure": "not_reported",
                                    "entry_threshold": "increase", "survival_recovery": "increase",
                                    "other": "~50% higher likelihood of intact righting; resistance "
                                             "inversely correlated with surviving PZGABA count; "
                                             "hypnotic isoflurane tripled c-Fos in PZGABA neurons; NO "
                                             "EEG signature of anaesthetic resistance"},
                "context_dependence": "none_reported", "statement": S_PZ,
                "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"]}],
              "PROMOTES_STATE",
              [ch("AAV-caspase ablation of parafacial GABAergic neurons", 7, "E-A", ["PMID:40240218"]),
               ch("loss of a brainstem NREM-promoting node", 7, "E-A", ["PMID:40240218"]),
               ch("behavioural resistance to isoflurane and sevoflurane hypnosis; faster emergence",
                  None, "E-A", ["PMID:40240218"])],
              7, [{"name": "parafacial zone GABAergic neurons (PZGABA)", "species": "mmus",
                   "identifier": None,
                   "ortholog_relation": "Same neurons, same ablation, same animals as the NEGATIVE "
                                        "recorded at S4_deep_mmus c7. EXACT_MOLECULE overlap across "
                                        "two states with opposite verdicts."}],
              ["PMID:40240218"],
              "removal of a GABAergic brainstem node that hypnotic volatile doses depolarise",
              {"level": "EXACT_MOLECULE", "partner": "S4_deep_mmus c7 (same paper, NEGATIVE)",
               "justification": "The identical manipulation in the identical animals is positive for "
                                "the drug-induced state and negative for natural NREM sleep."}),
         note=("AXIS DISSOCIATION stated by the authors: ablation shifted the BEHAVIOURAL (righting) "
               "endpoint but did NOT produce EEG signatures of anaesthetic resistance. A_beh moved, "
               "A_neu did not. This is precisely the case the frozen three-axis rule exists to keep "
               "visible, and it would have been erased by any single-axis 'depth of anaesthesia' score."),
         extra_roles=["CONTROLS_ENTRY", "ENABLES_EXIT"], grade="E-A")

# ---------------------------------------------------------------- 3) mouse NREM c7 — the matching NEGATIVE
add_mech('S4_deep_mmus', 7,
         mech("Parafacial-zone GABAergic neurons are NOT required for the amount of natural NREM "
              "sleep or for sleep homeostasis",
              [{"role": "MAINTAINS_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"],
                "basis": "TESTED AND NEGATIVE on sleep amount and on homeostatic rebound, with an "
                         "internal positive control (a large anaesthetic phenotype) in the same animals."}],
              [{"manipulation": "ablation", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "no_change", "state_structure": "no_change",
                                    "entry_threshold": "no_change", "survival_recovery": "not_reported",
                                    "other": "no insomnia; sleep pressure after deprivation unchanged; "
                                             "70-80% of PZGABA neurons destroyed; the SAME animals were "
                                             "behaviourally resistant to isoflurane and sevoflurane"},
                "context_dependence": "state_dependent", "statement": S_PZ_NEG,
                "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"]}],
              "NO_ESTABLISHED_EFFECT",
              [ch("AAV-caspase ablation of parafacial GABAergic neurons", 7, "E-A", ["PMID:40240218"]),
               ch("no change in NREM amount or homeostatic drive", None, "E-A", ["PMID:40240218"])],
              7, [{"name": "parafacial zone GABAergic neurons (PZGABA)", "species": "mmus",
                   "identifier": None, "ortholog_relation": None}],
              ["PMID:40240218"],
              "no resolvable change in endogenous sleep amount or sleep pressure",
              {"level": "EXACT_MOLECULE", "partner": "S5_ga_volatile_mmus c7 (same paper, POSITIVE)",
               "justification": "Not merely the same class - the same neurons, ablation, animals and "
                                "paper. The rows differ only in which state was assayed. The cleanest "
                                "available demonstration that causal role is a property of the STATE."}),
         note=("A NEGATIVE THAT IS MORE INFORMATIVE THAN MOST POSITIVES. A node of the sleep-promoting "
               "circuitry is REQUIRED for volatile-anaesthetic hypnosis (S5_ga_volatile_mmus c7) and "
               "DISPENSABLE for the amount and homeostasis of natural NREM sleep. It directly "
               "constrains the 'anaesthesia co-opts sleep circuitry' hypothesis: co-option is not "
               "symmetric, and a shared node can be load-bearing in one direction only. SCOPE: one "
               "node, not the circuit class; nothing here licenses a general claim about sleep "
               "circuitry being dispensable for NREM."),
         extra_roles=[], grade="E-A")

# ---------------------------------------------------------------- 4) mouse REM c6
add_mech('S3_rem_mmus', 6,
         mech("Cholinergic PPT/LDT neurons are sufficient to induce REM sleep from NREM",
              [{"role": "PRODUCES_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:25548191"],
                "basis": "'Activation of cholinergic neurons in the PPT or LDT during NREM sleep was "
                         "sufficient to induce REM sleep.' An explicit sufficiency demonstration."},
               {"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:25548191"],
                "basis": "The measured effect is on episode NUMBER, i.e. on transition rate into the "
                         "state, not on how long the state is held."}],
              [{"manipulation": "optogenetic_activation", "direction_of_manipulation": "increase",
                "agent": None,
                "observed_effect": {"total_quiescence": "increase", "state_structure": "increase",
                                    "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                    "other": "number of REM episodes INCREASED; REM episode DURATION "
                                             "UNCHANGED; obtained independently in PPT and in LDT"},
                "context_dependence": "state_dependent", "statement": S_PPT,
                "evidence_grade": "E-A", "citation_ids": ["PMID:25548191"]}],
              "PROMOTES_STATE",
              [ch("optogenetic activation of cholinergic mesopontine neurons", 6, "E-A",
                  ["PMID:25548191"]),
               ch("increased rate of NREM-to-REM transitions", None, "E-A", ["PMID:25548191"])],
              6, [{"name": "ChAT-positive PPT/LDT neurons; acetylcholine", "species": "mmus",
                   "identifier": None,
                   "ortholog_relation": "Acetylcholine also carries the two human anaesthesia class-6 "
                                        "entries (physostigmine reversal of sevoflurane; raised "
                                        "propofol induction dose), where its direction is ANTI-state. "
                                        "SAME_PHYSICAL_CLASS with opposite sign across states."}],
              ["PMID:25548191"],
              "cholinergic depolarisation of REM-generating pontine circuitry raising transition probability",
              None),
         note=("ENTRY WITHOUT MAINTENANCE, measured in one experiment: episode NUMBER rose, episode "
               "DURATION did not. Under the frozen role axis that is PRODUCES_STATE plus "
               "CONTROLS_ENTRY with MAINTAINS_STATE tested and negative. Very few manipulations in "
               "this table separate entry from maintenance that cleanly, and it is the same "
               "separation the anaesthesia rows conspicuously lack."),
         extra_roles=["PRODUCES_STATE", "CONTROLS_ENTRY"], grade="E-A")

add_mech('S3_rem_mmus', 6,
         mech("Orexin restrains REM intrusion through both OX2R-dependent and OX2R-independent pathways",
              [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:12797957"],
                "basis": "Two germline genotypes dissociate the phenotype: OX2R loss gives MILD "
                         "cataplexy-like REM attacks, full orexin loss gives SEVERE ones, while both "
                         "give equal non-REM sleep attacks."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "increase", "state_structure": "decrease",
                                    "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                    "other": "OX2R-/- only MILDLY affected by cataplexy-like REM "
                                             "attacks; orexin-/- SEVERELY affected; both equally "
                                             "affected by non-REM sleep attacks and disrupted wakefulness"},
                "context_dependence": "receptor_subtype_dependent", "statement": S_OX,
                "evidence_grade": "E-A", "citation_ids": ["PMID:12797957"]}],
              "OPPOSES_STATE",
              [ch("orexin or OX2R deletion", 6, "E-A", ["PMID:12797957"]),
               ch("loss of orexin excitation of monoaminergic and histaminergic populations", 6, "E-A",
                  ["PMID:12797957"]),
               ch("REM intrusion into wakefulness", None, "E-A", ["PMID:12797957"])],
              6, [{"name": "orexin (hypocretin) peptide and OX2R receptor", "species": "mmus",
                   "identifier": None, "ortholog_relation": None}],
              ["PMID:12797957"],
              "loss of peptidergic excitatory tone that normally gates REM-generating circuitry",
              None),
         note=("LIGAND AND RECEPTOR DISSOCIATE. Deleting the ligand is worse than deleting OX2R for "
               "REM but equivalent for NREM. The class-6 entry therefore cannot be summarised as "
               "'orexin signalling'; the receptor subtype carries the NREM phenotype and something "
               "beyond it carries the REM phenotype."),
         extra_roles=["CONTROLS_ENTRY"], grade="E-A")

# ---------------------------------------------------------------- 5) mouse NREM c6
add_mech('S4_deep_mmus', 6,
         mech("OX2R activation is required for normal wake-to-NREM transition control",
              [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:12797957"],
                "basis": "Germline receptor deletion produces behaviourally abnormal attacks of "
                         "non-REM sleep; the authors attribute wake/non-REM transition control "
                         "specifically to OX2R."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "increase", "state_structure": "decrease",
                                    "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                    "other": "abnormal non-REM 'sleep attacks'; OX2R loss eliminates "
                                             "orexin-evoked excitation of histaminergic neurons that "
                                             "gate non-REM sleep onset"},
                "context_dependence": "receptor_subtype_dependent", "statement": S_OX,
                "evidence_grade": "E-A", "citation_ids": ["PMID:12797957"]}],
              "OPPOSES_STATE",
              [ch("OX2R deletion", 6, "E-A", ["PMID:12797957"]),
               ch("loss of orexin-evoked excitation of histaminergic neurons", 6, "E-A",
                  ["PMID:12797957"]),
               ch("uncontrolled non-REM sleep onset", None, "E-A", ["PMID:12797957"])],
              6, [{"name": "OX2R (Hcrtr2)", "species": "mmus", "identifier": None,
                   "ortholog_relation": None}],
              ["PMID:12797957"],
              "loss of peptidergic excitatory drive onto histaminergic wake-promoting neurons",
              None),
         note=("Wake/NREM transition control is attributed to OX2R specifically, and the SAME paper "
               "shows the REM phenotype is not carried by OX2R alone - see the matching entry at "
               "S3_rem_mmus c6."),
         extra_roles=["CONTROLS_ENTRY"], grade="E-A")

add_mech('S4_deep_mmus', 6,
         mech("CD73-derived extracellular adenosine is required for the homeostatic NREM response to "
              "sleep deprivation, not for baseline NREM",
              [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:22540145"],
                "basis": "Knockout abolishes the deprivation-induced NREM increase while baseline "
                         "NREM is if anything GREATER - an effect on the entry controller that is "
                         "separable from the state itself."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "increase", "state_structure": "decrease",
                                    "entry_threshold": "not_reported", "survival_recovery": "not_reported",
                                    "other": "baseline NREMS GREATER in KO; NO NREMS enhancement after "
                                             "sleep deprivation; IL1beta STILL enhanced NREMS in KO "
                                             "(positive control for sleep-response capacity); 1.0-2.5 "
                                             "Hz power rise after deprivation smaller in KO; REM "
                                             "unchanged between strains in all conditions"},
                "context_dependence": "challenge_dependent", "statement": S_CD73,
                "evidence_grade": "E-A", "citation_ids": ["PMID:22540145"]}],
              "PROMOTES_STATE",
              [ch("Nt5e/CD73 deletion", 6, "E-A", ["PMID:22540145"]),
               ch("loss of extracellular AMP-to-adenosine conversion", 6, "E-A", ["PMID:22540145"]),
               ch("absent homeostatic NREM rebound", None, "E-A", ["PMID:22540145"])],
              6, [{"name": "CD73 / Nt5e 5'-ectonucleotidase; extracellular adenosine", "species": "mmus",
                   "identifier": None, "ortholog_relation": None}],
              ["PMID:22540145"],
              "loss of activity-dependent extracellular adenosine accumulation that raises sleep propensity",
              None),
         note=("THE STATE AND ITS CONTROLLER COME APART. CD73-KO mice sleep MORE at baseline yet show "
               "NO rebound after deprivation, and IL1beta still increases their NREM - so the "
               "machinery for entering NREM is intact and only the homeostatic drive is lost. The "
               "IL1beta arm is the positive control that makes the null interpretable, which is the "
               "standard this table's negative_assay_statement field demands. REM was unaffected in "
               "every condition, so this is also a state-specific negative for S3_rem_mmus."),
         extra_roles=["CONTROLS_ENTRY"], grade="E-A")

print('APPLIED (%d):' % len(APPLIED))
for a in APPLIED:
    print('  ' + a)
print('SKIPPED (%d):' % len(SKIPPED))
for s in SKIPPED:
    print('  ' + s)
