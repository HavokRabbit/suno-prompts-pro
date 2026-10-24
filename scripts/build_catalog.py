"""Merge the preserved detail profiles with sourced genre references.

Rules that keep the result honest:
  * A legacy detailed profile is never overwritten or reworded.
  * The same act spelled two ways collapses to one entry; the other spelling is
    kept as an alias so provenance is not lost.
  * Reference entries keep their source and matched genre tags.
  * Release/label/company rows are rejected: a genre statement is not enough if
    the record itself describes something that is not a musical act.
"""
import json
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from genre_profiles import GENRES, identity_key, categories_for  # noqa: E402

BASELINE = pathlib.Path('G:/Vespers/suno-prompts-pro-baseline')

REJECT = re.compile(
    r'\b(album|ep|single|mixtape|record label|label|festival|television|tv series|'
    r'film|movie|fictional|character|company|brand|magazine|website|video game|'
    r'song by|split|soundtrack)\b',
    re.I,
)


def load_legacy():
    return json.loads((BASELINE / 'artists.json').read_text(encoding='utf-8'))


def load_candidates():
    out = {}
    for path in sorted((ROOT / 'research' / 'candidates').glob('*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        key = data['category']
        for record in data['artists']:
            record = dict(record)
            record['categories'] = [key]
            out.setdefault(record['wikidata_id'], record)
    return out


def load_extras():
    out = {}
    for path in sorted((ROOT / 'research').glob('extra-*.json')):
        try:
            records = json.loads(path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            print(f'WARN unreadable {path.name}')
            continue
        if not isinstance(records, list):
            continue
        for record in records:
            if isinstance(record, dict) and record.get('name'):
                out.setdefault(record['name'].casefold(), record)
    return out


def main():
    legacy = load_legacy()
    candidates = load_candidates()
    extras = load_extras()

    artists = {}
    seen = {}
    aliases_collapsed = []

    for name, data in legacy.items():
        key = identity_key(name)
        entry = {**data, 'kind': 'profile', 'source': 'original catalogue'}
        detected = categories_for(entry.get('genre', ''))
        if detected:
            entry['categories'] = detected
        if key in seen:
            # Same act, different spelling. Keep one entry, record the other.
            keeper = artists[seen[key]]
            keeper.setdefault('aliases', [])
            if name not in keeper['aliases']:
                keeper['aliases'].append(name)
            aliases_collapsed.append((seen[key], name))
            continue
        seen[key] = name
        artists[name] = entry

    rejected = 0
    merged = 0
    for record in candidates.values():
        description = record.get('description') or ''
        if REJECT.search(description):
            rejected += 1
            continue
        key = identity_key(record['name'])
        if key in seen:
            existing = artists[seen[key]]
            existing['categories'] = list(dict.fromkeys(
                (existing.get('categories') or []) + record['categories']
            ))
            if existing.get('kind') == 'reference':
                existing['matched_genres'] = list(dict.fromkeys(
                    (existing.get('matched_genres') or []) + record['matched_genres']
                ))
            continue
        textual = categories_for(description)
        cats = list(dict.fromkeys(record['categories'] + [c for c in textual if c in GENRES]))
        seen[key] = record['name']
        artists[record['name']] = {
            'name': record['name'],
            'kind': 'reference',
            'categories': cats,
            'matched_genres': record['matched_genres'],
            'description': description,
            'wikidata_id': record.get('wikidata_id', ''),
            'musicbrainz_id': record.get('musicbrainz_id', ''),
            'sitelinks': record.get('sitelinks', 0),
            'source': 'wikidata (CC0)',
            'source_url': (f"https://www.wikidata.org/wiki/{record['wikidata_id']}"
                           if record.get('wikidata_id') else ''),
        }
        merged += 1

    added = 0
    skipped_extra = 0
    for record in extras.values():
        key = identity_key(record['name'])
        cat_key = record.get('category')
        if cat_key not in GENRES:
            skipped_extra += 1
            continue
        if key in seen:
            existing = artists[seen[key]]
            existing['categories'] = list(dict.fromkeys(
                (existing.get('categories') or []) + [cat_key]
            ))
            continue
        seen[key] = record['name']
        artists[record['name']] = {
            'name': record['name'],
            'kind': 'reference',
            'categories': [cat_key],
            'matched_genres': record.get('matched_genres') or [],
            'description': record.get('evidence', ''),
            'evidence': record.get('evidence', ''),
            'wikidata_id': '',
            'musicbrainz_id': '',
            'sitelinks': 0,
            'source': 'researched source',
            'source_url': record.get('source_url', ''),
        }
        added += 1

    counts = Counter()
    for entry in artists.values():
        for cat_key in entry.get('categories') or []:
            counts[cat_key] += 1

    out = ROOT / 'artists.json'
    out.write_text(json.dumps(artists, ensure_ascii=False, indent=1), encoding='utf-8')

    meta = {
        'total': len(artists),
        'profiles': sum(1 for x in artists.values() if x['kind'] == 'profile'),
        'references': sum(1 for x in artists.values() if x['kind'] == 'reference'),
        'rejected': rejected,
        'merged_candidates': merged,
        'research_added': added,
        'research_skipped': skipped_extra,
        'aliases_collapsed': aliases_collapsed,
        'genre_counts': dict(sorted(counts.items())),
        'genre_labels': {k: v[0] for k, v in GENRES.items()},
        'shelves': {k: v[1] for k, v in GENRES.items()},
        'sources': {
            'wikidata': 'structured artist and genre statements, CC0',
            'original catalogue': 'detail profiles preserved from the deployed app',
            'researched source': 'explicit per-record source_url',
        },
    }
    (ROOT / 'catalog_meta.json').write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

    print(json.dumps({k: meta[k] for k in
                      ('total', 'profiles', 'references', 'rejected',
                       'merged_candidates', 'research_added', 'research_skipped')}, indent=2))
    if aliases_collapsed:
        print('collapsed duplicate spellings:', aliases_collapsed)
    for cat_key in sorted(counts, key=lambda c: -counts[c]):
        print(f'  {cat_key:16s} {counts[cat_key]:5d}')


if __name__ == '__main__':
    main()
