"""Apply PE-5 (corrected boolean protocol) findings to rows. Idempotent: re-running is safe."""
import json, collections, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rows_v2')

def save_and_recompute(d, f):
    rc = collections.Counter(); cnt = collections.Counter(); cov = 0; srcs = set(); napp = 0
    for c in d['cells']:
        cnt[c['status']] += 1
        if c['coverage'] != 'NOT_TESTED': cov += 1
        if c['applicability'] == 'NOT_APPLICABLE': napp += 1
        for m in c['mechanisms']:
            for r in m['roles']: rc[r['role']] += 1
            srcs.update(m.get('citation_ids', []))
            for p in m['perturbations']: srcs.update(p.get('citation_ids', []))
    d['row_summary'].update(coverage_denominator=cov, n_positive=cnt['POSITIVE'], n_suggested=cnt['SUGGESTED'],
        n_negative=cnt['NEGATIVE'], n_not_tested=cnt['NOT_TESTED'], n_distinct_sources=len(srcs),
        n_not_applicable=napp,
        role_counts={k: rc[k] for k in ['PRODUCES_STATE','CONTROLS_ENTRY','MAINTAINS_STATE',
                                        'PROTECTS_THROUGH_STATE','BUILDS_MACHINERY','ENABLES_EXIT']})
    json.dump(d, open(f, 'w'), indent=1)
    return cov, dict(cnt)

def mech(label, roles, perts, pol, chain, prox, mols, cits, phys, ovl=None):
    m = dict(label=label, roles=roles, perturbations=perts, state_polarity=pol, chain=chain,
             proximal_class=prox, upstream_classes=[], molecules=mols, citation_ids=cits,
             proximal_physical_effect=phys)
    if ovl: m['overlap_resolution'] = ovl
    return m

NMDA_STMT = ("Deleting the NMDA receptor GluN1 subunit from LPO abolished calcium signals in all cells and produced "
 "insomnia. Mice of both sexes had highly fragmented NREM sleep-wake patterns and could not generate conventionally "
 "classified REM sleep... sleep homeostasis remained intact after NMDA receptor ablation. We suggest NMDA glutamate "
 "receptor activation stabilizes firing of sleep-on neurons and that mechanisms of sleep maintenance differ from that "
 "of the sleep drive itself.")

# ---------------- 1) mouse REM class 4 ----------------
f = os.path.join(D, 'S3_rem_mmus.json'); d = json.load(open(f))
for c in d['cells']:
    if c['class_id'] == 4 and c['coverage'] == 'NOT_TESTED':
        c.update(coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
          discovery_route="CLASS_FIRST",
          roles_present=["PRODUCES_STATE"], roles_tested_negative=[],
          ambiguity=("GluN1 deletion abolished conventionally classified REM entirely - a production-level phenotype - "
            "but the same manipulation also fragmented NREM, so the receptor is not REM-specific. Sleep HOMEOSTASIS "
            "(delta-power drive) remained intact, which the authors use to separate maintenance machinery from sleep drive."),
          strongest_grade="E-B", all_grades=["E-B"], negative_assay_statement=None,
          mechanisms=[mech(
            "NMDA receptors (GluN1) on GABA neurons of the lateral preoptic hypothalamus are required to generate REM sleep",
            [{"role":"PRODUCES_STATE","evidence_grade":"E-B","citation_ids":["PMID:35649726"],
              "basis":"Conditional GluN1 deletion from LPO abolished calcium signals and mice 'could not generate "
                      "conventionally classified REM sleep'. Absence of the state, not a shift in its amount."}],
            [{"manipulation":"loss_of_function","direction_of_manipulation":"remove","agent":None,
              "observed_effect":{"total_quiescence":"decrease","state_structure":"decrease","entry_threshold":"not_reported",
               "survival_recovery":"not_reported","other":"insomnia; fragmented NREM; REM not generated; effect localised "
               "to LPO (anterior hypothalamic deletion had no effect); originated from NMDA receptors on GABA neurons; "
               "delta-power sleep drive INTACT"},
              "context_dependence":"cell_type_dependent","statement":NMDA_STMT,
              "evidence_grade":"E-B","citation_ids":["PMID:35649726"]}],
            "PROMOTES_STATE",
            [{"step":"GluN1 deletion from lateral preoptic hypothalamus","class_id":4,"role":"proximal","inferred":False,
              "evidence_grade":"E-B","citation_ids":["PMID:35649726"]},
             {"step":"loss of excitatory drive onto LPO GABA neurons","class_id":7,"role":"proximal","inferred":False,
              "evidence_grade":"E-B","citation_ids":["PMID:35649726"]},
             {"step":"REM not generated; NREM fragmented","class_id":None,"role":"proximal","inferred":False,
              "evidence_grade":"E-B","citation_ids":["PMID:35649726"]}],
            4, [{"name":"Grin1 / GluN1 NMDA receptor subunit","species":"mmus","identifier":None,
                 "ortholog_relation":"Worm class-4 evidence is nmr-1/NMDA for nitrous oxide (SUGGESTED, agent-mismatched). "
                 "SAME_PHYSICAL_CLASS, now with a genuine organism-level positive on the mammalian side."}],
            ["PMID:35649726"],
            "loss of ionotropic excitatory drive onto preoptic GABAergic sleep-on neurons, destabilising their firing",
            "SAME_PHYSICAL_CLASS vs worm; EXACT_MOLECULE vs S4_deep_mmus c4")],
          discriminating_experiment=("Separate REM-generation from NREM-stabilisation by restricting GluN1 deletion to "
            "REM-specific LPO subpopulations, or by acute blockade timed to REM onset."),
          notes=("NEW CELL FROM PE-5 under the CORRECTED boolean protocol. The v1 concatenated battery returned zero hits "
            "for this query family. First organism-level class-4 positive in any mammalian sleep row, and it carries a "
            "PRODUCES_STATE role - rare in this table."))
print('S3_rem_mmus', save_and_recompute(d, f))

# ---------------- 2) mouse NREM classes 3 and 4 ----------------
f = os.path.join(D, 'S4_deep_mmus.json'); d = json.load(open(f))
for c in d['cells']:
    if c['class_id'] == 4 and c['coverage'] == 'NOT_TESTED':
        c.update(coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
          discovery_route="CLASS_FIRST", roles_present=["MAINTAINS_STATE"], roles_tested_negative=[],
          ambiguity=("Same manipulation as S3_rem_mmus c4 but a DIFFERENT phenotype: NREM is fragmented rather than "
            "abolished, so the role is maintenance, not production. The authors explicitly separate sleep maintenance "
            "from sleep drive, which remained intact."),
          strongest_grade="E-B", all_grades=["E-B"], negative_assay_statement=None,
          mechanisms=[mech(
            "NMDA receptors on LPO GABA neurons stabilise NREM sleep-wake architecture",
            [{"role":"MAINTAINS_STATE","evidence_grade":"E-B","citation_ids":["PMID:35649726"],
              "basis":"Deletion produced highly fragmented NREM sleep-wake patterns with normal TOTAL sleep and intact "
                      "homeostatic drive - a consolidation phenotype, not a production one."}],
            [{"manipulation":"loss_of_function","direction_of_manipulation":"remove","agent":None,
              "observed_effect":{"total_quiescence":"unchanged","state_structure":"decrease","entry_threshold":"not_reported",
               "survival_recovery":"not_reported","other":"normal total sleep, high sleep-wake fragmentation; transiently "
               "rescued by zolpidem or dexmedetomidine; fragmentation persisted under sleep deprivation despite high propensity"},
              "context_dependence":"cell_type_dependent",
              "statement":("When NMDA receptors are selectively reduced from inhibitory preoptic neurons, mice have normal "
                "total amounts of sleep but high sleep-wake fragmentation, providing a model for studying intractable insomnia."),
              "evidence_grade":"E-B","citation_ids":["PMID:35649726"]}],
            "STRUCTURE_ONLY",
            [{"step":"GluN1 deletion from LPO GABA neurons","class_id":4,"role":"proximal","inferred":False,
              "evidence_grade":"E-B","citation_ids":["PMID:35649726"]},
             {"step":"destabilised firing of sleep-on neurons; fragmented NREM","class_id":None,"role":"proximal",
              "inferred":False,"evidence_grade":"E-B","citation_ids":["PMID:35649726"]}],
            4, [{"name":"Grin1 / GluN1","species":"mmus","identifier":None,
                 "ortholog_relation":"EXACT_MOLECULE shared with S3_rem_mmus c4, DIFFERENT ROLE (MAINTAINS vs PRODUCES)."}],
            ["PMID:35649726"],
            "loss of ionotropic excitatory drive onto preoptic GABAergic sleep-on neurons",
            "EXACT_MOLECULE vs S3_rem_mmus c4, DIFFERENT ROLE")],
          discriminating_experiment=None,
          notes=("NEW CELL FROM PE-5. THE SAME MOLECULE AND THE SAME EXPERIMENT YIELD A DIFFERENT ROLE IN THE TWO SLEEP "
            "ROWS - PRODUCES_STATE for REM, MAINTAINS_STATE for NREM. Cleanest demonstration in the project that causal "
            "role is a property of the STATE, not of the molecule."))
    if c['class_id'] == 3 and c['coverage'] == 'NOT_TESTED':
        c.update(coverage="TESTED_POSITIVE", status="POSITIVE", applicability="APPLICABLE",
          discovery_route="CLASS_FIRST", roles_present=["MAINTAINS_STATE"], roles_tested_negative=[],
          ambiguity="The phenotype is electrocortical (EEG spectral content), not sleep amount. Whether altered oscillations change sleep function is untested.",
          strongest_grade="E-B", all_grades=["E-B"], negative_assay_statement=None,
          mechanisms=[mech(
            "delta-subunit GABA-A receptors on parvalbumin interneurons maintain normal sleep-state cortical oscillations",
            [{"role":"MAINTAINS_STATE","evidence_grade":"E-B","citation_ids":["PMID:40204438"],
              "basis":"Conditional deletion altered NREM and REM EEG spectral content; viral reintroduction of Gabrd into "
                      "PV+ interneurons RESCUED the REM phenotype - a loss/rescue pair on the state's electrocortical signature."}],
            [{"manipulation":"loss_of_function","direction_of_manipulation":"remove","agent":None,
              "observed_effect":{"total_quiescence":"not_reported","state_structure":"decrease","entry_threshold":"not_reported",
               "survival_recovery":"not_reported","other":"increased oscillatory activity in NREM; transient high-amplitude "
               "theta bursts in REM; rescued by viral Gabrd reintroduction into PV+ interneurons"},
              "context_dependence":"cell_type_dependent",
              "statement":("PV delta-cKO mice showed altered spectral content of EEG during NREM and REM sleep that was a "
                "result of increased oscillatory activity in NREM and the emergence of transient high-amplitude bursts of "
                "theta-frequency activity during REM. Viral reintroduction of Gabrd to PV+ interneurons rescued REM EEG phenotypes."),
              "evidence_grade":"E-B","citation_ids":["PMID:40204438"]}],
            "STRUCTURE_ONLY",
            [{"step":"conditional deletion of Gabrd from PV+ interneurons","class_id":3,"role":"proximal","inferred":False,
              "evidence_grade":"E-B","citation_ids":["PMID:40204438"]},
             {"step":"loss of tonic extrasynaptic inhibition of PV+ interneurons","class_id":3,"role":"proximal",
              "inferred":False,"evidence_grade":"E-B","citation_ids":["PMID:40204438"]},
             {"step":"altered NREM and REM cortical oscillations","class_id":None,"role":"proximal","inferred":False,
              "evidence_grade":"E-B","citation_ids":["PMID:40204438"]}],
            3, [{"name":"Gabrd (GABA-A delta subunit) on PV+ interneurons","species":"mmus","identifier":None,
                 "ortholog_relation":"Worm class-3 sleep evidence is a TESTED_NEGATIVE (GABA not required for lethargus "
                 "quiescence). Mouse gives a positive for a DIFFERENT readout - oscillation structure, not quiescence amount. "
                 "SAME_PHYSICAL_CLASS on non-comparable endpoints; NOT a species contradiction."}],
            ["PMID:40204438"],
            "loss of tonic extrasynaptic chloride conductance on fast-spiking interneurons, altering network oscillation structure",
            "SAME_PHYSICAL_CLASS vs worm, non-comparable endpoints")],
          discriminating_experiment=("Measure sleep amount and fragmentation, not only EEG spectra, in PV-Gabrd cKO mice, "
            "to determine whether the oscillation phenotype carries any change in the state itself."),
          notes=("NEW CELL FROM PE-5. Contrast with worm is endpoint-driven, not species-driven: worm class 3 in sleep is a "
            "TESTED_NEGATIVE for quiescence; mouse class 3 is a POSITIVE for oscillation structure."))
print('S4_deep_mmus', save_and_recompute(d, f))

# ---------------- 3) mouse volatile class 1: NALCN activated by volatiles ----------------
f = os.path.join(D, 'S5_ga_volatile_mmus.json'); d = json.load(open(f))
for c in d['cells']:
    if c['class_id'] == 1 and not any('retrotrapezoid' in m['label'] for m in c['mechanisms']):
        c['all_grades'] = sorted(set(c['all_grades'] + ["E-B", "E-D"]))
        c['roles_present'] = sorted(set(c['roles_present'] + ["PROTECTS_THROUGH_STATE"]))
        c['ambiguity'] = (c.get('ambiguity') or '') + (
          " PE-5 ADDITION: a second, mechanistically explicit line now exists. Volatile anaesthetics DIRECTLY ACTIVATE the "
          "NALCN-mediated leak conductance in retrotrapezoid nucleus neurons, and NALCN there is required for the CO2 "
          "ventilatory response during anaesthesia. CRITICAL ENDPOINT DISTINCTION: that endpoint is RESPIRATORY OUTPUT, not "
          "the anaesthetic state endpoint, so it cannot be read as NALCN producing or gating anaesthesia. AGENT-SPECIFIC: "
          "isoflurane and sevoflurane activate the conductance; PROPOFOL DOES NOT.")
        c['mechanisms'].append(mech(
          "Volatile anaesthetics activate NALCN sodium leak conductance in retrotrapezoid nucleus neurons, preserving respiratory drive during anaesthesia",
          [{"role":"PROTECTS_THROUGH_STATE","evidence_grade":"E-B","citation_ids":["PMID:32773689"],
            "basis":"Genetic silencing of NALCN in the retrotrapezoid nucleus diminished the CO2 ventilatory response DURING "
                    "isoflurane anaesthesia. The mechanism preserves a vital function through the state; it does not produce, "
                    "gate or maintain the state itself."}],
          [{"manipulation":"pharmacological_activation","direction_of_manipulation":"increase","agent":"isoflurane",
            "observed_effect":{"total_quiescence":"not_reported","state_structure":"not_reported","entry_threshold":"not_reported",
             "survival_recovery":"not_reported","other":"NALCN holding current -75.0+/-12.9 to -130.1+/-34.9 pA (P=0.002), "
             "conductance 1.8+/-0.5 to 3.6+/-1.0 nS (P=0.001) at ~1.5 MAC; Phox2b RTN firing 1.1 to 2.8 Hz (P<0.001), "
             "eliminated by gadolinium or NALCN silencing; sevoflurane comparable; PROPOFOL DID NOT activate the conductance"},
            "context_dependence":"readout_dependent",
            "statement":("Isoflurane and sevoflurane increase neuronal excitability of chemosensitive retrotrapezoid nucleus "
              "neurons partly by enhancing sodium leak channel conductance. Sodium leak channel expression in the "
              "retrotrapezoid nucleus is required for the ventilatory response to carbon dioxide during anesthesia by "
              "isoflurane and sevoflurane."),
            "evidence_grade":"E-B","citation_ids":["PMID:32773689"]}],
          "UNDETERMINED",
          [{"step":"volatile anaesthetic acts on Phox2b RTN neurons","class_id":None,"role":"proximal","inferred":False,
            "evidence_grade":"E-D","citation_ids":["PMID:32773689"]},
           {"step":"increased NALCN-mediated sodium leak conductance","class_id":1,"role":"proximal","inferred":False,
            "evidence_grade":"E-B","citation_ids":["PMID:32773689"]},
           {"step":"preserved CO2 ventilatory response during anaesthesia","class_id":None,"role":"proximal","inferred":False,
            "evidence_grade":"E-B","citation_ids":["PMID:32773689"]}],
          1, [{"name":"Nalcn (retrotrapezoid nucleus, Phox2b neurons)","species":"mmus","identifier":None,
               "ortholog_relation":"EXACT_MOLECULE with S3_rem_mmus c1; ORTHOLOGOUS_MOLECULE with worm nca-1/nca-2/unc-79/unc-80."}],
          ["PMID:32773689","PMID:38767833"],
          "increased background sodium leak conductance raising firing of chemosensitive brainstem neurons",
          "EXACT_MOLECULE across mouse rows; ORTHOLOGOUS vs worm"))
        c['notes'] = (c.get('notes') or '') + (
          " PE-5: second mechanism added. NALCN is now implicated in mouse volatile anaesthesia by TWO independent routes "
          "with DIFFERENT roles - Unc79 germline mutation altering anaesthetic sensitivity (CONTROLS_ENTRY), and direct "
          "anaesthetic activation of the conductance preserving respiratory drive (PROTECTS_THROUGH_STATE). The agent "
          "dissociation (volatiles yes, propofol no) constrains any general 'NALCN mediates anaesthesia' claim.")
print('S5_ga_volatile_mmus', save_and_recompute(d, f))

# ---------------- 4) human volatile class 11: reverse causal direction ----------------
f = os.path.join(D, 'S5_ga_volatile_hsap.json'); d = json.load(open(f))
for c in d['cells']:
    if c['class_id'] == 11 and not any('thermoregulatory defences' in m['label'] for m in c['mechanisms']):
        c['all_grades'] = sorted(set(c['all_grades'] + ["E-C"]))
        c['ambiguity'] = (c.get('ambiguity') or '') + (
          " PE-5 ADDITION - THE COUPLING IS BIDIRECTIONAL. Existing evidence is temperature -> anaesthetic requirement "
          "(cooling lowers MAC). Added evidence is the REVERSE: isoflurane dose-dependently and NON-LINEARLY lowers the "
          "vasoconstriction and shivering thresholds by ~4.6 degC at 1% end-tidal in humans. The two variables are mutually "
          "coupled rather than one being a confound on the other.")
        c['mechanisms'].append(mech(
          "Volatile anaesthesia impairs thermoregulatory defences in humans (state-induced consequence, not a state mechanism)",
          [],
          [{"manipulation":"pharmacological_activation","direction_of_manipulation":"increase","agent":"isoflurane",
            "observed_effect":{"total_quiescence":"not_reported","state_structure":"not_reported","entry_threshold":"not_reported",
             "survival_recovery":"not_reported","other":"vasoconstriction and shivering thresholds each reduced ~4.6 degC at "
             "1% end-tidal, non-linearly and dose-dependently; vasoconstriction-to-shivering range unchanged (1.5+/-0.8 degC); "
             "n=8 volunteers, 4 randomised days"},
            "context_dependence":"dose_dependent",
            "statement":("Isoflurane administration produced a dose-dependent reduction in the vasoconstriction and shivering "
              "thresholds, decreasing each approximately 4.6 degrees C at an end-tidal concentration of 1%."),
            "evidence_grade":"E-C","citation_ids":["PMID:8712437"]}],
          "UNDETERMINED",
          [{"step":"volatile anaesthetic exposure","class_id":None,"role":"proximal","inferred":False,
            "evidence_grade":"E-C","citation_ids":["PMID:8712437"]},
           {"step":"reduced thermoregulatory response thresholds","class_id":11,"role":"proximal","inferred":False,
            "evidence_grade":"E-C","citation_ids":["PMID:8712437"]}],
          11, [], ["PMID:8712437"],
          "suppression of central thermoregulatory response thresholds, widening the interthreshold range and permitting core cooling",
          "state-induced consequence; no causal role on the state"))
        c['notes'] = (c.get('notes') or '') + (
          " PE-5: role-less mechanism added capturing the REVERSE causal direction. Class 11 here now holds both directions: "
          "temperature -> MAC (CONTROLS_ENTRY) and anaesthesia -> thermoregulation (no role, consequence). This "
          "bidirectionality is the strongest single argument for a dedicated thermal PHENOTYPE axis, because the consequence "
          "direction has nowhere to live except as a role-less mechanism.")
print('S5_ga_volatile_hsap', save_and_recompute(d, f))
