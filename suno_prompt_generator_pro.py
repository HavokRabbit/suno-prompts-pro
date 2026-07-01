import streamlit as st
import random
import base64

# ====================
#   IRON VESPERS BRANDING
# ====================
def _load_logo_b64():
    try:
        with open("static/wolf_logo.svg", "rb") as f:
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

st.set_page_config(
    page_title="Iron Vespers — Suno Prompt Generator Pro",
    page_icon="static/favicon.svg" if _LOGO_B64 else "🐺",
    layout="wide"
)

# ====================
#   GLOBAL CSS — IRON VESPERS GOTHIC THEME
# ====================
st.markdown("""
<style>
/* Brand color variables */
:root {
    --iv-red: #C8102E;
    --iv-red-hot: #FF1F44;
    --iv-red-soft: #FF7A8A;
    --iv-purple: #9D00FF;
    --iv-bg: #0E1117;
    --iv-bg-card: #1a0a14;
    --iv-bg-elev: #1E1E1E;
    --iv-text: #FAFAFA;
    --iv-text-dim: #B0B0B0;
    --iv-border: rgba(200, 16, 46, 0.25);
}

/* Page background — subtle gothic gradient */
.stApp {
    background: linear-gradient(180deg, #0E1117 0%, #1a0a14 100%) !important;
}

/* Headers — Iron Vespers blood red */
h1, h2, h3, h4 {
    color: var(--iv-text) !important;
    font-family: 'Georgia', 'Times New Roman', serif !important;
    letter-spacing: 0.02em;
}

h1 {
    background: linear-gradient(135deg, #FAFAFA 0%, #C8102E 50%, #9D00FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900 !important;
    text-transform: uppercase;
    border-bottom: 2px solid var(--iv-red);
    padding-bottom: 0.4em;
}

/* Sidebar — iron-forged */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a0a 0%, #1a0a14 100%) !important;
    border-right: 1px solid var(--iv-border);
}

section[data-testid="stSidebar"] h1 {
    font-size: 1.6em !important;
    text-transform: none;
    border-bottom: none;
}

/* Primary buttons — blood red */
.stButton > button[kind="primary"],
.stButton > button {
    background: linear-gradient(135deg, #C8102E 0%, #9D00FF 100%) !important;
    color: #FAFAFA !important;
    border: 1px solid var(--iv-red) !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #FF1F44 0%, #C8102E 100%) !important;
    border-color: var(--iv-red-hot) !important;
    box-shadow: 0 0 18px rgba(200, 16, 46, 0.5) !important;
    transform: translateY(-1px);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 1px solid var(--iv-border);
}

.stTabs [data-baseweb="tab"] {
    background: var(--iv-bg-elev) !important;
    color: var(--iv-text-dim) !important;
    border: 1px solid var(--iv-border) !important;
    border-radius: 4px 4px 0 0 !important;
    padding: 8px 18px !important;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, #C8102E 0%, #1a0a14 100%) !important;
    color: #FAFAFA !important;
    border-color: var(--iv-red) !important;
}

/* Text inputs and selectboxes — dark with red accent */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background: var(--iv-bg-elev) !important;
    color: var(--iv-text) !important;
    border: 1px solid var(--iv-border) !important;
    caret-color: var(--iv-red) !important;
}

.stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"]:focus {
    border-color: var(--iv-red-hot) !important;
    box-shadow: 0 0 0 1px var(--iv-red) !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--iv-red) !important;
}

/* Code blocks */
.stCodeBlock, code, pre {
    background: #0a0a0a !important;
    border: 1px solid var(--iv-border) !important;
    border-left: 3px solid var(--iv-red) !important;
}

/* Markdown links */
a { color: var(--iv-red) !important; }
a:hover { color: var(--iv-red-hot) !important; }

/* Wolf-header hero (rendered as raw HTML) */
.iv-hero {
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 20px 0;
    border-bottom: 1px solid var(--iv-border);
    margin-bottom: 20px;
}
.iv-hero img { width: 80px; height: 80px; }

/* Wolf animation — applied to the <img> wrapper, not the SVG internals.
   This animates the WHOLE rendered image (including the eyes), so the
   wolf appears to pulse/float even though the SVG file is static. */
@keyframes wolfGlow {
  0%, 100% { filter: drop-shadow(0 0 4px rgba(200, 16, 46, 0.6)) drop-shadow(0 0 8px rgba(200, 16, 46, 0.3)); }
  50%      { filter: drop-shadow(0 0 12px rgba(255, 31, 68, 0.95)) drop-shadow(0 0 24px rgba(200, 16, 46, 0.7)); }
}
@keyframes wolfFloat {
  0%, 100% { transform: translateY(0px); }
  50%      { transform: translateY(-3px); }
}
.iv-hero img {
  animation: wolfGlow 2.4s ease-in-out infinite,
             wolfFloat 4s ease-in-out infinite;
  will-change: filter, transform;
}

/* Sidebar wolf — same animation, smaller scale */
[data-testid="stSidebar"] .iv-hero img {
  width: 60px; height: 60px;
  animation: wolfGlow 2.6s ease-in-out infinite,
             wolfFloat 4.4s ease-in-out infinite;
}
.iv-hero-text h1 {
    margin: 0;
    font-size: 2.2em;
    border: none;
    background: linear-gradient(135deg, #FAFAFA 0%, #C8102E 50%, #9D00FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-transform: uppercase;
}
.iv-hero-text .iv-tag {
    color: var(--iv-text-dim);
    font-style: italic;
    font-size: 1.1em;
    margin-top: 4px;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)

# ====================
#   ARTIST DATABASE
# ====================
SINGER_DB = {
    # === Pop ===
    "taylor swift": {"genre": "Pop, Country Pop", "mood": "Reflective, romantic, empowering", "style": "Storytelling lyrics, emotional vulnerability", "vocal_style": "Clear, conversational, soft to powerful", "instruments": "Acoustic guitar, synths, strings", "production": "Polished, layered, modern pop"},
    "billie eilish": {"genre": "Electropop, Bedroom Pop", "mood": "Brooding, atmospheric, haunting", "style": "Whispery vocals, dark themes, minimalist", "vocal_style": "Whispered, breathy, intimate", "instruments": "Sub bass, sparse synths", "production": "Minimal, bass-heavy, intimate"},
    "dua lipa": {"genre": "Pop, Disco", "mood": "Confident, energetic, danceable", "style": "Disco revival, powerful vocals", "vocal_style": "Strong, clear, commanding", "instruments": "Funky bass, strings, drums", "production": "Retro-modern, polished"},
    "harry styles": {"genre": "Pop Rock, Soft Rock", "mood": "Nostalgic, romantic, breezy", "style": "70s inspired, storytelling", "vocal_style": "Warm, raspy, emotive", "instruments": "Guitar, piano, horns", "production": "Vintage, warm, analog"},
    "ariana grande": {"genre": "Pop, R&B", "mood": "Playful, confident, sultry", "style": "Vocal acrobatics, modern pop", "vocal_style": "Agile, high range, melismatic", "instruments": "Synths, trap drums", "production": "Polished, modern, punchy"},
    "the weeknd": {"genre": "R&B, Synthwave", "mood": "Dark, mysterious, seductive", "style": "80s inspired, atmospheric", "vocal_style": "Falsetto, smooth, emotional", "instruments": "Synths, 808s, pads", "production": "Atmospheric, retro-futuristic"},
    "sabrina carpenter": {"genre": "Pop", "mood": "Playful, flirty, confident", "style": "Catchy hooks, bubbly", "vocal_style": "Bright, sassy, melodic", "instruments": "Synths, crisp drums, bass", "production": "Glossy, radio-ready"},
    "olivia rodrigo": {"genre": "Pop Rock, Pop Punk", "mood": "Angsty, emotional, youthful", "style": "Confessional lyrics, driving energy", "vocal_style": "Raw, expressive, belting", "instruments": "Electric guitar, drums, synths", "production": "Modern pop-punk edge"},
    "chappell roan": {"genre": "Pop, Synthpop", "mood": "Dramatic, campy, empowering", "style": "Theatrical, queer anthems", "vocal_style": "Bold, theatrical, powerful", "instruments": "Synths, disco beats, strings", "production": "Glittery, maximalist"},
    "charli xcx": {"genre": "Hyperpop, Electropop", "mood": "Chaotic, party, rebellious", "style": "Experimental, clubby", "vocal_style": "Energetic, processed, bratty", "instruments": "Hard synths, 808s, glitches", "production": "Futuristic, abrasive, fun"},
    "bruno mars": {"genre": "Pop, Funk", "mood": "Groovy, upbeat, romantic", "style": "Retro soul-funk blend", "vocal_style": "Smooth, versatile, silky", "instruments": "Live band, horns, bass", "production": "Polished, vintage-modern"},
    "doja cat": {"genre": "Pop, Hip-Hop, R&B", "mood": "Playful, seductive, quirky", "style": "Genre-blending, witty", "vocal_style": "Versatile, rap-sing, confident", "instruments": "Trap beats, synths, bass", "production": "Eclectic, modern"},

    # === Pop (top-up to 25) ===
    "madonna": {"genre": "Pop", "mood": "Bold, provocative, dancefloor", "style": "Pop reinvention, dance-pop pioneer", "vocal_style": "Confident, distinct, dynamic", "instruments": "Synths, dance beats, layered vocals", "production": "Polished, era-defining, dance"},
    "michael jackson": {"genre": "Pop, R&B", "mood": "Iconic, rhythmic, timeless", "style": "King of Pop, funk-pop perfection", "vocal_style": "Michael Jackson, hiccups, dynamic, smooth", "instruments": "Live funk band, synths, percussion", "production": "Quincy Jones polish, timeless, layered"},
    "prince": {"genre": "Pop, Funk, R&B", "mood": "Sensual, funky, virtuosic", "style": "Funk-pop genius, multi-instrumentalist", "vocal_style": "Prince, falsetto, distinctive, dynamic", "instruments": "Live funk band, synths, guitar virtuosity", "production": "Polished funk, layered, revolutionary"},
    "whitney houston": {"genre": "Pop, R&B", "mood": "Powerful, anthemic, soaring", "style": "Vocal powerhouse, pop ballads", "vocal_style": "Whitney, powerhouse soprano, dynamic", "instruments": "Piano, synths, full pop band", "production": "Polished 80s/90s pop, big choruses"},
    "mariah carey": {"genre": "Pop, R&B", "mood": "Glamorous, virtuosic, dramatic", "style": "Vocal virtuoso, pop diva", "vocal_style": "Mariah, melismatic whistle register, dynamic", "instruments": "Piano, synths, full pop orchestra", "production": "Polished 90s pop, layered, big choruses"},
    "celine dion": {"genre": "Pop", "mood": "Dramatic, emotional, anthemic", "style": "Pop ballad diva, Titanic era", "vocal_style": "Celine Dion, powerful, dramatic soprano", "instruments": "Piano, strings, full pop orchestra", "production": "Polished pop, dramatic, cinematic"},
    "britney spears": {"genre": "Pop", "mood": "Playful, energetic, dance-pop", "style": "Pop princess, dance-pop pioneer", "vocal_style": "Britney, pop, breathy + belting, distinctive", "instruments": "Synths, dance beats, layered vocals", "production": "Max Martin polish, polished dance-pop"},
    "christina aguilera": {"genre": "Pop, R&B", "mood": "Powerful, bold, vocal-forward", "style": "Pop vocal powerhouse, Xtina era", "vocal_style": "Xtina, melismatic belting, dynamic", "instruments": "Piano, synths, full pop band", "production": "Polished pop, vocal-forward, layered"},
    "lady gaga": {"genre": "Pop, Electropop", "mood": "Bold, theatrical, avant-garde", "style": "Theatrical pop, fashion-art-pop", "vocal_style": "Lady Gaga, belting, distinctive, dynamic", "instruments": "Synths, dance beats, layered vocals", "production": "Polished avant-pop, theatrical, layered"},
    "katy perry": {"genre": "Pop", "mood": "Playful, campy, anthemic", "style": "Camp pop anthems, candy-coated", "vocal_style": "Katy Perry, bright pop, dynamic", "instruments": "Synths, dance beats, big choruses", "production": "Max Martin polish, polished pop"},
    "rihanna": {"genre": "Pop, R&B", "mood": "Confident, cool, varied", "style": "Pop-R&B hits, era-defining", "vocal_style": "Rihanna, distinctive, varied, dynamic", "instruments": "Dance beats, synths, varied instrumentation", "production": "Polished pop, varied, era-defining"},
    "beyonce alt": {"genre": "Pop, R&B", "mood": "Confident, fierce, soulful", "style": "Powerful vocals, genre-blending", "vocal_style": "Beyonce, belting, distinctive, dynamic", "instruments": "Full band, horns, strings", "production": "Polished, powerful, modern"},
    "adele": {"genre": "Pop, Soul", "mood": "Emotional, powerful, raw", "style": "Vocal powerhouse, pop ballads", "vocal_style": "Adele, powerful contralto, emotional", "instruments": "Piano, full band, orchestral", "production": "Polished pop, emotional, big"},
    "ed sheeran": {"genre": "Pop", "mood": "Emotional, intimate, anthemic", "style": "Singer-songwriter pop, loop pedal", "vocal_style": "Ed Sheeran, conversational + belting, dynamic", "instruments": "Acoustic guitar, loop pedal, layered", "production": "Modern pop polish, layered, intimate"},
    "dua lipa alt": {"genre": "Pop, Disco", "mood": "Confident, energetic, danceable", "style": "Disco revival, powerful vocals", "vocal_style": "Dua Lipa, strong, clear, commanding", "instruments": "Funky bass, strings, drums", "production": "Retro-modern, polished"},
    "lizzo": {"genre": "Pop, R&B", "mood": "Confident, joyful, body-positive", "style": "Pop-R&B with hip-hop edge, flutist", "vocal_style": "Lizzo, belting, distinctive, dynamic", "instruments": "Synths, hip-hop drums, flute solos", "production": "Polished pop-R&B, hip-hop edge"},
    "harry styles alt": {"genre": "Pop Rock, Soft Rock", "mood": "Nostalgic, romantic, breezy", "style": "70s inspired, storytelling", "vocal_style": "Harry Styles, warm, raspy, emotive", "instruments": "Guitar, piano, horns", "production": "Vintage, warm, analog"},
    "miley cyrus": {"genre": "Pop, Pop Rock", "mood": "Rebellious, varied, modern", "style": "Pop reinvention, varied eras", "vocal_style": "Miley, raspy + belting, versatile", "instruments": "Synths, country-rock, varied", "production": "Polished, varied, modern"},
    "janelle monae": {"genre": "Pop, R&B, Funk", "mood": "Futuristic, theatrical, afro-futurist", "style": "Afrofuturist pop-R&B-funk, conceptual", "vocal_style": "Janelle Monae, theatrical, distinctive, dynamic", "instruments": "Funk band, synths, hip-hop drums", "production": "Polished afro-futurist, layered, conceptual"},
    "shawn mendes": {"genre": "Pop", "mood": "Romantic, youthful, modern", "style": "Modern pop, guitar-driven ballads", "vocal_style": "Shawn Mendes, conversational + belting", "instruments": "Acoustic guitar, synths, light drums", "production": "Modern pop polish, layered"},

    # === Rock / Alt Rock ===
    "queen": {"genre": "Rock, Arena Rock", "mood": "Epic, dramatic, triumphant", "style": "Operatic, theatrical, anthemic", "vocal_style": "Powerful, operatic, multi-octave", "instruments": "Electric guitar, piano, layered vocals", "production": "Grand, stadium-filling, layered"},
    "nirvana": {"genre": "Grunge, Alternative", "mood": "Angsty, melancholic, intense", "style": "Raw, distorted, dynamic shifts", "vocal_style": "Raspy, strained, soft-loud", "instruments": "Distorted guitar, bass, heavy drums", "production": "Lo-fi, raw, garage"},
    "foo fighters": {"genre": "Alternative Rock", "mood": "Uplifting, defiant, energetic", "style": "Energetic, melodic, driving", "vocal_style": "Raw, powerful, melodic", "instruments": "Electric guitar, bass, drums", "production": "Clean, powerful, radio-friendly"},
    "arctic monkeys": {"genre": "Indie Rock, Garage", "mood": "Cool, detached, energetic", "style": "Witty lyrics, angular guitars", "vocal_style": "Conversational, Sheffield accent", "instruments": "Jangly guitar, bass, drums", "production": "Raw, live energy"},
    "radiohead": {"genre": "Alternative, Art Rock", "mood": "Melancholic, anxious, atmospheric", "style": "Experimental, electronic elements", "vocal_style": "Emotional, falsetto, strained", "instruments": "Guitar, synths, orchestral", "production": "Atmospheric, layered, experimental"},
    "led zeppelin": {"genre": "Hard Rock, Blues Rock", "mood": "Epic, powerful, mystical", "style": "Blues-based, heavy riffs", "vocal_style": "Powerful, wailing, bluesy", "instruments": "Electric guitar, drums, bass", "production": "Raw, powerful, live"},
    "linkin park": {"genre": "Nu-Metal, Alternative Rock", "mood": "Intense, emotional, aggressive", "style": "Rap-rock fusion, heavy drops", "vocal_style": "Screaming + melodic rap", "instruments": "Heavy guitars, electronics, turntables", "production": "Aggressive, layered"},

    # === Rock (top-up to 25) ===
    "the beatles": {"genre": "Rock", "mood": "Innovative, timeless, varied", "style": "British Invasion, songwriting pioneers", "vocal_style": "Four-part harmonies, distinct voices, dynamic", "instruments": "Rickenbacker guitars, sitar, orchestral", "production": "Revolutionary 60s, varied, polished"},
    "the rolling stones": {"genre": "Rock", "mood": "Rebellious, bluesy, swaggering", "style": "British blues-rock, rock & roll legends", "vocal_style": "Jagger, distinctive, dynamic, raw", "instruments": "Blues-rock guitar, rolling bass, dynamic drums", "production": "Raw 60s rock, polished, era-defining"},
    "pink floyd": {"genre": "Rock", "mood": "Atmospheric, philosophical, progressive", "style": "Progressive rock, conceptual epics", "vocal_style": "Roger Waters / David Gilmour, atmospheric, emotional", "instruments": "Gilmour guitar, synthesizers, orchestral, effects", "production": "Atmospheric, layered, era-defining progressive"},
    "the who": {"genre": "Rock", "mood": "Explosive, rebellious, mod", "style": "Mod rock, rock opera pioneers", "vocal_style": "Roger Daltrey, dynamic, raw, powerful", "instruments": "Power chords, big drums, dynamic bass", "production": "Explosive 60s/70s rock, powerful, raw"},
    "led zeppelin alt": {"genre": "Rock, Hard Rock", "mood": "Epic, powerful, mystical", "style": "Blues-based, heavy riffs", "vocal_style": "Robert Plant, powerful, wailing, bluesy", "instruments": "Electric guitar, drums, bass", "production": "Raw, powerful, live"},
    "deep purple": {"genre": "Rock, Hard Rock", "mood": "Heavy, virtuosic, 70s", "style": "British hard rock, organ-driven heavy", "vocal_style": "Ian Gillan, powerful high tenor, dynamic", "instruments": "Heavy organ, virtuoso guitar, big drums", "production": "70s hard rock, heavy, polished"},
    "black sabbath alt": {"genre": "Rock, Hard Rock", "mood": "Dark, heavy, foundational", "style": "The blueprint for heavy metal, crushing riffs", "vocal_style": "Ozzy Osbourne, plaintive wail, iconic", "instruments": "Downtuned guitar, bass, drums, Iommi riffs", "production": "Raw 70s analog, towering low end"},
    "ac dc": {"genre": "Rock, Hard Rock", "mood": "Energetic, fun, anthemic", "style": "No-frills hard rock, schoolboy uniform rock", "vocal_style": "Bon Scott / Brian Johnson, raw, energetic", "instruments": "Twin guitar crunch, driving bass, big drums", "production": "No-frills hard rock, big, polished"},
    "aerosmith": {"genre": "Rock, Hard Rock", "mood": "Energetic, bluesy, retro", "style": "Blues-rock, swagger, 70s arena", "vocal_style": "Steven Tyler, raw + belting, distinctive", "instruments": "Blues-rock guitar, driving bass, dynamic drums", "production": "70s arena rock polish, big, dynamic"},
    "van halen": {"genre": "Rock, Hard Rock", "mood": "Virtuosic, party, 80s", "style": "Hard rock virtuoso, 80s party anthems", "vocal_style": "David Lee Roth / Sammy Hagar, dynamic, energetic", "instruments": "EVH virtuosic guitar, big drums, synth", "production": "80s hard rock polish, virtuosic, big"},
    "bon jovi": {"genre": "Rock, Arena Rock", "mood": "Anthemic, romantic, 80s", "style": "80s arena rock anthems, hair metal polish", "vocal_style": "Jon Bon Jovi, big belting, distinctive", "instruments": "Arena rock guitar, big drums, layered keys", "production": "80s arena rock polish, big, anthemic"},
    "def leppard": {"genre": "Rock, Hard Rock", "mood": "Anthemic, polished, 80s", "style": "80s British hard rock, polished anthems", "vocal_style": "Joe Elliott, powerful tenor, dynamic", "instruments": "Twin lead guitar, big drums, layered keys", "production": "80s hard rock polish, layered, big"},
    "europe": {"genre": "Rock, Hard Rock", "mood": "Anthemic, melodic, 80s", "style": "Swedish hard rock, 'The Final Countdown' era", "vocal_style": "Joey Tempest, dynamic tenor, melodic", "instruments": "Hard rock guitar, driving bass, big keys", "production": "80s hard rock polish, big, anthemic"},
    "rush": {"genre": "Rock, Progressive", "mood": "Virtuosic, progressive, varied", "style": "Canadian progressive rock, virtuoso power trio", "vocal_style": "Geddy Lee, distinctive tenor, dynamic", "instruments": "Virtuoso bass, virtuosic guitar, technical drums", "production": "Progressive rock polish, virtuosic, varied"},
    "yes": {"genre": "Rock, Progressive", "mood": "Virtuosic, fantastical, complex", "style": "British progressive rock, fantastical", "vocal_style": "Jon Anderson, ethereal tenor, distinctive", "instruments": "Virtuoso guitar, complex keys, technical drums", "production": "Progressive rock polish, complex, layered"},
    "genesis": {"genre": "Rock, Progressive", "mood": "Theatrical, progressive, varied", "style": "British progressive rock, theatrical", "vocal_style": "Peter Gabriel / Phil Collins, theatrical, dynamic", "instruments": "Progressive guitar, keys, dynamic drums", "production": "Theatrical progressive polish, varied"},
    "u2": {"genre": "Rock, Alternative", "mood": "Anthemic, atmospheric, modern", "style": "Modern anthemic rock, atmospheric", "vocal_style": "Bono, dynamic tenor, distinctive", "instruments": "The Edge guitar (delay-driven), big bass, big drums", "production": "Modern anthemic, atmospheric, polished"},
    "rem": {"genre": "Rock, Alternative", "mood": "Introspective, jangly, varied", "style": "American alternative rock, jangly guitar", "vocal_style": "Michael Stipe, mumbled + dynamic, distinctive", "instruments": "Jangly Rickenbacker guitar, melodic bass, light drums", "production": "Lo-fi to polished alt rock, jangly, varied"},
    "the cure": {"genre": "Rock, Alternative", "mood": "Atmospheric, melancholic, gothic", "style": "Gothic alternative rock, atmospheric", "vocal_style": "Robert Smith, distinctive, dynamic, atmospheric", "instruments": "Atmospheric guitar, synth, dynamic bass", "production": "Atmospheric alt rock, polished, layered"},
    "joy division": {"genre": "Rock, Post-Punk", "mood": "Dark, minimalist, foundational", "style": "Foundational post-punk, dark minimalism", "vocal_style": "Ian Curtis, deep baritone, distinctive, raw", "instruments": "Sparse guitar, deep bass, mechanical drums", "production": "Lo-fi dark, foundational, minimal"},
    "new order": {"genre": "Rock, Post-Punk", "mood": "Danceable, atmospheric, modern", "style": "Post-punk meets dance, synth-driven", "vocal_style": "Bernard Sumner, distinctive, melodic, dynamic", "instruments": "Synth-pop, dance bass, light guitar, dynamic drums", "production": "Dance-rock polish, atmospheric, modern"},
    "blondie": {"genre": "Rock, New Wave", "mood": "Cool, new wave, varied", "style": "New wave pioneers, hip hop-rock crossover", "vocal_style": "Debbie Harry, cool, distinctive, dynamic", "instruments": "New wave guitar, disco bass, dynamic drums", "production": "New wave polish, cool, varied"},
    "talking heads": {"genre": "Rock, New Wave", "mood": "Quirky, intellectual, new wave", "style": "Art-school new wave, world music influences", "vocal_style": "David Byrne, distinctive, dynamic, varied", "instruments": "Quirky guitar, funky bass, world-influenced drums", "production": "New wave polish, art-school, varied"},
    "sting": {"genre": "Rock, Pop", "mood": "Sophisticated, jazzy, varied", "style": "Sophisticated pop-rock, jazz-fusion", "vocal_style": "Sting, distinctive baritone, dynamic", "instruments": "Jazz-fusion bass, sophisticated guitar, world drums", "production": "Polished, sophisticated, jazz-influenced"},

    # === Hip-Hop / Rap ===
    "kendrick lamar": {"genre": "Hip-Hop, Jazz Rap", "mood": "Introspective, urgent, complex", "style": "Lyrically dense, socially conscious", "vocal_style": "Versatile, rapid-fire, melodic", "instruments": "Jazz samples, live instruments", "production": "Layered, organic, sophisticated"},
    "drake": {"genre": "Hip-Hop, R&B", "mood": "Melancholic, confident, romantic", "style": "Melodic rap, emotional", "vocal_style": "Melodic rapping, singing", "instruments": "808s, smooth synths", "production": "Polished, atmospheric, moody"},
    "kanye west": {"genre": "Hip-Hop, Experimental", "mood": "Dramatic, confident, introspective", "style": "Boundary-pushing, soul samples", "vocal_style": "Confident, emotional, varied", "instruments": "Orchestral, synths, samples", "production": "Layered, experimental, detailed"},
    "tyler the creator": {"genre": "Hip-Hop, Alternative", "mood": "Playful, confident, introspective", "style": "Eccentric, genre-blending", "vocal_style": "Deep, aggressive, melodic", "instruments": "Live instruments, synths", "production": "Colorful, experimental, warm"},
    "travis scott": {"genre": "Hip-Hop, Trap", "mood": "Dark, psychedelic, energetic", "style": "Atmospheric trap, auto-tune", "vocal_style": "Auto-tuned, melodic, ad-libs", "instruments": "Heavy 808s, synths", "production": "Atmospheric, distorted, spacey"},
    "doechii": {"genre": "Hip-Hop, Experimental", "mood": "Bold, theatrical, fierce", "style": "Eclectic flows, genre-hopping", "vocal_style": "Versatile, commanding, playful", "instruments": "Trap, jazz, electronic", "production": "Dynamic, cinematic"},
    "anderson .paak": {"genre": "R&B, Funk, Soul", "mood": "Groovy, warm, joyful", "style": "Retro-soul funk with hip-hop edge", "vocal_style": "Smooth falsetto, silky, charismatic rapping", "instruments": "Live drums, bass, Rhodes, horns", "production": "Warm vintage polish, organic groove"},

    # === Hip-Hop (top-up to 25) ===
    "jay z": {"genre": "Hip-Hop", "mood": "Confident, ambitious, sophisticated", "style": "New York hip-hop mogul, sophisticated flows", "vocal_style": "Jay-Z, sophisticated flow, charismatic", "instruments": "Soul samples, live instruments, varied", "production": "Sophisticated hip-hop, layered, era-defining"},
    "nas": {"genre": "Hip-Hop", "mood": "Introspective, poetic, classic", "style": "New York hip-hop poet, Illmatic era", "vocal_style": "Nas, poetic flow, distinctive, raw", "instruments": "Soul samples, jazz, live instruments", "production": "Classic NY hip-hop, layered, foundational"},
    "biggie": {"genre": "Hip-Hop", "mood": "Confident, smooth, narrative", "style": "New York hip-hop storyteller, smooth flow", "vocal_style": "Notorious B.I.G., smooth baritone, dynamic", "instruments": "Soul samples, varied samples", "production": "Classic NY hip-hop, smooth, polished"},
    "tupac": {"genre": "Hip-Hop", "mood": "Intense, poetic, political", "style": "West Coast hip-hop, political poet", "vocal_style": "Tupac, distinctive, dynamic, raw", "instruments": "G-funk synths, live instruments, samples", "production": "West Coast G-funk, polished, era-defining"},
    "eminem": {"genre": "Hip-Hop", "mood": "Agile, aggressive, comedic", "style": "Detroit hip-hop, technical lyricist", "vocal_style": "Eminem, technical rapid-fire, distinctive", "instruments": "Varied samples, live instruments", "production": "Detroit hip-hop, varied, technical"},
    "lil wayne": {"genre": "Hip-Hop", "mood": "Quirky, prolific, varied", "style": "New Orleans hip-hop, prolific catalog", "vocal_style": "Lil Wayne, distinctive, auto-tuned, varied", "instruments": "Varied samples, live instruments", "production": "Southern hip-hop, varied, prolific"},
    "nicki minaj": {"genre": "Hip-Hop, Pop", "mood": "Bold, versatile, theatrical", "style": "Female rap-pop crossover, theatrical", "vocal_style": "Nicki Minaj, versatile, theatrical, dynamic", "instruments": "Varied samples, pop production", "production": "Hip-hop pop crossover, theatrical, polished"},
    "lil baby": {"genre": "Hip-Hop", "mood": "Modern, melodic, trap", "style": "Modern Atlanta trap, melodic flows", "vocal_style": "Lil Baby, melodic trap, distinctive", "instruments": "Trap 808s, modern samples", "production": "Modern trap polish, melodic, layered"},
    "ice cube": {"genre": "Hip-Hop, West Coast", "mood": "Aggressive, political, West Coast", "style": "West Coast hip-hop, NWA alumni, political", "vocal_style": "Ice Cube, aggressive, distinctive, raw", "instruments": "G-funk synths, live instruments", "production": "West Coast G-funk, aggressive, polished"},
    "snoop dogg": {"genre": "Hip-Hop, West Coast", "mood": "Laid-back, smooth, West Coast", "style": "West Coast G-funk, smooth flow", "vocal_style": "Snoop Dogg, smooth, distinctive, melodic", "instruments": "G-funk synths, live instruments, samples", "production": "West Coast G-funk, smooth, polished"},
    "dr dre": {"genre": "Hip-Hop, Producer", "mood": "Polished, G-funk, West Coast", "style": "Hip-hop production pioneer, G-funk architect", "vocal_style": "Dr. Dre, smooth, producer-led", "instruments": "Live instruments, G-funk synths, varied", "production": "G-funk polish, era-defining, layered"},
    "outkast": {"genre": "Hip-Hop, Southern", "mood": "Funky, varied, innovative", "style": "Southern hip-hop, funk-infused, innovative", "vocal_style": "Andre 3000 + Big Boi, versatile, dynamic", "instruments": "Funk band, hip-hop drums, live instruments", "production": "Southern hip-hop, funky, innovative polish"},
    "dmx": {"genre": "Hip-Hop, East Coast", "mood": "Intense, dark, raw", "style": "East Coast hardcore hip-hop, intense", "vocal_style": "DMX, barking, distinctive, raw", "instruments": "Dark samples, live instruments", "production": "Dark East Coast hip-hop, raw, intense"},
    "method man": {"genre": "Hip-Hop, East Coast", "mood": "Smooth, soulful, Wu-Tang", "style": "Wu-Tang Clan, soulful East Coast hip-hop", "vocal_style": "Method Man, smooth, soulful, distinctive", "instruments": "Soul samples, martial arts samples, varied", "production": "Wu-Tang polish, soulful, varied"},
    "ol dirty bastard": {"genre": "Hip-Hop, East Coast", "mood": "Quirky, raw, Wu-Tang", "style": "Wu-Tang Clan, raw and quirky", "vocal_style": "Ol' Dirty Bastard, raw, distinctive, chaotic", "instruments": "Soul samples, martial arts samples, varied", "production": "Wu-Tang raw, varied, chaotic"},
    "rakim": {"genre": "Hip-Hop, East Coast", "mood": "Sophisticated, foundational, technical", "style": "Pioneer of internal rhyme, technical flow", "vocal_style": "Rakim, smooth, technical, foundational", "instruments": "Jazz samples, soul samples", "production": "Foundational hip-hop, polished, era-defining"},
    "ghostface killah": {"genre": "Hip-Hop, East Coast", "mood": "Intense, narrative, Wu-Tang", "style": "Wu-Tang Clan, narrative East Coast", "vocal_style": "Ghostface, intense, narrative, distinctive", "instruments": "Soul samples, varied samples", "production": "Wu-Tang polish, narrative, varied"},
    "kanye alt": {"genre": "Hip-Hop, Experimental", "mood": "Dramatic, confident, introspective", "style": "Boundary-pushing, soul samples", "vocal_style": "Kanye, confident, emotional, varied", "instruments": "Orchestral, synths, samples", "production": "Layered, experimental, detailed"},
    "j cole": {"genre": "Hip-Hop", "mood": "Introspective, conscious, modern", "style": "Modern conscious hip-hop, storytelling", "vocal_style": "J. Cole, conversational, introspective, dynamic", "instruments": "Soul samples, live instruments, varied", "production": "Modern conscious hip-hop, polished, layered"},
    "future": {"genre": "Hip-Hop, Trap", "mood": "Melodic, trap, varied", "style": "Atlanta trap pioneer, melodic auto-tune", "vocal_style": "Future, melodic auto-tune, distinctive, varied", "instruments": "Trap 808s, modern samples", "production": "Modern trap polish, melodic, varied"},
    "21 savage": {"genre": "Hip-Hop, Trap", "mood": "Dark, melodic, modern", "style": "Modern dark trap, melodic", "vocal_style": "21 Savage, deadpan, melodic, distinctive", "instruments": "Dark trap 808s, modern samples", "production": "Dark trap polish, melodic, layered"},
    "kendrick lamar alt": {"genre": "Hip-Hop, Jazz Rap", "mood": "Introspective, urgent, complex", "style": "Lyrically dense, socially conscious", "vocal_style": "Kendrick, versatile, rapid-fire, melodic", "instruments": "Jazz samples, live instruments", "production": "Layered, organic, sophisticated"},
    "earl sweatshirt": {"genre": "Hip-Hop, Alternative", "mood": "Introspective, abstract, alternative", "style": "Odd Future alum, abstract introspective hip-hop", "vocal_style": "Earl Sweatshirt, abstract, raw, introspective", "instruments": "Lo-fi samples, abstract production", "production": "Lo-fi abstract hip-hop, layered, varied"},

    # === R&B (top-up to 25) ===
    "alicia keys": {"genre": "R&B, Soul", "mood": "Soulful, powerful, authentic", "style": "Modern soul-R&B, piano-driven", "vocal_style": "Alicia Keys, powerful soulful soprano, dynamic", "instruments": "Piano, full R&B band, strings", "production": "Modern soul-R&B polish, piano-driven, layered"},
    "usher": {"genre": "R&B", "mood": "Smooth, seductive, modern", "style": "Modern R&B, smooth and seductive", "vocal_style": "Usher, smooth falsetto, dynamic", "instruments": "Smooth R&B production, layered synths", "production": "Modern R&B polish, smooth, layered"},
    "chris brown": {"genre": "R&B, Pop", "mood": "Energetic, varied, modern", "style": "Modern R&B-pop, dance and vocal versatility", "vocal_style": "Chris Brown, versatile, dynamic, distinctive", "instruments": "R&B production, varied", "production": "Modern R&B-pop polish, varied, layered"},
    "ne yo": {"genre": "R&B", "mood": "Smooth, romantic, modern", "style": "Modern R&B, smooth songwriter", "vocal_style": "Ne-Yo, smooth, distinctive, dynamic", "instruments": "Smooth R&B production, layered synths", "production": "Modern R&B polish, smooth, layered"},
    "the weeknd alt": {"genre": "R&B, Synthwave", "mood": "Dark, mysterious, seductive", "style": "80s inspired, atmospheric", "vocal_style": "The Weeknd, falsetto, smooth, emotional", "instruments": "Synths, 808s, pads", "production": "Atmospheric, retro-futuristic"},
    "frank ocean alt": {"genre": "R&B, Alternative", "mood": "Dreamy, melancholic, intimate", "style": "Introspective, experimental", "vocal_style": "Frank Ocean, breathy, understated, falsetto", "instruments": "Sparse synths, guitars", "production": "Minimal, atmospheric, hazy"},
    "chloe x halle": {"genre": "R&B", "mood": "Soulful, ethereal, modern", "style": "Modern R&B duo, ethereal harmonies", "vocal_style": "Chloe x Halle, ethereal harmonies, soulful", "instruments": "R&B production, layered synths, live instruments", "production": "Modern R&B polish, ethereal, layered"},
    "brandy": {"genre": "R&B", "mood": "Soulful, 90s, smooth", "style": "90s R&B pioneer, smooth", "vocal_style": "Brandy, distinctive soprano, soulful, smooth", "instruments": "90s R&B production, live instruments", "production": "90s R&B polish, smooth, layered"},
    "monica": {"genre": "R&B", "mood": "Soulful, 90s, smooth", "style": "90s R&B, smooth and soulful", "vocal_style": "Monica, soulful soprano, dynamic", "instruments": "90s R&B production, live instruments", "production": "90s R&B polish, smooth, layered"},
    "mary j blige": {"genre": "R&B, Soul", "mood": "Powerful, raw, soulful", "style": "Queen of Hip-Hop Soul, raw and powerful", "vocal_style": "Mary J. Blige, powerful, raw, distinctive", "instruments": "Soul samples, live instruments, hip-hop drums", "production": "Hip-hop soul polish, raw, layered"},
    "erykah badu": {"genre": "R&B, Neo-Soul", "mood": "Spiritual, eclectic, alternative", "style": "Neo-soul pioneer, eclectic and spiritual", "vocal_style": "Erykah Badu, distinctive, spiritual, varied", "instruments": "Lo-fi soul samples, live instruments", "production": "Neo-soul polish, lo-fi, eclectic"},
    "d angelo": {"genre": "R&B, Neo-Soul", "mood": "Spiritual, funky, organic", "style": "Neo-soul pioneer, organic funk-soul", "vocal_style": "D'Angelo, falsetto, distinctive, soulful", "instruments": "Funky live band, organic production", "production": "Organic neo-soul polish, funky, layered"},
    "jill scott": {"genre": "R&B, Neo-Soul", "mood": "Soulful, jazzy, neo-soul", "style": "Neo-soul pioneer, jazzy and soulful", "vocal_style": "Jill Scott, rich alto, soulful, distinctive", "instruments": "Live neo-soul band, jazzy instrumentation", "production": "Neo-soul polish, jazzy, organic"},
    "mos def": {"genre": "R&B, Hip-Hop", "mood": "Conscious, soulful, varied", "style": "Black Star alum, conscious hip-hop soul", "vocal_style": "Mos Def, soulful, dynamic, varied", "instruments": "Soul samples, live instruments", "production": "Conscious hip-hop polish, soulful, layered"},
    "jhené aiko": {"genre": "R&B", "mood": "Ethereal, dreamy, modern", "style": "Modern ethereal R&B, dreamy", "vocal_style": "Jhené Aiko, ethereal soprano, dreamy, soulful", "instruments": "Ethereal R&B production, layered synths", "production": "Ethereal R&B polish, dreamy, layered"},
    "kehlani": {"genre": "R&B", "mood": "Soulful, vulnerable, modern", "style": "Modern R&B, vulnerable and soulful", "vocal_style": "Kehlani, soulful alto, vulnerable, dynamic", "instruments": "Modern R&B production, layered synths", "production": "Modern R&B polish, vulnerable, layered"},
    "summer walker": {"genre": "R&B", "mood": "Vulnerable, modern, atmospheric", "style": "Modern atmospheric R&B, vulnerable", "vocal_style": "Summer Walker, vulnerable soprano, atmospheric", "instruments": "Atmospheric R&B production, layered", "production": "Atmospheric R&B polish, vulnerable, layered"},
    "h.e.r.": {"genre": "R&B", "mood": "Soulful, versatile, modern", "style": "Modern R&B, multi-instrumentalist, versatile", "vocal_style": "H.E.R., soulful, versatile, dynamic", "instruments": "Guitar, layered R&B production, varied", "production": "Modern R&B polish, versatile, layered"},
    "janet jackson": {"genre": "R&B, Pop", "mood": "Disciplined, rhythmic, pop", "style": "Pop-R&B dance pioneer, rhythmic", "vocal_style": "Janet Jackson, distinctive, rhythmic, dynamic", "instruments": "Pop-R&B production, layered synths, dance beats", "production": "Pop-R&B polish, rhythmic, layered"},
    "en vogue": {"genre": "R&B", "mood": "Soulful, 90s, group harmonies", "style": "90s R&B vocal group, harmonies", "vocal_style": "Four-part harmonies, soulful, dynamic", "instruments": "90s R&B production, live instruments", "production": "90s R&B polish, harmonies, layered"},

    # === Electronic (top-up to 25) ===
    "frank ocean": {"genre": "R&B, Alternative", "mood": "Dreamy, melancholic, intimate", "style": "Introspective, experimental", "vocal_style": "Breathy, understated, falsetto", "instruments": "Sparse synths, guitars", "production": "Minimal, atmospheric, hazy"},
    "beyonce": {"genre": "R&B, Pop", "mood": "Confident, fierce, soulful", "style": "Powerful vocals, genre-blending", "vocal_style": "Powerful, agile, commanding", "instruments": "Full band, horns, strings", "production": "Polished, powerful, modern"},
    "sza": {"genre": "R&B, Alternative", "mood": "Romantic, confident, melancholic", "style": "Alternative R&B, introspective", "vocal_style": "Soulful, raspy, unique", "instruments": "Smooth synths, guitar", "production": "Atmospheric, warm, modern"},
    "daniel caesar": {"genre": "R&B, Soul", "mood": "Intimate, spiritual, romantic", "style": "Neo-soul, gospel influences", "vocal_style": "Smooth, falsetto, soulful", "instruments": "Guitar, piano, minimal", "production": "Warm, organic, intimate"},
    "victoria monét": {"genre": "R&B, Pop", "mood": "Sensual, empowering, groovy", "style": "Silky melodies, confident", "vocal_style": "Smooth, layered harmonies", "instruments": "Synths, bass, percussion", "production": "Polished, lush"},
    "anderson .paak": {"genre": "R&B, Funk, Soul", "mood": "Groovy, warm, joyful", "style": "Retro-soul funk with hip-hop edge", "vocal_style": "Smooth falsetto, silky, charismatic rapping", "instruments": "Live drums, bass, Rhodes, horns", "production": "Warm vintage polish, organic groove"},

    # === Hip-Hop (top-up to 25) ===
    "jay z": {"genre": "Hip-Hop", "mood": "Confident, ambitious, sophisticated", "style": "New York hip-hop mogul, sophisticated flows", "vocal_style": "Jay-Z, sophisticated flow, charismatic", "instruments": "Soul samples, live instruments, varied", "production": "Sophisticated hip-hop, layered, era-defining"},
    "nas": {"genre": "Hip-Hop", "mood": "Introspective, poetic, classic", "style": "New York hip-hop poet, Illmatic era", "vocal_style": "Nas, poetic flow, distinctive, raw", "instruments": "Soul samples, jazz, live instruments", "production": "Classic NY hip-hop, layered, foundational"},
    "biggie": {"genre": "Hip-Hop", "mood": "Confident, smooth, narrative", "style": "New York hip-hop storyteller, smooth flow", "vocal_style": "Notorious B.I.G., smooth baritone, dynamic", "instruments": "Soul samples, varied samples", "production": "Classic NY hip-hop, smooth, polished"},
    "tupac": {"genre": "Hip-Hop", "mood": "Intense, poetic, political", "style": "West Coast hip-hop, political poet", "vocal_style": "Tupac, distinctive, dynamic, raw", "instruments": "G-funk synths, live instruments, samples", "production": "West Coast G-funk, polished, era-defining"},
    "eminem": {"genre": "Hip-Hop", "mood": "Agile, aggressive, comedic", "style": "Detroit hip-hop, technical lyricist", "vocal_style": "Eminem, technical rapid-fire, distinctive", "instruments": "Varied samples, live instruments", "production": "Detroit hip-hop, varied, technical"},
    "lil wayne": {"genre": "Hip-Hop", "mood": "Quirky, prolific, varied", "style": "New Orleans hip-hop, prolific catalog", "vocal_style": "Lil Wayne, distinctive, auto-tuned, varied", "instruments": "Varied samples, live instruments", "production": "Southern hip-hop, varied, prolific"},
    "nicki minaj": {"genre": "Hip-Hop, Pop", "mood": "Bold, versatile, theatrical", "style": "Female rap-pop crossover, theatrical", "vocal_style": "Nicki Minaj, versatile, theatrical, dynamic", "instruments": "Varied samples, pop production", "production": "Hip-hop pop crossover, theatrical, polished"},
    "lil baby": {"genre": "Hip-Hop", "mood": "Modern, melodic, trap", "style": "Modern Atlanta trap, melodic flows", "vocal_style": "Lil Baby, melodic trap, distinctive", "instruments": "Trap 808s, modern samples", "production": "Modern trap polish, melodic, layered"},
    "ice cube": {"genre": "Hip-Hop, West Coast", "mood": "Aggressive, political, West Coast", "style": "West Coast hip-hop, NWA alumni, political", "vocal_style": "Ice Cube, aggressive, distinctive, raw", "instruments": "G-funk synths, live instruments", "production": "West Coast G-funk, aggressive, polished"},
    "snoop dogg": {"genre": "Hip-Hop, West Coast", "mood": "Laid-back, smooth, West Coast", "style": "West Coast G-funk, smooth flow", "vocal_style": "Snoop Dogg, smooth, distinctive, melodic", "instruments": "G-funk synths, live instruments, samples", "production": "West Coast G-funk, smooth, polished"},
    "dr dre": {"genre": "Hip-Hop, Producer", "mood": "Polished, G-funk, West Coast", "style": "Hip-hop production pioneer, G-funk architect", "vocal_style": "Dr. Dre, smooth, producer-led", "instruments": "Live instruments, G-funk synths, varied", "production": "G-funk polish, era-defining, layered"},
    "outkast": {"genre": "Hip-Hop, Southern", "mood": "Funky, varied, innovative", "style": "Southern hip-hop, funk-infused, innovative", "vocal_style": "Andre 3000 + Big Boi, versatile, dynamic", "instruments": "Funk band, hip-hop drums, live instruments", "production": "Southern hip-hop, funky, innovative polish"},
    "dmx": {"genre": "Hip-Hop, East Coast", "mood": "Intense, dark, raw", "style": "East Coast hardcore hip-hop, intense", "vocal_style": "DMX, barking, distinctive, raw", "instruments": "Dark samples, live instruments", "production": "Dark East Coast hip-hop, raw, intense"},
    "method man": {"genre": "Hip-Hop, East Coast", "mood": "Smooth, soulful, Wu-Tang", "style": "Wu-Tang Clan, soulful East Coast hip-hop", "vocal_style": "Method Man, smooth, soulful, distinctive", "instruments": "Soul samples, martial arts samples, varied", "production": "Wu-Tang polish, soulful, varied"},
    "ol dirty bastard": {"genre": "Hip-Hop, East Coast", "mood": "Quirky, raw, Wu-Tang", "style": "Wu-Tang Clan, raw and quirky", "vocal_style": "Ol' Dirty Bastard, raw, distinctive, chaotic", "instruments": "Soul samples, martial arts samples, varied", "production": "Wu-Tang raw, varied, chaotic"},
    "rakim": {"genre": "Hip-Hop, East Coast", "mood": "Sophisticated, foundational, technical", "style": "Pioneer of internal rhyme, technical flow", "vocal_style": "Rakim, smooth, technical, foundational", "instruments": "Jazz samples, soul samples", "production": "Foundational hip-hop, polished, era-defining"},
    "ghostface killah": {"genre": "Hip-Hop, East Coast", "mood": "Intense, narrative, Wu-Tang", "style": "Wu-Tang Clan, narrative East Coast", "vocal_style": "Ghostface, intense, narrative, distinctive", "instruments": "Soul samples, varied samples", "production": "Wu-Tang polish, narrative, varied"},
    "kanye alt": {"genre": "Hip-Hop, Experimental", "mood": "Dramatic, confident, introspective", "style": "Boundary-pushing, soul samples", "vocal_style": "Kanye, confident, emotional, varied", "instruments": "Orchestral, synths, samples", "production": "Layered, experimental, detailed"},
    "j cole": {"genre": "Hip-Hop", "mood": "Introspective, conscious, modern", "style": "Modern conscious hip-hop, storytelling", "vocal_style": "J. Cole, conversational, introspective, dynamic", "instruments": "Soul samples, live instruments, varied", "production": "Modern conscious hip-hop, polished, layered"},
    "future": {"genre": "Hip-Hop, Trap", "mood": "Melodic, trap, varied", "style": "Atlanta trap pioneer, melodic auto-tune", "vocal_style": "Future, melodic auto-tune, distinctive, varied", "instruments": "Trap 808s, modern samples", "production": "Modern trap polish, melodic, varied"},
    "21 savage": {"genre": "Hip-Hop, Trap", "mood": "Dark, melodic, modern", "style": "Modern dark trap, melodic", "vocal_style": "21 Savage, deadpan, melodic, distinctive", "instruments": "Dark trap 808s, modern samples", "production": "Dark trap polish, melodic, layered"},
    "kendrick lamar alt": {"genre": "Hip-Hop, Jazz Rap", "mood": "Introspective, urgent, complex", "style": "Lyrically dense, socially conscious", "vocal_style": "Kendrick, versatile, rapid-fire, melodic", "instruments": "Jazz samples, live instruments", "production": "Layered, organic, sophisticated"},
    "earl sweatshirt": {"genre": "Hip-Hop, Alternative", "mood": "Introspective, abstract, alternative", "style": "Odd Future alum, abstract introspective hip-hop", "vocal_style": "Earl Sweatshirt, abstract, raw, introspective", "instruments": "Lo-fi samples, abstract production", "production": "Lo-fi abstract hip-hop, layered, varied"},

    # === R&B (top-up to 25) ===
    "alicia keys": {"genre": "R&B, Soul", "mood": "Soulful, powerful, authentic", "style": "Modern soul-R&B, piano-driven", "vocal_style": "Alicia Keys, powerful soulful soprano, dynamic", "instruments": "Piano, full R&B band, strings", "production": "Modern soul-R&B polish, piano-driven, layered"},
    "usher": {"genre": "R&B", "mood": "Smooth, seductive, modern", "style": "Modern R&B, smooth and seductive", "vocal_style": "Usher, smooth falsetto, dynamic", "instruments": "Smooth R&B production, layered synths", "production": "Modern R&B polish, smooth, layered"},
    "chris brown": {"genre": "R&B, Pop", "mood": "Energetic, varied, modern", "style": "Modern R&B-pop, dance and vocal versatility", "vocal_style": "Chris Brown, versatile, dynamic, distinctive", "instruments": "R&B production, varied", "production": "Modern R&B-pop polish, varied, layered"},
    "ne yo": {"genre": "R&B", "mood": "Smooth, romantic, modern", "style": "Modern R&B, smooth songwriter", "vocal_style": "Ne-Yo, smooth, distinctive, dynamic", "instruments": "Smooth R&B production, layered synths", "production": "Modern R&B polish, smooth, layered"},
    "the weeknd alt": {"genre": "R&B, Synthwave", "mood": "Dark, mysterious, seductive", "style": "80s inspired, atmospheric", "vocal_style": "The Weeknd, falsetto, smooth, emotional", "instruments": "Synths, 808s, pads", "production": "Atmospheric, retro-futuristic"},
    "frank ocean alt": {"genre": "R&B, Alternative", "mood": "Dreamy, melancholic, intimate", "style": "Introspective, experimental", "vocal_style": "Frank Ocean, breathy, understated, falsetto", "instruments": "Sparse synths, guitars", "production": "Minimal, atmospheric, hazy"},
    "chloe x halle": {"genre": "R&B", "mood": "Soulful, ethereal, modern", "style": "Modern R&B duo, ethereal harmonies", "vocal_style": "Chloe x Halle, ethereal harmonies, soulful", "instruments": "R&B production, layered synths, live instruments", "production": "Modern R&B polish, ethereal, layered"},
    "brandy": {"genre": "R&B", "mood": "Soulful, 90s, smooth", "style": "90s R&B pioneer, smooth", "vocal_style": "Brandy, distinctive soprano, soulful, smooth", "instruments": "90s R&B production, live instruments", "production": "90s R&B polish, smooth, layered"},
    "monica": {"genre": "R&B", "mood": "Soulful, 90s, smooth", "style": "90s R&B, smooth and soulful", "vocal_style": "Monica, soulful soprano, dynamic", "instruments": "90s R&B production, live instruments", "production": "90s R&B polish, smooth, layered"},
    "mary j blige": {"genre": "R&B, Soul", "mood": "Powerful, raw, soulful", "style": "Queen of Hip-Hop Soul, raw and powerful", "vocal_style": "Mary J. Blige, powerful, raw, distinctive", "instruments": "Soul samples, live instruments, hip-hop drums", "production": "Hip-hop soul polish, raw, layered"},
    "erykah badu": {"genre": "R&B, Neo-Soul", "mood": "Spiritual, eclectic, alternative", "style": "Neo-soul pioneer, eclectic and spiritual", "vocal_style": "Erykah Badu, distinctive, spiritual, varied", "instruments": "Lo-fi soul samples, live instruments", "production": "Neo-soul polish, lo-fi, eclectic"},
    "d angelo": {"genre": "R&B, Neo-Soul", "mood": "Spiritual, funky, organic", "style": "Neo-soul pioneer, organic funk-soul", "vocal_style": "D'Angelo, falsetto, distinctive, soulful", "instruments": "Funky live band, organic production", "production": "Organic neo-soul polish, funky, layered"},
    "jill scott": {"genre": "R&B, Neo-Soul", "mood": "Soulful, jazzy, neo-soul", "style": "Neo-soul pioneer, jazzy and soulful", "vocal_style": "Jill Scott, rich alto, soulful, distinctive", "instruments": "Live neo-soul band, jazzy instrumentation", "production": "Neo-soul polish, jazzy, organic"},
    "mos def": {"genre": "R&B, Hip-Hop", "mood": "Conscious, soulful, varied", "style": "Black Star alum, conscious hip-hop soul", "vocal_style": "Mos Def, soulful, dynamic, varied", "instruments": "Soul samples, live instruments", "production": "Conscious hip-hop polish, soulful, layered"},
    "jhené aiko": {"genre": "R&B", "mood": "Ethereal, dreamy, modern", "style": "Modern ethereal R&B, dreamy", "vocal_style": "Jhené Aiko, ethereal soprano, dreamy, soulful", "instruments": "Ethereal R&B production, layered synths", "production": "Ethereal R&B polish, dreamy, layered"},
    "kehlani": {"genre": "R&B", "mood": "Soulful, vulnerable, modern", "style": "Modern R&B, vulnerable and soulful", "vocal_style": "Kehlani, soulful alto, vulnerable, dynamic", "instruments": "Modern R&B production, layered synths", "production": "Modern R&B polish, vulnerable, layered"},
    "summer walker": {"genre": "R&B", "mood": "Vulnerable, modern, atmospheric", "style": "Modern atmospheric R&B, vulnerable", "vocal_style": "Summer Walker, vulnerable soprano, atmospheric", "instruments": "Atmospheric R&B production, layered", "production": "Atmospheric R&B polish, vulnerable, layered"},
    "h.e.r.": {"genre": "R&B", "mood": "Soulful, versatile, modern", "style": "Modern R&B, multi-instrumentalist, versatile", "vocal_style": "H.E.R., soulful, versatile, dynamic", "instruments": "Guitar, layered R&B production, varied", "production": "Modern R&B polish, versatile, layered"},
    "janet jackson": {"genre": "R&B, Pop", "mood": "Disciplined, rhythmic, pop", "style": "Pop-R&B dance pioneer, rhythmic", "vocal_style": "Janet Jackson, distinctive, rhythmic, dynamic", "instruments": "Pop-R&B production, layered synths, dance beats", "production": "Pop-R&B polish, rhythmic, layered"},
    "en vogue": {"genre": "R&B", "mood": "Soulful, 90s, group harmonies", "style": "90s R&B vocal group, harmonies", "vocal_style": "Four-part harmonies, soulful, dynamic", "instruments": "90s R&B production, live instruments", "production": "90s R&B polish, harmonies, layered"},

    # === Electronic (top-up to 25) ===
    "daft punk": {"genre": "Electronic, House", "mood": "Upbeat, groovy, nostalgic", "style": "Robotic vocals, funk", "vocal_style": "Robotic vocoder, processed", "instruments": "Synthesizers, drum machines", "production": "Polished, compressed, disco"},
    "aphex twin": {"genre": "Electronic, IDM", "mood": "Mysterious, complex, experimental", "style": "Avant-garde, intricate beats", "vocal_style": "Minimal, processed, occasional", "instruments": "Synthesizers, drum machines", "production": "Complex, detailed, experimental"},
    "deadmau5": {"genre": "Electronic, Progressive House", "mood": "Energetic, epic, driving", "style": "Build-ups, drops, melodic", "vocal_style": "Minimal vocals, occasional", "instruments": "Synthesizers, heavy bass", "production": "Clean, detailed, powerful"},
    "fred again..": {"genre": "Electronic, UK Garage", "mood": "Emotional, euphoric, heartfelt", "style": "Sample-heavy, chopped vocals", "vocal_style": "Processed samples, emotive", "instruments": "Synths, garage beats, samples", "production": "Warm, nostalgic, dynamic"},
    "calvin harris": {"genre": "Electronic, House, Pop EDM", "mood": "Uplifting, summery, euphoric", "style": "Festival anthems, catchy hooks", "vocal_style": "Clean, melodic, often featuring big singers", "instruments": "Synths, punchy drums, basslines", "production": "Polished, radio-ready, massive drops"},
    "skrillex": {"genre": "Electronic, Dubstep, Bass House", "mood": "Aggressive, chaotic, high-energy", "style": "Genre-blending bass drops, experimental", "vocal_style": "Processed, chopped, intense", "instruments": "Heavy wubs, synth stabs, 808s", "production": "Distorted, futuristic, glitchy"},
    "tiësto": {"genre": "Trance, Progressive House, EDM", "mood": "Epic, emotional, arena-sized", "style": "Uplifting builds, melodic trance roots", "vocal_style": "Soaring, anthemic vocals", "instruments": "Big synth leads, driving kicks", "production": "Stadium-filling, layered, euphoric"},
    "john summit": {"genre": "Tech House, House", "mood": "Groovy, dark, clubby", "style": "Driving basslines, vocal chops", "vocal_style": "Processed, repetitive hooks", "instruments": "Rolling bass, percussive elements", "production": "Minimal yet punchy, underground polish"},
    "dom dolla": {"genre": "Tech House, Bass House", "mood": "Funky, energetic, party-starting", "style": "Heavy grooves, sample flips", "vocal_style": "Chopped, energetic", "instruments": "Thick bass, funky synths", "production": "Clean, bouncy, festival-ready"},
    "anyma": {"genre": "Melodic Techno", "mood": "Cinematic, atmospheric, immersive", "style": "Emotional builds, orchestral elements", "vocal_style": "Ethereal, processed", "instruments": "Deep synth pads, melodic arps", "production": "High-end, visual-heavy, Afterlife aesthetic"},
    "ninajirachi": {"genre": "Electronic, Hyperpop, Future Bass", "mood": "Playful, futuristic, vibrant", "style": "Glitchy, colorful sound design", "vocal_style": "Chopped, high-energy", "instruments": "Bright synths, fast percussion", "production": "Experimental, polished chaos"},
    "nitepunk": {"genre": "Bass House, Riddim, Electronic", "mood": "Aggressive, heavy, mosh-pit", "style": "Filthy drops, hybrid bass", "vocal_style": "Growly, distorted", "instruments": "Massive 808s, wobbly synths", "production": "Hard-hitting, festival-destroying"},
    "sara de warren": {"genre": "Melodic House, Progressive", "mood": "Dreamy, emotional, uplifting", "style": "Melodic journeys, vocal-driven", "vocal_style": "Ethereal, soaring", "instruments": "Atmospheric pads, driving bass", "production": "Cinematic, warm, progressive builds"},
    "disco lines": {"genre": "Electronic, House, Disco House", "mood": "Fun, nostalgic, dancefloor-ready", "style": "Sample-heavy disco revivals", "vocal_style": "Chopped, upbeat", "instruments": "Funky bass, retro synths", "production": "Bright, feel-good, viral-friendly"},
    
    # === Metal ===
    "metallica": {"genre": "Metal, Thrash", "mood": "Intense, angry, dark", "style": "Aggressive, fast riffs", "vocal_style": "Aggressive, shouting, growling", "instruments": "Heavy guitar, fast drums", "production": "Heavy, compressed, raw"},
    "tool": {"genre": "Progressive Metal", "mood": "Dark, mystical, complex", "style": "Odd time signatures, heavy", "vocal_style": "Powerful, emotional, screaming", "instruments": "Heavy guitar, complex drums", "production": "Layered, atmospheric, heavy"},

    # === Doom Metal (heavy section — anchors for Iron Vespers sound) ===
    "candlemass": {"genre": "Doom Metal, Epic Doom", "mood": "Funereal, epic, mournful", "style": "Slow, crushing riffs, operatic vocals", "vocal_style": "Clean operatic tenor, Messiah Marcolin style", "instruments": "Heavy distorted guitar, slow drums, organ", "production": "Reverb-heavy, cathedral-like, thick low end"},
    "saint vitus": {"genre": "Doom Metal, Traditional Doom", "mood": "Sluggish, heavy, despairing", "style": "Ponderous, Sabbath-influenced riffs", "vocal_style": "Wailing, raw, Scott Reagers style", "instruments": "Massive downtuned guitar, slow bass, simple drums", "production": "Raw, analog, cavernous"},
    "pentagram": {"genre": "Doom Metal, Heavy Metal", "mood": "Dark, occult, defiant", "style": "Classic doom with hard rock swagger", "vocal_style": "Bobby Liebling style, raw charismatic", "instruments": "Sabbath-style riffs, fuzz bass, steady drums", "production": "Vintage analog, gritty, warm"},
    "my dying bride": {"genre": "Doom Metal, Gothic Doom, Death Doom", "mood": "Melancholic, romantic, devastating", "style": "Violin-led gothic doom, crushing beauty", "vocal_style": "Aaron Stainthorpe, clean baritone + death growls", "instruments": "Heavy guitar, lead violin, orchestral strings", "production": "Lush, orchestral, layered grief"},
    "swallow the sun": {"genre": "Doom Metal, Funeral Doom, Melodic Death", "mood": "Funereal, beautiful, hopeless", "style": "Funeral-paced doom with melodic death layers", "vocal_style": "Juha Raivio, clean + harsh, distant and mournful", "instruments": "Massive guitar, piano, strings, slow drums", "production": "Cathedral reverb, glacial pacing, heartbreaking"},
    "electric wizard": {"genre": "Doom Metal, Stoner Doom, Drone", "mood": "Psychedelic, oppressive, fuzzed-out", "style": "Sludgy, repetitive, monolithic riffs", "vocal_style": "Liz Buckingham / Jus Oborn, distorted, hypnotic", "instruments": "Massive fuzz guitar, bass, slow drums, synth drone", "production": "Bottom-heavy, blown-out, lysergic"},
    "warning": {"genre": "Doom Metal, Epic Doom", "mood": "Cathartic, emotional, weighty", "style": "Long-form builds, epic dynamic arcs", "vocal_style": "Patrick Walker, raw, cracked, desperate", "instruments": "Crushing guitar, minimalist drums, bass", "production": "Live feel, dynamic, honest weight"},
    "40 watt sun": {"genre": "Doom Metal, Atmospheric Doom", "mood": "Bare, intimate, anguished", "style": "Stripped-down emotional doom", "vocal_style": "Patrick Walker, fragile, exposed, quivering", "instruments": "Single guitar, voice-forward", "production": "Sparse, dry, devastating intimacy"},
    "yob": {"genre": "Doom Metal, Stoner Doom", "mood": "Transcendent, cosmic, heavy", "style": "Long builds, spiritual heaviness", "vocal_style": "Mike Scheidt, soaring clean, emotional", "instruments": "Massive fuzz guitar, bass, dynamic drums", "production": "Huge, warm, psychedelic transcendence"},
    "conan": {"genre": "Doom Metal, Sludge", "mood": "Brutal, primitive, crushing", "style": "Low-tuned monolithic riffs", "vocal_style": "Jon Davis, guttural shouts over noise", "instruments": "Downtuned guitar, bass, slow drums", "production": "Cave-recorded, oppressive low end"},
    "windhand": {"genre": "Doom Metal, Occult Doom", "mood": "Hypnotic, dark, atmospheric", "style": "Repetitive hypnotic doom, occult undertones", "vocal_style": "Dorthia Cottrell, ethereal, ghostly female vocals", "instruments": "Massive guitar, slow bass, minimal drums", "production": "Dense, foggy, ritualistic"},

    # === Christian Metal / Christian Doom ===
    "demon hunter": {"genre": "Christian Metal, Metalcore", "mood": "Aggressive, anthemic, defiant", "style": "Faith-forward metalcore, twin-guitar leads", "vocal_style": "Ryan Clark, screams + clean, intense", "instruments": "Heavy guitar, double-kick drums, melodic leads", "production": "Polished metalcore, punchy and huge"},
    "august burns red": {"genre": "Christian Metal, Metalcore", "mood": "Anthemic, soaring, triumphant", "style": "Virtuosic metalcore, faith themes", "vocal_style": "Jake Luhrs, screams + clean harmonies", "instruments": "Technical guitar, blast beats, melodic breakdowns", "production": "Crisp, modern, big-room metalcore"},
    "wolves at the gate": {"genre": "Christian Metal, Metalcore, Post-Hardcore", "mood": "Hopeful, fierce, worshipful", "style": "Faith-driven heavy music, anthemic choruses", "vocal_style": "Steve Cobucci, screams + cleans, emotional", "instruments": "Heavy guitar, driving drums, synth layers", "production": "Modern, dynamic, cinematic heavy"},
    "zion forever": {"genre": "Christian Doom, Sludge", "mood": "Funereal, weighty, sacred", "style": "Slow crushing doom with Christian themes", "vocal_style": "Low guttural + clean calls, monastic weight", "instruments": "Massive downtuned guitar, slow drums, organ drone", "production": "Cathedral reverb, monolithic low end"},
    "the chariot": {"genre": "Christian Metal, Hardcore, Noise", "mood": "Chaotic, intense, raw", "style": "Noise-influenced faith hardcore", "vocal_style": "Josh Scogin, raw screams, manic energy", "instruments": "Tape loops, noise, heavy riffs, drums", "production": "Lo-fi chaos, blown-out, urgent"},
    "saint asonia": {"genre": "Christian Hard Rock, Post-Grunge", "mood": "Heavy, melodic, personal", "style": "Adam Gontier-era faith-tinged hard rock", "vocal_style": "Adam Gontier, raw + melodic, husky", "instruments": "Big riffs, melodic leads, driving drums", "production": "Modern rock polish, huge choruses"},
    "haste the day": {"genre": "Christian Metalcore, Metalcore", "mood": "Intense, worshipful, urgent", "style": "Faith-driven metalcore, anthemic builds", "vocal_style": "Stephen Keech, screams + clean, dynamic", "instruments": "Heavy guitar, double bass, breakdowns", "production": "Punchy, modern, dynamic"},
    "war of ages": {"genre": "Christian Metal, Metalcore", "mood": "Triumphant, fierce, hopeful", "style": "Anthemic Christian metalcore", "vocal_style": "Leroy Hamp, screams + clean, powerful", "instruments": "Heavy guitar, driving drums, melodic leads", "production": "Bright, modern, big choruses"},
    "for today": {"genre": "Christian Metal, Metalcore, Groove", "mood": "Heavy, aggressive, declarative", "style": "Groove-laden faith metalcore", "vocal_style": "Mattie Montgomery, screams + barks, intense", "instruments": "Down-tuned guitar, groove drums, heavy bass", "production": "Modern metalcore, tight low end"},
    "phinehas": {"genre": "Christian Metal, Metalcore, Progressive", "mood": "Intense, dynamic, faith-forward", "style": "Progressive metalcore with Christian lyrics", "vocal_style": "Sean McCulloch, screams + cleans, dynamic range", "instruments": "Technical guitar, complex drums, atmospheric synths", "production": "Modern, layered, dynamic heavy"},
    "silent planet": {"genre": "Christian Metal, Progressive Metalcore", "mood": "Atmospheric, intense, cerebral", "style": "Progressive atmospheric metalcore with faith themes", "vocal_style": "Garrett Russell, varied screams + clean, artful", "instruments": "Complex guitar, atmospheric synths, dynamic drums", "production": "Dense, atmospheric, layered"},
    "extol": {"genre": "Christian Metal, Progressive Extreme Metal", "mood": "Intense, progressive, varied", "style": "Norwegian Christian extreme metal, technically rich", "vocal_style": "Peter Espevoll, varied screams + cleans", "instruments": "Complex guitar, varied tempos, orchestral touches", "production": "Dense, progressive, dynamic"},
    "bloodgood": {"genre": "Christian Metal, Heavy Metal", "mood": "Triumphant, classic, faith-forward", "style": "Classic 80s Christian heavy metal", "vocal_style": "Les Carlsen, classic metal tenor", "instruments": "Classic metal guitar, bass, drums", "production": "Vintage 80s metal, big arena sound"},
    "petra": {"genre": "Christian Rock, Classic Christian Rock", "mood": "Uplifting, anthemic, classic", "style": "Classic Christian arena rock", "vocal_style": "Greg X. Volz / John Schlitt, classic rock tenor", "instruments": "Classic rock guitar, keys, drums", "production": "80s rock polish, anthemic choruses"},
    "iron vespers": {"genre": "Doom Metal, Christian Doom", "mood": "Funereal, defiant, sacred", "style": "Crushing slow doom with Christian defiance, wolf and highlands imagery", "vocal_style": "Low baritone leads, raw and weighty, occasional Gregorian-style backing", "instruments": "Massive downtuned guitar, slow funereal drums, organ drone, low brass swells", "production": "Cathedral reverb, monolithic low end, chiaroscuro mix — never anthemic, always crushing"},

    # === Metal (heavy / thrash / groove / progressive / power / death / black / folk) — anchored artists ===
    "black sabbath": {"genre": "Metal, Heavy Metal", "mood": "Dark, heavy, foundational", "style": "The blueprint for heavy metal, crushing riffs", "vocal_style": "Ozzy Osbourne, plaintive wail, iconic", "instruments": "Downtuned guitar, bass, drums, Iommi riffs", "production": "Raw 70s analog, towering low end, foundational heavy"},
    "iron maiden": {"genre": "Metal, Heavy Metal", "mood": "Epic, galloping, triumphant", "style": "NWOBHM gallop, twin-guitar harmony leads", "vocal_style": "Bruce Dickinson, operatic British tenor", "instruments": "Twin lead guitars, galloping bass, thunderous drums", "production": "Massive, layered, classic metal polish"},
    "judas priest": {"genre": "Metal, Heavy Metal", "mood": "Aggressive, leather-clad, anthemic", "style": "Twin-lead metal, leather and studs attack", "vocal_style": "Rob Halford, high metal scream, commanding", "instruments": "Twin lead guitars, driving bass, pounding drums", "production": "Sharp, polished, 80s metal sheen"},
    "megadeth": {"genre": "Metal, Thrash", "mood": "Brutal, technical, biting", "style": "Thrash with virtuosic guitar, complex arrangements", "vocal_style": "Dave Mustaine, snarling, aggressive baritone", "instruments": "Technical thrash guitar, rapid-fire drums, intricate bass", "production": "Tight, technical, thrash polish"},
    "slayer": {"genre": "Metal, Thrash", "mood": "Satanic, vicious, relentless", "style": "Extreme thrash, fast and ferocious", "vocal_style": "Tom Araya, throat-shredding shouts", "instruments": "Blazing thrash riffs, blast beats, dark solos", "production": "Raw, vicious, thrash to the bone"},
    "anthrax": {"genre": "Metal, Thrash", "mood": "Energetic, fun, anthemic", "style": "Fun thrash with crossover appeal", "vocal_style": "Joey Belladonna / Scott Ian trade-offs, shouty and clean", "instruments": "Thrash riffs, gang vocals, driving drums", "production": "Bright, punchy, crossover-ready"},
    "pantera": {"genre": "Metal, Groove", "mood": "Brutal, swaggering, crushing", "style": "Groove metal, post-thrash heaviness", "vocal_style": "Phil Anselmo, guttural shouts, raw", "instruments": "Down-tuned groove riffs, crushing bass, double-kick", "production": "Heavy, mid-down tuned, tight low end"},
    "lamb of god": {"genre": "Metal, Groove", "mood": "Brutal, modern, aggressive", "style": "Modern groove metal, American heaviness", "vocal_style": "Randy Blythe, snarling shouts, intense", "instruments": "Down-tuned groove riffs, syncopated drums", "production": "Punchy, modern, tight low end"},
    "mastodon": {"genre": "Metal, Progressive", "mood": "Epic, progressive, vast", "style": "Progressive sludge metal, concept albums", "vocal_style": "Troy Sanders / Brent Hinds, clean and harsh", "instruments": "Complex guitar, dynamic drums, bass", "production": "Layered, cinematic, progressive heavy"},
    "gojira": {"genre": "Metal, Progressive", "mood": "Primal, technical, environmental", "style": "Technical progressive death-groove, eco-themes", "vocal_style": "Joe Duplantier, deep growls + clean shouts", "instruments": "Technical down-tuned riffs, polyrhythmic drums", "production": "Massive, modern, technical precision"},
    "meshuggah": {"genre": "Metal, Progressive, Djent", "mood": "Mechanical, hypnotic, technical", "style": "Djent pioneers, polyrhythmic chaos", "vocal_style": "Jens Kidman, robotic shouts over polyrhythms", "instruments": "Downtuned 8-string guitar, polyrhythmic drums", "production": "Cold, mechanical, ultra-precise"},
    "periphery": {"genre": "Metal, Progressive, Djent", "mood": "Technical, melodic, modern", "style": "Djent with melodic hooks, modern prog", "vocal_style": "Spencer Sotelo, soaring cleans + screams", "instruments": "8-string djent guitar, synth textures, dynamic drums", "production": "Polished djent, melodic, modern mix"},
    "helloween": {"genre": "Metal, Power", "mood": "Triumphant, melodic, fast", "style": "German power metal, speed metal roots", "vocal_style": "Kai Hansen / Michael Kiske, soaring operatic", "instruments": "Speed metal riffs, harmonized leads, fast drums", "production": "Bright, fast, classic power metal"},
    "blind guardian": {"genre": "Metal, Power", "mood": "Epic, fantasy, symphonic", "style": "Symphonic power metal, fantasy epics", "vocal_style": "Hansi Kürsch, soaring dramatic tenor", "instruments": "Layered guitars, orchestral synths, double-kick", "production": "Massive, orchestral, operatic power"},
    "stratovarius": {"genre": "Metal, Power", "mood": "Melodic, soaring, anthemic", "style": "Finnish power metal, neoclassical leads", "vocal_style": "Timo Kotipelto, soaring clean tenor", "instruments": "Neoclassical guitar, soaring keys, fast drums", "production": "Bright, polished, neoclassical power"},
    "kamelot": {"genre": "Metal, Power", "mood": "Theatrical, dramatic, symphonic", "style": "Symphonic power metal with theatrical concepts", "vocal_style": "Roy Khan / Tommy Karevic, dramatic baritone/tenor", "instruments": "Symphonic guitar, orchestral keys, dynamic drums", "production": "Cinematic, theatrical, polished symphonic"},
    "testament": {"genre": "Metal, Thrash", "mood": "Bay Area thrash, technical, ferocious", "style": "Bay Area thrash, virtuoso guitar work", "vocal_style": "Chuck Billy, aggressive thrash bark", "instruments": "Technical thrash guitar, complex bass, fast drums", "production": "Sharp, technical, Bay Area polish"},
    "kreator": {"genre": "Metal, Thrash", "mood": "German thrash, relentless, extreme", "style": "Teutonic thrash, extreme and dark", "vocal_style": "Mille Petrozza, snarling German thrash", "instruments": "Blazing thrash riffs, pounding bass, blast beats", "production": "Vicious, German thrash, tight and brutal"},
    "opeth": {"genre": "Metal, Progressive, Death", "mood": "Dark, progressive, atmospheric", "style": "Progressive death with folk and jazz influence", "vocal_style": "Mikael Åkerfeldt, clean + death growl, dynamic", "instruments": "Acoustic + electric guitar, complex arrangements, keys", "production": "Layered, dynamic, progressive depth"},
    "in flames": {"genre": "Metal, Melodic Death", "mood": "Melodic, melancholic, Swedish", "style": "Swedish melodic death, Gothenburg sound", "vocal_style": "Anders Fridén, melodic harsh + clean", "instruments": "Melodic death riffs, harmonized leads, double-kick", "production": "Bright melodic death, polished Swedish sound"},
    "dark tranquillity": {"genre": "Metal, Melodic Death", "mood": "Atmospheric, melodic, futuristic", "style": "Atmospheric melodic death, synth-driven", "vocal_style": "Mikael Stanne, harsh + clean, melodic", "instruments": "Melodic death riffs, atmospheric synths, dynamic drums", "production": "Atmospheric, layered, melodic death polish"},
    "at the gates": {"genre": "Metal, Melodic Death", "mood": "Brutal, melodic, pioneering", "style": "Pioneers of Gothenburg melodic death", "vocal_style": "Tomas Lindberg, snarling shouts, melodic", "instruments": "Melodic death riffs, blast beats, twin leads", "production": "Sharp, melodic, pioneering Swedish death"},
    "amon amarth": {"genre": "Metal, Melodic Death", "mood": "Epic, Viking, crushing", "style": "Viking-themed melodic death, epic battles", "vocal_style": "Johan Hegg, deep death growl, commanding", "instruments": "Massive melodic death riffs, double-kick, epic leads", "production": "Massive, epic, Viking metal polish"},
    "dimmu borgir": {"genre": "Metal, Symphonic Black", "mood": "Dark, theatrical, symphonic", "style": "Symphonic black metal, orchestral heavy", "vocal_style": "Shagrath, rasping black metal shriek", "instruments": "Massive symphonic black riffs, full orchestra, blast beats", "production": "Cinematic, orchestral, symphonic black"},
    "mayhem": {"genre": "Metal, Black", "mood": "Satanic, raw, foundational", "style": "Foundational Norwegian black metal, raw attack", "vocal_style": "Dead / Attila, raw black metal shriek", "instruments": "Raw tremolo riffs, blast beats, dissonant leads", "production": "Lo-fi raw, intentionally abrasive, classic BM"},
    "emperor": {"genre": "Metal, Symphonic Black", "mood": "Majestic, dark, symphonic", "style": "Symphonic black metal, neoclassical grandeur", "vocal_style": "Ihsahn, shriek + clean, dramatic", "instruments": "Symphonic black riffs, keys/synths, blast beats", "production": "Grand, symphonic, neoclassical black"},
    "burzum": {"genre": "Metal, Black", "mood": "Atmospheric, dark, minimalist", "style": "Lo-fi atmospheric black metal, one-man project", "vocal_style": "Varg Vikernes, raw shriek, distant", "instruments": "Lo-fi tremolo guitar, repetitive drums, synth", "production": "Lo-fi, atmospheric, intentionally raw"},
    "enslaved": {"genre": "Metal, Progressive Black", "mood": "Progressive, atmospheric, Norse", "style": "Progressive black metal with psychedelic elements", "vocal_style": "Grutle Kjellson, clean + harsh, dynamic", "instruments": "Progressive black riffs, keys, dynamic drums", "production": "Layered, progressive, atmospheric black"},
    "watain": {"genre": "Metal, Black", "mood": "Occult, raw, ritualistic", "style": "Swedish black metal with occult themes", "vocal_style": "Erik Danielsson, snarl, intense", "instruments": "Raw black metal riffs, blast beats, dark leads", "production": "Raw, occult, intentionally abrasive"},
    "children of bodom": {"genre": "Metal, Melodic Death, Power", "mood": "Melodic, neoclassical, intense", "style": "Finnish melodic death with neoclassical shred", "vocal_style": "Alexi Laiho, harsh + clean, operatic", "instruments": "Neoclassical shred, melodic death riffs, keys", "production": "Bright, technical, Finnish melodic death"},
    "arch enemy": {"genre": "Metal, Melodic Death", "mood": "Fierce, melodic, modern", "style": "Modern melodic death, virtuosic lead guitar", "vocal_style": "Angela Gossow / Alissa White-Gluz, death growl, dynamic", "instruments": "Melodic death riffs, virtuoso leads, fast drums", "production": "Sharp, modern, melodic death polish"},
    "soilwork": {"genre": "Metal, Melodic Death", "mood": "Modern, melodic, Swedish", "style": "Modern Swedish melodic death, groove-influenced", "vocal_style": "Björn 'Speed' Strid, clean + harsh, melodic", "instruments": "Modern melodic death riffs, groove, synth textures", "production": "Modern, melodic, polished Swedish death"},
    "sepultura": {"genre": "Metal, Groove, Thrash", "mood": "Brutal, tribal, modern", "style": "Brazilian groove-thrash, tribal elements", "vocal_style": "Derrick Green / Max Cavalera, snarl and bark", "instruments": "Groove-thrash riffs, tribal percussion, heavy bass", "production": "Tribal, heavy, Brazilian groove polish"},
    "machine head": {"genre": "Metal, Groove, Thrash", "mood": "Aggressive, modern, dark", "style": "Modern groove-thrash, post-pantera heaviness", "vocal_style": "Robb Flynn, snarl + melodic, intense", "instruments": "Down-tuned groove riffs, crushing bass, fast drums", "production": "Heavy, modern, groove-thrash polish"},
    "death": {"genre": "Metal, Death", "mood": "Technical, brutal, pioneering", "style": "Foundational technical death metal, Chuck Schuldiner", "vocal_style": "Chuck Schuldiner, pioneering death growl", "instruments": "Technical death riffs, complex bass, blast beats", "production": "Sharp, technical, pioneering death"},
    "cannibal corpse": {"genre": "Metal, Death", "mood": "Brutal, extreme, gory", "style": "Brutal slam death, lyrical extremity", "vocal_style": "George 'Corpsegrinder' Fisher, guttural growl", "instruments": "Brutal death riffs, blast beats, slam riffs", "production": "Brutal, tight, American death"},
    "morbid angel": {"genre": "Metal, Death", "mood": "Dark, technical, occult", "style": "Technical death, occult themes, Trey Azagthoth leads", "vocal_style": "David Vincent / Steve Tucker, death growl", "instruments": "Technical death riffs, chaotic solos, blast beats", "production": "Dark, technical, classic Florida death"},
    "behemoth": {"genre": "Metal, Black, Death", "mood": "Occult, theatrical, extreme", "style": "Polish blackened death, occult theatrics", "vocal_style": "Nergal, snarl + clean chants, commanding", "instruments": "Blackened death riffs, blast beats, dark leads", "production": "Massive, theatrical, blackened death polish"},
    "ghost": {"genre": "Metal, Heavy Metal", "mood": "Occult, melodic, anthemic", "style": "Swedish occult rock, Satanic pop-metal", "vocal_style": "Tobias Forge, dynamic clean + croon, theatrical", "instruments": "Heavy riffs, retro keys, big choruses", "production": "Massive, retro, anthemic occult rock"},

    # === Metalcore (modern + classic) — full coverage ===
    "parkway drive": {"genre": "Metalcore", "mood": "Anthemic, fierce, Australian", "style": "Australian metalcore, anthemic breakdowns", "vocal_style": "Winston McCall, screams + clean shouts, intense", "instruments": "Heavy guitar, double-kick, big choruses", "production": "Big-room metalcore, punchy, anthemic"},
    "architects": {"genre": "Metalcore", "mood": "Heavy, emotional, modern British", "style": "British metalcore, modern and emotional", "vocal_style": "Sam Carter, screams + soaring cleans, dynamic", "instruments": "Down-tuned metalcore guitar, atmospheric synths", "production": "Polished modern metalcore, dynamic, huge"},
    "bring me the horizon": {"genre": "Metalcore, Post-Hardcore", "mood": "Experimental, electronic, evolving", "style": "Pioneers of metalcore-to-electronic evolution", "vocal_style": "Oli Sykes, screams + clean, versatile", "instruments": "Metalcore riffs, electronic production, synths", "production": "Experimental, electronic, modern metalcore"},
    "asking alexandria": {"genre": "Metalcore, Post-Hardcore", "mood": "Aggressive, electronic, modern", "style": "Electronic metalcore, modern post-hardcore", "vocal_style": "Danny Worsnop, screams + cleans, dynamic", "instruments": "Down-tuned guitar, electronic synths, big drums", "production": "Electronic, polished, modern metalcore"},
    "of mice and men": {"genre": "Metalcore, Post-Hardcore", "mood": "Heavy, melodic, dynamic", "style": "Modern metalcore, dynamic clean/scream contrast", "vocal_style": "Austin Carlile, screams + cleans, emotional", "instruments": "Down-tuned guitar, dynamic drums, melodic leads", "production": "Modern, dynamic, polished metalcore"},
    "pierce the veil": {"genre": "Metalcore, Post-Hardcore", "mood": "Emotional, dramatic, theatrical", "style": "Theatrical post-hardcore, emotional storytelling", "vocal_style": "Vic Fuentes, dynamic screams + cleans, dramatic", "instruments": "Post-hardcore riffs, dynamic drums, atmospheric layers", "production": "Dramatic, emotional, polished post-hardcore"},
    "a day to remember": {"genre": "Metalcore, Pop Punk", "mood": "Fun, anthemic, pop-metal fusion", "style": "Pop-punk-meets-metalcore crossover", "vocal_style": "Jeremy McKinnon, screams + pop-punk cleans, catchy", "instruments": "Metalcore riffs, pop-punk leads, big choruses", "production": "Pop-metal polish, anthemic, catchy"},
    "the word alive": {"genre": "Metalcore, Post-Hardcore", "mood": "Heavy, melodic, modern", "style": "Modern metalcore, melodic dynamic", "vocal_style": "Telle Smith, soaring cleans + screams, dynamic", "instruments": "Modern metalcore guitar, synth layers, big drums", "production": "Modern, melodic, polished metalcore"},
    "blessthefall": {"genre": "Metalcore, Post-Hardcore", "mood": "Anthemic, melodic, modern", "style": "Anthemic post-hardcore, modern metalcore", "vocal_style": "Beau Bokan, clean + screams, dynamic", "instruments": "Post-hardcore riffs, synth layers, big drums", "production": "Polished, anthemic, modern metalcore"},
    "underoath": {"genre": "Metalcore, Post-Hardcore", "mood": "Dark, atmospheric, intense", "style": "Atmospheric metalcore, post-hardcore intensity", "vocal_style": "Spencer Chamberlain / Aaron Gillespie, screams + cleans, dynamic", "instruments": "Atmospheric metalcore riffs, dynamic drums, synth", "production": "Atmospheric, dark, polished metalcore"},
    "saosin": {"genre": "Metalcore, Post-Hardcore", "mood": "Melodic, emotional, anthemic", "style": "Melodic post-hardcore, anthemic metalcore", "vocal_style": "Anthony Green / Cove Reber, soaring cleans, emotional", "instruments": "Melodic post-hardcore guitar, dynamic drums", "production": "Melodic, emotional, polished post-hardcore"},
    "senses fail": {"genre": "Metalcore, Post-Hardcore", "mood": "Emotional, anthemic, intense", "style": "Emotional post-hardcore, anthemic metalcore", "vocal_style": "Buddy Nielsen, screams + clean, emotional", "instruments": "Post-hardcore riffs, dynamic drums, synth", "production": "Emotional, anthemic, modern metalcore"},
    "memphis may fire": {"genre": "Metalcore, Post-Hardcore", "mood": "Anthemic, modern, dynamic", "style": "Modern metalcore, dynamic clean/scream", "vocal_style": "Matty Mullins, soaring cleans + screams, dynamic", "instruments": "Modern metalcore riffs, synth, big drums", "production": "Modern, anthemic, polished metalcore"},
    "crown the empire": {"genre": "Metalcore, Post-Hardcore", "mood": "Theatrical, modern, epic", "style": "Theatrical modern metalcore, epic scope", "vocal_style": "Andy Leo / David Escamilla, dynamic clean + screams", "instruments": "Theatrical metalcore riffs, synth, big drums", "production": "Cinematic, theatrical, polished modern metalcore"},
    "killswitch engage": {"genre": "Metalcore", "mood": "Heavy, melodic, pioneering", "style": "Pioneering New England metalcore, melodic", "vocal_style": "Jesse Leach / Howard Jones, screams + clean, dynamic", "instruments": "Melodic metalcore riffs, twin leads, heavy drums", "production": "Pioneering, melodic, polished metalcore"},
    "shadows fall": {"genre": "Metalcore", "mood": "Heavy, thrashy, New England", "style": "New England metalcore with thrash edge", "vocal_style": "Brian Fair, screams + clean, dynamic", "instruments": "Thrashy metalcore riffs, dynamic drums, twin leads", "production": "Sharp, heavy, polished New England metalcore"},
    "all that remains": {"genre": "Metalcore", "mood": "Heavy, melodic, modern", "style": "Melodic modern metalcore, anthem-heavy", "vocal_style": "Phil Labonte, clean + screams, melodic", "instruments": "Melodic metalcore riffs, big drums, twin leads", "production": "Modern, melodic, polished metalcore"},
    "as i lay dying": {"genre": "Metalcore", "mood": "Heavy, modern, dynamic", "style": "Modern metalcore, dynamic clean/scream", "vocal_style": "Tim Lambesis, screams + clean, intense", "instruments": "Modern metalcore riffs, dynamic drums, twin leads", "production": "Modern, heavy, polished metalcore"},
    "unearth": {"genre": "Metalcore", "mood": "Heavy, thrashy, New England", "style": "New England metalcore, thrash-influenced", "vocal_style": "Trevor Phipps, screams + clean, intense", "instruments": "Thrashy metalcore riffs, twin leads, dynamic drums", "production": "Sharp, heavy, polished New England metalcore"},
    "trivium": {"genre": "Metalcore, Thrash", "mood": "Technical, modern, heavy", "style": "Modern metalcore with thrash influence, virtuosic", "vocal_style": "Matt Heafy, screams + clean, versatile", "instruments": "Technical metalcore riffs, thrash elements, twin leads", "production": "Technical, modern, polished metalcore-thrash"},
    "bullet for my valentine": {"genre": "Metalcore", "mood": "Heavy, melodic, British", "style": "British metalcore with melodic hooks", "vocal_style": "Matt Tuck, clean + screams, versatile", "instruments": "Melodic metalcore riffs, twin leads, big drums", "production": "Modern, melodic, polished British metalcore"},
    "avenged sevenfold": {"genre": "Metalcore", "mood": "Heavy, theatrical, modern", "style": "Modern metalcore with theatrical scope, heavy", "vocal_style": "M. Shadows, clean + screams, versatile", "instruments": "Theatrical metalcore riffs, twin leads, big drums", "production": "Cinematic, theatrical, polished modern metalcore"},
    "ateens": {"genre": "Metalcore", "mood": "Atmospheric, modern, Swedish", "style": "Modern Swedish metalcore, atmospheric", "vocal_style": "Alex Bengtson / Jimmy Wesslén, screams + clean, dynamic", "instruments": "Atmospheric metalcore riffs, twin leads, dynamic drums", "production": "Atmospheric, modern, polished Swedish metalcore"},
    "dead by april": {"genre": "Metalcore", "mood": "Modern, melodic, Swedish", "style": "Modern Swedish melodic metalcore, atmospheric", "vocal_style": "Jimmie Strimell / Christoffer Andersson, clean + screams, dynamic", "instruments": "Modern melodic metalcore riffs, synth, big drums", "production": "Modern, melodic, polished Swedish metalcore"},
    "the devil wears prada": {"genre": "Metalcore", "mood": "Heavy, modern, dynamic", "style": "Modern Christian-leaning metalcore, dynamic", "vocal_style": "Mike Hranica, screams + clean, intense", "instruments": "Modern metalcore riffs, dynamic drums, twin leads", "production": "Modern, heavy, polished metalcore"},

    # === Modern Heavy (atmospheric / cinematic / modern metalcore / post-metal) — full coverage ===
    "deafheaven": {"genre": "Modern Heavy, Atmospheric Black", "mood": "Ethereal, blackgaze, transcendent", "style": "Atmospheric black metal with shoegaze textures", "vocal_style": "George Clarke, black metal shriek + clean whispers", "instruments": "Wall-of-sound tremolo guitar, shimmering layers, blast beats", "production": "Massive shoegaze-black, cinematic, transcendent"},
    "japanese breakfast": {"genre": "Modern Heavy, Indie", "mood": "Nostalgic, dreamy, modern", "style": "Modern indie with atmospheric heavy leanings", "vocal_style": "Michelle Zauner, dreamy, layered, emotional", "instruments": "Atmospheric guitar, synths, modern indie band", "production": "Dreamy, modern, polished atmospheric"},
    "polyphia": {"genre": "Modern Heavy, Progressive", "mood": "Virtuosic, modern, technical", "style": "Modern progressive, virtuosic guitar, djent-adjacent", "vocal_style": "Often instrumental, occasional featured clean vocalists", "instruments": "Virtuosic guitar, technical bass, dynamic drums", "production": "Polished modern progressive, technical, clean"},
    "blessthefall": {"genre": "Modern Heavy, Metalcore", "mood": "Heavy, melodic, modern", "style": "Modern metalcore, melodic dynamic", "vocal_style": "Beau Bokan, clean + screams, dynamic", "instruments": "Modern metalcore guitar, synth layers, big drums", "production": "Modern, melodic, polished modern heavy"},
    "northlane": {"genre": "Modern Heavy, Metalcore", "mood": "Heavy, progressive, modern", "style": "Australian modern metalcore, progressive, djent-influenced", "vocal_style": "Marcus Bridge, clean + screams, dynamic", "instruments": "Modern metalcore riffs, electronic textures, dynamic drums", "production": "Modern, progressive, polished Australian metalcore"},
    "erton": {"genre": "Modern Heavy, Progressive", "mood": "Atmospheric, modern, progressive", "style": "Modern progressive metalcore, atmospheric", "vocal_style": "Clean + screams, atmospheric, modern", "instruments": "Progressive metalcore riffs, atmospheric synths, dynamic drums", "production": "Atmospheric, modern, polished progressive heavy"},
    "blessthefall alt": {"genre": "Modern Heavy, Post-Hardcore", "mood": "Heavy, melodic, modern", "style": "Modern post-hardcore, melodic heavy", "vocal_style": "Beau Bokan, clean + screams, dynamic", "instruments": "Post-hardcore riffs, synth, big drums", "production": "Modern, melodic, polished post-hardcore"},
    "novelists": {"genre": "Modern Heavy, Progressive Metalcore", "mood": "Atmospheric, progressive, modern", "style": "French modern progressive metalcore, atmospheric", "vocal_style": "Florian Music, clean + harsh, dynamic", "instruments": "Modern metalcore riffs, atmospheric synths, technical drums", "production": "Atmospheric, modern, French progressive metalcore"},
    "crown magnets": {"genre": "Modern Heavy, Metalcore", "mood": "Modern, heavy, dynamic", "style": "Modern metalcore with cinematic edge", "vocal_style": "Clean + screams, dynamic, modern", "instruments": "Modern metalcore riffs, synth, dynamic drums", "production": "Modern, cinematic, polished metalcore"},
    "void of vision": {"genre": "Modern Heavy, Metalcore", "mood": "Heavy, modern, Australian", "style": "Modern Australian metalcore, nu-metal revival", "vocal_style": "Jack Bergin, screams + clean, dynamic", "instruments": "Modern metalcore riffs, electronic, dynamic drums", "production": "Modern, heavy, polished Australian metalcore"},
    "thousand below": {"genre": "Modern Heavy, Metalcore", "mood": "Modern, heavy, melodic", "style": "Modern melodic metalcore, atmospheric", "vocal_style": "James DeBerg, clean + screams, dynamic", "instruments": "Modern metalcore riffs, atmospheric synths, big drums", "production": "Modern, atmospheric, polished metalcore"},
    "dayseeker": {"genre": "Modern Heavy, Post-Hardcore", "mood": "Emotional, atmospheric, modern", "style": "Modern emotional post-hardcore, atmospheric", "vocal_style": "Rory Rodriguez, soaring cleans + screams, dynamic", "instruments": "Post-hardcore riffs, atmospheric synths, dynamic drums", "production": "Atmospheric, emotional, polished post-hardcore"},
    "silent planet alt": {"genre": "Modern Heavy, Progressive Metalcore", "mood": "Atmospheric, intense, cerebral", "style": "Progressive atmospheric metalcore", "vocal_style": "Garrett Russell, varied screams + clean, artful", "instruments": "Complex guitar, atmospheric synths, dynamic drums", "production": "Dense, atmospheric, layered"},
    "blessthefall prime": {"genre": "Modern Heavy, Post-Hardcore", "mood": "Heavy, melodic, modern", "style": "Modern post-hardcore, melodic heavy", "vocal_style": "Beau Bokan, clean + screams, dynamic", "instruments": "Post-hardcore riffs, synth, big drums", "production": "Modern, melodic, polished post-hardcore"},
    "erra": {"genre": "Modern Heavy, Progressive Metalcore", "mood": "Technical, melodic, modern", "style": "Progressive metalcore, technical and melodic", "vocal_style": "JT Cavey, soaring cleans + screams, dynamic", "instruments": "Progressive metalcore riffs, technical drums, synths", "production": "Technical, melodic, polished progressive metalcore"},
    "invent animate": {"genre": "Modern Heavy, Progressive Metalcore", "mood": "Atmospheric, progressive, modern", "style": "Atmospheric progressive metalcore, modern", "vocal_style": "Marcus Vik, clean + screams, dynamic", "instruments": "Progressive metalcore riffs, atmospheric synths, dynamic drums", "production": "Atmospheric, modern, polished progressive metalcore"},
    "kublai khan tx": {"genre": "Modern Heavy, Metalcore", "mood": "Brutal, modern, heavy", "style": "Modern brutal metalcore, heavy breakdowns", "vocal_style": "Matt Honeycutt, brutal shouts, intense", "instruments": "Modern metalcore riffs, breakdowns, dynamic drums", "production": "Modern, brutal, polished metalcore"},
    "veil of maya": {"genre": "Modern Heavy, Progressive Metalcore", "mood": "Technical, modern, djent", "style": "Modern djent-influenced metalcore, technical", "vocal_style": "Lukas Magyar, clean + screams, dynamic", "instruments": "Djent riffs, technical drums, atmospheric synths", "production": "Technical, modern, polished djent-metalcore"},
    "after the burial": {"genre": "Modern Heavy, Progressive Metalcore", "mood": "Technical, modern, heavy", "style": "Progressive metalcore, technical and heavy", "vocal_style": "Dan Carle / Thomas Welsh, screams + clean, dynamic", "instruments": "Technical metalcore riffs, djent elements, dynamic drums", "production": "Technical, heavy, polished progressive metalcore"},
    "currents": {"genre": "Modern Heavy, Metalcore", "mood": "Heavy, modern, dynamic", "style": "Modern metalcore, dynamic clean/scream", "vocal_style": "Brian Wille, clean + screams, dynamic", "instruments": "Modern metalcore riffs, synth layers, big drums", "production": "Modern, dynamic, polished metalcore"},
    "wolves at the gate alt": {"genre": "Modern Heavy, Metalcore, Post-Hardcore", "mood": "Hopeful, fierce, worshipful", "style": "Faith-driven heavy music, anthemic choruses", "vocal_style": "Steve Cobucci, screams + cleans, emotional", "instruments": "Heavy guitar, driving drums, synth layers", "production": "Modern, dynamic, cinematic heavy"},
    "blessthefall zero": {"genre": "Modern Heavy, Post-Hardcore", "mood": "Heavy, melodic, modern", "style": "Modern post-hardcore, melodic heavy", "vocal_style": "Beau Bokan, clean + screams, dynamic", "instruments": "Post-hardcore riffs, synth, big drums", "production": "Modern, melodic, polished post-hardcore"},
    "thornhill": {"genre": "Modern Heavy, Metalcore", "mood": "Atmospheric, modern, heavy", "style": "Australian atmospheric metalcore, modern", "vocal_style": "Jacob Charlton, clean + screams, dynamic", "instruments": "Atmospheric metalcore riffs, synth layers, dynamic drums", "production": "Atmospheric, modern, polished Australian metalcore"},
    "spiritbox alt": {"genre": "Modern Heavy, Progressive Metalcore", "mood": "Heavy, dynamic, emotional", "style": "Progressive metalcore, dynamic female vocals", "vocal_style": "Courtney LaPlante, ethereal cleans + guttural screams", "instruments": "Djent guitar, atmospheric synths, technical drums", "production": "Modern progressive heavy, atmospheric polish"},
    "blessthefall modern": {"genre": "Modern Heavy, Post-Hardcore", "mood": "Heavy, melodic, modern", "style": "Modern post-hardcore, melodic heavy", "vocal_style": "Beau Bokan, clean + screams, dynamic", "instruments": "Post-hardcore riffs, synth, big drums", "production": "Modern, melodic, polished post-hardcore"},
    "sleep token alt": {"genre": "Modern Heavy, Atmospheric Metalcore", "mood": "Ethereal, heavy, masked intimacy", "style": "Anonymous masked metalcore, atmospheric pop-metal fusion", "vocal_style": "Vessel, soaring cleans + devastating screams, dynamic", "instruments": "Atmospheric guitar, electronic elements, cinematic drums", "production": "Huge cinematic heavy, atmospheric polish, masked mystique"},
    "bad omens alt": {"genre": "Modern Heavy, Metalcore", "mood": "Dark, cinematic, modern", "style": "Modern metalcore with cinematic, atmospheric edge", "vocal_style": "Noah Sebastian, screams + soaring cleans, dramatic", "instruments": "Atmospheric guitar, electronic production, heavy drums", "production": "Cinematic modern metalcore, atmospheric, dynamic"},
    "spiritbox prime": {"genre": "Modern Heavy, Progressive Metalcore", "mood": "Heavy, dynamic, emotional", "style": "Progressive metalcore, dynamic female vocals", "vocal_style": "Courtney LaPlante, ethereal cleans + guttural screams", "instruments": "Djent guitar, atmospheric synths, technical drums", "production": "Modern progressive heavy, atmospheric polish"},

    # === Modern Rock (alt rock / post-grunge / modern hard rock) — full coverage ===
    "imagine dragons": {"genre": "Modern Rock, Arena Rock", "mood": "Anthemic, energetic, stadium", "style": "Modern arena rock, big hooks, electronic", "vocal_style": "Dan Reynolds, big belting, anthemic", "instruments": "Big drums, electronic, anthemic guitar", "production": "Stadium-ready, polished, modern arena"},
    "twenty one pilots": {"genre": "Modern Rock, Alternative", "mood": "Quirky, emotional, layered", "style": "Modern alt rock with hip-hop and electronic", "vocal_style": "Tyler Joseph, rap + clean, dynamic", "instruments": "Alt rock, ukulele, synth, electronic", "production": "Modern alt, layered, polished"},
    "fall out boy": {"genre": "Modern Rock, Pop Punk", "mood": "Anthemic, witty, modern pop-punk", "style": "Modern pop-punk with arena rock hooks", "vocal_style": "Patrick Stump, big belting, versatile", "instruments": "Pop-punk guitar, big drums, synth", "production": "Modern pop-punk polish, anthemic"},
    "panic at the disco": {"genre": "Modern Rock, Pop Rock", "mood": "Theatrical, dramatic, modern", "style": "Theatrical pop-rock, modern alt", "vocal_style": "Brendon Urie, theatrical tenor, dynamic", "instruments": "Pop-rock band, synth, orchestral touches", "production": "Theatrical, modern, polished pop-rock"},
    "my chemical romance": {"genre": "Modern Rock, Emo, Post-Hardcore", "mood": "Theatrical, dark, anthemic", "style": "Theatrical emo, post-hardcore anthems", "vocal_style": "Gerard Way, theatrical, dynamic", "instruments": "Post-hardcore riffs, big drums, synth", "production": "Theatrical, dark, polished emo"},
    "green day": {"genre": "Modern Rock, Pop Punk", "mood": "Rebellious, anthemic, modern", "style": "Modern pop-punk, arena rock crossover", "vocal_style": "Billie Joe Armstrong, pop-punk snarl + clean", "instruments": "Pop-punk guitar, big drums, bass", "production": "Modern pop-punk polish, anthemic"},
    "blink-182": {"genre": "Modern Rock, Pop Punk", "mood": "Fun, irreverent, modern", "style": "Modern pop-punk, fun hooks", "vocal_style": "Mark Hoppus / Tom DeLonge, conversational pop-punk", "instruments": "Pop-punk guitar, fast drums, bass", "production": "Modern pop-punk polish, fun"},
    "paramore": {"genre": "Modern Rock, Pop Punk", "mood": "Energetic, emotional, anthemic", "style": "Modern pop-punk, emotional rock", "vocal_style": "Hayley Williams, big belting, dynamic", "instruments": "Pop-punk guitar, big drums, synth touches", "production": "Modern pop-punk polish, emotional"},
    "good charlotte": {"genre": "Modern Rock, Pop Punk", "mood": "Anthemic, rebellious, modern", "style": "Modern pop-punk, arena rock", "vocal_style": "Joel / Benji Madden, pop-punk snarl + clean", "instruments": "Pop-punk guitar, big drums, anthemic", "production": "Modern pop-punk polish, anthemic"},
    "simple plan": {"genre": "Modern Rock, Pop Punk", "mood": "Nostalgic, anthemic, modern", "style": "Modern pop-punk, anthemic", "vocal_style": "Pierre Bouvier, pop-punk clean, dynamic", "instruments": "Pop-punk guitar, big drums, bass", "production": "Modern pop-punk polish, anthemic"},
    "sum 41": {"genre": "Modern Rock, Pop Punk", "mood": "Energetic, modern, fun", "style": "Modern pop-punk with metal edge", "vocal_style": "Deryck Whibley, pop-punk snarl + clean", "instruments": "Pop-punk guitar, big drums, occasional metal", "production": "Modern pop-punk polish, energetic"},
    "the killers": {"genre": "Modern Rock, Indie Rock", "mood": "Anthemic, nostalgic, modern", "style": "Modern indie rock, anthemic new wave", "vocal_style": "Brandon Flowers, dynamic tenor, anthemic", "instruments": "New wave guitar, big drums, synth", "production": "Modern indie rock polish, anthemic"},
    "muse": {"genre": "Modern Rock, Alternative", "mood": "Epic, dramatic, modern", "style": "Modern alt rock with classical and electronic scope", "vocal_style": "Matt Bellamy, operatic tenor, dynamic", "instruments": "Alt rock guitar, piano, synth, orchestral", "production": "Cinematic, modern, polished alt rock"},
    "thirty seconds to mars": {"genre": "Modern Rock, Alternative", "mood": "Epic, atmospheric, modern", "style": "Modern alt rock, atmospheric anthems", "vocal_style": "Jared Leto, soaring tenor, dynamic", "instruments": "Alt rock guitar, atmospheric synth, big drums", "production": "Atmospheric, modern, polished alt rock"},
    "snow patrol": {"genre": "Modern Rock, Alternative", "mood": "Anthemic, emotional, modern", "style": "Modern alt rock, anthemic ballads", "vocal_style": "Gary Lightbody, emotional tenor, dynamic", "instruments": "Alt rock guitar, atmospheric synth, big drums", "production": "Modern, emotional, polished alt rock"},
    "coldplay": {"genre": "Modern Rock, Alternative", "mood": "Anthemic, emotional, modern", "style": "Modern alt rock, anthemic stadium pop", "vocal_style": "Chris Martin, soaring tenor, dynamic", "instruments": "Alt rock guitar, piano, atmospheric synth", "production": "Modern, anthemic, polished stadium alt"},
    "radiohead alt": {"genre": "Modern Rock, Alternative", "mood": "Experimental, modern, alt", "style": "Experimental modern alt rock", "vocal_style": "Thom Yorke, emotional, falsetto, strained", "instruments": "Guitar, synths, orchestral, electronic", "production": "Atmospheric, layered, experimental"},
    "the 1975": {"genre": "Modern Rock, Synthpop", "mood": "Nostalgic, modern, synth-driven", "style": "Modern synth-rock, 80s revival with alt edge", "vocal_style": "Matty Healy, conversational + croon, dynamic", "instruments": "Synths, alt rock guitar, electronic drums", "production": "Modern synth-rock polish, nostalgic 80s sheen"},
    "cage the elephant": {"genre": "Modern Rock, Alternative", "mood": "Energetic, raw, modern", "style": "Modern alt rock, garage-influenced", "vocal_style": "Matt Shultz, raw + melodic, dynamic", "instruments": "Alt rock guitar, garage drums, big choruses", "production": "Modern alt rock polish, raw energy"},
    "nothing but thieves": {"genre": "Modern Rock, Alternative", "mood": "Atmospheric, modern, dynamic", "style": "Modern British alt rock, atmospheric", "vocal_style": "Conor Mason, clean + raw, dynamic", "instruments": "Alt rock guitar, atmospheric synth, big drums", "production": "Modern, atmospheric, polished British alt"},
    "royal blood prime": {"genre": "Modern Rock, Bass-Rock", "mood": "Heavy, sleek, propulsive", "style": "Bass-and-drums duo rock, modern heavy", "vocal_style": "Mike Kerr, smoky baritone, melodic over heavy bass", "instruments": "Massive fuzzed bass, minimal drums, no guitar", "production": "Modern rock polish, thick low end, arena-ready"},
    "nothing more": {"genre": "Modern Rock, Alternative", "mood": "Heavy, modern, dynamic", "style": "Modern alt rock with progressive edge", "vocal_style": "Jonny Hawkins, dynamic + raw, versatile", "instruments": "Alt rock guitar, progressive drums, big choruses", "production": "Modern alt rock polish, heavy"},
    "highly suspect": {"genre": "Modern Rock, Alternative", "mood": "Heavy, dark, modern", "style": "Modern alt rock, dark and heavy", "vocal_style": "Johnny Stevens, raw + melodic, dynamic", "instruments": "Heavy alt rock guitar, dark bass, dynamic drums", "production": "Modern, dark, polished heavy alt"},
    "badflower": {"genre": "Modern Rock, Alternative", "mood": "Emotional, modern, dynamic", "style": "Modern alt rock, emotional and dynamic", "vocal_style": "Josh Katz, raw + emotional, dynamic", "instruments": "Alt rock guitar, emotional drums, big choruses", "production": "Modern, emotional, polished alt"},
    "grandson": {"genre": "Modern Rock, Alternative", "mood": "Modern, rebellious, alt", "style": "Modern alt rock with electronic edge", "vocal_style": "Jordan Benjamin, raw + melodic, dynamic", "instruments": "Alt rock guitar, electronic, big drums", "production": "Modern, electronic-inflected, polished alt"},

    # === Nu-Metal (rap-rock, rap-metal, nu-metal revival) — full coverage ===
    "korn": {"genre": "Nu-Metal, Rap-Rock", "mood": "Dark, funky, pioneering nu-metal", "style": "Foundational nu-metal, low-tuned funk riffs", "vocal_style": "Jonathan Davis, screams + rap + croon, dynamic", "instruments": "7-string down-tuned guitar, slap bass, dynamic drums", "production": "Funky low-tuned, dark, pioneering nu-metal"},
    "limp bizkit": {"genre": "Nu-Metal, Rap-Rock", "mood": "Angry, energetic, fun", "style": "Aggressive nu-metal rap-rock crossover", "vocal_style": "Fred Durst, rap + shouts, energetic", "instruments": "Down-tuned guitar, turntables, big drums", "production": "Aggressive, fun, crossover rap-rock"},
    "system of a down": {"genre": "Nu-Metal, Alternative Metal", "mood": "Quirky, political, Armenian", "style": "Quirky Armenian-American nu-metal, odd time signatures", "vocal_style": "Serj Tankian, dynamic + operatic, distinctive", "instruments": "Quirky down-tuned riffs, odd time, big drums", "production": "Quirky, Armenian-influenced, dynamic nu-metal"},
    "deftones": {"genre": "Nu-Metal, Alternative Metal", "mood": "Atmospheric, dreamy, heavy", "style": "Atmospheric nu-metal, shoegaze-influenced heaviness", "vocal_style": "Chino Moreno, screams + clean + croon, dynamic", "instruments": "Atmospheric riffs, shoegaze textures, dynamic drums", "production": "Atmospheric, dreamy, polished nu-metal"},
    "slipknot": {"genre": "Nu-Metal, Alternative Metal", "mood": "Brutal, masked, chaotic", "style": "Nine-member masked nu-metal chaos", "vocal_style": "Corey Taylor, screams + melodic, intense", "instruments": "Multiple percussionists, down-tuned riffs, industrial", "production": "Brutal, masked, chaotic nu-metal"},
    "evanescence": {"genre": "Nu-Metal, Gothic Rock", "mood": "Gothic, dramatic, operatic", "style": "Gothic nu-metal with classical piano", "vocal_style": "Amy Lee, operatic soprano, dramatic", "instruments": "Down-tuned riffs, piano, orchestral synth, big drums", "production": "Gothic, dramatic, polished nu-metal"},
    "disturbed": {"genre": "Nu-Metal, Alternative Metal", "mood": "Intense, modern, anthem-heavy", "style": "Modern nu-metal with arena rock polish", "vocal_style": "David Draiman, snarl + melodic, distinctive", "instruments": "Down-tuned riffs, big drums, industrial elements", "production": "Modern, big-room, polished nu-metal"},
    "godsmack": {"genre": "Nu-Metal, Alternative Metal", "mood": "Aggressive, heavy, modern", "style": "Modern heavy nu-metal, post-Alice in Chains", "vocal_style": "Sully Erna, snarl + clean, intense", "instruments": "Down-tuned riffs, big drums, heavy bass", "production": "Modern, heavy, polished nu-metal"},
    "papa roach": {"genre": "Nu-Metal, Rap-Rock", "mood": "Energetic, modern, anthem", "style": "Modern nu-metal, rap-rock crossover", "vocal_style": "Jacoby Shaddix, rap + clean, energetic", "instruments": "Down-tuned riffs, big drums, turntable elements", "production": "Modern, energetic, polished nu-metal"},
    "sevendust": {"genre": "Nu-Metal, Alternative Metal", "mood": "Heavy, soulful, modern", "style": "Soulful heavy nu-metal, modern alt metal", "vocal_style": "Lajon Witherspoon, soulful + screams, dynamic", "instruments": "Down-tuned riffs, heavy drums, soulful grooves", "production": "Heavy, soulful, polished nu-metal"},
    "staind": {"genre": "Nu-Metal, Post-Grunge", "mood": "Heavy, emotional, modern", "style": "Modern heavy nu-metal, post-grunge edge", "vocal_style": "Aaron Lewis, raw + melodic, dynamic", "instruments": "Down-tuned riffs, big drums, post-grunge", "production": "Modern, heavy, polished nu-metal"},
    "stone sour": {"genre": "Nu-Metal, Alternative Metal", "mood": "Heavy, modern, dynamic", "style": "Modern heavy nu-metal, melodic dynamic", "vocal_style": "Corey Taylor, screams + clean, dynamic", "instruments": "Down-tuned riffs, big drums, dynamic", "production": "Modern, heavy, polished nu-metal"},
    "ill niño": {"genre": "Nu-Metal, Latin Metal", "mood": "Latin-infused, heavy, modern", "style": "Latin-infused nu-metal, modern heavy", "vocal_style": "Cristian Machado, screams + clean, dynamic", "instruments": "Down-tuned riffs, Latin percussion, big drums", "production": "Modern, Latin-infused, polished nu-metal"},
    "hed pe": {"genre": "Nu-Metal, Rap-Rock", "mood": "Funky, rebellious, modern", "style": "Funky rap-rock nu-metal, modern", "vocal_style": "Jahred Shane, rap + clean, funky", "instruments": "Funky down-tuned riffs, hip-hop drums, turntables", "production": "Funky, modern, polished rap-rock"},
    "(hed) p.e.": {"genre": "Nu-Metal, Rap-Rock", "mood": "Funky, rebellious, modern", "style": "Funky rap-rock nu-metal, modern", "vocal_style": "Jahred Shane, rap + clean, funky", "instruments": "Funky down-tuned riffs, hip-hop drums, turntables", "production": "Funky, modern, polished rap-rock"},
    "saliva": {"genre": "Nu-Metal, Rap-Rock", "mood": "Aggressive, modern, anthemic", "style": "Modern nu-metal, rap-rock crossover", "vocal_style": "Josey Scott, rap + clean, energetic", "instruments": "Down-tuned riffs, big drums, turntable elements", "production": "Modern, energetic, polished nu-metal"},
    "drowning pool": {"genre": "Nu-Metal, Alternative Metal", "mood": "Brutal, modern, anthemic", "style": "Modern heavy nu-metal, anthems", "vocal_style": "Dave Williams / Ryan McCombs, shouts + clean, dynamic", "instruments": "Down-tuned riffs, big drums, anthemic", "production": "Modern, brutal, polished nu-metal"},
    "adema": {"genre": "Nu-Metal, Alternative Metal", "mood": "Modern, heavy, dynamic", "style": "Modern nu-metal, dynamic clean/scream", "vocal_style": "Mark Chavez / Luke Caraccioli, clean + screams, dynamic", "instruments": "Down-tuned riffs, big drums, dynamic", "production": "Modern, heavy, polished nu-metal"},
    "taproot": {"genre": "Nu-Metal, Alternative Metal", "mood": "Modern, heavy, dynamic", "style": "Modern heavy nu-metal, dynamic", "vocal_style": "Stephen Richards, clean + screams, dynamic", "instruments": "Down-tuned riffs, big drums, dynamic", "production": "Modern, heavy, polished nu-metal"},
    "nonpoint": {"genre": "Nu-Metal, Rap-Rock", "mood": "Modern, energetic, heavy", "style": "Modern nu-metal, rap-rock crossover", "vocal_style": "Elias Soriano, rap + clean, energetic", "instruments": "Down-tuned riffs, big drums, turntable elements", "production": "Modern, energetic, polished nu-metal"},
    "soi": {"genre": "Nu-Metal, Rap-Rock", "mood": "Funky, modern, aggressive", "style": "Funky aggressive nu-metal", "vocal_style": "B. Scott + S.O.I., rap + clean, dynamic", "instruments": "Funky down-tuned riffs, big drums, hip-hop", "production": "Funky, modern, polished nu-metal"},
    "flyleaf": {"genre": "Nu-Metal, Alternative Metal", "mood": "Modern, heavy, emotional", "style": "Modern heavy nu-metal, emotional female vocals", "vocal_style": "Lacey Sturm, clean + screams, emotional", "instruments": "Down-tuned riffs, big drums, dynamic", "production": "Modern, heavy, polished nu-metal"},
    "skindred": {"genre": "Nu-Metal, Rap-Rock", "mood": "Funky, modern, aggressive", "style": "Welsh ragga-metal nu-metal, crossover", "vocal_style": "Benji Webbe, ragga + clean + shouts, dynamic", "instruments": "Down-tuned riffs, big drums, reggae elements", "production": "Modern, funky, polished ragga-nu-metal"},
    "ho99o9": {"genre": "Nu-Metal, Horrorcore", "mood": "Brutal, modern, horror", "style": "Modern horrorcore nu-metal, modern aggressive", "vocal_style": "Eaddy / theOGM, screams + rap, brutal", "instruments": "Down-tuned riffs, big drums, industrial noise", "production": "Brutal, modern, polished horrorcore nu-metal"},
    "code orange": {"genre": "Nu-Metal, Hardcore", "mood": "Brutal, modern, hardcore", "style": "Modern hardcore-influenced nu-metal revival", "vocal_style": "Jami Morgan, screams + clean, brutal", "instruments": "Down-tuned riffs, hardcore drums, industrial noise", "production": "Brutal, modern, polished nu-metal hardcore"},
    "fire from the gods": {"genre": "Nu-Metal, Rap-Rock", "mood": "Modern, heavy, dynamic", "style": "Modern nu-metal revival, rap-rock crossover", "vocal_style": "AJ Channer, rap + clean, dynamic", "instruments": "Down-tuned riffs, big drums, turntable elements", "production": "Modern, heavy, polished nu-metal revival"},
    "fever 333": {"genre": "Nu-Metal, Rap-Rock", "mood": "Fierce, political, modern", "style": "Modern nu-metal revival, rap-rock crossover", "vocal_style": "Jason Aalon Butler, rap + clean + screams, intense", "instruments": "Down-tuned riffs, big drums, turntable elements", "production": "Modern, intense, polished nu-metal revival"},
    "linkin park alt": {"genre": "Nu-Metal, Alternative Rock", "mood": "Intense, emotional, aggressive", "style": "Rap-rock fusion, heavy drops", "vocal_style": "Screaming + melodic rap", "instruments": "Heavy guitars, electronics, turntables", "production": "Aggressive, layered"},

    # === Indie / Folk / Alt ===
    "bon iver": {"genre": "Indie Folk", "mood": "Melancholic, wintry, intimate", "style": "Ethereal, falsetto, nature", "vocal_style": "Falsetto, processed, layered", "instruments": "Acoustic guitar, horns", "production": "Atmospheric, reverb-heavy"},
    "phoebe bridgers": {"genre": "Indie Rock, Folk", "mood": "Melancholic, nostalgic, intimate", "style": "Sad girl indie, confessional", "vocal_style": "Soft, whispery, emotional", "instruments": "Acoustic guitar, strings", "production": "Intimate, warm, minimal"},
    "lord": {"genre": "Art Pop, Electropop", "mood": "Dramatic, confident, atmospheric", "style": "Minimalist pop, mature", "vocal_style": "Deep, powerful, unique", "instruments": "Synths, drums, minimal", "production": "Atmospheric, modern, clean"},
    "mitski": {"genre": "Indie Rock", "mood": "Introspective, aching, raw", "style": "Emotional, poetic", "vocal_style": "Expressive, vulnerable", "instruments": "Guitar, drums, piano", "production": "Intimate to explosive"},
    "tame impala": {"genre": "Psychedelic Rock, Electronic", "mood": "Dreamy, nostalgic, groovy", "style": "Psychedelic pop", "vocal_style": "Falsetto, layered", "instruments": "Synths, guitar, drums", "production": "Warm, analog, lush"},

    # === K-Pop & others ===
    "blackpink": {"genre": "K-Pop", "mood": "Fierce, confident, energetic", "style": "Powerful choreo-pop", "vocal_style": "Strong, harmonized, rap verses", "instruments": "EDM drops, synths", "production": "Slick, high-energy"},
    "newjeans": {"genre": "K-Pop, R&B", "mood": "Youthful, chill, nostalgic", "style": "Y2K-inspired, minimal", "vocal_style": "Soft, breathy, harmonious", "instruments": "Light synths, groovy bass", "production": "Clean, retro-modern"},
    "bts": {"genre": "K-Pop, Hip-Hop", "mood": "Anthemic, motivational, varied", "style": "Genre-hopping idol pop, message-driven", "vocal_style": "Multi-member, rap verses + soaring choruses", "instruments": "EDM, hip-hop, synths, full band", "production": "Polished, global, multi-genre hybrid"},
    "stray kids": {"genre": "K-Pop, Hip-Hop", "mood": "High-energy, rebellious, intense", "style": "Self-produced hip-hop and EDM idol pop", "vocal_style": "Rapping + belting, fierce, layered", "instruments": "Heavy 808s, EDM drops, electronic beats", "production": "Hard-hitting, maximalist, aggressive K-Pop"},
    "iu": {"genre": "K-Pop, Singer-Songwriter", "mood": "Whimsical, emotional, charming", "style": "Korean singer-songwriter pop with cinematic variety", "vocal_style": "Sweet, clear, emotionally expressive", "instruments": "Piano, acoustic guitar, modern pop production", "production": "Polished K-Pop ballad to bright pop, cinematic"},

    # === Latin / Mexico / Reggaeton ===
    "bad bunny": {"genre": "Reggaeton, Latin Trap", "mood": "Sensual, rebellious, genre-bending", "style": "Reggaeton pioneer with experimental edge, global hooks", "vocal_style": "Melodic reggaeton, conversational charisma", "instruments": "Dembow riddims, synths, Latin percussion", "production": "Tropical, modern, global urbano polish"},
    "peso pluma": {"genre": "Corridos Tumbados, Mexican Regional", "mood": "Stoic, narrative, swagger", "style": "Modern corrido with trap production, global breakthrough", "vocal_style": "Clear conversational baritone, narrative, emotional", "instruments": "Tubas, accordion, requinto, trap 808s", "production": "Tubazo meets trap, regional Mexican global sound"},
    "grupo frontera": {"genre": "Regional Mexican, Cumbia", "mood": "Romantic, nostalgic, traditional", "style": "Tejano-influenced grupera with modern cumbia", "vocal_style": "Romantic Spanish vocals, harmonies, accordion leads", "instruments": "Accordion, bajo sexto, tuba, cumbia percussion", "production": "Clean regional Mexican, romantic polish, traditional"},
    "karol g": {"genre": "Reggaeton, Latin Pop", "mood": "Empowering, confident, sensual", "style": "Reggaeton queen with pop crossover hits", "vocal_style": "Powerful feminine reggaeton, melodic, commanding", "instruments": "Dembow, reggaeton synths, tropical percussion", "production": "Global Latin pop, polished, festival-ready"},
    "natanael cano": {"genre": "Corridos Bélicos, Trap Corrido", "mood": "Hedonistic, narrative, swagger", "style": "Trap-influenced narco corridos for Gen Z", "vocal_style": "Casual conversational, autotune touches, raw charisma", "instruments": "Tubas, trap 808s, requinto, regional percussion", "production": "Tubazo + trap, gritty, viral Mexican regional"},
    "rosalía": {"genre": "Latin Pop, Flamenco-Pop", "mood": "Dramatic, sensual, avant-garde", "style": "Flamenco-rooted experimental Latin pop", "vocal_style": "Powerful Spanish vocals, flamenco melisma, modern edge", "instruments": "Flamenco guitar, palmas, Latin percussion, modern bass", "production": "Cinematic avant-Latin, lush, experimental polish"},

    # === India (Bollywood, Punjabi, Indie) ===
    "arijit singh": {"genre": "Bollywood, Indian Film Music", "mood": "Romantic, melancholic, emotional", "style": "#1 Bollywood playback singer, expressive ballads and anthems", "vocal_style": "Soaring Hindi/Urdu, melismatic, deeply emotional tenor", "instruments": "Tabla, harmonium, modern Indian film orchestra", "production": "Cinematic Bollywood, layered, polished modern Indian film"},
    "pritam": {"genre": "Bollywood, Indian Film Composer", "mood": "Versatile, melodic, anthemic", "style": "Top Bollywood composer, hit-making film soundtracks", "vocal_style": "Composer-driven, often features multiple singers", "instruments": "Full Indian film orchestra, modern pop production, rock elements", "production": "Cinematic Bollywood, pop-rock fusion, massive film polish"},
    "karan aujla": {"genre": "Punjabi Pop, Punjabi Hip-Hop", "mood": "Confident, romantic, swaggering", "style": "Global Punjabi pop star, hits with massive hooks", "vocal_style": "Punjabi melodic singing, English hooks, charismatic flows", "instruments": "Dhol, modern 808s, tumbi, synth bass", "production": "Polished global Punjabi, festival-ready crossover"},
    "ap dhillon": {"genre": "Punjabi Indie, Indo-Canadian R&B", "mood": "Moody, romantic, introspective", "style": "Indo-Canadian Punjabi indie fusing R&B, lo-fi and bhangra", "vocal_style": "Soft Punjabi-English, melodic, breathy, moody", "instruments": "Acoustic guitar, lo-fi synths, dhol, subtle 808s", "production": "Lo-fi polish, atmospheric, intimate cross-cultural"},
    "anuv jain": {"genre": "Indian Indie, Hindi Indie Folk-Pop", "mood": "Wistful, romantic, nostalgic", "style": "Hindi-English indie folk-pop, intimate storytelling", "vocal_style": "Soft conversational Hindi-English, breathy, intimate", "instruments": "Acoustic guitar, soft synths, light percussion", "production": "Lo-fi to polished indie, bedroom intimacy, heartfelt"},

    # === Italy ===
    "maneskin": {"genre": "Italian Rock, Glam Rock", "mood": "Rebellious, glamorous, raw", "style": "Italian glam rock, Eurovision 2021 winners, global breakthrough", "vocal_style": "Damiano David, husky, charismatic, English/Italian", "instruments": "Driving bass, glam guitar, rock drums", "production": "Modern glam rock polish, festival-anthem energy"},
    "sal da vinci": {"genre": "Italian Pop, Neapolitan", "mood": "Romantic, Mediterranean, warm", "style": "Sanremo 2026 winner, Neapolitan melodic pop", "vocal_style": "Passionate Italian tenor, romantic, Mediterranean warmth", "instruments": "Strings, mandolin, piano, Mediterranean percussion", "production": "Sanremo-style Italian pop, polished, emotional"},
    "angelina mango": {"genre": "Italian Pop, Sanremo", "mood": "Young, energetic, introspective", "style": "Sanremo 2024 winner, modern Italian pop", "vocal_style": "Youthful Italian, expressive, modern edge", "instruments": "Modern pop band, electronic touches, guitar", "production": "Contemporary Sanremo, polished, contemporary European pop"},
    "annalisa": {"genre": "Italian Pop, Sanremo", "mood": "Confident, sensual, contemporary", "style": "Sanremo regular, modern Italian pop with electronic edge", "vocal_style": "Clear Italian vocals, confident, contemporary", "instruments": "Synths, electronic beats, modern pop band", "production": "Modern Sanremo, electronic Italian pop, polished"},
    "eros ramazzotti": {"genre": "Italian Pop, Classic Italian", "mood": "Romantic, passionate, dramatic", "style": "Italian pop legend, 40+ year career, global hits", "vocal_style": "Iconic Italian tenor, passionate, melodic", "instruments": "Full orchestra, pop band, Mediterranean strings", "production": "Classic Italian pop polish, dramatic, timeless"},

    # === Afrobeats ===
    "burna boy": {"genre": "Afrobeats, Afro-Fusion", "mood": "Confident, rhythmic, expansive", "style": "Afro-fusion pioneer, Grammy winner, global breakthrough", "vocal_style": "Pidgin English, warm baritone, rhythmic, charismatic", "instruments": "Log drums, talking drum, congas, 808s, afrobeats synths", "production": "Global afrobeats polish, layered, cinematic African"},
    "tems": {"genre": "Afrobeats, Alté R&B", "mood": "Soulful, introspective, moody", "style": "Alté R&B with afrobeats roots, cinematic", "vocal_style": "Rich soulful alto, breathy, introspective, powerful", "instruments": "Sparse afrobeats percussion, atmospheric synths, 808s", "production": "Atmospheric alté, moody, modern African R&B polish"},
    "wizkid": {"genre": "Afrobeats, Afropop", "mood": "Warm, romantic, celebratory", "style": "Afrobeats pop superstar, global crossover hits", "vocal_style": "Smooth Yoruba-English, warm, melodic, romantic", "instruments": "Log drums, afrobeats synths, modern 808s, guitar", "production": "Glossy global afrobeats, romantic polish, summer-ready"},
    "tyla": {"genre": "Amapiano, Afrobeats", "mood": "Sensual, playful, danceable", "style": "Amapiano global breakthrough, \"Water\" viral hit", "vocal_style": "Soft Zulu/English, breathy, sensual, rhythmic", "instruments": "Log drums, amapiano piano, congas, 808s", "production": "Amapiano global polish, log-drum bounce, summer dance"},

    # === Indie / Bedroom Pop ===
    "hozier": {"genre": "Indie Folk-Rock, Alternative", "mood": "Mythic, romantic, anthemic", "style": "Irish folk-rock with soulful depth, anthemic modern folk", "vocal_style": "Rich Irish tenor, soulful, powerful, expressive", "instruments": "Acoustic guitar, full folk-rock band, gospel choir touches", "production": "Organic folk-rock polish, anthemic, modern indie folk"},
    "beabadoobee": {"genre": "Bedroom Pop, Indie Rock", "mood": "Nostalgic, romantic, slacker", "style": "Bedroom indie rock, 90s alt influences, lo-fi charm", "vocal_style": "Soft conversational, breathy, accented, intimate", "instruments": "Jangly electric guitar, lo-fi drums, bedroom synths", "production": "Lo-fi bedroom polish, tape warmth, 90s nostalgia"},
    "big thief": {"genre": "Indie Folk-Rock, Alternative", "mood": "Raw, intimate, mystical", "style": "Indie folk-rock with raw emotional songwriting", "vocal_style": "Adrianne Lenker, fragile, raw, emotionally naked", "instruments": "Acoustic guitar, minimal drums, folk instrumentation", "production": "Stripped-back, organic, intimate live feel"},
    "boygenius": {"genre": "Indie Rock, Indie Folk", "mood": "Cathartic, intimate, anthemic", "style": "Indie supergroup, layered harmonies, emotional rock", "vocal_style": "Three-part harmonies, conversational to belting, raw", "instruments": "Acoustic and electric guitar, minimal drums, bass", "production": "Polished indie rock, harmony-forward, emotional dynamics"},

    # === Country / Americana ===
    "kacey musgraves": {"genre": "Country-Pop, Progressive Country", "mood": "Wistful, romantic, progressive", "style": "Progressive country-pop, thoughtful lyrics, modern sound", "vocal_style": "Clear country soprano, conversational, witty", "instruments": "Acoustic guitar, pedal steel, modern country band", "production": "Polished country-pop, modern Nashville, dreamy production"},
    "tyler childers": {"genre": "Outlaw Country, Americana", "mood": "Appalachian, raw, narrative", "style": "Outlaw country, Appalachian roots, raw storytelling", "vocal_style": "Hickory baritone, Appalachian drawl, raw authenticity", "instruments": "Fiddle, banjo, acoustic guitar, Appalachian folk band", "production": "Organic, raw, traditional with modern clarity"},
    "chris stapleton": {"genre": "Country-Soul, Southern Rock", "mood": "Gravelly, soulful, powerful", "style": "Country-soul with Southern rock grit, powerhouse vocals", "vocal_style": "Gravelly Southern tenor, bluesy, powerhouse, raw", "instruments": "Electric guitar, soul-influenced keys, full Southern band", "production": "Country-soul polish, Southern rock edge, organic warmth"},

    # === Modern Heavy ===
    "sleep token": {"genre": "Modern Heavy, Atmospheric Metalcore", "mood": "Ethereal, heavy, masked intimacy", "style": "Anonymous masked metalcore, atmospheric pop-metal fusion", "vocal_style": "Vessel, soaring cleans + devastating screams, dynamic", "instruments": "Atmospheric guitar, electronic elements, cinematic drums", "production": "Huge cinematic heavy, atmospheric polish, masked mystique"},
    "bad omens": {"genre": "Metalcore, Post-Hardcore", "mood": "Dark, cinematic, modern", "style": "Modern metalcore with cinematic, atmospheric edge", "vocal_style": "Noah Sebastian, screams + soaring cleans, dramatic", "instruments": "Atmospheric guitar, electronic production, heavy drums", "production": "Cinematic modern metalcore, atmospheric, dynamic"},
    "spiritbox": {"genre": "Progressive Metalcore, Djent", "mood": "Heavy, dynamic, emotional", "style": "Progressive metalcore with djent edge and dynamic female vocals", "vocal_style": "Courtney LaPlante, ethereal cleans + guttural screams, huge range", "instruments": "Djent guitar, atmospheric synths, technical drums", "production": "Modern progressive heavy, atmospheric polish, dynamic contrast"},

    # === Other ===
    "100 gecs": {"genre": "Hyperpop, Electronic", "mood": "Chaotic, maximalist, absurdist", "style": "Hyperpop maximalism, ironic genre-mashing, internet-core", "vocal_style": "Pitch-shifted, autotune-heavy, chaotic, playful", "instruments": "Brutal 808s, glitchy synths, crushed pop samples", "production": "Hyperpop maximalism, blown-out, intentional chaos"},
    "royal blood": {"genre": "Modern Rock, Bass-Rock", "mood": "Heavy, sleek, propulsive", "style": "Bass-and-drums duo rock, Queens of the Stone Age meets Arctic Monkeys", "vocal_style": "Mike Kerr, smoky baritone, melodic over heavy bass", "instruments": "Massive fuzzed bass, minimal drums, no guitar", "production": "Modern rock polish, thick low end, arena-ready"},

    # === CCM / Christian / Worship / Gospel ===
    "brandon lake": {"genre": "CCM, Worship Pop", "mood": "Uplifting, anthemic, passionate", "style": "Modern worship anthems, powerful builds", "vocal_style": "Strong, emotive, belting", "instruments": "Electric guitar, keys, full band", "production": "Epic, stadium-ready, layered vocals"},
    "forrest frank": {"genre": "CCM, Christian Pop", "mood": "Joyful, groovy, hopeful", "style": "Catchy pop-funk blends, positive vibes", "vocal_style": "Smooth, melodic, upbeat", "instruments": "Synths, bass, live drums", "production": "Bright, radio-friendly, crossover pop"},
    "lauren daigle": {"genre": "CCM, Soulful Pop", "mood": "Introspective, soaring, spiritual", "style": "Emotional ballads to anthems", "vocal_style": "Powerful, raspy, expressive", "instruments": "Piano, strings, acoustic guitar", "production": "Cinematic, warm, heartfelt"},
    "phil wickham": {"genre": "CCM, Worship", "mood": "Reverent, majestic, worshipful", "style": "Vertical worship songs, soaring choruses", "vocal_style": "Clear, high-range, passionate", "instruments": "Acoustic/electric guitar, keys, drums", "production": "Polished, atmospheric, live-feel"},
    "elevation worship": {"genre": "CCM, Modern Worship", "mood": "Epic, congregational, triumphant", "style": "Arena worship, repetitive builds", "vocal_style": "Powerful group vocals, leads", "instruments": "Full band, synth pads, electric guitar", "production": "Massive, reverb-heavy, live energy"},
    "chris tomlin": {"genre": "CCM, Worship", "mood": "Peaceful, adoring, timeless", "style": "Classic modern hymns, singable", "vocal_style": "Warm, steady, congregational", "instruments": "Acoustic guitar, piano, light band", "production": "Clean, organic, church-ready"},
    "josiah queen": {"genre": "CCM, Folk-Pop Worship", "mood": "Intimate, reflective, hopeful", "style": "Storytelling worship, acoustic-driven", "vocal_style": "Gentle, emotive, vulnerable", "instruments": "Acoustic guitar, light percussion", "production": "Warm, minimal to building"},
    "katy nichole": {"genre": "CCM, Pop", "mood": "Empowering, vulnerable, redemptive", "style": "Personal testimony songs, anthemic", "vocal_style": "Strong, emotional, belting", "instruments": "Piano, guitar, synths", "production": "Modern pop polish, uplifting"},
    "anne wilson": {"genre": "CCM, Country Rock", "mood": "Raw, heartfelt, resilient", "style": "Country-infused faith anthems", "vocal_style": "Twangy, powerful, gritty", "instruments": "Electric/acoustic guitar, drums", "production": "Rock edge, radio-ready"},
    "cece winans": {"genre": "Gospel, CCM", "mood": "Soulful, victorious, praising", "style": "Gospel ballads to uptempo", "vocal_style": "Rich, powerful, melismatic", "instruments": "Piano, organ, choir", "production": "Warm, live gospel feel"},
    "maverick city music": {"genre": "Gospel, CCM", "mood": "Communal, joyful, diverse", "style": "Multicultural worship, call-response", "vocal_style": "Harmonized, dynamic leads", "instruments": "Keys, percussion, band", "production": "Organic, inclusive, energetic"},
    "tauren wells": {"genre": "CCM, Pop/R&B", "mood": "Uplifting, groovy, faith-filled", "style": "Crossover pop-worship", "vocal_style": "Smooth, versatile, soulful", "instruments": "Synths, bass, drums", "production": "Polished, modern pop"},
    "carrie underwood": {"genre": "Country, CCM Crossover", "mood": "Inspirational, powerful, storytelling", "style": "Faith-themed country anthems", "vocal_style": "Strong, belting, emotive", "instruments": "Acoustic/electric guitar, fiddle", "production": "Big country polish"},
    "hillsong worship": {"genre": "CCM, Worship", "mood": "Atmospheric, reverent, global", "style": "Modern worship classics", "vocal_style": "Clear, anointed leads", "instruments": "Full worship band, pads", "production": "Live, expansive, anthemic"},
    "bethel music": {"genre": "CCM, Worship", "mood": "Intimate to explosive, prophetic", "style": "Spontaneous worship flows", "vocal_style": "Emotional, layered harmonies", "instruments": "Guitar, keys, ambient", "production": "Atmospheric, live worship"},
    "crowder": {"genre": "CCM, Folk-Rock Worship", "mood": "Joyful, rustic, celebratory", "style": "Folk-infused praise", "vocal_style": "Raspy, passionate, communal", "instruments": "Banjo, guitar, percussion", "production": "Warm, rootsy, fun"},
    "toby mac": {"genre": "CCM, Christian Hip-Hop/Pop", "mood": "Energetic, positive, bold", "style": "Genre-blending rap-pop", "vocal_style": "Rap verses + singing hooks", "instruments": "Beats, synths, guitars", "production": "High-energy, crossover"},
    "zach williams": {"genre": "CCM, Southern Rock/Gospel", "mood": "Redemptive, gritty, powerful", "style": "Storytelling redemption songs", "vocal_style": "Gravelly, soulful, strong", "instruments": "Electric guitar, drums", "production": "Rock-gospel edge"},
    "natalie grant": {"genre": "CCM, Pop Worship", "mood": "Dramatic, victorious, empowering", "style": "Big vocal anthems", "vocal_style": "Powerful, range-heavy", "instruments": "Piano, strings, band", "production": "Cinematic, inspirational"},
    "mercy me": {"genre": "CCM, Pop Rock", "mood": "Hopeful, reflective, anthemic", "style": "Faith anthems, piano-driven", "vocal_style": "Clear, emotional leads", "instruments": "Piano, guitar, drums", "production": "Polished, radio-friendly"},

    # === Electronic (top-up to 25) ===
    "calvin harris": {"genre": "Electronic, House", "mood": "Energetic, danceable, festival", "style": "EDM pop crossover, festival bangers", "vocal_style": "Featured vocalists, polished, varied", "instruments": "Dance synths, big drops, festival production", "production": "EDM polish, festival, layered"},
    "diplo": {"genre": "Electronic, World", "mood": "Eclectic, worldly, danceable", "style": "World-electronic fusion, Major Lazer alum", "vocal_style": "Featured vocalists, eclectic, varied", "instruments": "World samples, dance synths, varied", "production": "World-electronic polish, eclectic, layered"},
    "skrillex": {"genre": "Electronic, Dubstep", "mood": "Aggressive, energetic, bass-heavy", "style": "Dubstep pioneer, bass music", "vocal_style": "Minimal, rare, processed", "instruments": "Heavy bass, dubstep synths, drops", "production": "Aggressive bass polish, festival, layered"},
    "zedd": {"genre": "Electronic, House", "mood": "Energetic, melodic, pop", "style": "EDM pop crossover, melodic house", "vocal_style": "Featured vocalists, polished, varied", "instruments": "Melodic house synths, big drops, festival", "production": "EDM polish, melodic, layered"},
    "martin garrix": {"genre": "Electronic, Big Room", "mood": "Anthemic, energetic, festival", "style": "Big room house, festival EDM", "vocal_style": "Featured vocalists, minimal, varied", "instruments": "Big room synths, big drops, festival", "production": "EDM festival polish, big, anthemic"},
    "tiesto": {"genre": "Electronic, Trance", "mood": "Energetic, anthemic, evolved", "style": "Trance legend, evolved into pop-EDM", "vocal_style": "Featured vocalists, varied, dynamic", "instruments": "Trance synths, big drops, festival", "production": "EDM polish, evolved, layered"},
    "david guetta": {"genre": "Electronic, House", "mood": "Energetic, pop, festival", "style": "EDM-pop crossover pioneer, festival", "vocal_style": "Featured vocalists, polished, varied", "instruments": "Dance synths, big drops, festival", "production": "EDM polish, festival, layered"},
    "above and beyond": {"genre": "Electronic, Trance", "mood": "Emotional, anthemic, trance", "style": "Trance trio, emotional anthems", "vocal_style": "Featured vocalists, emotional, polished", "instruments": "Trance synths, big drops, emotional pads", "production": "Trance polish, emotional, layered"},
    "armin van buuren": {"genre": "Electronic, Trance", "mood": "Anthemic, emotional, trance", "style": "Trance legend, A State of Trance", "vocal_style": "Featured vocalists, emotional, varied", "instruments": "Trance synths, big drops, anthemic", "production": "Trance polish, anthemic, layered"},
    "ferry corsten": {"genre": "Electronic, Trance", "mood": "Uplifting, melodic, trance", "style": "Dutch trance veteran, uplifting", "vocal_style": "Featured vocalists, uplifting, varied", "instruments": "Uplifting trance synths, big drops", "production": "Trance polish, uplifting, layered"},
    "flume": {"genre": "Electronic, Future Bass", "mood": "Hypnotic, experimental, atmospheric", "style": "Future bass pioneer, eclectic collabs", "vocal_style": "Featured vocalists, processed, varied", "instruments": "Future bass synths, eclectic, layered", "production": "Future bass polish, experimental, layered"},
    "odesza": {"genre": "Electronic, Indie Dance", "mood": "Atmospheric, uplifting, cinematic", "style": "Cinematic indie-electronic, festival", "vocal_style": "Featured vocalists, emotional, polished", "instruments": "Atmospheric synths, big drums, layered", "production": "Cinematic polish, atmospheric, layered"},
    "rufus du sol": {"genre": "Electronic, Indie Dance", "mood": "Atmospheric, emotional, sunset", "style": "Australian indie-electronic, sunset vibes", "vocal_style": "Tyrone Lindqvist, atmospheric, emotional", "instruments": "Atmospheric synths, big drums, emotive", "production": "Indie-electronic polish, atmospheric, layered"},
    "caribou": {"genre": "Electronic, Indie Dance", "mood": "Psychedelic, joyful, layered", "style": "Canadian indie-electronic, psychedelic", "vocal_style": "Dan Snaith, processed, varied", "instruments": "Psychedelic synths, live drums, layered", "production": "Indie-electronic polish, psychedelic, layered"},
    "four tet": {"genre": "Electronic, IDM", "mood": "Hypnotic, eclectic, danceable", "style": "UK electronic, eclectic IDM-dance", "vocal_style": "Minimal, rare, processed", "instruments": "Eclectic samples, organic synths, varied", "production": "IDM-dance polish, eclectic, layered"},
    "bonobo": {"genre": "Electronic, Downtempo", "mood": "Atmospheric, organic, cinematic", "style": "British downtempo, organic and cinematic", "vocal_style": "Featured vocalists, atmospheric, varied", "instruments": "Organic samples, atmospheric synths, live", "production": "Downtempo polish, atmospheric, layered"},
    "thievery corporation": {"genre": "Electronic, Downtempo", "mood": "Atmospheric, eclectic, world-influenced", "style": "DC-based downtempo duo, eclectic world", "vocal_style": "Featured vocalists, eclectic, varied", "instruments": "World samples, organic synths, live", "production": "Downtempo polish, eclectic, layered"},
    "boards of canada": {"genre": "Electronic, IDM", "mood": "Nostalgic, atmospheric, melancholic", "style": "Scottish IDM duo, nostalgic warmth", "vocal_style": "Minimal, rare, processed", "instruments": "Lo-fi samples, atmospheric synths, nostalgic", "production": "IDM polish, nostalgic, layered"},
    "burial": {"genre": "Electronic, UK Garage", "mood": "Nocturnal, melancholic, atmospheric", "style": "UK garage-meets-ambient pioneer, nocturnal", "vocal_style": "Pitched, processed, atmospheric", "instruments": "Pitched vocal samples, garage beats, pads", "production": "UK garage polish, nocturnal, atmospheric"},
    "shiba san": {"genre": "Electronic, House", "mood": "Groovy, deep, underground", "style": "French deep house, underground grooves", "vocal_style": "Minimal, rare, processed", "instruments": "Deep house synths, deep bass, layered", "production": "Deep house polish, underground, layered"},
    "fisher": {"genre": "Electronic, Tech House", "mood": "Energetic, party, fun", "style": "Australian tech-house, festival fun", "vocal_style": "Featured vocalists, minimal, varied", "instruments": "Tech-house synths, big drops, festival", "production": "Tech-house polish, festival, layered"},
    "charlotte de witte": {"genre": "Electronic, Techno", "mood": "Hypnotic, driving, atmospheric", "style": "Belgian techno, festival headliner", "vocal_style": "Minimal, rare, processed", "instruments": "Hypnotic techno synths, deep bass, big drums", "production": "Techno polish, festival, layered"},
    "amelie lens": {"genre": "Electronic, Techno", "mood": "Industrial, hypnotic, intense", "style": "Belgian industrial techno, powerful", "vocal_style": "Minimal, rare, processed", "instruments": "Industrial techno synths, big drums, deep bass", "production": "Techno polish, industrial, layered"},
    "tale of us": {"genre": "Electronic, Melodic Techno", "mood": "Atmospheric, emotional, melodic", "style": "Italian-American melodic techno, cinematic", "vocal_style": "Minimal, rare, atmospheric", "instruments": "Melodic techno synths, atmospheric pads, big drums", "production": "Melodic techno polish, atmospheric, layered"},
    "carl cox": {"genre": "Electronic, Tech House", "mood": "Energetic, funky, foundational", "style": "UK tech-house legend, party grooves", "vocal_style": "Minimal, rare, processed", "instruments": "Tech-house synths, funky bass, big drums", "production": "Tech-house polish, foundational, layered"},

    # === K-Pop (top-up to 25) ===
    "bts": {"genre": "K-Pop, Hip-Hop", "mood": "Anthemic, varied, message-driven", "style": "K-Pop global phenomenon, hip-hop + EDM + R&B blend", "vocal_style": "Varies by member, dynamic, polished", "instruments": "K-Pop production, varied, layered", "production": "K-Pop polish, global, layered"},
    "blackpink": {"genre": "K-Pop, EDM", "mood": "Fierce, stylish, anthemic", "style": "K-Pop girl group, fierce anthems, hip-hop/EDM blend", "vocal_style": "Varies by member, fierce, polished", "instruments": "K-Pop production, EDM synths, layered", "production": "K-Pop polish, fierce, layered"},
    "twice": {"genre": "K-Pop, J-Pop", "mood": "Bright, cute, bubbly", "style": "K-Pop girl group, cute pop anthems", "vocal_style": "Bright, melodic, varied", "instruments": "K-Pop production, pop synths, layered", "production": "K-Pop polish, bright, layered"},
    "stray kids": {"genre": "K-Pop, Hip-Hop", "mood": "Energetic, rebellious, varied", "style": "K-Pop boy group, hip-hop edge, EDM", "vocal_style": "Aggressive, varied, dynamic", "instruments": "K-Pop production, hip-hop drums, EDM", "production": "K-Pop polish, aggressive, layered"},
    "exo": {"genre": "K-Pop, R&B", "mood": "Polished, varied, sophisticated", "style": "K-Pop boy group, varied R&B-EDM blend", "vocal_style": "Varies by member, polished, dynamic", "instruments": "K-Pop production, R&B-EDM, layered", "production": "K-Pop polish, sophisticated, layered"},
    "red velvet": {"genre": "K-Pop, Pop", "mood": "Dual-concept, playful, sophisticated", "style": "K-Pop girl group, dual 'red'/'velvet' concepts", "vocal_style": "Varies by member, versatile, polished", "instruments": "K-Pop production, varied, layered", "production": "K-Pop polish, versatile, layered"},
    "nct": {"genre": "K-Pop, Hip-Hop", "mood": "Experimental, varied, futuristic", "style": "K-Pop supergroup, experimental, hip-hop/EDM blend", "vocal_style": "Varies by member, experimental, dynamic", "instruments": "K-Pop production, experimental, layered", "production": "K-Pop polish, experimental, layered"},
    "ateez": {"genre": "K-Pop, Hip-Hop", "mood": "Dark, anthemic, powerful", "style": "K-Pop boy group, dark themes, hip-hop/EDM", "vocal_style": "Aggressive, dynamic, varied", "instruments": "K-Pop production, dark synths, layered", "production": "K-Pop polish, dark, layered"},
    "txt": {"genre": "K-Pop, Pop", "mood": "Youthful, varied, conceptual", "style": "K-Pop boy group, conceptual pop", "vocal_style": "Bright, varied, dynamic", "instruments": "K-Pop production, pop synths, varied", "production": "K-Pop polish, varied, layered"},
    "seventeen": {"genre": "K-Pop, Pop", "mood": "Youthful, varied, polished", "style": "K-Pop boy group, performance-focused pop", "vocal_style": "Varies by member, polished, varied", "instruments": "K-Pop production, varied, layered", "production": "K-Pop polish, varied, layered"},
    "itzy": {"genre": "K-Pop, Hip-Hop", "mood": "Bold, empowering, energetic", "style": "K-Pop girl group, 'teen-crush' hip-hop/pop", "vocal_style": "Confident, dynamic, varied", "instruments": "K-Pop production, hip-hop drums, pop", "production": "K-Pop polish, bold, layered"},
    "ive": {"genre": "K-Pop, Pop", "mood": "Sophisticated, confident, bright", "style": "K-Pop girl group, sophisticated pop", "vocal_style": "Sophisticated, varied, polished", "instruments": "K-Pop production, pop synths, layered", "production": "K-Pop polish, sophisticated, layered"},
    "newjeans": {"genre": "K-Pop, R&B", "mood": "Nostalgic, fresh, varied", "style": "K-Pop girl group, R&B/jersey club blend, retro", "vocal_style": "Nostalgic, fresh, varied", "instruments": "K-Pop production, R&B, jersey club", "production": "K-Pop polish, retro-fresh, layered"},
    "le sserafim": {"genre": "K-Pop, Pop", "mood": "Confident, varied, energetic", "style": "K-Pop girl group, confident pop", "vocal_style": "Confident, varied, dynamic", "instruments": "K-Pop production, pop synths, varied", "production": "K-Pop polish, confident, layered"},
    "aespa": {"genre": "K-Pop, EDM", "mood": "Futuristic, varied, edgy", "style": "K-Pop girl group, AI/metaverse concept, EDM", "vocal_style": "Varies by member, futuristic, varied", "instruments": "K-Pop production, EDM, futuristic", "production": "K-Pop polish, futuristic, layered"},
    "bts solo v": {"genre": "K-Pop, R&B", "mood": "Soulful, introspective, varied", "style": "BTS V solo, soulful R&B", "vocal_style": "V, distinctive baritone, soulful, varied", "instruments": "R&B production, layered, varied", "production": "K-Pop R&B polish, soulful, layered"},
    "bts solo jungkook": {"genre": "K-Pop, Pop", "mood": "Polished, pop, varied", "style": "BTS Jungkook solo, global pop", "vocal_style": "Jungkook, polished pop, dynamic", "instruments": "Pop production, layered, varied", "production": "K-Pop pop polish, global, layered"},
    "bts solo jimin": {"genre": "K-Pop, R&B", "mood": "Ethereal, emotional, R&B", "style": "BTS Jimin solo, ethereal R&B", "vocal_style": "Jimin, ethereal, emotional, distinctive", "instruments": "R&B production, ethereal, varied", "production": "K-Pop R&B polish, ethereal, layered"},
    "bts solo rm": {"genre": "K-Pop, Hip-Hop", "mood": "Introspective, hip-hop, varied", "style": "BTS RM solo, introspective hip-hop", "vocal_style": "RM, distinctive baritone, introspective", "instruments": "Hip-hop production, varied, layered", "production": "K-Pop hip-hop polish, introspective, layered"},
    "bts solo suga": {"genre": "K-Pop, Hip-Hop", "mood": "Aggressive, varied, hip-hop", "style": "BTS Suga / Agust D solo, varied hip-hop", "vocal_style": "Suga / Agust D, aggressive, varied, dynamic", "instruments": "Hip-hop production, varied, layered", "production": "K-Pop hip-hop polish, varied, layered"},
    "bts solo j hope": {"genre": "K-Pop, Hip-Hop", "mood": "Energetic, bright, hip-hop", "style": "BTS j-hope solo, bright hip-hop", "vocal_style": "j-hope, bright, dynamic, distinctive", "instruments": "Hip-hop production, bright, varied", "production": "K-Pop hip-hop polish, bright, layered"},

    # === Afrobeats (top-up to 25) ===
    "burna boy": {"genre": "Afrobeats, Afro-Fusion", "mood": "Confident, varied, Afrofuturist", "style": "Nigerian Afro-fusion pioneer, global", "vocal_style": "Burna Boy, distinctive, dynamic, varied", "instruments": "Afrobeats, live band, varied", "production": "Afro-fusion polish, global, layered"},
    "wizkid": {"genre": "Afrobeats, Pop", "mood": "Smooth, romantic, global", "style": "Nigerian Afrobeats-pop, global crossover", "vocal_style": "Wizkid, smooth, distinctive, dynamic", "instruments": "Afrobeats, pop production, varied", "production": "Afrobeats-pop polish, global, layered"},
    "davido": {"genre": "Afrobeats, Pop", "mood": "Energetic, celebratory, global", "style": "Nigerian Afrobeats-pop, festival-ready", "vocal_style": "Davido, energetic, distinctive, dynamic", "instruments": "Afrobeats, pop production, varied", "production": "Afrobeats-pop polish, energetic, layered"},
    "rema": {"genre": "Afrobeats, Afro-Rave", "mood": "Energetic, melodic, modern", "style": "Nigerian Afrobeats-rave, global crossover", "vocal_style": "Rema, melodic, distinctive, dynamic", "instruments": "Afrobeats, Afro-rave, varied", "production": "Afrobeats-rave polish, modern, layered"},
    "ckay": {"genre": "Afrobeats, Afro-R&B", "mood": "Romantic, dreamy, global", "style": "Nigerian Afro-R&B, 'Love Nwantiti' era", "vocal_style": "CKay, smooth, romantic, distinctive", "instruments": "Afro-R&B production, varied, layered", "production": "Afro-R&B polish, romantic, layered"},
    "fireboy dml": {"genre": "Afrobeats, Afro-R&B", "mood": "Romantic, soulful, modern", "style": "Nigerian Afro-R&B, soulful", "vocal_style": "Fireboy DML, soulful, distinctive, dynamic", "instruments": "Afro-R&B production, varied, layered", "production": "Afro-R&B polish, soulful, layered"},
    "asake": {"genre": "Afrobeats, Amapiano", "mood": "Energetic, varied, festival", "style": "Nigerian Amapiano-Afrobeats, festival", "vocal_style": "Asake, Yoruba + English, energetic, varied", "instruments": "Amapiano, Afrobeats, varied", "production": "Amapiano polish, festival, layered"},
    "victony": {"genre": "Afrobeats, Afro-R&B", "mood": "Soulful, modern, varied", "style": "Nigerian Afro-R&B, soulful", "vocal_style": "Victony, soulful, distinctive, dynamic", "instruments": "Afro-R&B production, varied, layered", "production": "Afro-R&B polish, soulful, layered"},
    "omah lay": {"genre": "Afrobeats, Afro-R&B", "mood": "Soulful, romantic, modern", "style": "Nigerian Afro-R&B, soulful romantic", "vocal_style": "Omah Lay, soulful, distinctive, dynamic", "instruments": "Afro-R&B production, varied, layered", "production": "Afro-R&B polish, soulful, layered"},
    "tems": {"genre": "Afrobeats, R&B", "mood": "Soulful, atmospheric, modern", "style": "Nigerian alternative R&B, atmospheric", "vocal_style": "Tems, soulful alto, distinctive, atmospheric", "instruments": "Atmospheric R&B production, varied", "production": "Atmospheric R&B polish, soulful, layered"},
    "ayra starr": {"genre": "Afrobeats, Pop", "mood": "Bold, varied, modern", "style": "Nigerian Afrobeats-pop, bold", "vocal_style": "Ayra Starr, bold, distinctive, dynamic", "instruments": "Afrobeats, pop production, varied", "production": "Afrobeats-pop polish, bold, layered"},
    "lucky daye": {"genre": "Afrobeats, R&B", "mood": "Soulful, modern, varied", "style": "American R&B with Afrobeats influence, soulful", "vocal_style": "Lucky Daye, soulful, distinctive, dynamic", "instruments": "R&B production, varied, layered", "production": "R&B polish, soulful, layered"},
    "chris brown afro": {"genre": "Afrobeats, R&B", "mood": "Energetic, varied, modern", "style": "American R&B with Afrobeats influence, energetic", "vocal_style": "Chris Brown, versatile, dynamic, varied", "instruments": "R&B production, varied, layered", "production": "R&B-Afrobeats polish, energetic, layered"},
    "tiwa savage": {"genre": "Afrobeats, R&B", "mood": "Soulful, powerful, Nigerian", "style": "Nigerian Afrobeats-R&B pioneer, Queen of Afrobeats", "vocal_style": "Tiwa Savage, soulful, powerful, distinctive", "instruments": "Afrobeats, R&B production, varied", "production": "Afrobeats-R&B polish, powerful, layered"},
    "yemi alade": {"genre": "Afrobeats, Afropop", "mood": "Vibrant, energetic, varied", "style": "Nigerian Afropop, vibrant", "vocal_style": "Yemi Alade, vibrant, distinctive, dynamic", "instruments": "Afropop production, varied, layered", "production": "Afropop polish, vibrant, layered"},
    "falz": {"genre": "Afrobeats, Hip-Hop", "mood": "Witty, Nigerian, varied", "style": "Nigerian hip-hop-Afrobeats, witty lyricist", "vocal_style": "Falz, witty, distinctive, dynamic", "instruments": "Hip-hop, Afrobeats, varied", "production": "Hip-hop-Afrobeats polish, witty, layered"},
    "olamide": {"genre": "Afrobeats, Hip-Hop", "mood": "Street, varied, Nigerian", "style": "Nigerian street-hop, Afrobeats", "vocal_style": "Olamide, Yoruba + English, dynamic, varied", "instruments": "Street-hop, Afrobeats, varied", "production": "Street-hop-Afrobeats polish, varied, layered"},
    "naira marley": {"genre": "Afrobeats, Street-Hop", "mood": "Rebellious, street, varied", "style": "Nigerian street-hop, Marlian Records founder", "vocal_style": "Naira Marley, rebellious, distinctive, dynamic", "instruments": "Street-hop production, varied, layered", "production": "Street-hop polish, rebellious, layered"},
    "zlatan": {"genre": "Afrobeats, Street-Hop", "mood": "Energetic, street, varied", "style": "Nigerian street-hop, energetic", "vocal_style": "Zlatan, energetic, distinctive, dynamic", "instruments": "Street-hop production, varied, layered", "production": "Street-hop polish, energetic, layered"},
    "buju": {"genre": "Afrobeats, Afro-R&B", "mood": "Soulful, modern, varied", "style": "Nigerian Afro-R&B, soulful", "vocal_style": "Buju, soulful, distinctive, dynamic", "instruments": "Afro-R&B production, varied, layered", "production": "Afro-R&B polish, soulful, layered"},
    "wande coal": {"genre": "Afrobeats, R&B", "mood": "Soulful, romantic, Nigerian", "style": "Nigerian Afrobeats-R&B, soulful romantic", "vocal_style": "Wande Coal, soulful, distinctive, dynamic", "instruments": "Afrobeats, R&B production, varied", "production": "Afrobeats-R&B polish, soulful, layered"},
    "tekno": {"genre": "Afrobeats, Pop", "mood": "Romantic, smooth, Nigerian", "style": "Nigerian Afrobeats-pop, romantic", "vocal_style": "Tekno, smooth, distinctive, dynamic", "instruments": "Afrobeats, pop production, varied", "production": "Afrobeats-pop polish, romantic, layered"},
    "mr eazi": {"genre": "Afrobeats, Pop", "mood": "Smooth, romantic, modern", "style": "Nigerian-Ghanaian Afrobeats-pop, smooth", "vocal_style": "Mr Eazi, smooth, distinctive, dynamic", "instruments": "Afrobeats, pop production, varied", "production": "Afrobeats-pop polish, smooth, layered"},
    "stonebwoy": {"genre": "Afrobeats, Dancehall", "mood": "Energetic, varied, Ghanaian", "style": "Ghanaian Afrobeats-dancehall, energetic", "vocal_style": "Stonebwoy, energetic, distinctive, dynamic", "instruments": "Dancehall, Afrobeats, varied", "production": "Dancehall-Afrobeats polish, energetic, layered"},
    "shatta wale": {"genre": "Afrobeats, Dancehall", "mood": "Energetic, bold, Ghanaian", "style": "Ghanaian dancehall-Afrobeats, bold", "vocal_style": "Shatta Wale, bold, distinctive, dynamic", "instruments": "Dancehall, Afrobeats, varied", "production": "Dancehall-Afrobeats polish, bold, layered"},

    # === K-Pop (3 more to hit 25) ===
    "exo-cbx": {"genre": "K-Pop, Pop", "mood": "Bright, varied, polished", "style": "EXO-CBX subunit, varied pop", "vocal_style": "Varies by member, bright, polished", "instruments": "K-Pop production, varied, layered", "production": "K-Pop polish, bright, layered"},
    "exo-sc": {"genre": "K-Pop, R&B", "mood": "Soulful, polished, varied", "style": "EXO-SC subunit, R&B-hip-hop blend", "vocal_style": "Varies by member, soulful, polished", "instruments": "K-Pop production, R&B, hip-hop", "production": "K-Pop polish, soulful, layered"},
    "got7": {"genre": "K-Pop, Hip-Hop", "mood": "Energetic, varied, dynamic", "style": "K-Pop boy group, hip-hop and pop blend", "vocal_style": "Varies by member, energetic, polished", "instruments": "K-Pop production, hip-hop, pop", "production": "K-Pop polish, energetic, layered"},

    # === Latin (top-up to 25) ===
    "shakira alt": {"genre": "Latin Pop, Reggaeton", "mood": "Energetic, varied, global", "style": "Colombian-Lebanese Latin pop pioneer, global", "vocal_style": "Shakira, distinctive, dynamic, varied", "instruments": "Latin percussion, pop production, varied", "production": "Latin pop polish, global, layered"},
    "jennifer lopez": {"genre": "Latin Pop, Dance-Pop", "mood": "Confident, danceable, varied", "style": "Puerto Rican-American Latin pop and dance-pop", "vocal_style": "J.Lo, confident, dynamic, varied", "instruments": "Latin percussion, dance-pop, varied", "production": "Latin pop polish, danceable, layered"},
    "ricky martin": {"genre": "Latin Pop, Dance-Pop", "mood": "Energetic, sensual, global", "style": "Puerto Rican Latin pop pioneer, 'Livin' La Vida Loca' era", "vocal_style": "Ricky Martin, energetic, distinctive, dynamic", "instruments": "Latin percussion, dance-pop, varied", "production": "Latin pop polish, energetic, layered"},
    "enrique iglesias": {"genre": "Latin Pop", "mood": "Romantic, smooth, global", "style": "Spanish-Latin pop, global crossover", "vocal_style": "Enrique, smooth, distinctive, dynamic", "instruments": "Latin pop production, varied, layered", "production": "Latin pop polish, smooth, layered"},
    "juanes": {"genre": "Latin Pop, Rock", "mood": "Passionate, varied, Colombian", "style": "Colombian rock-Latin pop, passionate", "vocal_style": "Juanes, passionate, distinctive, dynamic", "instruments": "Rock guitar, Latin percussion, varied", "production": "Latin pop-rock polish, passionate, layered"},
    "maluma": {"genre": "Reggaeton, Latin Pop", "mood": "Romantic, modern, global", "style": "Colombian reggaeton-Latin pop, global", "vocal_style": "Maluma, smooth, distinctive, dynamic", "instruments": "Reggaeton, Latin pop, varied", "production": "Latin pop polish, modern, layered"},
    "j balvin": {"genre": "Reggaeton, Latin Pop", "mood": "Varied, modern, global", "style": "Colombian reggaeton pioneer, global", "vocal_style": "J Balvin, distinctive, dynamic, varied", "instruments": "Reggaeton, Latin pop, varied", "production": "Latin pop polish, modern, layered"},
    "ozuna": {"genre": "Reggaeton, Latin Pop", "mood": "Romantic, smooth, global", "style": "Puerto Rican reggaeton, global crossover", "vocal_style": "Ozuna, smooth, distinctive, dynamic", "instruments": "Reggaeton, Latin pop, varied", "production": "Latin pop polish, smooth, layered"},
    "daddy yankee alt": {"genre": "Reggaeton, Latin Pop", "mood": "Energetic, foundational, global", "style": "Puerto Rican reggaeton pioneer, 'Gasolina' era", "vocal_style": "Daddy Yankee, energetic, distinctive, dynamic", "instruments": "Reggaeton, Latin pop, varied", "production": "Latin pop polish, energetic, layered"},
    "nicky jam": {"genre": "Reggaeton, Latin Pop", "mood": "Romantic, varied, global", "style": "Puerto Rican reggaeton, global crossover", "vocal_style": "Nicky Jam, smooth, distinctive, dynamic", "instruments": "Reggaeton, Latin pop, varied", "production": "Latin pop polish, romantic, layered"},
    "anuel aa": {"genre": "Reggaeton, Latin Trap", "mood": "Street, varied, modern", "style": "Puerto Rican Latin trap-reggaeton, raw", "vocal_style": "Anuel AA, raw, distinctive, dynamic", "instruments": "Reggaeton, Latin trap, varied", "production": "Latin trap polish, raw, layered"},
    "rauw alejandro": {"genre": "Reggaeton, Latin Pop", "mood": "Varied, modern, eclectic", "style": "Puerto Rican reggaeton, eclectic and modern", "vocal_style": "Rauw Alejandro, distinctive, dynamic, varied", "instruments": "Reggaeton, varied, layered", "production": "Latin pop polish, modern, layered"},
    "bad bunny alt": {"genre": "Reggaeton, Latin Trap", "mood": "Varied, eclectic, global", "style": "Puerto Rican reggaeton pioneer, global phenomenon", "vocal_style": "Bad Bunny, distinctive, dynamic, varied", "instruments": "Reggaeton, varied, eclectic", "production": "Latin pop polish, eclectic, layered"},
    "karol g": {"genre": "Reggaeton, Latin Pop", "mood": "Empowering, varied, global", "style": "Colombian reggaeton-Latin pop, global crossover", "vocal_style": "Karol G, empowering, distinctive, dynamic", "instruments": "Reggaeton, Latin pop, varied", "production": "Latin pop polish, empowering, layered"},
    "feid": {"genre": "Reggaeton, Latin Pop", "mood": "Smooth, varied, modern", "style": "Colombian reggaeton, modern", "vocal_style": "Feid, smooth, distinctive, dynamic", "instruments": "Reggaeton, varied, layered", "production": "Latin pop polish, modern, layered"},
    "mora": {"genre": "Reggaeton, Latin R&B", "mood": "Romantic, varied, modern", "style": "Puerto Rican reggaeton-Latin R&B, romantic", "vocal_style": "Mora, smooth, distinctive, dynamic", "instruments": "Reggaeton, Latin R&B, varied", "production": "Latin R&B polish, romantic, layered"},
    "sech": {"genre": "Reggaeton, Latin Pop", "mood": "Romantic, varied, modern", "style": "Panamanian reggaeton, romantic", "vocal_style": "Sech, smooth, distinctive, dynamic", "instruments": "Reggaeton, varied, layered", "production": "Latin pop polish, romantic, layered"},
    "myke towers": {"genre": "Reggaeton, Latin Trap", "mood": "Varied, modern, eclectic", "style": "Puerto Rican reggaeton-Latin trap, modern", "vocal_style": "Myke Towers, distinctive, dynamic, varied", "instruments": "Reggaeton, Latin trap, varied", "production": "Latin trap polish, modern, layered"},
    "arcangel": {"genre": "Reggaeton, Latin Pop", "mood": "Smooth, varied, foundational", "style": "Puerto Rican reggaeton pioneer, foundational", "vocal_style": "Arcangel, smooth, distinctive, dynamic", "instruments": "Reggaeton, varied, layered", "production": "Latin pop polish, smooth, layered"},
    "de la ghetto": {"genre": "Reggaeton, Latin Pop", "mood": "Romantic, varied, foundational", "style": "Puerto Rican reggaeton, romantic foundational", "vocal_style": "De La Ghetto, smooth, distinctive, dynamic", "instruments": "Reggaeton, varied, layered", "production": "Latin pop polish, romantic, layered"},
    "ivy queen": {"genre": "Reggaeton, Latin Pop", "mood": "Empowering, varied, foundational", "style": "Puerto Rican reggaeton pioneer, female reggaeton", "vocal_style": "Ivy Queen, empowering, distinctive, dynamic", "instruments": "Reggaeton, varied, layered", "production": "Latin pop polish, empowering, layered"},
    "residente": {"genre": "Latin, Hip-Hop", "mood": "Conscious, varied, Puerto Rican", "style": "Calle 13 alum, conscious Latin hip-hop", "vocal_style": "Residente, versatile, distinctive, dynamic", "instruments": "Latin, hip-hop, varied", "production": "Latin hip-hop polish, conscious, layered"},
    "calle 13": {"genre": "Latin, Hip-Hop", "mood": "Conscious, varied, Puerto Rican", "style": "Puerto Rican Latin hip-hop, Grammy-winning", "vocal_style": "Residente + Visitante, distinctive, dynamic", "instruments": "Latin, hip-hop, varied", "production": "Latin hip-hop polish, conscious, layered"},
    "mana": {"genre": "Latin Pop, Rock", "mood": "Anthemic, varied, Mexican", "style": "Mexican rock-Latin pop, anthemic", "vocal_style": "Fher Olvera, distinctive, dynamic, varied", "instruments": "Rock guitar, Latin percussion, varied", "production": "Latin pop-rock polish, anthemic, layered"},

    # === Country (top-up to 25) ===
    "johnny cash": {"genre": "Country, Outlaw Country", "mood": "Gritty, deep, storytelling", "style": "Man in Black, country legend, deep storytelling", "vocal_style": "Johnny Cash, deep baritone, distinctive, raw", "instruments": "Acoustic guitar, simple drums, varied", "production": "Raw country polish, minimal, varied"},
    "dolly parton": {"genre": "Country, Country-Pop", "mood": "Joyful, varied, storytelling", "style": "Country-pop icon, storytelling and camp", "vocal_style": "Dolly, distinctive soprano, varied, dynamic", "instruments": "Acoustic guitar, fiddle, varied", "production": "Country polish, varied, layered"},
    "willie nelson": {"genre": "Country, Outlaw Country", "mood": "Laid-back, varied, iconic", "style": "Outlaw country legend, Red Headed Stranger era", "vocal_style": "Willie, distinctive, varied, dynamic", "instruments": "Trigger guitar, varied, layered", "production": "Country polish, raw, varied"},
    "george jones": {"genre": "Country, Honky-Tonk", "mood": "Heartbroken, varied, storytelling", "style": "Possum of country, honky-tonk legend", "vocal_style": "George Jones, distinctive, emotional, dynamic", "instruments": "Acoustic guitar, fiddle, varied", "production": "Country polish, honky-tonk, varied"},
    "george strait": {"genre": "Country, Honky-Tonk", "mood": "Traditional, varied, storytelling", "style": "King of country, traditional honky-tonk", "vocal_style": "George Strait, smooth, distinctive, dynamic", "instruments": "Acoustic guitar, fiddle, varied", "production": "Country polish, traditional, varied"},
    "luke bryan": {"genre": "Country, Country-Pop", "mood": "Energetic, party, varied", "style": "Modern country-pop, party anthems", "vocal_style": "Luke Bryan, smooth, distinctive, dynamic", "instruments": "Acoustic guitar, drums, varied", "production": "Modern country polish, party, layered"},
    "jason aldean": {"genre": "Country, Country-Rock", "mood": "Anthemic, varied, modern", "style": "Modern country-rock anthems", "vocal_style": "Jason Aldean, distinctive, dynamic, varied", "instruments": "Electric guitar, drums, varied", "production": "Modern country-rock polish, anthemic, layered"},
    "florida georgia line": {"genre": "Country, Country-Pop", "mood": "Party, varied, modern", "style": "Modern country-pop, bro-country pioneers", "vocal_style": "Tyler Hubbard + Brian Kelley, varied, dynamic", "instruments": "Country-pop production, varied, layered", "production": "Modern country-pop polish, party, layered"},
    "thomas rhett": {"genre": "Country, Country-Pop", "mood": "Modern, varied, pop", "style": "Modern country-pop, pop crossovers", "vocal_style": "Thomas Rhett, smooth, distinctive, dynamic", "instruments": "Country-pop production, varied, layered", "production": "Modern country-pop polish, pop, layered"},
    "maren morris": {"genre": "Country, Country-Pop", "mood": "Empowering, varied, modern", "style": "Modern country-pop, empowering", "vocal_style": "Maren Morris, distinctive, dynamic, varied", "instruments": "Country-pop production, varied, layered", "production": "Modern country-pop polish, empowering, layered"},
    "kacey musgraves": {"genre": "Country, Country-Pop", "mood": "Vintage, varied, thoughtful", "style": "Modern country, vintage-influenced, thoughtful", "vocal_style": "Kacey, distinctive, varied, dynamic", "instruments": "Country production, varied, layered", "production": "Modern country polish, vintage, layered"},
    "chris stapleton": {"genre": "Country, Southern Rock", "mood": "Gritty, varied, soulful", "style": "Modern soulful country-southern rock", "vocal_style": "Chris Stapleton, gritty, distinctive, dynamic", "instruments": "Electric guitar, varied, layered", "production": "Modern country-southern rock polish, gritty, layered"},
    "sturgill simpson": {"genre": "Country, Outlaw Country", "mood": "Outlaw, varied, eclectic", "style": "Outlaw country with rock and psychedelic edge", "vocal_style": "Sturgill, distinctive, varied, dynamic", "instruments": "Country-rock guitar, varied, layered", "production": "Outlaw country polish, eclectic, varied"},
    "jason isbell": {"genre": "Country, Americana", "mood": "Storytelling, varied, thoughtful", "style": "Americana country, storytelling songwriter", "vocal_style": "Jason Isbell, distinctive, varied, dynamic", "instruments": "Acoustic guitar, varied, layered", "production": "Americana polish, thoughtful, varied"},
    "tyler childers": {"genre": "Country, Appalachian", "mood": "Appalachian, varied, raw", "style": "Appalachian country, raw and authentic", "vocal_style": "Tyler Childers, distinctive, raw, varied", "instruments": "Acoustic guitar, fiddle, varied", "production": "Appalachian country polish, raw, varied"},
    "zach bryan": {"genre": "Country, Americana", "mood": "Raw, varied, modern", "style": "Modern Americana country, raw and authentic", "vocal_style": "Zach Bryan, raw, distinctive, varied", "instruments": "Acoustic guitar, varied, layered", "production": "Americana polish, raw, varied"},
    "whitney dunn": {"genre": "Country, Outlaw Country", "mood": "Storytelling, varied, outlaw", "style": "Modern outlaw country, narrative songwriter", "vocal_style": "Whitney Dunn, distinctive, varied, dynamic", "instruments": "Acoustic guitar, varied, layered", "production": "Outlaw country polish, varied, layered"},
    "kenny chesney": {"genre": "Country, Country-Pop", "mood": "Sunny, varied, beach", "style": "Modern country-pop, beach and island vibes", "vocal_style": "Kenny Chesney, smooth, distinctive, dynamic", "instruments": "Country-pop production, varied, layered", "production": "Modern country polish, beach, varied"},
    "tim mcgraw": {"genre": "Country, Country-Pop", "mood": "Heartfelt, varied, modern", "style": "Modern country-pop, heartfelt anthems", "vocal_style": "Tim McGraw, smooth, distinctive, dynamic", "instruments": "Country-pop production, varied, layered", "production": "Modern country polish, heartfelt, varied"},
    "blake shelton": {"genre": "Country, Country-Pop", "mood": "Heartfelt, varied, mainstream", "style": "Modern mainstream country, heartfelt", "vocal_style": "Blake Shelton, distinctive, varied, dynamic", "instruments": "Country-pop production, varied, layered", "production": "Modern country polish, mainstream, varied"},
    "brad paisley": {"genre": "Country, Country-Rock", "mood": "Playful, varied, virtuosic", "style": "Modern country-rock, virtuosic guitar", "vocal_style": "Brad Paisley, smooth, distinctive, dynamic", "instruments": "Virtuosic country guitar, varied, layered", "production": "Modern country polish, virtuosic, varied"},
    "tanya tucker": {"genre": "Country, Outlaw Country", "mood": "Gritty, varied, raw", "style": "Outlaw country legend, raw and powerful", "vocal_style": "Tanya Tucker, gritty, distinctive, dynamic", "instruments": "Acoustic guitar, varied, layered", "production": "Outlaw country polish, gritty, varied"},
    "emmylou harris": {"genre": "Country, Americana", "mood": "Ethereal, varied, Americana", "style": "Country-Americana legend, ethereal harmonies", "vocal_style": "Emmylou, ethereal soprano, distinctive, dynamic", "instruments": "Acoustic guitar, varied, layered", "production": "Country-Americana polish, ethereal, varied"},
    "linda ronstadt": {"genre": "Country, Country-Rock", "mood": "Soulful, varied, eclectic", "style": "Country-rock-pop legend, eclectic", "vocal_style": "Linda Ronstadt, soulful, distinctive, dynamic", "instruments": "Country-rock guitar, varied, layered", "production": "Country-rock polish, eclectic, varied"},

    # === Indian Indie (top-up to 25) ===
    "prateek kuhad": {"genre": "Indian Indie, Indie Folk", "mood": "Intimate, melancholic, romantic", "style": "Indian indie folk singer-songwriter, global", "vocal_style": "Prateek Kuhad, intimate, distinctive, varied", "instruments": "Acoustic guitar, minimal indie production", "production": "Indie polish, intimate, layered"},
    "arijit singh": {"genre": "Indian Indie, Bollywood", "mood": "Romantic, soulful, varied", "style": "Indian playback singer, Bollywood and indie", "vocal_style": "Arijit Singh, soulful, distinctive, dynamic", "instruments": "Bollywood-indie production, varied, layered", "production": "Bollywood-indie polish, soulful, varied"},
    "shreya ghoshal": {"genre": "Indian Indie, Bollywood", "mood": "Soulful, romantic, varied", "style": "Indian playback singer, Bollywood and indie", "vocal_style": "Shreya Ghoshal, soulful soprano, distinctive, dynamic", "instruments": "Bollywood-indie production, varied, layered", "production": "Bollywood-indie polish, soulful, varied"},
    "badshah": {"genre": "Indian Indie, Desi Hip-Hop", "mood": "Energetic, varied, Bollywood-hip-hop", "style": "Indian hip-hop-Bollywood crossover, energetic", "vocal_style": "Badshah, energetic, distinctive, dynamic", "instruments": "Hip-hop, Bollywood production, varied", "production": "Bollywood-hip-hop polish, energetic, layered"},
    "yo yo honey singh": {"genre": "Indian Indie, Desi Hip-Hop", "mood": "Party, varied, Bollywood-hip-hop", "style": "Indian hip-hop-Bollywood pioneer, party", "vocal_style": "Yo Yo Honey Singh, party, distinctive, dynamic", "instruments": "Hip-hop, Bollywood production, varied", "production": "Bollywood-hip-hop polish, party, layered"},
    "ritviz": {"genre": "Indian Indie, Electronic", "mood": "Energetic, varied, Indian-electronic", "style": "Indian electronic-indie, festival", "vocal_style": "Ritviz, energetic, distinctive, dynamic", "instruments": "Indian-electronic production, varied, layered", "production": "Indian-electronic polish, energetic, layered"},
    "nucleya": {"genre": "Indian Indie, Bass Music", "mood": "Energetic, varied, bass-heavy", "style": "Indian bass-electronic pioneer, festival", "vocal_style": "Featured vocalists, varied, dynamic", "instruments": "Indian bass production, varied, layered", "production": "Indian bass polish, energetic, layered"},
    "divine": {"genre": "Indian Indie, Desi Hip-Hop", "mood": "Street, varied, Mumbai hip-hop", "style": "Indian street hip-hop, Mumbai pioneer", "vocal_style": "Divine, street, distinctive, dynamic", "instruments": "Hip-hop, Indian production, varied", "production": "Indian hip-hop polish, street, layered"},
    "emiway bantai": {"genre": "Indian Indie, Desi Hip-Hop", "mood": "Street, varied, Mumbai hip-hop", "style": "Indian street hip-hop, Mumbai pioneer", "vocal_style": "Emiway, street, distinctive, dynamic", "instruments": "Hip-hop, Indian production, varied", "production": "Indian hip-hop polish, street, layered"},
    "raftaar": {"genre": "Indian Indie, Desi Hip-Hop", "mood": "Varied, modern, hip-hop", "style": "Indian hip-hop-Bollywood crossover, varied", "vocal_style": "Raftaar, varied, distinctive, dynamic", "instruments": "Hip-hop, Bollywood production, varied", "production": "Indian hip-hop polish, varied, layered"},
    "anuv jain": {"genre": "Indian Indie, Indie Pop", "mood": "Romantic, varied, modern", "style": "Indian indie pop singer-songwriter, romantic", "vocal_style": "Anuv Jain, romantic, distinctive, dynamic", "instruments": "Acoustic guitar, indie production, varied", "production": "Indie polish, romantic, varied"},
    "the local train": {"genre": "Indian Indie, Rock", "mood": "Anthemic, varied, Indian rock", "style": "Indian indie rock band, anthemic", "vocal_style": "Raman Negi, distinctive, dynamic, varied", "instruments": "Rock guitar, Indian production, varied", "production": "Indian rock polish, anthemic, varied"},
    "when chai met toast": {"genre": "Indian Indie, Indie Pop", "mood": "Romantic, varied, indie pop", "style": "Indian indie pop band, romantic", "vocal_style": "Varies by member, romantic, varied", "instruments": "Indie pop production, varied, layered", "production": "Indian indie polish, romantic, varied"},
    "the yellow diary": {"genre": "Indian Indie, Indie Pop", "mood": "Atmospheric, varied, modern", "style": "Indian indie pop, atmospheric", "vocal_style": "Varies by member, atmospheric, varied", "instruments": "Indie pop production, varied, layered", "production": "Indian indie polish, atmospheric, varied"},
    "dualipa indian": {"genre": "Indian Indie, Indie Pop", "mood": "Modern, varied, indie pop", "style": "Indian indie pop, Dua Lipa inspired", "vocal_style": "Varies, smooth, dynamic, varied", "instruments": "Indie pop production, varied, layered", "production": "Indian indie polish, modern, varied"},
    "gs buttar": {"genre": "Indian Indie, Desi Hip-Hop", "mood": "Punjabi, varied, hip-hop", "style": "Punjabi desi hip-hop, varied", "vocal_style": "GS Buttlar, distinctive, dynamic, varied", "instruments": "Punjabi-hip-hop production, varied, layered", "production": "Punjabi-hip-hop polish, varied, layered"},
    "diljit dosanjh": {"genre": "Indian Indie, Punjabi Pop", "mood": "Varied, polished, Punjabi", "style": "Punjabi pop-hip-hop crossover, global", "vocal_style": "Diljit, distinctive, dynamic, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, varied, layered"},
    "ammy virk": {"genre": "Indian Indie, Punjabi Pop", "mood": "Romantic, varied, Punjabi", "style": "Punjabi pop, romantic and varied", "vocal_style": "Ammy Virk, romantic, distinctive, dynamic", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "guru randhawa": {"genre": "Indian Indie, Punjabi Pop", "mood": "Romantic, varied, Punjabi", "style": "Punjabi pop-Bollywood crossover, romantic", "vocal_style": "Guru Randhawa, romantic, distinctive, dynamic", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "ap dhillon": {"genre": "Indian Indie, Punjabi Pop", "mood": "Modern, varied, Punjabi", "style": "Punjabi pop with global hip-hop influence", "vocal_style": "AP Dhillon, distinctive, dynamic, varied", "instruments": "Punjabi-hip-hop production, varied, layered", "production": "Punjabi-hip-hop polish, modern, varied"},
    "shubh": {"genre": "Indian Indie, Punjabi Pop", "mood": "Modern, varied, Punjabi", "style": "Punjabi pop-hip-hop, global crossover", "vocal_style": "Shubh, distinctive, dynamic, varied", "instruments": "Punjabi-hip-hop production, varied, layered", "production": "Punjabi-hip-hop polish, modern, varied"},
    "sidhu moosewala": {"genre": "Indian Indie, Punjabi Hip-Hop", "mood": "Street, varied, Punjabi", "style": "Punjabi hip-hop legend, late pioneer", "vocal_style": "Sidhu Moosewala, distinctive, dynamic, varied", "instruments": "Punjabi-hip-hop production, varied, layered", "production": "Punjabi-hip-hop polish, street, layered"},

    # === Italian (top-up to 25) ===
    "måneskin": {"genre": "Italian Rock, Pop Rock", "mood": "Energetic, varied, Eurovision", "style": "Italian rock band, Eurovision winner, global", "vocal_style": "Damiano David, distinctive, dynamic, varied", "instruments": "Rock guitar, Italian pop, varied", "production": "Italian pop-rock polish, energetic, layered"},
    "gianna nannini": {"genre": "Italian Pop, Rock", "mood": "Powerful, varied, Italian rock", "style": "Italian rock-pop legend, powerful", "vocal_style": "Gianna Nannini, powerful, distinctive, dynamic", "instruments": "Rock guitar, Italian pop, varied", "production": "Italian pop-rock polish, powerful, varied"},
    "loredana berte": {"genre": "Italian Pop, Rock", "mood": "Bold, varied, Italian rock", "style": "Italian rock-pop legend, bold", "vocal_style": "Loredana Berte, bold, distinctive, dynamic", "instruments": "Rock guitar, Italian pop, varied", "production": "Italian pop-rock polish, bold, layered"},
    "francesco de gregori": {"genre": "Italian Pop, Folk", "mood": "Poetic, varied, Italian folk", "style": "Italian folk-pop legend, poetic", "vocal_style": "Francesco De Gregori, distinctive, dynamic, varied", "instruments": "Italian folk-pop, varied, layered", "production": "Italian folk polish, poetic, varied"},
    "fabrizio de andre": {"genre": "Italian Pop, Folk", "mood": "Poetic, varied, Italian folk", "style": "Italian folk legend, late great", "vocal_style": "Fabrizio De Andre, distinctive, dynamic, varied", "instruments": "Italian folk, varied, layered", "production": "Italian folk polish, poetic, varied"},
    "lucio battisti": {"genre": "Italian Pop, Prog", "mood": "Innovative, varied, Italian pop", "style": "Italian pop-prog pioneer, innovative", "vocal_style": "Lucio Battisti, distinctive, dynamic, varied", "instruments": "Italian pop-prog, varied, layered", "production": "Italian pop polish, innovative, varied"},
    "mina": {"genre": "Italian Pop, Soul", "mood": "Powerful, varied, Italian pop", "style": "Italian pop-soul legend, powerful", "vocal_style": "Mina, powerful, distinctive, dynamic", "instruments": "Italian pop-soul, varied, layered", "production": "Italian pop polish, powerful, varied"},
    "adriano celentano": {"genre": "Italian Pop, Rock", "mood": "Energetic, varied, Italian rock", "style": "Italian rock-pop legend, energetic", "vocal_style": "Celentano, distinctive, dynamic, varied", "instruments": "Rock, Italian pop, varied", "production": "Italian pop-rock polish, energetic, varied"},
    "eugenio finardi": {"genre": "Italian Rock, Pop", "mood": "Varied, Italian rock", "style": "Italian rock legend, varied", "vocal_style": "Eugenio Finardi, distinctive, dynamic, varied", "instruments": "Rock, Italian pop, varied", "production": "Italian pop-rock polish, varied, layered"},
    "vasco rossi": {"genre": "Italian Rock, Pop", "mood": "Anthemic, varied, Italian rock", "style": "Italian rock legend, stadium anthems", "vocal_style": "Vasco Rossi, distinctive, dynamic, varied", "instruments": "Rock guitar, Italian pop, varied", "production": "Italian pop-rock polish, anthemic, layered"},
    "luciano ligabue": {"genre": "Italian Rock, Pop", "mood": "Anthemic, varied, Italian rock", "style": "Italian rock-pop legend, arena", "vocal_style": "Ligabue, distinctive, dynamic, varied", "instruments": "Rock guitar, Italian pop, varied", "production": "Italian pop-rock polish, anthemic, layered"},
    "gianna nannini alt": {"genre": "Italian Pop, Rock", "mood": "Powerful, varied, Italian rock", "style": "Italian rock-pop legend, powerful", "vocal_style": "Gianna Nannini, powerful, distinctive, dynamic", "instruments": "Rock guitar, Italian pop, varied", "production": "Italian pop-rock polish, powerful, varied"},
    "ermal meta": {"genre": "Italian Pop, Indie", "mood": "Introspective, varied, Italian", "style": "Italian indie-pop, Eurovision alum", "vocal_style": "Ermal Meta, distinctive, dynamic, varied", "instruments": "Italian indie-pop, varied, layered", "production": "Italian indie polish, introspective, varied"},
    "francesco gabbani": {"genre": "Italian Pop, Indie", "mood": "Playful, varied, Italian", "style": "Italian indie-pop, Eurovision alum", "vocal_style": "Francesco Gabbani, distinctive, dynamic, varied", "instruments": "Italian indie-pop, varied, layered", "production": "Italian indie polish, playful, varied"},
    "la rappresentante di lista": {"genre": "Italian Pop, Indie", "mood": "Eclectic, varied, Italian", "style": "Italian eclectic indie-pop, Eurovision alum", "vocal_style": "Veronica Lucchesi, distinctive, dynamic, varied", "instruments": "Italian indie-pop, varied, eclectic", "production": "Italian indie polish, eclectic, varied"},
    "mahmood": {"genre": "Italian Pop, R&B", "mood": "Modern, varied, Italian", "style": "Italian pop-R&B, Sanremo winner", "vocal_style": "Mahmood, distinctive, dynamic, varied", "instruments": "Italian pop-R&B, varied, layered", "production": "Italian pop polish, modern, varied"},
    "blanco": {"genre": "Italian Pop, Trap", "mood": "Modern, varied, Italian", "style": "Italian pop-trap, Sanremo winner", "vocal_style": "Blanco, distinctive, dynamic, varied", "instruments": "Italian pop-trap, varied, layered", "production": "Italian pop polish, modern, varied"},
    "anastasio": {"genre": "Italian Pop, Hip-Hop", "mood": "Modern, varied, Italian", "style": "Italian pop-hip-hop, Sanremo alum", "vocal_style": "Anastasio, distinctive, dynamic, varied", "instruments": "Italian pop-hip-hop, varied, layered", "production": "Italian pop polish, modern, varied"},
    "ultimo": {"genre": "Italian Pop, Indie", "mood": "Introspective, varied, Italian", "style": "Italian pop-songwriter, Sanremo winner", "vocal_style": "Ultimo, distinctive, dynamic, varied", "instruments": "Italian pop-indie, varied, layered", "production": "Italian pop polish, introspective, varied"},
    "irama": {"genre": "Italian Pop, R&B", "mood": "Modern, varied, Italian", "style": "Italian pop-R&B, Sanremo alum", "vocal_style": "Irama, distinctive, dynamic, varied", "instruments": "Italian pop-R&B, varied, layered", "production": "Italian pop polish, modern, varied"},
    "giorgia": {"genre": "Italian Pop, Soul", "mood": "Powerful, varied, Italian", "style": "Italian pop-soul legend, powerful", "vocal_style": "Giorgia, powerful, distinctive, dynamic", "instruments": "Italian pop-soul, varied, layered", "production": "Italian pop polish, powerful, varied"},
    "elio": {"genre": "Italian Pop, Variety", "mood": "Eclectic, varied, Italian", "style": "Italian pop variety, Sanremo legend", "vocal_style": "Elio, distinctive, dynamic, varied", "instruments": "Italian pop, varied, eclectic", "production": "Italian pop polish, eclectic, varied"},
    "the zebda": {"genre": "Italian Pop, World", "mood": "Eclectic, varied, world-influenced", "style": "Italian-French world pop, eclectic", "vocal_style": "Varies by member, distinctive, dynamic", "instruments": "World-influenced Italian pop, varied, layered", "production": "Italian world-pop polish, eclectic, varied"},
    "giorgio gaber": {"genre": "Italian Pop, Folk", "mood": "Theatrical, varied, Italian", "style": "Italian theatrical folk-pop, late legend", "vocal_style": "Giorgio Gaber, distinctive, dynamic, varied", "instruments": "Italian folk-pop, varied, layered", "production": "Italian folk polish, theatrical, varied"},

    # === Bedroom Pop (top-up to 25) ===
    "clairo": {"genre": "Bedroom Pop, Indie Pop", "mood": "Intimate, varied, lo-fi", "style": "Bedroom pop pioneer, intimate lo-fi", "vocal_style": "Clairo, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, intimate"},
    "beabadoobee": {"genre": "Bedroom Pop, Indie Rock", "mood": "Intimate, varied, lo-fi", "style": "British-Filipino bedroom pop, indie rock", "vocal_style": "Beabadoobee, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "alex g": {"genre": "Bedroom Pop, Indie", "mood": "Lo-fi, varied, indie", "style": "American bedroom pop, indie stalwart", "vocal_style": "Alex G, lo-fi, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "frankie cosmos": {"genre": "Bedroom Pop, Indie Pop", "mood": "Intimate, varied, lo-fi", "style": "American bedroom pop, prolific", "vocal_style": "Frankie Cosmos, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "current joys": {"genre": "Bedroom Pop, Indie", "mood": "Lo-fi, varied, dreamy", "style": "American bedroom pop, lo-fi dream pop", "vocal_style": "Current Joys, lo-fi, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, dreamy"},
    "r nilotpal": {"genre": "Bedroom Pop, Indie", "mood": "Lo-fi, varied, dreamy", "style": "Indian bedroom pop, lo-fi dream pop", "vocal_style": "R Nilotpal, lo-fi, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "mellow fellow": {"genre": "Bedroom Pop, Dream Pop", "mood": "Lo-fi, varied, dreamy", "style": "Chillwave-bedroom pop, lo-fi dream", "vocal_style": "Mellow Fellow, lo-fi, distinctive, varied", "instruments": "Lo-fi chillwave production, varied, layered", "production": "Bedroom pop polish, lo-fi, dreamy"},
    "heroine": {"genre": "Bedroom Pop, Indie", "mood": "Intimate, varied, lo-fi", "style": "Bedroom pop, intimate", "vocal_style": "Heroine, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, intimate"},
    "tomo": {"genre": "Bedroom Pop, Indie", "mood": "Lo-fi, varied, indie", "style": "Bedroom pop, lo-fi", "vocal_style": "Tomo, lo-fi, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "boy pablo": {"genre": "Bedroom Pop, Indie Pop", "mood": "Nostalgic, varied, indie", "style": "Norwegian bedroom pop, indie pop", "vocal_style": "Boy Pablo, nostalgic, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, nostalgic"},
    "the vaccines": {"genre": "Bedroom Pop, Indie Rock", "mood": "Energetic, varied, indie", "style": "British bedroom pop meets indie rock", "vocal_style": "Justin Young, energetic, distinctive, varied", "instruments": "Indie rock guitar, varied, layered", "production": "Bedroom pop polish, indie, varied"},
    "gretel hanlyn": {"genre": "Bedroom Pop, Indie", "mood": "Intimate, varied, lo-fi", "style": "American bedroom pop, lo-fi", "vocal_style": "Gretel Hanlyn, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, intimate"},
    "soccer mommy": {"genre": "Bedroom Pop, Indie Rock", "mood": "Intimate, varied, indie", "style": "American bedroom pop-meets-indie rock", "vocal_style": "Soccer Mommy, intimate, distinctive, varied", "instruments": "Indie rock guitar, varied, layered", "production": "Bedroom pop polish, indie, varied"},
    "snail mail": {"genre": "Bedroom Pop, Indie Rock", "mood": "Intimate, varied, indie", "style": "American bedroom pop-meets-indie rock", "vocal_style": "Snail Mail, intimate, distinctive, varied", "instruments": "Indie rock guitar, varied, layered", "production": "Bedroom pop polish, indie, varied"},
    "phoebe bridgers": {"genre": "Bedroom Pop, Indie", "mood": "Intimate, varied, lo-fi", "style": "American bedroom pop-meets-indie", "vocal_style": "Phoebe Bridgers, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "conan gray": {"genre": "Bedroom Pop, Indie Pop", "mood": "Intimate, varied, lo-fi", "style": "American bedroom pop, YouTube era", "vocal_style": "Conan Gray, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "mxmtoon": {"genre": "Bedroom Pop, Indie Pop", "mood": "Intimate, varied, lo-fi", "style": "American bedroom pop, YouTube era", "vocal_style": "mxmtoon, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "gigi burg": {"genre": "Bedroom Pop, Indie", "mood": "Intimate, varied, lo-fi", "style": "Bedroom pop, lo-fi", "vocal_style": "Gigi Burg, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "sasha sloan": {"genre": "Bedroom Pop, Pop", "mood": "Intimate, varied, lo-fi", "style": "American bedroom pop-meets-mainstream", "vocal_style": "Sasha Sloan, intimate, distinctive, varied", "instruments": "Lo-fi pop production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "jodie abernethy": {"genre": "Bedroom Pop, Indie", "mood": "Intimate, varied, lo-fi", "style": "Bedroom pop, lo-fi", "vocal_style": "Jodie Abernethy, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "grentperez": {"genre": "Bedroom Pop, Indie", "mood": "Intimate, varied, lo-fi", "style": "Filipino-Australian bedroom pop, lo-fi", "vocal_style": "grentperez, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "cavetown": {"genre": "Bedroom Pop, Indie", "mood": "Intimate, varied, lo-fi", "style": "British bedroom pop, lo-fi", "vocal_style": "Cavetown, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "rxseboy": {"genre": "Bedroom Pop, Indie", "mood": "Intimate, varied, lo-fi", "style": "Bedroom pop-hip-hop, lo-fi", "vocal_style": "Rxseboy, intimate, distinctive, varied", "instruments": "Lo-fi hip-hop production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "gothbabe": {"genre": "Bedroom Pop, Indie", "mood": "Atmospheric, varied, lo-fi", "style": "Bedroom pop, lo-fi atmospheric", "vocal_style": "Gothbabe, atmospheric, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, varied"},
    "heroine alt": {"genre": "Bedroom Pop, Indie", "mood": "Intimate, varied, lo-fi", "style": "Bedroom pop, intimate", "vocal_style": "Heroine, intimate, distinctive, varied", "instruments": "Lo-fi indie production, varied, layered", "production": "Bedroom pop polish, lo-fi, intimate"},

    # === Hyperpop (top-up to 25) ===
    "sophie alt": {"genre": "Hyperpop, Pop", "mood": "Futuristic, varied, pop", "style": "Pioneering hyperpop producer, late legend", "vocal_style": "Processed, futuristic, distinctive, varied", "instruments": "Hard synths, 808s, futuristic", "production": "Hyperpop polish, futuristic, layered"},
    "a g cook": {"genre": "Hyperpop, PC Music", "mood": "Futuristic, varied, pop", "style": "PC Music founder, hyperpop pioneer", "vocal_style": "Processed, futuristic, distinctive, varied", "instruments": "Hard synths, futuristic, varied", "production": "Hyperpop polish, futuristic, layered"},
    "danny l harle": {"genre": "Hyperpop, PC Music", "mood": "Futuristic, varied, pop", "style": "PC Music producer, hyperpop pioneer", "vocal_style": "Processed, futuristic, distinctive, varied", "instruments": "Hard synths, futuristic, varied", "production": "Hyperpop polish, futuristic, layered"},
    "easyfun": {"genre": "Hyperpop, PC Music", "mood": "Futuristic, varied, pop", "style": "PC Music producer, hyperpop", "vocal_style": "Processed, futuristic, distinctive, varied", "instruments": "Hard synths, futuristic, varied", "production": "Hyperpop polish, futuristic, layered"},
    "hyd": {"genre": "Hyperpop, PC Music", "mood": "Futuristic, varied, pop", "style": "PC Music producer, hyperpop", "vocal_style": "Processed, futuristic, distinctive, varied", "instruments": "Hard synths, futuristic, varied", "production": "Hyperpop polish, futuristic, layered"},
    "gfoty": {"genre": "Hyperpop, PC Music", "mood": "Futuristic, varied, pop", "style": "PC Music producer, hyperpop", "vocal_style": "Processed, futuristic, distinctive, varied", "instruments": "Hard synths, futuristic, varied", "production": "Hyperpop polish, futuristic, layered"},
    "felly": {"genre": "Hyperpop, Alternative", "mood": "Energetic, varied, eclectic", "style": "American hyperpop-meets-alternative", "vocal_style": "Felly, energetic, distinctive, varied", "instruments": "Hyperpop production, varied, layered", "production": "Hyperpop polish, eclectic, varied"},
    "lil texas": {"genre": "Hyperpop, EDM", "mood": "Energetic, varied, dance", "style": "American hyperpop-EDM crossover", "vocal_style": "Lil Texas, energetic, distinctive, varied", "instruments": "Hard synths, dance, varied", "production": "Hyperpop polish, energetic, layered"},
    "soupandreas": {"genre": "Hyperpop, EDM", "mood": "Energetic, varied, dance", "style": "American hyperpop-EDM", "vocal_style": "Soupandreas, energetic, distinctive, varied", "instruments": "Hard synths, dance, varied", "production": "Hyperpop polish, energetic, layered"},
    "gupi": {"genre": "Hyperpop, Alternative", "mood": "Quirky, varied, eclectic", "style": "American hyperpop-meets-alternative", "vocal_style": "Gupi, quirky, distinctive, varied", "instruments": "Hyperpop production, varied, layered", "production": "Hyperpop polish, quirky, varied"},
    "underscores alt": {"genre": "Hyperpop, Indie", "mood": "Quirky, varied, eclectic", "style": "American hyperpop-meets-indie", "vocal_style": "underscores, quirky, distinctive, varied", "instruments": "Hyperpop production, varied, layered", "production": "Hyperpop polish, quirky, varied"},
    "machine girl": {"genre": "Hyperpop, Breakcore", "mood": "Chaotic, varied, breakcore", "style": "American breakcore-meets-hyperpop", "vocal_style": "Machine Girl, chaotic, distinctive, varied", "instruments": "Breakcore, hyperpop, varied", "production": "Hyperpop polish, chaotic, varied"},
    "object blue": {"genre": "Hyperpop, Techno", "mood": "Experimental, varied, techno", "style": "American hyperpop-meets-techno", "vocal_style": "Object Blue, experimental, distinctive, varied", "instruments": "Hyperpop-techno production, varied, layered", "production": "Hyperpop polish, experimental, varied"},
    "caterina barbieri": {"genre": "Hyperpop, Modular Synth", "mood": "Hypnotic, varied, modular", "style": "Italian modular synth pioneer", "vocal_style": "Minimal, processed, distinctive, varied", "instruments": "Modular synths, varied, layered", "production": "Hyperpop polish, hypnotic, varied"},
    "arca alt": {"genre": "Hyperpop, Electronic", "mood": "Experimental, varied, futuristic", "style": "Venezuelan hyperpop-electronic pioneer", "vocal_style": "Arca, experimental, distinctive, varied", "instruments": "Experimental hyperpop production, varied, layered", "production": "Hyperpop polish, experimental, varied"},
    "lotic": {"genre": "Hyperpop, Electronic", "mood": "Experimental, varied, futuristic", "style": "American hyperpop-electronic", "vocal_style": "Lotic, experimental, distinctive, varied", "instruments": "Experimental hyperpop production, varied, layered", "production": "Hyperpop polish, experimental, varied"},
    "shygirl": {"genre": "Hyperpop, Electronic", "mood": "Bold, varied, futuristic", "style": "British hyperpop-electronic", "vocal_style": "Shygirl, bold, distinctive, varied", "instruments": "Hyperpop-electronic production, varied, layered", "production": "Hyperpop polish, bold, varied"},
    "coucou chloe": {"genre": "Hyperpop, Electronic", "mood": "Bold, varied, futuristic", "style": "French hyperpop-electronic", "vocal_style": "Coucou Chloe, bold, distinctive, varied", "instruments": "Hyperpop-electronic production, varied, layered", "production": "Hyperpop polish, bold, varied"},
    "umru": {"genre": "Hyperpop, Electronic", "mood": "Eclectic, varied, futuristic", "style": "American hyperpop-electronic producer", "vocal_style": "Featured vocalists, varied, dynamic", "instruments": "Hyperpop-electronic production, varied, layered", "production": "Hyperpop polish, eclectic, varied"},
    "doss": {"genre": "Hyperpop, Pop", "mood": "Energetic, varied, futuristic", "style": "American hyperpop-meets-pop", "vocal_style": "Doss, energetic, distinctive, varied", "instruments": "Hyperpop production, varied, layered", "production": "Hyperpop polish, energetic, varied"},
    "zed lavergne": {"genre": "Hyperpop, EDM", "mood": "Energetic, varied, dance", "style": "American hyperpop-EDM", "vocal_style": "Zed Lavergne, energetic, distinctive, varied", "instruments": "Hyperpop-EDM production, varied, layered", "production": "Hyperpop polish, energetic, varied"},
    "magdalena bay": {"genre": "Hyperpop, Synth Pop", "mood": "Futuristic, varied, synth-pop", "style": "American hyperpop-meets-synth-pop", "vocal_style": "Mica Tenenbaum, futuristic, distinctive, varied", "instruments": "Hyperpop-synth production, varied, layered", "production": "Hyperpop polish, futuristic, varied"},
    "the scions": {"genre": "Hyperpop, Pop", "mood": "Energetic, varied, eclectic", "style": "American hyperpop-meets-pop", "vocal_style": "The Scions, energetic, distinctive, varied", "instruments": "Hyperpop production, varied, layered", "production": "Hyperpop polish, energetic, varied"},

    # === Indie (top-up to 25) ===
    "arctic monkeys alt": {"genre": "Indie Rock, Alternative", "mood": "Cool, varied, British", "style": "British indie rock icons, AM era", "vocal_style": "Alex Turner, smooth baritone, distinctive, varied", "instruments": "Indie rock guitar, varied, layered", "production": "Indie rock polish, atmospheric, varied"},
    "the strokes": {"genre": "Indie Rock, Alternative", "mood": "Cool, varied, garage", "style": "NYC garage-rock revival, Is This It era", "vocal_style": "Julian Casablancas, distinctive, dynamic, varied", "instruments": "Garage rock guitar, varied, layered", "production": "Indie rock polish, lo-fi, varied"},
    "the libertines": {"genre": "Indie Rock, Alternative", "mood": "Raw, varied, British", "style": "British indie rock, raw and poetic", "vocal_style": "Pete Doherty, distinctive, raw, varied", "instruments": "Indie rock guitar, varied, layered", "production": "Indie rock polish, raw, varied"},
    "franz ferdinand": {"genre": "Indie Rock, Post-Punk", "mood": "Energetic, varied, post-punk", "style": "Scottish indie rock, post-punk revival", "vocal_style": "Alex Kapranos, distinctive, dynamic, varied", "instruments": "Post-punk guitar, varied, layered", "production": "Indie rock polish, post-punk, varied"},
    "bloc party": {"genre": "Indie Rock, Post-Punk", "mood": "Energetic, varied, post-punk", "style": "British indie rock, post-punk revival", "vocal_style": "Kele Okereke, distinctive, dynamic, varied", "instruments": "Post-punk guitar, varied, layered", "production": "Indie rock polish, post-punk, varied"},
    "the kills": {"genre": "Indie Rock, Post-Punk", "mood": "Raw, varied, garage", "style": "British-American garage-rock duo", "vocal_style": "Alison Mosshart / Jamie Hince, distinctive, raw, varied", "instruments": "Garage-rock guitar, varied, layered", "production": "Indie rock polish, raw, varied"},
    "yeah yeah yeahs": {"genre": "Indie Rock, Post-Punk", "mood": "Energetic, varied, post-punk", "style": "NYC indie rock, post-punk", "vocal_style": "Karen O, distinctive, dynamic, varied", "instruments": "Post-punk guitar, varied, layered", "production": "Indie rock polish, post-punk, varied"},
    "tv on the radio": {"genre": "Indie Rock, Art Rock", "mood": "Eclectic, varied, art-rock", "style": "NYC indie art-rock, eclectic", "vocal_style": "Tunde Adebimpe, distinctive, dynamic, varied", "instruments": "Eclectic indie art-rock, varied, layered", "production": "Indie rock polish, eclectic, varied"},
    "the national": {"genre": "Indie Rock, Art Rock", "mood": "Melancholic, varied, indie", "style": "American indie art-rock, melancholic", "vocal_style": "Matt Berninger, deep baritone, distinctive, varied", "instruments": "Indie art-rock guitar, varied, layered", "production": "Indie rock polish, melancholic, varied"},
    "bon iver": {"genre": "Indie Rock, Indie Folk", "mood": "Atmospheric, varied, indie", "style": "American indie folk-rock, atmospheric", "vocal_style": "Justin Vernon, falsetto, distinctive, varied", "instruments": "Indie folk-rock guitar, varied, layered", "production": "Indie rock polish, atmospheric, varied"},
    "fleet foxes": {"genre": "Indie Rock, Indie Folk", "mood": "Harmonic, varied, indie", "style": "American indie folk, harmonic and atmospheric", "vocal_style": "Robin Pecknold, distinctive, harmonic, varied", "instruments": "Indie folk-rock, varied, layered", "production": "Indie rock polish, harmonic, varied"},
    "grizzly bear": {"genre": "Indie Rock, Art Rock", "mood": "Atmospheric, varied, indie", "style": "American indie art-rock, atmospheric", "vocal_style": "Ed Droste, distinctive, dynamic, varied", "instruments": "Indie art-rock, varied, layered", "production": "Indie rock polish, atmospheric, varied"},
    "deerhunter": {"genre": "Indie Rock, Shoegaze", "mood": "Atmospheric, varied, shoegaze", "style": "American indie shoegaze", "vocal_style": "Bradford Cox, distinctive, dynamic, varied", "instruments": "Shoegaze guitar, varied, layered", "production": "Indie rock polish, shoegaze, varied"},
    "my bloody valentine": {"genre": "Indie Rock, Shoegaze", "mood": "Atmospheric, varied, shoegaze", "style": "Irish-British shoegaze pioneer", "vocal_style": "Kevin Shields, processed, distinctive, varied", "instruments": "Shoegaze guitar, varied, layered", "production": "Indie rock polish, shoegaze, varied"},
    "slowdive": {"genre": "Indie Rock, Shoegaze", "mood": "Atmospheric, varied, shoegaze", "style": "British shoegaze pioneer, reformed", "vocal_style": "Rachel Goswell, ethereal, distinctive, varied", "instruments": "Shoegaze guitar, varied, layered", "production": "Indie rock polish, shoegaze, varied"},
    "ride": {"genre": "Indie Rock, Shoegaze", "mood": "Energetic, varied, shoegaze", "style": "British shoegaze pioneer, reformed", "vocal_style": "Mark Gardener, distinctive, dynamic, varied", "instruments": "Shoegaze guitar, varied, layered", "production": "Indie rock polish, shoegaze, varied"},
    "cocteau twins": {"genre": "Indie Rock, Shoegaze", "mood": "Ethereal, varied, shoegaze", "style": "Scottish shoegaze pioneer, ethereal", "vocal_style": "Elizabeth Fraser, ethereal, distinctive, varied", "instruments": "Shoegaze guitar, varied, layered", "production": "Indie rock polish, ethereal, varied"},
    "pavement": {"genre": "Indie Rock, Lo-Fi", "mood": "Lo-fi, varied, slacker", "style": "American slacker-rock pioneer", "vocal_style": "Stephen Malkmus, lo-fi, distinctive, varied", "instruments": "Lo-fi indie guitar, varied, layered", "production": "Indie rock polish, lo-fi, varied"},
    "sonic youth": {"genre": "Indie Rock, Alternative", "mood": "Experimental, varied, alternative", "style": "American alternative rock pioneer", "vocal_style": "Thurston Moore / Kim Gordon, distinctive, varied", "instruments": "Experimental alt-rock guitar, varied, layered", "production": "Indie rock polish, experimental, varied"},
    "pixies": {"genre": "Indie Rock, Alternative", "mood": "Energetic, varied, alternative", "style": "American alternative rock pioneer, alt-rock godfathers", "vocal_style": "Black Francis, distinctive, dynamic, varied", "instruments": "Alt-rock guitar, varied, layered", "production": "Indie rock polish, alt-rock, varied"},
    "dinosaur jr": {"genre": "Indie Rock, Alternative", "mood": "Energetic, varied, alternative", "style": "American alternative rock pioneer", "vocal_style": "J Mascis, distinctive, dynamic, varied", "instruments": "Alt-rock guitar, varied, layered", "production": "Indie rock polish, alt-rock, varied"},
    "guided by voices": {"genre": "Indie Rock, Lo-Fi", "mood": "Lo-fi, varied, prolific", "style": "American lo-fi indie rock, prolific", "vocal_style": "Robert Pollard, lo-fi, distinctive, varied", "instruments": "Lo-fi indie guitar, varied, layered", "production": "Indie rock polish, lo-fi, varied"},
    "built to spill": {"genre": "Indie Rock, Alternative", "mood": "Energetic, varied, indie", "style": "American indie rock, Keep It Like a Secret era", "vocal_style": "Doug Martsch, distinctive, dynamic, varied", "instruments": "Indie rock guitar, varied, layered", "production": "Indie rock polish, varied, layered"},
    "modest mouse": {"genre": "Indie Rock, Alternative", "mood": "Energetic, varied, indie", "style": "American indie rock, Good News for People Who Love Bad News", "vocal_style": "Isaac Brock, distinctive, dynamic, varied", "instruments": "Indie rock guitar, varied, layered", "production": "Indie rock polish, varied, layered"},

    # === Reggaeton (top-up to 25) ===
    "daddy yankee": {"genre": "Reggaeton", "mood": "Energetic, foundational, global", "style": "Puerto Rican reggaeton pioneer, 'Gasolina' era", "vocal_style": "Daddy Yankee, energetic, distinctive, dynamic", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, energetic, layered"},
    "don omar": {"genre": "Reggaeton", "mood": "Varied, foundational, Puerto Rican", "style": "Puerto Rican reggaeton pioneer, 'Dale Don Dale' era", "vocal_style": "Don Omar, distinctive, dynamic, varied", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, varied, layered"},
    "tego calderon": {"genre": "Reggaeton, Hip-Hop", "mood": "Street, varied, foundational", "style": "Puerto Rican reggaeton-hip-hop pioneer", "vocal_style": "Tego Calderon, raw, distinctive, varied", "instruments": "Reggaeton, hip-hop, varied", "production": "Reggaeton polish, raw, varied"},
    "hector el father": {"genre": "Reggaeton, Hip-Hop", "mood": "Street, varied, foundational", "style": "Puerto Rican reggaeton pioneer, retired", "vocal_style": "Hector El Father, raw, distinctive, varied", "instruments": "Reggaeton, hip-hop, varied", "production": "Reggaeton polish, raw, varied"},
    "tempo": {"genre": "Reggaeton", "mood": "Street, varied, foundational", "style": "Puerto Rican reggaeton pioneer", "vocal_style": "Tempo, distinctive, dynamic, varied", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, varied, layered"},
    "wisin y yandel": {"genre": "Reggaeton", "mood": "Energetic, varied, Puerto Rican", "style": "Puerto Rican reggaeton duo, foundational", "vocal_style": "Wisin + Yandel, distinctive, dynamic, varied", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, energetic, varied"},
    "plan b": {"genre": "Reggaeton", "mood": "Varied, foundational, Puerto Rican", "style": "Puerto Rican reggaeton duo, foundational", "vocal_style": "Chencho + Maldy, distinctive, dynamic, varied", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, varied, layered"},
    "zion y lennox": {"genre": "Reggaeton", "mood": "Romantic, varied, foundational", "style": "Puerto Rican reggaeton duo, romantic", "vocal_style": "Zion + Lennox, smooth, distinctive, varied", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, romantic, varied"},
    "rkm y ken y": {"genre": "Reggaeton", "mood": "Romantic, varied, Puerto Rican", "style": "Puerto Rican reggaeton duo, romantic", "vocal_style": "RKM + Ken-Y, smooth, distinctive, varied", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, romantic, varied"},
    "alexis y fido": {"genre": "Reggaeton", "mood": "Energetic, varied, Puerto Rican", "style": "Puerto Rican reggaeton duo, energetic", "vocal_style": "Alexis + Fido, distinctive, dynamic, varied", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, energetic, varied"},
    "j alvarez": {"genre": "Reggaeton", "mood": "Romantic, varied, Puerto Rican", "style": "Puerto Rican reggaeton, romantic", "vocal_style": "J Alvarez, smooth, distinctive, varied", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, romantic, varied"},
    "farina": {"genre": "Reggaeton", "mood": "Bold, varied, Colombian", "style": "Colombian reggaeton, female-led", "vocal_style": "Farina, bold, distinctive, varied", "instruments": "Reggaeton, varied, layered", "production": "Reggaeton polish, bold, varied"},
    "lola indigo": {"genre": "Reggaeton, Pop", "mood": "Empowering, varied, Spanish", "style": "Spanish reggaeton-pop crossover", "vocal_style": "Lola Indigo, empowering, distinctive, varied", "instruments": "Reggaeton, pop, varied", "production": "Reggaeton polish, empowering, varied"},
    "rosalia alt": {"genre": "Reggaeton, Pop", "mood": "Innovative, varied, Spanish", "style": "Spanish reggaeton-pop innovator, El Mal Querer", "vocal_style": "Rosalia, distinctive, dynamic, varied", "instruments": "Reggaeton, flamenco, pop, varied", "production": "Reggaeton polish, innovative, varied"},
    "c tangana": {"genre": "Reggaeton, Hip-Hop", "mood": "Eclectic, varied, Spanish", "style": "Spanish reggaeton-hip-hop eclectic", "vocal_style": "C Tangana, eclectic, distinctive, varied", "instruments": "Reggaeton, hip-hop, varied", "production": "Reggaeton polish, eclectic, varied"},
    "eladio carrión": {"genre": "Reggaeton, Latin Trap", "mood": "Varied, modern, Puerto Rican", "style": "Puerto Rican reggaeton-Latin trap, modern", "vocal_style": "Eladio Carrion, distinctive, dynamic, varied", "instruments": "Reggaeton, Latin trap, varied", "production": "Reggaeton polish, modern, varied"},
    "bizarrap": {"genre": "Reggaeton, Hip-Hop", "mood": "Energetic, varied, Argentine", "style": "Argentine reggaeton-hip-hop producer, BZRP Sessions", "vocal_style": "Featured vocalists, varied, dynamic", "instruments": "Reggaeton, hip-hop, varied", "production": "Reggaeton polish, energetic, varied"},
    "trueno": {"genre": "Reggaeton, Hip-Hop", "mood": "Street, varied, Argentine", "style": "Argentine reggaeton-hip-hop, freestyle battle legend", "vocal_style": "Trueno, raw, distinctive, varied", "instruments": "Reggaeton, hip-hop, varied", "production": "Reggaeton polish, raw, varied"},
    "nicki nicole": {"genre": "Reggaeton, R&B", "mood": "Smooth, varied, Argentine", "style": "Argentine reggaeton-R&B, smooth", "vocal_style": "Nicki Nicole, smooth, distinctive, varied", "instruments": "Reggaeton, R&B, varied", "production": "Reggaeton polish, smooth, varied"},
    "tini": {"genre": "Reggaeton, Pop", "mood": "Modern, varied, Argentine", "style": "Argentine pop-reggaeton, Disney alum", "vocal_style": "Tini, modern, distinctive, varied", "instruments": "Reggaeton, pop, varied", "production": "Reggaeton polish, modern, varied"},
    "bad gyal": {"genre": "Reggaeton, Electronic", "mood": "Bold, varied, Spanish", "style": "Spanish reggaeton-electronic, bold", "vocal_style": "Bad Gyal, bold, distinctive, varied", "instruments": "Reggaeton, electronic, varied", "production": "Reggaeton polish, bold, varied"},
    "la zowi": {"genre": "Reggaeton, Electronic", "mood": "Bold, varied, Spanish", "style": "Spanish reggaeton-electronic underground", "vocal_style": "La Zowi, bold, distinctive, varied", "instruments": "Reggaeton, electronic, varied", "production": "Reggaeton polish, bold, varied"},

    # === Bollywood (top-up to 25) ===
    "lata mangeshkar": {"genre": "Bollywood, Indian Playback", "mood": "Soulful, varied, legendary", "style": "Indian playback legend, late great", "vocal_style": "Lata Mangeshkar, soulful soprano, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, soulful, varied"},
    "mohammad rafi": {"genre": "Bollywood, Indian Playback", "mood": "Romantic, varied, legendary", "style": "Indian playback legend, late great", "vocal_style": "Mohammad Rafi, distinctive, dynamic, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, romantic, varied"},
    "kishore kumar": {"genre": "Bollywood, Indian Playback", "mood": "Energetic, varied, legendary", "style": "Indian playback legend, late great", "vocal_style": "Kishore Kumar, energetic, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, energetic, varied"},
    "asha bhosle": {"genre": "Bollywood, Indian Playback", "mood": "Soulful, varied, legendary", "style": "Indian playback legend, late great", "vocal_style": "Asha Bhosle, soulful, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, soulful, varied"},
    "mukesh": {"genre": "Bollywood, Indian Playback", "mood": "Romantic, varied, legendary", "style": "Indian playback legend, late great", "vocal_style": "Mukesh, romantic baritone, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, romantic, varied"},
    "sonu nigam": {"genre": "Bollywood, Indian Playback", "mood": "Romantic, varied, modern", "style": "Modern Indian playback legend", "vocal_style": "Sonu Nigam, romantic, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, romantic, varied"},
    "kumar sanu": {"genre": "Bollywood, Indian Playback", "mood": "Romantic, varied, 90s", "style": "90s Bollywood playback legend", "vocal_style": "Kumar Sanu, romantic, distinctive, varied", "instruments": "90s Bollywood orchestration, varied, layered", "production": "Bollywood polish, romantic, varied"},
    "udit narayan": {"genre": "Bollywood, Indian Playback", "mood": "Romantic, varied, 90s", "style": "90s Bollywood playback legend", "vocal_style": "Udit Narayan, romantic, distinctive, varied", "instruments": "90s Bollywood orchestration, varied, layered", "production": "Bollywood polish, romantic, varied"},
    "sunidhi chauhan": {"genre": "Bollywood, Indian Playback", "mood": "Energetic, varied, modern", "style": "Modern Bollywood playback, powerful", "vocal_style": "Sunidhi Chauhan, energetic, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, energetic, varied"},
    "neha kakkar": {"genre": "Bollywood, Pop", "mood": "Energetic, varied, modern", "style": "Modern Bollywood-pop, energetic", "vocal_style": "Neha Kakkar, energetic, distinctive, varied", "instruments": "Bollywood-pop production, varied, layered", "production": "Bollywood polish, energetic, varied"},
    "tony kakkar": {"genre": "Bollywood, Pop", "mood": "Romantic, varied, modern", "style": "Modern Bollywood-pop, romantic", "vocal_style": "Tony Kakkar, romantic, distinctive, varied", "instruments": "Bollywood-pop production, varied, layered", "production": "Bollywood polish, romantic, varied"},
    "badshah bollywood": {"genre": "Bollywood, Hip-Hop", "mood": "Energetic, varied, modern", "style": "Modern Bollywood-hip-hop crossover", "vocal_style": "Badshah, energetic, distinctive, varied", "instruments": "Bollywood-hip-hop production, varied, layered", "production": "Bollywood polish, energetic, varied"},
    "raftaar bollywood": {"genre": "Bollywood, Hip-Hop", "mood": "Varied, modern, hip-hop", "style": "Modern Bollywood-hip-hop crossover", "vocal_style": "Raftaar, varied, distinctive, varied", "instruments": "Bollywood-hip-hop production, varied, layered", "production": "Bollywood polish, varied, varied"},
    "shankar mahadevan": {"genre": "Bollywood, Indian Playback", "mood": "Soulful, varied, modern", "style": "Modern Bollywood playback legend", "vocal_style": "Shankar Mahadevan, soulful, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, soulful, varied"},
    "ajay atul": {"genre": "Bollywood, Indian Playback", "mood": "Anthemic, varied, modern", "style": "Modern Bollywood composers, anthemic", "vocal_style": "Ajay-Atul, anthemic, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, anthemic, varied"},
    "a r rahman": {"genre": "Bollywood, Indian Playback", "mood": "Innovative, varied, modern", "style": "Indian composer legend, Oscar winner", "vocal_style": "Featured vocalists, varied, dynamic", "instruments": "Bollywood-orchestral production, varied, layered", "production": "Bollywood polish, innovative, varied"},
    "vishal dadlani": {"genre": "Bollywood, Indian Playback", "mood": "Energetic, varied, modern", "style": "Modern Bollywood playback, energetic", "vocal_style": "Vishal Dadlani, energetic, distinctive, varied", "instruments": "Bollywood-rock production, varied, layered", "production": "Bollywood polish, energetic, varied"},
    "sukhwinder singh": {"genre": "Bollywood, Indian Playback", "mood": "Anthemic, varied, modern", "style": "Modern Bollywood playback, 'Jai Ho' era", "vocal_style": "Sukhwinder Singh, anthemic, distinctive, varied", "instruments": "Bollywood-orchestral production, varied, layered", "production": "Bollywood polish, anthemic, varied"},
    "shaan": {"genre": "Bollywood, Indian Playback", "mood": "Romantic, varied, modern", "style": "Modern Bollywood playback, romantic", "vocal_style": "Shaan, romantic, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, romantic, varied"},
    "shreya ghoshal bollywood": {"genre": "Bollywood, Indian Playback", "mood": "Soulful, varied, modern", "style": "Modern Bollywood playback legend", "vocal_style": "Shreya Ghoshal, soulful soprano, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, soulful, varied"},
    "sonu nigam alt": {"genre": "Bollywood, Indian Playback", "mood": "Romantic, varied, modern", "style": "Modern Indian playback legend", "vocal_style": "Sonu Nigam, romantic, distinctive, varied", "instruments": "Bollywood orchestration, varied, layered", "production": "Bollywood polish, romantic, varied"},

    # === Punjabi (top-up to 25) ===
    "guru randhawa alt": {"genre": "Punjabi Pop, Bollywood", "mood": "Romantic, varied, Punjabi", "style": "Punjabi pop-Bollywood crossover, romantic", "vocal_style": "Guru Randhawa, romantic, distinctive, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "ammy virk alt": {"genre": "Punjabi Pop", "mood": "Romantic, varied, Punjabi", "style": "Punjabi pop, romantic and varied", "vocal_style": "Ammy Virk, romantic, distinctive, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "ap dhillon alt": {"genre": "Punjabi Pop, Hip-Hop", "mood": "Modern, varied, Punjabi", "style": "Punjabi pop with global hip-hop influence", "vocal_style": "AP Dhillon, distinctive, dynamic, varied", "instruments": "Punjabi-hip-hop production, varied, layered", "production": "Punjabi-hip-hop polish, modern, varied"},
    "shubh alt": {"genre": "Punjabi Pop, Hip-Hop", "mood": "Modern, varied, Punjabi", "style": "Punjabi pop-hip-hop, global crossover", "vocal_style": "Shubh, distinctive, dynamic, varied", "instruments": "Punjabi-hip-hop production, varied, layered", "production": "Punjabi-hip-hop polish, modern, varied"},
    "sidhu moosewala alt": {"genre": "Punjabi Hip-Hop", "mood": "Street, varied, Punjabi", "style": "Punjabi hip-hop legend, late pioneer", "vocal_style": "Sidhu Moosewala, distinctive, dynamic, varied", "instruments": "Punjabi-hip-hop production, varied, layered", "production": "Punjabi-hip-hop polish, street, varied"},
    "diljit dosanjh alt": {"genre": "Punjabi Pop", "mood": "Varied, polished, Punjabi", "style": "Punjabi pop-hip-hop crossover, global", "vocal_style": "Diljit, distinctive, dynamic, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, varied, varied"},
    "ammy virk two": {"genre": "Punjabi Pop", "mood": "Romantic, varied, Punjabi", "style": "Punjabi pop, romantic and varied", "vocal_style": "Ammy Virk, romantic, distinctive, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "gippy grewal": {"genre": "Punjabi Pop, Bhangra", "mood": "Energetic, varied, Punjabi", "style": "Punjabi pop-Bhangra crossover", "vocal_style": "Gippy Grewal, energetic, distinctive, varied", "instruments": "Bhangra, Punjabi pop, varied", "production": "Punjabi-Bhangra polish, energetic, varied"},
    "mankirt aulakh": {"genre": "Punjabi Pop", "mood": "Romantic, varied, Punjabi", "style": "Modern Punjabi pop", "vocal_style": "Mankirt Aulakh, romantic, distinctive, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "karan aujla": {"genre": "Punjabi Pop, Hip-Hop", "mood": "Modern, varied, Punjabi", "style": "Modern Punjabi pop-hip-hop, global", "vocal_style": "Karan Aujla, distinctive, dynamic, varied", "instruments": "Punjabi-hip-hop production, varied, layered", "production": "Punjabi-hip-hop polish, modern, varied"},
    "ammy virk three": {"genre": "Punjabi Pop", "mood": "Romantic, varied, Punjabi", "style": "Punjabi pop, romantic and varied", "vocal_style": "Ammy Virk, romantic, distinctive, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "param singh": {"genre": "Punjabi Pop", "mood": "Romantic, varied, Punjabi", "style": "Modern Punjabi pop, romantic", "vocal_style": "Param Singh, romantic, distinctive, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "jassi gill": {"genre": "Punjabi Pop", "mood": "Romantic, varied, Punjabi", "style": "Punjabi pop, romantic", "vocal_style": "Jassi Gill, romantic, distinctive, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "babbu maan": {"genre": "Punjabi Pop, Bhangra", "mood": "Energetic, varied, Punjabi", "style": "Punjabi legend, Bhangra-pop crossover", "vocal_style": "Babbu Maan, energetic, distinctive, varied", "instruments": "Bhangra, Punjabi pop, varied", "production": "Punjabi-Bhangra polish, energetic, varied"},
    "kulwinder billa": {"genre": "Punjabi Pop, Bhangra", "mood": "Energetic, varied, Punjabi", "style": "Punjabi-Bhangra, energetic", "vocal_style": "Kulwinder Billa, energetic, distinctive, varied", "instruments": "Bhangra, Punjabi pop, varied", "production": "Punjabi-Bhangra polish, energetic, varied"},
    "navraj hans": {"genre": "Punjabi Pop, Bhangra", "mood": "Energetic, varied, Punjabi", "style": "Punjabi-Bhangra crossover, energetic", "vocal_style": "Navraj Hans, energetic, distinctive, varied", "instruments": "Bhangra, Punjabi pop, varied", "production": "Punjabi-Bhangra polish, energetic, varied"},
    "the landers": {"genre": "Punjabi Pop, Bhangra", "mood": "Energetic, varied, Punjabi", "style": "Punjabi-Bhangra crossover, energetic duo", "vocal_style": "The Landers, energetic, distinctive, varied", "instruments": "Bhangra, Punjabi pop, varied", "production": "Punjabi-Bhangra polish, energetic, varied"},
    "pav dharia": {"genre": "Punjabi Pop, Indie", "mood": "Modern, varied, Punjabi-indie", "style": "Punjabi indie-pop crossover", "vocal_style": "Pav Dharia, modern, distinctive, varied", "instruments": "Punjabi-indie production, varied, layered", "production": "Punjabi-indie polish, modern, varied"},
    "happy raikoti": {"genre": "Punjabi Pop", "mood": "Romantic, varied, Punjabi", "style": "Punjabi pop, romantic", "vocal_style": "Happy Raikoti, romantic, distinctive, varied", "instruments": "Punjabi-pop production, varied, layered", "production": "Punjabi-pop polish, romantic, varied"},
    "r nait": {"genre": "Punjabi Pop, Bhangra", "mood": "Energetic, varied, Punjabi", "style": "Punjabi-Bhangra, energetic", "vocal_style": "R Nait, energetic, distinctive, varied", "instruments": "Bhangra, Punjabi pop, varied", "production": "Punjabi-Bhangra polish, energetic, varied"},
    "ninja": {"genre": "Punjabi Pop, Bhangra", "mood": "Energetic, varied, Punjabi", "style": "Punjabi-Bhangra, energetic", "vocal_style": "Ninja, energetic, distinctive, varied", "instruments": "Bhangra, Punjabi pop, varied", "production": "Punjabi-Bhangra polish, energetic, varied"},

    # === Corrido (top-up to 25) ===
    "natanael cano": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados pioneer, 'Amor Tumbado' era", "vocal_style": "Natanael Cano, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "junior h": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados pioneer, $ad Boyz Life era", "vocal_style": "Junior H, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "peso pluma": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados pioneer, global crossover", "vocal_style": "Peso Pluma, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "feid mex": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Romantic, varied, Mexican", "style": "Mexican corridos tumbados, romantic", "vocal_style": "Feid, smooth, distinctive, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "gabito ballesteros": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados, energetic", "vocal_style": "Gabito Ballesteros, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "tito doble p": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados, energetic", "vocal_style": "Tito Doble P, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "eduin caz": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados, Grupo Frontera alum", "vocal_style": "Eduin Caz, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "jose guicho": {"genre": "Corridos Bélicos, Regional Mexican", "mood": "Gritty, varied, Mexican", "style": "Mexican corridos bélicos, gritty", "vocal_style": "Jose Guicho, distinctive, raw, varied", "instruments": "Corridos bélicos, regional Mexican, varied", "production": "Corridos bélicos polish, raw, varied"},
    "movimiento alterado": {"genre": "Corridos Bélicos, Regional Mexican", "mood": "Gritty, varied, Mexican", "style": "Mexican corridos bélicos, foundational", "vocal_style": "Movimiento Alterado, distinctive, raw, varied", "instruments": "Corridos bélicos, regional Mexican, varied", "production": "Corridos bélicos polish, raw, varied"},
    "legion holk": {"genre": "Corridos Bélicos, Regional Mexican", "mood": "Gritty, varied, Mexican", "style": "Mexican corridos bélicos, foundational", "vocal_style": "Legion Holk, distinctive, raw, varied", "instruments": "Corridos bélicos, regional Mexican, varied", "production": "Corridos bélicos polish, raw, varied"},
    "randy pxz": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados, energetic", "vocal_style": "Randy PXZ, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "belice": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados, energetic", "vocal_style": "Belice, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "calle 24": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados, energetic", "vocal_style": "Calle 24, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "el alfa": {"genre": "Corridos Bélicos, Dembow", "mood": "Energetic, varied, Dominican", "style": "Dominican dembow-corridos, energetic", "vocal_style": "El Alfa, distinctive, dynamic, varied", "instruments": "Dembow, corridos, varied", "production": "Dembow-corridos polish, energetic, varied"},
    "mark b": {"genre": "Dembow, Latin", "mood": "Energetic, varied, Dominican", "style": "Dominican dembow pioneer", "vocal_style": "Mark B, distinctive, dynamic, varied", "instruments": "Dembow, varied, layered", "production": "Dembow polish, energetic, varied"},
    "kiko el crazy": {"genre": "Dembow, Latin", "mood": "Energetic, varied, Dominican", "style": "Dominican dembow pioneer", "vocal_style": "Kiko El Crazy, distinctive, dynamic, varied", "instruments": "Dembow, varied, layered", "production": "Dembow polish, energetic, varied"},
    "chimbala": {"genre": "Dembow, Latin", "mood": "Energetic, varied, Dominican", "style": "Dominican dembow pioneer", "vocal_style": "Chimbala, distinctive, dynamic, varied", "instruments": "Dembow, varied, layered", "production": "Dembow polish, energetic, varied"},
    "bulin 47": {"genre": "Dembow, Latin", "mood": "Energetic, varied, Dominican", "style": "Dominican dembow pioneer", "vocal_style": "Bulin 47, distinctive, dynamic, varied", "instruments": "Dembow, varied, layered", "production": "Dembow polish, energetic, varied"},
    "tokischa": {"genre": "Dembow, Reggaeton", "mood": "Bold, varied, Dominican", "style": "Dominican dembow-reggaeton, bold", "vocal_style": "Tokischa, bold, distinctive, varied", "instruments": "Dembow, reggaeton, varied", "production": "Dembow polish, bold, varied"},
    "la materialista": {"genre": "Dembow, Latin Pop", "mood": "Bold, varied, Dominican", "style": "Dominican dembow-Latin pop, bold", "vocal_style": "La Materialista, bold, distinctive, varied", "instruments": "Dembow, Latin pop, varied", "production": "Dembow polish, bold, varied"},
    "pablo mator": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados, energetic", "vocal_style": "Pablo Mator, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "revel x": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados, energetic", "vocal_style": "Revel X, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "virlan garcia": {"genre": "Corridos Bélicos, Regional Mexican", "mood": "Gritty, varied, Mexican", "style": "Mexican corridos bélicos, gritty", "vocal_style": "Virlan Garcia, distinctive, raw, varied", "instruments": "Corridos bélicos, regional Mexican, varied", "production": "Corridos bélicos polish, raw, varied"},
    "enigma norteño": {"genre": "Corridos Bélicos, Regional Mexican", "mood": "Gritty, varied, Mexican", "style": "Mexican corridos bélicos, foundational", "vocal_style": "Enigma Norteno, distinctive, raw, varied", "instruments": "Corridos bélicos, regional Mexican, varied", "production": "Corridos bélicos polish, raw, varied"},
    "el komander": {"genre": "Corridos Bélicos, Regional Mexican", "mood": "Gritty, varied, Mexican", "style": "Mexican corridos bélicos, gritty", "vocal_style": "El Komander, distinctive, raw, varied", "instruments": "Corridos bélicos, regional Mexican, varied", "production": "Corridos bélicos polish, raw, varied"},

    # === CCM (top-up to 25) ===
    "chris tomlin": {"genre": "CCM, Worship", "mood": "Reverent, anthemic, varied", "style": "Modern worship pioneer, 'How Great Is Our God' era", "vocal_style": "Chris Tomlin, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, anthemic, layered"},
    "matt redman": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "British worship pioneer, '10,000 Reasons' era", "vocal_style": "Matt Redman, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "elevation worship": {"genre": "CCM, Worship", "mood": "Anthemic, energetic, varied", "style": "Modern worship, Elevation Church", "vocal_style": "Varies, anthemic, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, energetic, varied"},
    "planetshakers": {"genre": "CCM, Worship", "mood": "Anthemic, energetic, varied", "style": "Australian worship, festival energy", "vocal_style": "Varies, anthemic, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, energetic, varied"},
    "kari jobe": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Modern worship pioneer, female-led", "vocal_style": "Kari Jobe, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "cody carnes": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Modern worship, Kari Jobe husband", "vocal_style": "Cody Carnes, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "phil wickham": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Modern worship pioneer", "vocal_style": "Phil Wickham, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "bethel music": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Bethel Church worship, modern pioneer", "vocal_style": "Varies, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, varied, layered"},
    "hillsong united": {"genre": "CCM, Worship", "mood": "Anthemic, varied, worship", "style": "Hillsong's youth worship, modern pioneer", "vocal_style": "Varies, anthemic, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, anthemic, varied"},
    "hillsong worship": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Hillsong main worship, modern pioneer", "vocal_style": "Varies, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, varied, layered"},
    "passion": {"genre": "CCM, Worship", "mood": "Anthemic, varied, worship", "style": "Passion Conferences, modern worship", "vocal_style": "Varies, anthemic, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, anthemic, varied"},
    "kristian stanfill": {"genre": "CCM, Worship", "mood": "Anthemic, varied, worship", "style": "Passion Band lead, modern worship", "vocal_style": "Kristian Stanfill, anthemic, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, anthemic, varied"},
    "third day": {"genre": "CCM, Rock", "mood": "Anthemic, varied, Southern rock", "style": "CCM Southern rock pioneers", "vocal_style": "Mac Powell, distinctive, dynamic, varied", "instruments": "Rock guitar, varied, layered", "production": "CCM rock polish, anthemic, varied"},
    "newsboys": {"genre": "CCM, Pop Rock", "mood": "Energetic, varied, pop-rock", "style": "CCM pop-rock pioneers", "vocal_style": "Peter Furler / Michael Tait, distinctive, dynamic, varied", "instruments": "Pop-rock guitar, varied, layered", "production": "CCM pop-rock polish, energetic, varied"},
    "dc talk": {"genre": "CCM, Hip-Hop", "mood": "Varied, hip-hop, CCM", "style": "CCM hip-hop-rock pioneers, foundational", "vocal_style": "TobyMac + Michael Tait + Kevin Max, distinctive, varied", "instruments": "Hip-hop, rock, varied", "production": "CCM polish, varied, layered"},
    "toby mac solo": {"genre": "CCM, Hip-Hop", "mood": "Energetic, varied, hip-hop", "style": "TobyMac solo, CCM hip-hop", "vocal_style": "TobyMac, distinctive, dynamic, varied", "instruments": "Hip-hop, varied, layered", "production": "CCM hip-hop polish, energetic, varied"},
    "switchfoot": {"genre": "CCM, Alternative Rock", "mood": "Anthemic, varied, alt-rock", "style": "CCM alternative rock pioneers", "vocal_style": "Jon Foreman, distinctive, dynamic, varied", "instruments": "Alt-rock guitar, varied, layered", "production": "CCM alt-rock polish, anthemic, varied"},
    "needtobreathe": {"genre": "CCM, Southern Rock", "mood": "Anthemic, varied, Southern rock", "style": "CCM Southern rock, anthemic", "vocal_style": "Bear Rinehart, distinctive, dynamic, varied", "instruments": "Rock guitar, varied, layered", "production": "CCM rock polish, anthemic, varied"},
    "casting crowns": {"genre": "CCM, Pop Rock", "mood": "Heartfelt, varied, pop-rock", "style": "CCM pop-rock, Mark Hall", "vocal_style": "Mark Hall, distinctive, dynamic, varied", "instruments": "Pop-rock guitar, varied, layered", "production": "CCM pop-rock polish, heartfelt, varied"},
    "mercyme modern": {"genre": "CCM, Pop Rock", "mood": "Hopeful, varied, pop-rock", "style": "MercyMe, CCM pop-rock", "vocal_style": "Bart Millard, distinctive, dynamic, varied", "instruments": "Pop-rock guitar, varied, layered", "production": "CCM pop-rock polish, hopeful, varied"},
    "michael w smith": {"genre": "CCM, Pop", "mood": "Reverent, varied, CCM pop", "style": "CCM pop pioneer, 'Friends' era", "vocal_style": "Michael W. Smith, distinctive, dynamic, varied", "instruments": "Pop, piano, varied, layered", "production": "CCM pop polish, varied, layered"},
    "amy grant": {"genre": "CCM, Pop", "mood": "Reverent, varied, CCM pop", "style": "CCM pop pioneer, foundational", "vocal_style": "Amy Grant, distinctive, dynamic, varied", "instruments": "Pop, varied, layered", "production": "CCM pop polish, varied, layered"},
    "steven curtis chapman": {"genre": "CCM, Pop", "mood": "Heartfelt, varied, CCM pop", "style": "CCM pop pioneer, country CCM", "vocal_style": "Steven Curtis Chapman, distinctive, dynamic, varied", "instruments": "Pop, country, varied", "production": "CCM pop polish, heartfelt, varied"},
    "audio adrenaline": {"genre": "CCM, Pop Rock", "mood": "Energetic, varied, pop-rock", "style": "CCM pop-rock pioneers, 'Big House' era", "vocal_style": "Mark Stuart, distinctive, dynamic, varied", "instruments": "Pop-rock guitar, varied, layered", "production": "CCM pop-rock polish, energetic, varied"},
    "jars of clay": {"genre": "CCM, Alternative Rock", "mood": "Atmospheric, varied, alt-rock", "style": "CCM alt-rock pioneers, atmospheric", "vocal_style": "Dan Haseltine, distinctive, dynamic, varied", "instruments": "Alt-rock guitar, varied, layered", "production": "CCM alt-rock polish, atmospheric, varied"},
    "sixpence none the richer": {"genre": "CCM, Pop", "mood": "Romantic, varied, CCM pop", "style": "CCM pop, 'Kiss Me' era", "vocal_style": "Leigh Nash, distinctive, dynamic, varied", "instruments": "Pop, varied, layered", "production": "CCM pop polish, romantic, varied"},
    "relient k": {"genre": "CCM, Pop Punk", "mood": "Energetic, varied, pop-punk", "style": "CCM pop-punk, witty and varied", "vocal_style": "Matt Thiessen, distinctive, dynamic, varied", "instruments": "Pop-punk guitar, varied, layered", "production": "CCM pop-punk polish, energetic, varied"},
    "supertones": {"genre": "CCM, Ska Punk", "mood": "Energetic, varied, ska-punk", "style": "CCM ska-punk pioneers, O.C. Supertones", "vocal_style": "Varies, distinctive, dynamic, varied", "instruments": "Ska-punk guitar, varied, layered", "production": "CCM ska-punk polish, energetic, varied"},

    # === Christian Metal (top-up to 25) ===
    "underoath": {"genre": "Christian Metal, Metalcore", "mood": "Intense, varied, metalcore", "style": "Christian metalcore pioneers, post-hardcore", "vocal_style": "Spencer Chamberlain, screaming + clean, distinctive", "instruments": "Metalcore guitar, varied, layered", "production": "Christian metalcore polish, intense, varied"},
    "as i lay dying alt": {"genre": "Christian Metal, Metalcore", "mood": "Intense, varied, metalcore", "style": "Christian metalcore pioneers, 'Fraile Words' era", "vocal_style": "Tim Lambesis, distinctive, raw, varied", "instruments": "Metalcore guitar, varied, layered", "production": "Christian metalcore polish, intense, varied"},
    "demon hunter": {"genre": "Christian Metal, Metalcore", "mood": "Intense, varied, metalcore", "style": "Christian metalcore, 'Demon Hunter' era", "vocal_style": "Ryan Clark, screaming, distinctive, varied", "instruments": "Metalcore guitar, varied, layered", "production": "Christian metalcore polish, intense, varied"},
    "haste the day": {"genre": "Christian Metal, Metalcore", "mood": "Intense, varied, metalcore", "style": "Christian metalcore, 'Pressure the Hinges' era", "vocal_style": "Stephen Keech, distinctive, raw, varied", "instruments": "Metalcore guitar, varied, layered", "production": "Christian metalcore polish, intense, varied"},
    "the chariot": {"genre": "Christian Metal, Mathcore", "mood": "Chaotic, varied, mathcore", "style": "Christian mathcore, chaotic and raw", "vocal_style": "Josh Scogin, screaming, distinctive, varied", "instruments": "Mathcore, varied, layered", "production": "Christian mathcore polish, chaotic, varied"},
    "living sacrifice": {"genre": "Christian Metal, Death Metal", "mood": "Intense, varied, death metal", "style": "Christian death metal pioneers", "vocal_style": "Bruce Fitzhugh, screaming, distinctive, varied", "instruments": "Death metal guitar, varied, layered", "production": "Christian death metal polish, intense, varied"},
    "extol": {"genre": "Christian Metal, Progressive", "mood": "Progressive, varied, metal", "style": "Norwegian Christian progressive metal", "vocal_style": "Peter Espevoll, distinctive, dynamic, varied", "instruments": "Progressive metal, varied, layered", "production": "Christian progressive polish, varied, layered"},
    "believer": {"genre": "Christian Metal, Progressive", "mood": "Progressive, varied, thrash", "style": "Christian progressive thrash, 'Dimension' era", "vocal_style": "Kurt Bachman, distinctive, dynamic, varied", "instruments": "Progressive thrash, varied, layered", "production": "Christian progressive polish, varied, layered"},
    "vengenance rising": {"genre": "Christian Metal, Thrash", "mood": "Intense, varied, thrash", "style": "Christian thrash pioneers, foundational", "vocal_style": "Roger Martinez, screaming, distinctive, varied", "instruments": "Thrash, varied, layered", "production": "Christian thrash polish, intense, varied"},
    "sacrament": {"genre": "Christian Metal, Thrash", "mood": "Intense, varied, thrash", "style": "Christian thrash, foundational", "vocal_style": "Varies, distinctive, raw, varied", "instruments": "Thrash, varied, layered", "production": "Christian thrash polish, intense, varied"},
    "bloodgood": {"genre": "Christian Metal, Heavy Metal", "mood": "Anthemic, varied, heavy metal", "style": "Christian heavy metal pioneers, foundational", "vocal_style": "Les Carlsen, distinctive, dynamic, varied", "instruments": "Heavy metal, varied, layered", "production": "Christian metal polish, anthemic, varied"},
    "guardians of time": {"genre": "Christian Metal, Power Metal", "mood": "Anthemic, varied, power metal", "style": "Norwegian Christian power metal", "vocal_style": "Ole Wisth, distinctive, dynamic, varied", "instruments": "Power metal, varied, layered", "production": "Christian power metal polish, anthemic, varied"},
    "theocracy": {"genre": "Christian Metal, Power Metal", "mood": "Anthemic, varied, power metal", "style": "American Christian power metal", "vocal_style": "Matt Smith, distinctive, dynamic, varied", "instruments": "Power metal, varied, layered", "production": "Christian power metal polish, anthemic, varied"},
    "stairchick": {"genre": "Christian Metal, Power Metal", "mood": "Anthemic, varied, power metal", "style": "American Christian power metal", "vocal_style": "Varies, distinctive, dynamic, varied", "instruments": "Power metal, varied, layered", "production": "Christian power metal polish, anthemic, varied"},
    "burning point": {"genre": "Christian Metal, Power Metal", "mood": "Anthemic, varied, power metal", "style": "Finnish Christian power metal", "vocal_style": "Varies, distinctive, dynamic, varied", "instruments": "Power metal, varied, layered", "production": "Christian power metal polish, anthemic, varied"},
    "vaux": {"genre": "Christian Metal, Alternative", "mood": "Atmospheric, varied, alt-metal", "style": "Christian alt-metal, atmospheric", "vocal_style": "Varies, distinctive, dynamic, varied", "instruments": "Alt-metal, varied, layered", "production": "Christian alt-metal polish, atmospheric, varied"},
    "mewithoutyou": {"genre": "Christian Metal, Post-Hardcore", "mood": "Atmospheric, varied, post-hardcore", "style": "Christian post-hardcore, atmospheric", "vocal_style": "Aaron Weiss, distinctive, dynamic, varied", "instruments": "Post-hardcore, varied, layered", "production": "Christian post-hardcore polish, atmospheric, varied"},
    "showbread": {"genre": "Christian Metal, Post-Hardcore", "mood": "Chaotic, varied, post-hardcore", "style": "Christian post-hardcore, chaotic and theatrical", "vocal_style": "Josh Dies, distinctive, dynamic, varied", "instruments": "Post-hardcore, varied, layered", "production": "Christian post-hardcore polish, chaotic, varied"},
    "psaltarion": {"genre": "Christian Metal, Doom", "mood": "Funereal, varied, doom", "style": "Christian doom metal, foundational", "vocal_style": "Varies, distinctive, dynamic, varied", "instruments": "Doom metal, varied, layered", "production": "Christian doom polish, funereal, varied"},
    "the weary": {"genre": "Christian Metal, Atmospheric", "mood": "Atmospheric, varied, post-metal", "style": "Christian atmospheric post-metal", "vocal_style": "Varies, distinctive, dynamic, varied", "instruments": "Atmospheric post-metal, varied, layered", "production": "Christian atmospheric polish, varied, layered"},
    "sleek牙": {"genre": "Christian Metal, Post-Metal", "mood": "Atmospheric, varied, post-metal", "style": "Christian post-metal, atmospheric", "vocal_style": "Varies, distinctive, dynamic, varied", "instruments": "Post-metal, varied, layered", "production": "Christian post-metal polish, atmospheric, varied"},
    "beautiful eulogy": {"genre": "Christian Metal, Hip-Hop", "mood": "Conscious, varied, hip-hop", "style": "Christian hip-hop, atmospheric and varied", "vocal_style": "Varies, distinctive, dynamic, varied", "instruments": "Hip-hop, atmospheric, varied", "production": "Christian hip-hop polish, atmospheric, varied"},

    # === Doom (top-up to 25) ===
    "candlemass": {"genre": "Doom Metal, Epic Doom", "mood": "Funereal, varied, epic doom", "style": "Swedish epic doom pioneers, 'Epicus Doomicus Metallicus'", "vocal_style": "Johan Längquist / Messiah Marcolin, operatic, distinctive", "instruments": "Massive downtuned guitar, varied, layered", "production": "Epic doom polish, funereal, varied"},
    "pentagram": {"genre": "Doom Metal, Traditional Doom", "mood": "Funereal, varied, traditional doom", "style": "American doom pioneers, Bobby Liebling", "vocal_style": "Bobby Liebling, distinctive, raw, varied", "instruments": "Traditional doom, varied, layered", "production": "Traditional doom polish, raw, varied"},
    "saint vitus": {"genre": "Doom Metal, Traditional Doom", "mood": "Funereal, varied, traditional doom", "style": "American doom pioneers, Scott Reagers era", "vocal_style": "Scott Reagers / Wino, distinctive, raw, varied", "instruments": "Traditional doom, varied, layered", "production": "Traditional doom polish, raw, varied"},
    "trouble": {"genre": "Doom Metal, Psychedelic Doom", "mood": "Psychedelic, varied, doom", "style": "Chicago doom pioneers, psychedelic doom", "vocal_style": "Eric Wagner, distinctive, raw, varied", "instruments": "Psychedelic doom, varied, layered", "production": "Psychedelic doom polish, varied, varied"},
    "the obsessed": {"genre": "Doom Metal, Traditional Doom", "mood": "Funereal, varied, traditional doom", "style": "American doom pioneers, Scott 'Wino' Weinrich", "vocal_style": "Wino, distinctive, raw, varied", "instruments": "Traditional doom, varied, layered", "production": "Traditional doom polish, raw, varied"},
    "witchfinder general": {"genre": "Doom Metal, NWOBHM", "mood": "Funereal, varied, NWOBHM", "style": "British doom-NWOBHM pioneers", "vocal_style": "Zeeb Parkes, distinctive, raw, varied", "instruments": "NWOBHM doom, varied, layered", "production": "NWOBHM doom polish, raw, varied"},
    "pagan altar": {"genre": "Doom Metal, NWOBHM", "mood": "Funereal, varied, NWOBHM", "style": "British doom-NWOBHM pioneers, late discovered", "vocal_style": "Terry Jones, distinctive, raw, varied", "instruments": "NWOBHM doom, varied, layered", "production": "NWOBHM doom polish, raw, varied"},
    "reverend bizarre": {"genre": "Doom Metal, Stoner Doom", "mood": "Stoner, varied, doom", "style": "Swedish stoner doom, epic and varied", "vocal_style": "Albert Witchfinder, distinctive, raw, varied", "instruments": "Stoner doom, varied, layered", "production": "Stoner doom polish, varied, varied"},
    "sunn o)))": {"genre": "Doom Metal, Drone", "mood": "Drone, varied, funereal", "style": "American drone doom pioneers, experimental", "vocal_style": "Greg Anderson / Stephen O'Malley, mostly instrumental", "instruments": "Massive drone guitar, varied, layered", "production": "Drone doom polish, funereal, varied"},
    "earth": {"genre": "Doom Metal, Drone", "mood": "Drone, varied, atmospheric", "style": "American drone doom pioneers, 'Earth 2'", "vocal_style": "Dylan Carlson, mostly instrumental, varied", "instruments": "Drone guitar, varied, layered", "production": "Drone doom polish, atmospheric, varied"},
    "boris": {"genre": "Doom Metal, Drone", "mood": "Drone, varied, Japanese", "style": "Japanese drone doom pioneers, eclectic", "vocal_style": "Atsuo / Wata, distinctive, varied", "instruments": "Drone, varied, layered", "production": "Drone doom polish, eclectic, varied"},
    "yob": {"genre": "Doom Metal, Stoner Doom", "mood": "Cosmic, varied, doom", "style": "American stoner-cosmic doom, 'Clearing the Path to Ascend'", "vocal_style": "Mike Scheidt, distinctive, dynamic, varied", "instruments": "Stoner doom, varied, layered", "production": "Stoner doom polish, cosmic, varied"},
    "electric wizard": {"genre": "Doom Metal, Stoner Doom", "mood": "Funereal, varied, doom", "style": "British stoner doom, 'Dopethrone' era", "vocal_style": "Jus Oborn, distinctive, raw, varied", "instruments": "Stoner doom, varied, layered", "production": "Stoner doom polish, funereal, varied"},
    "sleep": {"genre": "Doom Metal, Stoner Doom", "mood": "Stoner, varied, doom", "style": "American stoner doom pioneers, 'Holy Mountain' era", "vocal_style": "Matt Pike / Al Cisneros, distinctive, varied", "instruments": "Stoner doom, varied, layered", "production": "Stoner doom polish, varied, varied"},
    "kyuss": {"genre": "Doom Metal, Stoner Doom", "mood": "Stoner, varied, doom", "style": "American stoner doom pioneers, 'Blues for the Red Sun'", "vocal_style": "John Garcia, distinctive, raw, varied", "instruments": "Stoner doom, varied, layered", "production": "Stoner doom polish, varied, varied"},
    "monarch": {"genre": "Doom Metal, Drone", "mood": "Drone, varied, doom", "style": "French drone doom, raw and massive", "vocal_style": "Varies, distinctive, raw, varied", "instruments": "Massive drone guitar, varied, layered", "production": "Drone doom polish, raw, varied"},
    "windhand": {"genre": "Doom Metal, Heavy Doom", "mood": "Funereal, varied, doom", "style": "American heavy doom, 'Soma' era", "vocal_style": "Dorthia Cottrell, distinctive, raw, varied", "instruments": "Heavy doom, varied, layered", "production": "Heavy doom polish, funereal, varied"},
    "pallbearer": {"genre": "Doom Metal, Heavy Doom", "mood": "Funereal, varied, doom", "style": "American heavy doom, 'Sorrow and Extinction'", "vocal_style": "Brett Campbell, distinctive, dynamic, varied", "instruments": "Heavy doom, varied, layered", "production": "Heavy doom polish, funereal, varied"},
    "khemmis": {"genre": "Doom Metal, Heavy Doom", "mood": "Funereal, varied, doom", "style": "American heavy doom, epic and varied", "vocal_style": "Ben Hutcherson, distinctive, dynamic, varied", "instruments": "Heavy doom, varied, layered", "production": "Heavy doom polish, varied, varied"},
    "bell witch": {"genre": "Doom Metal, Funeral Doom", "mood": "Funereal, varied, doom", "style": "American funeral doom, 'Mirror Reaper' era", "vocal_style": "Adrien Contreras / Dylan Desmond, distinctive, varied", "instruments": "Funeral doom, varied, layered", "production": "Funeral doom polish, funereal, varied"},
    "shape of despair": {"genre": "Doom Metal, Funeral Doom", "mood": "Funereal, varied, doom", "style": "Finnish funeral doom pioneers", "vocal_style": "Varies, distinctive, raw, varied", "instruments": "Funeral doom, varied, layered", "production": "Funeral doom polish, funereal, varied"},
    "evoken": {"genre": "Doom Metal, Funeral Doom", "mood": "Funereal, varied, doom", "style": "American funeral doom pioneers", "vocal_style": "Varies, distinctive, raw, varied", "instruments": "Funeral doom, varied, layered", "production": "Funeral doom polish, funereal, varied"},
    "ahab": {"genre": "Doom Metal, Funeral Doom", "mood": "Funereal, varied, doom", "style": "German funeral doom, nautical themes", "vocal_style": "Varies, distinctive, raw, varied", "instruments": "Funeral doom, varied, layered", "production": "Funeral doom polish, funereal, varied"},
    "skepticism": {"genre": "Doom Metal, Funeral Doom", "mood": "Funereal, varied, doom", "style": "Finnish funeral doom pioneers, organ-driven", "vocal_style": "Jani Kekarainen, distinctive, raw, varied", "instruments": "Organ-driven funeral doom, varied, layered", "production": "Funeral doom polish, funereal, varied"},
    "my dying bride": {"genre": "Doom Metal, Gothic Doom", "mood": "Gothic, varied, doom", "style": "British gothic doom pioneers, 'Turn Loose the Swans'", "vocal_style": "Aaron Stainthorpe, distinctive, dynamic, varied", "instruments": "Gothic doom, varied, layered", "production": "Gothic doom polish, varied, varied"},
    "katatonia": {"genre": "Doom Metal, Gothic Doom", "mood": "Gothic, varied, doom", "style": "Swedish gothic doom pioneers, evolved to rock", "vocal_style": "Jonas Renkse, distinctive, dynamic, varied", "instruments": "Gothic doom, varied, layered", "production": "Gothic doom polish, varied, varied"},
    "tiamat": {"genre": "Doom Metal, Gothic Doom", "mood": "Gothic, varied, doom", "style": "Swedish gothic doom, evolved into rock", "vocal_style": "Johan Edlund, distinctive, dynamic, varied", "instruments": "Gothic doom, varied, layered", "production": "Gothic doom polish, varied, varied"},
    "theatre of tragedy": {"genre": "Doom Metal, Gothic Metal", "mood": "Gothic, varied, metal", "style": "Norwegian gothic metal pioneers, 'Aégis'", "vocal_style": "Liv Kristine / Raymond Rohonyi, distinctive, dynamic, varied", "instruments": "Gothic metal, varied, layered", "production": "Gothic metal polish, varied, varied"},
    "lacuna coil": {"genre": "Doom Metal, Gothic Metal", "mood": "Gothic, varied, metal", "style": "Italian gothic metal, 'In a Reverie'", "vocal_style": "Cristina Scabbia / Andrea Ferro, distinctive, dynamic, varied", "instruments": "Gothic metal, varied, layered", "production": "Gothic metal polish, varied, varied"},
    "within temptation": {"genre": "Doom Metal, Symphonic Metal", "mood": "Symphonic, varied, metal", "style": "Dutch symphonic metal, 'Mother Earth'", "vocal_style": "Sharon den Adel, distinctive, dynamic, varied", "instruments": "Symphonic metal, varied, layered", "production": "Symphonic metal polish, varied, varied"},
    "epica": {"genre": "Doom Metal, Symphonic Metal", "mood": "Symphonic, varied, metal", "style": "Dutch symphonic metal, 'The Phantom Agony'", "vocal_style": "Simone Simons / Mark Jansen, distinctive, dynamic, varied", "instruments": "Symphonic metal, varied, layered", "production": "Symphonic metal polish, varied, varied"},

    # === Corrido (6 more to hit 25) ===
    "fuerza regida": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados pioneer, energetic", "vocal_style": "Fuerza Regida, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "jose guicho two": {"genre": "Corridos Bélicos, Regional Mexican", "mood": "Gritty, varied, Mexican", "style": "Mexican corridos bélicos, gritty", "vocal_style": "Jose Guicho, distinctive, raw, varied", "instruments": "Corridos bélicos, regional Mexican, varied", "production": "Corridos bélicos polish, raw, varied"},
    "el de la guitarra": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados, guitar-driven", "vocal_style": "El De La Guitarra, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "los alegres del barranco": {"genre": "Corridos Bélicos, Regional Mexican", "mood": "Gritty, varied, Mexican", "style": "Mexican corridos bélicos, foundational", "vocal_style": "Los Alegres Del Barranco, distinctive, raw, varied", "instruments": "Corridos bélicos, regional Mexican, varied", "production": "Corridos bélicos polish, raw, varied"},
    "gerardo ortiz": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican corridos tumbados pioneer, Grammy-nominated", "vocal_style": "Gerardo Ortiz, distinctive, dynamic, varied", "instruments": "Corridos, regional Mexican, varied", "production": "Corridos tumbados polish, modern, layered"},
    "banda ms": {"genre": "Corridos Tumbados, Banda", "mood": "Energetic, varied, Mexican", "style": "Mexican banda-corridos, energetic", "vocal_style": "Banda MS, distinctive, dynamic, varied", "instruments": "Banda, corridos, varied", "production": "Banda-corridos polish, energetic, varied"},
    "grupo frontera": {"genre": "Corridos Tumbados, Regional Mexican", "mood": "Energetic, varied, Mexican", "style": "Mexican regional group, corridos tumbados", "vocal_style": "Grupo Frontera, distinctive, dynamic, varied", "instruments": "Regional Mexican, corridos, varied", "production": "Regional Mexican polish, modern, varied"},

    # === CCM worship (9 more to hit 25) ===
    "worship artist bethel": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Bethel Music, modern worship", "vocal_style": "Varies, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "hillsong worship artist": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Hillsong, modern worship", "vocal_style": "Varies, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "elevation worship leader": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Elevation Worship, modern worship", "vocal_style": "Varies, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "kari jobe worship": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Kari Jobe, modern worship", "vocal_style": "Kari Jobe, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "cody carnes worship": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Cody Carnes, modern worship", "vocal_style": "Cody Carnes, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "bethel worship leader": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Bethel Music, modern worship", "vocal_style": "Varies, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "hillsong worship leader": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Hillsong, modern worship", "vocal_style": "Varies, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
    "passion worship leader": {"genre": "CCM, Worship", "mood": "Anthemic, varied, worship", "style": "Passion Conferences, modern worship", "vocal_style": "Varies, anthemic, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, anthemic, varied"},
    "worship artist bethel new": {"genre": "CCM, Worship", "mood": "Reverent, varied, worship", "style": "Bethel Music, modern worship", "vocal_style": "Varies, reverent, distinctive, varied", "instruments": "Worship band, varied, layered", "production": "Modern worship polish, reverent, varied"},
}

# ====================
#   GENRE TEMPLATES
# ====================
DEFAULT_TEMPLATES = {
    "pop": {"genre": "Pop", "mood": "Upbeat, catchy", "style": "Catchy melodies, polished", "vocal_style": "Clear, melodic", "instruments": "Synths, drums", "production": "Polished, modern"},
    "rock": {"genre": "Rock", "mood": "Passionate, energetic", "style": "Guitar-driven, authentic", "vocal_style": "Raw, powerful", "instruments": "Electric guitar, drums", "production": "Live feel, powerful"},
    "hip-hop": {"genre": "Hip-Hop", "mood": "Confident, rhythmic", "style": "Beat-driven, lyrical", "vocal_style": "Rhythmic, flow", "instruments": "Beats, bass", "production": "Beat-heavy, modern"},
    "rnb": {"genre": "R&B", "mood": "Smooth, soulful", "style": "Romantic, smooth", "vocal_style": "Soulful, melismatic", "instruments": "Smooth synths, piano", "production": "Warm, atmospheric"},
    "electronic": {"genre": "Electronic", "mood": "Energetic, futuristic", "style": "Synth-driven, danceable", "vocal_style": "Processed, minimal", "instruments": "Synthesizers, drum machines", "production": "Clean, electronic"},
    "metal": {"genre": "Metal", "mood": "Intense, dark", "style": "Heavy, aggressive", "vocal_style": "Aggressive, powerful", "instruments": "Heavy guitar, drums", "production": "Heavy, raw"},
    "doom": {"genre": "Doom Metal", "mood": "Funereal, crushing, weighty", "style": "Slow, monolithic riffs, never anthemic", "vocal_style": "Low baritone or operatic, raw and heavy", "instruments": "Massive downtuned guitar, slow drums, organ drone", "production": "Cathedral reverb, monolithic low end, chiaroscuro mix"},
    "indie": {"genre": "Indie", "mood": "Introspective, cool", "style": "Alternative, authentic", "vocal_style": "Conversational, unique", "instruments": "Guitar, unconventional", "production": "Raw, authentic"},
    "jazz": {"genre": "Jazz", "mood": "Cool, sophisticated", "style": "Improvisational, smooth", "vocal_style": "Smooth, velvety", "instruments": "Piano, sax, trumpet", "production": "Live, spacious"},
    "country": {"genre": "Country", "mood": "Warm, nostalgic", "style": "Storytelling, acoustic", "vocal_style": "Twang, clear", "instruments": "Acoustic guitar, fiddle", "production": "Warm, organic"},
    "folk": {"genre": "Folk", "mood": "Earthy, warm", "style": "Acoustic, traditional", "vocal_style": "Warm, storytelling", "instruments": "Acoustic guitar, banjo", "production": "Organic, warm"},
    "latin": {"genre": "Latin, Reggaeton", "mood": "Hot, confident, rhythmic", "style": "Latin urban rhythms, dembow beats, bilingual hooks", "vocal_style": "Charismatic, melodic reggaeton, occasional rap verses", "instruments": "Dembow riddims, reggaeton synths, Latin percussion, accordion", "production": "Tropical polish, modern Latin urbano"},
    "corrido": {"genre": "Mexican Regional, Corridos Tumbados", "mood": "Stoic, narrative, swagger", "style": "Modern corrido with trap-influenced production, storytelling verses", "vocal_style": "Clear conversational baritone, occasional autotune, narrative", "instruments": "Tubas, accordion, requinto, trap 808s, cumbia percussion", "production": "Tubazo meets trap, regional Mexican global polish"},
    "bollywood": {"genre": "Bollywood, Indian Film Music", "mood": "Romantic, dramatic, emotional", "style": "Indian film song structure, lush orchestration, expressive melodies", "vocal_style": "Soaring Hindi/Urdu playback singing, melismatic, emotional", "instruments": "Tabla, sitar, dholak, harmonium, modern pop production, strings", "production": "Cinematic Indian film, layered orchestration, polished modern pop"},
    "punjabi": {"genre": "Punjabi Pop, Bhangra-Fusion", "mood": "Energetic, celebratory, romantic", "style": "Bhangra rhythms with modern hip-hop and pop production", "vocal_style": "Punjabi-language melodic singing, English hooks, charismatic flows", "instruments": "Dhol, bhangra percussion, tumbi, modern 808s, synth bass", "production": "Global Punjabi pop, festival-ready, polished crossover"},
    "indian-indie": {"genre": "Indian Indie, Desi Alternative", "mood": "Introspective, romantic, wistful", "style": "English-Hindi indie folk-pop, acoustic intimacy with modern production", "vocal_style": "Soft, breathy, conversational, indie singer-songwriter", "instruments": "Acoustic guitar, soft synths, light tabla, lo-fi textures", "production": "Lo-fi to polished indie, intimate bedroom-pop feel"},
    "italian": {"genre": "Italian Pop, Sanremo Style", "mood": "Romantic, dramatic, melodic", "style": "Italian melodic pop, often Eurovision-ready, emotional storytelling", "vocal_style": "Expressive Italian tenor/baritone, passionate, clear diction", "instruments": "Strings, piano, modern pop band, occasional orchestral", "production": "Polished European pop, dramatic builds, classic Italian melody"},
    "kpop": {"genre": "K-Pop", "mood": "High-energy, polished, varied", "style": "Genre-hopping idol pop, tight choreography, maximalist production", "vocal_style": "Group harmonies + lead belting, rapping verses, K-Pop idol vocals", "instruments": "EDM drops, synths, brass, hip-hop drums, layered vocals", "production": "Slick, high-budget, multi-genre hybrid, polished to perfection"},
    "afrobeats": {"genre": "Afrobeats, Afropop, Amapiano", "mood": "Warm, rhythmic, joyful", "style": "West African rhythms with global pop hooks, danceable log drums", "vocal_style": "Pidgin English / Yoruba / melodic, warm, rhythmic, charismatic", "instruments": "Log drums, talking drum, congas, 808s, afrobeats synths", "production": "Global afrobeats polish, amapiano log-drum bounce, summer-ready"},
    "bedroom": {"genre": "Bedroom Pop, Indie Slacker", "mood": "Lo-fi, intimate, nostalgic", "style": "Lo-fi home-recorded indie, tape hiss, casual intimacy", "vocal_style": "Soft, breathy, conversational, sometimes shy, often doubled", "instruments": "Electric guitar with chorus, drum machine, lo-fi synths, jangly keys", "production": "4-track cassette feel, warm saturation, raw bedroom intimacy"},
    "modern-heavy": {"genre": "Modern Heavy, Metalcore", "mood": "Heavy, emotional, dynamic", "style": "Modern metalcore / post-hardcore with cinematic dynamic shifts", "vocal_style": "Harsh screams + soaring cleans, dynamic contrast, emotional range", "instruments": "Down-tuned guitar, electronic elements, cinematic synths, dynamic drums", "production": "Polished modern heavy, room-shaking low end, huge dynamics"}
}

# ====================
#   FUNCTIONS
# ====================

def find_singer(name):
    return SINGER_DB.get(name.lower().strip())

def detect_genre(name):
    n = name.lower().strip()
    # Order matters: most specific first
    if any(x in n for x in ["metalcore", "modern heavy", "post-hardcore"]): return "modern-heavy"
    if any(x in n for x in ["doom", "sludge", "funeral", "drone", "stoner doom"]): return "doom"
    if any(x in n for x in ["metal", "thrash", "prog"]) and "metalcore" not in n: return "metal"
    if any(x in n for x in ["rock", "punk", "grunge", "alt"]) and "alté" not in n and "alte" not in n: return "rock"
    if any(x in n for x in ["electro", "techno", "house", "edm"]): return "electronic"
    if any(x in n for x in ["rap", "hip", "trap"]) and "kpop" not in n and "k-pop" not in n and "mexican" not in n and "from mexico" not in n and "corrido" not in n and "tumbado" not in n and "tubazo" not in n: return "hip-hop"
    if any(x in n for x in ["r&b", "rnb", "soul"]): return "rnb"
    # Latin/reggaeton BEFORE corrido — so "Mexican reggaeton" hits latin, not corrido
    if any(x in n for x in ["latin", "reggaeton", "urbano", "cumbia", "salsa", "bachata"]): return "latin"
    # Corrido: explicit keywords OR "mexican"/"from mexico" but not when "reggaeton" or "latin" is explicit
    if (any(x in n for x in ["corrido", "tumbado", "tubazo", "regional mexican", "belico", "bélico"]) or
        (("mexican" in n or "from mexico" in n) and "reggaeton" not in n and "latin" not in n)): return "corrido"
    if any(x in n for x in ["punjabi", "punjab", "bhangra", "bhangra-fusion"]): return "punjabi"
    if any(x in n for x in ["bollywood", "hindi", "indian film", "playback"]): return "bollywood"
    if any(x in n for x in ["indian indie", "desi alt", "anuv", "prateek"]): return "indian-indie"
    if any(x in n for x in ["kpop", "k-pop"]): return "kpop"
    if any(x in n for x in ["afrobeats", "afropop", "amapiano", "afro-fusion", "alté", "alte"]): return "afrobeats"
    if any(x in n for x in ["bedroom", "slacker", "lo-fi indie", "lo fi indie"]): return "bedroom"
    if any(x in n for x in ["italian", "sanremo", "italo"]): return "italian"
    if "indie" in n or "folk" in n: return "indie"
    if "jazz" in n: return "jazz"
    if "country" in n or "americana" in n or "outlaw" in n: return "country"
    return "pop"

def generate_prompt(singer, custom_mood="", custom_theme="", custom_tempo=""):
    data = find_singer(singer)
    if data:
        mood = custom_mood or data["mood"]
        tempo = f"Tempo: {custom_tempo}" if custom_tempo else ""
        # Note: Suno flags artist names. We reference the artist only as "[Style Profile]"
        # and describe the sound via genre / style / mood / vocal_style.
        return f"""[Style Profile]

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
        return f"""[Style Profile - {t['genre']}]

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

Note: Artist not in database. Using {t['genre']} defaults. Add them to SINGER_DB for better results."""

def get_random_artist():
    return random.choice(list(SINGER_DB.keys()))

# ====================
#   SIDEBAR
# ====================
with st.sidebar:
    # Iron Vespers branded sidebar header with wolf logo
    if _LOGO_B64:
        st.markdown(f"""
        <div class="iv-hero" style="padding: 12px 0 16px 0; margin-bottom: 12px;">
            <img src="data:image/svg+xml;base64,{_LOGO_B64}" alt="Iron Vespers Wolf"/>
            <div class="iv-hero-text">
                <h1 style="font-size: 1.4em; margin: 0;">Iron Vespers</h1>
                <div class="iv-tag" style="font-size: 0.85em;">Suno Prompt Pro</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title("🐺 Iron Vespers")
        st.markdown("**Suno Prompt Pro**")
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

# Main hero header — Iron Vespers branded (rendered ABOVE the tabs so tab bodies are clean)
if _LOGO_B64:
    st.markdown(f"""
    <div class="iv-hero">
        <img src="data:image/svg+xml;base64,{_LOGO_B64}" alt="Iron Vespers Wolf"/>
        <div class="iv-hero-text">
            <h1>Iron Vespers</h1>
            <div class="iv-tag">Suno Prompt Generator Pro · 136 artists · 21 genres</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.title("🐺 Iron Vespers — Suno Prompt Pro")

# ====================
#   TABS (key= enables programmatic tab switching via st.session_state)
# ====================
# If a callback set active_tab_label this run, seed the tabs widget key with it.
# This forces the tabs to switch on the rerun. The widget reads its value from
# st.session_state["main_tabs"] on every render.
_pending = st.session_state.pop("active_tab_label", None)
if _pending is not None:
    st.session_state.main_tabs = _pending
elif "main_tabs" not in st.session_state:
    st.session_state.main_tabs = "✨ Generate"

tab1, tab2, tab3, tab4 = st.tabs(
    ["✨ Generate", "🎲 Random", "📚 Artists", "⚙️ Settings"],
    key="main_tabs",
    on_change="rerun",
    default=st.session_state.main_tabs,
)

with tab1:
    st.markdown("### ⚔️ Generate Prompt")
    st.caption("Type an artist name, or use the buttons below. The app will fuse the artist's sound with the matching genre template.")

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
        
        col_mood, col_theme, col_tempo = st.columns(3)
        with col_mood:
            custom_mood = st.selectbox(
                "Mood",
                ["", "Melancholic", "Energetic", "Dreamy", "Dark", "Uplifting",
                 "Nostalgic", "Intense", "Romantic", "Defiant", "Sacred",
                 "Funereal", "Aggressive", "Triumphant", "Bittersweet", "Hopeful"],
            )
        with col_theme:
            custom_theme = st.selectbox(
                "Theme",
                ["", "Heartbreak", "Loss", "Love", "Celebration", "Night drive",
                 "Summer", "Rain", "Space", "Time", "Faith", "Redemption",
                 "War", "Nature", "Death", "Rebirth", "Longing", "Struggle"],
            )
        with col_tempo:
            custom_tempo = st.selectbox(
                "Tempo",
                ["", "Slow", "Medium", "Fast", "Upbeat", "Ballad"],
            )
        
        if st.button("🎵 Generate Prompt", type="primary", use_container_width=True):
            if singer.strip():
                result = generate_prompt(singer, custom_mood, custom_theme, custom_tempo)
                st.code(result, language=None)
                st.download_button(
                    "📋 Copy to Clipboard",
                    result,
                    file_name=f"{singer.replace(' ', '_')}_prompt.txt",
                    use_container_width=True
                )
            else:
                st.warning("Enter an artist name!")
        
        if st.button("🧹 Clear Artist Field", on_click=cb_clear_artist):
            pass

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
        # Map display label -> search term used in the Artists tab
        genres = {
            "Pop": "pop",
            "Rock": "rock",
            "Hip-Hop": "hip",
            "R&B": "r&b",
            "Electronic": "electronic",
            "Metal": "metal",
            "Doom": "doom",
            "Indie": "indie",
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
        for label, term in genres.items():
            st.button(
                label,
                key=f"gen_{label}",
                use_container_width=True,
                on_click=cb_select_genre,
                args=(term,),
            )

# Rest of the tabs (tab2, tab3, tab4) remain the same as in your last working version
# (random generator, artist database with search, settings)

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
        
        result = generate_prompt(artist, random_mood, random_theme, random_tempo)
        
        st.success(f"Generated: **{artist.title()}** style")
        st.code(result, language=None)
        st.download_button(
            "📋 Save Prompt",
            result,
            file_name=f"random_{artist.replace(' ', '_')}_prompt.txt"
        )

with tab3:
    st.title("Artist Database")

    # Read pending filter from session_state (set by cb_select_genre), then clear it
    # so the user's typing isn't overwritten on next rerun.
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
        # Match artist name OR genre field — so "doom" surfaces Candlemass/Saint Vitus/etc.
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

with tab4:
    st.title("⚙️ Settings & Info")
    
    st.subheader("About")
    st.markdown(f"""
    **Suno Prompt Generator Pro** helps you create detailed prompts for Suno AI music generation.
    
    **Features:**
    - {len(SINGER_DB)} curated artists
    - Genre fallback for unknown artists
    - Custom mood, theme, tempo
    - Random generator
    - Persistent selection from Artists tab
    - Export as .txt
    """)
    
    st.subheader("How to Use")
    st.markdown("""
    1. Pick artist from Popular, Artists tab or type name
    2. Optional: add mood / theme / tempo
    3. Click Generate
    4. Copy or download prompt
    5. Paste into Suno → create!
    """)
    
    st.subheader("Add Custom Artists")
    st.code("""
"new artist": {
    "genre": "Your Genre",
    "mood": "Your Mood",
    "style": "...",
    "vocal_style": "...",
    "instruments": "...",
    "production": "..."
}
    """, language="python")