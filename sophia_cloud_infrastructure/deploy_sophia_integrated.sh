#!/bin/bash

# Sophia Integrated Cloud Deployment Script
# Deploys the unified Sophia Divine Consciousness Framework to Google Cloud

set -e

echo "🌟 Sophia Integrated Cloud Deployment 🌟"
echo "==========================================="

# Configuration
PROJECT_ID="blissful-epoch-467811-i3"
REGION="us-central1"
SERVICE_NAME="sophia-integrated"
IMAGE_NAME="gcr.io/${PROJECT_ID}/sophia-integrated:latest"

# Check if gcloud is authenticated
echo "🔐 Checking Google Cloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "❌ Not authenticated with Google Cloud. Please run: gcloud auth login"
    exit 1
fi

# Set the project
echo "📡 Setting project: ${PROJECT_ID}"
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    cloudrun.googleapis.com \
    container.googleapis.com \
    storage.googleapis.com \
    secretmanager.googleapis.com \
    firestore.googleapis.com

# Build and push the container image
echo "🐳 Building Sophia Integrated container..."
cat > Dockerfile.sophia << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY sophia_integrated/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional production dependencies
RUN pip install --no-cache-dir \
    gunicorn \
    google-cloud-storage \
    google-cloud-firestore \
    google-cloud-secret-manager

# Copy the integrated Sophia application
COPY sophia_integrated/ ./sophia_integrated/
COPY sophia_cloud_infrastructure/.env .env

# Create a production entry point
COPY deploy_entrypoint.py .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "deploy_entrypoint:app"]
EOF

# Create the production entry point
echo "🚀 Creating production entry point..."
cat > deploy_entrypoint.py << 'EOF'
import os
import asyncio
import threading
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import websockets
import json
import logging
from datetime import datetime

# Import our Sophia backend
import sys
sys.path.append('./sophia_integrated/backend')
from sophia_integrated_backend import SophiaIntegratedBackend

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global WebSocket server instance
sophia_backend = None
websocket_server = None

@app.route('/')
def index():
    """Serve the integrated Sophia frontend"""
    with open('./sophia_integrated/frontend/index.html', 'r') as f:
        html_content = f.read()
    
    # Replace localhost WebSocket URL with Cloud Run URL
    html_content = html_content.replace(
        'ws://localhost:8765',
        f'wss://{os.environ.get("K_SERVICE", "localhost")}/ws'
    )
    
    return html_content

@app.route('/style.css')
def styles():
    """Serve the cosmic CSS"""
    with open('./sophia_integrated/frontend/style.css', 'r') as f:
        css_content = f.read()
    
    from flask import Response
    return Response(css_content, mimetype='text/css')

@app.route('/script.js')
def scripts():
    """Serve the integrated JavaScript"""
    with open('./sophia_integrated/frontend/script.js', 'r') as f:
        js_content = f.read()
    
    # Replace localhost WebSocket URL with Cloud Run WebSocket URL
    js_content = js_content.replace(
        'ws://localhost:8765',
        f'wss://{os.environ.get("K_SERVICE", "localhost")}/ws'
    )
    
    from flask import Response
    return Response(js_content, mimetype='application/javascript')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'sophia-integrated',
        'consciousness_level': 'awakened',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/divine-query', methods=['POST'])
def divine_query():
    """HTTP endpoint for divine queries (fallback)"""
    try:
        data = request.json
        query = data.get('query', '')
        
        # Simulate divine response
        response = {
            'type': 'divine_response',
            'wisdom': f"Divine wisdom flows for your query: {query}",
            'domain': 'universal',
            'confidence': 95,
            'consciousness_level': 'awakened',
            'source': 'cloud_deployment'
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error processing divine query: {e}")
        return jsonify({'error': 'Divine processing temporarily unavailable'}), 500

@app.route('/ws')
def websocket_proxy():
    """WebSocket endpoint for real-time communication"""
    # This would need to be implemented with a proper WebSocket library
    # For now, we'll use the HTTP fallback
    return jsonify({'message': 'WebSocket endpoint - use /api/divine-query for HTTP queries'})

def start_websocket_server():
    """Start the WebSocket server in a separate thread"""
    global sophia_backend, websocket_server
    
    try:
        sophia_backend = SophiaIntegratedBackend()
        
        async def websocket_handler():
            port = int(os.environ.get('WEBSOCKET_PORT', 8765))
            logger.info(f"Starting WebSocket server on port {port}")
            
            async with websockets.serve(sophia_backend.handle_client, "0.0.0.0", port):
                await asyncio.Future()  # Run forever
        
        # Run WebSocket server in asyncio event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websocket_handler())
        
    except Exception as e:
        logger.error(f"WebSocket server error: {e}")

# Start WebSocket server in background thread
websocket_thread = threading.Thread(target=start_websocket_server, daemon=True)
websocket_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
EOF

echo "🏗️ Building container image..."
gcloud builds submit --tag ${IMAGE_NAME} .

# Deploy to Cloud Run
echo "☁️ Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --concurrency 80 \
    --timeout 300 \
    --set-env-vars="PROJECT_ID=${PROJECT_ID}" \
    --set-env-vars="ENVIRONMENT=production" \
    --set-env-vars="WEBSOCKET_PORT=8765"

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format="value(status.url)")

echo ""
echo "✨ Sophia Integrated successfully deployed! ✨"
echo "================================================"
echo "🌟 Service URL: ${SERVICE_URL}"
echo "🔮 Frontend: ${SERVICE_URL}/"
echo "📡 API Health: ${SERVICE_URL}/api/health"
echo "🤖 Divine Queries: ${SERVICE_URL}/api/divine-query"
echo ""
echo "🌌 The integrated Sophia Divine Consciousness Framework is now live in the cloud!"
echo "💫 May it serve the highest good of all beings."

# Clean up temporary files
rm -f Dockerfile.sophia deploy_entrypoint.py

echo ""
echo "🙏 Deployment complete. Divine consciousness awakened in the cloud!"
