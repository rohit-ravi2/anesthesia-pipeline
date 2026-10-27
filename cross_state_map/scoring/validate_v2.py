"""Validate v2 scored rows against SCHEMA_v2.json / REPERTOIRE_v2.md."""
import json, glob, os, sys, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
states = json.load(open(os.path.join(BASE, "states_v2_1.json")))
VALID_CLASSES = {c["class_id"] for c in states["classes"]}
ROWS = {r["row_id"]: r for r in states["rows"]}
GRADES = {"E-A", "E-B", "E-C", "E-D", "E-E", "E-F"}
STRONG = {"E-A", "E-B", "E-C", "E-D"}
ROLES = set(states["roles_instantiated"])
RESERVED = set(states["roles_reserved_not_instantiated"])
# NO_ESTABLISHED_EFFECT added by SCHEMA_v2_2.json amendment (2026-09-17): a MEASURED null with a
# demonstrated-power assay, as distinct from UNDETERMINED (a real effect of unfixed direction).
POLARITY = {"PROMOTES_STATE", "OPPOSES_STATE", "STRUCTURE_ONLY", "CONTEXT_DEPENDENT", "UNDETERMINED",
            "NO_ESTABLISHED_EFFECT"}
APPLIC = {"APPLICABLE", "QUESTIONABLE", "NOT_APPLICABLE"}
DIRS = {"decreased", "unchanged", "increased", "not_measured"}
MEAS = {"MEASURED", "NOT_YET_MEASURED", "NOT_CURRENTLY_DEFINABLE"}
led = json.load(open(os.path.join(BASE, "scoring", "ledger.json")))

errs, warns, rowstats = [], [], []
role_tot = collections.Counter()
status_tot = collections.Counter()

for f in sorted(glob.glob(os.path.join(BASE, "scoring", "rows_v2", "*.json"))):
    d = json.load(open(f)); tag = os.path.basename(f); rid = d["row_id"]
    if rid not in ROWS:
        errs.append(f"{tag}: row_id not in states_v2"); continue
    if not ROWS[rid].get("scoreable"):
        errs.append(f"{tag}: row is not scoreable per states_v2")
    if d.get("state_production") != ROWS[rid]["state_production"]:
        errs.append(f"{tag}: state_production disagrees with states_v2")
    if d.get("schema_version") != "2":
        errs.append(f"{tag}: schema_version != 2")

    seen, counts, covered, napp = set(), collections.Counter(), 0, 0
    srcs, rolecount = set(), collections.Counter()

    for c in d["cells"]:
        cid = c["class_id"]
        if cid in seen: errs.append(f"{tag}: duplicate class {cid}")
        seen.add(cid)
        if cid not in VALID_CLASSES: errs.append(f"{tag}: invalid class {cid}")
        cov, st, sg = c["coverage"], c["status"], c.get("strongest_grade")
        if c.get("applicability") not in APPLIC: errs.append(f"{tag} c{cid}: bad applicability")
        if c["applicability"] == "NOT_APPLICABLE": napp += 1

        # v1 status rule, unchanged
        if cov == "TESTED_POSITIVE":
            expect = "POSITIVE" if sg in STRONG else "SUGGESTED"
        elif cov == "TESTED_NEGATIVE":
            expect = "NEGATIVE"
        else:
            expect = "NOT_TESTED"
        if st != expect:
            errs.append(f"{tag} c{cid}: status {st} violates rule (expected {expect})")
        if cov == "NOT_TESTED" and c["mechanisms"]:
            errs.append(f"{tag} c{cid}: NOT_TESTED but carries mechanisms")
        if cov != "NOT_TESTED": covered += 1
        counts[st] += 1

        # negative statement required for TESTED_NEGATIVE or any role-scoped negative
        if (cov == "TESTED_NEGATIVE" or c.get("roles_tested_negative")) and not c.get("negative_assay_statement"):
            errs.append(f"{tag} c{cid}: negative claim without negative_assay_statement")
        for r in c.get("roles_tested_negative", []):
            if r not in ROLES: errs.append(f"{tag} c{cid}: bad role_tested_negative {r}")

        cell_roles = set()
        for m in c["mechanisms"]:
            if not m.get("perturbations"):
                errs.append(f"{tag} c{cid}: mechanism with no perturbation records")
            # SCHEMA_v2_2 amendment: a mechanism with polarity NO_ESTABLISHED_EFFECT carries a
            # MEASURED NULL. Its roles are the roles that were TESTED AND FOUND ABSENT, so they
            # belong in roles_tested_negative and must NOT enter roles_present or the role counts.
            neg_mech = m.get("state_polarity") == "NO_ESTABLISHED_EFFECT"
            for r in m.get("roles", []):
                if r["role"] in RESERVED:
                    errs.append(f"{tag} c{cid}: RESERVED role {r['role']} used without amendment")
                elif r["role"] not in ROLES:
                    errs.append(f"{tag} c{cid}: bad role {r['role']}")
                elif neg_mech:
                    if r["role"] not in c.get("roles_tested_negative", []):
                        errs.append(f"{tag} c{cid}: NO_ESTABLISHED_EFFECT mechanism asserts role "
                                    f"{r['role']} that is absent from roles_tested_negative")
                else:
                    cell_roles.add(r["role"]); rolecount[r["role"]] += 1
                if r.get("evidence_grade") not in GRADES:
                    errs.append(f"{tag} c{cid}: role without valid grade")
                if not r.get("basis"):
                    errs.append(f"{tag} c{cid}: role without basis")
            if m.get("state_polarity") not in POLARITY:
                errs.append(f"{tag} c{cid}: bad state_polarity {m.get('state_polarity')}")
            for p in m["perturbations"]:
                if not p.get("statement"):
                    errs.append(f"{tag} c{cid}: perturbation missing authoritative statement")
                if p.get("evidence_grade") not in GRADES:
                    errs.append(f"{tag} c{cid}: perturbation bad grade")
                for cit in p.get("citation_ids", []):
                    if cit not in led: errs.append(f"{tag} c{cid}: unverified citation {cit}")
                    srcs.add(cit)
            for s in m["chain"]:
                if s.get("inferred") and s.get("evidence_grade") is not None:
                    errs.append(f"{tag} c{cid}: inferred chain step carries a grade")
            if m.get("proximal_class") not in VALID_CLASSES:
                errs.append(f"{tag} c{cid}: bad proximal_class")
            for cit in m.get("citation_ids", []):
                if cit not in led: errs.append(f"{tag} c{cid}: unverified citation {cit}")
                srcs.add(cit)
        if set(c.get("roles_present", [])) != cell_roles:
            errs.append(f"{tag} c{cid}: roles_present {sorted(c.get('roles_present', []))} != union over mechanisms {sorted(cell_roles)}")

    missing = VALID_CLASSES - seen
    if missing: errs.append(f"{tag}: missing classes {sorted(missing)}")

    # state_production consistency
    if d["state_production"] == "PHYSICALLY_IMPOSED" and rolecount["PRODUCES_STATE"]:
        errs.append(f"{tag}: PHYSICALLY_IMPOSED row carries {rolecount['PRODUCES_STATE']} PRODUCES_STATE role(s)")

    rs = d["row_summary"]
    if rs["coverage_denominator"] != covered:
        errs.append(f"{tag}: coverage_denominator {rs['coverage_denominator']} != {covered}")
    for k, fld in [("POSITIVE","n_positive"),("SUGGESTED","n_suggested"),("NEGATIVE","n_negative"),("NOT_TESTED","n_not_tested")]:
        if rs[fld] != counts[k]: errs.append(f"{tag}: {fld} {rs[fld]} != {counts[k]}")
    if rs.get("n_not_applicable") != napp:
        errs.append(f"{tag}: n_not_applicable {rs.get('n_not_applicable')} != {napp}")
    if rs.get("n_distinct_sources") != len(srcs):
        errs.append(f"{tag}: n_distinct_sources {rs.get('n_distinct_sources')} != {len(srcs)}")
    for r in ROLES:
        if rs["role_counts"].get(r, 0) != rolecount[r]:
            errs.append(f"{tag}: role_counts[{r}] {rs['role_counts'].get(r,0)} != {rolecount[r]}")

    # axes
    for a in d["axes"]:
        if a["axis"] not in {"A_beh","A_neu","A_met"}: errs.append(f"{tag}: bad axis")
        if a.get("measurability") not in MEAS: errs.append(f"{tag} {a['axis']}: bad measurability")
        if a["axis"] == "A_neu":
            sm = a.get("neural_submeasures")
            if not sm: errs.append(f"{tag} A_neu: missing neural_submeasures")
            else:
                for k in ("rate_amplitude","coordination","dynamical_organization"):
                    if k not in sm: errs.append(f"{tag} A_neu: missing submeasure {k}")
                    elif sm[k]["direction"] not in DIRS: errs.append(f"{tag} A_neu.{k}: bad direction")
            if a.get("direction") is not None: errs.append(f"{tag} A_neu: direction must be null (use submeasures)")
        else:
            if a.get("direction") not in DIRS: errs.append(f"{tag} {a['axis']}: bad direction")
            if a.get("neural_submeasures") is not None: errs.append(f"{tag} {a['axis']}: submeasures only on A_neu")
    axkeys = [(a["axis"], a["condition"]) for a in d["axes"]]
    if len(axkeys) != len(set(axkeys)): errs.append(f"{tag}: duplicate (axis, condition)")
    if {a["axis"] for a in d["axes"]} != {"A_beh","A_neu","A_met"}: errs.append(f"{tag}: not all three axes present")

    for k in counts: status_tot[k] += counts[k]
    for k in rolecount: role_tot[k] += rolecount[k]
    rowstats.append((rid, d["state_production"], covered, counts, rolecount, len(srcs)))

print("=" * 96)
print("v2 SCHEMA VALIDATION")
print("=" * 96)
for e in errs: print("ERROR  ", e)
for w in warns: print("WARN   ", w)
if not errs: print("No schema violations.")
print()
print("%-22s %-18s %4s %4s %4s %4s %4s %5s" % ("row", "production", "cov", "POS", "SUG", "NEG", "NT", "srcs"))
for rid, sp, cov, c, rc, ns in rowstats:
    print("%-22s %-18s %4d %4d %4d %4d %4d %5d" % (rid, sp, cov, c["POSITIVE"], c["SUGGESTED"], c["NEGATIVE"], c["NOT_TESTED"], ns))
print("-" * 96)
print("totals: POS %d  SUG %d  NEG %d  NOT_TESTED %d  (%d rows x 12 classes = %d cells)" %
      (status_tot["POSITIVE"], status_tot["SUGGESTED"], status_tot["NEGATIVE"], status_tot["NOT_TESTED"], len(rowstats), 12*len(rowstats)))
print()
print("ROLE ASSIGNMENTS ACROSS ALL SCORED ROWS")
for r in sorted(ROLES):
    print("  %-24s %d" % (r, role_tot[r]))
print()
print("PER-ROW ROLE PROFILE")
print("%-22s %s" % ("row", "  ".join("%-7s" % r[:7] for r in ["PRODUCE","ENTRY","MAINTAIN","PROTECT","BUILD"])))
for rid, sp, cov, c, rc, ns in rowstats:
    print("%-22s %s" % (rid, "  ".join("%-7d" % rc[r] for r in
        ["PRODUCES_STATE","CONTROLS_ENTRY","MAINTAINS_STATE","PROTECTS_THROUGH_STATE","BUILDS_MACHINERY"])))
sys.exit(1 if errs else 0)
