"""Comprehensive analysis pass: branches H, I, J, K, L, M, N over the scored v2 rows.
Reads row files only; writes derived artifacts. Never mutates rows."""
import json, glob, os, collections, itertools, csv

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(BASE, "scoring")
rows = {json.load(open(f))["row_id"]: json.load(open(f)) for f in glob.glob(os.path.join(S, "rows_v2", "*.json"))}
CLS = {c["class_id"]: c["name"] for c in json.load(open(os.path.join(BASE, "states_v2_1.json")))["classes"]}
ORDER = ['S2_core_cele','S5_ga_volatile_cele','S6_starv_L1_cele','S7_dauer_cele','S8_crypto_cele',
         'S3_rem_mmus','S4_deep_mmus','S5_ga_volatile_mmus','S5_ga_volatile_hsap','S5_ga_propofol_hsap']
SH = {'S2_core_cele':'w-lethargus','S5_ga_volatile_cele':'w-volatile','S6_starv_L1_cele':'w-L1sleep',
      'S7_dauer_cele':'w-dauer','S8_crypto_cele':'w-anhydro','S3_rem_mmus':'m-REM','S4_deep_mmus':'m-NREM',
      'S5_ga_volatile_mmus':'m-volatile','S5_ga_volatile_hsap':'h-sevo','S5_ga_propofol_hsap':'h-propofol'}
DOMAIN = {'S2_core_cele':'sleep','S6_starv_L1_cele':'sleep','S3_rem_mmus':'sleep','S4_deep_mmus':'sleep',
          'S5_ga_volatile_cele':'anaesthesia','S5_ga_volatile_mmus':'anaesthesia',
          'S5_ga_volatile_hsap':'anaesthesia','S5_ga_propofol_hsap':'anaesthesia',
          'S7_dauer_cele':'dormancy','S8_crypto_cele':'dormancy'}

pop  = {r: {c["class_id"] for c in rows[r]["cells"] if c["coverage"] != "NOT_TESTED"} for r in ORDER}
roles= {r: {c["class_id"]: {x["role"] for m in c["mechanisms"] for x in m["roles"]}
            for c in rows[r]["cells"] if c["coverage"] != "NOT_TESTED"} for r in ORDER}
pol  = {r: {c["class_id"]: {m["state_polarity"] for m in c["mechanisms"]}
            for c in rows[r]["cells"] if c["coverage"] != "NOT_TESTED"} for r in ORDER}

out = []
def P(s=""):
    out.append(s); print(s)

# ---------------- BRANCH M: maintenance gap ----------------
P("="*100); P("BRANCH M - ENTRY / MAINTENANCE / EXIT DISTRIBUTION BY DOMAIN"); P("="*100)
dom_roles = collections.defaultdict(collections.Counter)
for r in ORDER:
    for c in rows[r]["cells"]:
        for m in c["mechanisms"]:
            for x in m["roles"]:
                dom_roles[DOMAIN[r]][x["role"]] += 1
allroles = ["PRODUCES_STATE","CONTROLS_ENTRY","MAINTAINS_STATE","ENABLES_EXIT","PROTECTS_THROUGH_STATE","BUILDS_MACHINERY"]
P("%-14s %s" % ("domain", "  ".join("%-9s" % r[:9] for r in allroles)))
for dmn in ["sleep","anaesthesia","dormancy"]:
    P("%-14s %s" % (dmn, "  ".join("%-9d" % dom_roles[dmn][r] for r in allroles)))
tot_an = sum(dom_roles["anaesthesia"].values())
P("")
P("anaesthesia rows: %d role assignments total; MAINTAINS_STATE = %d (%.0f%%)"
  % (tot_an, dom_roles["anaesthesia"]["MAINTAINS_STATE"], 100*dom_roles["anaesthesia"]["MAINTAINS_STATE"]/max(tot_an,1)))
P("anaesthesia rows: PRODUCES_STATE = %d" % dom_roles["anaesthesia"]["PRODUCES_STATE"])
P("sleep rows:       PRODUCES_STATE = %d of %d (%.0f%%)"
  % (dom_roles["sleep"]["PRODUCES_STATE"], sum(dom_roles["sleep"].values()),
     100*dom_roles["sleep"]["PRODUCES_STATE"]/max(sum(dom_roles['sleep'].values()),1)))

# ---------------- BRANCH I: negatives ----------------
P(""); P("="*100); P("BRANCH I - ALL NEGATIVES (cell-level and role-scoped)"); P("="*100)
negs = []
for r in ORDER:
    for c in rows[r]["cells"]:
        if c["coverage"] == "TESTED_NEGATIVE":
            negs.append((SH[r], c["class_id"], "CELL-LEVEL", c["strongest_grade"], c.get("negative_assay_statement","")))
        if c.get("roles_tested_negative"):
            negs.append((SH[r], c["class_id"], "ROLE-SCOPED:"+",".join(c["roles_tested_negative"]),
                         c["strongest_grade"], c.get("negative_assay_statement","")))
for n in negs:
    P("  %-12s c%-2d %-34s grade=%s" % (n[0], n[1], n[2], n[3]))
P("  TOTAL: %d negatives of 120 cells (%.1f%%)" % (len(negs), 100*len(negs)/120))

# ---------------- BRANCH L: REM dissociation ----------------
P(""); P("="*100); P("BRANCH L - AXIS DIRECTIONS ACROSS ALL ROWS (is the map tracking immobility?)"); P("="*100)
P("%-13s %-10s | %-11s %-11s %-11s | %-12s" % ("row","A_beh","neu:rate","neu:coord","neu:dyn","A_met"))
for r in ORDER:
    beh = [a for a in rows[r]["axes"] if a["axis"]=="A_beh"]
    neu = [a for a in rows[r]["axes"] if a["axis"]=="A_neu"]
    met = [a for a in rows[r]["axes"] if a["axis"]=="A_met"]
    b = "/".join(a["direction"] for a in beh)
    sm = neu[0]["neural_submeasures"] if neu and neu[0].get("neural_submeasures") else None
    ra = "/".join(a["neural_submeasures"]["rate_amplitude"]["direction"] for a in neu if a.get("neural_submeasures"))
    co = "/".join(a["neural_submeasures"]["coordination"]["direction"] for a in neu if a.get("neural_submeasures"))
    dy = "/".join(a["neural_submeasures"]["dynamical_organization"]["direction"] for a in neu if a.get("neural_submeasures"))
    mt = "/".join(a["direction"] for a in met)
    P("%-13s %-10s | %-11s %-11s %-11s | %-12s" % (SH[r], b[:10], ra[:11], co[:11], dy[:11], mt[:12]))
P("")
P("KEY: count of rows where ANY A_neu sub-measure is 'decreased':")
dec = [SH[r] for r in ORDER if any(a.get("neural_submeasures") and
       any(a["neural_submeasures"][k]["direction"]=="decreased" for k in a["neural_submeasures"]) for a in rows[r]["axes"] if a["axis"]=="A_neu")]
P("  %s" % dec)
P("  rows with A_beh decreased: %d of %d" % (sum(1 for r in ORDER if any(a["direction"]=="decreased" for a in rows[r]["axes"] if a["axis"]=="A_beh")), len(ORDER)))

# ---------------- BRANCH K: nesting ----------------
P(""); P("="*100); P("BRANCH K - NESTING TEST (is any state's class-set a subset of another's?)"); P("="*100)
nest = []
for a,b in itertools.permutations(ORDER,2):
    if pop[a] and pop[a] < pop[b]:
        nest.append((SH[a],SH[b],sorted(pop[a]),sorted(pop[b])))
if nest:
    for a,b,pa,pb in nest: P("  %-12s subset of %-12s  %s  <  %s" % (a,b,pa,pb))
else:
    P("  NO strict subset relations exist between any pair of states at class level.")
P("")
P("  class-set sizes: " + ", ".join("%s=%d"%(SH[r],len(pop[r])) for r in ORDER))
P("  pairs where neither is a subset and both non-empty: %d of %d ordered pairs"
  % (sum(1 for a,b in itertools.permutations(ORDER,2) if pop[a] and pop[b] and not pop[a]<=pop[b]), len(ORDER)*(len(ORDER)-1)))

# ---------------- BRANCH J: pairwise overlap ----------------
P(""); P("="*100); P("BRANCH J - PAIRWISE OVERLAP WITH COVERAGE SHOWN BESIDE"); P("="*100)
P("%-26s %6s %6s %8s %9s %10s" % ("pair","shared","union","bothNT","sameRole","oppPolarity"))
rowsout=[]
for a,b in itertools.combinations(ORDER,2):
    sh = pop[a]&pop[b]
    if not sh: continue
    bothNT = len(set(range(1,13)) - (pop[a]|pop[b]))
    same = sum(1 for c in sh if roles[a].get(c) and roles[b].get(c) and roles[a][c]&roles[b][c])
    opp  = sum(1 for c in sh if {"PROMOTES_STATE"} <= pol[a].get(c,set()) and {"OPPOSES_STATE"} <= pol[b].get(c,set())
               or {"OPPOSES_STATE"} <= pol[a].get(c,set()) and {"PROMOTES_STATE"} <= pol[b].get(c,set()))
    P("%-26s %6d %6d %8d %9d %10d" % (SH[a]+"/"+SH[b], len(sh), len(pop[a]|pop[b]), bothNT, same, opp))
    rowsout.append([SH[a],SH[b],len(sh),len(pop[a]|pop[b]),bothNT,same,opp])
with open(os.path.join(S,"pairwise_overlap.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["state_a","state_b","shared_classes","union","both_not_tested","shared_role","opposite_polarity"]); w.writerows(rowsout)

# ---------------- BRANCH N: physical-effect layer ----------------
P(""); P("="*100); P("BRANCH N - PHYSICAL-EFFECT LAYER"); P("="*100)
phys=[]
for r in ORDER:
    for c in rows[r]["cells"]:
        for m in c["mechanisms"]:
            pe = m.get("proximal_physical_effect")
            if pe:
                ro="+".join(x["role"] for x in m["roles"]) or "NO_ROLE"
                mol="; ".join(x["name"] for x in m["molecules"]) or "n/a"
                phys.append([SH[r],c["class_id"],mol,ro,m["state_polarity"],pe,c["strongest_grade"]])
P("  mechanisms carrying proximal_physical_effect: %d" % len(phys))
with open(os.path.join(S,"physical_effect_matrix.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["state","class","molecules","role","polarity","proximal_physical_effect","grade"]); w.writerows(phys)
for p in phys: P("  %-12s c%-2d %-34s %-22s %s" % (p[0],p[1],p[2][:34],p[3][:22],p[5][:60]))

# ---------------- coverage summary ----------------
P(""); P("="*100); P("COVERAGE"); P("="*100)
tot=sum(len(pop[r]) for r in ORDER)
P("  populated cells: %d / %d = %.0f%%" % (tot,12*len(ORDER),100*tot/(12*len(ORDER))))
P("  class breadth: " + ", ".join("c%d=%d"%(c,sum(c in pop[r] for r in ORDER)) for c in range(1,13)))

open(os.path.join(S,"analysis_output.txt"),"w").write("\n".join(out))
print("\n[written: analysis_output.txt, pairwise_overlap.csv, physical_effect_matrix.csv]")
