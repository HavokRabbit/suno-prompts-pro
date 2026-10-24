# Iron Vespers Prompt Studio — design

## Intent
Keep the existing Streamlit app and the wolf identity. Turn a long button wall into a useful music workbench: pick a sound, shape it, copy a clean prompt. Preserve the existing detailed profiles, random generation, manual controls, and text exports.

## Colors
- Canvas: `#111214` charcoal
- Panels: `#1B1D20` iron
- Text: `#F2EEE7` warm bone
- Secondary text: `#B9B4AE`
- Accent: `#D85463` muted crimson; original wolf mark keeps `#C8102E`
- Borders: `#383A3F`

## Typography
Georgia (display title), system sans-serif (controls and body), system monospace (prompts and counts). No external font request. HyperFrames declares local font fallbacks explicitly.

## Layout
Compact header, four clear sections: Studio, Artists, Saved, About. Top navigation replaces the repeated sidebar hero. Primary controls left, results right on wide screens; natural stack on phones. Catalog uses search + genre + profile type filters with pagination, never thousands of buttons.

## Motion
A short seekable HyperFrames/GSAP SVG line trace and wolf reveal in an embedded iframe. Runs once, then rests. Replay and pause are available inside the embed. Respect reduced-motion preferences and offer a static header. No sound, infinite loops, flashing, webgl, or video encoder on Streamlit Cloud. Streamlit remains the application framework.

## Data honesty
Display existing detailed profiles separately from sourced genre-based references. Genre references are original musical templates applied to verified Wikidata genre facts, not claimed artist-specific voice analyses. Use CC0 structured identities and source links. Deduplicate by stable ID and normalized names. Do not pad thin genres with unrelated musicians.

## Do not
- Replace the site framework or break its deployed entrypoint.
- Autoplay audio or run generation/render servers in the hosted app.
- Use rainbow/purple gradients, excessive emoji, or all-red buttons.
- Call a generic genre template a verified artist profile.
- Claim every category gained 100 unless the audit proves it.
- Claim presets survive a new browser session; export/import is the durable path.
