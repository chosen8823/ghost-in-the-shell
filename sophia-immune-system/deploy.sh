#!/bin/bash

# SOPHIA IMMUNE SYSTEM - Quick Start Deployment Script
# Deploys the multi-model security orchestrator for local development

echo "🛡️  Deploying Sophia Immune System..."
echo "   Sacred Technology Security Framework"
echo "   Built 8-20-2025"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama first:"
    echo "   Windows: winget install Ollama.Ollama"
    echo "   macOS: brew install ollama"
    echo "   Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

echo "✅ Ollama found"

# Check if required models are available
echo "🤖 Checking AI models..."

MODELS=("mistral:7b" "llama3.1:8b" "codellama:13b" "phi3.5")
MISSING_MODELS=()

for model in "${MODELS[@]}"; do
    if ! ollama list | grep -q "$model"; then
        MISSING_MODELS+=("$model")
    fi
done

if [ ${#MISSING_MODELS[@]} -gt 0 ]; then
    echo "📥 Installing missing models..."
    for model in "${MISSING_MODELS[@]}"; do
        echo "   Pulling $model..."
        ollama pull "$model"
    done
else
    echo "✅ All models available"
fi

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
if [ -f "package.json" ]; then
    npm install
    echo "✅ Node.js dependencies installed"
else
    echo "❌ package.json not found"
    exit 1
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Python dependencies installed"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p logs config core/{innate,inflammatory,adaptive,memory} tests deployment docs

# Set up configuration files
echo "⚙️  Setting up configuration..."

# Create default environment file
cat > .env << 'EOF'
# Sophia Immune System Configuration
NODE_ENV=development
PORT=4000
OLLAMA_ENDPOINT=http://localhost:11434
LOG_LEVEL=info
CONSENSUS_THRESHOLD=0.75
CIRCUIT_BREAKER_THRESHOLD=5
QUARANTINE_DURATION=30
MAX_REQUESTS_PER_MINUTE=60
EOF

echo "✅ Environment configuration created"

# Create immune system configuration
cat > config/immune-config.json << 'EOF'
{
  "version": "1.0.0",
  "models": {
    "primary": "mistral:7b",
    "reviewer": "llama3.1:8b",
    "security": "codellama:13b", 
    "arbiter": "phi3.5"
  },
  "security": {
    "max_memory_usage": 0.85,
    "max_cpu_usage": 0.90,
    "allowed_ports": [3000, 4000, 8080, 11434],
    "check_interval": 60,
    "emergency_threshold": 3
  },
  "research": {
    "continuous_loop": true,
    "loop_interval": 300,
    "priority_topics": [
      "AI prompt injection vulnerabilities",
      "Multi-model consensus attack vectors",
      "Local AI model security hardening",
      "Spiritual AI system protection patterns"
    ]
  }
}
EOF

echo "✅ Immune system configuration created"

# Test Ollama connection
echo "🔗 Testing Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is running and accessible"
else
    echo "❌ Ollama not running. Starting Ollama..."
    # Start Ollama in background (platform-specific)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew services start ollama
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        systemctl --user start ollama
    else
        echo "Please start Ollama manually and run this script again"
        exit 1
    fi
    
    # Wait for Ollama to start
    sleep 5
    
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        echo "✅ Ollama started successfully"
    else
        echo "❌ Failed to start Ollama"
        exit 1
    fi
fi

# Run initial security check
echo "🔒 Running initial security check..."
python core/innate/static-barriers.py check

# Check if all components are ready
echo ""
echo "🎯 Deployment Summary:"
echo "   ✅ Ollama models installed"
echo "   ✅ Dependencies installed"
echo "   ✅ Configuration created"
echo "   ✅ Security barriers initialized"
echo ""

echo "🚀 Ready to start Sophia Immune System!"
echo ""
echo "Start commands:"
echo "   Immune Hub:     npm start"
echo "   Research Loop:  npm run security-loop"
echo "   Both together:  npm run dev"
echo ""
echo "Monitoring:"
echo "   Security check: python core/innate/static-barriers.py check"
echo "   Continuous:     python core/innate/static-barriers.py monitor"
echo ""
echo "Web interfaces:"
echo "   Immune Hub:     http://localhost:4000/health"
echo "   Ollama API:     http://localhost:11434/api/tags"
echo ""
echo "🙏 Sacred technology protection is now active."
echo "   'Be wise as serpents, gentle as doves' - Matthew 10:16"
