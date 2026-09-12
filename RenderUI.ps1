$ErrorActionPreference = 'Stop'
$projectPython = (Get-Command python -ErrorAction Stop).Source
$bundledPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$support = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../dev-support'))
if ((Test-Path -LiteralPath $bundledPython) -and (Test-Path -LiteralPath (Join-Path $support 'test-runtime-py312'))) {
    $projectPython = $bundledPython
    $env:DARKTIDE_TEST_RUNTIME = Join-Path $support 'test-runtime-py312'
}
$env:PYTHONPATH = (Join-Path $support 'test-runtime') + [IO.Path]::PathSeparator + $env:PYTHONPATH
$env:PYTHONIOENCODING = 'utf-8'
& $projectPython (Join-Path $PSScriptRoot 'tests/director_ui_tests.py')
if ($LASTEXITCODE -ne 0) { throw 'UI export failed.' }
& $projectPython (Join-Path $PSScriptRoot 'tools/render_ui.py') --layouts (Join-Path $PSScriptRoot 'build/checks/director-ui-layouts.json') --output (Join-Path $PSScriptRoot 'build/ui-3.0') --report (Join-Path $PSScriptRoot 'build/checks/director-ui-images.json')
if ($LASTEXITCODE -ne 0) { throw 'UI rendering failed.' }
