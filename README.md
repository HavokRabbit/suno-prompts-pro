# 🎵 Suno Prompt Generator Pro

A free tool for **lyricists who don't produce music** to generate detailed Suno AI music prompts.

**Live app:** *(add URL after deploy)*

---

## What it does

- **Pick an artist style** → generates a structured Suno prompt with genre, mood, vocal style, instrumentation, and production notes
- **Customize** mood / theme / tempo
- **Copy or download** as `.txt` and paste into Suno
- **136 artists** across 21 genres — Pop, Rock, Hip-Hop, R&B, Electronic, Metal, Doom, Indie, Bedroom, Country, Latin, Corridos Tumbados, Reggaeton, K-Pop, Bollywood, Punjabi, Indian Indie, Italian, Afrobeats, Hyperpop, Modern Heavy, CCM
- **Random generator** for when you don't know what you want
- **Search artists** by genre

## Built for

- Songwriters who have lyrics but don't play instruments
- People who want to hear their words in a specific style/vibe
- Anyone using Suno AI to make music

## How to use

1. Pick an artist (Popular list, Artists tab, or type a name)
2. Optionally add mood / theme / tempo
3. Click Generate
4. Copy prompt and paste into Suno
5. Create!

## Tech

- **Streamlit** web app
- **Python 3.11+**
- Zero external APIs (runs entirely offline once deployed)
- 1GB RAM (well within Streamlit Community Cloud free tier)

## Local development

```bash
pip install -r requirements.txt
streamlit run suno_prompt_generator_pro.py
```

Opens at http://localhost:8501

## License

MIT — use it, fork it, share it.

---

Built by David for the songwriters in the world.