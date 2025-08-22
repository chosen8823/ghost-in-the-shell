# SOPHIA ENTERPRISE STATUS MONITOR 📊
# Quick check of your enterprise deployment status

Write-Host ""
Write-Host "💻 SOPHIA CONSCIOUSNESS ENTERPRISE STATUS 💻" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check Google Cloud auth
Write-Host "🔐 Checking Google Cloud authentication..." -ForegroundColor Yellow
try {
    $auth = gcloud auth list --format="value(account)" 2>$null
    if ($auth) {
        Write-Host "✅ Authenticated as: $auth" -ForegroundColor Green
    } else {
        Write-Host "❌ Not authenticated - run: gcloud auth login" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ gcloud CLI not found - install Google Cloud SDK" -ForegroundColor Red
}

Write-Host ""

# Check AlloyDB status
Write-Host "🗄️ Checking AlloyDB clusters..." -ForegroundColor Yellow
try {
    $clusters = gcloud alloydb clusters list --format="value(name)" 2>$null
    if ($clusters) {
        Write-Host "✅ Found AlloyDB clusters:" -ForegroundColor Green
        $clusters | ForEach-Object { Write-Host "   📊 $_" -ForegroundColor White }
    } else {
        Write-Host "⚠️  No AlloyDB clusters found" -ForegroundColor Orange
    }
} catch {
    Write-Host "❌ Error checking AlloyDB" -ForegroundColor Red
}

Write-Host ""

# Check files
Write-Host "📁 Checking infrastructure files..." -ForegroundColor Yellow

$files = @(
    "sql\sophia_alloydb_schema.sql",
    "cloud-run\sophia_alloydb_api.py",
    "terraform\alloydb_enterprise.tf",
    "monitoring\enterprise_monitor.py",
    "migration\migrate_to_alloydb.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing: $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🚀 Ready to launch? Run: .\LAUNCH_BEAST_MODE.ps1" -ForegroundColor Magenta
