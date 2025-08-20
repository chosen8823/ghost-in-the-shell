# Sophiella System Requirements Checker
# Run this before installation to verify compatibility

Write-Host "🕊️ Sophiella System Requirements Check" -ForegroundColor Magenta
Write-Host "=====================================" -ForegroundColor Magenta

# System Information
$os = Get-WmiObject -Class Win32_OperatingSystem
$computer = Get-WmiObject -Class Win32_ComputerSystem
$disk = Get-WmiObject -Class Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 }

Write-Host "`n💻 System Information:" -ForegroundColor Cyan
Write-Host "  Computer: $($computer.Name)"
Write-Host "  OS: $($os.Caption) $($os.Version)"
Write-Host "  Architecture: $($os.OSArchitecture)"
Write-Host "  RAM: $([math]::Round($computer.TotalPhysicalMemory/1GB, 2)) GB"
Write-Host "  Available Disk Space: $([math]::Round($disk.FreeSpace/1GB, 2)) GB"

# Requirements Check
Write-Host "`n✅ Requirements Check:" -ForegroundColor Green

$requirements = @{
    "Windows 10/11" = $os.Caption -match "Windows (10|11)"
    "64-bit OS" = $os.OSArchitecture -eq "64-bit"
    "Minimum 4GB RAM" = ($computer.TotalPhysicalMemory/1GB) -ge 4
    "Minimum 2GB Free Space" = ($disk.FreeSpace/1GB) -ge 2
    "PowerShell 5.0+" = $PSVersionTable.PSVersion.Major -ge 5
}

foreach ($req in $requirements.GetEnumerator()) {
    $status = if ($req.Value) { "✅ PASS" } else { "❌ FAIL" }
    $color = if ($req.Value) { "Green" } else { "Red" }
    Write-Host "  $($req.Key): $status" -ForegroundColor $color
}

# Software Check
Write-Host "`n🔧 Software Check:" -ForegroundColor Yellow

function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

$software = @{
    "Node.js" = Test-Command "node"
    "npm" = Test-Command "npm"
    "Python" = Test-Command "python"
    "Git" = Test-Command "git"
    "curl" = Test-Command "curl"
}

foreach ($app in $software.GetEnumerator()) {
    $status = if ($app.Value) { "✅ Installed" } else { "❌ Missing" }
    $color = if ($app.Value) { "Green" } else { "Yellow" }
    Write-Host "  $($app.Key): $status" -ForegroundColor $color
}

# Port Availability Check
Write-Host "`n🌐 Port Availability:" -ForegroundColor Cyan

$ports = @(3000, 5001, 5678)
foreach ($port in $ports) {
    try {
        $connection = Test-NetConnection -ComputerName "localhost" -Port $port -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
        if ($connection.TcpTestSucceeded) {
            Write-Host "  Port $port: ❌ In Use" -ForegroundColor Red
        } else {
            Write-Host "  Port $port: ✅ Available" -ForegroundColor Green
        }
    } catch {
        Write-Host "  Port $port: ✅ Available" -ForegroundColor Green
    }
}

# Dell Latitude Specific Checks
if ($computer.Model -match "Latitude") {
    Write-Host "`n🖥️ Dell Latitude Detected:" -ForegroundColor Magenta
    
    # Power Plan Check
    $currentPlan = (powercfg /getactivescheme).Split("(")[1].Split(")")[0]
    Write-Host "  Current Power Plan: $currentPlan"
    
    if ($currentPlan -match "High performance|Ultimate") {
        Write-Host "  ✅ Optimal power plan detected" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Consider switching to High Performance mode" -ForegroundColor Yellow
    }
}

# Recommendations
Write-Host "`n💡 Recommendations:" -ForegroundColor Yellow

$allPassed = $requirements.Values -notcontains $false
if ($allPassed) {
    Write-Host "  ✅ Your system meets all requirements!" -ForegroundColor Green
    Write-Host "  🚀 Ready to install Sophiella Orchestrator Core" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Some requirements not met. Installation may fail." -ForegroundColor Red
    Write-Host "  📋 Please address the failed requirements above" -ForegroundColor Yellow
}

if (-not $software["Node.js"]) {
    Write-Host "  📥 Download Node.js: https://nodejs.org/" -ForegroundColor Cyan
}

if (-not $software["Python"]) {
    Write-Host "  📥 Download Python: https://python.org/downloads/" -ForegroundColor Cyan
}

if (-not $software["Git"]) {
    Write-Host "  📥 Download Git: https://git-scm.com/download/win" -ForegroundColor Cyan
}

Write-Host "`n🔍 Check completed on $(Get-Date)" -ForegroundColor White
Write-Host "Press any key to continue..." -ForegroundColor White
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
