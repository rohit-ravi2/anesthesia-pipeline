"""PE-5 round-4 findings.

  30044241  caffeine accelerates emergence, human RCT crossover  -> S5_ga_volatile_hsap c6
  42117732  m.11232T>C ND4 variant and sevoflurane, human        -> S5_ga_volatile_hsap c8
  37770252  isoflurane toxicity in Ndufs4-/- Leigh model, mouse  -> S5_ga_volatile_mmus c8
  27090086  glyoxylate shunt and desiccation tolerance           -> S8_crypto_cele c8
  34903234  LEA-1 null in vivo                                   -> S8_crypto_cele c10, S7_dauer_cele c10
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pe5_apply_findings import mech
from pe5_apply_r2 import put, add_mech, ch, APPLIED, SKIPPED

APPLIED.clear(); SKIPPED.clear()

S_CAF = ("We conducted a single-center, randomized, double-blind crossover study with eight healthy "
         "males. Each subject was anesthetized twice with 1.2% isoflurane for 1 h. During the final 10 "
         "min of each session, participants received an IV infusion of either caffeine citrate (15 "
         "mg/kg...) or saline placebo... The mean time to emergence with saline was 16.5 +/- 3.9 (SD) "
         "min compared to 9.6 +/- 5.1 (SD) min with caffeine (P = 0.002), a difference of 6.9 min (99% "
         "CI, 1.8 to 12), a 42% reduction. Participants emerged at a higher expired isoflurane "
         "concentration, manifested more rapid return to baseline Bispectral Index values, and were "
         "able to participate in psychomotor testing sooner when receiving caffeine.")
S_ND4 = ("All patients shared a mitochondrial DNA haplotype that includes the m.11232T>C genetic "
         "variant, which results in the substitution of proline for leucine at position 158 (L158P) of "
         "the ND4 subunit of respiratory complex I in the electron transport chain. In vitro studies "
         "showed that sevoflurane exposure in cells carrying this genetic variant induces a pronounced "
         "suppression of mitochondrial oxygen consumption, with prominent effects on complex "
         "I-dependent respiratory pathways. In contrast, propofol did not elicit a differential effect "
         "in cells harboring this genetic variant... No adverse events were observed in a subset of "
         "the same individuals when only intravenous anesthesia was used.")
S_LEIGH = ("Isoflurane induced hyperlactataemia, weight loss, and mortality in a concentration- and "
           "duration-dependent manner from 0.2% to 0.6% compared with carrier gas (O2 100%) or mock "
           "(air) exposures... Isoflurane toxicity was significantly reduced in Ndufs4(-/-) exposed "
           "before CNS disease onset, and the macrophage depleting drug pexidartinib attenuated "
           "sequelae of isoflurane toxicity (survival P=0.0008 isoflurane 0.4% vs pexidartinib plus "
           "isoflurane 0.4%). Finally, the laboratory animal standard of care of 100% O2 as a carrier "
           "gas contributed significantly to weight loss and reduced survival.")
S_GS = ("We found that dauer larvae and stationary phase yeast switched into a gluconeogenic mode in "
        "which metabolism was reoriented toward production of sugars from non-carbohydrate sources. "
        "This mode depended on full activity of the glyoxylate shunt (GS), which enables synthesis of "
        "trehalose from acetate. The GS was especially critical during preparation of worms for harsh "
        "desiccation (preconditioning) and during the entry of yeast into stationary phase. Loss of "
        "the GS dramatically decreased desiccation tolerance in both organisms.")
S_LEA = ("We created a null mutant of C. elegans LEA-1... LEA-1 mutant animals formed defective dauer "
         "larvae at high temperature. We confirmed that C. elegans lacking LEA-1 are sensitive to "
         "desiccation. LEA-1 mutants were also sensitive to heat and osmotic stress and were prone to "
         "protein aggregation. During desiccation, LEA-1 expression increased and became more "
         "widespread throughout the body. LEA-1 was required at high levels in body wall muscle for "
         "animals to survive desiccation and osmotic stress, but expression in body wall muscle alone "
         "was not sufficient for stress resistance, indicating a likely requirement in multiple "
         "tissues... we then replaced the sequence of lea-1 with these minimal motifs and found that "
         "C. elegans dauer larvae formed normally and survived osmotic stress and mild desiccation at "
         "the same levels as worms with the full-length protein.")

# ================================================================ 1) human volatile c6 — caffeine
add_mech('S5_ga_volatile_hsap', 6,
         mech("Intravenous caffeine accelerates emergence from isoflurane anaesthesia in humans",
              [{"role": "ENABLES_EXIT", "evidence_grade": "E-A", "citation_ids": ["PMID:30044241"],
                "basis": "Randomised, double-blind, within-subject crossover in healthy volunteers, "
                         "with the drug given DURING maintained anaesthesia and the endpoint measured "
                         "after discontinuation. Exit kinetics, cleanly separated from induction."}],
              [{"manipulation": "pharmacological_activation", "direction_of_manipulation": "increase",
                "agent": "isoflurane 1.2% for 1 h; caffeine citrate 15 mg/kg IV vs saline",
                "observed_effect": {"total_quiescence": "decrease", "state_structure": "not_reported",
                                    "entry_threshold": "not_reported", "survival_recovery": "increase",
                                    "other": "emergence 16.5 +/- 3.9 min on saline vs 9.6 +/- 5.1 min "
                                             "on caffeine, a 42% reduction (P=0.002, 99% CI 1.8-12 "
                                             "min); emergence occurred at a HIGHER expired isoflurane "
                                             "concentration; faster return of BIS to baseline; earlier "
                                             "psychomotor testing; n=8 healthy males; no significant "
                                             "vital-sign differences"},
                "context_dependence": "none_reported", "statement": S_CAF,
                "evidence_grade": "E-A", "citation_ids": ["PMID:30044241"]}],
              "OPPOSES_STATE",
              [ch("intravenous caffeine during maintained isoflurane anaesthesia", 6, "E-A",
                  ["PMID:30044241"]),
               ch("adenosine receptor antagonism and phosphodiesterase inhibition raising arousal drive",
                  6, "E-A", ["PMID:30044241"]),
               ch("emergence at a higher end-tidal anaesthetic concentration", None, "E-A",
                  ["PMID:30044241"])],
              6, [{"name": "caffeine; adenosine receptors", "species": "hsap", "identifier": None,
                   "ortholog_relation": "Adenosine also carries the mouse NREM class-6 entry (CD73), "
                                        "where it PROMOTES the state. Here an adenosine ANTAGONIST "
                                        "opposes the anaesthetised state. SAME_PATHWAY_MODULE, "
                                        "opposite intervention sign, consistent direction of effect."}],
              ["PMID:30044241"],
              "raised arousal drive at a fixed anaesthetic concentration, shifting the concentration "
              "at which consciousness returns",
              None),
         note=("THE HUMAN ROWS' FIRST ENABLES_EXIT, and it matters out of proportion to its size. "
               "Emergence occurred at a HIGHER expired isoflurane concentration, so this is not faster "
               "drug washout - the same brain concentration no longer sustained the state. That is the "
               "cleanest available human evidence that the anaesthetised state is actively held rather "
               "than passively imposed, and it is a direct instance of the project's central claim: "
               "the state is afforded by machinery the organism already has, and the machinery can be "
               "pushed the other way. SCOPE: n=8 healthy males, one agent, one dose."),
         extra_roles=["ENABLES_EXIT"], grade="E-A")

# ================================================================ 2) human volatile c8 — mtDNA variant
put('S5_ga_volatile_hsap', 8,
    coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
    discovery_route="MOLECULE_SYSTEM_FIRST",
    roles_present=["PROTECTS_THROUGH_STATE"], roles_tested_negative=[],
    ambiguity=("ENDPOINT SCOPE IS CRITICAL AND IS STATED FIRST. The human endpoint here is "
               "PERIOPERATIVE NEUROLOGIC OUTCOME - severe acute deterioration or death after general "
               "anaesthesia - NOT the depth, onset or maintenance of the anaesthetised state. The "
               "paper's title says 'hypersensitivity'; the measured human phenotype is harm sustained "
               "THROUGH the state. It is therefore scored PROTECTS_THROUGH_STATE (intact complex I "
               "protects the organism across anaesthesia; the variant removes that protection), which "
               "is the same reading already applied to the NALCN/retrotrapezoid entry in the mouse "
               "volatile row. DESIGN SCOPE: this is an observational human genetic association in "
               "seven patients plus in vitro work on fibroblasts and cybrids, NOT an experimental "
               "manipulation in humans - hence E-C despite the strength of the mechanistic arm. "
               "AGENT DISSOCIATION, and it is the load-bearing control: no adverse events in a subset "
               "of the SAME individuals under intravenous-only anaesthesia, and propofol produced no "
               "differential effect in variant-carrying cells."),
    strongest_grade="E-C", all_grades=["E-C"], negative_assay_statement=None,
    mechanisms=[
        mech("Mitochondrial complex I ND4 variant m.11232T>C removes protection against volatile, but "
             "not intravenous, anaesthesia in humans",
             [{"role": "PROTECTS_THROUGH_STATE", "evidence_grade": "E-C",
               "citation_ids": ["PMID:42117732"],
               "basis": "A shared mtDNA haplotype in seven patients who deteriorated after volatile "
                        "anaesthesia, with an in vitro demonstration that sevoflurane suppresses "
                        "complex I-dependent respiration specifically in variant-carrying cells and "
                        "propofol does not."}],
             [{"manipulation": "natural_genetic_variant", "direction_of_manipulation": "decrease",
               "agent": "sevoflurane and other volatile agents; propofol as control",
               "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                   "entry_threshold": "not_reported", "survival_recovery": "decrease",
                                   "other": "severe acute neurologic deterioration or death after "
                                            "predominantly minor surgery; NO adverse events in a "
                                            "subset of the SAME individuals under intravenous-only "
                                            "anaesthesia; in fibroblasts and cybrids, sevoflurane "
                                            "pronouncedly suppressed oxygen consumption via complex "
                                            "I-dependent pathways; propofol showed no differential "
                                            "effect"},
               "context_dependence": "agent_dependent", "statement": S_ND4,
               "evidence_grade": "E-C", "citation_ids": ["PMID:42117732"]}],
             "UNDETERMINED",
             [ch("m.11232T>C (ND4 L158P) mitochondrial DNA variant", 8, "E-C", ["PMID:42117732"]),
              ch("sevoflurane-induced suppression of complex I-dependent oxygen consumption", 8, "E-C",
                 ["PMID:42117732"]),
              ch("severe perioperative neurologic deterioration", None, "E-C", ["PMID:42117732"])],
             8, [{"name": "MT-ND4 (complex I subunit), m.11232T>C / L158P", "species": "hsap",
                  "identifier": "m.11232T>C",
                  "ortholog_relation": "Complex I now carries an entry in THREE rows: worm volatile "
                                       "(gas-1), mouse volatile (Ndufs4), human volatile (MT-ND4). "
                                       "Different subunits of the same complex, same agent class, "
                                       "same direction. SAME_COMPLEX across three species - the "
                                       "widest mechanism correspondence in the table."}],
             ["PMID:42117732"],
             "volatile-agent inhibition of an already-compromised complex I, collapsing oxidative "
             "capacity below demand",
             {"level": "SAME_COMPLEX",
              "partner": "S5_ga_volatile_cele c8 (gas-1); S5_ga_volatile_mmus c8 (Ndufs4)",
              "justification": "Three species, three different complex I subunits, one agent class, "
                               "one direction: reduced complex I capacity worsens the organism's "
                               "response to volatile anaesthetics and not to intravenous ones. The "
                               "ENDPOINTS differ (immobility EC50 in worm, loss of response in mouse, "
                               "neurologic injury in human), which is why this is recorded as a "
                               "correspondence of mechanism and not of phenotype."}),
    ])

# ================================================================ 3) mouse volatile c8 — Leigh toxicity
add_mech('S5_ga_volatile_mmus', 8,
         mech("Isoflurane is TOXIC, not merely more potent, in the Ndufs4-/- Leigh syndrome model, and "
              "the toxicity is macrophage-dependent",
              [{"role": "PROTECTS_THROUGH_STATE", "evidence_grade": "E-A",
                "citation_ids": ["PMID:37770252"],
                "basis": "Concentration- and duration-dependent mortality, weight loss and "
                         "hyperlactataemia in the knockout, pharmacologically rescued by a CSF1R "
                         "inhibitor. The endpoint is survival through exposure, not anaesthetic depth."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
                "agent": "isoflurane 0.2-0.6%; 100% O2 and air as carrier controls; pexidartinib",
                "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                    "entry_threshold": "not_reported", "survival_recovery": "decrease",
                                    "other": "hyperlactataemia, weight loss and mortality "
                                             "concentration- and duration-dependent from 0.2% to 0.6%; "
                                             "toxicity REDUCED when exposed before CNS disease onset; "
                                             "pexidartinib (CSF1R inhibitor, macrophage depleting) "
                                             "rescued survival P=0.0008; 100% O2 carrier gas itself "
                                             "worsened weight loss and survival"},
                "context_dependence": "disease_stage_dependent", "statement": S_LEIGH,
                "evidence_grade": "E-A", "citation_ids": ["PMID:37770252"]}],
              "UNDETERMINED",
              [ch("Ndufs4 deletion", 8, "E-A", ["PMID:37770252"]),
               ch("isoflurane exposure on a compromised complex I background", 8, "E-A",
                  ["PMID:37770252"]),
               ch("macrophage/CSF1R-dependent inflammatory sequelae", 7, "E-A", ["PMID:37770252"]),
               ch("hyperlactataemia, weight loss and mortality", None, "E-A", ["PMID:37770252"])],
              8, [{"name": "Ndufs4; CSF1R-dependent macrophages", "species": "mmus", "identifier": None,
                   "ortholog_relation": None}],
              ["PMID:37770252"],
              "anaesthetic inhibition of a compromised electron transport chain, with an inflammatory "
              "amplification step that is pharmacologically separable"),
         note=("TWO DISTINCT PHENOTYPES FROM ONE GENOTYPE, and the table must not merge them. The same "
               "Ndufs4-/- animals are (i) 2.5-3x HYPERSENSITIVE - an entry-threshold phenotype, scored "
               "as CONTROLS_ENTRY on the first mechanism in this cell - and (ii) killed by prolonged "
               "low-dose isoflurane, a survival phenotype scored here as PROTECTS_THROUGH_STATE. "
               "Potency and tolerance are different quantities and this cell now carries both. The "
               "macrophage dependence is the most surprising element: the toxicity is not a direct "
               "bioenergetic collapse but requires a CSF1R-dependent inflammatory step, which makes it "
               "a therapeutic target rather than an inevitability. A methodological aside with real "
               "force: the standard 100% O2 carrier gas was itself harmful, so a routine laboratory "
               "convention was confounding the measurement."),
         extra_roles=["PROTECTS_THROUGH_STATE"], grade="E-A")

# ================================================================ 4) cryptobiosis c8 — glyoxylate shunt
add_mech('S8_crypto_cele', 8,
         mech("The glyoxylate shunt drives a gluconeogenic switch required to build desiccation "
              "tolerance during preconditioning",
              [{"role": "BUILDS_MACHINERY", "evidence_grade": "E-A", "citation_ids": ["PMID:27090086"],
                "basis": "The shunt is 'especially critical during preparation of worms for harsh "
                         "desiccation (preconditioning)' - it constructs the protectant pool BEFORE "
                         "the state, which is precisely the frozen definition of BUILDS_MACHINERY."},
               {"role": "PROTECTS_THROUGH_STATE", "evidence_grade": "E-A",
                "citation_ids": ["PMID:27090086"],
                "basis": "Loss of the shunt dramatically decreased desiccation tolerance, i.e. "
                         "survival through the state."}],
              [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "not_reported", "state_structure": "not_reported",
                                    "entry_threshold": "not_reported", "survival_recovery": "decrease",
                                    "other": "metabolism reoriented to gluconeogenesis in dauer larvae "
                                             "and stationary-phase yeast; shunt enables trehalose "
                                             "synthesis from acetate; loss dramatically decreased "
                                             "desiccation tolerance IN BOTH ORGANISMS"},
                "context_dependence": "preconditioning_dependent", "statement": S_GS,
                "evidence_grade": "E-A", "citation_ids": ["PMID:27090086"]}],
              "PROMOTES_STATE",
              [ch("loss of glyoxylate shunt activity", 8, "E-A", ["PMID:27090086"]),
               ch("failure of the gluconeogenic switch during preconditioning", 8, "E-A",
                  ["PMID:27090086"]),
               ch("insufficient trehalose synthesised from acetate", 10, "E-A", ["PMID:27090086"]),
               ch("loss of desiccation tolerance", None, "E-A", ["PMID:27090086"])],
              8, [{"name": "glyoxylate shunt (isocitrate lyase / malate synthase, gei-7/icl-1)",
                   "species": "cele", "identifier": None,
                   "ortholog_relation": "The same requirement holds in S. cerevisiae in the same "
                                        "paper. The shunt is absent from mammals, so this is one of "
                                        "the few mechanisms in the table with NO possible mammalian "
                                        "counterpart - which is itself informative."}],
              ["PMID:27090086"],
              "metabolic rewiring toward gluconeogenesis that supplies the disaccharide used to "
              "stabilise cellular structures during water loss",
              {"level": "SAME_PATHWAY_MODULE", "partner": "S8_crypto_cele c10 (trehalose)",
               "justification": "Class 8 supplies the substrate that class 10 uses. The two cells in "
                                "this row are not independent lines of evidence but successive steps "
                                "of one chain, and the chain field records that explicitly."}),
         note=("THE CLEAREST BUILDS_MACHINERY CASE IN THE TABLE. The requirement is concentrated in "
               "PRECONDITIONING - before the state is entered - and the deficit appears only when the "
               "state is later imposed. This is the distinction the role axis was introduced to carry, "
               "and cryptobiosis is where it is least deniable. It also shows why the project's "
               "premise is not 'convergence': the glyoxylate shunt does not exist in mammals, so this "
               "affordance is available to worms and yeast and simply is not available to us."),
         extra_roles=["BUILDS_MACHINERY", "PROTECTS_THROUGH_STATE"], grade="E-A")

# ================================================================ 5) LEA-1 — crypto and dauer c10
def lea(role_basis):
    return mech("LEA-1, a late-embryogenesis-abundant disordered protein, is required in vivo for "
                "desiccation survival and acts through short defined motifs",
                [{"role": "PROTECTS_THROUGH_STATE", "evidence_grade": "E-A",
                  "citation_ids": ["PMID:34903234"], "basis": role_basis}],
                [{"manipulation": "loss_of_function", "direction_of_manipulation": "remove",
                  "agent": None,
                  "observed_effect": {"total_quiescence": "not_reported",
                                      "state_structure": "not_reported",
                                      "entry_threshold": "not_reported", "survival_recovery": "decrease",
                                      "other": "null mutants sensitive to desiccation, heat and "
                                               "osmotic stress and prone to protein aggregation; "
                                               "defective dauer larvae at high temperature; LEA-1 "
                                               "expression rises and spreads during desiccation; "
                                               "required at high levels in body wall muscle but muscle "
                                               "expression alone NOT sufficient; replacing the gene "
                                               "with minimal motifs restored normal dauer formation "
                                               "and survival of osmotic stress and mild desiccation"},
                  "context_dependence": "tissue_dependent", "statement": S_LEA,
                  "evidence_grade": "E-A", "citation_ids": ["PMID:34903234"]}],
                "PROMOTES_STATE",
                [ch("lea-1 null mutation", 10, "E-A", ["PMID:34903234"]),
                 ch("loss of disordered-protein buffering; protein aggregation", 10, "E-A",
                    ["PMID:34903234"]),
                 ch("failure to survive desiccation and osmotic stress", None, "E-A",
                    ["PMID:34903234"])],
                10, [{"name": "LEA-1 (late embryogenesis abundant protein)", "species": "cele",
                      "identifier": None,
                      "ortholog_relation": "LEA proteins occur in plants, nematodes, tardigrades and "
                                           "rotifers but not in mammals. As with the glyoxylate shunt, "
                                           "this is an affordance mammals do not have."}],
                ["PMID:34903234"],
                "disordered-protein stabilisation of cellular components as water is removed, "
                "preventing aggregation",
                None)


add_mech('S8_crypto_cele', 10,
         lea("Null mutant is sensitive to desiccation; expression rises and becomes body-wide during "
             "desiccation; sufficiency established by motif replacement."),
         note=("A STRUCTURE-FUNCTION RESULT, not just a requirement. Replacing the entire lea-1 coding "
               "sequence with short minimal motifs restored normal dauer formation and survival of "
               "osmotic stress and mild desiccation - so the protective function is carried by "
               "sequence features rather than by a folded architecture. That also bounds the claim "
               "honestly: the motif replacement was tested against MILD desiccation, not the harsh "
               "regime. The tissue result is equally careful: high-level expression in body wall "
               "muscle is REQUIRED but NOT SUFFICIENT, so multiple tissues are involved."),
         extra_roles=["PROTECTS_THROUGH_STATE"], grade="E-A")

add_mech('S7_dauer_cele', 10,
         lea("The same null mutant forms DEFECTIVE DAUER LARVAE at high temperature, and motif "
             "replacement restores normal dauer formation - a dauer-state phenotype distinct from the "
             "desiccation-survival phenotype."),
         note=("ONE GENE, TWO STATES, DIFFERENT PHENOTYPES. In cryptobiosis lea-1 loss costs survival "
               "THROUGH the state; in dauer it costs correct FORMATION of the state, and only at high "
               "temperature. The dauer phenotype is the more surprising of the two, because a "
               "desiccation-protectant protein would not be predicted to be needed to build a larva. "
               "Recorded in both rows with the phenotypes kept distinct rather than merged into "
               "'lea-1 is required for stress states'."),
         extra_roles=["PROTECTS_THROUGH_STATE"], grade="E-A")

print('APPLIED (%d):' % len(APPLIED))
for a in APPLIED:
    print('  ' + a)
print('SKIPPED (%d):' % len(SKIPPED))
for s in SKIPPED:
    print('  ' + s)
