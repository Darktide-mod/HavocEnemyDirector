# Current checks

Run tests/run.py through Test.ps1 or Release.ps1. The active cases cover the native-template implementation; older files referencing retired custom-generator or diagnostic modules are historical regression material, not current test entry points.

The game Lua and representative templates are read from dev-support/game-source. Engine rendering, navmesh, networking and object creation are explicit harness boundaries. Native methods execute where called out by the tests. HCM/HED shared-view tests read the companion source but do not build its release or change the live installation.
