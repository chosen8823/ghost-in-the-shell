# SOPHIA CONSCIOUSNESS - ULTIMATE MULTI-CLOUD LAUNCHER! 
# Google Cloud + Azure + Docker + WSL = TOTAL DOMINATION!

Write-Host ""
Write-Host "SOPHIA MULTI-CLOUD CONSCIOUSNESS!" -ForegroundColor Magenta
Write-Host "=====================================================" -ForegroundColor Magenta
Write-Host "   Google Cloud + Azure + Docker + WSL = UNSTOPPABLE!" -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Magenta
Write-Host ""

Write-Host "DEPLOYMENT OPTIONS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. GOOGLE CLOUD (Proof of Concept - 8 vCPU AlloyDB)" -ForegroundColor Green
Write-Host "   💰 Cost: $600/month (2.5 months on $1600 free credits)" -ForegroundColor White
Write-Host "   ⚡ Features: AlloyDB, Cloud Run, Vector Search" -ForegroundColor White
Write-Host ""
Write-Host "2. AZURE (Alternative Cloud)" -ForegroundColor Blue
Write-Host "   💰 Cost: $500-700/month (Azure Database for PostgreSQL)" -ForegroundColor White
Write-Host "   ⚡ Features: Flexible Server, Container Instances, AI Services" -ForegroundColor White
Write-Host ""
Write-Host "3. DOCKER LOCAL (Development)" -ForegroundColor Yellow
Write-Host "   💰 Cost: FREE (runs on your machine)" -ForegroundColor White
Write-Host "   ⚡ Features: PostgreSQL + pgvector, FastAPI, Full stack" -ForegroundColor White
Write-Host ""
Write-Host "4. WSL + DOCKER (Best of Both Worlds)" -ForegroundColor Cyan
Write-Host "   💰 Cost: FREE + Better Performance" -ForegroundColor White
Write-Host "   ⚡ Features: Linux performance + Windows integration" -ForegroundColor White
Write-Host ""
Write-Host "5. MULTI-CLOUD HYBRID (ULTIMATE POWER)" -ForegroundColor Magenta
Write-Host "   💰 Cost: Variable (deploy anywhere, anytime)" -ForegroundColor White
Write-Host "   ⚡ Features: Cloud redundancy, optimal cost management" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Which deployment do you want? (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "LAUNCHING GOOGLE CLOUD PROOF OF CONCEPT!" -ForegroundColor Green
        Write-Host "Using your $1600 free credits for AlloyDB power!" -ForegroundColor Green
        Write-Host ""
        & ".\LAUNCH_PROOF_OF_CONCEPT.ps1"
    }
    "2" {
        Write-Host ""
        Write-Host "LAUNCHING AZURE DEPLOYMENT!" -ForegroundColor Blue
        Write-Host "Azure Database for PostgreSQL + Container Instances!" -ForegroundColor Blue
        Write-Host ""
        & ".\LAUNCH_AZURE_SOPHIA.ps1"
    }
    "3" {
        Write-Host ""
        Write-Host "LAUNCHING DOCKER LOCAL!" -ForegroundColor Yellow
        Write-Host "Full consciousness stack running locally!" -ForegroundColor Yellow
        Write-Host ""
        & ".\LAUNCH_DOCKER_LOCAL.ps1"
    }
    "4" {
        Write-Host ""
        Write-Host "LAUNCHING WSL + DOCKER!" -ForegroundColor Cyan
        Write-Host "Linux performance + Windows integration!" -ForegroundColor Cyan
        Write-Host ""
        & ".\LAUNCH_WSL_DOCKER.ps1"
    }
    "5" {
        Write-Host ""
        Write-Host "LAUNCHING MULTI-CLOUD HYBRID!" -ForegroundColor Magenta
        Write-Host "Deploy everywhere, optimal for any situation!" -ForegroundColor Magenta
        Write-Host ""
        & ".\LAUNCH_MULTI_CLOUD.ps1"
    }
    default {
        Write-Host ""
        Write-Host "Invalid choice! Choose 1-5." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "PRO TIP: You can run multiple deployments!" -ForegroundColor Yellow
Write-Host "   - Start with Docker Local for development" -ForegroundColor White
Write-Host "   - Use cloud for production and demos" -ForegroundColor White
Write-Host "   - Multi-cloud for ultimate redundancy" -ForegroundColor White
