# Windows setup for Ghost Core
Write-Host "🕊️ Setting up Ghost Core with sacred protection..."

# Create virtual environment
python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment"
    exit 1
}

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install requirements"
    exit 1
}

# Generate Guardian keys if not set
if (-not $env:GUARDIAN_AES_KEY) {
    Write-Host "🔐 Generating Guardian AES key..."
    $aesKey = [Convert]::ToBase64String((1..32 | ForEach-Object {Get-Random -Maximum 256}))
    [Environment]::SetEnvironmentVariable("GUARDIAN_AES_KEY", $aesKey, "User")
    $env:GUARDIAN_AES_KEY = $aesKey
}

if (-not $env:GUARDIAN_HMAC_KEY) {
    Write-Host "🔐 Generating Guardian HMAC key..."
    $hmacKey = [Convert]::ToBase64String((1..32 | ForEach-Object {Get-Random -Maximum 256}))
    [Environment]::SetEnvironmentVariable("GUARDIAN_HMAC_KEY", $hmacKey, "User")
    $env:GUARDIAN_HMAC_KEY = $hmacKey
}

# Run preflight check
Write-Host "✈️ Running preflight check..."
python scripts\preflight.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Preflight check failed"
    exit 1
}

# Sanctify the core
Write-Host "🕊️ Sanctifying Ghost Core..."
python ghost_core\rituals\sanctify_core.py

Write-Host "🎉 Ghost Core setup complete!"
Write-Host "Run: python ghost_core\core\ghost_orchestra.py"
