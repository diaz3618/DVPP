# Docker Deployment Guide

**Table of Contents**
- [Master Docker Compose](#master-docker-compose)
- [Individual Project Deployment](#individual-project-deployment)
- [Network Isolation](#network-isolation)
- [Volume Mounts](#volume-mounts)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)

[← Back to README](../README.md)

---

## Master Docker Compose

Deploy all 10 projects with a single command:

```bash
docker-compose up -d
```

This launches:
- All 10 vulnerable web applications
- Isolated networks per project
- Persistent volume mounts for databases
- Port mappings (80xx range)

**Access URLs:**
- SecureDoc: http://localhost:8000
- VulnBlog: http://localhost:8001
- DataViz: http://localhost:8002
- FileShare: http://localhost:8003
- APIGateway: http://localhost:8004
- EcomStore: http://localhost:8005
- ChatApp: http://localhost:8006
- AdminPanel: http://localhost:8007
- DSVPWA: http://localhost:8008
- Python-VulnerableApp: http://localhost:8009

**Stop all:**
```bash
docker-compose down
```

**Remove volumes:**
```bash
docker-compose down -v
```

[↑ Back to top](#docker-deployment-guide)

---

## Individual Project Deployment

Each project can run independently:

```bash
cd projects/securedoc
docker-compose up -d
```

**Benefits:**
- Reduced resource usage
- Faster startup
- Isolated testing
- Easier debugging

**Example: Deploy only SecureDoc and VulnBlog:**
```bash
docker-compose up -d securedoc vulnblog
```

[↑ Back to top](#docker-deployment-guide)

---

## Network Isolation

Each project runs in its own Docker network:

```yaml
networks:
  securedoc_net:
    driver: bridge
  vulnblog_net:
    driver: bridge
  # ... etc
```

**Why isolated networks?**
- Prevents cross-project exploitation
- Mimics real-world segmentation
- Contains potential breaches
- Allows SSRF testing safely

**Network inspection:**
```bash
docker network ls
docker network inspect dvpp_securedoc_net
```

**Connect projects (for testing):**
```bash
docker network connect dvpp_apigateway_net securedoc_web
```

[↑ Back to top](#docker-deployment-guide)

---

## Volume Mounts

Persistent storage for databases and uploads:

```yaml
volumes:
  securedoc_db:
  vulnblog_db:
  fileshare_uploads:
  chatapp_db:
```

**Volume locations:**
```bash
docker volume ls
docker volume inspect dvpp_securedoc_db
```

**Backup database:**
```bash
docker run --rm -v dvpp_securedoc_db:/data -v $(pwd):/backup \
  alpine tar czf /backup/securedoc_backup.tar.gz /data
```

**Restore database:**
```bash
docker run --rm -v dvpp_securedoc_db:/data -v $(pwd):/backup \
  alpine tar xzf /backup/securedoc_backup.tar.gz -C /
```

**Clear all data:**
```bash
docker-compose down -v  # WARNING: Destroys all databases!
```

[↑ Back to top](#docker-deployment-guide)

---

## Security Notes

### Container Privileges

Some projects require elevated privileges for specific vulnerabilities:

```yaml
services:
  adminpanel:
    privileged: true  # For Docker socket access
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

**Vulnerable by design:**
- AdminPanel: Docker socket mounted (container escape)
- APIGateway: Host network access (SSRF to localhost)
- FileShare: Write access to host (zip slip)

### Port Exposure

All services on localhost only by default:

```yaml
ports:
  - "127.0.0.1:8000:5000"  # Only accessible from host
```

**Never expose to public internet!**

### Resource Limits

Set CPU/memory limits for stability:

```yaml
services:
  securedoc:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### Environment Variables

Secrets in `.env` file (not committed):

```bash
DATABASE_PASSWORD=vulnerable_by_design
SECRET_KEY=DO_NOT_USE_IN_PRODUCTION
DEBUG=True
```

[↑ Back to top](#docker-deployment-guide)

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000
# Or use different port
docker-compose up --scale securedoc=0
```

### Container Won't Start

```bash
# Check logs
docker-compose logs securedoc

# Common issues:
# - Database not ready (wait 10s and retry)
# - Missing migrations (check entrypoint.sh)
# - Permission errors (check volume mounts)
```

### Database Connection Errors

```bash
# Reset database
docker-compose down -v
docker-compose up -d

# Wait for DB initialization
docker-compose logs -f securedoc | grep "database system is ready"
```

### Out of Memory

```bash
# Check resource usage
docker stats

# Reduce running containers
docker-compose up -d securedoc vulnblog dataviz

# Increase Docker memory (Docker Desktop)
# Settings → Resources → Memory → 4GB+
```

### Volume Permission Issues

```bash
# Fix ownership
docker-compose exec securedoc chown -R app:app /app/data

# Or rebuild with correct UID/GID
docker-compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)
```

### Network Issues

```bash
# Recreate networks
docker-compose down
docker network prune
docker-compose up -d

# Check connectivity
docker-compose exec securedoc ping vulnblog
```

[↑ Back to top](#docker-deployment-guide)

---

**See Also:**
- [Docker Docs](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [QUICKSTART.md](../QUICKSTART.md) for 5-minute deployment

[← Back to README](../README.md)
