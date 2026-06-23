"""
Resolve each intervention's citation to a real PubMed reference.

Turns the author-and-topic citation query in data/interventions.csv into a real
PMID, title, journal, and year using NCBI E-utilities (esearch then esummary).
Metadata only, never abstracts, to respect copyright. Writes data/citations.csv.

Because the reference is resolved live from PubMed rather than hardcoded, a wrong
or invented citation query simply returns no hit and is flagged, instead of
silently shipping a fake reference.

Needs internet. Run on your machine:
  python src/pubmed.py
"""

import json
import os
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL = "longevity-evidence-explorer"
EMAIL = "brandon.duplantier@gmail.com"
PAUSE = 0.34  # NCBI etiquette: at most 3 requests per second without an API key


def _get(url):
    with urllib.request.urlopen(url, timeout=20) as resp:
        return resp.read().decode("utf-8")


def resolve(query):
    q = urllib.parse.quote(query)
    base = "&tool={}&email={}".format(TOOL, EMAIL)
    es = _get(EUTILS + "esearch.fcgi?db=pubmed&retmode=json&retmax=1&term=" + q + base)
    ids = json.loads(es).get("esearchresult", {}).get("idlist", [])
    if not ids:
        return None
    pmid = ids[0]
    time.sleep(PAUSE)
    su = _get(EUTILS + "esummary.fcgi?db=pubmed&retmode=json&id=" + pmid + base)
    rec = json.loads(su).get("result", {}).get(pmid, {})
    return {
        "pmid": pmid,
        "title": rec.get("title"),
        "journal": rec.get("fulljournalname") or rec.get("source"),
        "year": (rec.get("pubdate", "") or "")[:4],
        "url": "https://pubmed.ncbi.nlm.nih.gov/{}/".format(pmid),
    }


def main():
    import pandas as pd
    df = pd.read_csv(os.path.join(ROOT, "data", "interventions.csv"))
    out = []
    for _, r in df.iterrows():
        res = None
        try:
            res = resolve(r["citation_query"])
        except Exception as exc:
            print("  [warn] {}: {}".format(r["intervention"], exc))
        if res:
            print("  {} -> PMID {} | {}".format(
                r["intervention"], res["pmid"], (res["title"] or "")[:60]))
            out.append({"intervention": r["intervention"], **res})
        else:
            print("  {} -> no PubMed hit, verify citation_query".format(r["intervention"]))
        time.sleep(PAUSE)
    import pandas as pd
    pd.DataFrame(out).to_csv(os.path.join(ROOT, "data", "citations.csv"), index=False)
    print("[pubmed] wrote data/citations.csv ({} of {} resolved). "
          "Confirm each title matches the claim before publishing.".format(len(out), len(df)))


if __name__ == "__main__":
    main()
