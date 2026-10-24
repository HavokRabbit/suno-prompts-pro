"""Tests for the catalogue layer: sources, dedupe, references, blending.

Run with:  .venv/Scripts/python.exe _test_catalog.py
The original _test_suite.py still guards behaviour compatibility; this file
guards the new data contract and the honesty rules that go with it.
"""
import json
import pathlib
import subprocess
import sys

import catalog as cat
import genre_profiles as gp
import suno_prompt_generator_pro as app

ROOT = pathlib.Path(__file__).resolve().parent
passed, failed = [], []


def check(name, condition, detail=""):
    if condition:
        print(f"  PASS - {name}")
        passed.append(name)
    else:
        print(f"  FAIL - {name} {detail}")
        failed.append(name)


print("=" * 70)
print("CATALOGUE TEST SUITE")
print("=" * 70)

# 1 - baseline profiles preserved
print("\n[1] Original detail profiles preserved")
baseline = json.loads((pathlib.Path("G:/Vespers/suno-prompts-pro-baseline/artists.json")).read_text(encoding="utf-8"))
profiles = cat.profiles()
all_names = set(cat.catalog())
alias_names = {a for d in cat.catalog().values() for a in (d.get("aliases") or [])}
present = [n for n in baseline if n in all_names or n in alias_names]
check("all 776 baseline identities preserved as entries or aliases",
      len(present) == len(baseline),
      f"(missing {[n for n in baseline if n not in present][:5]})")
identical = all(
    profiles[n][f] == baseline[n][f]
    for n in baseline if n in profiles for f in gp.FIELDS
)
check("profile field text unchanged", identical)

# 2 - schema
print("\n[2] Profile schema")
bad = [n for n, d in profiles.items() if not all(isinstance(d.get(f), str) and d[f].strip() for f in gp.FIELDS)]
check("every profile has six non-empty string fields", not bad, f"{bad[:3]}")

# 3 - dedupe
print("\n[3] Dedupe")
keys = {}
dupes = []
for name in cat.catalog():
    key = gp.identity_key(name)
    if key in keys:
        dupes.append((keys[key], name))
    keys[key] = name
check("no duplicate identities after normalisation", not dupes, f"{dupes[:3]}")

# 4 - references carry provenance
print("\n[4] Reference provenance")
refs = cat.references()
missing = [n for n, d in refs.items() if not d.get("source")]
check("every reference records a source", not missing, f"{missing[:3]}")
claims = [n for n, d in refs.items() if all(f in d for f in gp.FIELDS) and d.get("kind") == "reference"]
check("no reference pretends to be a detail profile", not claims, f"{claims[:3]}")

# 5 - reference prompt is complete and labelled
print("\n[5] Reference prompt")
sample = next((n for n, d in refs.items() if d.get("matched_genres")), None)
if sample:
    text = app.generate_prompt(sample)
    required = ["Genre:", "Style:", "Mood:", "Vocal Style:", "Instrumentation:", "Production:", "[Short Prompt]:"]
    check("reference prompt has every field", all(r in text for r in required))
    check("reference prompt is labelled as a reference", "Genre Reference" in text)
    check("reference prompt discloses its source", "Source:" in text)
    check("reference prompt does not claim an artist analysis", "verified artist profile" not in text.lower())
else:
    check("a reference with genre tags exists", False)

# 6 - fallback still complete
print("\n[6] Unknown name fallback")
LABELS = ["Genre:", "Style:", "Mood:", "Vocal Style:", "Instrumentation:", "Production:", "[Short Prompt]:"]
unknown = app.generate_prompt("Completely Unmade Band Name")
check("unknown name still returns a full prompt", all(lbl in unknown for lbl in LABELS),
      str([lbl for lbl in LABELS if lbl not in unknown]))
check("unknown name is disclosed", "not in database" in unknown)

# 7 - blending
print("\n[7] Blend")
blend_raw = app.generate_blend("candlemass", "portishead", "Dark", "Loss", "Slow", sanitize=False)
check("blend returns a full prompt", all(lbl in blend_raw for lbl in LABELS),
      str([lbl for lbl in LABELS if lbl not in blend_raw]))
check("blend names both sides", "candlemass" in blend_raw.lower() and "portishead" in blend_raw.lower())
blend_clean = app.generate_blend("candlemass", "portishead", "Dark", "Loss", "Slow", sanitize=True)
check("blend output is sanitized when asked",
      "candlemass" not in blend_clean.lower() and "portishead" not in blend_clean.lower())

# 8 - sanitizer removes the selected name
print("\n[8] Sanitizer")
clean, hits = app._sanitize_prompt("In the style of Candlemass and Black Sabbath", extra=("Candlemass",))
check("selected artist name is stripped", "Candlemass" not in clean and hits >= 2, f"hits={hits}")
leaked = [n for n in ("Queen", "Prince", "Tool", "Future") if not app._strippable(n)]
check("common single words stay out of the strip list", len(leaked) == 4)

# 9 - filtering + pagination helpers
print("\n[9] Catalogue filters")
everything = cat.entries()
check("unfiltered query returns the whole catalogue", len(everything) == len(cat.catalog()))
only_profiles = cat.entries(kind="profile")
check("kind filter returns only profiles", all(d.get("kind") == "profile" for _, d in only_profiles) and len(only_profiles) == len(profiles))
only_refs = cat.entries(kind="reference")
check("kind filter returns only references", all(d.get("kind") == "reference" for _, d in only_refs) and len(only_refs) == len(refs))
cats = cat.categories()
check("categories are non-empty", bool(cats) and all(cat.counts_by_genre()[c] > 0 for c in cats))
first = cats[0]
in_cat = cat.entries(category=first)
check(f"category filter works ({first})", in_cat and all(first in d.get("categories", []) for _, d in in_cat))
hits_q = cat.entries(query="candle")
check("text query narrows results", 0 < len(hits_q) < len(everything))
check("search_names finds a known artist", any("candlemass" in n.lower() for n in cat.search_names("candl")))

# 10 - metadata in step with the data
print("\n[10] Metadata integrity")
meta = cat.meta()
if meta:
    counts = cat.counts_by_genre()
    check("meta genre counts match live counts", meta.get("genre_counts") == counts,
          f"meta={len(meta.get('genre_counts', {}))} live={len(counts)}")
    check("meta totals match the file",
          meta.get("profiles") == len(profiles) and meta.get("references") == len(refs))
else:
    check("catalog_meta.json exists", False)

# 11 - every template key used by a category is real
print("\n[11] Template coverage")
missing_tpl = [c for c in cats if c not in gp.TEMPLATES]
check("every category has an original template", not missing_tpl, f"{missing_tpl}")

# 12 - delivered header animation
print("\n[12] Header animation artifact")
header = ROOT / "static" / "header.mp4"
if header.is_file():
    check("header.mp4 is present and non-trivial", header.stat().st_size > 50_000, f"{header.stat().st_size} bytes")
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-show_entries", "stream=width,height,codec_name",
             "-of", "default=noprint_wrappers=1", str(header)],
            capture_output=True, text=True, timeout=60,
        ).stdout.strip().replace("\n", " ")
        check("header.mp4 is a real video", "codec_name=h264" in out and "width=1200" in out, out)
    except FileNotFoundError:
        check("ffprobe available", False)
else:
    check("header.mp4 exists", False)

# 13 - app module surface used by the UI
print("\n[13] App surface")
for fn in ("find_singer", "detect_genre", "get_random_artist", "generate_prompt",
           "generate_blend", "resolve_profile", "blend_profiles", "_sanitize_prompt",
           "render_header", "main"):
    if not hasattr(app, fn):
        check(f"app exposes {fn}", False)
check("app exposes every required callable", all(hasattr(app, f) for f in (
    "find_singer", "detect_genre", "get_random_artist", "generate_prompt",
    "generate_blend", "resolve_profile", "blend_profiles", "_sanitize_prompt", "render_header", "main")))
check("page config call present in source", "set_page_config" in (ROOT / "suno_prompt_generator_pro.py").read_text(encoding="utf-8"))

print()
print("=" * 70)
print(f"SUMMARY: {len(passed)} passed, {len(failed)} failed")
if failed:
    print(f"FAILED: {failed}")
    sys.exit(1)
print("=" * 70)
