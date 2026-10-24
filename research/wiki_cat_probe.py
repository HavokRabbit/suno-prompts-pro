import json, time, urllib.parse, urllib.request
UA = {"User-Agent": "VespersCatalogResearch/1.0 (artist catalog research; contact dave@ironvespers.example)"}
cats = ["Bhangra (music) musicians","Bhangra (music) musical groups","Punjabi-language singers","Punjabi singers","Indian Punjabi singers","Punjabi folk musicians","Pakistani Punjabi singers","Indian indie rock groups","Indian alternative rock groups","Indian indie musicians","Indian indie pop musicians","Indian rock music groups","Indian pop musicians","Indian singer-songwriters","Indian independent musicians","Indian folk singers"]
out={}
for c in cats:
    url="https://en.wikipedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","list":"categorymembers","cmtitle":"Category:"+c,"cmlimit":"500","format":"json"})
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30) as r:
            d=json.load(r)
        m=d.get("query",{}).get("categorymembers",[])
        out[c]=[x["title"] for x in m if x["ns"]==0]
    except Exception as e:
        out[c]=["ERROR: "+repr(e)]
    print(c, len(out[c]))
    time.sleep(1.2)
json.dump(out,open("wiki-categories-probe.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for c,v in out.items():
    print("\n##",c)
    print(v)
