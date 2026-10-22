#!/usr/bin/env python3
"""Apply the pack's branding (branding.json) to upstream-owned prose and docstrings.

Why a script and not a one-off find-and-replace: this fork follows CowboyBingus/VanillaPlusMegapack. Upstream
keeps editing README.md and friends in its own brand, so hand-edited copies would conflict on every sync. The
rules below are deterministic and idempotent; the sync (sync_merge.sh) takes upstream's version of any file
listed here on conflict and re-runs this script.

The name comes from branding.json; `previous` lists earlier brands (upstream's original first), so the same
rules also work for a future rename. Only prose is rewritten. Identity (module id, GUID, resource names) is
never touched; see docs/IDENTITY.md.

Vendored components/ files are pinned by components.lock.json. Only Python build scripts' docstrings are edited
there, and the lock's source hashes for exactly those files are recomputed afterwards (`sync_lock`).

NEVER edit a component's Lua source (components/*/src/*): for plaintext ("direct") components the source text,
comments included, IS the shipped resource, so even a comment change alters the package and fails the build's
byte-for-byte check against the pinned standalone release. tests/test_branding.py enforces this.

    python rebrand.py            apply
    python rebrand.py --check    exit 1 if anything would change (writes nothing)
    python rebrand.py --list     print every file this script may modify
"""
import glob
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import branding  # noqa: E402

B = branding.load(ROOT)
NAME, SHORT, STEM = B['name'], B['short_name'], B['artifact_stem']
UPSTREAM_URL = 'https://github.com/CowboyBingus/VanillaPlusMegapack'
PREVIOUS = [p for p in B.get('previous', []) if p['name'] != NAME]
OLD_NAMES = [p['name'] for p in PREVIOUS]
OLD_SHORTS = [p['short_name'] for p in PREVIOUS if p.get('short_name') and p['short_name'] != SHORT]
OLD_STEMS = [p['artifact_stem'] for p in PREVIOUS if p['artifact_stem'] != STEM]


def alt(values):
    return '(?:' + '|'.join(re.escape(v) for v in sorted(values, key=len, reverse=True)) + ')'


NAMES, ANY = alt(OLD_NAMES), alt(OLD_NAMES + OLD_SHORTS)
STEMS = alt(OLD_STEMS)


def split_name_rules():
    """Names that a docstring wraps across a line ("The Vanilla Plus\\nMegapack repository's ...")."""
    rules = []
    for old in OLD_NAMES + OLD_SHORTS:
        words = old.split(' ')
        if len(words) > 1:
            rules.append((rf"The {re.escape(' '.join(words[:-1]))}\r?\n{re.escape(words[-1])} repository's",
                          f"The {SHORT}\nrepository's"))
    return rules


ZIP = (rf'{STEMS}-v(\d+)\.zip', rf'{STEM}-v\1.zip')   # `<stem>-v42.zip`; not `-Rows` and not the `vN` placeholder
RULES = [
    ('README.md', [
        (rf'!\[{ANY}\]\(assets/(?:mhga/)?banner\.png\)', f'![{NAME}](assets/mhga/banner.png)'),
        (rf'(?m)^# {ANY}$', f'# {NAME}'),
        ZIP,
    ]),
    ('INSTALL.txt', [(rf'\A{ANY}( - v[\d.]+)', NAME + r'\1'), ZIP]),
    ('CONTRIBUTING.md', [ZIP]),
    ('TRANSLATING.md', [(rf'The {ANY} repository', f'The {SHORT} repository')]),
    ('assets/source/covers.py', [(rf'for the {ANY} options', f'for the {SHORT} options')]),
    # Vendored, lock-pinned: comments and docstrings only.
    ('scripts/translations.py', None),
    ('components/*/scripts/translations.py', None),
    ('components/*/scripts/entry.py', [(rf'the {ANY} build', f'the {SHORT} build')]),
]
TRANSLATIONS = [*split_name_rules(), (rf"the {ANY}'s components", f"the {SHORT} pack's components")]

NOTE_START, NOTE_END = '<!-- mhga-note:start -->', '<!-- mhga-note:end -->'
NOTE = f"""{NOTE_START}
> **{SHORT}** is an unofficial fork of [Vanilla Plus Megapack]({UPSTREAM_URL}) by CowboyBingus ([Zero-Clause BSD](LICENSE)). It follows upstream daily and adds semantic-versioned releases, CI and an optional AI-assisted review of each release.
>
> This repository builds `{STEM}-vN.zip`. Nothing is published from it yet, so until then upstream's [`Vanilla-Plus-Megapack-vN.zip`]({UPSTREAM_URL}/releases/latest) carries the same mods. The display name lives in [`branding.json`](branding.json) and is not part of the package's identity: the module id (`mods/cowboybingus/vanilla_plus_megapack`) and GUID are fixed contracts with the loader and mod managers ([docs/IDENTITY.md](docs/IDENTITY.md)).
{NOTE_END}"""


def owned_files():
    out = []
    for pattern, _ in RULES:
        out += sorted(Path(p).relative_to(ROOT).as_posix() for p in glob.glob(str(ROOT / pattern)))
    return out


def rules_for(rel):
    for pattern, rules in RULES:
        if rel in glob.glob(str(ROOT / pattern)) or (ROOT / rel).as_posix() in glob.glob(str(ROOT / pattern)):
            return TRANSLATIONS if rules is None else rules
    return []


def apply_note(text):
    if NOTE_START in text and NOTE_END in text:
        return re.sub(re.escape(NOTE_START) + r'.*?' + re.escape(NOTE_END), lambda _: NOTE, text, count=1, flags=re.S)
    title = re.search(rf'(?m)^# {re.escape(NAME)}$', text)
    return text if not title else text[: title.end()] + '\n\n' + NOTE + text[title.end():]


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def sync_lock(apply):
    """Pin the lock's source hash for each owned component file to the file's current bytes."""
    path = ROOT / 'components.lock.json'
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding='utf-8'))
    owned, updated = set(owned_files()), []
    for entry in data:
        for rel, old in entry['source_sha256'].items():
            target = f"components/{entry['slug']}/{rel}"
            if target in owned and (ROOT / target).is_file():
                new = sha((ROOT / target).read_bytes())
                if new != old:
                    entry['source_sha256'][rel] = new
                    updated.append(target)
    if updated and apply:
        path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    return updated


def main():
    if '--list' in sys.argv:
        print('\n'.join(owned_files() + ['components.lock.json']))
        return 0
    check = '--check' in sys.argv
    changed = []
    for rel in owned_files():
        path = ROOT / rel
        text = path.read_bytes().decode('utf-8')
        new = text
        for pattern, repl in rules_for(rel):
            new = re.sub(pattern, repl, new)
        if rel == 'README.md':
            new = apply_note(new)
        if new != text:
            changed.append(rel)
            if not check:
                path.write_bytes(new.encode('utf-8'))
    locked = sync_lock(apply=not check)
    for rel in changed:
        print(('would change: ' if check else 'rebranded: ') + rel)
    for rel in locked:
        print(('would re-pin: ' if check else 're-pinned in components.lock.json: ') + rel)
    if not changed and not locked:
        print('branding already applied')
    return 1 if (check and (changed or locked)) else 0


if __name__ == '__main__':
    sys.exit(main())
