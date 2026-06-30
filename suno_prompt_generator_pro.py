import streamlit as st
import random

# ====================
#   IRON VESPERS BRANDING
# ====================
def _load_logo_svg():
    """Return the raw SVG markup (not base64) so animations and styling work inline."""
    try:
        with open("static/wolf_logo.svg", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

_LOGO_SVG = _load_logo_svg()

st.set_page_config(
    page_title="Iron Vespers — Suno Prompt Generator Pro",
    page_icon="🐺",  # Wolf emoji as fallback (the SVG wolf renders inline in the hero)
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
.iv-hero .iv-wolf { width: 80px; height: 80px; flex-shrink: 0; }
.iv-hero .iv-wolf svg { width: 100%; height: 100%; display: block; }
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

/* Wolf logo animations — pulsing red eyes + subtle floating motion */
.iv-wolf .wolf-eye {
    animation: eyePulse 2.4s ease-in-out infinite;
    transform-origin: center;
}
.iv-wolf .wolf-eye-right {
    animation-delay: 0.2s;
}
.iv-wolf .wolf-glow {
    animation: glowFlicker 3s ease-in-out infinite;
}
.iv-wolf .wolf-head {
    animation: headFloat 4s ease-in-out infinite;
    transform-origin: center;
}
@keyframes eyePulse {
    0%, 100% { opacity: 1; filter: drop-shadow(0 0 4px #FF1F44); }
    50% { opacity: 0.55; filter: drop-shadow(0 0 12px #FF1F44); }
}
@keyframes glowFlicker {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 0.7; }
}
@keyframes headFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}

/* Sidebar wolf animations - smaller scale */
section[data-testid="stSidebar"] .iv-wolf .wolf-head {
    animation: headFloat 5s ease-in-out infinite;
}
section[data-testid="stSidebar"] .iv-wolf .wolf-eye {
    animation: eyePulse 2.4s ease-in-out infinite;
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
        return f"""[{singer.title()} Style]

Genre: {data['genre']}
Style: {data['style']}
Mood: {mood}
Vocal Style: {data['vocal_style']}
Instrumentation: {data['instruments']}
Production: {data['production']}
{tempo}
{f'Theme: {custom_theme}' if custom_theme else ''}

---
[Short Prompt]: {data['genre'].split(',')[0]} song in the style of {singer.title()}, {mood.split(',')[0].lower()} mood, {data['vocal_style'].split(',')[0].lower()} vocals"""
    else:
        g = detect_genre(singer)
        t = DEFAULT_TEMPLATES.get(g, DEFAULT_TEMPLATES["pop"])
        mood = custom_mood or t["mood"]
        tempo = f"Tempo: {custom_tempo}" if custom_tempo else ""
        return f"""[{singer.title()} Style - {t['genre']}]

Genre: {t['genre']}
Style: {t['style']}
Mood: {mood}
Vocal Style: {t['vocal_style']}
Instrumentation: {t['instruments']}
Production: {t['production']}
{tempo}
{f'Theme: {custom_theme}' if custom_theme else ''}

---
[Short Prompt]: {t['genre']} song in the style of {singer.title()}, {mood.split(',')[0].lower()} mood

Note: Singer not in database. Using {t['genre']} defaults. Add them to SINGER_DB for better results."""

def get_random_artist():
    return random.choice(list(SINGER_DB.keys()))

# ====================
#   SIDEBAR
# ====================
with st.sidebar:
    # Iron Vespers branded sidebar header with wolf logo
    if _LOGO_SVG:
        st.markdown(f"""
        <div class="iv-hero" style="padding: 12px 0 16px 0; margin-bottom: 12px;">
            <div class="iv-wolf">{_LOGO_SVG}</div>
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

    if st.button("🎲 Random Artist"):
        st.session_state.random_artist = get_random_artist()
        st.rerun()

    st.markdown("---")
    st.markdown("**Quick Links**")
    st.markdown("[Suno AI](https://suno.com)")
    st.markdown("[Iron Vespers](https://github.com/HavokRabbit/Suno-prompts-pro)")

# ====================
#   TABS
# ====================
tab1, tab2, tab3, tab4 = st.tabs(["✨ Generate", "🎲 Random", "📚 Artists", "⚙️ Settings"])

# Main hero header — Iron Vespers branded
if _LOGO_SVG:
    st.markdown(f"""
    <div class="iv-hero">
        <div class="iv-wolf">{_LOGO_SVG}</div>
        <div class="iv-hero-text">
            <h1>Iron Vespers</h1>
            <div class="iv-tag">Suno Prompt Generator Pro · 136 artists · 21 genres</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.title("🐺 Iron Vespers — Suno Prompt Pro")

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
            custom_mood = st.text_input("Mood", placeholder="e.g., melancholic")
        with col_theme:
            custom_theme = st.text_input("Theme", placeholder="e.g., heartbreak")
        with col_tempo:
            custom_tempo = st.selectbox("Tempo", ["", "Slow", "Medium", "Fast", "Upbeat", "Ballad"])
        
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
        
        if st.button("🧹 Clear Artist Field"):
            st.session_state.pop('selected_artist', None)
            st.session_state.pop('random_artist', None)
            st.rerun()
    
    with col2:
        st.subheader("⭐ Popular")
        popular = ["taylor swift", "billie eilish", "kendrick lamar", "queen", "frank ocean", "daft punk", "sabrina carpenter", "chappell roan", "iron vespers", "candlemass", "demon hunter", "bad bunny", "arijit singh", "burna boy", "maneskin", "bts", "peso pluma", "karan aujla", "tyla", "sal da vinci"]
        for artist in popular:
            if st.button(artist.title(), key=f"pop_{artist}", use_container_width=True):
                st.session_state.selected_artist = artist
                st.rerun()
        
        st.markdown("---")
        st.subheader("🎸 By Genre")
        genres = ["Pop", "Rock", "Hip-Hop", "R&B", "Electronic", "Metal", "Doom", "Indie", "Bedroom", "Country", "Latin", "Corrido", "Reggaeton", "K-Pop", "Bollywood", "Punjabi", "Indian Indie", "Italian", "Afrobeats", "Hyperpop", "Modern Heavy", "CCM", "Christian Metal"]
        for g in genres:
            if st.button(g, key=f"gen_{g}", use_container_width=True):
                st.info(f"Search for {g} artists in the Artists tab!")

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
    
    search = st.text_input(
        "🔍 Search artists",
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
        matches = [(n, d) for n, d in artists if not search_term or search_term in n]
        if matches:
            found_any = True
            with st.expander(f"{genre} ({len(matches)} found)"):
                for name, data in matches:
                    st.markdown(f"**{name.title()}**")
                    st.caption(f"{data['mood']} • {data['genre']}")
                    if st.button(f"Use {name.title()}", key=f"use_artist_{name}"):
                        st.session_state.selected_artist = name
                        st.rerun()
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