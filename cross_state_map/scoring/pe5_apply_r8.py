"""PE-5 round-8 — a finding located by the HAS-THIS-ALREADY-BEEN-DONE check on pending experiment PE-A.

  41573848  chemogenetic reactivation of brain-wide anaesthesia-activated ensembles -> S5_ga_volatile_mmus c7

This is the closest anyone has come to producing the anaesthetised state WITHOUT an anaesthetic, and
it is recorded as a role-scoped NEGATIVE on PRODUCES_STATE because the defining endpoint did not move.
It converts claim D2 from "nobody has attempted it" to "it has been attempted at ensemble level and
the axes dissociated", which is a much stronger and much more falsifiable statement.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pe5_apply_findings import mech
from pe5_apply_r2 import add_mech, ch, APPLIED, SKIPPED

APPLIED.clear(); SKIPPED.clear()

S_ENS = ("We take advantage of a mouse that expresses chemogenetic designer receptors exclusively "
         "activated by a designer drug (DREADDs) in an inducible Cre-dependent manner driven by Fos "
         "immediate early gene expression. Since Fos expression peaks with metabolic activity, we use "
         "this system to insert synthetic DREADDs into brain-wide neurons that are active under "
         "isoflurane anesthesia. We then test the behavioral consequences of chemogenetic stimulation "
         "of anesthesia-activated neural ensembles. We observe immobility, discoordination, "
         "anti-nociception, and significantly increased anesthetic sensitivity, but not a loss of "
         "consciousness as measured by the righting reflex.")

add_mech('S5_ga_volatile_mmus', 7,
         mech("Chemogenetic reactivation of brain-wide anaesthesia-activated neuronal ensembles "
              "reproduces several anaesthetic endpoints but NOT loss of consciousness",
              [{"role": "PRODUCES_STATE", "evidence_grade": "E-C", "citation_ids": ["PMID:41573848"],
                "basis": "TESTED AND NEGATIVE on the defining endpoint. Fos-driven DREADD capture of "
                         "the neurons active under isoflurane, then chemogenetic reactivation without "
                         "anaesthetic. Immobility, discoordination and anti-nociception appeared; the "
                         "righting reflex did NOT. Listed under roles_tested_negative."},
               {"role": "CONTROLS_ENTRY", "evidence_grade": "E-C", "citation_ids": ["PMID:41573848"],
                "basis": "The same reactivation significantly INCREASED anaesthetic sensitivity, "
                         "which is an entry-threshold effect and is positive."}],
              [{"manipulation": "chemogenetic_activation", "direction_of_manipulation": "increase",
                "agent": "isoflurane (for ensemble capture); CNO/designer drug for reactivation",
                "observed_effect": {"total_quiescence": "increase", "state_structure": "not_reported",
                                    "entry_threshold": "decrease", "survival_recovery": "not_reported",
                                    "other": "immobility, discoordination and anti-nociception "
                                             "produced; anaesthetic sensitivity significantly "
                                             "increased; LOSS OF CONSCIOUSNESS, as measured by the "
                                             "righting reflex, NOT produced; captured ensemble is "
                                             "sparse and spatially distributed brain-wide (iDISCO+ "
                                             "light-sheet map)"},
                "context_dependence": "endpoint_dependent", "statement": S_ENS,
                "evidence_grade": "E-C", "citation_ids": ["PMID:41573848"]}],
              "CONTEXT_DEPENDENT",
              [ch("Fos-driven DREADD capture of isoflurane-activated neurons brain-wide", 7, "E-C",
                  ["PMID:41573848"]),
               ch("chemogenetic reactivation of that ensemble without anaesthetic present", 7, "E-C",
                  ["PMID:41573848"]),
               ch("immobility, discoordination, anti-nociception and lowered anaesthetic threshold, "
                  "WITHOUT loss of righting", None, "E-C", ["PMID:41573848"])],
              7, [{"name": "isoflurane-activated neuronal ensemble (Fos-captured, brain-wide)",
                   "species": "mmus", "identifier": None, "ortholog_relation": None}],
              ["PMID:41573848"],
              "synthetic re-excitation of the population that the anaesthetic itself activates, "
              "in the absence of the anaesthetic",
              None),
         note=("THE DIRECT TEST OF THE PROJECT'S HEADLINE GAP, AND IT DISSOCIATED THE AXES. Claim D2 "
               "says nothing has been shown to PRODUCE the anaesthetised state. This is the closest "
               "attempt on record: capture the neurons the anaesthetic activates, then drive them "
               "without the drug. Three endpoints moved - immobility, discoordination, "
               "anti-nociception - and the defining one, righting, did not. The gap is therefore no "
               "longer 'unattempted'; it is 'attempted at ensemble level, and the components of the "
               "anaesthetic state came apart under the attempt'. That is a far stronger and far more "
               "falsifiable position for D2 than the absence of evidence it rested on before. "
               "PREPRINT (bioRxiv 2025.12.02.691631), graded E-C on that ground and flagged for "
               "revisit on peer review. SCOPE: an ensemble captured by immediate-early-gene activity "
               "is not a defined cell type and includes whatever was metabolically active under "
               "anaesthesia, so a negative here does not rule out that some specific population is "
               "sufficient - which is exactly the residue pending experiment PE-A now targets."),
         extra_roles=["CONTROLS_ENTRY"], grade="E-C")

# record the tested-negative role at cell level
f = os.path.join(HERE, 'rows_v2', 'S5_ga_volatile_mmus.json')
d = json.load(open(f))
for c in d['cells']:
    if c['class_id'] == 7:
        if 'PRODUCES_STATE' not in c.setdefault('roles_tested_negative', []):
            c['roles_tested_negative'].append('PRODUCES_STATE')
        if not c.get('negative_assay_statement'):
            c['negative_assay_statement'] = (
                "Chemogenetic reactivation of Fos-captured, isoflurane-activated brain-wide ensembles "
                "(PMID:41573848) produced immobility, discoordination and anti-nociception and "
                "significantly increased anaesthetic sensitivity, but did NOT produce loss of "
                "consciousness as measured by the righting reflex. The assay resolved four positive "
                "effects in the same animals, so it had demonstrated power; the defining endpoint "
                "specifically did not move. PREPRINT, E-C.")
json.dump(d, open(f, 'w'), indent=1)

print('APPLIED (%d):' % len(APPLIED))
for a in APPLIED:
    print('  ' + a)
print('SKIPPED (%d):' % len(SKIPPED))
for s in SKIPPED:
    print('  ' + s)
