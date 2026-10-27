"""PE-5 round-6 findings.

  32958651  melatonin -> PCDR-1 -> Gbeta-gamma -> SLO-1 BK channel   -> S2_core_cele c2
  12962913  N-type Ca2+ channel knockout, halothane vs propofol      -> S5_ga_volatile_mmus c5

NOT APPLIED, and the reason is recorded here rather than silently dropped:
  42161335  glr-5 ionotropic glutamate receptor in STRESS-INDUCED SLEEP. Stress-induced sleep is a
            different state from developmentally timed sleep (lethargus) and is NOT a committed row
            in this table. Scoring it under S2_core_cele would be a state-substitution error of
            exactly the kind INCLUSION_CRITERION.md forbids. It is the THIRD paper in this run to
            argue for committing a stress-induced-sleep row (with PMID:38371321 and PMID:37682636).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pe5_apply_findings import mech
from pe5_apply_r2 import put, add_mech, ch, APPLIED, SKIPPED

APPLIED.clear(); SKIPPED.clear()

S_MEL = ("We identified the Caenorhabditis elegans BK channel SLO-1 as a molecular target of the Mel "
         "receptor PCDR-1. Knockout of pcdr-1, slo-1, or homt-1 (a gene required for Mel synthesis) "
         "causes substantially increased neurotransmitter release and shortened sleep duration, and "
         "these effects are nonadditive in double knockouts. Exogenous Mel inhibits neurotransmitter "
         "release and promotes sleep in wild-type (WT) but not pcdr-1 and slo-1 mutants. In a "
         "heterologous expression system, Mel activates the human BK channel (hSlo1) in a "
         "membrane-delimited manner in the presence of the Mel receptor MT1 but not MT2. A peptide "
         "acting to release free Gbeta-gamma also activates hSlo1 in a MT1-dependent and "
         "membrane-delimited manner, whereas a Gbeta-gamma inhibitor abolishes the stimulating effect "
         "of Mel.")
S_CAV = ("We examined the sensitivity to halothane in mice lacking the N-type Ca2+ channel, a major "
         "contributor of presynaptic neurotransmitter release. Sensitivity to halothane was "
         "significantly increased in the knockout mice compared with the wild-type littermates. "
         "Halothane also depressed field excitatory postsynaptic potentials recorded from the Schaffer "
         "collateral-CA1 hippocampal synapses more greatly in the knockout mice. We further examined "
         "sleep time induced by injection of propofol, an intravenous anesthetic that mainly affects "
         "inhibitory synaptic transmission. In contrast, sensitivity to propofol was significantly "
         "decreased in the knockout mice. We suggest that inhibition of the N-type Ca2+ channel "
         "underlies mechanisms of halothane anesthesia but counteracts propofol anesthesia.")

# ================================================================ 1) worm lethargus c2 — SLO-1
put('S2_core_cele', 2,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["MAINTAINS_STATE", "PRODUCES_STATE"], roles_tested_negative=[],
    ambiguity=("STATE-IDENTIFICATION SCOPE, stated first because it is the real limitation. The "
               "abstract reports 'shortened sleep duration' without naming the paradigm, so whether "
               "the measurement is developmentally timed sleep (this row's state) or another C. "
               "elegans quiescent state is not established from the abstract. Graded E-B rather than "
               "E-A for that reason alone; the genetics and the epistasis are otherwise first-rate. "
               "THE EPISTASIS IS THE STRENGTH: knockouts of the ligand-synthesis gene (homt-1), the "
               "receptor (pcdr-1) and the channel (slo-1) each shorten sleep, and the effects are "
               "NON-ADDITIVE in double mutants, which places all three on one pathway rather than "
               "three parallel ones. Exogenous melatonin promotes sleep in wild type but NOT in pcdr-1 "
               "or slo-1 mutants - an epistatic negative that pins the ligand's action to that "
               "receptor and that channel. The human hSlo1/MT1 arm is HETEROLOGOUS EXPRESSION and is "
               "recorded as such; it does not qualify as organism-level evidence and is not scored in "
               "any human row."),
    strongest_grade="E-B", all_grades=["E-B"], negative_assay_statement=None,
    mechanisms=[
        mech("Melatonin acts through the PCDR-1 receptor and G-beta-gamma to open the SLO-1 BK channel, "
             "suppressing neurotransmitter release and lengthening sleep",
             [{"role": "MAINTAINS_STATE", "evidence_grade": "E-B", "citation_ids": ["PMID:32958651"],
               "basis": "Loss of the channel, the receptor or the ligand shortens sleep DURATION - "
                        "the state is entered but not held."},
              {"role": "PRODUCES_STATE", "evidence_grade": "E-B", "citation_ids": ["PMID:32958651"],
               "basis": "Exogenous melatonin PROMOTES sleep in wild type, and fails to do so in pcdr-1 "
                        "or slo-1 mutants. Sufficiency, conditional on the pathway being intact."}],
             [{"manipulation": "loss_of_function_and_pharmacological_activation",
               "direction_of_manipulation": "bidirectional", "agent": "exogenous melatonin",
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "decrease",
                                   "entry_threshold": "increase", "survival_recovery": "not_reported",
                                   "other": "pcdr-1, slo-1 and homt-1 knockouts each substantially "
                                            "INCREASE neurotransmitter release and SHORTEN sleep; "
                                            "effects NON-ADDITIVE in double knockouts; exogenous "
                                            "melatonin inhibits release and promotes sleep in wild "
                                            "type but not in pcdr-1 or slo-1 mutants; in heterologous "
                                            "expression melatonin activates human hSlo1 via MT1 but "
                                            "NOT MT2, membrane-delimited, abolished by a "
                                            "Gbeta-gamma inhibitor"},
               "context_dependence": "pathway_dependent", "statement": S_MEL,
               "evidence_grade": "E-B", "citation_ids": ["PMID:32958651"]}],
             "PROMOTES_STATE",
             [ch("melatonin synthesis (homt-1) and release", 6, "E-B", ["PMID:32958651"]),
              ch("PCDR-1 melatonin receptor activation liberating free G-beta-gamma", 6, "E-B",
                 ["PMID:32958651"]),
              ch("membrane-delimited activation of the SLO-1 BK potassium channel", 2, "E-B",
                 ["PMID:32958651"]),
              ch("reduced neurotransmitter release", 5, "E-B", ["PMID:32958651"]),
              ch("longer sleep", None, "E-B", ["PMID:32958651"])],
             2, [{"name": "SLO-1 (BK, calcium-activated potassium channel); PCDR-1 melatonin receptor",
                  "species": "cele", "identifier": None,
                  "ortholog_relation": "SLO-1 ALREADY CARRIES THIS TABLE'S S5_ga_volatile_cele class-2 "
                                       "entry, where slo-1 loss of function confers volatile-"
                                       "anaesthetic resistance. Same gene, same species, two states. "
                                       "The human orthologue hSlo1 responds to melatonin through MT1 "
                                       "in heterologous expression, which is suggestive for mammals "
                                       "but is not organism-level evidence."}],
             ["PMID:32958651"],
             "increased potassium conductance at the presynaptic terminal, reducing transmitter "
             "release and network excitability",
             {"level": "EXACT_MOLECULE", "partner": "S5_ga_volatile_cele c2 (slo-1)",
              "justification": "slo-1 loss of function SHORTENS natural sleep and CONFERS RESISTANCE "
                               "to volatile anaesthetics. In both states the channel promotes reduced "
                               "activity, and in both the causal chain runs through suppression of "
                               "transmitter release - but the roles differ (MAINTAINS for sleep, "
                               "CONTROLS_ENTRY for anaesthesia). Together with unc-9 at class 12 and "
                               "the NALCN complex at class 1, this is the third molecule shared "
                               "between the worm sleep and worm anaesthesia rows, and the pattern of "
                               "shared machinery with differing role is now robust within species."}),
    ])

# ================================================================ 2) mouse volatile c5 — N-type Cav
put('S5_ga_volatile_mmus', 5,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["CONTROLS_ENTRY"], roles_tested_negative=[],
    ambiguity=("A SIGNED DOUBLE DISSOCIATION ACROSS AGENTS IN ONE GENOTYPE, and it is the sharpest "
               "agent result in the table. The SAME knockout is MORE sensitive to halothane and LESS "
               "sensitive to propofol. Not 'less affected' - oppositely affected. The authors' "
               "conclusion is quoted exactly because it is the claim: 'inhibition of the N-type Ca2+ "
               "channel underlies mechanisms of halothane anesthesia but counteracts propofol "
               "anesthesia.' MECHANISTIC CORROBORATION AT THE SYNAPSE: halothane depressed Schaffer "
               "collateral-CA1 field EPSPs MORE in the knockout, so the behavioural shift has a "
               "matched synaptic correlate in the expected direction. CLASS ASSIGNMENT IS DIRECT: the "
               "frozen class-5 definition names 'presynaptic Ca_v' among its representative "
               "implementations. SCOPE: agent identity is halothane, which is in this row's frozen "
               "agent scope; the propofol arm is recorded for the dissociation and is not "
               "transferable to the human propofol row, which is a different species."),
    strongest_grade="E-A", all_grades=["E-A"], negative_assay_statement=None,
    mechanisms=[
        mech("Presynaptic N-type Ca2+ channels mediate halothane anaesthesia and OPPOSE propofol "
             "anaesthesia in the same animals",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:12962913"],
               "basis": "Germline knockout shifts whole-animal anaesthetic sensitivity in opposite "
                        "directions for two agents, with a matched hippocampal field-potential "
                        "measurement for the volatile arm."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
               "agent": "halothane; propofol",
               "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                   "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                   "other": "halothane sensitivity SIGNIFICANTLY INCREASED; propofol "
                                            "sleep time SIGNIFICANTLY DECREASED; halothane depressed "
                                            "Schaffer collateral-CA1 fEPSPs MORE in knockouts"},
               "context_dependence": "agent_dependent", "statement": S_CAV,
               "evidence_grade": "E-A", "citation_ids": ["PMID:12962913"]}],
             "CONTEXT_DEPENDENT",
             [ch("N-type (Cav2.2) calcium channel deletion", 5, "E-A", ["PMID:12962913"]),
              ch("reduced presynaptic calcium entry and transmitter release", 5, "E-A",
                 ["PMID:12962913"]),
              ch("greater halothane depression of excitatory field potentials", 4, "E-A",
                 ["PMID:12962913"]),
              ch("increased halothane and decreased propofol sensitivity", None, "E-A",
                 ["PMID:12962913"])],
             5, [{"name": "N-type Ca2+ channel (Cacna1b / Cav2.2)", "species": "mmus",
                  "identifier": None,
                  "ortholog_relation": "The worm volatile row's class-5 entry is unc-64/syntaxin-1A "
                                       "with enhanced excitatory release. Both are presynaptic release "
                                       "machinery and both set volatile-anaesthetic sensitivity, but "
                                       "they are different proteins at different steps: "
                                       "SAME_PATHWAY_MODULE, not orthologous."}],
             ["PMID:12962913"],
             "altered presynaptic calcium-dependent release, changing how much further an anaesthetic "
             "must depress transmission to produce the state",
             {"level": "SAME_PATHWAY_MODULE", "partner": "S5_ga_volatile_cele c5 (unc-64 syntaxin)",
              "justification": "Both manipulate the presynaptic release step and both change "
                               "volatile-anaesthetic potency in the whole animal, in the same "
                               "direction (compromised release -> hypersensitivity). Different "
                               "proteins, same module. This is one of only two cross-phylum "
                               "correspondences in the table where the DIRECTION also matches, the "
                               "other being complex I."}),
    ])

print('APPLIED (%d):' % len(APPLIED))
for a in APPLIED:
    print('  ' + a)
print('SKIPPED (%d):' % len(SKIPPED))
for s in SKIPPED:
    print('  ' + s)
