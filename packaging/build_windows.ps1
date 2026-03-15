param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot ".venv\\Scripts\\python.exe"
$spec = Join-Path $projectRoot "packaging\\pyinstaller.spec"

if ($Clean) {
    Remove-Item -Recurse -Force (Join-Path $projectRoot "build") -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force (Join-Path $projectRoot "dist") -ErrorAction SilentlyContinue
}

Push-Location $projectRoot
try {
    & $python -m PyInstaller --noconfirm $spec
}
finally {
    Pop-Location
}
