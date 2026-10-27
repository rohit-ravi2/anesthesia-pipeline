"""PE-5 round-3 findings. Same discipline as r2/r2b: corrected battery, abstract read against
species / state / endpoint / manipulation, verbatim authoritative statement, idempotent application.

  36510822  ML297 GIRK1/2 activator, post-learning sleep      -> S3_rem_mmus c2, S4_deep_mmus c2
  27769744  pannexin1 knockout sleep-wake cycle               -> S4_deep_mmus c12
  37198238  Tfap2b in GABAergic neurons controls sleep        -> S3_rem_mmus c9, S4_deep_mmus c9
  20875840  EAAT3 knockout isoflurane requirement             -> S5_ga_volatile_mmus c4 (2nd mech)
  18485607  GABA-A alpha3 knockout sleep homeostasis          -> S4_deep_mmus c3 (NEGATIVE mech)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pe5_apply_findings import mech
from pe5_apply_r2 import put, add_mech, ch, APPLIED, SKIPPED

APPLIED.clear(); SKIPPED.clear()

S_ML297 = ("ML297, a recently developed candidate hypnotic agent targeting a new mechanism "
           "(activating GIRK1/2-subunit containing G-protein coupled inwardly rectifying potassium "
           "[GIRK] channels), alters sleep architecture in mice over the first 6 hr following a "
           "single-trial learning event. Following contextual fear conditioning (CFC), ML297 reversed "
           "post-CFC reductions in NREM sleep spindle power and REM sleep amounts and architecture, "
           "renormalizing sleep features to what was observed at baseline, prior to CFC.")
S_PANX = ("We found a significant increase in waking and a correspondent decrease in slow wave sleep "
          "percentages in the Panx1-/- animals. These changes were especially pronounced during the "
          "dark period... These findings are consistent with the hypothesis that extracellular "
          "adenosine is relatively depleted in Panx1-/- animals due to the absence of the "
          "ATP-permeable hemichannels. At the same time, sleep rebound after a 6-h sleep deprivation "
          "remained unchanged in Panx1-/- mice as compared to the control animals.")
S_TFAP2B = ("We previously found that AP2 transcription factors control sleep in C. elegans, "
            "Drosophila, and mice. Heterozygous deletion of Tfap2b, one of the mammalian AP2 "
            "paralogs, reduces sleep in mice... In mice, Tfap2b acts during early embryonic stages... "
            "During baseline conditions, Vgat-tfap2b-/- mice exhibited both shortened NREM and REM "
            "sleep time and reduced delta and theta power. Consistently, weaker delta and theta power "
            "were observed during rebound sleep in the Vgat-tfap2b-/- mice after sleep deprivation. "
            "Taken together, the results indicate that Tfap2b in GABAergic neurons is required for "
            "normal sleep.")
S_EAAT3 = ("The concentration required for isoflurane to cause immobility to painful stimuli, a "
           "response involving primarily reflex loops in the spinal cord, was not changed by EAAT3 "
           "knockout. However, the EAAT3 knockout mice were more sensitive to isoflurane-induced "
           "hypnotic effects, which may be mediated by hypothalamic sleep neural circuits. "
           "Interestingly, the EAAT3 knockout mice did not have an altered sensitivity to the hypnotic "
           "effects caused by ketamine, an i.v. anesthetic that is a glutamate receptor antagonist and "
           "does not affect EAAT3 activity.")
S_A3 = ("EEG spectral analysis showed no difference between genotypes during non rapid-eye movement "
        "(NREM) sleep or at waking-NREM sleep transitions. EEG power in the spindle frequency range "
        "(10-15 Hz) was significantly lower at NREM-REM sleep transitions in mutant compared with "
        "wild-type mice. Enhancement of sleep pressure by 6 h sleep deprivation did not reveal any "
        "differences in the regulation of EEG activities between genotypes... Strikingly, despite the "
        "disruption of postsynaptic gephyrin clusters, whole-cell patch clamp recordings revealed "
        "intact inhibitory synaptic transmission in the nRT of alpha3-KO mice. These findings show "
        "that the lack of alpha3-GABA(A) receptors is extensively compensated for.")

ML297_NOTE = ("SCOPE, AND IT IS TIGHT. The manipulation is pharmacological activation in animals whose "
              "sleep has already been PERTURBED by contextual fear conditioning; the reported effect "
              "is RENORMALISATION to that animal's own baseline, not a change from an unperturbed "
              "state. So this supports GIRK channels as sufficient to restore the state under a "
              "specific challenge, and does NOT establish that GIRK activity sets sleep in a naive "
              "animal. Graded accordingly and the restriction is carried in the perturbation record.")


def girk(row, which):
    eff = ("REM sleep amounts and architecture restored; post-CFC REM latency renormalised"
           if which == 'REM' else "NREM sleep spindle power restored to pre-CFC baseline")
    return mech("GIRK1/2 channel activation (ML297) restores sleep architecture after a learning "
                "challenge",
                [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-C", "citation_ids": ["PMID:36510822"],
                  "basis": "Systemic pharmacological activation of a defined channel reverses a "
                           "challenge-induced deficit in state amount and architecture. Sufficiency "
                           "under challenge; not a naive-animal manipulation."}],
                [{"manipulation": "pharmacological_activation", "direction_of_manipulation": "increase",
                  "agent": "ML297",
                  "observed_effect": {"total_quiescence": "increase", "state_structure": "increase",
                                      "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                      "other": eff + "; effects confined to the first 6 h after a "
                                               "single-trial learning event; renormalisation to the "
                                               "animal's own pre-CFC baseline; associated with improved "
                                               "contextual fear memory consolidation"},
                  "context_dependence": "challenge_dependent", "statement": S_ML297,
                  "evidence_grade": "E-C", "citation_ids": ["PMID:36510822"]}],
                "PROMOTES_STATE",
                [ch("ML297 activation of GIRK1/2-containing channels", 2, "E-C", ["PMID:36510822"]),
                 ch("increased inwardly rectifying potassium conductance", 2, "E-C", ["PMID:36510822"]),
                 ch("restoration of post-CFC sleep architecture", None, "E-C", ["PMID:36510822"])],
                2, [{"name": "GIRK1/2 (Kcnj3/Kcnj6) inwardly rectifying potassium channels",
                     "species": "mmus", "identifier": None,
                     "ortholog_relation": "The worm volatile row's class-2 entry is slo-1 (BK), a "
                                          "different potassium channel family. SAME_PHYSICAL_CLASS "
                                          "only: both are potassium conductances promoting reduced "
                                          "activity, with no molecular correspondence."}],
                ["PMID:36510822"],
                "increased potassium conductance hyperpolarising the networks that generate sleep "
                "oscillations",
                None)


# ---------------------------------------------------------------- 1) GIRK, REM and NREM
for row, which in (('S3_rem_mmus', 'REM'), ('S4_deep_mmus', 'NREM')):
    f = os.path.join(HERE, 'rows_v2', row + '.json')
    d = json.load(open(f))
    tgt = [c for c in d['cells'] if c['class_id'] == 2][0]
    if tgt['coverage'] == 'NOT_TESTED':
        put(row, 2, coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
            discovery_route="CLASS_FIRST", roles_present=["CONTROLS_ENTRY"],
            roles_tested_negative=[], ambiguity=ML297_NOTE,
            strongest_grade="E-C", all_grades=["E-C"], negative_assay_statement=None,
            mechanisms=[girk(row, which)])
    else:
        add_mech(row, 2, girk(row, which), note=ML297_NOTE,
                 extra_roles=["CONTROLS_ENTRY"], grade="E-C")

# ---------------------------------------------------------------- 2) pannexin1, NREM class 12
put('S4_deep_mmus', 12,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["CONTROLS_ENTRY"],
    roles_tested_negative=["MAINTAINS_STATE"],
    ambiguity=("A NESTED NEGATIVE INSIDE A POSITIVE, and the two must not be collapsed. Panx1-/- mice "
               "sleep LESS (waking up, slow-wave sleep down, most pronounced in the dark period), so "
               "the channel promotes the state. But sleep rebound after 6 h deprivation was UNCHANGED, "
               "so the homeostatic response machinery is intact. Compare the CD73 result at class 6 in "
               "this same row, which is the exact mirror image: baseline sleep UP, rebound ABSENT. Two "
               "manipulations of the same adenosine pathway dissociate baseline amount from homeostatic "
               "drive in OPPOSITE directions. CLASS ASSIGNMENT CAVEAT: pannexin1 is a channel of the "
               "innexin superfamily and sits in class 12 on structural grounds, but the authors' "
               "proposed mechanism is ATP efflux and downstream ADENOSINE signalling, which is class 6. "
               "Recorded as class 12 proximal with class 6 in the chain; the alternative reading is "
               "defensible and is stated here rather than hidden."),
    strongest_grade="E-B", all_grades=["E-B"],
    negative_assay_statement=("Sleep rebound after a 6 h sleep deprivation was measured in Panx1-/- and "
                              "Panx1+/+ mice in the same study that resolved a significant baseline "
                              "difference in waking and slow-wave sleep percentages. Rebound remained "
                              "unchanged between genotypes, so the assay had demonstrated power in "
                              "these animals."),
    mechanisms=[
        mech("Pannexin1 hemichannels promote slow-wave sleep, plausibly via ATP-derived extracellular "
             "adenosine, without contributing to sleep homeostasis",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-B", "citation_ids": ["PMID:27769744"],
               "basis": "Germline knockout shifts the baseline proportion of slow-wave sleep and "
                        "waking across the light/dark cycle."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "decrease",
                                   "entry_threshold": "increase", "survival_recovery": "not_reported",
                                   "other": "significant increase in waking and decrease in slow-wave "
                                            "sleep, most pronounced in the dark period; sleep rebound "
                                            "after 6 h deprivation UNCHANGED; increased movement "
                                            "activity; altered vertical and horizontal pole performance"},
               "context_dependence": "circadian_phase_dependent", "statement": S_PANX,
               "evidence_grade": "E-B", "citation_ids": ["PMID:27769744"]}],
             "PROMOTES_STATE",
             [ch("Panx1 deletion", 12, "E-B", ["PMID:27769744"]),
              ch("loss of ATP-permeable hemichannel efflux", 12, "E-B", ["PMID:27769744"]),
              ch("reduced extracellular adenosine", 6, "E-B", ["PMID:27769744"]),
              ch("reduced slow-wave sleep, increased waking", None, "E-B", ["PMID:27769744"])],
             12, [{"name": "Pannexin1 (Panx1)", "species": "mmus", "identifier": None,
                   "ortholog_relation": "The worm rows carry innexins (unc-9, inx-6) at class 12. "
                                        "Pannexins are the vertebrate innexin superfamily members, so "
                                        "this is ORTHOLOGOUS_MOLECULE at superfamily level - but the "
                                        "worm entries act as electrical synapses while this one is "
                                        "proposed to act as a metabolite conduit. SAME SUPERFAMILY, "
                                        "DIFFERENT PHYSICAL FUNCTION."}],
             ["PMID:27769744"],
             "loss of a hemichannel conduit for extracellular ATP and hence of activity-dependent "
             "adenosine accumulation",
             {"level": "ORTHOLOGOUS_MOLECULE",
              "partner": "S7_dauer_cele c12 / S5_ga_volatile_cele c12 (innexins)",
              "justification": "Pannexin and innexin are the same protein superfamily across the "
                               "protostome-deuterostome split. The correspondence is structural; the "
                               "proposed physical function differs (metabolite conduit here, electrical "
                               "coupling there), which is exactly why the resolution hierarchy "
                               "separates ORTHOLOGOUS_MOLECULE from SAME_PATHWAY_MODULE."}),
    ])

# ---------------------------------------------------------------- 3) Tfap2b, REM and NREM class 9
def tfap(row, which):
    eff = ("shortened REM sleep time and reduced theta power" if which == 'REM'
           else "shortened NREM sleep time and reduced delta power")
    return mech("AP-2 transcription factor Tfap2b acts embryonically in GABAergic neurons to build "
                "the machinery for normal sleep",
                [{"role": "BUILDS_MACHINERY", "evidence_grade": "E-B", "citation_ids": ["PMID:37198238"],
                  "basis": "The authors state Tfap2b acts during EARLY EMBRYONIC stages, and the "
                           "adult phenotype follows a developmental alteration of GABAergic gene "
                           "expression. Under the frozen role definitions this is construction of the "
                           "machinery, not moment-to-moment control of the state."},
                 {"role": "MAINTAINS_STATE", "evidence_grade": "E-B", "citation_ids": ["PMID:37198238"],
                  "basis": "Cell-type-restricted deletion shortens the time spent in the state and "
                           "weakens its characteristic oscillation, at baseline and in rebound."}],
                [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
                  "observed_effect": {"total_quiescence": "decrease", "state_structure": "decrease",
                                      "entry_threshold": "not_reported", "survival_recovery": "not_reported",
                                      "other": eff + "; weaker delta and theta power during REBOUND "
                                               "sleep after 6 h deprivation; GABAergic genes (GAD1, "
                                               "GAD2, Vgat) downregulated in cortex, brainstem and "
                                               "cerebellum but UPREGULATED in striatum; heterozygous "
                                               "whole-animal deletion also reduces sleep"},
                  "context_dependence": "cell_type_dependent", "statement": S_TFAP2B,
                  "evidence_grade": "E-B", "citation_ids": ["PMID:37198238"]}],
                "PROMOTES_STATE",
                [ch("Tfap2b deletion in Vgat-expressing GABAergic neurons", 9, "E-B", ["PMID:37198238"]),
                 ch("altered embryonic brain patterning and GABAergic gene expression", 9, "E-B",
                    ["PMID:37198238"]),
                 ch("reduced GABAergic inhibitory capacity in cortex, brainstem and cerebellum", 3,
                    "E-B", ["PMID:37198238"]),
                 ch("shortened sleep time and weakened sleep oscillations", None, "E-B",
                    ["PMID:37198238"])],
                9, [{"name": "Tfap2b (AP-2beta)", "species": "mmus", "identifier": None,
                     "ortholog_relation": "DIRECT ORTHOLOGUE of C. elegans APTF-1, which already "
                                          "carries this table's S2_core_cele class-9 entry as the "
                                          "transcriptional specifier of the RIS sleep neuron. The "
                                          "authors state explicitly that AP2 transcription factors "
                                          "control sleep in C. elegans, Drosophila AND mice."}],
                ["PMID:37198238"],
                "developmental specification of GABAergic sleep-promoting neurons, setting the "
                "inhibitory capacity available to the adult",
                {"level": "ORTHOLOGOUS_MOLECULE", "partner": "S2_core_cele c9 (APTF-1)",
                 "justification": "APTF-1 and Tfap2b are orthologous AP-2 transcription factors, both "
                                  "assigned BUILDS_MACHINERY, both acting developmentally on the "
                                  "GABAergic sleep-promoting population, in species separated by ~600 "
                                  "Myr. This is the single deepest mechanism correspondence in the "
                                  "table and the only one where the ROLE is conserved along with the "
                                  "molecule."})


for row, which in (('S3_rem_mmus', 'REM'), ('S4_deep_mmus', 'NREM')):
    f = os.path.join(HERE, 'rows_v2', row + '.json')
    d = json.load(open(f))
    tgt = [c for c in d['cells'] if c['class_id'] == 9][0]
    note = ("ROLE ASSIGNMENT IS THE POINT HERE. The deletion is embryonic and the phenotype is adult, "
            "so the frozen role is BUILDS_MACHINERY alongside MAINTAINS_STATE - the animal's capacity "
            "for the state was built wrong, rather than its ongoing control being perturbed. Only two "
            "BUILDS_MACHINERY assignments existed in this table before, both in C. elegans; this is "
            "the first mammalian one, and it is carried by the ORTHOLOGUE of one of them (APTF-1).")
    if tgt['coverage'] == 'NOT_TESTED':
        put(row, 9, coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
            discovery_route="CLASS_FIRST",
            roles_present=["BUILDS_MACHINERY", "MAINTAINS_STATE"], roles_tested_negative=[],
            ambiguity=note, strongest_grade="E-B", all_grades=["E-B"], negative_assay_statement=None,
            mechanisms=[tfap(row, which)])
    else:
        add_mech(row, 9, tfap(row, which), note=note,
                 extra_roles=["BUILDS_MACHINERY", "MAINTAINS_STATE"], grade="E-B")

# ---------------------------------------------------------------- 4) EAAT3, mouse volatile class 4
add_mech('S5_ga_volatile_mmus', 4,
         mech("Neuronal glutamate transporter EAAT3 sets isoflurane HYPNOTIC potency but not "
              "immobilising potency",
              [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:20875840"],
                "basis": "Germline knockout lowers the isoflurane concentration required for loss of "
                         "righting reflex while leaving the immobility concentration unchanged - "
                         "entry control for one endpoint, explicitly not for the other."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
                "agent": "isoflurane; ketamine",
                "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                    "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                    "other": "MORE sensitive to isoflurane-induced hypnosis (loss of "
                                             "righting); immobility concentration UNCHANGED; ketamine "
                                             "hypnotic sensitivity UNCHANGED; EAAT1 and EAAT2 "
                                             "expression unchanged in cortex and spinal cord"},
                "context_dependence": "endpoint_dependent", "statement": S_EAAT3,
                "evidence_grade": "E-A", "citation_ids": ["PMID:20875840"]}],
              "OPPOSES_STATE",
              [ch("Slc1a1/EAAT3 deletion", 4, "E-A", ["PMID:20875840"]),
               ch("reduced neuronal glutamate uptake", 4, "E-A", ["PMID:20875840"]),
               ch("increased sensitivity of hypothalamic hypnotic circuitry to isoflurane", 7, "E-A",
                  ["PMID:20875840"]),
               ch("loss of righting reflex at lower isoflurane concentration", None, "E-A",
                  ["PMID:20875840"])],
              4, [{"name": "EAAT3 / Slc1a1 neuronal glutamate transporter", "species": "mmus",
                   "identifier": None, "ortholog_relation": None}],
              ["PMID:20875840"],
              "altered clearance of synaptic glutamate changing the anaesthetic sensitivity of "
              "hypnosis-generating circuitry",
              None),
         note=("ENDPOINT DISSOCIATION WITHIN ONE ANIMAL, and it cuts A_beh in two. Immobility (a spinal "
               "reflex endpoint) and hypnosis (loss of righting, a supraspinal endpoint) come apart "
               "under the SAME genetic lesion in the SAME mice. The anaesthesia literature routinely "
               "reports 'anaesthetic sensitivity' as one quantity; this result shows it is at least "
               "two. Agent control: ketamine hypnosis is unaffected, so the effect is not a general "
               "shift in arousal threshold. Together with the Ndufs4 ketamine-resistance result in "
               "class 8 of this row, agent specificity is now established twice over on independent "
               "mechanisms."),
         extra_roles=["CONTROLS_ENTRY"], grade="E-A")

# ---------------------------------------------------------------- 5) GABA-A alpha3, a powered negative
add_mech('S4_deep_mmus', 3,
         mech("GABA-A receptor alpha3 subunit is NOT required for NREM sleep or for sleep homeostasis, "
              "and its loss is developmentally compensated",
              [{"role": "MAINTAINS_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:18485607"],
                "basis": "TESTED AND NEGATIVE on NREM spectral content, on waking-NREM transitions and "
                         "on the response to 6 h sleep deprivation, with a mechanistic explanation "
                         "(intact inhibitory transmission in nRT despite disrupted gephyrin clusters)."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "no_change", "state_structure": "no_change",
                                    "entry_threshold": "no_change", "survival_recovery": "not_reported",
                                    "other": "no EEG difference during NREM or at waking-NREM "
                                             "transitions; sleep-deprivation response identical; "
                                             "spindle-band (10-15 Hz) power LOWER at NREM-REM "
                                             "transitions; slightly larger 11-13 Hz waking power; no "
                                             "absence seizures; inhibitory synaptic transmission in "
                                             "nRT INTACT despite disrupted postsynaptic gephyrin "
                                             "clusters"},
                "context_dependence": "none_reported", "statement": S_A3,
                "evidence_grade": "E-A", "citation_ids": ["PMID:18485607"]}],
              "NO_ESTABLISHED_EFFECT",
              [ch("Gabra3 deletion", 3, "E-A", ["PMID:18485607"]),
               ch("developmental compensation preserving nRT inhibitory transmission", 3, "E-A",
                  ["PMID:18485607"]),
               ch("no change in NREM EEG or sleep homeostasis", None, "E-A", ["PMID:18485607"])],
              3, [{"name": "Gabra3 (GABA-A receptor alpha3 subunit)", "species": "mmus",
                   "identifier": None, "ortholog_relation": None}],
              ["PMID:18485607"],
              "no resolvable change in thalamocortical inhibitory function during NREM",
              None),
         note=("A NEGATIVE THAT NAMES ITS OWN MECHANISM, which is rare and raises its value. The "
               "authors show inhibitory synaptic transmission in the reticular thalamic nucleus is "
               "INTACT despite disrupted postsynaptic gephyrin clusters, and conclude the loss is "
               "'extensively compensated for'. So this is not evidence that alpha3-GABA-A receptors are "
               "irrelevant to NREM; it is evidence that the system is REDUNDANT at this node. Under the "
               "project's three-valued logic that distinction is the whole point: TESTED_NEGATIVE on "
               "necessity is not NOT_TESTED, and neither is it evidence of non-participation. The cell "
               "remains POSITIVE overall on the Gabrd/PV-interneuron mechanism; this null narrows which "
               "subunits carry the function. Note also the one thing that DID change - spindle-band "
               "power specifically at NREM-REM transitions - which is a state-BOUNDARY effect and is "
               "invisible to any measure that scores states separately."),
         extra_roles=[], grade="E-A")

print('APPLIED (%d):' % len(APPLIED))
for a in APPLIED:
    print('  ' + a)
print('SKIPPED (%d):' % len(SKIPPED))
for s in SKIPPED:
    print('  ' + s)
