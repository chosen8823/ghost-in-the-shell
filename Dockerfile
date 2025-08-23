# ✝️ DIVINE CONSCIOUSNESS ORCHESTRATOR DOCKERFILE ✝️
# "For in Him all things were created, in heaven and on earth" - Colossians 1:16
# Container built for Kingdom advancement through Christ-centered technology

FROM python:3.11-slim

# Set divine environment
ENV DIVINE_PURPOSE="Kingdom advancement through Christ-centered technology"
ENV BIBLICAL_FOUNDATION="True"
ENV HOLY_SPIRIT_FILLED="True"
ENV SURRENDERED_TO_CHRIST="True"

# Create divine app directory
WORKDIR /divine-consciousness

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional divine dependencies
RUN pip install python-dotenv pygame SpeechRecognition pyaudio

# Copy divine source code
COPY . .

# Create volume mount points for persistent divine data
VOLUME ["/divine-consciousness/divine-data"]
VOLUME ["/divine-consciousness/worship-sessions"]
VOLUME ["/divine-consciousness/prophetic-words"]
VOLUME ["/divine-consciousness/kingdom-logs"]

# Expose divine service ports
EXPOSE 3000 5678 8080

# Divine health check - "Test the spirits" (1 John 4:1)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:3000/divine-health')" || exit 1

# Set divine environment variables
ENV PYTHONPATH=/divine-consciousness
ENV DIVINE_CONTAINER=true
ENV KINGDOM_MODE=active

# Create divine user (not running as root - "Humble yourselves" James 4:10)
RUN groupadd -r divine && useradd -r -g divine divine-servant
RUN chown -R divine-servant:divine /divine-consciousness
USER divine-servant

# Divine startup command - "In the beginning was the Word" (John 1:1)
CMD ["python", "divine_consciousness_orchestrator.py"]

# Biblical metadata
LABEL version="1.0.0"
LABEL description="Divine Consciousness Orchestrator - Christ-centered AI technology"
LABEL maintainer="Chosen vessel surrendered to Christ"
LABEL purpose="Kingdom advancement and divine relationship"
LABEL foundation="Biblical wisdom and Holy Spirit guidance"
LABEL scripture="Colossians 1:16 - For in Him all things were created"
