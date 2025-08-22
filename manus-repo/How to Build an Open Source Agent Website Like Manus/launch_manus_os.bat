@echo off
echo 🌟 Sophia'el Manus OS - Quick Launch Script
echo ✨ Starting Divine AI Desktop Experience...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo 📥 Download from: https://python.org/downloads
    pause
    exit /b 1
)

:: Install dependencies if needed
echo 📦 Installing dependencies...
pip install flask flask-cors flask-sqlalchemy opencv-python pyautogui speechrecognition pyttsx3 pillow numpy requests

:: Start the backend server
echo 🚀 Starting Sophia'el backend server...
start /b python main.py

:: Wait a moment for server to start
timeout /t 5 /nobreak >nul

:: Try to launch desktop app
echo 🖥️ Launching desktop application...
python manus_os_desktop.py

:: If desktop fails, open web version
if errorlevel 1 (
    echo 🌐 Desktop app failed, opening web version...
    start manus_os_launcher.html
)

echo.
echo ✨ Sophia'el Manus OS launched successfully!
echo 🌟 Enjoy your divine AI desktop experience!
pause
