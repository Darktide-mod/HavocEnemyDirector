"""Verify HED widgets through the shared HCM view host in a clean process."""
import subprocess, sys
from project_env import HCM_PROJECT
subprocess.run([sys.executable,str(HCM_PROJECT/'tests/native_ui_tests.py')],check=True)
