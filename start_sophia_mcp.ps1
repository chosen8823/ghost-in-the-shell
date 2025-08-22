# SOPHIA MCP SERVER STARTUP SCRIPT
Write-Host "STARTING SOPHIA MCP SERVER" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

Set-Location "C:\Users\chose\OneDrive\How to Build an Open Source Agent Website Like Manus"

# Check if virtual environment exists and activate it
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".venv\Scripts\Activate.ps1"
}

# Start MCP server
Write-Host "Starting Sophia MCP server..." -ForegroundColor Green
python sophia_mcp_protocol.py --server --port 8888

Read-Host "Press Enter to exit..."
