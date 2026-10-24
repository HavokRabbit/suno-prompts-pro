import json, time, urllib.parse, urllib.request, re, sys
UA={"User-Agent":"VespersCatalogResearch/1.0 (artist catalog research; contact dave@ironvespers.example)"}
cats=json.load(open("wiki-categories-probe.json",encoding="utf-8"))
def clean(t):
    return re.sub(r'\s*\((singer|band|musician|rapper|actor|actress|Pakistani singer|Indian band)\)$','',t).strip()
pool=[]
for c in ["Bhangra (music) musicians","Bhangra (music) musical groups","Punjabi singers","Punjabi-language singers","Indian indie rock groups","Indian alternative rock groups","Indian rock music groups","Indian singer-songwriters"]:
    for t in cats[c]:
        if t.startswith("List of"): continue
        if t not in pool: pool.append(t)
print("pool",len(pool))
out={}
def chunks(l,n):
    for i in range(0,len(l),n): yield l[i:i+n]
for batch in chunks(pool,20):
    params={"action":"query","prop":"extracts|revisions|categories","exintro":"1","explaintext":"1","rvprop":"content","rvslots":"main","cllimit":"500","redirects":"1","format":"json","titles":"|".join(batch)}
    url="https://en.wikipedia.org/w/api.php?"+urllib.parse.urlencode(params)
    d=None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=45) as r: d=json.load(r); break
        except Exception as e:
            time.sleep(2+attempt*2)
    if not d: print("FAIL batch",batch[:2]); continue
    for pid,p in d.get("query",{}).get("pages",{}).items():
        title=p.get("title")
        txt=""
        try: txt=p["revisions"][0]["slots"]["main"]["*"]
        except Exception: pass
        m=re.search(r"\|\s*genres?\s*=\s*([^\n]*)",txt,re.I)
        genre=m.group(1) if m else ""
        genre=re.sub(r"<ref.*?</ref>|<ref[^>]*/>","",genre,flags=re.S)
        genre=re.sub(r"\{\{[^}]*\}\}","",genre)
        genre=re.sub(r"\[\[([^\]|]*\|)?","",genre).replace("]]","").strip(" |")
        out[p.get("title")]={
            "extract":(p.get("extract") or "").strip(),
            "genre_field":genre[:300],
            "categories":[c["title"].replace("Category:","") for c in p.get("categories",[])][:60],
        }
    time.sleep(1)
json.dump(out,open("wiki-article-meta.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("fetched",len(out))
