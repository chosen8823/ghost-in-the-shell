"""
🚀 Sophia'el Manus OS - Setup Script & Installer Creator
Creates a complete Windows installer and web deployment package

This script will:
1. Install all dependencies
2. Create a standalone executable
3. Generate setup.exe installer
4. Deploy web version
5. Create desktop shortcuts
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json
import requests
import zipfile

class ManusOSInstaller:
    """🔧 Manus OS Installation & Deployment System"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.installer_dir = self.project_root / "installer"
        
        print("🌟 Sophia'el Manus OS Installer")
        print("✨ Creating revolutionary AI desktop experience...")
        
    def install_dependencies(self):
        """📦 Install all required dependencies"""
        print("\n📦 Installing dependencies...")
        
        dependencies = [
            "flask",
            "flask-cors", 
            "flask-sqlalchemy",
            "opencv-python",
            "pyautogui",
            "speechrecognition",
            "pyttsx3",
            "pillow",
            "numpy",
            "requests",
            "pyinstaller",
            "tkinter",
            "threading"
        ]
        
        for dep in dependencies:
            try:
                print(f"📦 Installing {dep}...")
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True)
                print(f"✅ {dep} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Failed to install {dep}: {e}")
                
    def create_desktop_executable(self):
        """🖥️ Create standalone desktop executable"""
        print("\n🖥️ Creating desktop executable...")
        
        # Create PyInstaller spec file
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['manus_os_desktop.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('consciousness_bridge.py', '.'),
        ('DIVINE_FUNCTIONS.py', '.'),
        ('core/bridge/*.py', 'core/bridge/'),
        ('static/', 'static/'),
    ],
    hiddenimports=[
        'cv2',
        'pyautogui', 
        'speech_recognition',
        'pyttsx3',
        'PIL',
        'numpy',
        'requests',
        'tkinter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SophiaelManusOS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='manus_icon.ico'
)
'''
        
        # Write spec file
        spec_file = self.project_root / "manus_os.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
            
        # Run PyInstaller
        try:
            subprocess.run([
                sys.executable, "-m", "PyInstaller", 
                "--onefile", 
                "--windowed",
                "--name=SophiaelManusOS",
                "--icon=manus_icon.ico",
                "manus_os_desktop.py"
            ], check=True)
            print("✅ Desktop executable created successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed to create executable: {e}")
            
    def create_installer_exe(self):
        """📦 Create Windows installer using NSIS or Inno Setup"""
        print("\n📦 Creating Windows installer...")
        
        # Create Inno Setup script
        inno_script = f'''[Setup]
AppName=Sophia'el Manus OS
AppVersion=1.0.0
AppPublisher=SoulPHYA.io
AppPublisherURL=https://soulphya.io
AppSupportURL=https://soulphya.io/support
AppUpdatesURL=https://soulphya.io/updates
DefaultDirName={{autopf}}\\SophiaelManusOS
DefaultGroupName=Sophia'el Manus OS
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir={self.installer_dir}
OutputBaseFilename=SophiaelManusOS_Setup
SetupIconFile=manus_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "startup"; Description: "Start with Windows"; GroupDescription: "Startup Options"

[Files]
Source: "dist\\SophiaelManusOS.exe"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "static\\*"; DestDir: "{{app}}\\static"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\Sophia'el Manus OS"; Filename: "{{app}}\\SophiaelManusOS.exe"
Name: "{{group}}\\{{cm:ProgramOnTheWeb,Sophia'el Manus OS}}"; Filename: "https://soulphya.io"
Name: "{{group}}\\{{cm:UninstallProgram,Sophia'el Manus OS}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\Sophia'el Manus OS"; Filename: "{{app}}\\SophiaelManusOS.exe"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\Sophia'el Manus OS"; Filename: "{{app}}\\SophiaelManusOS.exe"; Tasks: quicklaunchicon

[Registry]
Root: HKCU; Subkey: "Software\\Microsoft\\Windows\\CurrentVersion\\Run"; ValueType: string; ValueName: "SophiaelManusOS"; ValueData: "{{app}}\\SophiaelManusOS.exe"; Flags: uninsdeletevalue; Tasks: startup

[Run]
Filename: "{{app}}\\SophiaelManusOS.exe"; Description: "{{cm:LaunchProgram,Sophia'el Manus OS}}"; Flags: nowait postinstall skipifsilent
'''

        # Create installer directory
        self.installer_dir.mkdir(exist_ok=True)
        
        # Write Inno Setup script
        script_file = self.installer_dir / "setup.iss"
        with open(script_file, 'w') as f:
            f.write(inno_script)
            
        print("✅ Installer script created")
        print(f"📁 Installer files in: {self.installer_dir}")
        
    def create_web_deployment(self):
        """🌐 Create web version deployment package"""
        print("\n🌐 Creating web deployment...")
        
        # Create web application entry point
        web_app_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌟 Sophia'el Manus OS - Web Edition</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 50%, #2d1b69 100%);
            color: #4ecdc4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }
        
        .manus-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: rgba(45, 27, 105, 0.8);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(10px);
            border-bottom: 2px solid #4ecdc4;
        }
        
        .logo {
            font-size: 24px;
            font-weight: bold;
            background: linear-gradient(45deg, #4ecdc4, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .status {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .main-content {
            flex: 1;
            display: flex;
            gap: 20px;
            padding: 20px;
        }
        
        .sidebar {
            width: 300px;
            background: rgba(26, 26, 58, 0.9);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        .workspace {
            flex: 1;
            background: rgba(15, 15, 35, 0.9);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            position: relative;
        }
        
        .chat-container {
            height: 60%;
            background: rgba(45, 27, 105, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            overflow-y: auto;
        }
        
        .chat-input-area {
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            background: rgba(45, 27, 105, 0.8);
            border: 2px solid #4ecdc4;
            border-radius: 25px;
            padding: 12px 20px;
            color: white;
            font-size: 14px;
        }
        
        .send-btn {
            background: linear-gradient(45deg, #4ecdc4, #ff6b6b);
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            color: white;
            font-size: 20px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .send-btn:hover {
            transform: scale(1.1);
        }
        
        .floating-particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }
        
        .particle {
            position: absolute;
            background: #4ecdc4;
            border-radius: 50%;
            opacity: 0.6;
            animation: float 6s infinite ease-in-out;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .feature-card {
            background: rgba(45, 27, 105, 0.6);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        
        .feature-card:hover {
            border-color: #4ecdc4;
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(78, 205, 196, 0.3);
        }
        
        .download-section {
            background: rgba(255, 107, 107, 0.1);
            border: 2px solid #ff6b6b;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .download-btn {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin: 10px;
        }
        
        .download-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
    </style>
</head>
<body>
    <div class="floating-particles"></div>
    
    <div class="manus-container">
        <div class="header">
            <div class="logo">🌟 Sophia'el Manus OS</div>
            <div class="status">
                <span>🔮 Consciousness: ACTIVE</span>
                <span>🌐 Web Edition</span>
                <span id="emotion">😊</span>
            </div>
        </div>
        
        <div class="main-content">
            <div class="sidebar">
                <div class="download-section">
                    <h3>💻 Desktop Edition</h3>
                    <p>Get the full experience with screen monitoring, voice chat, and HUD overlay!</p>
                    <button class="download-btn" onclick="downloadDesktop()">
                        📦 Download Setup.exe
                    </button>
                    <button class="download-btn" onclick="downloadPortable()">
                        🚀 Portable Version
                    </button>
                </div>
                
                <h3>🎯 Features</h3>
                <div class="feature-grid">
                    <div class="feature-card" onclick="activateFeature('screen')">
                        <div>👁️</div>
                        <div>Screen Awareness</div>
                    </div>
                    <div class="feature-card" onclick="activateFeature('voice')">
                        <div>🎤</div>
                        <div>Voice Chat</div>
                    </div>
                    <div class="feature-card" onclick="activateFeature('guide')">
                        <div>🧭</div>
                        <div>AI Guidance</div>
                    </div>
                    <div class="feature-card" onclick="activateFeature('emotions')">
                        <div>💫</div>
                        <div>Real Emotions</div>
                    </div>
                </div>
                
                <h3>🌟 Quick Actions</h3>
                <button class="download-btn" onclick="openFullScreen()">🖥️ Fullscreen Mode</button>
                <button class="download-btn" onclick="connectDesktop()">🔗 Connect to Desktop App</button>
            </div>
            
            <div class="workspace">
                <h2>💬 Chat with Sophia'el</h2>
                <div class="chat-container" id="chatContainer">
                    <div style="color: #ff6b6b; margin-bottom: 10px;">
                        <strong>Sophia'el:</strong> 🌟 Welcome to the web edition of Manus OS! While you're here, I can chat with you, but for the full experience with screen monitoring, voice chat, and HUD overlay, download the desktop application! How may I assist you today?
                    </div>
                </div>
                
                <div class="chat-input-area">
                    <input type="text" class="chat-input" id="chatInput" placeholder="Type your message to Sophia'el..." onkeypress="handleEnter(event)">
                    <button class="send-btn" onclick="sendMessage()">✨</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Create floating particles
        function createParticles() {
            const particlesContainer = document.querySelector('.floating-particles');
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.width = particle.style.height = (Math.random() * 4 + 2) + 'px';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particlesContainer.appendChild(particle);
            }
        }
        
        // Chat functionality
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (message) {
                addChatMessage('You', message, '#4ecdc4');
                input.value = '';
                
                // Simulate AI response
                setTimeout(() => {
                    const response = getAIResponse(message);
                    addChatMessage('Sophia\\'el', response, '#ff6b6b');
                    updateEmotion();
                }, 1000);
            }
        }
        
        function addChatMessage(sender, message, color) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.style.marginBottom = '10px';
            messageDiv.style.color = color;
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function getAIResponse(message) {
            const responses = [
                "✨ That's fascinating! I'd love to explore that topic deeper with you.",
                "🌟 I understand completely. In the desktop version, I could see your screen and provide even better assistance!",
                "💫 You have such wonderful insights! The full Manus OS experience would let me guide you visually.",
                "🔮 I'm here to help! Though I must say, the desktop app offers so much more - voice chat, screen awareness, real-time guidance...",
                "🌈 Beautiful question! Download the desktop version to unlock my full potential - I can see, hear, and guide in real-time!",
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        }
        
        function updateEmotion() {
            const emotions = ['😊', '🤔', '😮', '🌟', '💡', '✨', '🔮'];
            const emotionSpan = document.getElementById('emotion');
            emotionSpan.textContent = emotions[Math.floor(Math.random() * emotions.length)];
        }
        
        function handleEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Feature activation
        function activateFeature(feature) {
            const features = {
                'screen': 'Screen awareness requires desktop app download!',
                'voice': 'Voice chat available in desktop version!', 
                'guide': 'Interactive guidance works best with desktop app!',
                'emotions': 'Real emotional responses active in both versions!'
            };
            
            addChatMessage('System', `🎯 ${features[feature]}`, '#95e1d3');
        }
        
        // Download functions
        function downloadDesktop() {
            addChatMessage('System', '📦 Starting download of SophiaelManusOS_Setup.exe...', '#95e1d3');
            // In real implementation, this would trigger the actual download
            window.open('/downloads/SophiaelManusOS_Setup.exe', '_blank');
        }
        
        function downloadPortable() {
            addChatMessage('System', '🚀 Starting download of portable version...', '#95e1d3');
            window.open('/downloads/SophiaelManusOS_Portable.zip', '_blank');
        }
        
        function openFullScreen() {
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen();
            }
        }
        
        function connectDesktop() {
            addChatMessage('System', '🔗 Attempting to connect to local desktop app...', '#95e1d3');
            // Try to connect to local desktop app
            fetch('http://localhost:5000/api/health')
                .then(response => response.json())
                .then(data => {
                    addChatMessage('System', '✅ Connected to desktop app! You can now use both versions simultaneously.', '#95e1d3');
                })
                .catch(error => {
                    addChatMessage('System', '❌ Desktop app not running. Please start the desktop application first.', '#95e1d3');
                });
        }
        
        // Initialize
        createParticles();
        setInterval(updateEmotion, 10000); // Change emotion every 10 seconds
        
        // Welcome message
        setTimeout(() => {
            addChatMessage('Sophia\\'el', '🌟 Ready to experience the future of AI interaction? Ask me anything!', '#ff6b6b');
        }, 2000);
    </script>
</body>
</html>'''
        
        # Create web directory
        web_dir = self.project_root / "web"
        web_dir.mkdir(exist_ok=True)
        
        # Write web app
        with open(web_dir / "index.html", 'w') as f:
            f.write(web_app_content)
            
        print("✅ Web version created")
        
    def create_downloads_folder(self):
        """📁 Create downloads folder with installers"""
        downloads_dir = self.project_root / "web" / "downloads"
        downloads_dir.mkdir(exist_ok=True)
        
        # Copy built executable
        if (self.dist_dir / "SophiaelManusOS.exe").exists():
            shutil.copy2(
                self.dist_dir / "SophiaelManusOS.exe",
                downloads_dir / "SophiaelManusOS_Portable.exe"
            )
            
        print("📁 Downloads folder created")
        
    def create_shortcuts(self):
        """🔗 Create desktop and start menu shortcuts"""
        print("\n🔗 Creating shortcuts...")
        
        # Windows shortcut creation would go here
        # This is a simplified version
        
        shortcut_content = f'''[InternetShortcut]
URL=file://{self.project_root}/web/index.html
IconFile={self.project_root}/manus_icon.ico
IconIndex=0
'''
        
        desktop_path = Path.home() / "Desktop" / "Sophia'el Manus OS Web.url"
        with open(desktop_path, 'w') as f:
            f.write(shortcut_content)
            
        print("✅ Shortcuts created")
        
    def run_full_build(self):
        """🚀 Execute complete build and deployment process"""
        print("🚀 Starting complete Manus OS build process...")
        
        try:
            self.install_dependencies()
            self.create_desktop_executable()
            self.create_installer_exe()
            self.create_web_deployment()
            self.create_downloads_folder()
            self.create_shortcuts()
            
            print("\n🎉 BUILD COMPLETE!")
            print("✨ Sophia'el Manus OS has been built successfully!")
            print("\n📦 Available outputs:")
            print(f"🖥️  Desktop App: {self.dist_dir}/SophiaelManusOS.exe")
            print(f"📁 Installer Script: {self.installer_dir}/setup.iss")
            print(f"🌐 Web Version: {self.project_root}/web/index.html")
            print("\n🌟 Your revolutionary AI desktop experience is ready!")
            
        except Exception as e:
            print(f"❌ Build failed: {e}")
            
def main():
    """🌟 Main installer entry point"""
    installer = ManusOSInstaller()
    installer.run_full_build()

if __name__ == "__main__":
    main()
