"""Literature search + citation verification for ReducedActivityTable scoring.

Reuses the eutils approach from an earlier dauer citation harness (not included here),
which produced the 108/108 clean PMID sweep.

Every PMID that enters a cell must pass through verify(): the title is FETCHED,
never recalled. Resolution alone is not verification -- the title must be read
against the claim by the scorer.

Usage:
    python3 lit.py search "unc-79 volatile anesthetic C elegans"
    python3 lit.py abs 3576211 9012843
"""
import hashlib, json, os, sys, time, urllib.parse, urllib.request

B = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
os.makedirs(CACHE, exist_ok=True)


def _k(*parts):
    """Stable cache key. Python's builtin hash() is salted per process, so the original key
    scheme produced a cache that never hit across runs -- every rerun re-fetched everything."""
    return hashlib.sha256(repr(parts).encode()).hexdigest()[:24]


def _get(url, key):
    p = os.path.join(CACHE, key)
    if os.path.exists(p):
        return open(p, encoding="utf-8").read()
    err = None
    for _ in range(4):
        try:
            r = urllib.request.urlopen(url, timeout=45).read().decode("utf-8", "replace")
            open(p, "w", encoding="utf-8").write(r)
            time.sleep(0.4)
            return r
        except Exception as e:
            err = e
            time.sleep(2)
    raise err


def esearch(term, n=25, db="pubmed"):
    key = "s_" + _k(term, n, db) + ".json"
    u = B + "esearch.fcgi?db=%s&retmode=json&retmax=%d&term=%s" % (db, n, urllib.parse.quote(term))
    return json.loads(_get(u, key))["esearchresult"].get("idlist", [])


def esummary(pmids, db="pubmed"):
    if not pmids:
        return {}
    pmids = [str(p) for p in pmids]
    key = "m_" + _k(tuple(sorted(pmids)), db) + ".json"
    u = B + "esummary.fcgi?db=%s&retmode=json&id=%s" % (db, ",".join(pmids))
    r = json.loads(_get(u, key))["result"]
    out = {}
    for p in r.get("uids", []):
        d = r[p]
        doi = ""
        for aid in d.get("articleids", []):
            if aid.get("idtype") == "doi":
                doi = aid.get("value", "")
        out[p] = dict(pmid=p, title=d.get("title", ""),
                      authors=[a["name"] for a in d.get("authors", [])][:8],
                      journal=d.get("source", ""), year=(d.get("pubdate", "") or "")[:4],
                      doi=doi, pubtype=d.get("pubtype", []))
    return out


def abstracts(pmids):
    """Fetch abstract text. Primary-source evidence for scoring."""
    if not pmids:
        return ""
    pmids = [str(p) for p in pmids]
    key = "a_" + _k(tuple(sorted(pmids))) + ".txt"
    u = B + "efetch.fcgi?db=pubmed&rettype=abstract&retmode=text&id=%s" % ",".join(pmids)
    return _get(u, key)


def elink(pmids, linkname):
    """Citation chain. linkname is pubmed_pubmed_refs (what these papers cite) or
    pubmed_pubmed_citedin (what cites these papers)."""
    if not pmids:
        return []
    pmids = [str(p) for p in pmids]
    key = "l_" + _k(tuple(sorted(pmids)), linkname) + ".json"
    u = B + "elink.fcgi?dbfrom=pubmed&db=pubmed&retmode=json&linkname=%s&%s" % (
        linkname, "&".join("id=" + p for p in pmids))
    out = set()
    for ls in json.loads(_get(u, key)).get("linksets", []):
        for db in ls.get("linksetdbs", []):
            if db.get("linkname") == linkname:
                out.update(db.get("links", []))
    return sorted(out)


def verify(pmids):
    """Return fetched metadata for the ledger. Caller must read title against claim."""
    m = esummary(pmids)
    missing = [p for p in map(str, pmids) if p not in m]
    return m, missing


def search_report(term, n=20):
    ids = esearch(term, n)
    m = esummary(ids)
    lines = []
    for p in ids:
        d = m.get(p)
        if not d:
            continue
        rev = " [REVIEW]" if any("review" in t.lower() for t in d.get("pubtype", [])) else ""
        lines.append("%s | %s | %s %s | %s%s" % (
            p, d["title"][:145], d["journal"], d["year"],
            (d["authors"][0] if d["authors"] else "?"), rev))
    return "\n".join(lines) if lines else "(no hits)"


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        args = sys.argv[2:]
        n = 20
        if len(args) > 1 and args[-1].isdigit():
            n = int(args[-1]); args = args[:-1]
        print(search_report(" ".join(args), n))
    elif cmd == "abs":
        print(abstracts(sys.argv[2:]))
    elif cmd == "sabs":
        # compact: title line + abstract paragraphs only, affiliations stripped
        txt = abstracts(sys.argv[2:])
        for rec in txt.split("\n\n\n"):
            paras = [" ".join(p.split()) for p in rec.split("\n\n")]
            head = [p for p in paras[:3] if p and not p.startswith("Author information")]
            body = [p for p in paras if len(p) > 320 and "Author information" not in p
                    and not p.startswith("(1)") and "@" not in p[:80]]
            if head:
                print("---", head[0][:200])
                if len(head) > 1:
                    print("   ", head[1][:200])
            for b in body:
                print(b)
            print()
    elif cmd == "verify":
        m, miss = verify(sys.argv[2:])
        for p, d in m.items():
            print(json.dumps(d))
        if miss:
            print("UNRESOLVED:", miss)
