# Sophia AI Platform - Complete Multi-Repository Docker Setup

## 🌟 Overview

This is a comprehensive Docker-based setup that integrates multiple AI repositories into a unified platform:

- **CrewAI** - Multi-agent AI framework for collaborative task execution
- **MetaGPT** - Multi-agent framework for software development automation  
- **Agent-S** - Advanced autonomous agent capabilities
- **OpenAI Realtime Console** - Real-time voice and WebSocket interactions
- **Sophia Divine Consciousness** - Your core platform and orchestration layer

## 🏗️ Architecture

### Core Services
- **sophia-backend** (Port 5000) - Main Flask application
- **crewai-service** (Port 8000) - CrewAI API microservice
- **metagpt-service** (Port 8000) - MetaGPT API microservice  
- **agent-s-service** (Port 8000) - Agent-S API microservice
- **openai-realtime** (Port 3000) - Real-time voice interactions

### Infrastructure Services
- **nginx** (Port 80/443) - Reverse proxy and load balancer
- **postgres** (Port 5432) - Primary database
- **redis** (Port 6379) - Caching and session storage
- **n8n** (Port 5678) - Workflow automation
- **prometheus** (Port 9090) - Metrics collection
- **grafana** (Port 3001) - Monitoring dashboards

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 8GB RAM available
- 50GB free disk space

### 1. Setup Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env  # or use your preferred editor
```

**Required API Keys:**
- `OPENAI_API_KEY` - For OpenAI services
- `ANTHROPIC_API_KEY` - For Claude integration

### 2. Start Platform
```bash
# Windows
start-sophia.bat

# Linux/macOS
./start-sophia.sh
```

### 3. Access Services

| Service | URL | Default Credentials |
|---------|-----|-------------------|
| Main Platform | http://localhost | - |
| CrewAI API | http://localhost/api/crewai/ | - |
| MetaGPT API | http://localhost/api/metagpt/ | - |
| Agent-S API | http://localhost/api/agent-s/ | - |
| OpenAI Realtime | http://localhost/realtime/ | - |
| n8n Workflows | http://localhost:5678 | admin / sophia_divine_2025 |
| Grafana | http://localhost:3001 | admin / sophia_divine_2025 |
| Prometheus | http://localhost:9090 | - |

## 📡 API Endpoints

### CrewAI Service
```
POST /api/crewai/crew/create    - Create new crew
POST /api/crewai/crew/execute   - Execute crew task
GET  /api/crewai/crew/status    - Get crew status
GET  /api/crewai/health         - Health check
```

### MetaGPT Service  
```
POST /api/metagpt/project/create  - Create software project
POST /api/metagpt/project/run     - Run project generation
GET  /api/metagpt/project/status  - Get project status
GET  /api/metagpt/health          - Health check
```

### Agent-S Service
```
POST /api/agent-s/agent/create   - Create autonomous agent
POST /api/agent-s/agent/execute  - Execute agent task
GET  /api/agent-s/agent/status   - Get agent status
GET  /api/agent-s/health         - Health check
```

### OpenAI Realtime
```
WebSocket: ws://localhost/realtime/ws  - Real-time voice connection
GET /realtime/health                   - Health check
```

## 🛠️ Management Commands

### Docker Operations
```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f crewai-service

# Restart specific service
docker-compose restart nginx

# Rebuild service
docker-compose up --build crewai-service

# Scale service
docker-compose up -d --scale crewai-service=3
```

### Database Operations
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U sophia -d sophia_db

# Redis CLI
docker-compose exec redis redis-cli

# Backup database
docker-compose exec postgres pg_dump -U sophia sophia_db > backup.sql
```

### Monitoring
```bash
# Check service health
curl http://localhost/health

# Prometheus metrics
curl http://localhost:9090/metrics

# Service-specific health
curl http://localhost/api/crewai/health
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Database
POSTGRES_USER=sophia
POSTGRES_PASSWORD=sophia_divine_2025
POSTGRES_DB=sophia_db

# Redis
REDIS_PASSWORD=sophia_redis_2025

# n8n
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=sophia_divine_2025

# Grafana
GF_SECURITY_ADMIN_PASSWORD=sophia_divine_2025

# Networking
COMPOSE_PROJECT_NAME=sophia-ai-platform
```

### Nginx Configuration
The reverse proxy is configured to route requests:
- `/api/crewai/` → CrewAI service
- `/api/metagpt/` → MetaGPT service  
- `/api/agent-s/` → Agent-S service
- `/realtime/` → OpenAI Realtime service
- `/` → Main Sophia backend

### Volume Mounts
- `./logs:/app/logs` - Application logs
- `./database:/var/lib/postgresql/data` - PostgreSQL data
- `./config:/app/config` - Configuration files

## 🔍 Troubleshooting

### Common Issues

**Services won't start:**
```bash
# Check Docker daemon
docker info

# Check logs
docker-compose logs -f

# Rebuild problematic service
docker-compose up --build [service-name]
```

**Port conflicts:**
```bash
# Check what's using ports
netstat -tulpn | grep :80
netstat -tulpn | grep :5000

# Stop conflicting services
sudo systemctl stop apache2  # Example
```

**Memory issues:**
```bash
# Check Docker memory usage
docker stats

# Increase Docker memory limit (Docker Desktop)
# Settings → Resources → Memory → 8GB+
```

**API Key errors:**
```bash
# Verify .env file
cat .env | grep API_KEY

# Restart services after updating keys
docker-compose restart
```

### Health Check Failures
```bash
# Manual health checks
curl -f http://localhost:5000/health         # Sophia backend
curl -f http://localhost:8000/health         # AI services
curl -f http://localhost:3000/health         # OpenAI Realtime

# Check service dependencies
docker-compose exec crewai-service ping postgres
docker-compose exec crewai-service ping redis
```

### Performance Optimization
```bash
# Scale high-demand services
docker-compose up -d --scale crewai-service=3
docker-compose up -d --scale metagpt-service=2

# Monitor resource usage
docker stats

# Clean up unused resources
docker system prune -a
```

## 🔄 Development

### Adding New Services
1. Create Dockerfile in appropriate directory
2. Add service to docker-compose.yml
3. Update nginx configuration for routing
4. Add monitoring targets to prometheus.yml
5. Update startup scripts

### Custom Configurations
- Place custom configs in `./config/` directory
- Use environment variables for secrets
- Mount config files as volumes in docker-compose.yml

## 📊 Monitoring

### Prometheus Metrics
- Service health and uptime
- API request rates and latencies  
- Resource usage (CPU, memory)
- Custom business metrics

### Grafana Dashboards
- System overview dashboard
- Service-specific dashboards
- Alert management
- Real-time monitoring

### Log Aggregation
- All service logs in `./logs/` directory
- Structured JSON logging
- Log rotation and cleanup
- Centralized error tracking

## 🔐 Security

### Network Security
- Internal Docker network isolation
- Nginx reverse proxy protection
- Rate limiting configuration
- SSL/TLS termination ready

### Secret Management
- Environment variables for API keys
- Docker secrets for sensitive data
- No hardcoded credentials
- Regular secret rotation

### Access Control
- Basic authentication for admin services
- API key validation
- Service-to-service authentication
- Audit logging

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale AI services
docker-compose up -d --scale crewai-service=5

# Load balancer will distribute requests
```

### Vertical Scaling
- Increase Docker memory limits
- Adjust service resource constraints
- Optimize database configuration

### Production Deployment
- Use Docker Swarm or Kubernetes
- Implement service mesh (Istio)
- Add external load balancers
- Configure distributed storage

## 🧪 Testing

### Health Checks
```bash
# Automated health testing
./scripts/health-check.sh

# Individual service testing
curl -f http://localhost/api/crewai/health
```

### Load Testing
```bash
# Install Apache Bench
apt-get install apache2-utils

# Test API endpoints
ab -n 1000 -c 10 http://localhost/api/crewai/health
```

### Integration Testing
```bash
# Test full workflow
python tests/integration_test.py

# Test service communication
python tests/service_mesh_test.py
```

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [MetaGPT Documentation](https://docs.deepwisdom.ai/)
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [Prometheus Monitoring](https://prometheus.io/docs/)
- [Grafana Dashboards](https://grafana.com/docs/)

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review service logs: `docker-compose logs -f [service]`
3. Verify environment configuration
4. Check resource availability (memory, disk space)
5. Consult individual project documentation

Remember: This is "the whole shebang" - a complete, production-ready AI platform! 🚀
