"""Catalog access for the preserved detail profiles and the sourced references.

SINGER_DB (artists.json) holds the original detailed profiles exactly as they
were. catalog_meta.json plus the same artists.json also carry genre references
collected from Wikidata (CC0) and from explicit researched sources. Both live in
one file so the app makes a single read; the difference is the `kind` field.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from genre_profiles import GENRES, identity_key, normalize

DATA_DIR = Path(__file__).resolve().parent
PROFILE_FIELDS = ('genre', 'mood', 'style', 'vocal_style', 'instruments', 'production')

SHELVES = ['Rock', 'Metal', 'Electronic', 'Pop', 'Hip-hop', 'R&B / soul', 'Jazz & roots',
           'Global scenes', 'Faith', 'Classical']


@lru_cache(maxsize=1)
def load():
    artists = json.loads((DATA_DIR / 'artists.json').read_text(encoding='utf-8'))
    meta_path = DATA_DIR / 'catalog_meta.json'
    meta = json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.is_file() else {}
    profiles = {}
    references = {}
    for name, data in artists.items():
        kind = data.get('kind')
        if kind is None:
            # Pre-merge files have no `kind`; a complete six-field entry is a
            # preserved detail profile, anything else is a sourced reference.
            kind = 'profile' if all(f in data for f in PROFILE_FIELDS) else 'reference'
            data['kind'] = kind
        if kind == 'profile':
            profiles[name] = data
        else:
            references[name] = data
    return artists, profiles, references, meta


def catalog():
    return load()[0]


def profiles():
    return load()[1]


def references():
    return load()[2]


def meta():
    return load()[3]


def genre_label(key):
    return GENRES.get(key, (key.replace('-', ' ').title(), ''))[0]


def genre_shelf(key):
    return GENRES.get(key, ('', 'Other'))[1]


def categories():
    """Every category that actually has members, ordered by size."""
    counts = counts_by_genre()
    return [k for k, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]


def counts_by_genre():
    counts = {}
    for entry in catalog().values():
        for cat in entry.get('categories') or []:
            counts[cat] = counts.get(cat, 0) + 1
    return counts


def entries(category=None, shelf=None, kind=None, query=''):
    """Filtered catalog rows. `query` matches name, description and genre text."""
    needle = normalize(query)
    cats = set(categories())
    rows = []
    for name, data in catalog().items():
        name_norm = normalize(name)
        if needle and needle not in name_norm and needle not in normalize(data.get('description', '')):
            if needle not in normalize(' '.join(data.get('matched_genres') or [])):
                if needle not in normalize(data.get('genre', '')):
                    continue
        entry_cats = [c for c in (data.get('categories') or []) if c in cats]
        if category and category != 'All' and category not in entry_cats:
            continue
        if shelf and shelf != 'All' and not any(genre_shelf(c) == shelf for c in entry_cats):
            continue
        if kind and kind != 'All' and data.get('kind') != kind:
            continue
        rows.append((name, data))
    preferred = {'profile': 0, 'reference': 1}
    rows.sort(key=lambda row: (preferred.get(row[1].get('kind'), 2), -int(row[1].get('sitelinks') or 0), row[0].casefold()))
    return rows


def find(name):
    """Exact-or-normalised lookup across profiles and references."""
    if not name:
        return None, None
    data = catalog()
    direct = data.get(name.strip().lower())
    if direct:
        return name.strip().lower(), direct
    key = identity_key(name)
    for candidate, entry in data.items():
        if identity_key(candidate) == key:
            return candidate, entry
    return None, None


def suggestions(limit=40):
    """Compact, broad-name suggestions for the searchable picker."""
    names = sorted(catalog(), key=str.casefold)
    return names[:limit]


def search_names(query, limit=60):
    needle = normalize(query)
    if not needle:
        return []
    starts, contains = [], []
    for name in catalog():
        norm = normalize(name)
        if norm.startswith(needle):
            starts.append(name)
        elif needle in norm:
            contains.append(name)
    return (starts + contains)[:limit]
