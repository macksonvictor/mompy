param(
  [switch]$Zip
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = if ($env:PYTHON) { $env:PYTHON } else { "python" }
$IconPath = Join-Path $ProjectRoot "frontend\assets\mompy_idle.ico"
$DistPath = Join-Path $ProjectRoot "dist"
$BuildPath = Join-Path $ProjectRoot "build"
$SpecPath = Join-Path $ProjectRoot "Mompy.spec"
$ZipPath = Join-Path $DistPath "Mompy-windows-x64.zip"

Push-Location $ProjectRoot
try {
  & $Python -m PyInstaller --version | Out-Null

  if (Test-Path $DistPath) {
    Remove-Item -LiteralPath $DistPath -Recurse -Force
  }

  if (Test-Path $BuildPath) {
    Remove-Item -LiteralPath $BuildPath -Recurse -Force
  }

  if (Test-Path $SpecPath) {
    Remove-Item -LiteralPath $SpecPath -Force
  }

  $pyinstallerArgs = @(
    "--noconfirm",
    "--clean",
    "--windowed",
    "--name", "Mompy",
    "--icon", $IconPath,
    "--add-data", "frontend;frontend",
    "--collect-submodules", "backend",
    "main.py"
  )

  & $Python -m PyInstaller @pyinstallerArgs

  $ExePath = Join-Path $DistPath "Mompy\Mompy.exe"
  if (-not (Test-Path $ExePath)) {
    throw "Build finished, but executable was not found at $ExePath"
  }

  if ($Zip) {
    if (Test-Path $ZipPath) {
      Remove-Item -LiteralPath $ZipPath -Force
    }

    Compress-Archive -Path (Join-Path $DistPath "Mompy\*") -DestinationPath $ZipPath -Force
    Write-Host "Package created: $ZipPath"
  }

  Write-Host "Executable created: $ExePath"
} finally {
  Pop-Location
}
