"""Collect artist identities and genre facts from Wikidata (CC0).

No generated names, no fabricated per-artist vocal/production descriptions.
Each cached response is reusable; only this build script accesses the network.
The deployed app reads the resulting JSON offline.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'research' / 'wikidata'
UA = 'IronVespersPromptStudio/2.0 (https://github.com/HavokRabbit/suno-prompts-pro)'
ENDPOINT = 'https://query.wikidata.org/sparql'

# Regional/scene categories are labelled honestly, rather than treating
# nationality as a sound or padding narrow genres with unrelated artists.
GENRES = {
 'pop': ('Pop', ['pop music','dance-pop','electropop','synth-pop']),
 'rock': ('Rock', ['rock music','alternative rock','hard rock','progressive rock']),
 'hip-hop': ('Hip-hop', ['hip-hop music','hip hop music','trap music','alternative hip hop','East Coast hip hop','West Coast hip hop']),
 'rnb': ('R&B / soul', ['contemporary R&B','rhythm and blues','soul music','neo soul','alternative R&B']),
 'electronic': ('Electronic', ['electronic music','electronica','electronic dance music','ambient music','downtempo']),
 'metal': ('Metal', ['heavy metal','thrash metal','power metal','progressive metal','death metal']),
 'doom': ('Doom / sludge', ['doom metal','stoner rock','stoner metal','sludge metal','funeral doom','drone metal','death-doom']),
 'indie': ('Indie', ['indie rock','indie pop','indie folk','indie music']),
 'jazz': ('Jazz', ['jazz','bebop','hard bop','vocal jazz','jazz fusion','free jazz']),
 'country': ('Country / Americana', ['country music','Americana','alternative country','outlaw country','country pop']),
 'folk': ('Folk / acoustic', ['folk music','folk rock','contemporary folk music','indie folk','bluegrass music']),
 'latin': ('Latin', ['Latin pop','reggaeton','salsa','bachata','cumbia','Latin music','Latin trap']),
 'corrido': ('Corridos / regional Mexican', ['corrido','corridos tumbados','Regional Mexican','regional Mexican','ranchera','norteño','banda music','norteño music']),
 'bollywood': ('Bollywood / filmi', ['filmi','Bollywood','Hindi film music','Indian film music','Bollywood music']),
 'punjabi': ('Punjabi / bhangra', ['Punjabi music','Music of Punjab','bhangra','Bhangra','Punjabi pop']),
 'indian-indie': ('Indian indie', ['indie pop','indie rock','indie folk','alternative rock','Indian pop','Indian rock','Indian indie']),
 'italian': ('Italian pop / rock', ['pop music','rock music','pop rock','indie pop','Italian pop','musica leggera','canzone','Italo disco']),
 'kpop': ('K-pop', ['K-pop','Korean pop']),
 'afrobeats': ('Afrobeats / Afropop', ['Afrobeats','Afropop','African popular music','amapiano','Afro-fusion','afropop']),
 'bedroom': ('Bedroom pop / lo-fi indie', ['bedroom pop','lo-fi music','lo-fi','dream pop','slacker rock']),
 'modern-heavy': ('Metalcore / modern heavy', ['metalcore','post-hardcore','deathcore','djent','nu metal','progressive metalcore']),
 'ccm': ('CCM / worship / gospel', ['contemporary Christian music','contemporary worship music','gospel music','Christian rock','Christian pop','Christian hip hop']),
 'christian': ('Christian metal', ['Christian metal','unblack metal','Christian hardcore','Christian death metal']),
 'hyperpop': ('Hyperpop / digicore', ['hyperpop','digicore','bubblegum bass']),
 'reggae': ('Reggae / dub / dancehall', ['reggae','dub','dancehall','roots reggae','reggae fusion']),
 'dnb': ('Drum & bass / jungle', ['drum and bass','jungle music','liquid funk','neurofunk','darkstep']),
 'techno': ('Techno', ['techno','Detroit techno','minimal techno','hard techno','acid techno']),
 'house': ('House', ['house music','deep house','tech house','progressive house','electro house']),
 'blues': ('Blues', ['blues','electric blues','Chicago blues','Delta blues','blues rock']),
 'punk': ('Punk / post-punk', ['punk rock','post-punk','hardcore punk','pop punk','art punk']),
 'grunge': ('Grunge / post-grunge', ['grunge','post-grunge']),
 'classical': ('Classical / orchestral', ['classical music','contemporary classical music','orchestral music','symphony','film score']),
}
REGION = {'italian':'Q38','indian-indie':'Q668'}

def request(query: str, label: str) -> list[dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(query.encode()).hexdigest()[:16]
    path = CACHE / f'{label}-{key}.json'
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))['results']['bindings']
    url = ENDPOINT+'?'+urllib.parse.urlencode({'query':query,'format':'json'})
    error = None
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/sparql-results+json'})
            with urllib.request.urlopen(req,timeout=65) as response:
                data=json.load(response)
            path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
            time.sleep(1.1)
            return data['results']['bindings']
        except Exception as exc:
            error=exc
            print(f'RETRY {label}: {type(exc).__name__}',flush=True)
            time.sleep(3*(attempt+1))
    raise RuntimeError(f'{label}: {error}')

def collect(key: str) -> dict:
    label, labels = GENRES[key]
    values=' '.join(json.dumps(x)+'@en' for x in labels)
    region=REGION.get(key)
    country = f'{{?artist wdt:P27 wd:{region}}} UNION {{?artist wdt:P495 wd:{region}}}' if region else ''
    if region:country='{'+country+'}'
    # P434 is a MusicBrainz ARTIST id (not recording, release or label).
    # The additional entity-kind guard excludes releases and non-musician businesses.
    query='''SELECT DISTINCT ?artist ?name ?mbid ?desc ?matched ?links WHERE {
      VALUES ?matched { %s }
      ?genre rdfs:label ?matched.
      ?artist wdt:P136 ?genre; rdfs:label ?name.
      OPTIONAL {?artist wdt:P434 ?mbid}
      FILTER(LANG(?name)="en")
      %s
      FILTER(EXISTS {?artist wdt:P31 wd:Q5} || EXISTS {?artist wdt:P31/wdt:P279* wd:Q2088357})
      OPTIONAL {?artist schema:description ?desc. FILTER(LANG(?desc)="en")}
      OPTIONAL {?artist wikibase:sitelinks ?links}
    } ORDER BY DESC(?links) ?name LIMIT 900''' % (values,country)
    rows=request(query,key)
    records={}
    for row in rows:
        qid=row['artist']['value'].rsplit('/',1)[-1]
        rec=records.setdefault(qid,{'wikidata_id':qid,'name':row['name']['value'],'musicbrainz_id':row.get('mbid',{}).get('value',''),'description':row.get('desc',{}).get('value',''),'sitelinks':int(row.get('links',{}).get('value',0)),'matched_genres':[],'category':key})
        tag=row['matched']['value']
        if tag not in rec['matched_genres']:rec['matched_genres'].append(tag)
    return {'category':key,'label':label,'genre_labels':labels,'country_filter':region,'source':ENDPOINT,'license':'CC0-1.0','query':query,'artists':list(records.values())}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('genres',nargs='*');args=parser.parse_args()
    out=ROOT/'research'/'candidates';out.mkdir(parents=True,exist_ok=True)
    report=[]
    for key in args.genres or GENRES:
        try:
            data=collect(key)
            (out/f'{key}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
            report.append({'genre':key,'count':len(data['artists'])})
            print(json.dumps(report[-1]),flush=True)
        except Exception as exc:
            print(f'ERROR {key}: {exc}',flush=True)
            report.append({'genre':key,'error':str(exc)})
    (ROOT/'research'/'collection-latest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if __name__=='__main__': main()
