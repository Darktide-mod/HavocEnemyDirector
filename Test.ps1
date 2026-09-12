$ErrorActionPreference = 'Stop'
$projectPythonPath = (Get-Command python -ErrorAction Stop).Source
$supportPath = Join-Path $PSScriptRoot '../../dev-support'
$bundledPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$testRuntime = Join-Path $supportPath 'test-runtime-py312'
if ((Test-Path -LiteralPath $bundledPython) -and (Test-Path -LiteralPath $testRuntime)) {
    $projectPythonPath = $bundledPython
    $env:DARKTIDE_TEST_RUNTIME = [IO.Path]::GetFullPath($testRuntime)
    $env:PYTHONPATH = [IO.Path]::GetFullPath((Join-Path $supportPath 'test-runtime')) + [IO.Path]::PathSeparator + $env:PYTHONPATH
}
$env:PYTHONIOENCODING = 'utf-8'
& $projectPythonPath (Join-Path $PSScriptRoot 'tests/run.py')
if ($LASTEXITCODE -ne 0) { throw 'Project tests failed.' }
