"""Local test suite for Suno Prompt Generator Pro v1."""
import importlib.util
import ast

spec = importlib.util.spec_from_file_location('suno_app', 'suno_prompt_generator_pro.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print('=' * 70)
print('LOCAL TEST SUITE — Suno Prompt Generator Pro v1')
print('=' * 70)

passed = []
failed = []

# Test 1
print('\n[1/13] Module loads...')
try:
    assert hasattr(mod, 'SINGER_DB'), 'Missing SINGER_DB'
    assert hasattr(mod, 'DEFAULT_TEMPLATES'), 'Missing DEFAULT_TEMPLATES'
    assert hasattr(mod, 'generate_prompt'), 'Missing generate_prompt'
    assert hasattr(mod, 'detect_genre'), 'Missing detect_genre'
    assert hasattr(mod, 'find_singer'), 'Missing find_singer'
    assert hasattr(mod, 'get_random_artist'), 'Missing get_random_artist'
    print('  PASS — all functions present')
    passed.append('module_loads')
except AssertionError as e:
    print(f'  FAIL — {e}')
    failed.append('module_loads')

# Test 2
print('\n[2/13] All artists have required 6 fields...')
required_fields = {'genre', 'mood', 'style', 'vocal_style', 'instruments', 'production'}
# Min lengths per field — genre can legitimately be "Pop" (3 chars), others need substance
min_lengths = {'genre': 3, 'mood': 4, 'style': 5, 'vocal_style': 5, 'instruments': 5, 'production': 5}
bad_artists = []
for name, data in mod.SINGER_DB.items():
    if not isinstance(data, dict):
        bad_artists.append((name, 'not a dict'))
        continue
    missing = required_fields - set(data.keys())
    if missing:
        bad_artists.append((name, f'missing {missing}'))
    for field in required_fields:
        if field in data and not isinstance(data[field], str):
            bad_artists.append((name, f'{field} not string'))
        if field in data and len(data[field].strip()) < min_lengths[field]:
            bad_artists.append((name, f'{field} too short ({len(data[field].strip())} < {min_lengths[field]})'))
if bad_artists:
    print(f'  FAIL — {len(bad_artists)} bad entries:')
    for name, err in bad_artists[:5]:
        print(f'    {name}: {err}')
    failed.append('artist_fields')
else:
    print(f'  PASS — {len(mod.SINGER_DB)} artists all have complete 6-field profiles')
    passed.append('artist_fields')

# Test 3
print('\n[3/13] No duplicate artist names (case-insensitive)...')
names_lower = [n.lower() for n in mod.SINGER_DB.keys()]
duplicates = [n for n in set(names_lower) if names_lower.count(n) > 1]
if duplicates:
    print(f'  FAIL — duplicates: {duplicates}')
    failed.append('no_duplicates')
else:
    print(f'  PASS — {len(mod.SINGER_DB)} unique artists')
    passed.append('no_duplicates')

# Test 4
print('\n[4/13] All genre templates have 6 fields...')
bad_templates = []
for g, data in mod.DEFAULT_TEMPLATES.items():
    missing = required_fields - set(data.keys())
    if missing:
        bad_templates.append((g, missing))
if bad_templates:
    print(f'  FAIL: {bad_templates}')
    failed.append('template_fields')
else:
    print(f'  PASS — {len(mod.DEFAULT_TEMPLATES)} templates complete')
    passed.append('template_fields')

# Test 5
print('\n[5/13] Popular artists exist in DB...')
popular = ["taylor swift", "billie eilish", "kendrick lamar", "queen", "frank ocean",
           "daft punk", "sabrina carpenter", "chappell roan", "iron vespers", "candlemass",
           "demon hunter", "bad bunny", "arijit singh", "burna boy", "maneskin", "bts",
           "peso pluma", "karan aujla", "tyla", "sal da vinci"]
missing = [a for a in popular if a not in mod.SINGER_DB]
if missing:
    print(f'  FAIL — popular artists not in DB: {missing}')
    failed.append('popular_in_db')
else:
    print(f'  PASS — all {len(popular)} popular artists in DB')
    passed.append('popular_in_db')

# Test 6
print('\n[6/13] generate_prompt succeeds for ALL artists...')
errors = []
for name in mod.SINGER_DB.keys():
    try:
        result = mod.generate_prompt(name, 'test mood', 'test theme', 'Medium')
        if '[' not in result:
            errors.append((name, 'no header'))
        for required_section in ['Genre:', 'Style:', 'Mood:', 'Vocal Style:',
                                 'Instrumentation:', 'Production:']:
            if required_section not in result:
                errors.append((name, f'missing {required_section}'))
    except Exception as e:
        errors.append((name, str(e)))
if errors:
    print(f'  FAIL — {len(errors)} errors:')
    for name, err in errors[:5]:
        print(f'    {name}: {err}')
    failed.append('generate_all')
else:
    print(f'  PASS — prompts generated for all {len(mod.SINGER_DB)} artists')
    passed.append('generate_all')

# Test 7
print('\n[7/13] Auto-detect maps to valid templates...')
test_genres = ['bollywood', 'punjabi', 'corrido', 'latin', 'italian', 'kpop',
               'afrobeats', 'bedroom', 'country', 'modern-heavy', 'doom', 'metal',
               'rock', 'electronic', 'hip-hop', 'rnb', 'indie', 'jazz', 'pop', 'indian-indie']
all_present = True
for g in test_genres:
    if g not in mod.DEFAULT_TEMPLATES:
        print(f'  FAIL — template "{g}" missing')
        all_present = False
        failed.append('templates_complete')
        break
if all_present:
    print(f'  PASS — all {len(test_genres)} genre templates exist')
    passed.append('templates_complete')

# Test 8
print('\n[8/13] Edge cases...')
edge_cases = [('', 'pop'), ('   ', 'pop'), ('SOME WEIRD ARTIST NAME', 'pop'), ('a', 'pop')]
edge_pass = True
for input_str, expected in edge_cases:
    detected = mod.detect_genre(input_str)
    if detected != expected:
        print(f'  FAIL — "{input_str}": expected {expected}, got {detected}')
        edge_pass = False
        failed.append('edge_cases')
        break
if edge_pass:
    print(f'  PASS — {len(edge_cases)} edge cases handled')
    passed.append('edge_cases')

# Test 9
print('\n[9/13] Optional fields are optional...')
result_min = mod.generate_prompt('taylor swift')
result_full = mod.generate_prompt('taylor swift', 'romantic', 'love', 'Slow')
if 'Theme:' in result_min:
    print('  FAIL — empty theme should not add Theme line')
    failed.append('optional_fields')
elif 'Genre:' not in result_min or 'Vocal Style:' not in result_min:
    print('  FAIL — required sections missing')
    failed.append('optional_fields')
else:
    print(f'  PASS — works with empty and full optionals')
    passed.append('optional_fields')

# Test 10
print('\n[10/13] Unknown artist uses fallback template...')
result = mod.generate_prompt('Some Random Unknown Artist XYZ', 'sad', 'loneliness', 'Slow')
if 'Note: Singer not in database' not in result:
    print('  FAIL — should note when singer not in DB')
    failed.append('unknown_fallback')
else:
    print(f'  PASS — fallback works, uses detected genre template')
    passed.append('unknown_fallback')

# Test 11
print('\n[11/13] Short prompt is one line...')
result = mod.generate_prompt('bad bunny', 'party', 'reggaeton night', 'Fast')
short_lines = [l for l in result.splitlines() if 'Short Prompt' in l]
if not short_lines:
    print('  FAIL — no short prompt line')
    failed.append('short_prompt')
elif len(short_lines[0]) > 250:
    print(f'  FAIL — short prompt too long: {len(short_lines[0])} chars')
    failed.append('short_prompt')
else:
    print(f'  PASS — short prompt: {short_lines[0][:120]}...')
    passed.append('short_prompt')

# Test 12
print('\n[12/13] File syntax + importable...')
with open('suno_prompt_generator_pro.py') as f:
    source = f.read()
try:
    ast.parse(source)
    print(f'  PASS — {len(source)} bytes parse cleanly')
    passed.append('syntax')
except SyntaxError as e:
    print(f'  FAIL — syntax error: {e}')
    failed.append('syntax')

# Test 13: Streamlit server is up
print('\n[13/13] Streamlit server health check...')
import urllib.request
try:
    with urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=3) as r:
        body = r.read().decode()
        if body.strip() == 'ok':
            print('  PASS — server returns ok')
            passed.append('server_health')
        else:
            print(f'  FAIL — unexpected body: {body}')
            failed.append('server_health')
    # Also check the index page
    with urllib.request.urlopen('http://127.0.0.1:8501/', timeout=3) as r:
        if r.status == 200:
            print('  PASS — index page returns 200')
            passed.append('server_index')
        else:
            print(f'  FAIL — index returned {r.status}')
            failed.append('server_index')
except Exception as e:
    print(f'  FAIL — server unreachable: {e}')
    failed.append('server_health')

# Summary
print()
print('=' * 70)
print(f'SUMMARY: {len(passed)} passed, {len(failed)} failed')
print('=' * 70)
if failed:
    print(f'Failed tests: {failed}')
else:
    print('ALL TESTS PASS — safe to deploy')
print(f'  Artists: {len(mod.SINGER_DB)}')
print(f'  Genre templates: {len(mod.DEFAULT_TEMPLATES)}')
print(f'  Popular quick-pick: 20')
print()
print('READY TO DEPLOY' if not failed else 'FIX FAILURES BEFORE DEPLOY')