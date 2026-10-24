"""Original musical starting points, not claims about individual artists.

Broad categories are navigation shelves; an artist may belong to several.
When a specific sourced style is available it wins over the broad template.
"""
import re
import unicodedata

FIELDS = ('genre','mood','style','vocal_style','instruments','production')

def profile(genre,mood,style,voice,instruments,production):
    return dict(zip(FIELDS,(genre,mood,style,voice,instruments,production)))

GENRES = {
'pop': ('Pop','Pop'), 'rock':('Rock','Rock'), 'hip-hop':('Hip-hop','Hip-hop'),
'rnb':('R&B / soul','R&B / soul'), 'electronic':('Electronic','Electronic'),
'metal':('Metal','Metal'), 'doom':('Doom / sludge','Metal'), 'indie':('Indie','Rock'),
'jazz':('Jazz','Jazz & roots'), 'country':('Country / Americana','Jazz & roots'),
'folk':('Folk / acoustic','Jazz & roots'), 'latin':('Latin','Global scenes'),
'corrido':('Corridos / regional Mexican','Global scenes'),
'bollywood':('Bollywood / filmi','Global scenes'), 'punjabi':('Punjabi / bhangra','Global scenes'),
'indian-indie':('Indian indie','Global scenes'), 'italian':('Italian pop / rock','Global scenes'),
'kpop':('K-pop','Global scenes'), 'afrobeats':('Afrobeats / Afropop','Global scenes'),
'bedroom':('Bedroom pop / lo-fi indie','Rock'), 'modern-heavy':('Metalcore / modern heavy','Metal'),
'ccm':('CCM / worship / gospel','Faith'), 'christian':('Christian metal','Faith'),
'hyperpop':('Hyperpop / digicore','Electronic'), 'reggae':('Reggae / dub / dancehall','Jazz & roots'),
'dnb':('Drum & bass / jungle','Electronic'), 'techno':('Techno','Electronic'),
'house':('House','Electronic'), 'blues':('Blues','Jazz & roots'),
'punk':('Punk / post-punk','Rock'), 'grunge':('Grunge / post-grunge','Rock'),
'classical':('Classical / orchestral','Classical')}

TEMPLATES = {
'pop':profile('Pop','Bright, emotionally direct','Memorable melodic hook; concise verse-to-chorus lift','Melodic lead, controlled doubles at the hook','Synth bass, drum kit, keyboards, rhythmic guitar','Clear lead vocal, defined low end, layered but uncluttered choruses'),
'rock':profile('Rock','Urgent, driven','Riff-led arrangement; live-band dynamics; a strong recurring refrain','Expressive lead with a natural edge','Electric guitars, bass guitar, acoustic drum kit','Distinct guitar layers, audible room ambience, punchy transients'),
'hip-hop':profile('Hip-hop','Confident, focused','Rhythm-led verses; internal rhyme; space around the vocal','Rhythmic rap delivery; a contrasting melodic or spoken hook','Programmed drums, sub bass, chopped melodic motif','Forward vocal, articulate kick and bass, sparse arrangement around the bars'),
'rnb':profile('R&B, Soul','Warm, intimate','Syncopated pocket; extended chords; call-and-response backing parts','Expressive melodic lead with restrained ornamentation','Electric piano, bass, swung drums, soft guitar','Warm midrange, close vocal, layered harmonies with room to breathe'),
'electronic':profile('Electronic','Immersive, evolving','Motif-led sound design; deliberate builds and contrasting sections','Optional processed vocal texture; instrumental lead by default','Synthesizers, electronic percussion, sequenced bass','Detailed stereo field, controlled sub bass, evolving automation'),
'metal':profile('Heavy Metal','Forceful, dramatic','Riff-driven arrangement; clear rhythmic accents; contrasting lead section','Powerful lead; choose clean or harsh delivery to suit the subgenre','Distorted guitars, bass, drum kit, lead guitar','Tight rhythm section, separated guitars, dynamics between sections'),
'doom':profile('Doom Metal','Weighty, solemn','Slow sustained riffs; descending movement; long tension-and-release phrases','Low expressive clean lead or harsh voice chosen by the writer','Downtuned guitar, bass, slow drums, restrained organ','Dense low mids, natural sustain, deep but controlled reverb'),
'indie':profile('Indie Rock','Reflective, restless','Distinctive guitar motifs; intimate verses; an unforced melodic hook','Conversational lead with character rather than heavy polish','Guitars, bass, compact drums, understated keyboards','Textured midrange, light saturation, audible room character'),
'jazz':profile('Jazz','Warm, exploratory','Extended harmony; conversational ensemble phrasing; improvised development','Instrumental by default; optional phrased vocal lead','Piano, upright bass, brushed or swung drums, horns','Natural room, clear instrument separation, preserved dynamics'),
'country':profile('Country, Americana','Grounded, reflective','Story-first verses; memorable refrain; acoustic rhythmic foundation','Clear storytelling lead with natural phrasing','Acoustic guitar, bass, drums, pedal steel or fiddle','Warm band sound, intelligible lead, modest room reverb'),
'folk':profile('Folk','Intimate, earthy','Acoustic storytelling; simple recurring melody; restrained arrangement','Natural unforced lead; optional close harmonies','Fingerpicked acoustic guitar, light percussion, acoustic bass','Close microphones, audible string texture, minimal processing'),
'latin':profile('Latin Pop','Rhythmic, expressive','Song-led melodic hooks over a defined Latin rhythmic pattern','Expressive melodic lead; language chosen by the writer','Latin percussion, bass, piano, acoustic or electric guitar','Clear percussion transients, centered lead vocal, warm bass'),
'corrido':profile('Regional Mexican, Corrido','Narrative, resolute','Storytelling verses; acoustic string figures; regional ensemble rhythm','Direct narrative singing with clear phrasing','Requinto, acoustic guitar, bass or tuba; accordion when selected','Present strings and voice, coherent ensemble space, restrained effects'),
'bollywood':profile('Indian Film Music, Filmi','Romantic, cinematic','Expressive melodic development; a memorable refrain; instrumental interludes','Melodic playback-style phrasing; language chosen by the writer','Strings, hand percussion, keyboards, acoustic melodic instruments','Cinematic breadth with clear vocal focus and contrasting sections'),
'punjabi':profile('Punjabi Pop, Bhangra','Celebratory, rhythmic','Dhol-led bounce; recurring melodic hook; call-and-response accents','Rhythmic melodic singing; Punjabi if requested','Dhol, tumbi, bass, handclaps, contemporary drum programming','Crisp percussion, clear lead, controlled bass with rhythmic space'),
'indian-indie':profile('Indian Independent Music','Intimate, exploratory','Songwriter-led arrangement; acoustic or alternative-band textures','Conversational melodic lead; language selected by the writer','Guitar, bass, light drums, understated electronic texture','Personal small-room sound, natural phrasing, selective overdubs'),
'italian':profile('Italian Pop','Expressive, melodic','Strong melodic contour; narrative verses; a lifted refrain','Clear expressive melodic lead; Italian if requested','Piano, guitar, bass, drums, optional strings','Focused vocal, warm accompaniment, broad but controlled chorus'),
'kpop':profile('K-Pop','Dynamic, polished','Contrast between melodic verses, rhythmic sections and a recurring hook','Layered melodic leads, harmonies and optional rap contrast','Synth bass, programmed drums, keyboards, percussive accents','Precise transitions, tightly stacked harmonies, clear low end'),
'afrobeats':profile('Afrobeats','Warm, relaxed, danceable','Interlocking syncopation; repeating guitar or keyboard motif; melodic refrain','Relaxed rhythmic melodic lead; language chosen by the writer','Shakers, syncopated drums, rounded bass, plucked guitar or keys','Open percussion, dry forward lead, airy stereo ambience'),
'bedroom':profile('Bedroom Pop, Lo-fi Indie','Private, wistful','Small repeating motifs; compact arrangement; intimate melodic phrasing','Close conversational singing or soft doubles','Chorus guitar, drum machine, warm keys, bass','Gentle tape texture, intimate room, softened transients'),
'modern-heavy':profile('Metalcore, Modern Heavy','Intense, cathartic','Syncopated riffs; contrasting verse and hook; deliberate breakdown','Clean and harsh contrast when selected; articulate lead phrasing','Downtuned guitars, bass, double-kick drums, selective electronics','Tight low end, articulate guitars, impactful but unclipped drums'),
'ccm':profile('Contemporary Christian Music','Hopeful, devotional','Clear singable refrain; gradual dynamic build; testimony or worship theme','Sincere melodic lead with communal harmonies','Piano, acoustic guitar, electric swells, bass, drums','Open vocal, spacious supporting layers, controlled chorus build'),
'christian':profile('Christian Metal','Resolute, faith-driven','Heavy riff writing with a clear recurring hook; faith-centered lyrics if requested','Clean or harsh lead chosen to suit the metal subgenre','Distorted guitars, bass, drums, optional atmospheric keys','Articulate heavy rhythm section, defined vocals, contrasting dynamics'),
'hyperpop':profile('Hyperpop, Digicore','Playful, restless','Exaggerated pop hooks; abrupt textural contrasts; rhythmic digital edits','Processed melodic lead with controlled pitch effects','Bright digital synths, distorted bass, programmed drums, glitch accents','Intentional saturation and edits without uncontrolled output clipping'),
'reggae':profile('Reggae, Dub','Relaxed, grounded','Offbeat skank; spacious one-drop groove; repeating bass melody','Unhurried melodic phrasing or spoken rhythmic delivery','Skank guitar, organ bubble, rounded bass, one-drop drums','Deep bass, sparse arrangement, selective tape-delay and spring-reverb throws'),
'dnb':profile('Drum and Bass','Driving, kinetic','Fast breakbeat detail; strong sub-bass motif; contrast between breakdown and drop','Instrumental by default; optional short vocal motif','Chopped breaks, layered drums, sub bass, atmospheric pads','Tight transient control, mono sub bass, spacious midrange detail'),
'techno':profile('Techno','Hypnotic, driving','Four-on-the-floor pulse; repeating sequenced motif; gradual modulation','Instrumental by default; sparse voice texture if requested','Kick drum, sequenced bass, percussion, modular-style synth pattern','Controlled rumble, precise low end, spatial delay with slow filter movement'),
'house':profile('House','Warm, propulsive','Four-on-the-floor groove; syncopated bass; recurring chord and vocal hooks','Optional soulful hook or instrumental chord lead','Kick, claps, open hats, bass, piano or synth chords','Stable low end, rhythmic sidechain, clear groove and gradual builds'),
'blues':profile('Blues','Weathered, expressive','Call-and-response phrases; repeated harmonic cycle; dynamic guitar fills','Conversational expressive lead with bent notes and rough edges','Electric or acoustic guitar, bass, drums, harmonica or piano','Natural band space, touch-sensitive dynamics, light saturation'),
'punk':profile('Punk Rock','Urgent, defiant','Short direct sections; strong rhythmic attack; a repeatable shout-along refrain','Direct unpolished lead; optional group responses','Overdriven guitars, picked bass, fast drums','Lean arrangement, raw midrange, energetic room sound'),
'grunge':profile('Grunge, Alternative Rock','Raw, conflicted','Quiet-to-loud dynamics; heavy guitar riffs; imperfect live-band tension','Rough-edged melodic lead with dynamic restraint and release','Fuzz guitar, bass guitar, acoustic drums','Roomy drums, textured guitar distortion, natural vocal imperfections'),
'classical':profile('Classical, Orchestral','Expressive, expansive','Motivic development; instrumental counterpoint; shaped dynamic arcs','Instrumental; add choir only when explicitly requested','Strings, woodwinds, brass, orchestral percussion','Natural hall space, wide dynamic range, balanced orchestral sections'),
}

# More specific sourced genres must not inherit unrelated broad-category traits.
SUBSTYLES = {
'ambient music': profile('Ambient','Still, immersive','Slowly evolving harmony; sustained texture; no required beat','Instrumental, no lead vocal','Synth pads, drones, sparse tonal accents','Long reverb tails, gentle spectral changes, unhurried dynamics'),
'stoner rock': profile('Stoner Rock','Heavy, hazy','Fuzz riffs, blues-derived motifs, unhurried groove','Rough melodic lead','Fuzz guitar, bass, roomy drums','Thick mids, analog saturation, breathing band dynamics'),
'sludge metal': profile('Sludge Metal','Oppressive, abrasive','Slow riffs, dissonant accents, deliberate rhythmic weight','Raw harsh or barked lead','Downtuned guitars, distorted bass, heavy drums','Grainy distortion, physical low mids, limited polish'),
'death-doom': profile('Death-doom','Grieving, heavy','Slow death-metal riffs, melodic lament, long transitions','Deep harsh lead; optional clean contrast','Low-tuned guitars, bass, slow drums, atmospheric keyboards','Heavy sustained guitars, mournful space, clear kick separation'),
'synth-pop':profile('Synth-pop','Melodic, reflective','Repeating synth hook; structured pop verses; lifted chorus','Melodic lead, optional harmony doubles','Analog-style synths, drum machine, synth bass','Defined electronic drums, bright hooks, uncluttered stereo layers'),
'reggaeton':profile('Reggaeton','Confident, danceable','Dembow pulse; short rhythmic hooks; contrasting rap and melodic phrases','Rhythmic singing and rap; Spanish if requested','Dembow drums, sub bass, plucked synth hooks','Dry forward vocal, punchy drums, controlled low end'),
'salsa':profile('Salsa','Celebratory, rhythmic','Clave-based arrangement; montuno patterns; call-and-response coro','Lead and response phrasing','Piano montuno, bass tumbao, congas, timbales, brass','Live ensemble energy, clear percussion interplay, distinct brass accents'),
'amapiano':profile('Amapiano','Warm, hypnotic','Log-drum bass patterns; spacious rolling groove; repeated keyboard motifs','Optional melodic call and response','Log drum, shakers, piano, soft pads, percussion','Deep resonant bass, roomy arrangement, gradual rhythmic layering'),
'dub':TEMPLATES['reggae'], 'drum and bass':TEMPLATES['dnb'],
'jungle music':profile('Jungle','Raw, propulsive','Chopped breakbeat edits; syncopated sub bass; short breakdowns','Instrumental with optional short vocal calls','Sliced breaks, sub bass, dub textures, pads','Breakbeat detail, deep bass, delay throws, rugged rhythmic energy'),
'liquid funk':profile('Liquid Drum and Bass','Soulful, flowing','Rolling breaks; warm chord progression; smooth melodic bass movement','Optional soulful hook','Fast breaks, sub bass, electric piano, pads','Rounded transients, detailed highs, spacious melodic layers'),
'dream pop':profile('Dream Pop','Hazy, wistful','Sustained harmonic textures; gentle melodic hooks; unhurried pulse','Soft reverberant melodic lead','Chorus guitar, pads, bass, understated drums','Wide reverb, soft-edged layers, vocal integrated into the texture'),
'post-punk':profile('Post-punk','Tense, angular','Repetitive bass motifs; clipped guitar patterns; spacious drums','Detached or urgent lead phrasing','Melodic bass, angular guitar, drums, sparse synth','Dry rhythmic attack, selective reverb, bass-forward mix'),
'gospel music':profile('Gospel','Hopeful, fervent','Call-and-response; harmonic lift; expressive dynamic build','Lead vocal with responsive choir','Piano, organ, bass, drums, handclaps','Open lead and choir, natural ensemble dynamics, supportive rhythm section'),
'bluegrass music':profile('Bluegrass','Lively, earthy','Acoustic picking; alternating lead breaks; strong rhythmic pulse','Clear storytelling lead with close high harmonies','Banjo, fiddle, mandolin, acoustic guitar, upright bass','Natural acoustic balance, clear pick attack, minimal effects'),
'film score':profile('Film Score','Cinematic, evolving','Recurring leitmotif; scene-led tension; thematic development','Instrumental by default','Strings, brass, woodwinds, percussion, selective synth texture','Wide orchestral space, shaped crescendos, clear thematic focus'),
'nu metal':profile('Nu Metal','Aggressive, tense','Syncopated low riffs; hip-hop rhythmic influence; contrasting hooks','Rhythmic speech, harsh delivery or melodic chorus','Low-tuned guitar, bass, drums, optional turntable texture','Percussive guitars, punchy bass, focused vocal'),
'metalcore':TEMPLATES['modern-heavy'], 'grunge':TEMPLATES['grunge'],
'deep house':profile('Deep House','Warm, understated','Steady house pulse, syncopated bass, extended chords','Optional restrained soulful refrain','House drums, electric piano, bass, pads','Soft saturation, warm low end, restrained stereo ambience'),
'black metal':profile('Black Metal','Severe, atmospheric','Tremolo guitar motifs; driving blast passages; sustained harmonic tension','Harsh screamed lead','Distorted guitars, bass, rapid drums, optional atmospheric keys','Raw texture or clear atmospheric layers; preserve rhythmic articulation'),
'death metal':profile('Death Metal','Forceful, intense','Dense riff changes; palm-muted rhythmic accents; double-kick passages','Deep harsh or rasped lead','Distorted guitars, bass, fast drums','Articulate heavy guitars, separated kick, defined low end'),
}

def normalize(text):
    text=unicodedata.normalize('NFKD',str(text)).casefold()
    text=''.join(c for c in text if not unicodedata.combining(c))
    text=text.replace('&',' and ')
    text=re.sub(r'[^\w\s]',' ',text)
    return re.sub(r'\s+',' ',text).strip()

def identity_key(text):
    return re.sub(r'^the\s+','',normalize(text)).replace(' ','')

# Match descriptors, NEVER the artist's nationality or personal beliefs.
MATCHES={
'pop':r'\bpop\b|electropop|synthpop', 'rock':r'rock|grunge|post-punk',
'hip-hop':r'hip.hop|\brap\b|\btrap\b', 'rnb':r'r&b|\brnb\b|\bsoul\b',
'electronic':r'electronic|house|techno|trance|edm|dubstep|ambient|garage|idm',
'metal':r'metal|djent', 'doom':r'doom|sludge|drone|stoner', 'indie':r'indie|shoegaze',
'jazz':r'jazz|bebop', 'country':r'country|americana|honky', 'folk':r'folk|bluegrass',
'latin':r'latin|reggaeton|bachata|cumbia|salsa|dembow', 'corrido':r'corrido|regional mexican|mexican regional|norteno|norteño|ranchera',
'bollywood':r'bollywood|filmi|playback|indian film','punjabi':r'punjab|bhangra',
'indian-indie':r'indian indie|desi alt','italian':r'italian|sanremo|italo',
'kpop':r'k-pop|kpop','afrobeats':r'afrobeats|afropop|afro-fusion|afro-rave|amapiano',
'bedroom':r'bedroom|slacker|lo-fi|dream pop','modern-heavy':r'modern heavy|metalcore|post-hardcore|nu-metal|djent|deathcore',
'ccm':r'ccm|worship|gospel|christian pop|christian rock|christian hip',
'christian':r'christian metal|christian doom|unblack|white metal',
'hyperpop':r'hyperpop|digicore|bubblegum bass','reggae':r'reggae|\bdub\b|dancehall',
'dnb':r'drum and bass|drum & bass|\bdnb\b|jungle|neurofunk','techno':r'techno',
'house':r'house','blues':r'blues','punk':r'punk','grunge':r'grunge','classical':r'classical|orchestral|film score',
}

def categories_for(descriptor):
    return [k for k,v in MATCHES.items() if re.search(v,descriptor,re.I)]

def reference_profile(record,category=None):
    cats=record.get('categories') or ['pop']
    category=category if category in cats else cats[0]
    tags=record.get('matched_genres') or []
    exact=[t for t in tags if t.casefold() in SUBSTYLES and category in categories_for(t)]
    base=dict(SUBSTYLES[exact[0].casefold()] if exact else TEMPLATES[category])
    # A genre association is sourced. The rest is an editable original template.
    relevant=[t for t in tags if category in categories_for(t)]
    if relevant:base['genre']=', '.join(relevant[:3])
    return base
