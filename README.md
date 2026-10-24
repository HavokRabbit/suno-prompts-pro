# Iron Vespers — Prompt Studio

A prompt workbench for songwriters who have words but do not play an instrument. Pick a
sound, shape it, copy a structured prompt into Suno.

**Live app:** https://ironvespers.streamlit.app/

---

## What it does

- **Build a prompt** from 15,778 artists across 32 genres: genre, style, mood, vocal
  style, instrumentation and production, plus a one-line short prompt.
- **Blend two artists** — the first sets the arc, the second supplies texture.
- **Search and filter** by shelf, genre, kind and free text, with pagination.
- **Save presets** in the session and export or import them as JSON.
- **Strip artist names** from generated prompts, because Suno rejects prompts containing
  real artist names.
- **Animated header** rendered from a HyperFrames composition.

## Two kinds of entry

The catalogue deliberately separates authored depth from derived reference:

| Kind | What it is | How many |
|---|---|---|
| **Detail profile** | Hand-written six-field sound description | 773 |
| **Genre reference** | A real artist with a verified genre association, rendered through an original genre template | 15,005 |

A genre reference is a **starting point, not an analysis**. The genre fact is sourced; the
sound description is original writing applied to that genre, and the user is expected to
edit it. No entry invents an artist-specific vocal or production description.

## Sources

- **Wikidata** — structured artist and genre statements, released **CC0**. Reference
  entries link to their `wikidata.org` record.
- **Researched entries** — each carries an explicit `source_url` and the evidence used.
- **Original catalogue** — the profiles that shipped with the app.

No review text, biography or lyrics are ingested. Generated prompts never contain artist
names, album titles or lyrics.

## Layout

```
suno_prompt_generator_pro.py   Streamlit entrypoint (the deployed file)
catalog.py                     catalogue loading, filtering, lookup
genre_profiles.py              original genre templates + genre matching
artists.json                   all entries (profiles + references)
catalog_meta.json              build report: counts, sources, collapsed aliases
templates.json                 fallback templates used by the original app
genre_rules.json               free-text genre detection rules
static/style.css               theme
static/header.mp4              rendered header animation (see motion/)
motion/header/                 HyperFrames source for the header
scripts/collect_catalog.py     Wikidata collector (cached, rebuildable)
scripts/build_catalog.py       merge + dedupe + report
research/candidates/           collected candidates per genre
research/extra-*.json          hand-researched additions with source URLs
_test_suite.py                 behaviour-compatibility tests (15)
_test_catalog.py               catalogue contract tests (31)
```

## Rebuild the catalogue

The app reads JSON offline and never calls the network at request time.

```bash
python scripts/collect_catalog.py          # Wikidata -> research/candidates (cached)
python scripts/build_catalog.py            # merge, dedupe, reject, report
```

The build prints real per-genre counts and keeps a reject count, so a filter that starts
eating good records is visible instead of silent.

## Tests

```bash
python _test_suite.py      # behaviour compatibility + live server check
python _test_catalog.py    # provenance, dedupe, references, filters, header artifact
```

`_test_catalog.py` regenerates the rollback manifest check against
`../suno-prompts-pro-baseline/` when that folder exists.

## Header animation

`motion/header/` is a HyperFrames project (GSAP timeline, seekable, 1200×280, 3.5s).

```bash
cd motion/header
npm install gsap@3.14.2 && cp node_modules/gsap/dist/gsap.min.js assets/gsap.min.js
hyperframes lint && hyperframes check
hyperframes render --quality looks --output ../../static/header.mp4
```

The embed is muted, decorative and marked `aria-hidden`. When the viewer asks for reduced
motion it parks on the final frame instead of looping.

## Local development

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt pytest
.venv/Scripts/python.exe -m streamlit run suno_prompt_generator_pro.py
```

Opens at http://localhost:8501

## Tech

- **Streamlit** web app, Python 3.11+
- No external API calls at runtime
- Fits the Streamlit Community Cloud free tier

## Limits worth knowing

- A genre association is not a sound. Two records in the same genre can share nothing.
- Coverage is uneven because documented data is uneven. Thin scenes report real counts
  instead of padding.
- Presets and history are session-only; the export file is the durable copy.

## License

MIT — use it, fork it, share it.

---

Built by David for the songwriters in the world.
