import json, time, urllib.parse, urllib.request, re
UA={"User-Agent":"VespersCatalogResearch/1.0 (artist catalog research; contact dave@ironvespers.example)"}
titles=["Alaap (band)","Intermix (band)","Tru Skool","Avtar Singh Kang","Kaka Bhaniawala","Bombay Rockers","Kaka (singer)","Amar Arshi","Afsana Khan","Alfaaz","Nesdi Jones","Soom T","Rup Magon","Zack Knight","Achanak (band)","Bilal Saeed","Rahim Shah (musician)","Fariha Pervez","Hadiqa Kiani","Ali Sethi","Shae Gill","Momina Mustehsan","Asim Azhar","Shafqat Amanat Ali","Javed Bashir","Sanam Marvi","Quratulain Balouch","Shamoon Ismail"]
def chunks(l,n):
    for i in range(0,len(l),n): yield l[i:i+n]
out={}
for batch in chunks(titles,20):
    params={"action":"query","prop":"extracts|revisions|categories","exintro":"1","explaintext":"1","rvprop":"content","rvslots":"main","cllimit":"500","redirects":"1","format":"json","titles":"|".join(batch)}
    url="https://en.wikipedia.org/w/api.php?"+urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=45) as r: d=json.load(r)
    for pid,p in d.get("query",{}).get("pages",{}).items():
        txt=""
        try: txt=p["revisions"][0]["slots"]["main"]["*"]
        except Exception: pass
        m=re.search(r"\|\s*genres?\s*=\s*([^\n]*)",txt,re.I)
        genre=m.group(1) if m else ""
        out[p.get("title")]={"extract":(p.get("extract") or "").strip(),"genre_field":genre[:300],"categories":[c["title"].replace("Category:","") for c in p.get("categories",[])][:40]}
    time.sleep(1)
meta2=json.load(open("wiki-article-meta.json",encoding="utf-8")); meta2.update(out)
json.dump(meta2,open("wiki-article-meta.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("added",len(out))
for t,m in out.items(): print(t,'|',m['genre_field'][:60],'|',m['extract'][:150])
