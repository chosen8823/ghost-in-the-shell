@echo off
echo Setting up Sophia AI Platform for deployment...

REM Create directories
echo Creating directory structure...
mkdir database 2>nul
mkdir logs 2>nul
mkdir static 2>nul
mkdir config\nginx 2>nul
mkdir config\docker 2>nul
mkdir scripts\setup 2>nul
mkdir scripts\deployment 2>nul
mkdir scripts\maintenance 2>nul
mkdir scripts\development 2>nul
echo Directory structure created.

REM Create .env.example
echo Creating environment configuration...
(
echo # Flask Configuration
echo FLASK_ENV=production
echo SECRET_KEY=your_secret_key_here
echo DATABASE_URL=sqlite:///database/app.db
echo.
echo # CORS Configuration
echo CORS_ORIGINS=*
echo.
echo # LLM API Keys
echo OPENAI_API_KEY=your_openai_api_key_here
echo HUGGINGFACE_API_KEY=your_huggingface_api_key_here
echo.
echo # Google Cloud Configuration
echo GOOGLE_CLOUD_PROJECT=your_project_id
echo GOOGLE_CLOUD_REGION=us-central1
echo.
echo # Application Settings
echo APP_NAME=Sophia AI Platform
echo APP_VERSION=1.0.0
) > .env.example
echo Environment configuration template created.

REM Create .gitignore
echo Creating .gitignore...
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *.so
echo .Python
echo build/
echo dist/
echo *.egg-info/
echo.
echo # Environments
echo .env
echo .venv
echo env/
echo venv/
echo.
echo # Database files
echo *.db
echo *.sqlite
echo *.sqlite3
echo.
echo # Log files
echo *.log
echo logs/
echo.
echo # OS generated files
echo .DS_Store
echo Thumbs.db
echo.
echo # IDE files
echo .vscode/
echo .idea/
echo.
echo # Node.js
echo node_modules/
echo package-lock.json
echo.
echo # Build outputs
echo dist/
echo build/
echo.
echo # Google Cloud credentials
echo *.json
echo !*example*.json
) > .gitignore
echo .gitignore created.

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Copy .env.example to .env and configure your settings
echo 2. Install required tools: Python, Node.js, Docker, Google Cloud SDK
echo 3. Use Git Bash to run the deployment scripts
echo 4. See DEPLOYMENT.md for detailed instructions
echo.
echo Your Sophia AI Platform is ready for deployment!

pause
