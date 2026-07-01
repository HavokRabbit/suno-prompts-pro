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

    # === Rock / Alt Rock ===
    "queen": {"genre": "Rock, Arena Rock", "mood": "Epic, dramatic, triumphant", "style": "Operatic, theatrical, anthemic", "vocal_style": "Powerful, operatic, multi-octave", "instruments": "Electric guitar, piano, layered vocals", "production": "Grand, stadium-filling, layered"},
    "nirvana": {"genre": "Grunge, Alternative", "mood": "Angsty, melancholic, intense", "style": "Raw, distorted, dynamic shifts", "vocal_style": "Raspy, strained, soft-loud", "instruments": "Distorted guitar, bass, heavy drums", "production": "Lo-fi, raw, garage"},
    "foo fighters": {"genre": "Alternative Rock", "mood": "Uplifting, defiant, energetic", "style": "Energetic, melodic, driving", "vocal_style": "Raw, powerful, melodic", "instruments": "Electric guitar, bass, drums", "production": "Clean, powerful, radio-friendly"},
    "arctic monkeys": {"genre": "Indie Rock, Garage", "mood": "Cool, detached, energetic", "style": "Witty lyrics, angular guitars", "vocal_style": "Conversational, Sheffield accent", "instruments": "Jangly guitar, bass, drums", "production": "Raw, live energy"},
    "radiohead": {"genre": "Alternative, Art Rock", "mood": "Melancholic, anxious, atmospheric", "style": "Experimental, electronic elements", "vocal_style": "Emotional, falsetto, strained", "instruments": "Guitar, synths, orchestral", "production": "Atmospheric, layered, experimental"},
    "led zeppelin": {"genre": "Hard Rock, Blues Rock", "mood": "Epic, powerful, mystical", "style": "Blues-based, heavy riffs", "vocal_style": "Powerful, wailing, bluesy", "instruments": "Electric guitar, drums, bass", "production": "Raw, powerful, live"},
    "linkin park": {"genre": "Nu-Metal, Alternative Rock", "mood": "Intense, emotional, aggressive", "style": "Rap-rock fusion, heavy drops", "vocal_style": "Screaming + melodic rap", "instruments": "Heavy guitars, electronics, turntables", "production": "Aggressive, layered"},

    # === Hip-Hop / Rap ===
    "kendrick lamar": {"genre": "Hip-Hop, Jazz Rap", "mood": "Introspective, urgent, complex", "style": "Lyrically dense, socially conscious", "vocal_style": "Versatile, rapid-fire, melodic", "instruments": "Jazz samples, live instruments", "production": "Layered, organic, sophisticated"},
    "drake": {"genre": "Hip-Hop, R&B", "mood": "Melancholic, confident, romantic", "style": "Melodic rap, emotional", "vocal_style": "Melodic rapping, singing", "instruments": "808s, smooth synths", "production": "Polished, atmospheric, moody"},
    "kanye west": {"genre": "Hip-Hop, Experimental", "mood": "Dramatic, confident, introspective", "style": "Boundary-pushing, soul samples", "vocal_style": "Confident, emotional, varied", "instruments": "Orchestral, synths, samples", "production": "Layered, experimental, detailed"},
    "tyler the creator": {"genre": "Hip-Hop, Alternative", "mood": "Playful, confident, introspective", "style": "Eccentric, genre-blending", "vocal_style": "Deep, aggressive, melodic", "instruments": "Live instruments, synths", "production": "Colorful, experimental, warm"},
    "travis scott": {"genre": "Hip-Hop, Trap", "mood": "Dark, psychedelic, energetic", "style": "Atmospheric trap, auto-tune", "vocal_style": "Auto-tuned, melodic, ad-libs", "instruments": "Heavy 808s, synths", "production": "Atmospheric, distorted, spacey"},
    "doechii": {"genre": "Hip-Hop, Experimental", "mood": "Bold, theatrical, fierce", "style": "Eclectic flows, genre-hopping", "vocal_style": "Versatile, commanding, playful", "instruments": "Trap, jazz, electronic", "production": "Dynamic, cinematic"},
    "anderson .paak": {"genre": "R&B, Funk, Soul", "mood": "Groovy, warm, joyful", "style": "Retro-soul funk with hip-hop edge", "vocal_style": "Smooth falsetto, silky, charismatic rapping", "instruments": "Live drums, bass, Rhodes, horns", "production": "Warm vintage polish, organic groove"},

    # === R&B / Soul ===
    "frank ocean": {"genre": "R&B, Alternative", "mood": "Dreamy, melancholic, intimate", "style": "Introspective, experimental", "vocal_style": "Breathy, understated, falsetto", "instruments": "Sparse synths, guitars", "production": "Minimal, atmospheric, hazy"},
    "beyonce": {"genre": "R&B, Pop", "mood": "Confident, fierce, soulful", "style": "Powerful vocals, genre-blending", "vocal_style": "Powerful, agile, commanding", "instruments": "Full band, horns, strings", "production": "Polished, powerful, modern"},
    "sza": {"genre": "R&B, Alternative", "mood": "Romantic, confident, melancholic", "style": "Alternative R&B, introspective", "vocal_style": "Soulful, raspy, unique", "instruments": "Smooth synths, guitar", "production": "Atmospheric, warm, modern"},
    "daniel caesar": {"genre": "R&B, Soul", "mood": "Intimate, spiritual, romantic", "style": "Neo-soul, gospel influences", "vocal_style": "Smooth, falsetto, soulful", "instruments": "Guitar, piano, minimal", "production": "Warm, organic, intimate"},
    "victoria monét": {"genre": "R&B, Pop", "mood": "Sensual, empowering, groovy", "style": "Silky melodies, confident", "vocal_style": "Smooth, layered harmonies", "instruments": "Synths, bass, percussion", "production": "Polished, lush"},
    "morgan wallen": {"genre": "Country, Pop Country", "mood": "Heartfelt, rowdy, nostalgic", "style": "Storytelling, party anthems", "vocal_style": "Twangy, emotive", "instruments": "Acoustic/electric guitar, drums", "production": "Modern country polish"},

    # === Electronic ===
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
            "K-Pop": "kpop",
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