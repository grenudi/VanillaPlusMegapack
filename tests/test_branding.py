"""The pack's name is display-only: prove nothing functional depends on it.

Pure Python (no game files, no LuaJIT), so it runs anywhere:  python tests/test_branding.py
"""
import ast
import json
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import branding  # noqa: E402
from package import package_release  # noqa: E402

# The identity contract. Changing either breaks every installed pack and the loader, which lists the module id
# in its own source (BingusSharedLoader src/shared_loader.lua). They are NOT names; see docs/IDENTITY.md.
MODULE = 'mods/cowboybingus/vanilla_plus_megapack'
GUID = '876060ae-0640-4ac5-95b6-ec7c9a0567d3'

# Code (not prose) must never spell the display name: it comes from branding.json.
CODE_FILES = ['scripts/build.py', 'scripts/package.py', 'scripts/archive.py', 'src/megapack.lua',
              'tests/test_package.py', 'tests/test_loader.lua', 'tests/test_duplicates.lua', 'tests/test_components.py']


def brand(name, stem, short='MH'):
    return {'name': name, 'short_name': short, 'artifact_stem': stem}


class Validation(unittest.TestCase):
    def test_current_branding_is_valid(self):
        b = branding.load(ROOT)
        self.assertTrue(b['name'] and b['artifact_stem'] and b['short_name'])

    def test_rejects_unsafe_values(self):
        for bad in ({'name': "It's"}, {'name': 'a"b'}, {'name': 'a\\b'}, {'name': 'a\nb'}, {'name': ''},
                    {'name': ' padded '}, {'name': 'x' * 65}, {'artifact_stem': 'has space'},
                    {'artifact_stem': 'paren(s)'}, {'artifact_stem': '.hidden'}, {'artifact_stem': 'a/b'},
                    {'short_name': 'x' * 17}):
            with self.assertRaises(ValueError, msg=bad):
                branding.validate({**brand('Name', 'Stem'), **bad})

    def test_accepts_ordinary_values(self):
        branding.validate(brand('Make Helldivers Great Again (MHGA)', 'MHGA'))
        branding.validate(brand('Another Name: Part 2', 'Another-Name_2.0'))


class IdentityModule(unittest.TestCase):
    def source(self):
        return (ROOT / 'src/megapack.lua').read_text(encoding='utf-8')

    def test_name_is_substituted_and_only_the_name(self):
        a = branding.render_identity(self.source(), brand('First Name', 'First'))
        b = branding.render_identity(self.source(), brand('Second Name', 'Second'))
        self.assertIn("name = 'First Name'", a)
        self.assertEqual(a.replace('First Name', '@'), b.replace('Second Name', '@'))
        self.assertNotIn(branding.PLACEHOLDER, a)

    def test_missing_or_duplicated_placeholder_is_an_error(self):
        with self.assertRaises(ValueError):
            branding.render_identity("name = 'hardcoded'", brand('A', 'A'))
        token = "'" + branding.PLACEHOLDER + "'"
        with self.assertRaises(ValueError):
            branding.render_identity(token + token, brand('A', 'A'))


class IdentityContract(unittest.TestCase):
    def constants(self):
        tree = ast.parse((ROOT / 'scripts/build.py').read_text(encoding='utf-8'))
        found = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                found[node.targets[0].id] = node.value
        return found

    def test_module_and_guid_are_pinned_plain_constants(self):
        found = self.constants()
        for key, expected in (('MODULE', MODULE), ('GUID', GUID)):
            self.assertIsInstance(found[key], ast.Constant, f'{key} must be a literal, not computed from anything')
            self.assertEqual(found[key].value, expected)

    def test_identity_is_not_computed_from_branding(self):
        found = self.constants()
        for key in ('MODULE', 'GUID', 'VERSION', 'REVISION'):
            names = {n.id for n in ast.walk(found[key]) if isinstance(n, ast.Name)}
            self.assertNotIn('BRANDING', names, f'{key} must not depend on the display name')

    def test_no_display_name_literals_in_code(self):
        current = branding.load(ROOT)
        names = [current['name'], current['short_name'], current['artifact_stem']] + \
                [p[k] for p in current.get('previous', []) for k in ('name', 'artifact_stem')]
        for rel in CODE_FILES:
            text = (ROOT / rel).read_text(encoding='utf-8')
            for literal in names:
                self.assertNotIn(literal, text, f'{rel} spells the display name {literal!r}; read branding.json')
            self.assertIsNone(re.search(r'Vanilla ?Plus ?Megapack|Vanilla-Plus-Megapack', text), rel)


class PackagingIndependence(unittest.TestCase):
    """Package the same build under two different brands: only names may differ."""

    def package(self, tmp, b, tag):
        root, build = Path(tmp) / tag, Path(tmp) / (tag + '-build')
        (root / 'build').mkdir(parents=True)
        build.mkdir()
        (root / 'INSTALL.txt').write_bytes(b'install text\n')
        payload = bytes(range(256)) * 4
        (root / 'build/payload.bin').write_bytes(payload)
        digest = __import__('hashlib').sha256(payload).hexdigest().upper()
        report = {
            'name': b['name'], 'artifact_stem': b['artifact_stem'], 'revision': 'megapack-v1', 'version': '1',
            'guid': GUID, 'description': 'd', 'game_exe_sha256': '0' * 64, 'game_dll_sha256': '1' * 64,
            'deployment_files': {'options/A/payload.bin': 'build/payload.bin'}, 'files': {'build/payload.bin': digest},
            'options': [{'Name': 'A', 'Description': 'd', 'Include': ['options/A']}],
        }
        release = package_release(root, build, report)
        return release, zipfile.ZipFile(release)

    def test_only_names_differ(self):
        with tempfile.TemporaryDirectory() as tmp:
            one, z1 = self.package(tmp, brand('Alpha Pack', 'Alpha'), 'one')
            two, z2 = self.package(tmp, brand('Omega Pack (v2)', 'Omega'), 'two')
            self.assertEqual((one.name, two.name), ('Alpha-v1.zip', 'Omega-v1.zip'))
            functional = {'manifest.json', 'options/A/payload.bin'}
            self.assertEqual(set(z1.namelist()) & functional, functional)
            self.assertEqual(sorted(set(z1.namelist()) - functional), ['Alpha-README.txt', 'Alpha-manifest.json'])
            self.assertEqual(sorted(set(z2.namelist()) - functional), ['Omega-README.txt', 'Omega-manifest.json'])
            self.assertEqual(z1.read('options/A/payload.bin'), z2.read('options/A/payload.bin'))
            self.assertEqual(z1.read('Alpha-README.txt'), z2.read('Omega-README.txt'))
            m1, m2 = json.loads(z1.read('manifest.json')), json.loads(z2.read('manifest.json'))
            self.assertEqual(m1['Guid'], m2['Guid'])
            self.assertEqual(m1['Options'], m2['Options'])
            self.assertEqual((m1['Name'], m2['Name']), ('Alpha Pack - v1', 'Omega Pack (v2) - v1'))
            p1, p2 = json.loads(z1.read('Alpha-manifest.json')), json.loads(z2.read('Omega-manifest.json'))
            for key in set(p1) | set(p2):
                if key in ('name', 'artifact_stem'):
                    continue
                if key == 'files':
                    self.assertEqual({k: v for k, v in p1[key].items() if k in functional},
                                     {k: v for k, v in p2[key].items() if k in functional})
                else:
                    self.assertEqual(p1.get(key), p2.get(key), key)


if __name__ == '__main__':
    unittest.main(verbosity=2)
