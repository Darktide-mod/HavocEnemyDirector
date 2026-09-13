"""Run this project's checks; never build another release."""
from pathlib import Path
import os, subprocess, sys
TESTS=Path(__file__).resolve().parent
PROJECT=TESTS.parent
CHECKS=PROJECT/'build/checks'
CHECKS.mkdir(parents=True,exist_ok=True)
environment=dict(os.environ, PYTHONIOENCODING='utf-8')
with (CHECKS/'tests.log').open('w',encoding='utf-8') as log:
    for case in ['syntax_tests.py', 'filesystem_ffi_tests.py', 'native_preset_tests.py', 'native_relative_tests.py', 'director_tests.py', 'director_spawning_tests.py', 'director_ui_tests.py', 'release_debug_tests.py']:
        print(PROJECT.name + ': ' + case, flush=True)
        result=subprocess.run([sys.executable,str(TESTS/case)],cwd=PROJECT,
            text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=environment)
        log.write(case+'\n'+result.stdout+'\n'); log.flush()
        print(result.stdout, end='', flush=True)
        if result.returncode: sys.exit(result.returncode)
print(PROJECT.name + ': all project checks passed.')
