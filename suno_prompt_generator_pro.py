"""Iron Vespers — Suno Prompt Generator Pro.

Data lives in sibling JSON files (artists.json, templates.json, genre_rules.json)
so the artist database and genre logic can be edited without touching Python.
CSS lives in static/style.css.

A defensive sanitizer (_sanitize_prompt) strips real artist/band names from
generated prompts so Suno's SENSITIVE_WORD_ERROR filter doesn't reject them.
Originally added by the Streamlit sweep 2026-07-03; preserved here.
"""
import streamlit as st
import streamlit.components.v1 as components
import random
import base64
import json
from pathlib import Path

# ====================
#   DATA LOADING
# ====================
_DATA_DIR = Path(__file__).parent


def _load_json(name):
    """Load a JSON data file shipped alongside this script. Raises FileNotFoundError
    if missing — handled by the Streamlit error UI in main()."""
    with open(_DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


try:
    SINGER_DB = _load_json("artists.json")
    DEFAULT_TEMPLATES = _load_json("templates.json")
    GENRE_RULES = _load_json("genre_rules.json")
    _DATA_LOAD_ERROR = None
except FileNotFoundError as e:
    SINGER_DB, DEFAULT_TEMPLATES, GENRE_RULES = {}, {}, []
    _DATA_LOAD_ERROR = str(e)


# ====================
#   IRON VESPERS BRANDING
# ====================
def _load_logo_b64():
    try:
        with open(_DATA_DIR / "static" / "wolf_logo.svg", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


_LOGO_B64 = _load_logo_b64()


# ====================
#   CALLBACKS (defined before any st.button(on_click=...) that uses them)
# ====================
def cb_random_artist():
    """Sidebar 🎲 Random Artist → fill Generate tab's artist field."""
    new = get_random_artist()
    st.session_state.artist_input = new
    st.session_state.random_artist = new
    st.session_state.pop('selected_artist', None)


def cb_clear_artist():
    """Generate tab 🧹 Clear Artist Field → empty the artist field."""
    st.session_state.artist_input = ""
    st.session_state.pop('selected_artist', None)
    st.session_state.pop('random_artist', None)


def cb_select_artist(name):
    """Generate tab ⭐ Popular button → fill artist field."""
    st.session_state.artist_input = name
    st.session_state.selected_artist = name
    st.session_state.pop('random_artist', None)


def cb_use_artist(name):
    """Artists tab 'Use {Name}' button → fill Generate tab's field, jump to Generate."""
    st.session_state.artist_input = name
    st.session_state.selected_artist = name
    st.session_state.active_tab_label = "✨ Generate"


def cb_select_genre(term):
    """Generate tab 🎸 By Genre button → pre-fill Artists tab search, switch to Artists tab."""
    # Use a non-widget-bound key (genre_filter) so we don't trip the widget-key write block.
    # The Artists tab text_input reads from this via its `value=` argument.
    st.session_state.genre_filter = term
    st.session_state.active_tab_label = "📚 Artists"


# ====================
#   DEFENSIVE SANITIZER (added by Streamlit sweep 2026-07-03)
#   Strips real artist/band names from generated prompt text so Suno's
#   SENSITIVE_WORD_ERROR filter doesn't reject the prompt. SINGER_DB keys
#   (the search tabs) keep their names for lookup; the generated prompt
#   text must be clean. Single-name terms ("Alice", "Iron") are excluded
#   to avoid false-positive stripping of common English words.
# ====================
_NAME_LEAK_BLACKLIST = [
    # Vocalists (first + last combos)
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
    # Bands (full name only)
    "Nine Inch Nails", "Trent Reznor", "Soundgarden", "Chris Cornell",
    "Queens of the Stone Age", "Arctic Monkeys", "Alice in Chains",
    "Faith No More", "Stone Temple Pilots", "Pearl Jam", "Led Zeppelin",
    "Black Sabbath", "Iron Maiden", "Judas Priest", "Megadeth", "Slayer",
    "Tool", "System of a Down", "Deftones", "Rage Against the Machine",
    "Smashing Pumpkins", "Radiohead", "Muse", "Foo Fighters", "Nirvana",
    "My Chemical Romance", "Bring Me the Horizon", "Twenty One Pilots",
    "Imagine Dragons", "Coldplay", "Maroon 5", "OneRepublic", "Hozier",
    "Billie Eilish", "Taylor Swift", "Drake", "The Weeknd", "BTS", "BLACKPINK",
    "Ariana Grande", "Dua Lipa", "Post Malone", "Doja Cat", "SZA",
    "Kendrick Lamar", "J. Cole", "Future", "Travis Scott", "Lil Baby",
    "Cardi B", "Megan Thee Stallion", "Nicki Minaj",
    "Jerry Cantrell", "Layne Staley", "Kurt Cobain", "Dave Grohl",
    "Tupac", "Notorious", "Biggie", "Snoop", "Eminem",
    "Michael Jackson", "Quincy Jones", "Prince", "Rihanna", "Snoop Dogg",
    "Earl Sweatshirt", "Flume",
]


def _sanitize_prompt(text):
    """Strip any blacklisted artist/band name from generated prompt text.
    Returns (cleaned_text, hit_count) so callers can log when it fires."""
    if not text:
        return text, 0
    hits = 0
    for name in _NAME_LEAK_BLACKLIST:
        if name in text:
            text = text.replace(name, "[REDACTED]")
            hits += 1
    return text, hits


# ====================
#   FUNCTIONS
# ====================
def find_singer(name):
    return SINGER_DB.get(name.lower().strip())


def detect_genre(name):
    """Data-driven genre detection. Iterates GENRE_RULES in order; first rule whose
    `any` keywords all-substring-match (and whose `none` keywords don't) wins.
    Falls back to 'pop'."""
    n = name.lower().strip()
    for rule in GENRE_RULES:
        if any(k in n for k in rule.get("any", [])) and not any(k in n for k in rule.get("none", [])):
            return rule["genre"]
    return "pop"


def generate_prompt(singer, custom_mood="", custom_theme="", custom_tempo="", sanitize=True):
    """Build a Suno prompt for `singer`. If `sanitize` is True (default), run the
    output through _sanitize_prompt to strip real artist/band names so Suno's
    SENSITIVE_WORD_ERROR filter doesn't reject it. The UI gates `sanitize` via
    a sidebar checkbox; tests call with the default."""
    data = find_singer(singer)
    if data:
        mood = custom_mood or data["mood"]
        tempo = f"Tempo: {custom_tempo}" if custom_tempo else ""
        # Note: Suno flags artist names. We reference the artist only as "[Style Profile]"
        # and describe the sound via genre / style / mood / vocal_style.
        result = f"""[Style Profile]

Genre: {data['genre']}
Style: {data['style']}
Mood: {mood}
Vocal Style: {data['vocal_style']}
Instrumentation: {data['instruments']}
Production: {data['production']}
{tempo}
{f'Theme: {custom_theme}' if custom_theme else ''}

---
[Short Prompt]: {data['genre'].split(',')[0]} song, {data['style'].split(',')[0].lower()}, {mood.split(',')[0].lower()} mood, {data['vocal_style'].split(',')[0].lower()} vocals"""
    else:
        g = detect_genre(singer)
        t = DEFAULT_TEMPLATES.get(g, DEFAULT_TEMPLATES["pop"])
        mood = custom_mood or t["mood"]
        tempo = f"Tempo: {custom_tempo}" if custom_tempo else ""
        result = f"""[Style Profile - {t['genre']}]

Genre: {t['genre']}
Style: {t['style']}
Mood: {mood}
Vocal Style: {t['vocal_style']}
Instrumentation: {t['instruments']}
Production: {t['production']}
{tempo}
{f'Theme: {custom_theme}' if custom_theme else ''}

---
[Short Prompt]: {t['genre']} song, {t['style'].split(',')[0].lower()}, {mood.split(',')[0].lower()} mood, {t['vocal_style'].split(',')[0].lower()} vocals

Note: Artist not in database. Using {t['genre']} defaults. Add them to artists.json for better results."""

    if sanitize:
        result, _ = _sanitize_prompt(result)
    return result


def get_random_artist():
    return random.choice(list(SINGER_DB.keys()))


# ====================
#   UI HELPERS
# ====================
def select_or_custom(label, preset_options, key):
    """Selectbox with preset options + a 'Custom…' escape hatch that reveals a text
    input. Returns the chosen value (empty string if nothing chosen)."""
    options = list(preset_options) + ["Custom…"]
    choice = st.selectbox(label, options, key=f"{key}_sel")
    if choice == "Custom…":
        custom = st.text_input(
            f"✍️ Custom {label.lower()}",
            key=f"{key}_txt",
            placeholder=f"Type a custom {label.lower()}",
        )
        return custom.strip()
    return choice


# ====================
#   MAIN
# ====================
def main():
    st.set_page_config(
        page_title="Iron Vespers — Suno Prompt Generator Pro",
        page_icon="static/favicon.svg" if _LOGO_B64 else "🐺",
        layout="wide"
    )

    if _DATA_LOAD_ERROR:
        st.error(f"Could not load app data: {_DATA_LOAD_ERROR}")
        st.info("Make sure artists.json, templates.json, and genre_rules.json are next to this script.")
        st.stop()

    # ====================
    #   GLOBAL CSS — IRON VESPERS GOTHIC THEME
    # ====================
    try:
        with open(_DATA_DIR / "static" / "style.css", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # fall back to default Streamlit styling

    _sanitize_on = st.session_state.get("sanitize_prompts", True)

    # ====================
    #   SIDEBAR
    # ====================
    with st.sidebar:
        if _LOGO_B64:
            st.markdown(f"""
            <div class="iv-hero" style="padding: 12px 0 16px 0; margin-bottom: 12px;">
                <img src="data:image/svg+xml;base64,{_LOGO_B64}" alt="Iron Vespers Wolf"/>
                <div class="iv-hero-text">
                    <h1 style="font-size: 1.4em; margin: 0;">Iron Vespers</h1>
                    <div class="iv-tag" style="font-size: 0.78em; line-height: 1.35;">Suno Prompt Generator Pro · {len(SINGER_DB)} artists · {len(DEFAULT_TEMPLATES)} genre templates</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.title("🐺 Iron Vespers")
            st.markdown(f"**Suno Prompt Generator Pro · {len(SINGER_DB)} artists · {len(DEFAULT_TEMPLATES)} genre templates**")
        st.markdown("---")
        st.markdown(f"**Artists:** {len(SINGER_DB)}")
        st.markdown(f"**Genres:** {len(DEFAULT_TEMPLATES)}")
        st.markdown("---")

        if st.button("🎲 Random Artist", on_click=cb_random_artist):
            pass

        st.markdown("---")
        st.markdown("**Quick Links**")
        st.markdown("[Suno AI](https://suno.com)")
        st.markdown("[Iron Vespers](https://github.com/HavokRabbit/Suno-prompts-pro)")

        # Defensive sanitizer toggle (preserved from Streamlit sweep 2026-07-03)
        st.markdown("---")
        st.subheader("Suno Filter Safety")
        st.session_state.sanitize_prompts = st.checkbox(
            "Strip artist/band names from generated prompts",
            value=_sanitize_on,
            help="Defensive sanitizer that removes known artist/band names from "
                 "the generated prompt. Keep this ON unless you need to debug a "
                 "specific prompt — Suno will reject prompts containing real artist names."
        )

    # Re-read after the checkbox so generate calls in this run use the latest value
    _sanitize_on = st.session_state.get("sanitize_prompts", True)

    # Main hero header (rendered ABOVE the tabs so tab bodies are clean)
    if _LOGO_B64:
        st.markdown(f"""
        <div class="iv-hero">
            <img src="data:image/svg+xml;base64,{_LOGO_B64}" alt="Iron Vespers Wolf"/>
            <div class="iv-hero-text">
                <h1>Iron Vespers</h1>
                <div class="iv-tag">Suno Prompt Generator Pro · {len(SINGER_DB)} artists · {len(DEFAULT_TEMPLATES)} genre templates</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title("🐺 Iron Vespers — Suno Prompt Pro")

    # ====================
    #   TABS (key= enables programmatic tab switching via st.session_state)
    # ====================
    _pending = st.session_state.pop("active_tab_label", None)
    if _pending is not None:
        st.session_state.main_tabs = _pending
    elif "main_tabs" not in st.session_state:
        st.session_state.main_tabs = "✨ Generate"

    # === Google Analytics 4 (visitor counter) ===
    # Reads the measurement ID from Streamlit secrets: GA4_MEASUREMENT_ID
    # Falls back to the default HavokRabbit property ID if unset or no secrets file.
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

    tab1, tab2, tab3, tab4 = st.tabs(
        ["✨ Generate", "🎲 Random", "📚 Artists", "⚙️ Settings"],
        key="main_tabs",
        on_change="rerun",
        default=st.session_state.main_tabs,
    )

    # Init prompt history
    if "history" not in st.session_state:
        st.session_state.history = []

    # ====================
    #   TAB 1 — GENERATE
    # ====================
    with tab1:
        st.markdown("### ⚔️ Generate Prompt")
        st.caption("Type an artist name, or use the buttons below. The app will fuse the artist's sound with the matching genre template. Use the 📋 icon on the code block to copy, or download as .txt.")

        col1, col2 = st.columns([2, 1])

        with col1:
            default_val = st.session_state.get('selected_artist', '') or st.session_state.get('random_artist', '')

            singer = st.text_input(
                "Artist Name",
                value=default_val,
                placeholder="e.g., taylor swift, queen, kendrick lamar, chris tomlin",
                key="artist_input"
            )

            if default_val and singer == default_val:
                st.caption(f"Pre-selected: {default_val.title()}")

            # Mood / Theme / Tempo — each with a "Custom…" escape hatch for free-text
            col_mood, col_theme, col_tempo = st.columns(3)
            with col_mood:
                custom_mood = select_or_custom(
                    "Mood",
                    ["", "Melancholic", "Energetic", "Dreamy", "Dark", "Uplifting",
                     "Nostalgic", "Intense", "Romantic", "Defiant", "Sacred",
                     "Funereal", "Aggressive", "Triumphant", "Bittersweet", "Hopeful"],
                    key="mood",
                )
            with col_theme:
                custom_theme = select_or_custom(
                    "Theme",
                    ["", "Heartbreak", "Loss", "Love", "Celebration", "Night drive",
                     "Summer", "Rain", "Space", "Time", "Faith", "Redemption",
                     "War", "Nature", "Death", "Rebirth", "Longing", "Struggle"],
                    key="theme",
                )
            with col_tempo:
                custom_tempo = select_or_custom(
                    "Tempo",
                    ["", "Slow", "Medium", "Fast", "Upbeat", "Ballad"],
                    key="tempo",
                )

            if st.button("🎵 Generate Prompt", type="primary", use_container_width=True):
                if singer.strip():
                    result = generate_prompt(singer, custom_mood, custom_theme, custom_tempo, sanitize=_sanitize_on)
                    st.session_state.history.insert(0, {
                        "artist": singer.strip(),
                        "mood": custom_mood,
                        "theme": custom_theme,
                        "tempo": custom_tempo,
                        "prompt": result,
                    })
                    st.session_state.history = st.session_state.history[:20]
                    st.code(result, language=None)
                    st.download_button(
                        "⬇️ Download .txt",
                        result,
                        file_name=f"{singer.replace(' ', '_')}_prompt.txt",
                        use_container_width=True
                    )
                else:
                    st.warning("Enter an artist name!")

            if st.button("🧹 Clear Artist Field", on_click=cb_clear_artist):
                pass

            # Prompt history
            if st.session_state.history:
                with st.expander(f"🕘 Recent Prompts ({len(st.session_state.history)})"):
                    for i, h in enumerate(st.session_state.history):
                        meta = " · ".join(x for x in [h["mood"], h["theme"], h["tempo"]] if x)
                        st.caption(f"{h['artist'].title()}" + (f" — {meta}" if meta else ""))
                        st.code(h["prompt"], language=None)
                        st.download_button(
                            "⬇️ Download .txt",
                            h["prompt"],
                            file_name=f"{h['artist'].replace(' ', '_')}_prompt.txt",
                            key=f"hist_dl_{i}",
                        )
                        st.markdown("---")

        with col2:
            st.subheader("⭐ Popular")
            popular = ["taylor swift", "billie eilish", "kendrick lamar", "queen", "frank ocean", "daft punk", "sabrina carpenter", "chappell roan", "iron vespers", "candlemass", "demon hunter", "bad bunny", "arijit singh", "burna boy", "maneskin", "bts", "peso pluma", "karan aujla", "tyla", "sal da vinci"]

            for artist in popular:
                st.button(
                    artist.title(),
                    key=f"pop_{artist}",
                    use_container_width=True,
                    on_click=cb_select_artist,
                    args=(artist,),
                )

            st.markdown("---")
            st.subheader("🎸 By Genre")
            genres = {
                "Pop": "pop",
                "Rock": "rock",
                "Hip-Hop": "hip",
                "R&B": "r&b",
                "Electronic": "electronic",
                "Metal": "metal",
                "Doom": "doom",
                "Indie": "indie",
                "Folk": "folk",
                "Bedroom": "bedroom",
                "Country": "country",
                "Latin": "latin",
                "Corrido": "corrido",
                "Reggaeton": "reggaeton",
                "K-Pop": "k-pop",
                "Bollywood": "bollywood",
                "Punjabi": "punjabi",
                "Indian Indie": "indian",
                "Italian": "italian",
                "Afrobeats": "afrobeats",
                "Hyperpop": "hyperpop",
                "Modern Heavy": "modern",
                "CCM": "worship",
                "Christian Metal": "christian metal",
            }
            # 3-column grid instead of one long vertical stack
            gcols = st.columns(3)
            for i, (label, term) in enumerate(genres.items()):
                with gcols[i % 3]:
                    st.button(
                        label,
                        key=f"gen_{label}",
                        use_container_width=True,
                        on_click=cb_select_genre,
                        args=(term,),
                    )

    # ====================
    #   TAB 2 — RANDOM
    # ====================
    with tab2:
        st.title("🎲 Random Generator")
        st.markdown("Let fate decide your next track!")

        if st.button("🎰 Generate Random Prompt", type="primary", use_container_width=True):
            artist = get_random_artist()
            moods = ["melancholic", "energetic", "dreamy", "dark", "uplifting", "nostalgic", "intense"]
            themes = ["love", "loss", "celebration", "night drive", "summer", "rain", "space", "time"]

            random_mood = random.choice(moods)
            random_theme = random.choice(themes)
            random_tempo = random.choice(["Slow", "Medium", "Fast", "Upbeat"])

            result = generate_prompt(artist, random_mood, random_theme, random_tempo, sanitize=_sanitize_on)

            st.session_state.history.insert(0, {
                "artist": artist,
                "mood": random_mood,
                "theme": random_theme,
                "tempo": random_tempo,
                "prompt": result,
            })
            st.session_state.history = st.session_state.history[:20]

            st.success(f"Generated: **{artist.title()}** style")
            st.code(result, language=None)
            st.download_button(
                "⬇️ Download .txt",
                result,
                file_name=f"random_{artist.replace(' ', '_')}_prompt.txt"
            )

    # ====================
    #   TAB 3 — ARTISTS
    # ====================
    with tab3:
        st.title("Artist Database")

        pending = st.session_state.pop('genre_filter', '')
        if pending:
            st.success(f"🎸 Genre filter active: showing matches for '{pending}'. Clear the search box to see all artists.")

        search = st.text_input(
            "🔍 Search artists",
            value=pending,
            placeholder="e.g., chris tomlin, lauren daigle, elevation, mitski",
            key="artist_search_input"
        )

        search_term = (search or "").strip().lower()

        genres_dict = {}
        for name, data in SINGER_DB.items():
            g = data['genre'].split(',')[0].strip()
            genres_dict.setdefault(g, []).append((name, data))

        found_any = False
        for genre, artists in sorted(genres_dict.items()):
            matches = [
                (n, d) for n, d in artists
                if not search_term
                or search_term in n.lower()
                or search_term in d['genre'].lower()
            ]
            if matches:
                found_any = True
                with st.expander(f"{genre} ({len(matches)} found)"):
                    for name, data in matches:
                        st.markdown(f"**{name.title()}**")
                        st.caption(f"{data['mood']} • {data['genre']}")
                        st.button(
                            f"Use {name.title()}",
                            key=f"use_artist_{name}",
                            on_click=cb_use_artist,
                            args=(name,),
                        )
                        st.markdown("---")

        if search_term:
            if not found_any:
                st.warning(f"No matches for '{search}' — try partial name or different spelling")
        else:
            st.info("Type to filter artists (e.g. chris, lauren, worship...)")

    # ====================
    #   TAB 4 — SETTINGS
    # ====================
    with tab4:
        st.title("⚙️ Settings & Info")

        st.subheader("About")
        st.markdown(f"""
        **Suno Prompt Generator Pro** helps you create detailed prompts for Suno AI music generation.

        **Features:**
        - {len(SINGER_DB)} curated artists (edit `artists.json`)
        - {len(DEFAULT_TEMPLATES)} genre templates (edit `templates.json`)
        - Data-driven genre detection (edit `genre_rules.json`)
        - Defensive sanitizer strips real artist/band names (toggle in sidebar)
        - Genre fallback for unknown artists
        - Custom mood / theme / tempo (type your own via "Custom…")
        - Random generator
        - Persistent selection from Artists tab
        - Prompt history (last 20)
        - Export as .txt
        """)

        st.subheader("How to Use")
        st.markdown("""
        1. Pick artist from Popular, Artists tab or type name
        2. Optional: add mood / theme / tempo (pick a preset or choose "Custom…" to type your own)
        3. Click Generate
        4. Copy via the 📋 icon on the code block, or download as .txt
        5. Paste into Suno → create!

        Keep the sidebar "Strip artist/band names" toggle ON — Suno rejects prompts containing real artist names.
        """)

        st.subheader("Add Custom Artists")
        st.markdown("Edit **`artists.json`** (next to this script). Add an entry like:")
        st.code("""{
    "new artist": {
        "genre": "Your Genre, Sub-genre",
        "mood": "...",
        "style": "...",
        "vocal_style": "...",
        "instruments": "...",
        "production": "..."
    }
}""", language="json")
        st.markdown("Add a matching genre template in **`templates.json`** and, if the genre needs keyword-based detection for unknown artists, add a rule to **`genre_rules.json`**. If you add a well-known artist whose name might leak into field values, also add it to `_NAME_LEAK_BLACKLIST` in the script.")

        st.subheader("Project")
        st.markdown("[Source repo](https://github.com/HavokRabbit/Suno-prompts-pro)")


if __name__ == "__main__":
    main()