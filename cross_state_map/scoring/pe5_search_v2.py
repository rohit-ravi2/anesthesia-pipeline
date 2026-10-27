"""PE-5 search protocol v2 — BOOLEAN OR-GROUP construction.

WHY v2 EXISTS: the v1 battery concatenated species + state + class synonyms into a single space-
separated string. NCBI eutils ANDs bare terms, so those queries demanded that EVERY term appear.
The recovery control measured recall 0.13 (worm volatile) and 0.00 (mouse volatile) - the battery
recovered almost none of the known load-bearing papers, and its apparently "saturated" yield on the
worm rows was a query artefact, not a fact about the literature.

v2 builds explicit boolean queries:   (species) AND (state|endpoint) AND (class synonyms OR'd)
Diagnostic check: the same target paper returns 0 hits under v1 and is recovered under v2.
"""
import json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lit

LED = set(json.load(open(os.path.join(HERE, "ledger.json"))).keys())

def grp(terms):
    return "(" + " OR ".join('"%s"[tiab]' % t if " " in t else "%s[tiab]" % t for t in terms) + ")"

SPECIES = {
 'cele': grp(["Caenorhabditis elegans", "C elegans", "nematode"]),
 'mmus': grp(["mice", "mouse", "murine"]),
 'hsap': grp(["human", "humans", "volunteers", "patients"]),
}

STATE = {
 'S2_core_cele':        grp(["lethargus", "sleep", "quiescence"]),
 'S5_ga_volatile_cele': grp(["halothane", "isoflurane", "volatile anesthetic", "anesthetic"]),
 'S6_starv_L1_cele':    grp(["L1 arrest", "starvation", "quiescence", "sleep"]),
 'S7_dauer_cele':       grp(["dauer", "diapause"]),
 'S8_crypto_cele':      grp(["anhydrobiosis", "desiccation", "cryptobiosis"]),
 'S3_rem_mmus':         grp(["REM sleep", "paradoxical sleep", "REM"]),
 'S4_deep_mmus':        grp(["NREM", "slow wave sleep", "non-REM"]),
 'S5_ga_volatile_mmus': grp(["isoflurane", "halothane", "sevoflurane"]),
 'S5_ga_volatile_hsap': grp(["sevoflurane", "isoflurane", "desflurane"]),
 'S5_ga_propofol_hsap': grp(["propofol"]),
}

ENDPOINT = {
 'S5_ga_volatile_cele': grp(["immobility", "EC50", "sensitivity"]),
 'S5_ga_volatile_mmus': grp(["minimum alveolar concentration", "MAC", "loss of righting", "emergence"]),
 'S5_ga_volatile_hsap': grp(["minimum alveolar concentration", "MAC", "bispectral", "consciousness"]),
 'S5_ga_propofol_hsap': grp(["loss of consciousness", "induction", "bispectral", "sedation"]),
 'S3_rem_mmus':         grp(["REM sleep", "atonia", "sleep architecture"]),
 'S4_deep_mmus':        grp(["slow wave activity", "sleep homeostasis", "sleep need"]),
 'S2_core_cele':        grp(["quiescence", "arousal threshold", "lethargus"]),
 'S6_starv_L1_cele':    grp(["sleep", "survival", "arrest"]),
 'S7_dauer_cele':       grp(["dauer formation", "recovery", "quiescence"]),
 'S8_crypto_cele':      grp(["survival", "recovery", "desiccation tolerance"]),
}

CLASS = {
 1:  grp(["NALCN", "unc-79", "unc-80", "sodium leak", "nca-1", "nca-2", "leak conductance"]),
 2:  grp(["K2P", "TREK", "TASK", "GIRK", "BK channel", "slo-1", "KCNMA1", "potassium conductance", "potassium channel"]),
 3:  grp(["GABA-A", "GABAA", "glycine receptor", "chloride conductance", "unc-49", "gabrd", "inhibitory"]),
 4:  grp(["NMDA", "AMPA", "glutamate receptor", "glutamatergic", "nmr-1"]),
 5:  grp(["syntaxin", "SNAP-25", "SNARE", "VAMP", "synaptobrevin", "Munc13", "Munc18", "STXBP1", "synaptotagmin", "unc-64", "unc-13", "neurotransmitter release", "vesicle release"]),
 6:  grp(["adenosine", "galanin", "orexin", "hypocretin", "acetylcholine", "cholinergic", "neuropeptide", "flp-11", "muscarinic"]),
 7:  grp(["VLPO", "preoptic", "arousal", "thalamus", "brainstem", "sleep-active neuron", "RIS neuron", "circuit"]),
 8:  grp(["complex I", "NDUFS4", "gas-1", "mitochondrial", "oxidative phosphorylation", "ATP", "AMPK", "NADH", "metabolic"]),
 9:  grp(["DAF-16", "FoxO", "DAF-12", "transcription factor", "gene expression"]),
 10: grp(["trehalose", "LEA protein", "intrinsically disordered", "permeability", "membrane stabilization", "stomatin"]),
 11: grp(["temperature", "hypothermia", "thermoregulation", "Q10", "cooling", "thermal"]),
 12: grp(["gap junction", "electrical coupling", "innexin", "connexin", "unc-9", "inx-6"]),
}

NEG = grp(["unchanged", "no effect", "not required", "no difference", "normal", "does not"])

def run(rows=None, quiet=False):
    rows = rows or list(STATE)
    out, log, seen = [], [], set()
    n = 0
    for rid in rows:
        sp = 'cele' if rid.endswith('_cele') else ('mmus' if rid.endswith('_mmus') else 'hsap')
        for cid, cq in CLASS.items():
            qs = [
                ('CLASS_FIRST/MOLECULE_SYSTEM_FIRST', "%s AND %s AND %s" % (SPECIES[sp], STATE[rid], cq)),
                ('NEGATIVE_RESULT_SEARCH',            "%s AND %s AND %s AND %s" % (SPECIES[sp], STATE[rid], cq, NEG)),
                ('SPECIES_ENDPOINT_FIRST',            "%s AND %s AND %s" % (SPECIES[sp], ENDPOINT[rid], cq)),
            ]
            for route, q in qs:
                n += 1
                try:
                    ids = lit.esearch(q, n=12)
                except Exception as e:
                    log.append(dict(row=rid, cls=cid, route=route, error=str(e))); continue
                new = [p for p in ids if ('PMID:' + p) not in LED]
                log.append(dict(row=rid, cls=cid, route=route, n_hits=len(ids), n_new=len(new)))
                if not new: continue
                try: meta = lit.esummary(new[:12])
                except Exception: continue
                for p in new[:12]:
                    d = meta.get(p)
                    if not d or (rid, cid, p) in seen: continue
                    seen.add((rid, cid, p))
                    out.append([rid, str(cid), route, p, d['year'], d['journal'][:26], d['title'][:145].replace('\t',' ')])
            if not quiet and n % 60 == 0:
                print('  ...%d queries, %d candidates' % (n, len(out)), flush=True)
    with open(os.path.join(HERE, 'pe5_candidates_v2.tsv'), 'w') as fh:
        fh.write('row\tclass\troute\tpmid\tyear\tjournal\ttitle\n')
        for r in out: fh.write('\t'.join(r) + '\n')
    json.dump(log, open(os.path.join(HERE, 'pe5_search_log_v2.json'), 'w'), indent=1)
    print('V2 QUERIES RUN: %d ; CANDIDATES: %d' % (n, len(out)))
    for k, v in collections.Counter(r[0] for r in out).most_common():
        print('   %-24s %d' % (k, v))
    return out

if __name__ == '__main__':
    run()
