"""PE-5 round-5 findings.

  30323068  UNC-7/UNC-9 innexins in developmentally timed sleep -> S2_core_cele c12
  21418043  connexin36 knockout mice, isoflurane and propofol   -> S5_ga_volatile_mmus c12
  18846209  unc-31 / OCR-2 TRPV and L1 starvation survival      -> S6_starv_L1_cele c1, c5

Class assignments here follow the FROZEN class table in REPERTOIRE.md verbatim: class 1 lists
"TRP leak" among its representative implementations, and class 5 lists "dense-core release (unc-31)".
Neither is a judgement call; both are named in the frozen definitions.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pe5_apply_findings import mech
from pe5_apply_r2 import put, add_mech, ch, APPLIED, SKIPPED

APPLIED.clear(); SKIPPED.clear()

S_INX = ("We report that loss of UNC-7 or UNC-9 innexin function dramatically reduced sleep and "
         "decreased arousal threshold during developmentally timed sleep in Caenorhabditis elegans. "
         "UNC-7 function was required in premotor interneurons and UNC-9 function was required in "
         "motor neurons in this paradigm. Simultaneous transient overexpression of UNC-7 and UNC-9 was "
         "sufficient to induce anachronistic sleep in adult animals. Moreover, loss of UNC-7 or UNC-9 "
         "suppressed the increased sleep of EGL-4 gain-of-function animals... diminished NCA channel "
         "activity in C. elegans robustly increased arousal thresholds during sleep bouts... Total time "
         "in sleep bouts was only modestly increased in animals lacking NCA channel auxiliary subunit "
         "UNC-79, whereas increased channel activity dramatically decreased sleep. Loss of EGL-4 or "
         "innexin proteins suppressed UNC-79 loss-of-function sleep and arousal defects... loss of the "
         "PDF receptor PDFR-1 did not suppress gain-of-function sleep defects.")
S_CX36 = ("We measured the sensitivity of connexin36 knockout mice to the hypnotic effects of "
          "isoflurane and propofol. The experimental endpoint was recovery of the righting reflex of "
          "the anaesthetised animals during 0.2% step-reductions in isoflurane concentration, or "
          "following intraperitoneal injection of propofol (100 mg.kg-1). Connexin36 knockout animals "
          "were more sensitive to the hypnotic effects of isoflurane than 'normal' wild-type animals. "
          "The half maximal effective concentration (EC50) for recovery of righting reflex was 0.37% "
          "for connexin36 knockout vs 0.49% for wild-type animals (p < 0.001). For propofol, "
          "connexin36 knockout animals showed more rapid loss of righting reflex than wild-type "
          "animals (mean (SD) 2.8 (0.13) vs 3.8 (0.27) min); and young (< 60 days) connexin36 knockout "
          "animals remained anaesthetised for longer than young wild-type mice (47.2 (2.9) vs 30.5 "
          "(1.7) min; p < 0.00001).")
S_OCR2 = ("We isolated mutations in unc-31, encoding a calcium-activated regulator of neural dense-core "
          "vesicle release, which conferred enhanced starvation survival. This extended survival was "
          "reminiscent of that seen in daf-2 insulin-signaling deficient mutants and was ultimately "
          "dependent on daf-16... Cell-specific rescue experiments identified a small subset of primary "
          "sensory neurons where unc-31 reconstitution modulated starvation survival, suggesting that "
          "these neurons mediate perception of food availability. We found that OCR-2, a transient "
          "receptor potential vanilloid (TRPV) channel that localizes to the cilia of this subset of "
          "neurons, regulates peptide-hormone secretion and L1 starvation survival. Moreover, "
          "inactivation of ocr-2 caused a significant extension in adult lifespan.")

# ================================================================ 1) worm lethargus c12
put('S2_core_cele', 12,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["PRODUCES_STATE", "MAINTAINS_STATE", "CONTROLS_ENTRY"], roles_tested_negative=[],
    ambiguity=("NECESSITY AND SUFFICIENCY IN ONE PAPER, which almost nothing else in this table has. "
               "Loss of UNC-7 or UNC-9 dramatically reduces sleep AND lowers arousal threshold; "
               "simultaneous transient OVEREXPRESSION of both is sufficient to induce anachronistic "
               "sleep in adults, outside the developmental window when it normally occurs. The "
               "epistasis is equally informative and is recorded in the chain: innexin loss suppresses "
               "both EGL-4 gain-of-function sleep and the unc-79 loss-of-function phenotype, placing "
               "gap junctions DOWNSTREAM of the cGMP-dependent kinase and of the NCA/NALCN channels. "
               "EXPLICIT NEGATIVE inside the same study: loss of the PDF receptor PDFR-1 did NOT "
               "suppress the gain-of-function sleep defect, ruling out the Drosophila PDF route by "
               "which narrow abdomen acts. CELL-TYPE SPECIFICITY: UNC-7 is required in premotor "
               "interneurons, UNC-9 in motor neurons - the two innexins are not interchangeable."),
    strongest_grade="E-A", all_grades=["E-A"], negative_assay_statement=None,
    mechanisms=[
        mech("UNC-7 and UNC-9 innexin gap junctions are necessary and sufficient for developmentally "
             "timed sleep and set arousal threshold, acting downstream of EGL-4 and the NCA channels",
             [{"role": "PRODUCES_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:30323068"],
               "basis": "Simultaneous transient overexpression of UNC-7 and UNC-9 induced "
                        "anachronistic sleep in ADULT animals, i.e. the state was generated outside "
                        "its normal developmental window. A sufficiency demonstration."},
              {"role": "MAINTAINS_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:30323068"],
               "basis": "Loss of either innexin decreased arousal threshold DURING sleep bouts - the "
                        "defining property of the state was degraded while the state was in progress."},
              {"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:30323068"],
               "basis": "Loss of either innexin dramatically reduced total sleep."}],
             [{"manipulation": "loss_of_function_and_overexpression",
               "direction_of_manipulation": "bidirectional", "agent": None,
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "decrease",
                                   "entry_threshold": "increase", "survival_recovery": "not_reported",
                                   "other": "loss of UNC-7 or UNC-9 dramatically reduced sleep and "
                                            "decreased arousal threshold; UNC-7 required in premotor "
                                            "interneurons, UNC-9 in motor neurons; joint transient "
                                            "overexpression SUFFICIENT to induce anachronistic adult "
                                            "sleep; innexin loss suppressed EGL-4 gain-of-function "
                                            "sleep and unc-79 loss-of-function defects; loss of NCA "
                                            "activity raised arousal threshold while increased NCA "
                                            "activity dramatically decreased sleep; PDFR-1 loss did "
                                            "NOT suppress the gain-of-function defect"},
               "context_dependence": "cell_type_dependent", "statement": S_INX,
               "evidence_grade": "E-A", "citation_ids": ["PMID:30323068"]}],
             "PROMOTES_STATE",
             [ch("EGL-4 cGMP-dependent protein kinase activity", 9, "E-A", ["PMID:30323068"]),
              ch("NCA/NALCN cation channel activity", 1, "E-A", ["PMID:30323068"]),
              ch("UNC-7 and UNC-9 innexin gap-junctional coupling in premotor interneurons and motor "
                 "neurons", 12, "E-A", ["PMID:30323068"]),
              ch("reduced behavioural quiescence and lowered arousal threshold", None, "E-A",
                 ["PMID:30323068"])],
             12, [{"name": "UNC-7 and UNC-9 innexins", "species": "cele", "identifier": None,
                   "ortholog_relation": "UNC-9 already carries this table's S5_ga_volatile_cele "
                                        "class-12 entry, where it SUPPRESSES unc-79/unc-80 halothane "
                                        "hypersensitivity. Same molecule, two states, and in both it "
                                        "sits epistatically downstream of the NCA/NALCN complex - but "
                                        "with opposite phenotypic sign."}],
             ["PMID:30323068"],
             "electrical coupling between premotor interneurons and motor neurons that sets the "
             "network's responsiveness to external stimuli",
             {"level": "EXACT_MOLECULE", "partner": "S5_ga_volatile_cele c12 (unc-9)",
              "justification": "The same gene, in the same species, is load-bearing for natural "
                               "developmentally timed sleep and for volatile-anaesthetic sensitivity, "
                               "and in BOTH cases it is placed epistatically downstream of the "
                               "NCA/NALCN complex. This is the strongest same-species, two-state, "
                               "same-epistatic-position correspondence the table contains."}),
    ])

# ================================================================ 2) mouse volatile c12
put('S5_ga_volatile_mmus', 12,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["CONTROLS_ENTRY", "MAINTAINS_STATE"], roles_tested_negative=[],
    ambiguity=("DIRECTION IS THE INTERESTING PART AND IT IS COUNTER-INTUITIVE. The paper's own framing "
               "is that gap-junction blockade might CAUSE unconsciousness; the result is that removing "
               "connexin36 makes animals MORE sensitive to anaesthetic, i.e. intact electrical coupling "
               "OPPOSES the anaesthetised state rather than mediating it. Effect sizes are real but "
               "modest for isoflurane (EC50 0.37% vs 0.49%) and the authors say so ('moderately "
               "enhanced'). TWO ROLES FROM TWO ENDPOINTS: the isoflurane EC50 and the propofol "
               "induction time are entry measures, while 'young knockouts remained anaesthetised for "
               "longer' (47.2 vs 30.5 min) is a maintenance/duration measure, and that one is "
               "AGE-RESTRICTED to animals under 60 days. AGENT SCOPE: propofol data are recorded here "
               "because they came from the same animals, but they do not license a human propofol-row "
               "entry - different species."),
    strongest_grade="E-A", all_grades=["E-A"], negative_assay_statement=None,
    mechanisms=[
        mech("Connexin36 electrical coupling opposes anaesthetic hypnosis in mouse",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:21418043"],
               "basis": "Germline knockout lowers the isoflurane EC50 for recovery of righting "
                        "(0.37% vs 0.49%, p<0.001) and shortens propofol induction time."},
              {"role": "MAINTAINS_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:21418043"],
               "basis": "Young knockouts remained anaesthetised for longer after a fixed propofol "
                        "dose (47.2 vs 30.5 min, p<0.00001) - duration of the state, measured "
                        "separately from its onset."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
               "agent": "isoflurane; propofol 100 mg/kg i.p.",
               "observed_effect": {"total_quiescence": "increase", "state_structure": "not_reported",
                                   "entry_threshold": "decrease", "survival_recovery": "decrease",
                                   "other": "isoflurane EC50 for recovery of righting 0.37% (KO) vs "
                                            "0.49% (WT), p<0.001; propofol loss of righting 2.8 vs 3.8 "
                                            "min; anaesthesia duration in animals <60 days 47.2 vs "
                                            "30.5 min, p<0.00001; duration effect AGE-RESTRICTED"},
               "context_dependence": "age_dependent", "statement": S_CX36,
               "evidence_grade": "E-A", "citation_ids": ["PMID:21418043"]}],
             "OPPOSES_STATE",
             [ch("Gjd2/connexin36 deletion", 12, "E-A", ["PMID:21418043"]),
              ch("loss of interneuronal electrical coupling", 12, "E-A", ["PMID:21418043"]),
              ch("lower anaesthetic concentration sufficient for loss of righting", None, "E-A",
                 ["PMID:21418043"])],
             12, [{"name": "Connexin36 (Gjd2)", "species": "mmus", "identifier": None,
                   "ortholog_relation": "Connexins and innexins are NOT homologous - they are "
                                        "convergently evolved gap-junction proteins. The worm class-12 "
                                        "entries (unc-9, inx-6) therefore share only the PHYSICAL "
                                        "class with this one. That is exactly what "
                                        "SAME_PHYSICAL_CLASS is for, and it is the sharpest "
                                        "illustration in the table of why molecular resolution has to "
                                        "be recorded per pair rather than assumed from a class label."}],
             ["PMID:21418043"],
             "loss of electrical coupling between interneurons, lowering the network's resistance to "
             "anaesthetic-induced state transition",
             {"level": "SAME_PHYSICAL_CLASS", "partner": "S5_ga_volatile_cele c12 (unc-9 innexin)",
              "justification": "Connexins (chordates) and innexins (invertebrates) are convergent, not "
                               "orthologous. Both rows show gap-junction manipulation changing "
                               "volatile-anaesthetic sensitivity, but no molecular correspondence may "
                               "be claimed - and the signs differ, since unc-9 loss SUPPRESSES "
                               "hypersensitivity in worm while Gjd2 loss CAUSES hypersensitivity in "
                               "mouse."}),
    ])

# ================================================================ 3) L1 arrest c1 — TRPV leak
put('S6_starv_L1_cele', 1,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="MOLECULE_SYSTEM_FIRST",
    roles_present=["PROTECTS_THROUGH_STATE"], roles_tested_negative=[],
    ambiguity=("CLASS ASSIGNMENT IS DIRECT, NOT INFERRED: the frozen class-1 definition names 'TRP "
               "leak' among its representative implementations, and OCR-2 is a TRPV channel. "
               "DIRECTION: inactivating ocr-2 EXTENDS starvation survival, so the channel's normal "
               "activity SHORTENS it - the wild-type gene opposes survival through the state. The "
               "mechanism is sensory rather than cell-autonomous: OCR-2 sits in the cilia of a small "
               "subset of primary sensory neurons and regulates peptide-hormone secretion, so the "
               "channel reports food availability rather than executing the arrest. SPECIFICITY "
               "CONTROL, and it is a strong one: the survival extension is daf-16 dependent, yet "
               "insulin-independent pathways that also control metabolism, adult lifespan and dauer "
               "formation did NOT promote starvation survival - the authors conclude starvation "
               "survival is a DISTINCT programme, not a generic stress-resistance readout."),
    strongest_grade="E-A", all_grades=["E-A"], negative_assay_statement=None,
    mechanisms=[
        mech("OCR-2 TRPV channel in sensory-neuron cilia couples food perception to L1 starvation "
             "survival via dense-core peptide release",
             [{"role": "PROTECTS_THROUGH_STATE", "evidence_grade": "E-A",
               "citation_ids": ["PMID:18846209"],
               "basis": "Channel inactivation significantly extends survival through L1 arrest, so "
                        "the channel sets how long the arrested animal persists. Scored as "
                        "PROTECTS_THROUGH_STATE with polarity OPPOSES, because the wild-type activity "
                        "reduces rather than increases through-state survival."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                   "entry_threshold": "not_reported", "survival_recovery": "increase",
                                   "other": "ocr-2 inactivation extends L1 starvation survival and "
                                            "adult lifespan; OCR-2 localises to cilia of a small "
                                            "subset of primary sensory neurons and regulates "
                                            "peptide-hormone secretion; the parallel unc-31 phenotype "
                                            "is daf-16 dependent; insulin-INDEPENDENT pathways "
                                            "controlling metabolism, lifespan and dauer did NOT "
                                            "promote starvation survival"},
               "context_dependence": "cell_type_dependent", "statement": S_OCR2,
               "evidence_grade": "E-A", "citation_ids": ["PMID:18846209"]}],
             "OPPOSES_STATE",
             [ch("ocr-2 TRPV channel inactivation in ciliated sensory neurons", 1, "E-A",
                 ["PMID:18846209"]),
              ch("reduced dense-core vesicle peptide-hormone secretion", 5, "E-A", ["PMID:18846209"]),
              ch("reduced insulin-like signalling and DAF-16/FOXO activation", 9, "E-A",
                 ["PMID:18846209"]),
              ch("extended survival of L1 starvation arrest", None, "E-A", ["PMID:18846209"])],
             1, [{"name": "OCR-2 (TRPV channel)", "species": "cele", "identifier": None,
                  "ortholog_relation": "Every other class-1 entry in this table is a NALCN-complex "
                                       "component. This is the only TRP entry, and the frozen class "
                                       "definition admits it explicitly ('TRP leak'). No NALCN "
                                       "correspondence is claimed."}],
             ["PMID:18846209"],
             "ciliary cation influx in food-sensing neurons driving peptide release that shortens "
             "survivable arrest",
             None),
    ])

# ================================================================ 4) L1 arrest c5 — unc-31
add_mech('S6_starv_L1_cele', 5,
         mech("UNC-31/CAPS-dependent dense-core vesicle release in a small subset of sensory neurons "
              "limits L1 starvation survival",
              [{"role": "PROTECTS_THROUGH_STATE", "evidence_grade": "E-A",
                "citation_ids": ["PMID:18846209"],
                "basis": "Mutations isolated in a forward screen for enhanced starvation survival; "
                         "cell-specific rescue localises the requirement to a small subset of primary "
                         "sensory neurons; the effect is daf-16 dependent."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                    "entry_threshold": "not_reported", "survival_recovery": "increase",
                                    "other": "unc-31 mutations conferred ENHANCED starvation survival, "
                                             "resembling daf-2 insulin-signalling mutants and "
                                             "ultimately dependent on daf-16; cell-specific "
                                             "reconstitution in a small subset of primary sensory "
                                             "neurons was sufficient to modulate survival"},
                "context_dependence": "cell_type_dependent", "statement": S_OCR2,
                "evidence_grade": "E-A", "citation_ids": ["PMID:18846209"]}],
              "OPPOSES_STATE",
              [ch("unc-31 loss of function", 5, "E-A", ["PMID:18846209"]),
               ch("reduced calcium-activated dense-core vesicle release in food-sensing neurons", 5,
                  "E-A", ["PMID:18846209"]),
               ch("reduced insulin-like peptide signalling; DAF-16 nuclear activity", 9, "E-A",
                  ["PMID:18846209"]),
               ch("extended L1 starvation survival", None, "E-A", ["PMID:18846209"])],
              5, [{"name": "UNC-31 / CAPS (calcium-activated protein for secretion)", "species": "cele",
                   "identifier": None,
                   "ortholog_relation": "The frozen class-5 definition names unc-31 explicitly as the "
                                        "dense-core release implementation of this class."}],
              ["PMID:18846209"],
              "reduced peptide-hormone output from food-sensing neurons, lowering insulin-like "
              "signalling during arrest",
              None),
         note=("A SECOND, INDEPENDENT ROUTE INTO THIS CELL and it points the opposite way from the "
               "dgk-1 mechanism already recorded here. dgk-1 RESTRAINS synaptic transmission to PERMIT "
               "arrest; unc-31 loss REDUCES dense-core release and EXTENDS survival. Both are release "
               "machinery, both change starvation outcome, and the two sit on different secretory "
               "pathways (small clear vesicle versus dense-core), which is why class 5 must not be "
               "summarised by a single direction. The paper's own specificity control is worth "
               "keeping: insulin-independent pathways that govern metabolism, adult lifespan and dauer "
               "formation did NOT promote starvation survival, so this is a state-specific programme "
               "and not general stress resistance."),
         extra_roles=["PROTECTS_THROUGH_STATE"], grade="E-A")

print('APPLIED (%d):' % len(APPLIED))
for a in APPLIED:
    print('  ' + a)
print('SKIPPED (%d):' % len(SKIPPED))
for s in SKIPPED:
    print('  ' + s)
