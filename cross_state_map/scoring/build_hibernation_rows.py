"""Score the two committed hibernation rows: S9_hib_seasonal_isp and S9_hib_daily_mmus.

Hibernation was named in PE5_FINAL_REPORT.md §21 as "the state most likely to break the headline
claim", because it is the one endogenous state in which an animal does something anaesthesia-like
on purpose. It is scored here under the same frozen ontology, with the same v3 search protocol,
and the outcome is recorded whichever way it falls.

Retrieved under pe5_vocab_v3 at depth 600 (isp) / 1200 (mmus), 72 queries, 7750 ranked candidates.
"""
import json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'rows_v2')
sys.path.insert(0, HERE)
from pe5_apply_findings import mech

ROLES = ['PRODUCES_STATE', 'CONTROLS_ENTRY', 'MAINTAINS_STATE',
         'PROTECTS_THROUGH_STATE', 'BUILDS_MACHINERY', 'ENABLES_EXIT']


def ch(step, cid, g, cits):
    return {"step": step, "class_id": cid, "role": "proximal", "inferred": False,
            "evidence_grade": g, "citation_ids": cits}


def blank_cell(rid, cid):
    return dict(row_id=rid, class_id=cid, coverage="NOT_TESTED", status="NOT_TESTED",
                applicability="APPLICABLE", roles_present=[], roles_tested_negative=[],
                ambiguity=None, strongest_grade=None, all_grades=[],
                negative_assay_statement=None, mechanisms=[])


def axes(rid):
    if rid.endswith('_isp'):
        beh = ("Seasonal hibernators are immobile through a torpor bout, rousing only at periodic "
               "interbout arousals. Immobility is definitional for bout scoring.")
        neu = ("Cortical EEG becomes progressively isoelectric as Tb falls through a bout, and "
               "recovers during interbout arousal. Sub-measures are not separable from the "
               "abstracts used here.")
        met = ("Metabolic rate falls to a few percent of basal. Interbout arousals consume 60-80% "
               "of the entire winter energy budget (PMID:11893609) - the state is cheap, and "
               "LEAVING it is what is expensive.")
    else:
        beh = "Daily torpor: locomotor activity falls with Tb and heart rate (PMID:22785425)."
        neu = ("Neural phenotype is NOT well characterised for mouse daily torpor in the retrieved "
               "literature. Recorded as measurability-limited rather than as a measured decrease.")
        met = ("Metabolic rate, body temperature and heart rate all fall; heart-rate decline "
               "PRECEDES body-temperature decline (PMID:40593766), which orders the two.")
    return [
        dict(axis="A_beh", condition="whole_state", scope="whole_organism", measurability="MEASURED",
             direction="decreased", neural_submeasures=None, magnitude=None,
             units="locomotor activity; immobility", baseline="euthermic interbout / pre-fast",
             evidence_grade="E-B", citation_ids=["PMID:22785425"], notes=beh),
        dict(axis="A_neu", condition="whole_state", scope="whole_brain",
             measurability=("MEASURED" if rid.endswith('_isp') else "NOT_YET_MEASURED"),
             direction=None,
             neural_submeasures={
                 "rate_amplitude": dict(
                     direction=("decreased" if rid.endswith('_isp') else "not_measured"),
                     evidence_grade="E-D",
                     note=(("Cortical EEG becomes progressively isoelectric as body temperature "
                            "falls through a seasonal bout and recovers on interbout arousal. Graded "
                            "E-D: this is the standard description in the hibernation literature and "
                            "was not established by a primary manipulation paper retrieved here.")
                           if rid.endswith('_isp') else
                           ("NOT MEASURED in the retrieved mouse daily-torpor literature. The "
                            "manipulation papers scored in this row (PMID:22785425, PMID:40593766, "
                            "PMID:28378088) report body temperature, heart rate, metabolic rate and "
                            "locomotor activity - no neural readout. Recorded as an explicit gap."))),
                 "coordination": dict(direction="not_measured", evidence_grade=None,
                                      note="Not reported in the retrieved literature for either row."),
                 "dynamical_organization": dict(direction="not_measured", evidence_grade=None,
                                                note="Not reported in the retrieved literature."),
             },
             magnitude=None, units="cortical EEG amplitude",
             baseline="euthermia", evidence_grade="E-D", citation_ids=[], notes=neu),
        dict(axis="A_met", condition="whole_state", scope="whole_organism", measurability="MEASURED",
             direction="decreased", neural_submeasures=None, magnitude=None,
             units="metabolic rate, body temperature, heart rate",
             baseline="euthermic interbout / pre-fast", evidence_grade="E-A",
             citation_ids=["PMID:22785425", "PMID:40593766"], notes=met),
    ]


def new_row(rid, species, inst):
    return dict(
        row_id=rid, state="hibernation", species=species, instantiation=inst,
        schema_version="2", ontology_version="v2.1", scored_utc="2026-09-21",
        scorer="PE-5 hibernation extension",
        state_production="ENDOGENOUS",
        state_production_justification=(
            "The animal generates the state itself on a seasonal or fasting cue; no exogenous agent "
            "is required. This matters for the production/exit analysis, in which hibernation is the "
            "designated falsification test."),
        agent_scope=None,
        axes=axes(rid),
        cells=[blank_cell(rid, c) for c in range(1, 13)],
        row_summary=dict(row_id=rid),
        v1_migration=None,
        ontology_flags_v2=["scored directly under v2.1; no v1 predecessor"],
        citations_pending_verification=[])


# ---------------------------------------------------------------- verbatim statements
S_ADO = ("During a 23-h fast, saline-treated mice were torpid for 518 +/- 43 min, whereas "
         "aminophylline-treated mice were torpid for significantly less time (54 +/- 20 min). In a "
         "second experiment, aminophylline was infused subcutaneously into torpid mice to test the "
         "role of adenosine in the maintenance of torpor. Aminophylline reversed the hypometabolism, "
         "hypothermia, bradycardia, and hypoactivity of torpor, whereas saline did not... "
         "Intracerebroventricular, but not subcutaneous, infusion of 8-SPT causes a return to "
         "euthermia... whereas peripheral adenosine signaling is not necessary for the maintenance "
         "of torpor, antagonism of central adenosine is sufficient to disrupt torpor.")
S_CHA = ("Because central adenosine activation has been shown to induce a torpor-like state in the "
         "arctic ground squirrel, and blocking the adenosine-1 (A1) receptor prevents daily torpor, "
         "we hypothesized that central activation of the A1 adenosine receptors would induce a bout "
         "of natural torpor in mice... All conditions induced profound hypothermia. T b fell more "
         "rapidly in the FH, isoflurane-anesthesia, and CHA conditions compared to torpor, while "
         "mice treated with CHA recovered at half the rate of torpid mice... the hypothermic bouts "
         "showed distinct patterns of gene expression, with torpor characterized by elevated hepatic "
         "and cardiac Txnip expression and all other hypothermic states characterized by elevated "
         "c-Fos and Egr-1 expression. We conclude that CHA-induced hypothermia and natural torpor "
         "are largely different physiological states.")
S_VLM = ("Inhibiting catecholaminergic (CA) neurons in the ventrolateral medulla (VLM) significantly "
         "impairs torpor in mice, while their activation reduces body temperature, heart rate, energy "
         "expenditure, physical activity, and thermogenesis. Importantly, the heart rate decline "
         "precedes body temperature reduction, resembling patterns observed in natural torpid "
         "animals... these neurons are conserved in Daurian ground squirrels and become active before "
         "hibernation.")
S_POA = ("Here, we show that chemogenetic activation of neurons in the preoptic area (POA) elicits a "
         "torpor-like state in mice, characterized by sustained hypothermia and hypometabolism. In an "
         "animal stroke model, this endogenous hypothermic state significantly reduced infarct volume "
         "and improved motor outcomes compared to controls, whereas maintaining normothermia "
         "attenuated these protective effects.")
S_AVP = ("Hamsters whose lateral septum was infused with vasopressin showed almost no periods of "
         "hypothermia, whereas hamsters treated with control infusions displayed a normal hibernation "
         "pattern. The results indicate that persistence of vasopressin release in the lateral septum "
         "of the European hamster during winter can prevent hibernation.")
S_PGE = ("The acute-phase response to bacterial lipopolysaccharide (LPS) was arrested during "
         "hibernation and fully restored on arousal to normothermia... LPS was without effect in "
         "hibernating squirrels, neither inducing fever nor provoking arousal, but a fever did "
         "develop several days later, when squirrels next aroused from hibernation; the duration of "
         "this arousal was increased sixfold above baseline values. Intracerebroventricular infusions "
         "of prostaglandin E(2) provoked arousal from hibernation and induced fever, suggesting that "
         "neural signaling pathways that mediate febrile responses are functional during hibernation. "
         "Over the course of the hibernation season, arousals consume 60-80% of a squirrel's winter "
         "energy budget, but their functional significance is unknown and disputed.")
S_NHLH2 = ("We report significant differences in serum leptin levels and body temperature in N2KO "
           "mice compared with WT mice exposed to a 24-hour fast, suggestive of a defect in both "
           "white (WAT) and brown adipose tissue (BAT) function... The mRNAs for beta3-adrenergic "
           "receptors (beta3-AR), beta2-AR and uncoupling proteins were significantly reduced in WAT "
           "and BAT from N2KO mice compared with WT mice... all suggestive of a deficient torpor "
           "response in mutant animals.")


def put(row, cid, **kw):
    for c in row['cells']:
        if c['class_id'] == cid:
            c.update(kw)
            return
    raise KeyError(cid)


# ================================================================ daily torpor, mouse
daily = new_row('S9_hib_daily_mmus', 'mmus', 'daily torpor')

put(daily, 6,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["CONTROLS_ENTRY", "MAINTAINS_STATE", "ENABLES_EXIT"],
    roles_tested_negative=["PRODUCES_STATE"],
    ambiguity=(
        "THIS CELL CARRIES BOTH A MAINTENANCE POSITIVE AND A SUFFICIENCY NEGATIVE, and the pair is "
        "the reason hibernation was scored. (i) Central adenosine is required to ENTER and to HOLD "
        "torpor: aminophylline cuts torpor time 518 -> 54 min, and infused into an ALREADY TORPID "
        "mouse it reverses hypometabolism, hypothermia, bradycardia and hypoactivity. The "
        "BBB-impermeant antagonist 8-SPT works intracerebroventricularly and NOT subcutaneously, "
        "which localises the requirement centrally and is a genuine internal control. (ii) The "
        "matching sufficiency test FAILS: central A1 agonist CHA produces profound hypothermia that "
        "is NOT torpor - different Tb fall rate, different heart-rate trajectory, different shivering "
        "and arrhythmia pattern, half the recovery rate, and a different transcriptional signature "
        "(torpor elevates Txnip; CHA and every other induced hypothermia elevate c-Fos and Egr-1). "
        "The authors conclude they are 'largely different physiological states'. "
        "SCORING NOTE ON ENABLES_EXIT: the antagonist arm drives exit from an established bout. This "
        "is scored ENABLES_EXIT for exact consistency with S5_ga_volatile_hsap c6, where caffeine - "
        "also an adenosine antagonist, also given during the maintained state - was scored the same "
        "way. Scoring the same pharmacology differently in two rows would be indefensible."),
    strongest_grade="E-A", all_grades=["E-A"],
    negative_assay_statement=(
        "Sufficiency was tested directly (PMID:28378088): central A1 agonist CHA was compared against "
        "natural torpor, forced hypothermia and isoflurane anaesthesia on Tb kinetics, heart rate, "
        "shivering, arrhythmia, recovery rate, circulating lactate and gene expression. All four "
        "conditions produced profound hypothermia, so the assay had power; CHA-induced hypothermia "
        "separated from natural torpor on multiple independent measures."),
    mechanisms=[
        mech("Central adenosine receptor signalling is required to enter and to maintain daily torpor",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:22785425"],
               "basis": "Antagonist during fasting reduces total torpid time nearly tenfold."},
              {"role": "MAINTAINS_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:22785425"],
               "basis": "Antagonist infused into an already-torpid animal reverses the state on four "
                        "simultaneous readouts. A maintenance manipulation, not an entry one."},
              {"role": "ENABLES_EXIT", "evidence_grade": "E-A", "citation_ids": ["PMID:22785425"],
               "basis": "Central antagonism is 'sufficient to disrupt torpor' and returns the animal "
                        "to euthermia - exit driven pharmacologically from within the state."}],
             [{"manipulation": "pharmacological_antagonism", "direction_of_manipulation": "decrease",
               "agent": "aminophylline; 8-sulfophenyltheophylline (BBB-impermeant)",
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "decrease",
                                   "entry_threshold": "increase", "survival_recovery": "increase",
                                   "other": "torpid time 518+/-43 -> 54+/-20 min; reversal of "
                                            "hypometabolism, hypothermia, bradycardia and "
                                            "hypoactivity when infused into torpid animals; ICV but "
                                            "NOT subcutaneous 8-SPT returns animals to euthermia"},
               "context_dependence": "route_dependent", "statement": S_ADO,
               "evidence_grade": "E-A", "citation_ids": ["PMID:22785425"]}],
             "PROMOTES_STATE",
             [ch("central adenosine receptor antagonism", 6, "E-A", ["PMID:22785425"]),
              ch("loss of adenosinergic suppression of thermoregulatory and cardiovascular drive", 6,
                 "E-A", ["PMID:22785425"]),
              ch("return to euthermia", None, "E-A", ["PMID:22785425"])],
             6, [{"name": "adenosine; A1 adenosine receptor", "species": "mmus", "identifier": None,
                  "ortholog_relation": "Adenosine carries FOUR entries in this table now: mouse NREM "
                                       "class 6 (CD73-derived, homeostatic drive), human volatile "
                                       "anaesthesia class 6 (caffeine antagonism accelerating "
                                       "emergence), and both hibernation rows. Same molecule, three "
                                       "states, and in every case manipulating it moves the state."}],
             ["PMID:22785425"],
             "central adenosinergic suppression of thermogenic and cardiovascular drive",
             {"level": "EXACT_MOLECULE", "partner": "S5_ga_volatile_hsap c6 (caffeine)",
              "justification": "The same pharmacology - central adenosine antagonism delivered during "
                               "the maintained state - drives exit from BOTH daily torpor and "
                               "volatile anaesthesia. One of very few manipulations in this table "
                               "that acts the same way on an endogenous and an exogenous state."}),
        mech("A1 receptor activation produces hypothermia that is NOT torpor",
             [{"role": "PRODUCES_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:28378088"],
               "basis": "TESTED AND NEGATIVE. The induced state separates from natural torpor on Tb "
                        "kinetics, heart rate, shivering, arrhythmia, recovery rate and "
                        "transcriptional signature. Listed under roles_tested_negative."}],
             [{"manipulation": "pharmacological_activation", "direction_of_manipulation": "increase",
               "agent": "N6-cyclohexyladenosine (CHA), intracerebroventricular",
               "observed_effect": {"total_quiescence": "increase", "state_structure": "decrease",
                                   "entry_threshold": "decrease", "survival_recovery": "decrease",
                                   "other": "profound hypothermia produced, but faster Tb fall, "
                                            "blunted heart-rate drop, no shivering on recovery, "
                                            "extended >1 s heart-rate pauses, half the recovery rate, "
                                            "and c-Fos/Egr-1 rather than Txnip induction"},
               "context_dependence": "none_reported", "statement": S_CHA,
               "evidence_grade": "E-A", "citation_ids": ["PMID:28378088"]}],
             "NO_ESTABLISHED_EFFECT",
             [ch("central A1 receptor agonism in fed mice", 6, "E-A", ["PMID:28378088"]),
              ch("profound hypothermia that is transcriptionally and physiologically distinct from "
                 "torpor", None, "E-A", ["PMID:28378088"])],
             6, [{"name": "A1 adenosine receptor agonist CHA", "species": "mmus", "identifier": None,
                  "ortholog_relation": None}],
             ["PMID:28378088"],
             "hypothermia produced through a route that does not reconstitute the torpid state",
             None),
    ])

put(daily, 7,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="SPECIES_ENDPOINT_FIRST",
    roles_present=["PRODUCES_STATE", "CONTROLS_ENTRY"], roles_tested_negative=[],
    ambiguity=(
        "NECESSITY AND SUFFICIENCY IN ONE PAPER, which is rare anywhere in this table: inhibiting "
        "ventrolateral-medulla catecholaminergic neurons impairs torpor, and activating them lowers "
        "body temperature, heart rate, energy expenditure, activity and thermogenesis. The ORDERING "
        "result matters independently - heart-rate decline PRECEDES body-temperature decline, "
        "matching natural torpor, so the circuit is not simply cooling the animal. Cross-species "
        "note: the same neurons are conserved in Daurian ground squirrels and become active before "
        "hibernation, which is suggestive for the seasonal row and is NOT scored there, because "
        "'become active before' is a correlation, not a manipulation."),
    strongest_grade="E-A", all_grades=["E-A"], negative_assay_statement=None,
    mechanisms=[
        mech("Ventrolateral-medulla catecholaminergic neurons induce fasting torpor",
             [{"role": "PRODUCES_STATE", "evidence_grade": "E-A", "citation_ids": ["PMID:40593766"],
               "basis": "Activation drives the full multi-system phenotype with the correct internal "
                        "ordering (heart rate before temperature). A sufficiency demonstration."},
              {"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:40593766"],
               "basis": "Inhibition significantly impairs fasting-induced torpor."}],
             [{"manipulation": "chemogenetic_bidirectional", "direction_of_manipulation": "bidirectional",
               "agent": None,
               "observed_effect": {"total_quiescence": "increase", "state_structure": "increase",
                                   "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                   "other": "inhibition impairs torpor; activation reduces Tb, heart "
                                            "rate, energy expenditure, activity and thermogenesis; "
                                            "heart-rate decline PRECEDES Tb decline; projections to "
                                            "dorsal motor vagal nucleus and medial preoptic area"},
               "context_dependence": "none_reported", "statement": S_VLM,
               "evidence_grade": "E-A", "citation_ids": ["PMID:40593766"]}],
             "PROMOTES_STATE",
             [ch("bidirectional chemogenetic control of VLM catecholaminergic neurons", 7, "E-A",
                 ["PMID:40593766"]),
              ch("vagal and medial-preoptic projections lowering heart rate then thermogenesis", 7,
                 "E-A", ["PMID:40593766"]),
              ch("fasting-induced torpor", None, "E-A", ["PMID:40593766"])],
             7, [{"name": "ventrolateral medulla catecholaminergic (CA) neurons", "species": "mmus",
                  "identifier": None,
                  "ortholog_relation": "Conserved in Daurian ground squirrels per the same paper, but "
                                       "only as an activity correlation, so no seasonal-row entry."}],
             ["PMID:40593766"],
             "brainstem catecholaminergic drive lowering cardiovascular output ahead of thermogenesis",
             None),
        mech("Preoptic activation elicits a torpor-like hypometabolic state",
             [{"role": "PRODUCES_STATE", "evidence_grade": "E-C", "citation_ids": ["PMID:41280034"],
               "basis": "Chemogenetic POA activation produces sustained hypothermia and "
                        "hypometabolism described as torpor-like. PREPRINT, graded E-C."}],
             [{"manipulation": "chemogenetic_activation", "direction_of_manipulation": "increase",
               "agent": None,
               "observed_effect": {"total_quiescence": "increase", "state_structure": "not_reported",
                                   "entry_threshold": "decrease", "survival_recovery": "increase",
                                   "other": "sustained hypothermia and hypometabolism; reduced "
                                            "infarct volume and improved motor outcome in a stroke "
                                            "model; protection attenuated if normothermia maintained"},
               "context_dependence": "none_reported", "statement": S_POA,
               "evidence_grade": "E-C", "citation_ids": ["PMID:41280034"]}],
             "PROMOTES_STATE",
             [ch("chemogenetic activation of preoptic-area neurons", 7, "E-C", ["PMID:41280034"]),
              ch("engagement of endogenous thermoregulatory circuitry", 11, "E-C", ["PMID:41280034"]),
              ch("sustained torpor-like hypothermia and hypometabolism", None, "E-C",
                 ["PMID:41280034"])],
             7, [{"name": "preoptic area (POA) neurons", "species": "mmus", "identifier": None,
                  "ortholog_relation": "The preoptic area also carries this table's S4_deep_mmus "
                                       "class-7 and class-11 entries (VLPO galanin neurons driving "
                                       "sleep and heat loss). SAME_PATHWAY_MODULE across NREM sleep "
                                       "and torpor, with the caveat that neither paper resolves "
                                       "whether the same POA subpopulation is involved."}],
             ["PMID:41280034"],
             "recruitment of endogenous thermoregulatory circuitry to lower the defended temperature",
             {"level": "SAME_PATHWAY_MODULE", "partner": "S4_deep_mmus c7 / c11 (VLPO galanin)",
              "justification": "Preoptic manipulation drives both NREM sleep with heat loss and a "
                               "torpor-like hypometabolic state. Whether the same cells do both is "
                               "not resolved by either paper, so the correspondence is at module "
                               "level and no stronger."}),
    ])

put(daily, 9,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["BUILDS_MACHINERY"], roles_tested_negative=[],
    ambiguity=(
        "WEAK, AND LABELLED AS SUCH. The paper is about adipose-tissue function; the torpor claim is "
        "inferential - the authors write 'suggestive of a deficient torpor response', and the "
        "measured variables are serum leptin and body temperature after a 24 h fast, not a scored "
        "torpor bout. Graded E-C for that reason. Role is BUILDS_MACHINERY rather than "
        "CONTROLS_ENTRY because the deficit is developmental and peripheral - beta2/beta3-adrenergic "
        "receptor and uncoupling-protein mRNA are reduced in white and brown fat, i.e. the effector "
        "tissue was built wrong, rather than the torpor decision being altered."),
    strongest_grade="E-C", all_grades=["E-C"], negative_assay_statement=None,
    mechanisms=[
        mech("Nhlh2 is required for a normal fasting torpor response, via adrenergic and uncoupling "
             "machinery in adipose tissue",
             [{"role": "BUILDS_MACHINERY", "evidence_grade": "E-C", "citation_ids": ["PMID:20808804"],
               "basis": "Germline deletion of a hypothalamic bHLH transcription factor leaves the "
                        "thermogenic effector tissue depleted of beta-adrenergic receptors and "
                        "uncoupling proteins."}],
             [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "not_reported",
                                   "entry_threshold": "increase", "survival_recovery": "not_reported",
                                   "other": "altered serum leptin and body temperature after 24 h "
                                            "fast; beta3-AR, beta2-AR and uncoupling-protein mRNA "
                                            "reduced in WAT and BAT; adipose inflammation and "
                                            "macrophage markers elevated"},
               "context_dependence": "none_reported", "statement": S_NHLH2,
               "evidence_grade": "E-C", "citation_ids": ["PMID:20808804"]}],
             "PROMOTES_STATE",
             [ch("Nhlh2 deletion", 9, "E-C", ["PMID:20808804"]),
              ch("reduced beta-adrenergic and uncoupling-protein expression in adipose tissue", 8,
                 "E-C", ["PMID:20808804"]),
              ch("defective torpor response to fasting", None, "E-C", ["PMID:20808804"])],
             9, [{"name": "Nhlh2 (Nescient Helix-Loop-Helix 2)", "species": "mmus", "identifier": None,
                  "ortholog_relation": None}],
             ["PMID:20808804"],
             "developmental loss of the adrenergic and uncoupling machinery the torpor response acts through",
             None),
    ])

# ================================================================ seasonal hibernation, hibernator clade
seasonal = new_row('S9_hib_seasonal_isp', 'isp', 'seasonal torpor bout')

put(seasonal, 6,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="CLASS_FIRST",
    roles_present=["CONTROLS_ENTRY", "ENABLES_EXIT"], roles_tested_negative=[],
    ambiguity=(
        "THE ENABLES_EXIT ENTRY IS THE MOST CONSEQUENTIAL CELL IN THIS ROW and it is why hibernation "
        "was scored. Intracerebroventricular prostaglandin E2 PROVOKES AROUSAL from an established "
        "hibernation bout. Before hibernation was added, `ENABLES_EXIT` was empty across every "
        "endogenous state in the table and present only in anaesthesia. It is no longer empty. "
        "SCOPE, and it is real: the febrile pathway is not the mechanism that TIMES natural interbout "
        "arousal - the authors' point is that febrile signalling remains functional during "
        "hibernation, demonstrated by forcing arousal with it. So this is a pathway that CAN drive "
        "exit, not one shown to schedule normal exit. It is nevertheless scored ENABLES_EXIT, "
        "because that is exactly the standard applied to caffeine in S5_ga_volatile_hsap c6. "
        "SPECIES SCOPE: Spermophilus lateralis, a different genus from the Ictidomys the row is "
        "nominally keyed to; the row covers seasonal obligate hibernators as a clade and this is "
        "declared rather than hidden. The LPS arm is an internal control: LPS alone neither induced "
        "fever nor provoked arousal in hibernating animals, so the arousal is specific to PGE2 "
        "downstream of the blocked step."),
    strongest_grade="E-B", all_grades=["E-B"], negative_assay_statement=None,
    mechanisms=[
        mech("Central prostaglandin E2 provokes arousal from an established hibernation bout",
             [{"role": "ENABLES_EXIT", "evidence_grade": "E-B", "citation_ids": ["PMID:11893609"],
               "basis": "ICV infusion drives arousal from hibernation and induces fever, with an "
                        "internal negative control (LPS alone does neither in hibernating animals)."},
              {"role": "CONTROLS_ENTRY", "evidence_grade": "E-D", "citation_ids": ["PMID:11893609"],
               "basis": "Weak and inferential: a fever developing at the next natural arousal "
                        "extended that arousal sixfold, implying the pathway also modulates how long "
                        "the animal stays out. Graded E-D and not load-bearing."}],
             [{"manipulation": "pharmacological_activation", "direction_of_manipulation": "increase",
               "agent": "prostaglandin E2, intracerebroventricular; LPS intraperitoneal as control",
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "decrease",
                                   "entry_threshold": "not_reported", "survival_recovery": "increase",
                                   "other": "PGE2 provoked arousal and induced fever; LPS in "
                                            "hibernating squirrels induced NEITHER fever NOR arousal; "
                                            "a fever appeared at the next natural arousal and "
                                            "extended it sixfold; arousals consume 60-80% of the "
                                            "winter energy budget"},
               "context_dependence": "state_dependent", "statement": S_PGE,
               "evidence_grade": "E-B", "citation_ids": ["PMID:11893609"]}],
             "OPPOSES_STATE",
             [ch("intracerebroventricular prostaglandin E2", 6, "E-B", ["PMID:11893609"]),
              ch("activation of febrile thermoregulatory signalling that remains intact during the "
                 "bout", 11, "E-B", ["PMID:11893609"]),
              ch("arousal from hibernation", None, "E-B", ["PMID:11893609"])],
             6, [{"name": "prostaglandin E2; febrile signalling pathway", "species": "isp",
                  "identifier": None,
                  "ortholog_relation": "No corresponding entry anywhere else in the table. This is "
                                       "the only mechanism scored as driving exit from a natural "
                                       "reduced-activity state."}],
             ["PMID:11893609"],
             "pharmacological re-engagement of a thermoregulatory set-point pathway that is "
             "preserved but unused during the bout",
             None),
        mech("Septal vasopressin prevents seasonal hibernation",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-B", "citation_ids": ["PMID:2762331"],
               "basis": "Infusion into the lateral septum during autumn-winter abolishes the "
                        "hypothermic bouts the animal would otherwise show; controls hibernate "
                        "normally. The seasonal disappearance of endogenous septal vasopressin is "
                        "the matching natural observation."}],
             [{"manipulation": "pharmacological_activation", "direction_of_manipulation": "increase",
               "agent": "arginine vasopressin, lateral septum infusion",
               "observed_effect": {"total_quiescence": "decrease", "state_structure": "decrease",
                                   "entry_threshold": "increase", "survival_recovery": "not_reported",
                                   "other": "vasopressin-infused hamsters showed almost no periods of "
                                            "hypothermia; control-infused hamsters hibernated "
                                            "normally; endogenous septal vasopressin immunoreactivity "
                                            "is dense in summer and absent in autumn and winter"},
               "context_dependence": "season_dependent", "statement": S_AVP,
               "evidence_grade": "E-B", "citation_ids": ["PMID:2762331"]}],
             "OPPOSES_STATE",
             [ch("vasopressin infusion into the lateral septum", 6, "E-B", ["PMID:2762331"]),
              ch("maintenance of a summer-like thermoregulatory set point", 11, "E-B",
                 ["PMID:2762331"]),
              ch("hibernation prevented", None, "E-B", ["PMID:2762331"])],
             6, [{"name": "arginine vasopressin, lateral septum", "species": "isp",
                  "identifier": "European hamster Cricetus cricetus",
                  "ortholog_relation": None}],
             ["PMID:2762331"],
             "septal peptidergic maintenance of the euthermic thermoregulatory set point",
             None),
    ])

put(seasonal, 11,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="SPECIES_ENDPOINT_FIRST",
    roles_present=["CONTROLS_ENTRY"], roles_tested_negative=[],
    ambiguity=(
        "OBSERVATIONAL, NOT A MANIPULATION, and graded accordingly. CO2 chemosensitivity is blunted "
        "during entrance into hibernation and elevated during arousal, producing a significant "
        "hysteresis at matched body temperature. The authors read the blunting as permitting the CO2 "
        "retention that contributes to metabolic suppression. No intervention was performed, so this "
        "is a measured state-dependent change in a control variable rather than a demonstrated "
        "cause. It is recorded because the ENTRANCE and AROUSAL limbs differ at the same body "
        "temperature, which is a genuine asymmetry between getting into the state and getting out of "
        "it - and this row is where that distinction is under test."),
    strongest_grade="E-D", all_grades=["E-D"], negative_assay_statement=None,
    mechanisms=[
        mech("CO2 chemosensitivity is asymmetrically regulated between entrance and arousal",
             [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-D", "citation_ids": ["PMID:34739575"],
               "basis": "Blunted hypercapnic ventilatory response during entrance is proposed to "
                        "permit the CO2 retention that contributes to metabolic suppression. "
                        "Observational; no manipulation."}],
             [{"manipulation": "none_observational", "direction_of_manipulation": "none",
               "agent": None,
               "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                   "entry_threshold": "not_reported", "survival_recovery": "not_reported",
                                   "other": "respiratory exchange ratio drops on entrance and rises "
                                            "on arousal; CO2 chemosensitivity blunted while RER "
                                            "reduced, then rises late in entrance; at any given body "
                                            "temperature the hypercapnic ventilatory response is "
                                            "LOWER during entrance than arousal - a significant "
                                            "hysteresis; at matched oxygen consumption the two are "
                                            "the same"},
               "context_dependence": "phase_dependent", "statement": (
                   "We observed a significant drop (entrance) and rise (arousal) in the RER produced "
                   "by hypo- and hyperventilation, respectively. CO2 chemo-sensitivity while the RER "
                   "was reduced on entrance was blunted and rose late in entrance. On arousal, CO2 "
                   "chemo-sensitivity was elevated when the RER was elevated and fell immediately "
                   "after RER returned to normal values. At any given Tb, the HCVR was lower during "
                   "entrance compared to arousal producing a significant hysteresis. The HCVR, "
                   "however, was the same at any given VO2 during entrance and arousal."),
               "evidence_grade": "E-D", "citation_ids": ["PMID:34739575"]}],
             "UNDETERMINED",
             [ch("phase-dependent change in central CO2 chemosensitivity", 11, "E-D",
                 ["PMID:34739575"]),
              ch("CO2 retention contributing to metabolic suppression", 8, "E-D", ["PMID:34739575"]),
              ch("entrance-arousal hysteresis at matched body temperature", None, "E-D",
                 ["PMID:34739575"])],
             11, [{"name": "central CO2 chemosensitivity (hypercapnic ventilatory response)",
                   "species": "isp", "identifier": "Ictidomys tridecemlineatus",
                   "ortholog_relation": "The mouse volatile row carries a NALCN/retrotrapezoid entry "
                                        "for the CO2 ventilatory response under anaesthesia "
                                        "(S5_ga_volatile_mmus c1). Same physiological control "
                                        "variable, two states, no molecular claim made here."}],
             ["PMID:34739575"],
             "phase-dependent resetting of the central CO2 set point",
             None),
    ])

# ---------------------------------------------------------------- write + summarise
for row in (daily, seasonal):
    rc = collections.Counter(); cnt = collections.Counter(); cov = 0; srcs = set()
    for c in row['cells']:
        cnt[c['status']] += 1
        if c['coverage'] != 'NOT_TESTED':
            cov += 1
        for m in c['mechanisms']:
            if m.get('state_polarity') != 'NO_ESTABLISHED_EFFECT':
                for r in m['roles']:
                    rc[r['role']] += 1
            srcs.update(m.get('citation_ids', []))
            for p in m['perturbations']:
                srcs.update(p.get('citation_ids', []))
    row['row_summary'].update(coverage_denominator=cov, n_positive=cnt['POSITIVE'],
                              n_suggested=cnt['SUGGESTED'], n_negative=cnt['NEGATIVE'],
                              n_not_tested=cnt['NOT_TESTED'], n_distinct_sources=len(srcs),
                              n_not_applicable=0, role_counts={k: rc[k] for k in ROLES})
    json.dump(row, open(os.path.join(D, row['row_id'] + '.json'), 'w'), indent=1)
    print('%-22s %d/12 populated  roles=%s  sources=%d'
          % (row['row_id'], cov, {k: v for k, v in rc.items() if v}, len(srcs)))
