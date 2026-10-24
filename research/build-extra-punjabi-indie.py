"""Build research/extra-punjabi-indie.json.

Reads the baseline catalogue, the automated Wikidata candidate files, cached
Wikipedia article metadata and cached Rolling Stone India list pages, then emits
a JSON array of NEW artist records for the 'punjabi' and 'indian-indie'
categories.  No network access; all source text is cached in research/.

Record shape: {name, category, source_url, evidence, matched_genres}
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = Path("G:/Vespers/suno-prompts-pro-baseline/artists.json")

DIACRITICS = re.compile(r"[^a-z0-9]")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return DIACRITICS.sub("", s.casefold())


def tidy(s: str) -> str:
    """Normalise extraction artefacts without changing wording."""
    s = s.replace("\u2018", "\u2019").replace("_", "")
    s = re.sub(r"\u201c\s+", "\u201c", s)
    s = re.sub(r"\s+\u201d", "\u201d", s)
    s = re.sub(r"\u201d\"", "\u201d", s)
    s = re.sub(r'"\s*\u201d', "\u201d", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def first_sentence(txt: str, cap: int = 240) -> str:
    t = re.sub(r"\s+", " ", txt).strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\u201c\"(])", t)
    out = ""
    for p in parts:
        out = (out + " " + p).strip()
        if len(out) >= 70:
            break
    if len(out) > cap:
        out = out[:cap].rsplit(" ", 1)[0] + "\u2026"
    return tidy(out)


def wiki_url(title: str) -> str:
    return "https://en.wikipedia.org/wiki/" + title.replace(" ", "_").replace("'", "%27")


DISP = re.compile(
    r"\s*\((band|singer|musician|rapper|actress|actor|Indian band|Pakistani singer|"
    r"musical group|Indian singer)\)\s*$",
    re.I,
)


def display(name: str) -> str:
    return DISP.sub("", name).strip()


# ---------------------------------------------------------------- source cache
meta = json.loads((ROOT / "wiki-article-meta.json").read_text(encoding="utf-8"))

docs = {}
for f in ["punjabi-indie-evidence-batch1.json", "punjabi-indie-evidence-batch2.json",
          "punjabi-indie-evidence-batch3.json", "punjabi-indie-evidence-batch4.json"]:
    p = ROOT / f
    if not p.exists():
        continue
    for r in json.loads(p.read_text(encoding="utf-8"))["results"]:
        if r.get("content"):
            docs[r["url"]] = r["content"]

TITLES = {
    "https://rollingstoneindia.com/best-indian-songs-2025/": ("The 50 Best Indian Songs of 2025", "Dec 30, 2025"),
    "https://rollingstoneindia.com/best-indian-indie-songs-2023-dot-taba-chake-mali-aditi-ramesh/": ("The 15 Best Indian Singles of 2023", "Dec 26, 2023"),
    "https://rollingstoneindia.com/the-22-best-indian-independent-singles-of-2022/amp/": ("The 22 Best Indian Independent Singles of 2022", "Dec 28, 2022"),
    "https://rollingstoneindia.com/the-best-indian-indie-songs-of-2023-so-far/amp/": ("The Best Indian Indie Songs of 2023 So Far", "Jul 6, 2023"),
    "https://rollingstoneindia.com/10-best-indian-singles-of-2021/": ("10 Best Indian Singles of 2021", "Dec 22, 2021"),
    "https://rollingstoneindia.com/10-best-indian-singles-of-2020/": ("10 Best Indian Singles of 2020", "Dec 29, 2020"),
    "https://rollingstoneindia.com/10-best-indian-singles-of-2019/": ("10 Best Indian Singles of 2019", "2019"),
    "https://rollingstoneindia.com/10-best-indian-albums-of-2021/": ("10 Best Indian Albums of 2021", "2021"),
    "https://rollingstoneindia.com/best-indian-indie-albums-2023-so-far-indian-ocean-tsumyoki-dreamhour-ramil-ganjoo/": ("The Best Indian Indie Albums of 2023 So Far", "Jul 9, 2023"),
}


def strip_md(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return re.sub(r"[_*]", "", s)


def clean_body(b: str) -> str:
    b = strip_md(b)
    i = b.find("Terms & Conditions")
    if i != -1:
        b = b[i + len("Terms & Conditions"):]
    b = re.sub(r"PreviewE|Play on Spotify|Save on Spotify|Copy link|Privacy Policy|\u00b7", " ", b)
    return tidy(re.sub(r"\s+", " ", b))


def snippet(b: str, cap: int = 230) -> str:
    b = clean_body(b)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\u201c\"(])", b)
    out = ""
    for p in parts:
        out = (out + " " + p).strip()
        if len(out) >= 90:
            break
    if len(out) > cap:
        out = out[:cap].rsplit(" ", 1)[0] + "\u2026"
    return tidy(out)


def entries(text: str):
    pat = re.compile(r"\n(?=(?:#{1,4}\s*)?(?:\d+\.\s*)?\*\*)")
    out = []
    for p in pat.split(text):
        s = p.strip()
        m = re.match(r"(?:#{1,4}\s*)?(?:\d+\.\s*)?\*\*(.+?)\*\*", s, re.S)
        if not m:
            continue
        head = tidy(strip_md(m.group(1)).replace("\\", "").strip()).rstrip(" \u2013-")
        body = re.sub(r"\s+", " ", strip_md(s[m.end():])).strip()
        out.append((head, body))
    return out


ENT = {u: entries(t) for u, t in docs.items() if "rollingstoneindia" in u}


def nkey(s: str) -> str:
    return re.sub(r"[^a-z]", "", s.casefold())


def rni_record(name, src=None, cat="indian-indie"):
    for u in ([src] if src else list(TITLES)):
        for h, b in ENT.get(u, []):
            if nkey(name) and nkey(name) in nkey(h):
                title, date = TITLES[u]
                ev = f'Rolling Stone India, "{title}" ({date}) \u2014 entry "{h}": {snippet(b)}'
                return {"name": name, "category": cat, "source_url": u,
                        "evidence": ev, "matched_genres": []}
    return None


# ------------------------------------------------------------------- filtering
def clean_genre_field(g: str) -> str:
    if not g:
        return ""
    if re.search(r"\|\s*\w+\s*=", g) and not g.strip().startswith("[["):
        return ""
    g = re.sub(r"<ref.*?</ref>|<ref[^>]*/>", "", g, flags=re.S)
    g = re.sub(r"\[\[([^\]|]*\|)?", "", g).replace("]]", "")
    g = re.sub(r"\{\{[^}]*\}\}", "", g)
    g = re.sub(r"<br\s*/?>", "; ", g)
    g = re.sub(r"<!--.*?-->", "", g, flags=re.S)
    g = tidy(re.sub(r"\s+", " ", g).strip(" ;|"))
    if not g or "=" in g or "{{" in g or "}}" in g or "flat list" in g.casefold():
        return ""
    return g


def punjabi_tags(gf: str, ex: str):
    g, e, tags = gf.casefold(), ex.casefold(), []
    fs = re.split(r"(?<=[.!?])\s+", ex.strip())[0].casefold()

    def add(t):
        if t not in tags:
            tags.append(t)

    if "bhangra" in g or "bhangra" in e:
        add("bhangra")
    if "folk" in g or "folk" in e:
        add("Punjabi folk")
    if "pop" in g or re.search(r"\bpop\b|punjabi-pop|pop albums", e):
        add("Punjabi pop")
    if any(w in g for w in ("hip hop", "hip-hop", "rap")) or "rapper" in fs:
        add("Punjabi hip-hop")
    if "sufi" in g or "sufi" in e:
        add("Sufi")
    if "ghazal" in g or "ghazal" in e:
        add("ghazal")
    if "r&b" in g or "r&b" in e:
        add("R&B")
    if not any(t in ("bhangra", "Punjabi folk", "Punjabi pop", "Punjabi hip-hop", "Punjabi music") for t in tags):
        tags.insert(0, "Punjabi music")
    return tags


def indie_tags(txt: str):
    g, tags = txt.casefold(), []

    def add(t):
        if t not in tags:
            tags.append(t)

    if "indie rock" in g or "indie-rock" in g:
        add("indie rock")
    if "indie pop" in g or "indie-pop" in g:
        add("indie pop")
    if "indie folk" in g or "indie-folk" in g:
        add("indie folk")
    if "alternative rock" in g or "alt-rock" in g:
        add("alternative rock")
    if "post-rock" in g:
        add("post-rock")
    if "folk-metal" in g or "folk metal" in g:
        add("folk metal")
    elif "metal" in g:
        add("metal")
    if "hip hop" in g or "hip-hop" in g or "rapper" in g or "rap " in g:
        add("desi hip-hop")
    if "r&b" in g:
        add("R&B")
    if "punk" in g:
        add("punk")
    if "electronic" in g or "electronica" in g or "synth" in g:
        add("electronic")
    if "singer-songwriter" in g:
        add("singer-songwriter")
    if "rock" in g:
        add("Indian rock")
    if "pop" in g and "indie pop" not in tags and "Indian pop" not in tags:
        add("Indian pop")
    return tags or ["Indian indie"]


PUNJABI_TITLES = [
    "Amar Singh Chamkila", "Amrinder Gill", "Amrita Virk", "Anmol Gagan Maan", "Arif Lohar",
    "Asa Singh Mastana", "Balkar Sidhu", "Balwinder Safri", "Barbie Maan", "Bhinda Jatt",
    "Bups Saggu", "Channi Singh", "Dharampreet", "Didar Sandhu", "Dilbagh Singh (singer)",
    "Dilshad Akhtar", "Durga Rangila", "Foji Gill", "Gur Sidhu", "Gurcharan Pohli",
    "Gurmeet Bawa", "Gurnam Bhullar", "Guri (singer)", "Gurinder Gill", "Hakam Sufi",
    "Hans Raj Hans", "Harbhajan Mann", "Harcharan Garewal", "Jass Manak", "Jassa Dhillon",
    "Jassi Sidhu", "Jaz Dhami", "K. Deep", "K. S. Makhan", "Kamal Heer", "Kamaljit Neeru",
    "Kanth Kaler", "Karnail Gill", "Kuldeep Manak", "Kuljit Bhamra", "Kulwinder Billa",
    "Kulwinder Dhillon", "Labh Janjua", "Lal Chand Yamla Jatt", "Major Rajasthani", "Malkoo",
    "Maninder Buttar", "Manmohan Waris", "Mannat Noor", "Mansoor Malangi", "Master Saleem",
    "Mohinder Kaur Bhamra", "Nachhatar Chhatta", "Narinder Biba", "Naseebo Lal", "Nimrat Khaira",
    "Pammi Bai", "Pathanay Khan", "Prem Dhillon", "Raf-Saperra", "Raj Brar", "Rajvir Jawanda",
    "Resham Singh Anmol", "Romey Gill", "Sabar Koti", "Sardool Sikander", "Satinder Sartaaj",
    "Satwinder Bitti", "Shankar Sahney", "Shinda Kahlon", "Shooter Kahlon", "Singga",
    "Sukha (musician)", "Sukhe", "Sunny Malton", "Surinder Kaur", "Surinder Shinda",
    "Surjit Bindrakhia", "Swaran Lata (singer)", "Talwiinder", "Tarsem Jassar", "Tegi Pannu",
    "Alam Lohar", "Babu Rajab Ali", "Apna Sangeet", "Bhujhangy Group", "Chirag Pehchan",
    "Bombay Talkie (band)", "Delhi 2 Dublin", "The Dhol Foundation", "Jin & Seetal", "Sahotas",
    "Shava (band)", "Tigerstyle", "Alaap (band)", "Tru Skool", "Avtar Singh Kang",
    "Kaka Bhaniawala", "Bombay Rockers", "Amar Arshi", "Afsana Khan", "Alfaaz", "Amrit Maan",
    "Babbal Rai", "Barkat Sidhu", "Jagmohan Kaur", "Jass Bajwa", "Jordan Sandhu", "Mangi Mahal",
    "Navv Inder", "Parmish Verma", "Prakash Kaur", "Ranjit Kaur", "Ravinder Grewal",
    "Akhil (singer)", "Allah Ditta Loonay Wala", "B Praak", "Gurshabad", "Harrdy Sandhu",
    "Harjit Harman", "Imran Khan (singer)", "Inderjit Nikku", "Jasbir Jassi", "Jaspinder Narula",
    "Karamjit Anmol", "Kiran Ahluwalia", "Karnail Singh Paras", "Lakhwinder Wadali",
    "Manni Sandhu", "Mickey Singh", "Nisha Bano", "Sunanda Sharma", "Tarsame Singh Saini",
    "The PropheC", "Tufail Niazi", "Yuvraj Hans",
]

STRONG_PUNJABI = re.compile(
    r"bhangra|Punjabi[ -](folk|music|singer|singers|song|songs|language|film|films|cinema|"
    r"playback|pop|duets)|music of Punjab|Kavishar", re.I)

WIKI_INDIE = [
    "13AD (band)", "Aabha Hanjura", "Aaliyah Qureishi", "Aditi Ramesh", "Agnee (band)",
    "All the Fat Children", "Antaragni (band)", "Antariksh", "Aswekeepsearching", "Atomic Forest",
    "Avora Records", "Bolepur Bluez", "Cactus (Indian band)", "Cassini's Division",
    "Chandrabindoo (band)", "Chandrani Banerjee", "Daira (band)", "Dhunn", "Ditty (musician)",
    "Girish Prabhu", "Girish and the Chronicles", "High (musical group)", "Indian Ocean (band)",
    "Indus Creed", "Insomnia (band)", "Kabir Café", "Kollage (band)", "Lakkhichhara",
    "Masala Coffee", "Moheener Ghoraguli", "Motherjane", "Peter Cat Recording Co.", "Pragaash",
    "Prithibi", "Project Malabaricus", "Pseudonym (band)", "Raghu Dixit", "Rusty Moe",
    "Shaa'ir and Func", "Sifar (band)", "Soulmate (band)", "Swarathma", "Thaikkudam Bridge",
    "The LBG", "The Vinyl Records", "Thermal and a Quarter", "Voodoo Child (band)", "MC Stan",
    "Prabh Deep", "Hanumankind",
]

RNI_INDIE = [
    "Mali", "The Down Troddence", "Bloodywood", "Siroyi", "Sijya", "Midhaven", "Kushagra",
    "Kunwarr", "Sudan", "Frizzell D'Souza", "Street Stories", "Rascals Of The First Order",
    "Serpents of Pakhangba", "Justh", "Bhumi", "Utsavi Jha", "Skrat", "Brodha V", "Frappe Ash",
    "Akshath", "Anirudh Varma Collective", "Sufr", "Arpit Bala", "Pacifist", "Kinari", "Ranj",
    "Yelhomie", "Bhadrankar", "Dhanji", "Vengayo", "Tsumyoki", "Gini", "Abdon Mech",
    "Faheem Abdullah", "KR$NA", "Dasagriva", "Naam Sujal", "Shikriwal", "Mary Ann Alexander",
    "Parvaaz", "Chaar Diwaari", "Lisa Mishra", "Seedhe Maut", "Dreamhour", "Dot.",
    "Kamakshi Khanna", "Aarifah", "Long Distances", "The Lightyears Explode", "Trance Effect",
    "Taba Chake", "Tejas", "Meera", "Bharg", "Sanjeeta Bhattacharya", "Kenneth Soares",
    "Tanmaya Bhatnagar", "Gaya", "Raghav Meattle", "Anoushka Maskey", "Aanchal Bordoloi",
    "The Colour Compound", "Friends from Moon", "Meba Ofilia", "Vaisakh Somanath", "Shikhar",
    "Dhruv Visvanath", "Chirag Todi", "BeBhumika", "The Runway", "Karshni", "Jaden Maskie",
    "Sunflower Tape Machine", "Vasundhara Vee", "Albatross", "Kalika", "Swadesi", "Lifafa",
    "Blackstratblues", "Donn Bhat", "Irfana", "Yungsta", "Gauley Bhai", "Tech Panda x Kenzani",
    "Demonstealer", "Jamna Paar", "Ramil Ganjoo", "Arogya", "Godless", "Second Sight",
]
RNI_SRC = {"Reble": "https://rollingstoneindia.com/the-22-best-indian-independent-singles-of-2022/amp/"}


def main():
    base = json.loads(BASE.read_text(encoding="utf-8"))
    base_norm = {norm(n) for n in base}

    punjabi, indian = [], []
    for title in PUNJABI_TITLES:
        m = meta.get(title)
        if not m or not m["extract"]:
            continue
        ex, gf = m["extract"], clean_genre_field(m["genre_field"])
        if not (gf or STRONG_PUNJABI.search(ex)):
            continue
        ev = f'Wikipedia: "{first_sentence(ex)}"'
        if gf:
            ev += f" Infobox genres: {gf}."
        cats = [c for c in m["categories"] if c in (
            "Bhangra (music) musicians", "Bhangra (music) musical groups",
            "Punjabi singers", "Punjabi-language singers")]
        if cats:
            ev += " Categories: " + "; ".join(cats) + "."
        punjabi.append({"name": display(title), "category": "punjabi",
                        "source_url": wiki_url(title), "evidence": ev,
                        "matched_genres": punjabi_tags(gf, ex)})

    for title in WIKI_INDIE:
        m = meta.get(title)
        if not m or not m["extract"]:
            continue
        gf = clean_genre_field(m["genre_field"])
        ev = f'Wikipedia: "{first_sentence(m["extract"])}"'
        if gf:
            ev += f" Infobox genres: {gf}."
        indian.append({"name": display(title), "category": "indian-indie",
                       "source_url": wiki_url(title), "evidence": ev,
                       "matched_genres": indie_tags(gf + " " + m["extract"][:400])})

    for title in RNI_INDIE:
        rec = rni_record(title, RNI_SRC.get(title))
        if rec:
            rec["matched_genres"] = indie_tags(rec["evidence"])
            indian.append(rec)

    for rec in list(indian):
        if rec["name"] == "Kunwarr":
            indian.remove(rec)
            rec["category"] = "punjabi"
            rec["matched_genres"] = ["Punjabi pop"]
            punjabi.append(rec)

    out, seen = [], set()
    for rec in punjabi + indian:
        k = norm(rec["name"])
        if not k or k in seen or k in base_norm:
            continue
        seen.add(k)
        out.append(rec)

    (ROOT / "extra-punjabi-indie.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", len(out), Counter(r["category"] for r in out))


if __name__ == "__main__":
    main()
