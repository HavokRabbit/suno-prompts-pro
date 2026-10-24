import json, time, urllib.parse, urllib.request, re
UA={"User-Agent":"VespersCatalogResearch/1.0 (artist catalog research; contact dave@ironvespers.example)"}
titles=["Nirmal Sidhu","Benny Dhaliwal","Mangi Mahal","Ravinder Grewal","Babbal Rai","Amrit Maan","Jordan Sandhu","Jass Bajwa","Navv Inder","Parmish Verma","Geeta Zaildar","Prakash Kaur","Jagmohan Kaur","Ranjit Kaur","Barkat Sidhu"]
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
        out[p.get("title")]={"extract":(p.get("extract") or "").strip(),"genre_field":(m.group(1) if m else "")[:300],"categories":[c["title"].replace("Category:","") for c in p.get("categories",[])][:40]}
    time.sleep(1)
meta2=json.load(open("wiki-article-meta.json",encoding="utf-8")); meta2.update(out)
json.dump(meta2,open("wiki-article-meta.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("added",len(out))
for t,m in out.items(): print(t,'|',m['genre_field'][:70],'|',m['extract'][:170])
