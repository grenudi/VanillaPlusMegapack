#!/usr/bin/env python3
"""Apply the MHGA (Make Helldivers Great Again) branding to upstream-owned files.

Why a script and not a one-off find-and-replace: this fork follows
CowboyBingus/VanillaPlusMegapack. Upstream keeps editing README.md and friends, so
hand-edited copies would conflict on every sync. Instead the branding is a small
set of deterministic, idempotent rules; the sync (upstream-sync.yml ->
sync_merge.sh) takes upstream's version of any of these files on conflict and
re-runs this script.

What is renamed: user-facing prose (README title/banner/alt text, INSTALL.txt title
line, TRANSLATING.md, one art-script docstring).

What is deliberately NOT renamed (it is protocol or pinned bytes, not branding):
  - `mods/cowboybingus/vanilla_plus_megapack` (module id the loader/game resolve),
    the manifest `slug`/`name`, `src/megapack.lua` identity and the tests asserting them
  - package file names (`Vanilla-Plus-Megapack-vN.zip`, `...-manifest.json`): upstream's builds
  - everything under components/ (hash-pinned by components.lock.json) and the
    root scripts/ that mirror them
  - URLs and credits that point at upstream's real repository
  - thumbnail.png (re-rendering needs the Windows fonts the original used)

    python rebrand.py           apply
    python rebrand.py --check   exit 1 if anything would change (writes nothing)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME = "Make Helldivers Great Again (MHGA)"
UPSTREAM_URL = "https://github.com/CowboyBingus/VanillaPlusMegapack"

RULES = {
    "README.md": [
        (r"!\[Vanilla Plus Megapack\]\(assets/banner\.png\)", f"![{NAME}](assets/mhga/banner.png)"),
        (r"(?m)^# Vanilla Plus Megapack$", f"# {NAME}"),
    ],
    "INSTALL.txt": [
        (r"\AVanilla Plus Megapack( - v[\d.]+)", NAME + r"\1"),
    ],
    "TRANSLATING.md": [
        (r"The Vanilla Plus Megapack repository", "The MHGA repository"),
    ],
    "assets/source/covers.py": [
        (r"for the Vanilla Plus Megapack options", "for the MHGA options"),
    ],
}

NOTE_START, NOTE_END = "<!-- mhga-note:start -->", "<!-- mhga-note:end -->"
NOTE = f"""{NOTE_START}
> **MHGA** is an unofficial fork of [Vanilla Plus Megapack]({UPSTREAM_URL}) by CowboyBingus ([Zero-Clause BSD](LICENSE)). It follows upstream daily and adds semantic-versioned releases, CI and an optional AI-assisted review of each release.
>
> Built packages are upstream's: download `Vanilla-Plus-Megapack-vN.zip` from [upstream's releases]({UPSTREAM_URL}/releases/latest). Package file names and the in-game module id (`mods/cowboybingus/vanilla_plus_megapack`) keep the upstream name on purpose, so the loader, mod managers and the game's resource names keep working.
{NOTE_END}"""


def apply_note(text):
    if NOTE_START in text and NOTE_END in text:
        return re.sub(re.escape(NOTE_START) + r".*?" + re.escape(NOTE_END), lambda _: NOTE, text, count=1, flags=re.S)
    title = re.search(rf"(?m)^# {re.escape(NAME)}$", text)
    if not title:
        return text
    return text[: title.end()] + "\n\n" + NOTE + text[title.end():]


def main():
    check = "--check" in sys.argv
    changed = []
    for rel, rules in RULES.items():
        path = ROOT / rel
        if not path.is_file():
            print(f"skip (missing): {rel}")
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        new = text
        for pattern, repl in rules:
            new = re.sub(pattern, repl, new)
        if rel == "README.md":
            new = apply_note(new)
        if new != text:
            changed.append(rel)
            if not check:
                path.write_bytes(new.encode("utf-8"))
    for rel in changed:
        print(("would change: " if check else "rebranded: ") + rel)
    if not changed:
        print("branding already applied")
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
