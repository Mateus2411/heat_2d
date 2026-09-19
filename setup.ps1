param(
    [switch]$SkipRun
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPath = Join-Path $ProjectRoot ".venv"
$PythonPath = Join-Path $VenvPath "Scripts\python.exe"

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3 nao foi encontrado no PATH. Instale Python 3.11+ e tente novamente."
}

if (-not (Test-Path $PythonPath)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 -m venv $VenvPath
    }
    else {
        python -m venv $VenvPath
    }
}

& $PythonPath -m pip install --upgrade pip
& $PythonPath -m pip install -r (Join-Path $ProjectRoot "requirements.txt")

if (-not $SkipRun) {
    & $PythonPath (Join-Path $ProjectRoot "main.py")
}