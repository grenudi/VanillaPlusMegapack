"""The pack's human-facing name: one file (branding.json), display only.

Nothing functional is derived from it. Identity is separate and fixed (see docs/IDENTITY.md):
the module id and GUID in build.py are contracts with the loader and the mod managers and are
never computed from a name. Renaming the pack means editing branding.json and nothing else.

    name           shown in the mod manager, in the identity module's `name` field and in docs
    short_name     used in prose
    artifact_stem  file-name stem: <stem>-vN.zip, <stem>-manifest.json, <stem>-README.txt
    icon           (optional) the pack's box icon, a PNG under assets/; packaged as thumbnail.png
    previous       earlier brands, so .github/scripts/rebrand.py can rewrite docs that still use them
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = '@PACK_NAME@'
# The name goes inside a single-quoted Lua literal and a JSON string: no quotes, backslashes or control characters.
NAME = re.compile(r"[^\x00-\x1f\x7f'\"\\]{1,64}")
STEM = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,47}')
ICON = re.compile(r'assets/(?:[A-Za-z0-9_-][A-Za-z0-9._-]*/)*[A-Za-z0-9_-][A-Za-z0-9._-]*\.png')


def validate(branding):
    if not isinstance(branding, dict):
        raise ValueError('branding.json must be an object')
    for key, pattern in (('name', NAME), ('short_name', NAME), ('artifact_stem', STEM)):
        value = branding.get(key)
        if not isinstance(value, str) or not pattern.fullmatch(value) or value != value.strip():
            raise ValueError(f'branding.json: invalid {key}: {value!r}')
    icon = branding.get('icon')
    if icon is not None and (not isinstance(icon, str) or not ICON.fullmatch(icon) or '..' in icon):
        raise ValueError(f'branding.json: invalid icon: {icon!r}')
    if len(branding['short_name']) > 16:
        raise ValueError('branding.json: short_name is longer than 16 characters')
    for old in branding.get('previous', []):
        if not NAME.fullmatch(old.get('name', '')) or not STEM.fullmatch(old.get('artifact_stem', '')):
            raise ValueError(f'branding.json: invalid previous entry: {old!r}')
    return branding


def load(root=ROOT):
    return validate(json.loads((Path(root) / 'branding.json').read_text(encoding='utf-8')))


def render_identity(source, branding):
    """The identity module's source with its display name filled in (the only thing that varies)."""
    token = "'" + PLACEHOLDER + "'"
    if source.count(token) != 1:
        raise ValueError(f'src/megapack.lua must contain exactly one {token}')
    return source.replace(token, "'" + validate(branding)['name'] + "'")
