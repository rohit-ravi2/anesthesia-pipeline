"""PE-5 round-2 findings — v3 protocol (repaired vocabulary, depth 120/200/400).

Every finding here was retrieved by the corrected battery, read at abstract level against species,
state, endpoint and manipulation, and is applied with the verbatim authoritative statement.
Idempotent: re-running is safe (each block checks current coverage before writing).

Sources applied in this round:
  22912761  Ndufs4 KO mice, anaesthetic sensitivity             -> S5_ga_volatile_mmus c8
  27498564  Ndufs4 restricted to glutamatergic neurons          -> S5_ga_volatile_mmus c4, c8
  16931982  stomatin KO mice vs unc-1 worms                     -> S5_ga_volatile_mmus c10 NEGATIVE
  40240218  parafacial GABA ablation                            -> S5_ga_volatile_mmus c7 POSITIVE
                                                                   S4_deep_mmus        c7 NEGATIVE
  33942407  GABA-A beta1 KO sleep EEG                           -> S3_rem_mmus c3, S4_deep_mmus c3
  25548191  optogenetic PPT/LDT cholinergic activation          -> S3_rem_mmus c6
  12797957  OX2R-/- vs orexin-/- narcolepsy dissection          -> S3_rem_mmus c6, S4_deep_mmus c6
  22540145  CD73 (5'-ectonucleotidase) KO                       -> S4_deep_mmus c6
  37682636  dgk-1 forward screen, C. elegans sleep              -> S2_core_cele c5
  38371321  nlp-2/22/23 new alleles                             -> S2_core_cele c6
  33712439  dauer via AWC/ASI, EXP-1, STR-2                     -> S7_dauer_cele c7, c3
  41279428  HLH-30/TFEB in L1 arrest (PREPRINT)                 -> S6_starv_L1_cele c9
"""
import json, collections, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'rows_v2')
sys.path.insert(0, HERE)
from pe5_apply_findings import save_and_recompute, mech

APPLIED, SKIPPED = [], []


def put(row, cid, **kw):
    """Write a cell if it is still NOT_TESTED, else record as already-applied. Idempotent."""
    f = os.path.join(D, row + '.json')
    d = json.load(open(f))
    for c in d['cells']:
        if c['class_id'] != cid:
            continue
        if c['coverage'] != 'NOT_TESTED':
            SKIPPED.append('%s|c%d already %s' % (row, cid, c['coverage']))
            return False
        c.update(kw)
        cov, cnt = save_and_recompute(d, f)
        APPLIED.append('%s|c%d -> %s' % (row, cid, kw['coverage']))
        return True
    SKIPPED.append('%s|c%d MISSING CELL' % (row, cid))
    return False


def add_mech(row, cid, m, note=None, extra_roles=(), grade=None):
    """Append a mechanism to an already-populated cell (second line of evidence)."""
    f = os.path.join(D, row + '.json')
    d = json.load(open(f))
    for c in d['cells']:
        if c['class_id'] != cid:
            continue
        if any(x['label'] == m['label'] for x in c['mechanisms']):
            SKIPPED.append('%s|c%d mechanism already present' % (row, cid))
            return False
        c['mechanisms'].append(m)
        for r in extra_roles:
            if r not in c['roles_present']:
                c['roles_present'].append(r)
        if grade and grade not in c['all_grades']:
            c['all_grades'].append(grade)
        if note:
            c['ambiguity'] = (c.get('ambiguity') or '') + ' PE-5 R2: ' + note
        if c['coverage'] == 'NOT_TESTED':
            c['coverage'] = 'TESTED_POSITIVE'
            c['status'] = 'POSITIVE'
        save_and_recompute(d, f)
        APPLIED.append('%s|c%d += %s' % (row, cid, m['label'][:52]))
        return True
    return False


# ---------------------------------------------------------------- statements (verbatim)
S_NDUFS4 = ("KO mice were 2.5 - to 3-fold more sensitive to isoflurane and halothane than WT mice. "
            "KO mice were 2-fold more sensitive to propofol but resistant to ketamine. These changes "
            "in anesthetic sensitivity are the largest recorded in a mammal.")
S_NDUFS4_GLU = ("Limiting NDUFS4 loss to a subset of glutamatergic neurons recapitulates the VA "
                "hypersensitivity of Ndufs4(KO) mice, while loss in GABAergic or cholinergic neurons "
                "does not. Baseline electrophysiologic function of CA1 pyramidal neurons does not "
                "differ between Ndufs4(KO) and control mice. Isoflurane concentrations that "
                "anesthetize only Ndufs4(KO) mice (0.6%) decreased the frequency of spontaneous "
                "excitatory postsynaptic currents (sEPSCs) only in Ndufs4(KO) CA1 neurons... "
                "Spontaneous inhibitory postsynaptic currents (sIPSCs) were not differentially "
                "affected between genotypes.")
S_STOM = ("Stomatin-deficient mice had a 12% increase in sensitivity to diethyl ether but no "
          "significant change in sensitivity to halothane or isoflurane compared with wild type. "
          "No defect in locomotion was noted in the mutant mouse... Neither nematodes nor mice with "
          "stomatin deficiencies have significantly altered sensitivity to isoflurane or halothane.")
S_PZ = ("PZGABA-ablated mice developed significant and durable behavioural resistance to both "
        "isoflurane- and sevoflurane-induced hypnosis, with roughly 50% higher likelihood of intact "
        "righting than controls. PZGABA-ablated mice emerged from isoflurane significantly faster than "
        "mCherry controls with purposeful movements. The degree of anaesthetic resistance was "
        "inversely correlated with the number of surviving PZGABA neurones.")
S_PZ_NEG = ("Despite confirming that PZGABA ablation reduced the potency of two distinct volatile "
            "anaesthetics behaviourally, ablation did not alter the amount of endogenous sleep or "
            "wakefulness, nor did it affect the homeostatic sleep drive after sleep deprivation, and "
            "it did not produce EEG signatures of anaesthetic resistance during isoflurane exposure... "
            "destruction of up to 70-80% of PZGABA neurones was sufficient to alter anaesthetic "
            "susceptibility behaviourally without causing insomnia or altering sleep pressure.")
S_B1 = ("beta1-/- mice have a distinct and abnormal sleep phenotype characterized by increased delta "
        "power in non-rapid eye movement (NREM) sleep and decreased theta activity in rapid eye "
        "movement (REM) sleep compared to beta1+/+ mice, without any change in the overall sleep-wake "
        "architecture... the GABAA receptor beta1-subunit does not play an important role in sleep "
        "initiation or maintenance but instead regulates the power spectrum.")
S_PPT = ("Selective optogenetic activation of cholinergic neurons in the PPT or LDT during non-REM "
         "(NREM) sleep increased the number of REM sleep episodes and did not change REM sleep episode "
         "duration. Activation of cholinergic neurons in the PPT or LDT during NREM sleep was "
         "sufficient to induce REM sleep.")
S_OX = ("Both OX2R(-/-) and orexin(-/-) mice are similarly affected with behaviorally abnormal attacks "
        "of non-REM sleep (\"sleep attacks\") and show similar degrees of disrupted wakefulness. In "
        "contrast, OX2R(-/-) mice are only mildly affected with cataplexy-like attacks of REM sleep, "
        "whereas orexin(-/-) mice are severely affected... While normal regulation of wake/non-REM "
        "sleep transitions depends critically upon OX2R activation, the profound dysregulation of REM "
        "sleep control unique to the narcolepsy-cataplexy syndrome emerges from loss of signaling "
        "through both OX2R-dependent and OX2R-independent pathways.")
S_CD73 = ("Duration of spontaneous non-rapid eye movement sleep (NREMS) was greater in CD73-knockout "
          "(KO) mice than in C57BL/6 controls... After sleep deprivation (SD), NREMS was enhanced in "
          "controls but not CD73-KO mice. Interleukin-1 beta (IL1beta) enhanced NREMS in both strains, "
          "indicating that the CD73-KO mice were capable of sleep responses... Rapid eye movement sleep "
          "did not differ between strains in any of the experimental conditions.")
S_DGK = ("The causal gene of the abnormal sleep phenotypes in both mutants was mapped to dgk-1, which "
         "encodes diacylglycerol kinase. Perhaps due to the diminished SIS, dgk-1 mutant worms "
         "exhibited decreased survival following exposure to a noxious stimulus. Pan-neuronal and/or "
         "cholinergic expression of dgk-1 partly rescued the dgk-1 mutant defects in DTS, SIS, and "
         "post-stress survival... pkc-1/nPKC participates in sleep regulation and counteracts the "
         "effect of dgk-1.")
S_NLP = ("Confirming previous studies, we find that nlp-22 is required for developmentally-timed sleep, "
         "and show that nlp-23 is also required. However, all three genes are dispensable for "
         "stress-induced sleep.")
S_DAUER = ("Our dauer experiments reveal that in daf-7 mutants, ASI expressed EXP-1 and STR-2 (a "
           "G-protein-coupled receptor; GPCR) that partially maintained reproductive growth of animals. "
           "Further, studies suggest that neuronal connections between ASI and AWC neurons are allowed "
           "at least partially through ASI secreted DAF-7 or through alternate TGF-beta pathway/s "
           "regulated by EXP-1 and STR-2.")
S_HLH30 = ("We show that HLH-30 and DAF-16 collaborate to ensure survival under starvation, with "
           "reciprocal regulation of their subcellular localization and transcriptional activity. "
           "HLH-30 exerts broad transcriptional control during L1 arrest... Loss of HLH-30 disrupts "
           "seam cell cycle arrest and leads to overactivation of the pioneer transcription factor "
           "BLMP-1, leading to premature initiation of developmental programs under starvation.")


def ch(step, cid, g, cits):
    return {"step": step, "class_id": cid, "role": "proximal", "inferred": False,
            "evidence_grade": g, "citation_ids": cits}


# ================================================================ 1) mouse volatile c8 — complex I
put('S5_ga_volatile_mmus', 8,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["CONTROLS_ENTRY"], roles_tested_negative=[],
    ambiguity=("Direction is unambiguous and quantified: REDUCED complex I function gives "
               "HYPERSENSITIVITY, so intact complex I OPPOSES entry into the anaesthetised state. "
               "AGENT DISSOCIATION WITHIN ONE PAPER: hypersensitive to isoflurane, halothane and "
               "propofol; RESISTANT to ketamine - so this is not a general anaesthetic-sensitivity "
               "shift. The follow-up localises the effect to glutamatergic neurons and shows it is "
               "NOT reproduced by loss in GABAergic or cholinergic neurons, and that baseline CA1 "
               "electrophysiology is normal, which excludes a trivial sick-neuron explanation."),
    strongest_grade="E-A", all_grades=["E-A", "E-B"], negative_assay_statement=None,
    mechanisms=[
        mech("Mitochondrial complex I subunit NDUFS4 sets volatile-anaesthetic potency in mouse",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:22912761"],
               "basis": "Germline knockout shifts the whole-animal anaesthetic EC50 2.5-3 fold on a "
                        "loss-of-response-to-tail-clamp endpoint. Entry threshold, not maintenance."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
               "agent": "isoflurane; halothane; propofol; ketamine",
               "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                   "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                   "other": "2.5-3x hypersensitive to isoflurane and halothane; 2x to "
                                            "propofol; RESISTANT to ketamine; largest anaesthetic-"
                                            "sensitivity change recorded in a mammal"},
               "context_dependence": "agent_dependent", "statement": S_NDUFS4,
               "evidence_grade": "E-A", "citation_ids": ["PMID:22912761"]}],
             "OPPOSES_STATE",
             [ch("Ndufs4 deletion", 8, "E-A", ["PMID:22912761"]),
              ch("reduced mitochondrial complex I capacity", 8, "E-A", ["PMID:22912761"]),
              ch("presynaptic excitatory transmission in CA1 becomes hypersensitive to isoflurane", 5,
                 "E-B", ["PMID:27498564"]),
              ch("loss of response to tail clamp at lower anaesthetic concentration", None, "E-A",
                 ["PMID:22912761"])],
             8, [{"name": "Ndufs4 (complex I accessory subunit)", "species": "mmus", "identifier": None,
                  "ortholog_relation": "The worm volatile row carries gas-1 (complex I 49 kDa subunit) "
                                       "hypersensitivity. Relation is ORTHOLOGOUS_MOLECULE at the level "
                                       "of the complex, SAME_COMPLEX strictly: gas-1 and Ndufs4 are "
                                       "different subunits of the same complex I."}],
             ["PMID:22912761", "PMID:27498564"],
             "reduced electron-transport capacity lowers the anaesthetic concentration at which "
             "excitatory presynaptic function fails to meet metabolic demand",
             {"level": "SAME_COMPLEX",
              "partner": "S5_ga_volatile_cele c8 (gas-1)",
              "justification": "Different subunits, same respiratory complex, same direction "
                               "(loss of function -> hypersensitivity), same endpoint family "
                               "(immobility / loss of response). This is the strongest cross-species "
                               "mechanism correspondence in the table."}),
    ])

# ---- cell-type restriction as a second mechanism on the same cell
add_mech('S5_ga_volatile_mmus', 8,
         mech("Complex I loss acts through glutamatergic, not GABAergic or cholinergic, neurons",
              [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-B", "citation_ids": ["PMID:27498564"],
                "basis": "Conditional restriction of the same lesion to a neuron class reproduces the "
                         "whole-animal phenotype; restriction to two other classes does not."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
                "agent": "isoflurane",
                "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                    "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                    "other": "glutamatergic-restricted loss recapitulates VA "
                                             "hypersensitivity; GABAergic and cholinergic restriction "
                                             "do NOT; baseline CA1 electrophysiology unchanged; at "
                                             "0.6% isoflurane sEPSC frequency falls only in KO, sIPSCs "
                                             "not differentially affected"},
                "context_dependence": "cell_type_dependent", "statement": S_NDUFS4_GLU,
                "evidence_grade": "E-B", "citation_ids": ["PMID:27498564"]}],
              "OPPOSES_STATE",
              [ch("NDUFS4 loss restricted to glutamatergic neurons", 8, "E-B", ["PMID:27498564"]),
               ch("isoflurane-hypersensitive reduction of spontaneous EPSC frequency", 5, "E-B",
                  ["PMID:27498564"]),
               ch("VA hypersensitivity of the whole animal", None, "E-B", ["PMID:27498564"])],
              8, [{"name": "Ndufs4, conditional", "species": "mmus", "identifier": None,
                   "ortholog_relation": None}],
              ["PMID:27498564"],
              "presynaptic excitatory release becomes the metabolically limiting step under anaesthetic",
              None),
         note=("Cell-type restriction result: the metabolic mechanism is routed specifically through "
               "EXCITATORY transmission. This links class 8 to class 4 and class 5 within one animal "
               "and is the mechanistic bridge the table's class-8 entries previously lacked."),
         grade="E-B")

# ================================================================ 2) mouse volatile c4 — glutamatergic
put('S5_ga_volatile_mmus', 4,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["CONTROLS_ENTRY"], roles_tested_negative=[],
    ambiguity=("SCOPE. The manipulation is not of a glutamate receptor; it is a metabolic lesion "
               "TARGETED TO GLUTAMATERGIC NEURONS, with a measured presynaptic excitatory-transmission "
               "readout (sEPSC frequency) and an explicit negative on the inhibitory side (sIPSCs not "
               "differentially affected). It is therefore evidence that excitatory transmission is the "
               "route by which anaesthetic potency is set in this model, NOT evidence that a "
               "glutamate receptor is an anaesthetic target. Recorded as class 4 with that scope "
               "stated, because collapsing it into class 8 alone would hide the cell-type result."),
    strongest_grade="E-B", all_grades=["E-B"], negative_assay_statement=None,
    mechanisms=[
        mech("Excitatory (glutamatergic) neurons are the cell class through which complex I "
             "dysfunction sets volatile-anaesthetic potency",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-B", "citation_ids": ["PMID:27498564"],
               "basis": "Cell-type-restricted lesion plus a matched electrophysiological readout in "
                        "the same preparation, with an inhibitory-side negative control."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
               "agent": "isoflurane",
               "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                   "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                   "other": "sEPSC frequency reduced at 0.6% isoflurane only in KO; "
                                            "sIPSCs not differentially affected; evoked fEPSP and "
                                            "paired-pulse facilitation similar between genotypes"},
               "context_dependence": "cell_type_dependent", "statement": S_NDUFS4_GLU,
               "evidence_grade": "E-B", "citation_ids": ["PMID:27498564"]}],
             "OPPOSES_STATE",
             [ch("metabolic lesion confined to glutamatergic neurons", 8, "E-B", ["PMID:27498564"]),
              ch("spontaneous excitatory transmission becomes anaesthetic-hypersensitive", 4, "E-B",
                 ["PMID:27498564"]),
              ch("whole-animal anaesthetic hypersensitivity", None, "E-B", ["PMID:27498564"])],
             4, [{"name": "VGLUT2-lineage glutamatergic neurons (cell class, not a receptor)",
                  "species": "mmus", "identifier": None, "ortholog_relation": None}],
             ["PMID:27498564"],
             "anaesthetic-induced failure of excitatory presynaptic release at a reduced metabolic reserve",
             None),
    ])

# ================================================================ 3) mouse volatile c10 — TESTED_NEGATIVE
put('S5_ga_volatile_mmus', 10,
    coverage="TESTED_NEGATIVE", status="NEGATIVE", applicability="APPLICABLE",
    discovery_route="MOLECULE_SYSTEM_FIRST",
    roles_present=[], roles_tested_negative=["CONTROLS_ENTRY"],
    ambiguity=("A TRUE NEGATIVE WITH A POSITIVE INTERNAL CONTROL, which is what makes it "
               "interpretable. The same knockout, in the same experiment, DID shift diethyl ether "
               "sensitivity by 12%, so the assay could detect a shift; it detected none for "
               "isoflurane or halothane, the two agents in this row's frozen agent scope. Locomotion "
               "was normal, excluding a floor effect. The result is agent-specific, not "
               "mechanism-refuting: stomatin/UNC-1 matters for ether in both phyla and not for the "
               "halogenated agents in either."),
    strongest_grade="E-A", all_grades=["E-A"],
    negative_assay_statement=("EC50 for loss of response to tail clamp was determined in stomatin-"
                             "knockout and parental mice under continuous flows of diethyl ether, "
                             "halothane and isoflurane. A 12% sensitivity increase was resolved for "
                             "diethyl ether; no significant change was resolved for halothane or "
                             "isoflurane. The assay therefore had demonstrated power to detect a "
                             "shift of that size in the same animals."),
    mechanisms=[
        mech("Stomatin (mammalian homologue of C. elegans UNC-1) is NOT required for isoflurane or "
             "halothane sensitivity in mouse",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:16931982"],
               "basis": "TESTED AND NEGATIVE for the agents in this row's scope. Listed under "
                        "roles_tested_negative, not roles_present."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
               "agent": "diethyl ether; halothane; isoflurane",
               "observed_effect": {"total_quiescence": "no_change", "state_structure": "not_reported",
                                   "entry_threshold": "no_change", "survival_recovery": "not_reported",
                                   "other": "+12% sensitivity to diethyl ether (POSITIVE internal "
                                            "control); no significant change for halothane or "
                                            "isoflurane; no locomotor defect; the same agent pattern "
                                            "holds in C. elegans unc-1 mutants"},
               "context_dependence": "agent_dependent", "statement": S_STOM,
               "evidence_grade": "E-A", "citation_ids": ["PMID:16931982"]}],
             "NO_ESTABLISHED_EFFECT",
             [ch("stomatin deletion", 10, "E-A", ["PMID:16931982"]),
              ch("no change in halogenated-anaesthetic EC50", None, "E-A", ["PMID:16931982"])],
             10, [{"name": "Stomatin (Stom)", "species": "mmus", "identifier": None,
                   "ortholog_relation": "Direct homologue of C. elegans UNC-1, which IS load-bearing "
                                        "for volatile-anaesthetic phenotype in the worm row. "
                                        "ORTHOLOGOUS_MOLECULE, and the cross-species agreement is on "
                                        "the AGENT PATTERN (ether yes, halogenated no) rather than on "
                                        "a single phenotype."}],
             ["PMID:16931982"],
             "no resolvable change in membrane-protein-dependent anaesthetic potency for halogenated agents",
             {"level": "ORTHOLOGOUS_MOLECULE", "partner": "S5_ga_volatile_cele (unc-1)",
              "justification": "Same gene family, both phyla tested with the same endpoint logic, "
                               "and the agent-specific pattern replicates across the phylogenetic "
                               "boundary. A rare case where a NEGATIVE replicates cross-species."}),
    ])

# ================================================================ 4) mouse volatile c7 — PZ GABA
put('S5_ga_volatile_mmus', 7,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="SPECIES_ENDPOINT_FIRST",
    roles_present=["CONTROLS_ENTRY", "ENABLES_EXIT"], roles_tested_negative=[],
    ambiguity=("BEHAVIOURAL-EEG DISSOCIATION, stated by the authors: ablation shifted the "
               "behavioural (righting) endpoint but did NOT produce EEG signatures of anaesthetic "
               "resistance. So the circuit controls the motor/hypnotic endpoint rather than the "
               "cortical signature, and the two phenotype axes separate. This is exactly the case "
               "the frozen three-axis rule exists to keep visible: A_beh moved, A_neu did not."),
    strongest_grade="E-A", all_grades=["E-A"], negative_assay_statement=None,
    mechanisms=[
        mech("Parafacial-zone GABAergic neurons are required for volatile-anaesthetic hypnosis",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"],
               "basis": "Caspase ablation gives durable behavioural resistance to two agents, dose-"
                        "graded against surviving neuron number."},
              {"role": "ENABLES_EXIT", "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"],
               "basis": "Ablated mice emerged from isoflurane significantly faster with purposeful "
                        "movement - an exit-kinetics phenotype measured separately from induction."}],
             [{"manipulation": "ablation", "direction_of_manipulation": "remove",
               "agent": "isoflurane; sevoflurane",
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "not_reported",
                                   "entry_threshold": "increase", "survival_recovery": "increase",
                                   "other": "~50% higher likelihood of intact righting; resistance "
                                            "inversely correlated with surviving PZGABA neuron count; "
                                            "hypnotic isoflurane tripled c-Fos in PZGABA neurons; NO "
                                            "EEG signature of anaesthetic resistance"},
               "context_dependence": "none_reported", "statement": S_PZ,
               "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"]}],
             "PROMOTES_STATE",
             [ch("AAV-caspase ablation of parafacial GABAergic neurons", 7, "E-A", ["PMID:40240218"]),
              ch("loss of a brainstem NREM-promoting node", 7, "E-A", ["PMID:40240218"]),
              ch("behavioural resistance to isoflurane- and sevoflurane-induced hypnosis; faster "
                 "emergence", None, "E-A", ["PMID:40240218"])],
             7, [{"name": "parafacial zone GABAergic neurons (PZGABA)", "species": "mmus",
                  "identifier": None, "ortholog_relation": None}],
             ["PMID:40240218"],
             "removal of a GABAergic brainstem node that is depolarised by hypnotic doses of volatile agent",
             None),
    ])

# ================================================================ 5) mouse NREM c7 — the matching NEGATIVE
put('S4_deep_mmus', 7,
    coverage="TESTED_NEGATIVE", status="NEGATIVE", applicability="APPLICABLE",
    discovery_route="SPECIES_ENDPOINT_FIRST",
    roles_present=[], roles_tested_negative=["PRODUCES_STATE", "MAINTAINS_STATE", "CONTROLS_ENTRY"],
    ambiguity=("THE MOST INFORMATIVE SINGLE RESULT OF THIS ROUND, and it is a negative. The SAME "
               "ablation, in the SAME animals, in the SAME paper, is POSITIVE for volatile "
               "anaesthesia (S5_ga_volatile_mmus c7) and NEGATIVE for natural NREM sleep: no change "
               "in sleep amount, no change in wakefulness, no change in homeostatic sleep drive after "
               "deprivation. A node of the sleep-promoting circuitry is thus REQUIRED for the "
               "drug-induced state and DISPENSABLE for the endogenous one. SCOPE: this is one node, "
               "not the circuit class; it does not license any statement that sleep circuitry in "
               "general is dispensable for NREM."),
    strongest_grade="E-A", all_grades=["E-A"],
    negative_assay_statement=("EEG-defined sleep was measured in PZGABA-ablated and mCherry control "
                             "mice, as was the homeostatic drive to sleep after sleep deprivation. "
                             "Ablation of up to 70-80% of PZGABA neurones did not alter the amount of "
                             "endogenous sleep or wakefulness and did not affect homeostatic sleep "
                             "drive. The same animals showed a large, dose-graded anaesthetic "
                             "phenotype, so the preparation had demonstrated power."),
    mechanisms=[
        mech("Parafacial-zone GABAergic neurons are NOT required for the amount of natural NREM sleep "
             "or for sleep homeostasis",
             [{"role": "MAINTAINS_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"],
               "basis": "TESTED AND NEGATIVE on sleep amount and on homeostatic rebound, with an "
                        "internal positive control in the same animals."}],
             [{"manipulation": "ablation", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "no_change", "state_structure": "no_change",
                                   "entry_threshold": "no_change", "survival_recovery": "not_reported",
                                   "other": "no insomnia; sleep pressure after deprivation unchanged; "
                                            "SAME animals behaviourally resistant to isoflurane and "
                                            "sevoflurane"},
               "context_dependence": "state_dependent", "statement": S_PZ_NEG,
               "evidence_grade": "E-A", "citation_ids": ["PMID:40240218"]}],
             "NO_ESTABLISHED_EFFECT",
             [ch("AAV-caspase ablation of parafacial GABAergic neurons", 7, "E-A", ["PMID:40240218"]),
              ch("no change in NREM amount or homeostatic drive", None, "E-A", ["PMID:40240218"])],
             7, [{"name": "parafacial zone GABAergic neurons (PZGABA)", "species": "mmus",
                  "identifier": None, "ortholog_relation": None}],
             ["PMID:40240218"],
             "no resolvable change in endogenous sleep amount or sleep pressure",
             {"level": "EXACT_MOLECULE", "partner": "S5_ga_volatile_mmus c7",
              "justification": "Not merely the same class - the same neurons, the same ablation, the "
                               "same animals, the same paper. The two rows differ only in which state "
                               "was assayed. This is the cleanest available demonstration that a "
                               "mechanism's causal role is a property of the STATE, not of the "
                               "mechanism."}),
    ])

# ================================================================ 6) GABA-A beta1 — REM and NREM
for row, which in (('S3_rem_mmus', 'REM'), ('S4_deep_mmus', 'NREM')):
    eff = ("decreased theta activity in REM sleep" if which == 'REM'
           else "increased delta power in NREM sleep")
    mm = mech("GABA-A receptor beta1 subunit shapes sleep oscillations without changing sleep amount",
              [{"role": "MAINTAINS_STATE", "evidence_grade": "E-B", "citation_ids": ["PMID:33942407"],
                "basis": "Germline knockout changes the spectral content of the state while leaving "
                         "its amount and the overall sleep-wake architecture unchanged - a "
                         "within-state organisation effect, not a state-generation effect."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "no_change", "state_structure": "no_change",
                                    "entry_threshold": "not_reported", "survival_recovery": "not_reported",
                                    "other": eff + "; overall sleep-wake architecture UNCHANGED; "
                                             "highest beta1 binding in hippocampus and frontal cortex"},
                "context_dependence": "none_reported", "statement": S_B1,
                "evidence_grade": "E-B", "citation_ids": ["PMID:33942407"]}],
              "NO_ESTABLISHED_EFFECT",
              [ch("Gabrb1 deletion", 3, "E-B", ["PMID:33942407"]),
               ch("altered spectral power within the state", None, "E-B", ["PMID:33942407"])],
              3, [{"name": "Gabrb1 (GABA-A receptor beta1 subunit)", "species": "mmus",
                   "identifier": None, "ortholog_relation": None}],
              ["PMID:33942407"],
              "altered inhibitory conductance in hippocampus and frontal cortex changing network "
              "oscillation frequency content",
              None)
    note = ("AXIS SEPARATION. This manipulation moves A_neu (dynamical organisation: spectral power) "
            "with NO movement in A_beh or in state amount. Under the frozen three-axis rule it is a "
            "positive on one axis and a negative on the others, and it is the clearest case yet that "
            "'affects the state' must be axis-qualified. The authors state the subunit 'does not play "
            "an important role in sleep initiation or maintenance'.")
    f = os.path.join(D, row + '.json')
    dd = json.load(open(f))
    tgt = [c for c in dd['cells'] if c['class_id'] == 3][0]
    if tgt['coverage'] == 'NOT_TESTED':
        put(row, 3, coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
            discovery_route="CLASS_FIRST", roles_present=["MAINTAINS_STATE"],
            roles_tested_negative=["PRODUCES_STATE", "CONTROLS_ENTRY"],
            ambiguity=note, strongest_grade="E-B", all_grades=["E-B"],
            negative_assay_statement=("Sleep-wake architecture was scored in the same recordings that "
                                      "resolved the spectral changes; no change in overall architecture "
                                      "was detected, so the assay had power for both readouts."),
            mechanisms=[mm])
    else:
        add_mech(row, 3, mm, note=note, extra_roles=["MAINTAINS_STATE"], grade="E-B")

# ================================================================ 7) mouse REM c6 — cholinergic + orexin
put('S3_rem_mmus', 6,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["PRODUCES_STATE", "CONTROLS_ENTRY"], roles_tested_negative=["MAINTAINS_STATE"],
    ambiguity=("ENTRY WITHOUT MAINTENANCE, measured in the same experiment: optogenetic activation of "
               "PPT/LDT cholinergic neurons during NREM increased the NUMBER of REM episodes and did "
               "NOT change episode DURATION. Under the frozen role axis that is CONTROLS_ENTRY plus a "
               "sufficiency claim (PRODUCES_STATE), with MAINTAINS_STATE explicitly tested and "
               "negative. Very few manipulations anywhere in this table separate the two so cleanly. "
               "The orexin line adds a second, opposite-signed class-6 mechanism in the same row."),
    strongest_grade="E-A", all_grades=["E-A"], negative_assay_statement=None,
    mechanisms=[
        mech("Cholinergic PPT/LDT neurons are sufficient to induce REM sleep from NREM",
             [{"role": "PRODUCES_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:25548191"],
               "basis": "'Activation ... during NREM sleep was sufficient to induce REM sleep.' "
                        "A sufficiency demonstration, which is what PRODUCES_STATE requires."},
              {"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:25548191"],
               "basis": "The measured effect is on episode NUMBER, i.e. on transition rate into the "
                        "state."}],
             [{"manipulation": "optogenetic_activation", "direction_of_manipulation": "increase",
               "agent": None,
               "observed_effect": {"total_quiescence": "increase", "state_structure": "increase",
                                   "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                   "other": "number of REM episodes increased; REM episode DURATION "
                                            "unchanged; effect obtained in both PPT and LDT"},
               "context_dependence": "state_dependent", "statement": S_PPT,
               "evidence_grade": "E-A", "citation_ids": ["PMID:25548191"]}],
             "PROMOTES_STATE",
             [ch("optogenetic activation of cholinergic mesopontine neurons", 6, "E-A", ["PMID:25548191"]),
              ch("increased rate of NREM-to-REM transitions", None, "E-A", ["PMID:25548191"])],
             6, [{"name": "ChAT-positive PPT/LDT neurons; acetylcholine", "species": "mmus",
                  "identifier": None,
                  "ortholog_relation": "Acetylcholine also carries the human anaesthesia class-6 "
                                       "entries (physostigmine reversal and induction-dose shift), "
                                       "but there the direction is anti-state. SAME_PHYSICAL_CLASS "
                                       "with OPPOSITE sign across state and species."}],
             ["PMID:25548191"],
             "cholinergic depolarisation of REM-generating pontine circuitry raising transition probability",
             None),
        mech("Orexin signalling restrains REM intrusion; OX2R-independent pathways are also required",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:12797957"],
               "basis": "Two germline genotypes dissociate: OX2R loss gives mild cataplexy-like REM "
                        "attacks, full orexin loss gives severe ones."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "increase", "state_structure": "decrease",
                                   "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                   "other": "OX2R-/- MILDLY affected by cataplexy-like REM attacks; "
                                            "orexin-/- SEVERELY affected; both equally affected by "
                                            "non-REM sleep attacks"},
               "context_dependence": "receptor_subtype_dependent", "statement": S_OX,
               "evidence_grade": "E-A", "citation_ids": ["PMID:12797957"]}],
             "OPPOSES_STATE",
             [ch("orexin or OX2R deletion", 6, "E-A", ["PMID:12797957"]),
              ch("loss of excitation of monoaminergic wake-promoting neurons", 6, "E-A",
                 ["PMID:12797957"]),
              ch("REM intrusion into wakefulness", None, "E-A", ["PMID:12797957"])],
             6, [{"name": "orexin (hypocretin) and OX2R", "species": "mmus", "identifier": None,
                  "ortholog_relation": None}],
             ["PMID:12797957"],
             "loss of peptidergic excitatory tone that normally holds REM-generating circuitry gated",
             None),
    ])

# ================================================================ 8) mouse NREM c6 — orexin + adenosine
put('S4_deep_mmus', 6,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["CONTROLS_ENTRY"], roles_tested_negative=[],
    ambiguity=("Two independent class-6 mechanisms with different scopes. (i) OX2R governs the "
               "wake/NREM transition: 'normal regulation of wake/non-REM sleep transitions depends "
               "critically upon OX2R activation'. (ii) CD73-derived extracellular adenosine is "
               "required for the HOMEOSTATIC RESPONSE to sleep loss but not for baseline NREM - "
               "CD73-KO mice sleep MORE at baseline yet show no rebound after deprivation, while "
               "IL1beta still increases their NREM. That is a dissociation between the state and its "
               "homeostatic controller, and the IL1beta arm is the positive control that makes the "
               "null interpretable."),
    strongest_grade="E-A", all_grades=["E-A"], negative_assay_statement=None,
    mechanisms=[
        mech("OX2R activation is required for normal wake-to-NREM transition control",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:12797957"],
               "basis": "Germline receptor deletion produces abnormal attacks of non-REM sleep and "
                        "disrupted wakefulness; the authors attribute wake/non-REM transition control "
                        "specifically to OX2R."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "increase", "state_structure": "decrease",
                                   "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                   "other": "behaviourally abnormal non-REM 'sleep attacks'; OX2R loss "
                                            "eliminates orexin-evoked excitation of histaminergic "
                                            "neurons that gate non-REM sleep onset"},
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
        mech("CD73-derived extracellular adenosine is required for the homeostatic NREM response to "
             "sleep deprivation, not for baseline NREM",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:22540145"],
               "basis": "Knockout abolishes the deprivation-induced increase in NREM while baseline "
                        "NREM is if anything greater - an effect on the entry CONTROLLER, separable "
                        "from the state itself."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "increase", "state_structure": "decrease",
                                   "entry_threshold": "not_reported", "survival_recovery": "not_reported",
                                   "other": "baseline NREMS GREATER in KO; no NREMS enhancement after "
                                            "sleep deprivation; IL1beta still enhanced NREMS in KO "
                                            "(positive control); 1.0-2.5 Hz power rise after "
                                            "deprivation smaller in KO; REM unchanged in all conditions"},
               "context_dependence": "challenge_dependent", "statement": S_CD73,
               "evidence_grade": "E-A", "citation_ids": ["PMID:22540145"]}],
             "PROMOTES_STATE",
             [ch("Nt5e/CD73 deletion", 6, "E-A", ["PMID:22540145"]),
              ch("loss of extracellular AMP-to-adenosine conversion", 6, "E-A", ["PMID:22540145"]),
              ch("absent homeostatic NREM rebound", None, "E-A", ["PMID:22540145"])],
             6, [{"name": "CD73 / Nt5e 5'-ectonucleotidase; extracellular adenosine", "species": "mmus",
                  "identifier": None, "ortholog_relation": None}],
             ["PMID:22540145"],
             "loss of activity-dependent extracellular adenosine accumulation that normally raises "
             "sleep propensity",
             None),
    ])

# ================================================================ 9) worm lethargus c5 — DGK-1
put('S2_core_cele', 5,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["PRODUCES_STATE", "CONTROLS_ENTRY"], roles_tested_negative=[],
    ambiguity=("CLASS ASSIGNMENT IS A JUDGEMENT AND IS STATED AS SUCH. DGK-1 and PKC-1 are not "
               "release proteins themselves; they are the canonical upstream regulators of "
               "diacylglycerol-dependent UNC-13 priming, i.e. of the release machinery that defines "
               "class 5. The paper localises the requirement to cholinergic neurons by rescue, which "
               "is a release-machinery context. Assigned to class 5 as the proximal class with class "
               "6 upstream; an alternative reading places it in class 6. The counterbalance result "
               "(pkc-1 mutation SUPPRESSES the dgk-1 phenotype, and pkc-1's own excessive sleep is "
               "also suppressed) means the pathway is bidirectional, not a simple promoter."),
    strongest_grade="E-A", all_grades=["E-A"], negative_assay_statement=None,
    mechanisms=[
        mech("Neuronal diacylglycerol kinase DGK-1, counterbalanced by PKC-1, is required for "
             "developmentally timed sleep",
             [{"role": "PRODUCES_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:37682636"],
               "basis": "Unbiased forward screen; two independent alleles map to the same gene; "
                        "cell-type-restricted transgenic rescue restores the phenotype."},
              {"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:37682636"],
               "basis": "Both developmentally timed and stress-induced quiescence are reduced, i.e. "
                        "the animal enters the state less."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "decrease",
                                   "entry_threshold": "increase", "survival_recovery": "decrease",
                                   "other": "isolated in an unbiased forward screen (rem8, rem10); "
                                            "pan-neuronal and/or cholinergic dgk-1 expression partly "
                                            "rescues; pkc-1 loss SUPPRESSES the dgk-1 phenotype and "
                                            "pkc-1's own excessive sleep; reduced post-stress survival"},
               "context_dependence": "cell_type_dependent", "statement": S_DGK,
               "evidence_grade": "E-A", "citation_ids": ["PMID:37682636"]}],
             "PROMOTES_STATE",
             [ch("dgk-1 loss of function in neurons", 5, "E-A", ["PMID:37682636"]),
              ch("elevated diacylglycerol and unopposed PKC-1 signalling at the release machinery", 5,
                 "E-A", ["PMID:37682636"]),
              ch("reduced developmentally timed and stress-induced quiescence", None, "E-A",
                 ["PMID:37682636"])],
             5, [{"name": "dgk-1 (diacylglycerol kinase); pkc-1 (nPKC)", "species": "cele",
                  "identifier": None,
                  "ortholog_relation": "DGKtheta/PKCepsilon orthologues. No mammalian sleep row in this "
                                       "table currently carries a DGK entry, so this is an explicit "
                                       "cross-species prediction rather than a correspondence."}],
             ["PMID:37682636"],
             "shifted diacylglycerol tone at the presynaptic priming step, altering neurotransmitter "
             "release in cholinergic neurons",
             None),
    ])

# ================================================================ 10) worm lethargus c6 — RPamides
add_mech('S2_core_cele', 6,
         mech("RPamide neuropeptides nlp-22 and nlp-23 are required for developmentally timed sleep "
              "but dispensable for stress-induced sleep",
              [{"role": "PRODUCES_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:38371321"],
                "basis": "New CRISPR alleles, double and triple mutants, resolving a linkage problem "
                         "that had confounded earlier analyses."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "decrease", "state_structure": "not_reported",
                                    "entry_threshold": "not_reported", "survival_recovery": "not_reported",
                                    "other": "nlp-22 and nlp-23 each required for developmentally timed "
                                             "sleep; nlp-2, nlp-22 and nlp-23 all DISPENSABLE for "
                                             "stress-induced sleep, tested as singles, double and triple"},
                "context_dependence": "state_dependent", "statement": S_NLP,
                "evidence_grade": "E-A", "citation_ids": ["PMID:38371321"]}],
              "PROMOTES_STATE",
              [ch("CRISPR deletion of nlp-22 and nlp-23", 6, "E-A", ["PMID:38371321"]),
               ch("loss of RPamide peptidergic signalling", 6, "E-A", ["PMID:38371321"]),
               ch("reduced developmentally timed sleep", None, "E-A", ["PMID:38371321"])],
              6, [{"name": "nlp-2, nlp-22, nlp-23 (RPamide neuropeptides)", "species": "cele",
                   "identifier": None, "ortholog_relation": None}],
              ["PMID:38371321"],
              "loss of peptidergic quiescence-promoting signalling onto locomotor circuitry",
              None),
         note=("A SECOND within-species state dissociation, alongside the PZGABA result in mouse: the "
               "same three peptides are required for developmentally timed sleep and dispensable for "
               "stress-induced sleep, tested to triple-mutant depth. Stress-induced sleep is NOT a "
               "committed row in this table, so the negative arm is recorded here as scope rather "
               "than scored. It is a concrete argument for adding that row."),
         extra_roles=["PRODUCES_STATE"], grade="E-A")

# ================================================================ 11) dauer c7 — sensory circuit
put('S7_dauer_cele', 7,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["CONTROLS_ENTRY"], roles_tested_negative=[],
    ambiguity=("SCOPE: the dauer readout is partial maintenance of reproductive growth in a daf-7 "
               "mutant background, i.e. a modifier experiment rather than a clean dauer-formation "
               "quantification in wild type. Direction is therefore 'modulates entry', and the "
               "evidence grade reflects that. EXP-1 is an EXCITATORY, cation-selective GABA receptor, "
               "so its presence here does NOT make this a class-3 inhibitory mechanism; the shared "
               "ligand is real and the ionic consequence is opposite, which is exactly the "
               "distinction SAME_PHYSICAL_CLASS is meant to carry."),
    strongest_grade="E-C", all_grades=["E-C"], negative_assay_statement=None,
    mechanisms=[
        mech("ASI and AWC chemosensory neurons, via EXP-1 and STR-2, modulate dauer entry through "
             "DAF-7/TGF-beta",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-C", "citation_ids": ["PMID:33712439"],
               "basis": "Genetic modifier experiment in a daf-7 background; ASI-expressed EXP-1 and "
                        "STR-2 partially maintain reproductive growth, i.e. partially suppress dauer "
                        "entry."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                   "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                   "other": "exp-1 mutants defective in responses to AWC-sensed odours, "
                                            "non-autonomously through ASI; in daf-7 mutants, "
                                            "ASI-expressed EXP-1 and STR-2 partially maintained "
                                            "reproductive growth"},
               "context_dependence": "genetic_background_dependent", "statement": S_DAUER,
               "evidence_grade": "E-C", "citation_ids": ["PMID:33712439"]}],
             "OPPOSES_STATE",
             [ch("loss of EXP-1 or STR-2 in ASI", 7, "E-C", ["PMID:33712439"]),
              ch("altered ASI-AWC chemosensory integration of food cues", 7, "E-C", ["PMID:33712439"]),
              ch("reduced DAF-7/TGF-beta neuroendocrine output", 9, "E-C", ["PMID:33712439"]),
              ch("shifted dauer-versus-reproductive-growth decision", None, "E-C", ["PMID:33712439"])],
             7, [{"name": "ASI and AWC amphid chemosensory neurons; EXP-1 (excitatory GABA receptor); "
                  "STR-2 (GPCR); DAF-7/TGF-beta", "species": "cele", "identifier": None,
                  "ortholog_relation": None}],
             ["PMID:33712439"],
             "sensory-neuron-level integration of food and population cues setting neuroendocrine "
             "output that gates the developmental decision",
             None),
    ])

# ================================================================ 12) L1 arrest c9 — HLH-30/TFEB
put('S6_starv_L1_cele', 9,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["MAINTAINS_STATE", "PROTECTS_THROUGH_STATE"], roles_tested_negative=[],
    ambiguity=("PREPRINT, NOT PEER REVIEWED (bioRxiv 2025.10.31.685810). Graded E-C on that ground "
               "alone and flagged; if it does not appear in a peer-reviewed venue this cell must be "
               "revisited. The scientific content is directly on-role: loss of HLH-30 does not "
               "prevent L1 arrest from being entered, it disrupts the MAINTENANCE of arrest - seam "
               "cell cycle arrest breaks down and developmental programs start prematurely under "
               "starvation - and separately reduces survival. Those are two distinct frozen roles and "
               "are recorded separately."),
    strongest_grade="E-C", all_grades=["E-C"], negative_assay_statement=None,
    mechanisms=[
        mech("HLH-30/TFEB maintains L1 starvation arrest and, with DAF-16/FOXO, supports survival "
             "through it",
             [{"role": "MAINTAINS_STATE", "evidence_grade": "E-C", "citation_ids": ["PMID:41279428"],
               "basis": "Loss of HLH-30 disrupts seam cell cycle arrest and causes premature "
                        "initiation of developmental programs DURING starvation - failure to hold the "
                        "state, not failure to enter it."},
              {"role": "PROTECTS_THROUGH_STATE", "evidence_grade": "E-C",
               "citation_ids": ["PMID:41279428"],
               "basis": "HLH-30 and DAF-16 collaborate to ensure survival under starvation, a "
                        "through-state protective function distinct from holding the arrest."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "decrease",
                                   "entry_threshold": "not_reported", "survival_recovery": "decrease",
                                   "other": "loss of fasting-induced 3D chromatin reorganisation; "
                                            "BLMP-1 overactivation; premature developmental programs; "
                                            "reciprocal regulation with DAF-16 localisation"},
               "context_dependence": "none_reported", "statement": S_HLH30,
               "evidence_grade": "E-C",
               "citation_ids": ["PMID:41279428"]}],
             "PROMOTES_STATE",
             [ch("hlh-30 loss of function", 9, "E-C", ["PMID:41279428"]),
              ch("failure of fasting-induced 3D chromatin reorganisation", 9, "E-C",
                 ["PMID:41279428"]),
              ch("BLMP-1 overactivation and premature developmental programs", 9, "E-C",
                 ["PMID:41279428"]),
              ch("breakdown of seam cell cycle arrest; reduced starvation survival", None, "E-C",
                 ["PMID:41279428"])],
             9, [{"name": "HLH-30/TFEB; DAF-16/FOXO; BLMP-1", "species": "cele", "identifier": None,
                  "ortholog_relation": "DAF-16/FOXO already carries the dauer row's class-9 entry. "
                                       "ORTHOLOGOUS_MOLECULE across the two worm arrest states, with "
                                       "HLH-30/TFEB as the added partner here."}],
             ["PMID:41279428"],
             "transcription-factor-dependent chromatin reorganisation that holds the cell cycle "
             "arrested while nutrients are absent",
             None),
    ])


# ---------------------------------------------------------------- report
print('APPLIED (%d):' % len(APPLIED))
for a in APPLIED:
    print('  ' + a)
print('SKIPPED (%d):' % len(SKIPPED))
for s in SKIPPED:
    print('  ' + s)
