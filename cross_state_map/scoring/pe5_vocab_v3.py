"""PE-5 search vocabulary v3 — repaired against the eight measured Gate-C misses.

v2 raised measured internal recall from 0.05 to 0.90. The recall control then named exactly which
eight known papers the battery still could not reach, and a component-wise diagnostic (species AND
pmid[uid], state AND pmid[uid], class AND pmid[uid]) attributed each miss to a specific group:

  27806374 Funato 2016 forward-genetics sleep      STATE  REM group lacked bare "sleep"
  30297727 galanin VLPO sleep and heat loss        STATE  NREM group lacked bare "sleep"
  11020764 enflurane AMPA/NMDA spinal motor neuron STATE  volatile group lacked enflurane
  9398952  physostigmine raises propofol dose      CLASS  6 lacked cholinesterase inhibitors
  14504163 physostigmine antagonises sevoflurane   CLASS  6 lacked cholinesterase inhibitors
  32807382 circadian emergence, locus coeruleus    CLASS  6 lacked monoaminergic arousal terms
  33712439 dauer via AWC/ASI chemosensation        CLASS  7 lacked sensory-neuron terms
  11374601 hypothermia and isoflurane MAC          DEPTH  all three groups hit; ranked below 200

Seven were vocabulary; one was retrieval depth, which is why human depth rises to 400 here.

SCOPE: this file changes the SEARCH INSTRUMENT only. The frozen mechanism-class definitions in
REPERTOIRE.md are untouched; nothing here alters what a class means, only which strings are used to
look for it. Logged as an amendment because it changes the measured protocol.
"""
from pe5_search_v2 import grp

SPECIES = {
 'cele': grp(["Caenorhabditis elegans", "C elegans", "nematode", "worms"]),
 # hibernators are a clade, not one species: seasonal obligate hibernators (ground squirrel,
 # hamster, bear, bat) are grouped because no single one has enough mechanism literature alone.
 'isp':  grp(["ground squirrel", "Ictidomys", "Spermophilus", "Urocitellus", "hibernator",
              "hibernating", "hamster", "marmot", "bat", "bear", "dormouse", "Tenrec"]),
 'mmus': grp(["mice", "mouse", "murine"]),
 'hsap': grp(["human", "humans", "volunteers", "patients", "children", "pediatric",
              "paediatric", "infants", "adults", "subjects"]),
}

STATE = {
 'S2_core_cele':        grp(["lethargus", "sleep", "quiescence"]),
 'S5_ga_volatile_cele': grp(["halothane", "isoflurane", "enflurane", "volatile anesthetic",
                             "volatile anaesthetic", "anesthetic", "anaesthetic"]),
 'S6_starv_L1_cele':    grp(["L1 arrest", "starvation", "quiescence", "sleep"]),
 'S7_dauer_cele':       grp(["dauer", "diapause"]),
 'S8_crypto_cele':      grp(["anhydrobiosis", "desiccation", "cryptobiosis"]),
 'S3_rem_mmus':         grp(["REM sleep", "paradoxical sleep", "REM", "rapid eye movement", "sleep"]),
 'S4_deep_mmus':        grp(["NREM", "slow wave sleep", "slow-wave", "non-REM", "delta power", "sleep"]),
 'S5_ga_volatile_mmus': grp(["isoflurane", "halothane", "sevoflurane", "enflurane", "desflurane",
                             "volatile anesthetic", "volatile anaesthetic", "inhaled anesthetic",
                             "general anesthesia", "general anaesthesia"]),
 'S5_ga_volatile_hsap': grp(["sevoflurane", "isoflurane", "desflurane", "enflurane", "halothane",
                             "volatile anesthetic", "volatile anaesthetic", "inhaled anesthetic"]),
 'S5_ga_propofol_hsap': grp(["propofol"]),
 'S9_hib_seasonal_isp': grp(["hibernation", "hibernating", "torpor", "torpid", "torpor bout",
                             "interbout arousal", "deep torpor"]),
 'S9_hib_daily_mmus':   grp(["daily torpor", "torpor", "torpid", "fasting-induced torpor",
                             "hypometabolism", "hibernation"]),
}

from pe5_search_v2 import ENDPOINT as _EP_BASE  # no miss was ever attributed to the endpoint groups
ENDPOINT = dict(_EP_BASE)
ENDPOINT['S9_hib_seasonal_isp'] = grp(["torpor bout", "body temperature", "metabolic rate",
                                       "arousal", "T b", "oxygen consumption", "heart rate"])
ENDPOINT['S9_hib_daily_mmus'] = grp(["torpor bout", "body temperature", "metabolic rate",
                                     "arousal", "oxygen consumption", "entry into torpor"])

CLASS = {
 1:  grp(["NALCN", "unc-79", "unc-80", "sodium leak", "nca-1", "nca-2", "leak conductance",
          "background sodium"]),
 2:  grp(["K2P", "TREK", "TASK", "GIRK", "BK channel", "slo-1", "KCNMA1", "potassium conductance",
          "potassium channel", "Kv", "SK channel", "twik"]),
 3:  grp(["GABA-A", "GABAA", "GABAergic", "glycine receptor", "chloride conductance", "unc-49",
          "gabrd", "inhibitory", "muscimol", "benzodiazepine"]),
 4:  grp(["NMDA", "AMPA", "glutamate receptor", "glutamatergic", "nmr-1", "GluN1", "kainate",
          "excitatory transmission"]),
 5:  grp(["syntaxin", "SNAP-25", "SNARE", "VAMP", "synaptobrevin", "Munc13", "Munc18", "STXBP1",
          "synaptotagmin", "unc-64", "unc-13", "neurotransmitter release", "vesicle release",
          "exocytosis", "synaptic vesicle"]),
 6:  grp(["adenosine", "galanin", "orexin", "hypocretin", "acetylcholine", "cholinergic",
          "neuropeptide", "flp-11", "muscarinic", "nicotinic", "physostigmine", "neostigmine",
          "cholinesterase", "norepinephrine", "noradrenaline", "noradrenergic", "serotonin",
          "serotonergic", "dopamine", "dopaminergic", "histamine", "histaminergic",
          "melanin-concentrating hormone", "ectonucleotidase", "monoamine",
          "caffeine", "methylphenidate", "modafinil", "amphetamine", "CD73", "adenosine A1",
          "nociceptin", "galanin neurons"]),
 7:  grp(["VLPO", "preoptic", "arousal", "thalamus", "brainstem", "sleep-active neuron",
          "RIS neuron", "circuit", "locus coeruleus", "basal forebrain", "parafacial",
          "hypothalamus", "sensory neuron", "chemosensory", "interneuron", "AWC", "ASI", "ASJ",
          "neuronal ablation", "nucleus"]),
 8:  grp(["complex I", "NDUFS4", "gas-1", "mitochondrial", "oxidative phosphorylation", "ATP",
          "AMPK", "NADH", "metabolic", "metabolic rate", "oxygen consumption", "glycolysis"]),
 9:  grp(["DAF-16", "FoxO", "DAF-12", "transcription factor", "gene expression", "chromatin",
          "transcriptional"]),
 10: grp(["trehalose", "LEA protein", "intrinsically disordered", "permeability",
          "membrane stabilization", "stomatin", "lipid membrane", "membrane order",
          "disordered protein"]),
 11: grp(["temperature", "hypothermia", "thermoregulation", "Q10", "cooling", "thermal",
          "body temperature", "heat loss", "core temperature", "warming"]),
 12: grp(["gap junction", "electrical coupling", "innexin", "connexin", "unc-9", "inx-6",
          "pannexin"]),
}

from pe5_search_v2 import NEG  # unchanged

# Depth is a MEASURED parameter, not a guess. Calibration history, from pe5_recovery_v3:
#   v2 vocabulary, cele 120 / mmus 200 / hsap 200  -> overall internal recall 0.90
#   v3 vocabulary, cele 120 / mmus 200 / hsap 400  -> overall 0.92; six rows at 1.00
# Broadening the vocabulary at FIXED depth cost recall on the two largest literatures
# (S5_ga_volatile_mmus 0.89 -> 0.83): the extra OR-terms pull in more records, so known papers fall
# past the retrieval cut. Vocabulary breadth and depth must be raised together. The six remaining
# misses were all diagnosed as depth-limited (every query component matched the paper), hence:
# 2026-09-17, second calibration: at 150/500/800 overall internal recall reached 0.98 and
# nine of ten rows hit 1.00. The single remaining miss (PMID:30044241, caffeine emergence)
# sat below rank 800 in a class-6 human query set that is itself capped at ~900 records, so
# human depth is raised again. The human anaesthesia literature is the binding constraint
# in this table and is roughly an order of magnitude larger than the worm literatures.
# 2026-09-17, THIRD calibration, and the two residual misses were different in kind.
#   PMID:30044241 (caffeine emergence, human): NOT a depth problem. The complete class-6
#     human set is 1085 records, below the 1600 cap, and the paper is simply not in it -
#     its abstract names caffeine and never says adenosine. A VOCABULARY gap; 'caffeine'
#     and the other arousal-promoting stimulants are now in class 6.
#   PMID:22540145 (CD73 knockout, mouse NREM): every query component matched individually,
#     so it WAS depth. Mouse depth rises accordingly.
# The general lesson, now measured twice: a residual miss must be attributed to vocabulary
# or to depth by direct diagnostic before either is changed. Raising depth to fix a
# vocabulary gap would have cost thousands of records and fixed nothing.
DEPTH = {'cele': 150, 'mmus': 1200, 'hsap': 1600, 'isp': 600}
