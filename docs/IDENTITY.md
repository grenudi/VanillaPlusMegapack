# Identity versus name

The pack has a **name** (what people read) and an **identity** (what software matches on). They are
separate on purpose, so renaming the pack never changes anything functional.

## Name: `branding.json`

The only place the display name lives. Nothing functional is derived from it.

| Field | Used for |
|---|---|
| `name` | the title in Arsenal / HD2MM, the identity module's `name` field, docs |
| `short_name` | prose ("the MHGA repository") |
| `artifact_stem` | file names only: `<stem>-vN.zip`, `<stem>-manifest.json`, `<stem>-README.txt` |
| `previous` | earlier brands, so docs that still use them can be rewritten |

Values are validated (`scripts/branding.py`): no quotes, backslashes or control characters in names, and a safe
file-name character set for the stem, so a name can never break a Lua literal, a JSON string or a file name.

**To rename:** move the current `name`/`short_name`/`artifact_stem` into `previous`, put the new values in,
run `python .github/scripts/rebrand.py` (rewrites the prose in README, INSTALL.txt and friends), and rebuild.
That is the whole procedure. `tests/test_branding.py` proves the build output differs only in those names.

## Identity: fixed contracts, never derived from a name

| Identifier | Value | Who depends on it |
|---|---|---|
| Module id | `mods/cowboybingus/vanilla_plus_megapack` | hashed into the game's resource id (`79e4f54aa542ec98`); listed in the Bingus Shared Loader's own source (`src/shared_loader.lua`); quoted in the loader log line users look for |
| GUID | `876060ae-0640-4ac5-95b6-ec7c9a0567d3` | what Arsenal / HD2MM key the pack on |
| Revision | `megapack-vN` | the identity module and provenance manifest |
| Component module ids | `mods/cowboybingus/<component>` | each component's resource id and the loader |

The module id still reads like the original name. **That is not a bug and must not be "fixed" by renaming it:**
changing it would orphan every installed pack and break the loader, which lists the string. It is an opaque
identifier that happens to look like a name; the build never computes it from one.

`tests/test_branding.py` enforces the separation: `MODULE` and `GUID` must be pinned plain constants, must not
reference `BRANDING`, code files must not spell any brand name, and packaging the same build under two different
brands may differ only in the name fields and file names.

## Why the module id is not changed to something opaque

Doing so is possible but is a breaking change with no functional benefit: it needs a coordinated loader release,
new resource ids, and every user to disable the old pack first. The separation above already gives the property
that matters, that a rename cannot affect anything functional.
