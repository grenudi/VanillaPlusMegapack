#!/usr/bin/env python3
"""Compile every vendored component with the pinned LuaJIT and require the result to equal, byte for byte, the
resource pinned in components.lock.json (the same check scripts/build.py makes). Also pins the identity module's
resource id. Needs no game files and runs on Linux:

    HD2_LUAJIT=/path/to/luajit python3 .github/scripts/verify_components.py

LuaJIT must be the commit in dependencies.json built NON-GC64 (Windows: `msvcbuild.bat nogc64`; Linux:
`make XCFLAGS=-DLUAJIT_DISABLE_GC64`); a GC64 build produces different bytecode and fails every component.
"""
import importlib
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IDENTITY_RESOURCE_ID = '79e4f54aa542ec98'      # resource_hash(MODULE): a contract with the loader and the game

if not os.environ.get('HD2_LUAJIT'):
    sys.exit('Set HD2_LUAJIT to the pinned, non-GC64 luajit executable')
os.environ.setdefault('ProgramFiles(x86)', tempfile.gettempdir())   # archive.py reads it eagerly; nothing is read from it
sys.path.insert(0, str(ROOT / 'scripts'))
sys.dont_write_bytecode = True
build = importlib.import_module('build')

failures = []
components = build.load_components()
for component in components:
    try:
        build.build_component(component, Path(tempfile.mkdtemp()))
    except Exception as error:   # noqa: BLE001 - report every component, not just the first
        failures.append(f"{component['slug']}: {str(error)[:200]}")
print(f'{len(components) - len(failures)}/{len(components)} components match their pinned resources')

actual = f'{build.resource_hash(build.MODULE):016x}'
if actual != IDENTITY_RESOURCE_ID:
    failures.append(f'identity module resource id is {actual}, expected {IDENTITY_RESOURCE_ID}')
identity = build.compile_resource(
    build.render_identity((ROOT / 'src/megapack.lua').read_text(encoding='utf-8'), build.BRANDING), Path(tempfile.mkdtemp()))
if build.BRANDING['name'].encode() not in identity:
    failures.append('identity resource does not carry the display name from branding.json')
print(f'identity module compiles; resource id {actual}')

for line in failures:
    print('FAIL', line)
sys.exit(1 if failures else 0)
