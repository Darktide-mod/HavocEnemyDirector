"""Build one independent Nexus ZIP and three submission documents.

Internal configuration and validation stay in publishing/ and build/.
"""
from pathlib import Path, PurePosixPath
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import strip_debug as diagnostics

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'publishing'
STAGING = ROOT / 'src'
RELEASE = ROOT / 'release'
CHECKS = ROOT / 'build/checks'
PACKAGE_EXTENSIONS = {'.lua', '.mod', '.json', '.md', '.txt'}
VERSION = r'[0-9]+\.[0-9]+\.[0-9]+(?:-(?:test|experimental)\.[0-9]+)?'
FORBIDDEN_COPY = re.compile(r'\bbundle\b|整合包|整合安装|整合安裝|SoloPlayMoreHavoc|Will of the Emperor', re.I)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def bbcode(markdown):
    lines, in_list = [], False
    for line in markdown.splitlines():
        if line.startswith('- '):
            if not in_list:
                lines.append('[list]')
                in_list = True
            lines.append('[*]' + line[2:])
            continue
        if in_list:
            lines.append('[/list]')
            in_list = False
        if line.startswith('## '):
            line = '[size=4][b]' + line[3:] + '[/b][/size]'
        elif line.startswith('# '):
            line = '[size=5][b]' + line[2:] + '[/b][/size]'
        lines.append(line)
    if in_list:
        lines.append('[/list]')
    return '\n'.join(lines).strip() + '\n'


def collect_sources(strip_debug=False):
    config = read_json(SOURCE / 'release.json')
    name = config['mod']
    assert name == ROOT.name and re.fullmatch(r'[A-Za-z0-9]+', name)
    info = read_json(STAGING / name / 'info.json')
    version = info['version']
    assert re.fullmatch(VERSION, version), 'Invalid mod version.'
    assert re.fullmatch(re.escape(version) + r'(?:-r[0-9]+)?', config['release_id']), 'Use the mod version, optionally followed by -rN for publishing-only changes.'
    assert read_json(SOURCE / 'metadata.json')['version'] == version, 'Code and publishing versions differ.'
    category = config.get('file_category', 'Main Files')
    assert category in ('Main Files', 'Optional Files')
    strip_debug = strip_debug or category == 'Main Files'
    if '-test.' in version:
        assert category == 'Optional Files', 'Temporary diagnostic builds belong in Optional Files.'

    descriptions = []
    for lang in ('en', 'zh-CN'):
        body = diagnostics.document((SOURCE / f'description.{lang}.md').read_text(encoding='utf-8-sig'),strip_debug).strip()
        assert body and not FORBIDDEN_COPY.search(body)
        assert not re.search(VERSION, body), 'Keep version numbers in changelog.en.txt, not description.'
        assert not re.search(r'^#+\s+.*(?:\b(?:changelog|release|update|validation)\b|更新|变更|版本|发布|验证)', body, re.I | re.M), 'Description must contain features, not release notes.'
        assert 'SoloPlay' in body and 'Realms' in body
        assert 'Vortex' in body and 'mods/' + name in body
        assert ('Manual installation' if lang == 'en' else '手动安装') in body
        if lang == 'en':
            assert not re.search(r'[\u3400-\u9fff]', body), 'English description contains Chinese text.'
        descriptions.append(bbcode(body))
    documents = {
        'description.bbcode.txt': '[size=5][b]English[/b][/size]\n\n' + descriptions[0]
            + '\n[size=5][b]简体中文[/b][/size]\n\n' + descriptions[1],
        'summary.en.txt': (SOURCE / 'summary.en.txt').read_text(encoding='utf-8-sig').strip() + '\n',
        'changelog.en.txt': (SOURCE / 'changelog.en.txt').read_text(encoding='utf-8-sig').strip() + '\n',
    }
    summary = documents['summary.en.txt'].strip()
    assert summary and len(summary) <= 350 and 'SoloPlay' in summary and 'Realms' in summary
    for filename in ('summary.en.txt', 'changelog.en.txt'):
        body = documents[filename]
        assert body.strip() and not re.search(r'[\u3400-\u9fff]', body), filename + ' must be English.'
        assert not FORBIDDEN_COPY.search(body)
    assert not re.search(VERSION, summary), 'Keep the summary focused on features.'
    for tag in ('b', 'size', 'list'):
        body = documents['description.bbcode.txt']
        assert len(re.findall(r'\[' + tag + r'(?:=[^\]]*)?\]', body)) == body.count('[/' + tag + ']')

    payloads = {}
    for source in sorted((STAGING / name).rglob('*')):
        if not source.is_file():
            continue
        assert source.suffix.lower() in PACKAGE_EXTENSIONS, source
        data = source.read_bytes()
        assert not zipfile.is_zipfile(io.BytesIO(data)) and not data.startswith((b'7z\xbc\xaf\x27\x1c', b'Rar!')), source
        payloads[source.relative_to(STAGING).as_posix()] = data
    for required in (name + '/' + name + '.mod', f'{name}/scripts/mods/{name}/{name}.lua', name + '/info.json'):
        assert required in payloads, required
    payloads = diagnostics.payloads(payloads,strip_debug)
    if strip_debug:
        if category == 'Optional Files':
            config['release_id'] = config.get('stripped_release_id',version + '-r2')
            assert re.fullmatch(re.escape(version) + r'-r[0-9]+',config['release_id'])
        config['diagnostics_stripped'] = True
        if category == 'Optional Files':
            documents['changelog.en.txt'] = 'Packaging variant: performance diagnostics removed; test status and gameplay fixes are unchanged.\n\n' + documents['changelog.en.txt']
    return config, version, documents, payloads


def vortex_check(name, payloads):
    node = shutil.which('node')
    plugins = Path(os.environ.get('APPDATA', '')) / 'Vortex/plugins'
    candidates = [p for p in plugins.glob('*/index.js') if 'warhammer40kdarktide' in p.read_text(encoding='utf-8', errors='replace')]
    if not node or not candidates:
        return {'status': 'unavailable', 'detail': 'Vortex extension or Node not found; static layout checks still apply.'}
    extension = max(candidates, key=lambda p: p.stat().st_mtime)
    run = subprocess.run([node, str(ROOT / 'tools/release_vortex_check.cjs'), str(extension)],
        input=json.dumps([{'name': name, 'files': list(payloads)}]), text=True,
        capture_output=True, encoding='utf-8', check=True)
    return json.loads(run.stdout)


def validate(batch, config, version, documents, payloads):
    name = config['mod']
    archive = batch / f'{name}-{version}.zip'
    assert {p.name for p in batch.iterdir()} == set(documents) | {archive.name}, 'Release must contain exactly one ZIP and three documents.'
    assert all(p.is_file() for p in batch.iterdir()), 'No release subfolders.'
    for filename, body in documents.items():
        assert (batch / filename).read_bytes() == body.encode('utf-8'), filename
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        names = z.namelist()
        assert set(names) == set(payloads) and len(names) == len(payloads)
        assert len({p.casefold() for p in names}) == len(names)
        for entry in z.infolist():
            path = PurePosixPath(entry.filename)
            assert path.parts[0] == name and '..' not in path.parts and not path.is_absolute()
            assert not entry.flag_bits & 1 and entry.compress_type == zipfile.ZIP_DEFLATED
            assert z.read(entry.filename) == payloads[entry.filename]
    return {'mod': name, 'release_id': config['release_id'], 'version': version, 'status': 'passed',
        'files': sorted(p.name for p in batch.iterdir()), 'archive_entries': len(payloads),
        'nested_archives': 0, 'diagnostics_stripped': config.get('diagnostics_stripped',False), 'vortex_installer': vortex_check(name, payloads)}


def build(config, version, documents, payloads):
    batch = RELEASE / config['release_id']
    if batch.exists():
        try:
            return batch, validate(batch, config, version, documents, payloads)
        except AssertionError as error:
            raise AssertionError('Existing releases are immutable. Use a new release_id such as version-r2.') from error
    run = subprocess.run([sys.executable, str(ROOT / 'tests/run.py')], cwd=ROOT)
    assert run.returncode == 0, 'Project checks failed; no release created.'
    RELEASE.mkdir(parents=True, exist_ok=True)
    (ROOT / 'build').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='release-', dir=ROOT / 'build') as temporary:
        staged = Path(temporary) / config['release_id']
        staged.mkdir()
        for filename, body in documents.items():
            (staged / filename).write_text(body, encoding='utf-8', newline='\n')
        with zipfile.ZipFile(staged / f'{config["mod"]}-{version}.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for path, data in sorted(payloads.items()):
                z.writestr(path, data)
        report = validate(staged, config, version, documents, payloads)
        staged.rename(batch)
    return batch, report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate the configured release without rebuilding it.')
    parser.add_argument('--strip-debug', action='store_true', help='Remove performance diagnostics and publish the -r2 packaging variant.')
    args = parser.parse_args()
    config, version, documents, payloads = collect_sources(args.strip_debug)
    batch = RELEASE / config['release_id']
    if args.check:
        report = validate(batch, config, version, documents, payloads)
    else:
        batch, report = build(config, version, documents, payloads)
    CHECKS.mkdir(parents=True, exist_ok=True)
    (CHECKS / 'release-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Release ready:', batch)
    print('One ZIP; English + Simplified Chinese BBCode; English changelog and summary.')
    print('Vortex:', report['vortex_installer']['status'], '| Nexus category:', config.get('file_category', 'Main Files'))
