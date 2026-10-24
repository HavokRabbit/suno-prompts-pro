"""Iron Vespers — Prompt Studio.

Data lives in sibling JSON files so the catalogue can grow without touching
Python: artists.json (detail profiles plus sourced genre references),
templates.json, genre_rules.json, catalog_meta.json. CSS lives in
static/style.css. The header animation is static/header.mp4, rendered from the
HyperFrames project in motion/header/.

Two kinds of entry, kept visibly distinct in the UI:
  * profile   — the original hand-written six-field sound description
  * reference — a verified genre association (Wikidata CC0 or a cited source)
                rendered through an original, editable genre template. It is a
                starting point, not a claim about that artist's actual voice.

A defensive sanitizer strips real artist/band names from generated prompt text
so Suno's SENSITIVE_WORD_ERROR filter does not reject the prompt. The search
fields keep their names for lookup; only generated prompt text is cleaned.
"""
import base64
import json
import random
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

import catalog as cat
from genre_profiles import (
    FIELDS,
    GENRES,
    TEMPLATES,
    categories_for,
    identity_key,
    normalize,
    reference_profile,
)

_DATA_DIR = Path(__file__).parent


def _load_json(name):
    with open(_DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


try:
    SINGER_DB = cat.profiles()
    REFERENCE_DB = cat.references()
    CATALOG_META = cat.meta()
    DEFAULT_TEMPLATES = _load_json("templates.json")
    GENRE_RULES = _load_json("genre_rules.json")
    _DATA_LOAD_ERROR = None
except FileNotFoundError as e:
    SINGER_DB, REFERENCE_DB, CATALOG_META = {}, {}, {}
    DEFAULT_TEMPLATES, GENRE_RULES = {}, []
    _DATA_LOAD_ERROR = str(e)


# ====================
#   BRANDING ASSETS
# ====================
def _b64(path):
    try:
        return base64.b64encode((_DATA_DIR / path).read_bytes()).decode()
    except Exception:
        return None


_LOGO_B64 = _b64("static/wolf_logo.svg")
_HEADER_B64 = _b64("static/header.mp4")


def render_header():
    """Slim animated brand banner.

    The clip is a rendered HyperFrames composition. It is muted, decorative and
    marked aria-hidden; when the viewer asks for reduced motion the page parks it
    on its final frame so the banner is still complete, just still.

    The bytes are embedded inline rather than fetched from /app/static. The
    hosted platform puts the whole app behind an auth redirect, so an iframe
    pointed at a static path receives a login page instead of the video and the
    player sits on a spinner forever. Inline bytes cannot 404.
    """
    if not _HEADER_B64:
        st.markdown(
            '<div class="iv-plate"><div class="iv-plate-copy">'
            '<div class="iv-plate-title">Iron Vespers</div>'
            '<div class="iv-plate-sub">Prompt Studio</div></div></div>',
            unsafe_allow_html=True,
        )
        return
    components.html(
        f"""
<style>
  html, body {{ margin:0; padding:0; height:100%; background:transparent; overflow:hidden; }}
  .wrap {{
    height:100%; width:100%;
    display:flex; align-items:center; justify-content:center;
    line-height:0;
  }}
  video {{ display:block; max-width:100%; max-height:100%; width:auto; height:auto; border-radius:10px; }}
</style>
<div class="wrap">
  <video id="ivh" autoplay muted playsinline loop preload="auto"
         aria-hidden="true" tabindex="-1"
         src="data:video/mp4;base64,{_HEADER_B64}"></video>
</div>
<script>
  (function () {{
    var v = document.getElementById("ivh");
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    function apply() {{
      if (reduce.matches) {{
        v.removeAttribute("loop");
        v.pause();
        var park = function () {{ try {{ v.currentTime = 3.4; }} catch (e) {{}} }};
        if (v.readyState >= 1) {{ park(); }} else {{ v.addEventListener("loadedmetadata", park, {{ once: true }}); }}
      }}
    }}
    apply();
    if (reduce.addEventListener) {{ reduce.addEventListener("change", apply); }}
  }})();
</script>
""",
        height=300,
        scrolling=False,
    )


# ====================
#   DEFENSIVE SANITIZER
# ====================
# Names that must never survive into generated prompt text. Single short words
# ("Queen", "Prince", "Tool", "Future") are deliberately absent: stripping them
# would corrupt ordinary prose. The generated profile text is generic anyway -
# this list is the backstop for a name that leaks through a custom field.
_NAME_LEAK_BLACKLIST = [
    "Messiah Marcolin", "Scott Reagers", "Bobby Liebling", "Aaron Stainthorpe",
    "Juha Raivio", "Liz Buckingham", "Jus Oborn", "Patrick Walker",
    "Mike Scheidt", "Jon Davis", "Dorthia Cottrell", "Ryan Clark",
    "Jake Luhrs", "Steve Cobucci", "Josh Scogin", "Adam Gontier",
    "Stephen Keech", "Leroy Hamp", "Mattie Montgomery", "Garrett Russell",
    "Peter Espevoll", "Les Carlsen", "Greg X. Volz", "John Schlitt",
    "Damiano David", "Noah Sebastian", "Mike Kerr", "Adrianne Lenker",
    "Sean McCulloch", "Trey Azagthooth", "David Vincent", "Steve Tucker",
    "Nergal", "Johan Hegg", "Angela Gossow", "Alissa White-Gluz",
    "Derrick Green", "Max Cavalera", "Robb Flynn", "Mikael Åkerfeldt",
    "Nine Inch Nails", "Trent Reznor", "Soundgarden", "Chris Cornell",
    "Queens of the Stone Age", "Arctic Monkeys", "Alice in Chains",
    "Faith No More", "Stone Temple Pilots", "Pearl Jam", "Led Zeppelin",
    "Black Sabbath", "Iron Maiden", "Judas Priest", "Megadeth", "Slayer",
    "System of a Down", "Rage Against the Machine", "Smashing Pumpkins",
    "My Chemical Romance", "Bring Me the Horizon", "Twenty One Pilots",
    "Imagine Dragons", "Maroon 5", "OneRepublic",
    "Billie Eilish", "Taylor Swift", "The Weeknd", "Ariana Grande", "Dua Lipa",
    "Post Malone", "Doja Cat", "Kendrick Lamar", "Travis Scott", "Megan Thee Stallion",
    "Nicki Minaj", "Jerry Cantrell", "Layne Staley", "Kurt Cobain", "Dave Grohl",
    "Michael Jackson", "Quincy Jones", "Snoop Dogg", "Earl Sweatshirt",
]


def _strippable(name):
    """Only names distinctive enough to remove without wrecking prose."""
    return len(name) >= 8 or " " in name


@st.cache_data(show_spinner=False)
def _strip_pattern():
    """One case-insensitive pattern covering the blacklist and the catalogue.

    Catalogue names matter: a profile's own field text can contain the artist's
    name ("Vocal Style: Karan Aujla, ..."), and Suno rejects any prompt carrying
    a real artist name. Longest-first ordering means a full name is removed
    before a shorter name that sits inside it.
    """
    terms = {n for n in _NAME_LEAK_BLACKLIST if _strippable(n)}
    terms |= {n for n in cat.catalog() if _strippable(n)}
    if not terms:
        return None
    ordered = sorted(terms, key=len, reverse=True)
    return re.compile("|".join(re.escape(t) for t in ordered), re.IGNORECASE)


def _sanitize_prompt(text, extra=()):
    """Remove real artist/band names from generated prompt text.

    Case-insensitive, because profile text is written in Title Case while the
    short prompt is lowercased. Returns (cleaned_text, hit_count) so callers can
    tell the user it fired.
    """
    if not text:
        return text, 0
    hits = 0
    for name in sorted({n for n in extra if n and _strippable(n)}, key=len, reverse=True):
        text, count = re.subn(re.escape(name), "[style descriptor]", text, flags=re.IGNORECASE)
        hits += count
    pattern = _strip_pattern()
    if pattern is not None:
        text, count = pattern.subn("[style descriptor]", text)
        hits += count
    return text, hits


# ====================
#   LOOKUP + DETECTION
# ====================
def find_singer(name):
    """Resolve a typed name to (key, entry). Profiles win over references."""
    if not name:
        return None, None
    key = name.strip().lower()
    if key in SINGER_DB:
        return key, SINGER_DB[key]
    if key in REFERENCE_DB:
        return key, REFERENCE_DB[key]
    return cat.find(name)


def detect_genre(name):
    """Data-driven genre detection for a name that is not in the catalogue."""
    n = (name or "").lower().strip()
    for rule in GENRE_RULES:
        if any(k in n for k in rule.get("any", [])) and not any(k in n for k in rule.get("none", [])):
            return rule["genre"]
    return "pop"


def get_random_artist():
    return random.choice(sorted(SINGER_DB.keys(), key=str.casefold))


# ====================
#   PROFILE RESOLUTION
# ====================
def resolve_profile(name):
    """Return (profile_dict, provenance) for a typed name.

    provenance is one of 'profile', 'reference' or 'fallback'. `profile` is
    always a complete six-field dict.
    """
    key, entry = find_singer(name)
    if entry is None:
        template = DEFAULT_TEMPLATES.get(detect_genre(name), DEFAULT_TEMPLATES["pop"])
        return dict(template), "fallback"
    if entry.get("kind") == "profile" or all(f in entry for f in FIELDS):
        return {f: entry[f] for f in FIELDS}, "profile"
    cats = entry.get("categories") or [detect_genre(entry.get("genre", ""))]
    return reference_profile(entry, cats[0]), "reference"


def blend_profiles(primary, secondary):
    """Two-artist blend: keep the primary arc, borrow the second's texture."""
    out = dict(primary)
    out["genre"] = ", ".join(dict.fromkeys(
        [primary.get("genre", "").split(",")[0].strip(), secondary.get("genre", "").split(",")[0].strip()]
    ))
    out["style"] = f"{primary.get('style','')}; {secondary.get('style','')}"
    out["instruments"] = ", ".join(dict.fromkeys(
        [x.strip() for x in f"{primary.get('instruments','')}, {secondary.get('instruments','')}".split(",") if x.strip()]
    ))
    out["vocal_style"] = f"{primary.get('vocal_style','')} / {secondary.get('vocal_style','')}"
    return out


# ====================
#   PROMPT BUILDING
# ====================
def _compose(profile, provenance, label, mood, theme, tempo, extra_note=""):
    mood_value = mood or profile["mood"]
    if provenance == "reference":
        head = "[Genre Reference]"
    elif provenance == "blend":
        head = "[Blend]"
    else:
        head = "[Style Profile]"
    lines = [
        head,
        "",
        f"Genre: {profile['genre']}",
        f"Style: {profile['style']}",
        f"Mood: {mood_value}",
        f"Vocal Style: {profile['vocal_style']}",
        f"Instrumentation: {profile['instruments']}",
        f"Production: {profile['production']}",
    ]
    if tempo:
        lines.append(f"Tempo: {tempo}")
    if theme:
        lines.append(f"Theme: {theme}")
    if extra_note:
        lines += ["", extra_note]
    short = (
        f"{profile['genre'].split(',')[0]} song, "
        f"{profile['style'].split(',')[0].strip().lower()}, "
        f"{mood_value.split(',')[0].strip().lower()} mood, "
        f"{profile['vocal_style'].split(',')[0].strip().lower()} vocals"
    )
    lines += ["", "---", f"[Short Prompt]: {short}"]
    return "\n".join(lines)


def generate_prompt(singer, custom_mood="", custom_theme="", custom_tempo="", sanitize=True):
    """Build a Suno-ready prompt for any catalogue entry or free-typed name."""
    profile, provenance = resolve_profile(singer)
    note = ""
    if provenance == "fallback":
        genre = detect_genre(singer)
        note = (f"Note: artist not in database. The fields below come from the "
                f"{DEFAULT_TEMPLATES.get(genre, DEFAULT_TEMPLATES['pop'])['genre']} template, "
                f"chosen from the words in the name. Add the artist to artists.json for a closer match.")
    elif provenance == "reference":
        entry = find_singer(singer)[1] or {}
        tags = ", ".join((entry.get("matched_genres") or [])[:3])
        note = (f"Source: {entry.get('source', 'sourced genre association')}"
                f"{(' (' + tags + ')') if tags else ''}. "
                "The genre association is verified; the sound description is an original "
                "starting template - edit it to match the record you actually hear.")
    result = _compose(profile, provenance, singer, custom_mood, custom_theme, custom_tempo, note)
    if sanitize:
        result, _ = _sanitize_prompt(result, extra=(singer,))
    return result


def generate_blend(first, second, custom_mood="", custom_theme="", custom_tempo="", sanitize=True):
    a, _a_prov = resolve_profile(first)
    b, _b_prov = resolve_profile(second)
    blended = blend_profiles(a, b)
    note = (f"Blend of {first.strip()} and {second.strip()}. The first sets the arc; "
            "the second supplies texture and instrumentation.")
    result = _compose(blended, "blend", f"{first.strip()} x {second.strip()}",
                      custom_mood, custom_theme, custom_tempo, note)
    if sanitize:
        result, _ = _sanitize_prompt(result, extra=(first, second))
    return result


# ====================
#   UI HELPERS
# ====================
def select_or_custom(label, preset_options, key):
    """Selectbox with a preset list plus a Custom escape hatch."""
    options = list(preset_options) + ["Custom…"]
    choice = st.selectbox(label, options, key=f"{key}_sel")
    if choice == "Custom…":
        return st.text_input(
            f"Custom {label.lower()}", key=f"{key}_txt",
            placeholder=f"Type a custom {label.lower()}",
        ).strip()
    return choice


MOODS = ["", "Melancholic", "Energetic", "Dreamy", "Dark", "Uplifting", "Nostalgic",
         "Intense", "Romantic", "Defiant", "Sacred", "Funereal", "Aggressive",
         "Triumphant", "Bittersweet", "Hopeful", "Hypnotic", "Cold"]
THEMES = ["", "Heartbreak", "Loss", "Love", "Celebration", "Night drive", "Summer",
          "Rain", "Space", "Time", "Faith", "Redemption", "War", "Nature", "Death",
          "Rebirth", "Longing", "Struggle", "The sea", "Iron", "Wolves", "Home"]
TEMPOS = ["", "Slow", "Medium", "Fast", "Upbeat", "Ballad", "Half-time", "Double-time"]

POPULAR = ["taylor swift", "billie eilish", "kendrick lamar", "queen", "frank ocean",
           "daft punk", "sabrina carpenter", "chappell roan", "iron vespers", "candlemass",
           "demon hunter", "bad bunny", "arijit singh", "burna boy", "maneskin", "bts",
           "peso pluma", "karan aujla", "tyla", "sal da vinci"]

RANDOM_MOODS = [m for m in MOODS if m]
RANDOM_THEMES = [t for t in THEMES if t]
RANDOM_TEMPOS = ["Slow", "Medium", "Fast", "Upbeat"]


@st.cache_data(show_spinner=False)
def _catalog_stats():
    counts = cat.counts_by_genre()
    return (
        len(cat.catalog()),
        len(SINGER_DB),
        len(REFERENCE_DB),
        len(counts),
        counts,
    )


def _save_preset(entry):
    presets = st.session_state.setdefault("presets", [])
    presets.insert(0, entry)
    del presets[25:]
    st.session_state.presets = presets


def main():
    st.set_page_config(
        page_title="Iron Vespers — Prompt Studio",
        page_icon="static/favicon.svg" if _LOGO_B64 else "🐺",
        layout="wide",
    )

    if _DATA_LOAD_ERROR:
        st.error(f"Could not load app data: {_DATA_LOAD_ERROR}")
        st.info("artists.json, templates.json and genre_rules.json must sit next to this script.")
        st.stop()

    try:
        with open(_DATA_DIR / "static" / "style.css", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    total, profile_count, reference_count, genre_count, genre_counts = _catalog_stats()
    sanitize_on = st.session_state.get("sanitize_prompts", True)

    # ---------- sidebar ----------
    with st.sidebar:
        if _LOGO_B64:
            st.markdown(
                f'<div class="iv-side"><img src="data:image/svg+xml;base64,{_LOGO_B64}" alt="Iron Vespers wolf"/>'
                '<div class="iv-side-text"><strong>Iron Vespers</strong>'
                '<span>Prompt Studio</span></div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.title("🐺 Iron Vespers")

        st.markdown(
            f'<div class="iv-statgrid">'
            f'<div><b>{total:,}</b><span>artists</span></div>'
            f'<div><b>{genre_count}</b><span>genres</span></div>'
            f'<div><b>{profile_count:,}</b><span>detail profiles</span></div>'
            f'<div><b>{reference_count:,}</b><span>genre references</span></div>'
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.checkbox(
            "Strip artist names from prompts",
            value=sanitize_on,
            key="sanitize_prompts",
            help="Suno rejects prompts that contain real artist names. Keep this on. "
                 "The search boxes still show names; only the generated prompt text is cleaned.",
        )
        st.caption("Prompts are built offline in this app. Nothing is sent anywhere.")

    # ---------- header ----------
    render_header()
    st.markdown(
        f'<div class="iv-meta">Prompt Studio · {total:,} artists · {genre_count} genres · '
        f'{profile_count:,} detailed profiles · {reference_count:,} sourced references</div>',
        unsafe_allow_html=True,
    )

    if "history" not in st.session_state:
        st.session_state.history = []

    # === Google Analytics 4 (visitor counter) ===
    # Preserved from the original app. Reads GA4_MEASUREMENT_ID from Streamlit
    # secrets and falls back to the default HavokRabbit property so the counter
    # keeps working when no secrets file exists.
    try:
        _ga4_id = st.secrets.get("GA4_MEASUREMENT_ID", None) or "G-FPS8T1J4K0"
    except FileNotFoundError:
        _ga4_id = "G-FPS8T1J4K0"
    if _ga4_id:
        components.html(
            f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={_ga4_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{_ga4_id}');
</script>
""",
            height=0,
            width=0,
        )

    tab_studio, tab_artists, tab_saved, tab_about = st.tabs(
        ["Studio", "Artists", "Saved", "About"]
    )

    # ====================  STUDIO  ====================
    with tab_studio:
        st.markdown("### Build a prompt")
        st.caption(
            "Pick an artist, shape the sound, copy the prompt into Suno. "
            "Detailed profiles are hand-written; genre references start from a verified "
            "genre and an original template you can edit."
        )

        left, right = st.columns([3, 2], gap="large")

        with left:
            typed = st.text_input(
                "Artist name",
                placeholder="e.g. candlemass, burna boy, karan aujla",
                key="artist_input",
            )

            if typed and len(typed.strip()) >= 2:
                hits = cat.search_names(typed, limit=12)
                if hits:
                    st.caption("Matches")
                    st.selectbox(
                        "Suggestions", hits, key="artist_suggest", label_visibility="collapsed"
                    )
                elif not cat.find(typed)[1]:
                    st.caption("No catalogue match — a genre template will be used.")

            use_suggestion = st.checkbox(
                "Use the selected suggestion", value=False, key="use_suggestion",
                help="Turn on to build from the suggestion list instead of the free text.",
            )

            chosen = st.session_state.get("artist_suggest") if use_suggestion else typed
            chosen = (chosen or "").strip()
            if chosen:
                entry = find_singer(chosen)[1]
                if entry and entry.get("kind") == "reference":
                    tags = ", ".join((entry.get("matched_genres") or [])[:3])
                    st.info(
                        f"Genre reference · {tags or 'sourced association'}"
                        + (f" · [source]({entry.get('source_url')})" if entry.get("source_url") else "")
                    )
                elif entry:
                    st.info(f"Detailed profile · {entry.get('genre', '')}")

            with st.expander("Blend two artists", expanded=False):
                st.caption("The first artist sets the arc; the second supplies texture and instrumentation.")
                blend_on = st.checkbox("Blend with a second artist", key="blend_on")
                second = ""
                if blend_on:
                    second = st.text_input("Second artist", key="blend_second",
                                           placeholder="e.g. portishead")

            col_mood, col_theme, col_tempo = st.columns(3)
            with col_mood:
                mood = select_or_custom("Mood", MOODS, key="mood")
            with col_theme:
                theme = select_or_custom("Theme", THEMES, key="theme")
            with col_tempo:
                tempo = select_or_custom("Tempo", TEMPOS, key="tempo")

            go = st.button("Generate prompt", type="primary", use_container_width=True)

        with right:
            st.markdown("#### Quick picks")
            st.caption("Popular")
            pop_cols = st.columns(2)
            for i, name in enumerate(POPULAR):
                label = name.title()
                with pop_cols[i % 2]:
                    st.button(label, key=f"pop_{name}", use_container_width=True,
                              on_click=lambda n=name: st.session_state.update(artist_input=n))

            st.caption("Random")
            rnd_col1, rnd_col2 = st.columns(2)
            with rnd_col1:
                st.button("Random artist", use_container_width=True, key="rand_artist",
                          on_click=lambda: st.session_state.update(artist_input=get_random_artist()))
            with rnd_col2:
                if st.button("Random prompt", use_container_width=True, key="rand_prompt"):
                    pick = get_random_artist()
                    mood_pick = random.choice(RANDOM_MOODS)
                    theme_pick = random.choice(RANDOM_THEMES)
                    tempo_pick = random.choice(RANDOM_TEMPOS)
                    generated = generate_prompt(pick, mood_pick, theme_pick, tempo_pick,
                                                sanitize=sanitize_on)
                    st.session_state.last_result = generated
                    st.session_state.last_label = pick
                    st.session_state.flash = (f"Random prompt: {pick.title()} — "
                                              f"{mood_pick}, {theme_pick}, {tempo_pick}")
                    st.session_state.history.insert(0, {
                        "artist": pick, "mood": mood_pick, "theme": theme_pick,
                        "tempo": tempo_pick, "prompt": generated,
                    })
                    st.session_state.history = st.session_state.history[:20]

        if go:
            target = chosen
            if not target:
                st.warning("Enter an artist name, or use a quick pick.")
            else:
                if st.session_state.get("blend_on") and (second or "").strip():
                    result = generate_blend(target, second.strip(), mood, theme, tempo, sanitize=sanitize_on)
                    label = f"{target} × {second.strip()}"
                else:
                    result = generate_prompt(target, mood, theme, tempo, sanitize=sanitize_on)
                    label = target
                st.session_state.last_result = result
                st.session_state.last_label = label
                st.session_state.flash = None
                st.session_state.history.insert(0, {
                    "artist": label, "mood": mood, "theme": theme,
                    "tempo": tempo, "prompt": result,
                })
                st.session_state.history = st.session_state.history[:20]

        if st.session_state.get("last_result"):
            st.markdown("---")
            st.markdown("#### Result")
            if st.session_state.get("flash"):
                st.success(st.session_state.flash)
            st.code(st.session_state.last_result, language=None)
            dl_col, save_col = st.columns(2)
            slug_source = st.session_state.get("last_label") or chosen or "prompt"
            name_slug = re.sub(r"[^\w]+", "_", slug_source).strip("_")[:60] or "prompt"
            with dl_col:
                st.download_button("Download .txt", st.session_state.last_result,
                                   file_name=f"{name_slug}_prompt.txt", use_container_width=True)
            with save_col:
                if st.button("Save to presets", use_container_width=True, key="save_preset"):
                    _save_preset({
                        "artist": chosen or "prompt", "mood": mood, "theme": theme,
                        "tempo": tempo, "prompt": st.session_state.last_result,
                    })
                    st.success("Saved for this browser session. Export on the Saved tab to keep it.")

        if st.session_state.history:
            with st.expander(f"Recent prompts ({len(st.session_state.history)})"):
                for i, item in enumerate(st.session_state.history):
                    meta = " · ".join(x for x in [item["mood"], item["theme"], item["tempo"]] if x)
                    st.caption(item["artist"].title() + (f" — {meta}" if meta else ""))
                    st.code(item["prompt"], language=None)
                    st.download_button("Download .txt", item["prompt"],
                                       file_name=f"prompt_{i}.txt", key=f"hist_dl_{i}")
                    st.markdown("---")

    # ====================  ARTISTS  ====================
    with tab_artists:
        st.markdown("### Artist catalogue")
        shelved = {}
        for key in cat.categories():
            shelved.setdefault(cat.genre_shelf(key), []).append(key)
        counts = cat.counts_by_genre()
        all_count = len(cat.catalog())
        active_genre = st.session_state.get("genre_filter", "All")

        st.markdown("#### Browse by genre")
        st.caption("Pick a genre to filter the list. Every count is the real number of entries.")
        chips = [("All", "All genres", all_count)] + [
            (key, cat.genre_label(key), counts[key]) for key in cat.categories()
        ]
        chip_cols = st.columns(4)
        for i, (key, label, n) in enumerate(chips):
            with chip_cols[i % 4]:
                st.button(
                    f"{label} ({n:,})",
                    key=f"genre_chip_{key}",
                    use_container_width=True,
                    type="primary" if key == active_genre else "secondary",
                    on_click=lambda k=key: st.session_state.update(genre_filter=k),
                )

        st.markdown("---")
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            query = st.text_input("Search", key="cat_query", placeholder="name, genre or description")
        with f2:
            shelf = st.selectbox("Shelf", ["All"] + sorted(s for s in shelved if s != "Other"),
                                 key="cat_shelf")
        with f3:
            kind = st.selectbox("Kind", ["All", "Detailed profile", "Genre reference"], key="cat_kind")

        if active_genre != "All":
            st.caption(f"Filtered to **{cat.genre_label(active_genre)}** — "
                       f"{counts.get(active_genre, 0):,} artists")

        kind_key = {"All": None, "Detailed profile": "profile", "Genre reference": "reference"}[kind]
        rows = cat.entries(category=active_genre, shelf=None if shelf == "All" else shelf,
                           kind=kind_key, query=query)

        page_size = 25
        pages = max(1, (len(rows) + page_size - 1) // page_size)
        # Reset to page 1 when the filter set changes, and keep the stored page
        # inside the valid range. Both writes happen BEFORE the widget exists:
        # assigning a widget's key after it is built raises StreamlitAPIException,
        # and passing value= alongside an occupied key is a silent conflict.
        filter_signature = (query, shelf, active_genre, kind)
        if st.session_state.get("cat_filter_sig") != filter_signature:
            st.session_state["cat_filter_sig"] = filter_signature
            st.session_state["cat_page"] = 1
        st.session_state["cat_page"] = min(
            max(1, int(st.session_state.get("cat_page", 1))), pages
        )
        page = st.number_input(f"{len(rows):,} matches — page", min_value=1, max_value=pages,
                               key="cat_page", step=1)

        start = (int(page) - 1) * page_size
        for name, entry in rows[start:start + page_size]:
            is_profile = entry.get("kind") == "profile"
            badge = "Profile" if is_profile else "Reference"
            genres = entry.get("genre") if is_profile else ", ".join((entry.get("matched_genres") or [])[:3])
            with st.container():
                head_col, btn_col = st.columns([5, 1])
                with head_col:
                    st.markdown(
                        f'<div class="iv-row"><div class="iv-row-head">'
                        f'<span class="iv-name">{name.title()}</span>'
                        f'<span class="iv-badge {"iv-badge-profile" if is_profile else "iv-badge-ref"}">{badge}</span>'
                        f'</div><div class="iv-row-sub">{genres or "sourced association"}</div>'
                        + (f'<div class="iv-row-desc">{entry.get("description","")}</div>'
                           if entry.get("description") else "")
                        + (f'<div class="iv-row-src"><a href="{entry.get("source_url")}" '
                           f'target="_blank" rel="noopener">source</a></div>'
                           if entry.get("source_url") else "")
                        + "</div>",
                        unsafe_allow_html=True,
                    )
                with btn_col:
                    st.button("Use", key=f"use_{name}", use_container_width=True,
                              on_click=lambda n=name: st.session_state.update(artist_input=n))
                st.markdown('<div class="iv-rule"></div>', unsafe_allow_html=True)

    # ====================  SAVED  ====================
    with tab_saved:
        st.markdown("### Saved presets")
        st.caption(
            "Presets live in this browser session. Export them to a file to keep them — "
            "that file is the durable copy."
        )
        presets = st.session_state.get("presets", [])
        if presets:
            st.download_button(
                "Export presets (.json)", json.dumps(presets, indent=2, ensure_ascii=False),
                file_name="iron_vespers_presets.json", mime="application/json",
            )
            for i, item in enumerate(presets):
                st.markdown(f"**{item['artist'].title()}**")
                st.code(item["prompt"], language=None)
                st.download_button("Download .txt", item["prompt"], file_name=f"preset_{i}.txt",
                                   key=f"preset_dl_{i}")
            if st.button("Clear session presets"):
                st.session_state.presets = []
                st.rerun()
        else:
            st.info("Nothing saved yet. Generate a prompt and choose “Save to presets”.")

        st.markdown("---")
        uploaded = st.file_uploader("Import presets (.json)", type=["json"])
        if uploaded is not None:
            try:
                loaded = json.loads(uploaded.read().decode("utf-8"))
                if isinstance(loaded, list) and all("prompt" in x for x in loaded):
                    st.session_state.presets = loaded[:25]
                    st.success(f"Imported {len(loaded[:25])} presets for this session.")
                else:
                    st.error("That file is not a preset export.")
            except json.JSONDecodeError:
                st.error("That file is not valid JSON.")

    # ====================  ABOUT  ====================
    with tab_about:
        st.markdown("### How this catalogue works")
        st.markdown(f"""
**Two kinds of entry, deliberately kept apart.**

- **Detailed profile** ({profile_count:,} entries) — the hand-written six-field sound
  description that this tool has always used. Specific and opinionated.
- **Genre reference** ({reference_count:,} entries) — a real artist with a *verified*
  genre association, rendered through an original, editable genre template. The genre fact
  is sourced; the sound description is a starting point, not a claim about that artist's
  actual voice. Wikisourced entries link to their record.

Nothing here is scraped from reviews or biographies, and no entry invents an
artist-specific vocal analysis.

**Genres** ({genre_count}) are navigation shelves, not boxes. One artist can sit in
several — an act documented in both doom and sludge appears under both.
""")
        st.markdown("#### Sources and licensing")
        st.markdown("""
- **Wikidata** — structured artist and genre statements, released **CC0**.
  Reference entries carry their `wikidata.org` link.
- **Researched entries** — each carries an explicit `source_url` and the evidence used.
- **Original catalogue** — the profiles that shipped with this app.
- **Genre templates** — original writing, editable in `genre_profiles.py`.
""")
        if CATALOG_META.get("genre_counts"):
            st.markdown("#### Counts by genre")
            pairs = sorted(CATALOG_META["genre_counts"].items(), key=lambda kv: -kv[1])
            st.markdown(
                '<div class="iv-counts">'
                + "".join(
                    f'<div><span>{cat.genre_label(k)}</span><b>{v:,}</b></div>' for k, v in pairs
                )
                + "</div>",
                unsafe_allow_html=True,
            )

        st.markdown("#### Limits worth knowing")
        st.markdown("""
- A genre association is not a sound. Two death metal records can share nothing.
  Use the template as a floor, then edit the fields to match what you actually hear.
- Coverage is uneven because documented data is uneven. Popular scenes are deep;
  niche ones are thin, and the app reports the real count rather than padding it.
- Presets and history are session-only. The export file is the durable copy.
""")

        st.markdown("#### Add your own")
        st.markdown("Add a detail profile to **`artists.json`**:")
        st.code("""{
  "new artist": {
    "kind": "profile",
    "genre": "Your Genre, Sub-genre",
    "mood": "...",
    "style": "...",
    "vocal_style": "...",
    "instruments": "...",
    "production": "..."
  }
}""", language="json")
        st.markdown(
            "For a new genre, add a template in **`templates.json`** and a detection rule in "
            "**`genre_rules.json`**. Template keys live in `genre_profiles.py`."
        )
        st.markdown("---")
        st.markdown("[Source repository](https://github.com/HavokRabbit/suno-prompts-pro)")


if __name__ == "__main__":
    main()
