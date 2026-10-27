"""PE-5 batched five-route search harness.

Runs the full row x class x route query matrix against NCBI eutils, filters out PMIDs already in the
verified ledger, and writes candidate hits for scoring. Route 3 (citation chain) is run separately via
elink on load-bearing papers.

Output: pe5_candidates.tsv  (row, class, route, pmid, year, journal, title)
        pe5_search_log.json (every query run, hit counts -> proves search obligation was discharged)
"""
import json, os, sys, time, urllib.parse, urllib.request, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lit

LED = set(json.load(open(os.path.join(HERE, "ledger.json"))).keys())

ROW_CTX = {
 'S2_core_cele':      ('Caenorhabditis elegans lethargus sleep', 'cele'),
 'S5_ga_volatile_cele': ('Caenorhabditis elegans volatile anesthetic halothane isoflurane', 'cele'),
 'S6_starv_L1_cele':  ('Caenorhabditis elegans L1 arrest starvation sleep quiescence', 'cele'),
 'S7_dauer_cele':     ('Caenorhabditis elegans dauer larva', 'cele'),
 'S8_crypto_cele':    ('Caenorhabditis elegans anhydrobiosis desiccation cryptobiosis dauer', 'cele'),
 'S3_rem_mmus':       ('mouse REM sleep paradoxical sleep', 'mmus'),
 'S4_deep_mmus':      ('mouse NREM slow wave sleep', 'mmus'),
 'S5_ga_volatile_mmus': ('mouse isoflurane halothane volatile anesthesia', 'mmus'),
 'S5_ga_volatile_hsap': ('human sevoflurane isoflurane volatile anesthesia', 'hsap'),
 'S5_ga_propofol_hsap': ('human propofol anesthesia', 'hsap'),
}

CLASS_Q = {
 1:  ['NALCN sodium leak channel', 'UNC79 UNC80', 'background sodium leak conductance'],
 2:  ['potassium leak K2P TREK TASK', 'BK channel KCNMA1 SLO-1', 'GIRK potassium conductance'],
 3:  ['GABA-A receptor', 'glycine receptor chloride', 'inhibitory shunting conductance'],
 4:  ['NMDA receptor', 'AMPA glutamate receptor', 'excitatory receptor block'],
 5:  ['syntaxin SNAP-25 SNARE', 'Munc13 Munc18 STXBP synaptotagmin', 'vesicle release probability presynaptic calcium'],
 6:  ['adenosine galanin orexin hypocretin', 'cholinergic acetylcholine muscarinic', 'neuropeptide neuromodulator FLP-11'],
 7:  ['sleep active neuron circuit VLPO MnPO', 'arousal circuit thalamus brainstem', 'RIS ALA state switching neuron'],
 8:  ['mitochondrial complex I NDUFS4 GAS-1', 'oxidative phosphorylation ATP', 'AMPK NADH redox metabolic sensor'],
 9:  ['transcription factor DAF-16 FoxO', 'DAF-12 developmental program', 'state specific gene expression'],
 10: ['trehalose LEA intrinsically disordered protein', 'permeability barrier membrane stabilization', 'structural protection vitrification'],
 11: ['temperature hypothermia Q10', 'thermoregulation cooling core temperature', 'temperature dependent potency emergence'],
 12: ['gap junction electrical coupling', 'innexin UNC-9 INX-6 CHE-7', 'connexin astrocytic coupling'],
}

NEG_PHRASES = ['knockout no effect unchanged', 'not required normal no difference']

ENDPOINT = {
 'S5_ga_volatile_cele': ['immobility EC50 sensitivity'],
 'S5_ga_volatile_mmus': ['MAC loss of righting emergence'],
 'S5_ga_volatile_hsap': ['MAC bispectral index consciousness'],
 'S5_ga_propofol_hsap': ['loss of consciousness induction dose BIS'],
 'S3_rem_mmus': ['REM amount episode duration atonia'],
 'S4_deep_mmus': ['NREM amount slow wave activity sleep need'],
 'S2_core_cele': ['quiescence bout arousal threshold'],
 'S6_starv_L1_cele': ['sleep fraction survival arrest'],
 'S7_dauer_cele': ['dauer formation entry recovery'],
 'S8_crypto_cele': ['desiccation survival recovery'],
}

def run():
    out, log = [], []
    seen = set()
    rows = list(ROW_CTX.items())
    total = 0
    for rid, (ctx, sp) in rows:
        for cid, syns in CLASS_Q.items():
            queries = []
            # Route 1 + 2 (class terms are molecular synonyms, so these routes co-execute)
            for s in syns:
                queries.append(('CLASS_FIRST/MOLECULE_SYSTEM_FIRST', '%s %s' % (ctx, s)))
            # Route 4
            queries.append(('NEGATIVE_RESULT_SEARCH', '%s %s %s' % (ctx, syns[0], NEG_PHRASES[0])))
            queries.append(('NEGATIVE_RESULT_SEARCH', '%s %s %s' % (ctx, syns[1], NEG_PHRASES[1])))
            # Route 5
            for ep in ENDPOINT.get(rid, []):
                queries.append(('SPECIES_ENDPOINT_FIRST', '%s %s %s' % (ctx, ep, syns[0])))
            for route, q in queries:
                total += 1
                try:
                    ids = lit.esearch(q, n=6)
                except Exception as e:
                    log.append(dict(row=rid, cls=cid, route=route, query=q, error=str(e)))
                    continue
                new = [p for p in ids if ('PMID:' + p) not in LED]
                log.append(dict(row=rid, cls=cid, route=route, query=q, n_hits=len(ids), n_new=len(new)))
                if not new:
                    continue
                try:
                    meta = lit.esummary(new)
                except Exception:
                    continue
                for p in new:
                    d = meta.get(p)
                    if not d:
                        continue
                    key = (rid, cid, p)
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append([rid, str(cid), route, p, d['year'], d['journal'][:28],
                                d['title'][:150].replace('\t', ' ')])
            if total % 60 == 0:
                print('  ...%d queries, %d candidates' % (total, len(out)), flush=True)
    with open(os.path.join(HERE, 'pe5_candidates.tsv'), 'w') as fh:
        fh.write('row\tclass\troute\tpmid\tyear\tjournal\ttitle\n')
        for r in out:
            fh.write('\t'.join(r) + '\n')
    json.dump(log, open(os.path.join(HERE, 'pe5_search_log.json'), 'w'), indent=1)
    print('QUERIES RUN: %d' % total)
    print('CANDIDATE HITS (not already in ledger): %d' % len(out))
    byrow = collections.Counter(r[0] for r in out)
    for k, v in byrow.most_common():
        print('   %-24s %d' % (k, v))

if __name__ == '__main__':
    run()
