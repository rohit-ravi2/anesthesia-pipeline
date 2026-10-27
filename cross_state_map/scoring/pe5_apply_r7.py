"""PE-5 round-7 finding.

  35163194  DMH GABAergic neurons and ambient-temperature control of sleep -> S4_deep_mmus c11

NOT APPLIED, with reasons recorded:
  27806374  Funato 2016. Both of its mechanisms are already scored - NALCN gain-of-function at
            S3_rem_mmus c1 and SIK3 at S4_deep_mmus c8. The paper's statement that SIK3 and NALCN
            regulate "the amount of NREMS and REMS, respectively" is a DISSOCIATION BY EMPHASIS, not
            a measured null, so it does NOT license a TESTED_NEGATIVE at S4_deep_mmus c1. That cell
            stays NOT_TESTED. Recording the temptation and the refusal, because turning "respectively"
            into a negative is exactly the error the three-valued logic exists to prevent.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pe5_apply_findings import mech
from pe5_apply_r2 import add_mech, ch, APPLIED, SKIPPED

APPLIED.clear(); SKIPPED.clear()

S_DMH = ("We found that cold exposure (24/20/16/12 degC) increased wakefulness and decreased "
         "non-rapid eye movement (NREM) sleep, while warm exposure (32/36/40/44 degC) increased NREM "
         "sleep and decreased wakefulness compared to 28 degC conditions in wild-type mice. Then, "
         "using non-specific and specific apoptosis, we found that lesions of whole DMH neurons and "
         "DMH gamma-aminobutyric acid (GABA)-ergic neurons induced by caspase-3 virus aggravated the "
         "fluctuation of core body temperature after warm exposure and attenuated the change in "
         "sleep-wake behaviors during cold and warm exposure. However, chemogenetic activation or "
         "inhibition of DMH GABAergic neurons did not affect the sleep-wake cycle.")

add_mech('S4_deep_mmus', 11,
         mech("Dorsomedial hypothalamic GABAergic neurons are required for ambient temperature to "
              "modulate NREM sleep, but are not sufficient to drive it",
              [{"role": "CONTROLS_ENTRY", "evidence_grade": "E-A", "citation_ids": ["PMID:35163194"],
                "basis": "Caspase ablation attenuates the change in sleep-wake behaviour produced by "
                         "cold and warm exposure. The requirement is for the THERMAL CONTROL of entry, "
                         "and the sufficiency test in the same paper is negative."}],
              [{"manipulation": "ablation", "direction_of_manipulation": "remove", "agent": None,
                "observed_effect": {"total_quiescence": "no_change", "state_structure": "decrease",
                                    "entry_threshold": "no_change", "survival_recovery": "not_reported",
                                    "other": "in wild type, cold (24-12 degC) increased wake and "
                                             "decreased NREM while warm (32-44 degC) increased NREM "
                                             "and decreased wake, relative to 28 degC; DMH and DMH-"
                                             "GABA lesions ATTENUATED that temperature-driven change "
                                             "and aggravated core-temperature fluctuation after warm "
                                             "exposure; chemogenetic activation OR inhibition of DMH "
                                             "GABAergic neurons did NOT affect the sleep-wake cycle"},
                "context_dependence": "thermal_challenge_dependent", "statement": S_DMH,
                "evidence_grade": "E-A", "citation_ids": ["PMID:35163194"]}],
              "CONTEXT_DEPENDENT",
              [ch("caspase ablation of DMH GABAergic neurons", 7, "E-A", ["PMID:35163194"]),
               ch("loss of the thermoregulatory relay between preoptic input and sleep-wake output", 11,
                  "E-A", ["PMID:35163194"]),
               ch("ambient temperature no longer modulates NREM amount", None, "E-A",
                  ["PMID:35163194"])],
              11, [{"name": "dorsomedial hypothalamic (DMH) GABAergic neurons", "species": "mmus",
                    "identifier": None,
                    "ortholog_relation": "The other mammalian class-11 entries in this table are "
                                         "preoptic sleep-active neurons driving heat loss "
                                         "(S4_deep_mmus) and anaesthetic effects on thermoregulatory "
                                         "thresholds (S5_ga_volatile_hsap). This adds the reverse "
                                         "direction: temperature acting ON sleep, through a named "
                                         "hypothalamic relay."}],
              ["PMID:35163194"],
              "loss of a hypothalamic relay that converts ambient thermal load into a shift in "
              "sleep-wake balance",
              None),
         note=("REQUIRED BUT NOT SUFFICIENT, demonstrated in one paper by two manipulations pointing "
               "opposite ways: ablation removes the temperature-to-sleep coupling, while chemogenetic "
               "activation OR inhibition changes nothing about the sleep-wake cycle on its own. None "
               "of the six instantiated roles fits this cleanly - it is neither production, "
               "maintenance, entry control in the unconditional sense, protection, construction, nor "
               "exit. THIS IS THE STRONGEST CANDIDATE YET FOR INSTANTIATING THE RESERVED ROLE "
               "`PERMISSIVE_BACKGROUND`, and it is deliberately NOT instantiated here: one paper is "
               "not enough to open a frozen role, and doing so on a single result is precisely the "
               "kind of ontology drift the freeze discipline exists to stop. Recorded as a pending "
               "ontology decision with a named trigger: instantiate `PERMISSIVE_BACKGROUND` when a "
               "SECOND independent required-but-not-sufficient result appears in any row. Scored "
               "meanwhile as CONTROLS_ENTRY with context_dependence 'thermal_challenge_dependent', "
               "which is accurate but under-describes it. CLASS 11 SCOPE: this row's class-11 cell "
               "now carries BOTH directions of the thermal coupling - sleep-active preoptic neurons "
               "driving heat loss, and ambient temperature driving sleep through the DMH. The absence "
               "of a thermal phenotype axis (A_therm) is felt here again."),
         extra_roles=["CONTROLS_ENTRY"], grade="E-A")

print('APPLIED (%d):' % len(APPLIED))
for a in APPLIED:
    print('  ' + a)
print('SKIPPED (%d):' % len(SKIPPED))
for s in SKIPPED:
    print('  ' + s)
