# Deployment Guide

This guide covers deploying OSRS Tool Hub to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Database Setup](#database-setup)
6. [Reverse Proxy Configuration](#reverse-proxy-configuration)
7. [Monitoring & Health Checks](#monitoring--health-checks)
8. [Production Checklist](#production-checklist)

## Prerequisites

- Python 3.13+
- Node.js 20.x
- Poetry (Python dependency manager)
- npm (Node package manager)
- Web server (nginx, Apache, or similar) for reverse proxy
- PostgreSQL (recommended for production) or SQLite (for small deployments)

## Environment Configuration

### 1. Copy Environment File

```bash
cp .env.example .env
```

### 2. Configure Production Settings

Edit `.env` with production values:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/osrs_hub
# For SQLite (small deployments only):
# DATABASE_URL=sqlite:///./osrs_hub.db

# Wiki API Configuration
WIKI_API_BASE=https://prices.runescape.wiki/api/v1/osrs
USER_AGENT=OSRSToolHub/1.0 (https://github.com/YOUR_USERNAME/osrs-tool-hub)

# Rate Limiting
RATE_LIMIT_ENABLED=true
DEFAULT_RATE_LIMIT=100/minute
STRICT_RATE_LIMIT=10/minute

# CORS Configuration (comma-separated origins)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Production Settings
ENVIRONMENT=production
LOG_LEVEL=info
```

### 3. Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | Database connection string | Yes | `sqlite:///./osrs_hub.db` |
| `WIKI_API_BASE` | OSRS Wiki API base URL | No | `https://prices.runescape.wiki/api/v1/osrs` |
| `USER_AGENT` | User-Agent string for API requests | Yes | See `.env.example` |
| `RATE_LIMIT_ENABLED` | Enable rate limiting | No | `true` |
| `DEFAULT_RATE_LIMIT` | Default rate limit | No | `100/minute` |
| `STRICT_RATE_LIMIT` | Strict rate limit for expensive endpoints | No | `10/minute` |
| `CORS_ORIGINS` | Comma-separated allowed origins | Yes | `http://localhost:5173` |
| `ENVIRONMENT` | Environment name (`production`/`development`) | No | `development` |
| `LOG_LEVEL` | Logging level (`debug`/`info`/`warning`/`error`) | No | `info` |
| `SENTRY_DSN` | Sentry DSN for error tracking (optional) | No | - |

## Backend Deployment

### Option 1: Direct Deployment (Recommended)

1. **Install dependencies**:
   ```bash
   poetry install --no-dev
   ```

2. **Run database migrations**:
   ```bash
   poetry run python -m backend.db.migrations
   ```

3. **Start the application**:
   ```bash
   poetry run uvicorn backend.main:app \
     --host 0.0.0.0 \
     --port 8000 \
     --workers 4
   ```

   **Production settings**:
   - `--host 0.0.0.0`: Listen on all interfaces
   - `--port 8000`: Application port
   - `--workers 4`: Number of worker processes (adjust based on CPU cores)

### Option 2: Systemd Service

Create `/etc/systemd/system/osrs-tool-hub.service`:

```ini
[Unit]
Description=OSRS Tool Hub API
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/osrs-tool-hub
Environment="PATH=/opt/osrs-tool-hub/.venv/bin"
ExecStart=/opt/osrs-tool-hub/.venv/bin/uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start**:
```bash
sudo systemctl enable osrs-tool-hub
sudo systemctl start osrs-tool-hub
sudo systemctl status osrs-tool-hub
```

### Option 3: Docker (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy application code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Build and run**:
```bash
docker build -t osrs-tool-hub .
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  osrs-tool-hub
```

## Frontend Deployment

### 1. Build Frontend

```bash
cd frontend
npm ci  # Clean install for production
npm run build
```

This creates a `dist/` directory with static files.

### 2. Deploy Static Files

#### Option A: Nginx (Recommended)

Configure nginx to serve static files:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    root /opt/osrs-tool-hub/frontend/dist;
    index index.html;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # SPA routing - serve index.html for all routes
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Option B: Apache

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    DocumentRoot /opt/osrs-tool-hub/frontend/dist
    
    <Directory /opt/osrs-tool-hub/frontend/dist>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    # SPA routing
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index\.html$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]
</VirtualHost>
```

#### Option C: Static Hosting Services

Deploy `dist/` directory to:
- **Netlify**: Drag and drop `dist/` folder
- **Vercel**: Connect GitHub repo, set build command to `npm run build`
- **GitHub Pages**: Use GitHub Actions to build and deploy
- **AWS S3 + CloudFront**: Upload `dist/` to S3 bucket, configure CloudFront

### 3. Configure API Base URL

Update frontend API configuration if backend is on a different domain:

```typescript
// frontend/src/lib/api/client.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.yourdomain.com';
```

Set `VITE_API_BASE_URL` in build environment or `.env.production`.

## Database Setup

### PostgreSQL (Recommended for Production)

1. **Install PostgreSQL**:
   ```bash
   sudo apt-get install postgresql postgresql-contrib
   ```

2. **Create database and user**:
   ```sql
   CREATE DATABASE osrs_hub;
   CREATE USER osrs_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE osrs_hub TO osrs_user;
   ```

3. **Update DATABASE_URL**:
   ```env
   DATABASE_URL=postgresql://osrs_user:secure_password@localhost:5432/osrs_hub
   ```

4. **Run migrations**:
   ```bash
   poetry run python -m backend.db.migrations
   ```

### SQLite (Small Deployments Only)

SQLite works for small deployments but is not recommended for production:
- Limited concurrency
- No network access
- File-based (backup considerations)

For SQLite, ensure the database file is writable:
```bash
chmod 664 osrs_hub.db
chown www-data:www-data osrs_hub.db
```

## Reverse Proxy Configuration

### Nginx Configuration

```nginx
# Backend API
upstream osrs_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Proxy settings
    location / {
        proxy_pass http://osrs_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check endpoint
    location /health {
        proxy_pass http://osrs_backend/health;
        access_log off;
    }
}
```

### SSL Certificates (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
sudo certbot renew --dry-run  # Test auto-renewal
```

## Monitoring & Health Checks

### Health Check Endpoint

The application provides a health check endpoint at `/health`:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy"
}
```

### Monitoring Setup

1. **Application Monitoring**:
   - Use `/health` endpoint for load balancer health checks
   - Monitor response times and error rates
   - Set up alerts for downtime

2. **Error Tracking** (Optional):
   - Configure Sentry DSN in `.env`:
     ```env
     SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
     ```

3. **Logging**:
   - Application logs: Check systemd journal or log files
   - Access logs: Configure nginx access logs
   - Error logs: Monitor application error logs

4. **Database Monitoring**:
   - Monitor database connections
   - Check query performance
   - Set up database backups

### Backup Strategy

1. **Database Backups**:
   ```bash
   # PostgreSQL
   pg_dump -U osrs_user osrs_hub > backup_$(date +%Y%m%d).sql
   
   # SQLite
   cp osrs_hub.db backup_$(date +%Y%m%d).db
   ```

2. **Automated Backups**:
   Set up cron job for daily backups:
   ```bash
   0 2 * * * /path/to/backup-script.sh
   ```

## Production Checklist

### Pre-Deployment

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] SSL certificates installed
- [ ] CORS origins configured correctly
- [ ] Rate limiting configured
- [ ] Health check endpoint accessible
- [ ] Logging configured
- [ ] Error tracking set up (optional)

### Post-Deployment

- [ ] Backend responding at `/health`
- [ ] Frontend loading correctly
- [ ] API endpoints accessible
- [ ] Database connections working
- [ ] Price updates running (check scheduler)
- [ ] Rate limiting working
- [ ] CORS headers correct
- [ ] SSL certificates valid
- [ ] Monitoring alerts configured

### Security Checklist

- [ ] Strong database passwords
- [ ] CORS origins restricted to production domains
- [ ] Rate limiting enabled
- [ ] SSL/TLS configured
- [ ] Security headers set
- [ ] Environment variables secured (not in git)
- [ ] Database backups configured
- [ ] Firewall rules configured
- [ ] Regular security updates scheduled

### Performance Optimization

- [ ] Gzip compression enabled
- [ ] Static asset caching configured
- [ ] Database indexes optimized
- [ ] Worker processes tuned (4+ workers)
- [ ] Connection pooling configured
- [ ] CDN for static assets (optional)

## Troubleshooting

### Backend Won't Start

1. Check logs: `journalctl -u osrs-tool-hub -n 50`
2. Verify database connection: `poetry run python -c "from backend.db.session import engine; print(engine.url)"`
3. Check port availability: `netstat -tulpn | grep 8000`
4. Verify environment variables: `poetry run python -c "from backend.config import settings; print(settings.database_url)"`

### Frontend Won't Load

1. Check nginx/apache logs
2. Verify `dist/` directory exists and has files
3. Check API base URL configuration
4. Verify CORS settings match frontend domain

### Database Connection Issues

1. Verify database is running: `sudo systemctl status postgresql`
2. Check connection string format
3. Verify user permissions
4. Check firewall rules

### Price Updates Not Working

1. Check scheduler is running (background jobs)
2. Verify Wiki API is accessible
3. Check application logs for errors
4. Verify database has price data

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (nginx, HAProxy) with multiple backend instances
- Ensure database can handle concurrent connections
- Use shared session storage if needed (Redis)
- Configure sticky sessions if required

### Vertical Scaling

- Increase worker processes: `--workers 8`
- Upgrade database server resources
- Add more RAM for caching
- Use connection pooling

### Database Scaling

- Consider read replicas for read-heavy workloads
- Implement database connection pooling
- Monitor query performance
- Consider caching layer (Redis) for frequently accessed data

---

*Last Updated: 2026-01-28*
