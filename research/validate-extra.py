import json, re, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path("G:/Vespers/suno-prompts-pro-upgrade/research")
d = json.loads((ROOT / "extra-punjabi-indie.json").read_text(encoding="utf-8"))
meta = json.loads((ROOT / "wiki-article-meta.json").read_text(encoding="utf-8"))
docs = {}
for f in ["punjabi-indie-evidence-batch1.json", "punjabi-indie-evidence-batch2.json",
          "punjabi-indie-evidence-batch3.json", "punjabi-indie-evidence-batch4.json"]:
    for r in json.loads((ROOT / f).read_text(encoding="utf-8"))["results"]:
        if r.get("content"):
            docs[r["url"]] = r["content"]

def nz(s):
    return re.sub(r"[^a-z0-9]", "", s.casefold())

def nk(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.casefold())

print("records", len(d), Counter(r["category"] for r in d))
keys = {"name", "category", "source_url", "evidence", "matched_genres"}
print("bad schema", [r["name"] for r in d if set(r) != keys or not r["name"] or not r["source_url"].startswith("https://")])
names = [nk(r["name"]) for r in d]
print("dupe names", [n for n, c in Counter(names).items() if c > 1])
base = json.loads(Path("G:/Vespers/suno-prompts-pro-baseline/artists.json").read_text(encoding="utf-8"))
print("baseline overlap", [r["name"] for r in d if nk(r["name"]) in {nk(n) for n in base}])
print("artifacts", [r["name"] for r in d if "{{" in r["evidence"] or "\\" in r["evidence"] or "may refer to" in r["evidence"]])
print("source hosts", Counter(re.sub(r"https://([^/]+)/.*", r"\1", r["source_url"]) for r in d))

bad = []
for r in d:
    ev = r["evidence"]
    if ev.startswith("Wikipedia: \""):
        q = ev.split("Wikipedia: \"", 1)[1].rsplit("\"", 1)[0]
    elif '": ' in ev:
        q = ev.rsplit('": ', 1)[1]
    else:
        q = ""
    q = q.rstrip("\u2026").strip()
    u = r["source_url"]
    if u.startswith("https://en.wikipedia.org/wiki/"):
        t = [t for t in meta if "https://en.wikipedia.org/wiki/" + t.replace(" ", "_").replace("'", "%27") == u]
        src = meta[t[0]]["extract"] if t else None
    else:
        raw = docs.get(u, "")
        raw = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", raw)
        raw = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)
        src = re.sub(r"\s+", " ", raw) or None
    if not src:
        bad.append((r["name"], "no cached source"))
    elif len(q) > 25 and nz(q)[:60] not in nz(src):
        bad.append((r["name"], q[:70]))
print("quote failures", len(bad), bad[:6])
print("tag dist", Counter(t for r in d for t in r["matched_genres"]).most_common(18))
print("\nsample:")
for r in d[:3] + d[120:123] + d[-3:]:
    print("-", r["category"], "|", r["name"], "|", r["matched_genres"], "|", r["evidence"][:150])
