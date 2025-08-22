@echo off
echo 🌐 Setting up Sophia ChatGPT Public Tunnels
echo ==========================================

echo.
echo 🚀 Starting Sophia ChatGPT Bridge...
start "Sophia ChatGPT Bridge" python sophia_chatgpt_bridge.py

echo.
echo ⏳ Waiting for services to start...
timeout /t 5 /nobreak > nul

echo.
echo 🌐 Creating public tunnels with ngrok...
echo.

echo 📡 Tunnel 1: ChatGPT Bridge (Port 8080)
start "ChatGPT Bridge Tunnel" ngrok http 8080 --log=stdout

echo.
echo 📡 Tunnel 2: MCP Bridge (Port 3001) 
start "MCP Bridge Tunnel" ngrok http 3001 --log=stdout

echo.
echo 📡 Tunnel 3: N8N Workflows (Port 5678)
start "N8N Tunnel" ngrok http 5678 --log=stdout

echo.
echo ✅ All tunnels starting!
echo.
echo 🎯 Next Steps:
echo 1. Check ngrok terminals for public URLs
echo 2. Use the ChatGPT Bridge URL in ChatGPT Custom GPT
echo 3. Test with: [your-ngrok-url]/chatgpt/webhook
echo.
echo 📋 Example ChatGPT payload:
echo {
echo   "message": "open notepad",
echo   "action": "app_control", 
echo   "conversation_id": "test123"
echo }
echo.
echo Press any key to continue...
pause > nul
