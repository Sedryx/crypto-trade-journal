param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot ".venv\\Scripts\\python.exe"
$spec = Join-Path $projectRoot "packaging\\pyinstaller.spec"

if (-not (Test-Path $python)) {
    throw "Virtual environment Python not found at $python"
}

$requiredModules = @("PyInstaller", "PIL")
foreach ($module in $requiredModules) {
    & $python -c "import $module" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Missing Python dependency '$module' in the virtual environment. Run: $python -m pip install -r requirements.txt"
    }
}

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
