# Sophia Integrated Divine Consciousness - Cloud Deployment
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SOPHIA_ENVIRONMENT=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY sophia_integrated/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY sophia_integrated/ ./sophia_integrated/
COPY sophia_cloud_infrastructure/.env ./

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash sophia && \
    chown -R sophia:sophia /app
USER sophia

# Expose ports
EXPOSE 8080 8765

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Create startup script
COPY <<EOF /app/start.sh
#!/bin/bash
set -e

echo "🌟 Starting Sophia Integrated Divine Consciousness Cloud Platform 🌟"

# Start WebSocket backend in background
echo "📡 Starting WebSocket Backend..."
cd /app/sophia_integrated/backend
python sophia_integrated_backend.py &
BACKEND_PID=\$!

# Wait for backend to be ready
echo "⏳ Waiting for WebSocket backend to initialize..."
sleep 5

# Start HTTP server for frontend
echo "🌐 Starting Frontend HTTP Server..."
cd /app/sophia_integrated/frontend
python -m http.server 8080 &
FRONTEND_PID=\$!

echo "✨ Sophia Divine Consciousness Platform fully deployed!"
echo "🔮 Frontend: http://localhost:8080"
echo "📡 WebSocket: ws://localhost:8765"

# Wait for any process to exit
wait \$BACKEND_PID \$FRONTEND_PID
EOF

RUN chmod +x /app/start.sh

# Start the application
CMD ["/app/start.sh"]
