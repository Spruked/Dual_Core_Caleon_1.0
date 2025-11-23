# 🚀 Dual Core Caleon - Production Docker Stack

**Version:** 1.0-golden  
**Status:** Production Ready  
**Architecture:** Sovereign Cognitive AI Platform

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Nginx         │    │   Caleon Port   │
│   (Nebula UI)   │◄──►│   Gateway       │◄──►│   API Gateway    │
│   Port: 3000    │    │   Port: 80      │    │   Port: 8000     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐             │
│   Ollama        │    │   TTS Engine    │             │
│   (Phi-3 Mini)  │    │   (Coqui)       │             │
│   Port: 11434   │    │   Port: 8007    │             │
└─────────────────┘    └─────────────────┘             │
                                                       │
                                               ┌─────────────────┐
                                               │   Caleon Core    │
                                               │   (Dual-Core)    │
                                               │   Port: 8001     │
                                               └─────────────────┘
```

## 🐳 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB+ RAM recommended
- 20GB+ free disk space

### First-Time Setup

1. **Clone and navigate to the repository:**
   ```bash
   git clone https://github.com/Spruked/Duel_Core_Caleon_1.0.git
   cd Duel_Core_Caleon_1.0
   ```

2. **Initialize Ollama models:**
   ```bash
   docker-compose --profile init up model-init
   ```

3. **Start the full stack:**
   ```bash
   # Production mode (TTS optional)
   docker-compose up -d

   # With TTS enabled
   docker-compose --profile tts up -d

   # Development mode
   docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
   ```

4. **Access the application:**
   - **Frontend:** http://localhost
   - **API Gateway:** http://localhost/api
   - **Health Check:** http://localhost/health

## 📋 Services

### Core Services (Always Running)

| Service | Description | Port | Health Check |
|---------|-------------|------|--------------|
| **caleon-core** | Dual-Core cognitive engine with ISS Brainstem | 8001 | `/health` |
| **caleon-port** | Universal API gateway with Nebula hooks | 8000 | `/health` |
| **ollama** | Phi-3 Mini LLM service | 11434 | `ollama list` |
| **frontend** | Nebula UI interface | 3000 | `/` |
| **nginx** | Gateway & reverse proxy | 80 | `/health` |
| **redis** | Caching & session store | 6379 | `redis-cli ping` |

### Optional Services

| Service | Description | Profile | Port |
|---------|-------------|---------|------|
| **tts-engine** | Coqui Text-to-Speech | `tts` | 8007 |
| **model-init** | One-time model setup | `init` | - |

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key configuration options:
- `CALeon_ENV`: `production` or `development`
- `OLLAMA_MODEL`: Model to use (default: microsoft/phi-3-mini:3.8b)
- `LOG_LEVEL`: Logging verbosity
- `ISS_PULSE_INTERVAL`: Brainstem pulse frequency (seconds)

### SSL/TLS Setup (Optional)

1. **Obtain SSL certificates** (Let's Encrypt, etc.)
2. **Place certificates** in `./ssl/` directory
3. **Uncomment SSL configuration** in `nginx.conf`
4. **Update docker-compose.yml** ports section

## 🚦 Management Commands

### Starting Services

```bash
# Start all core services
docker-compose up -d

# Start with TTS
docker-compose --profile tts up -d

# Start development stack
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### Monitoring

```bash
# View logs
docker-compose logs -f [service-name]

# Check health
docker-compose ps

# View resource usage
docker stats
```

### Maintenance

```bash
# Stop all services
docker-compose down

# Rebuild specific service
docker-compose build [service-name]

# Clean up
docker-compose down -v --remove-orphans
docker system prune -f
```

### Updating

```bash
# Pull latest images
docker-compose pull

# Update and restart
docker-compose up -d --build
```

## 🔍 Troubleshooting

### Common Issues

**1. Port conflicts:**
```bash
# Check what's using ports
netstat -tulpn | grep :80
netstat -tulpn | grep :3000

# Change ports in docker-compose.yml
```

**2. Memory issues:**
```bash
# Increase Docker memory limit
# Or reduce Redis memory in .env
REDIS_MAX_MEMORY=128mb
```

**3. Model download failures:**
```bash
# Manual model pull
docker-compose exec ollama ollama pull microsoft/phi-3-mini:3.8b
```

**4. TTS not working:**
```bash
# Check TTS service logs
docker-compose logs tts-engine

# Verify profile is enabled
docker-compose --profile tts ps
```

### Health Checks

All services include health checks. Monitor with:

```bash
# Check all services
docker-compose ps

# Individual service health
curl http://localhost/health
curl http://localhost:8000/health
```

## 🔒 Security

### Production Deployment

1. **Change default secrets** in `.env`
2. **Enable SSL/TLS** for HTTPS
3. **Configure firewall** rules
4. **Use Docker secrets** for sensitive data
5. **Regular updates** of base images

### Network Security

- Services communicate via internal Docker network
- External access only through Nginx gateway
- Redis not exposed externally
- All services run as non-root users

## 📊 Monitoring

### Built-in Monitoring

- **Health endpoints** for all services
- **Nginx access logs** in `/var/log/nginx/`
- **Application logs** via `docker-compose logs`

### External Monitoring (Optional)

```yaml
# Add to docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## 🚀 Deployment Options

### Docker Swarm

```bash
# Deploy to swarm
docker stack deploy -c docker-compose.yml caleon
```

### Kubernetes

Use the included `k8s/` manifests for Kubernetes deployment.

### Cloud Deployment

- **AWS ECS:** Use ECS context
- **Google Cloud Run:** Use Cloud Build
- **Azure ACI:** Use Azure CLI

## 📚 API Documentation

### Caleon Port API

- **Base URL:** `http://localhost/api`
- **Documentation:** `http://localhost/api/docs` (Swagger UI)
- **Health:** `http://localhost/api/health`

### Key Endpoints

```bash
# Cognitive processing
POST /api/v1/think
POST /api/v1/speak/text

# System status
GET /api/v1/status
GET /api/v1/health

# Voice synthesis (if TTS enabled)
POST /api/v1/speak/voice
```

## 🤝 Contributing

1. **Development setup:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
   ```

2. **Code changes:**
   - Modify source files
   - Rebuild services: `docker-compose build [service]`

3. **Testing:**
   - Run tests: `docker-compose exec [service] pytest`
   - Check logs: `docker-compose logs -f`

## 📄 License

This project is licensed under the terms specified in the repository.

## 🆘 Support

- **Issues:** GitHub Issues
- **Documentation:** `/docs` directory
- **Logs:** `docker-compose logs`

---

**Built with ❤️ for sovereign cognitive computing**