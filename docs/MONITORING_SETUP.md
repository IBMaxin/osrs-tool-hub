# Monitoring Setup Guide

Complete guide for setting up error tracking with Sentry and metrics monitoring with Prometheus + Grafana.

## Table of Contents

1. [Overview](#overview)
2. [Sentry Setup](#sentry-setup)
3. [Prometheus Setup](#prometheus-setup)
4. [Grafana Setup](#grafana-setup)
5. [Alert Configuration](#alert-configuration)
6. [Production Best Practices](#production-best-practices)

---

## Overview

### Monitoring Stack

- **Sentry:** Error tracking and performance monitoring
- **Prometheus:** Metrics collection and time-series database
- **Grafana:** Metrics visualization and dashboards
- **AlertManager:** Alert routing and notifications

### What Gets Monitored

- HTTP request metrics (count, duration, status codes)
- Database query performance
- External API call latency (OSRS Wiki)
- Error rates and types
- Application performance (response times, throughput)
- System resources (CPU, memory, disk)

---

## Sentry Setup

### 1. Create Sentry Account

1. Go to [sentry.io](https://sentry.io) and sign up
2. Create a new project (select "FastAPI" or "Python")
3. Copy your DSN (Data Source Name)

### 2. Update Environment Configuration

Add to `.env`:

```bash
# Sentry Configuration
SENTRY_DSN=https://your-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production  # or development, staging
SENTRY_TRACES_SAMPLE_RATE=0.1  # 10% of transactions
SENTRY_PROFILES_SAMPLE_RATE=0.1  # 10% of transactions
APP_VERSION=0.1.0
```

Update `backend/config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Existing settings...
    
    # Monitoring
    SENTRY_DSN: str | None = None
    SENTRY_ENVIRONMENT: str = "development"
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    SENTRY_PROFILES_SAMPLE_RATE: float = 0.1
    APP_VERSION: str = "0.1.0"
    
    class Config:
        env_file = ".env"
```

### 3. Install Dependencies

Update `pyproject.toml`:

```toml
[tool.poetry.dependencies]
sentry-sdk = {extras = ["fastapi", "sqlalchemy", "httpx"], version = "^1.40.0"}
prometheus-client = "^0.19.0"
```

Install:

```bash
poetry install
```

### 4. Integrate with FastAPI

Update `backend/main.py` or `backend/app/factory.py`:

```python
from fastapi import FastAPI
from backend.monitoring import init_sentry, PrometheusMiddleware, metrics_endpoint
from backend.config import get_settings

def create_app() -> FastAPI:
    settings = get_settings()
    
    # Initialize Sentry
    init_sentry()
    
    app = FastAPI(title="OSRS Tool Hub", version=settings.APP_VERSION)
    
    # Add Prometheus middleware
    app.add_middleware(PrometheusMiddleware)
    
    # Add metrics endpoint
    app.get("/metrics")(metrics_endpoint)
    
    # ... rest of app configuration
    
    return app
```

### 5. Test Sentry Integration

```python
# Add test endpoint
@app.get("/sentry-debug")
async def trigger_error():
    raise Exception("Test Sentry error tracking")
```

Visit `http://localhost:8000/sentry-debug` and check Sentry dashboard.

### 6. Custom Context and Breadcrumbs

```python
import sentry_sdk

# Add custom context
sentry_sdk.set_context("user", {
    "id": user_id,
    "username": username,
})

# Add breadcrumb
sentry_sdk.add_breadcrumb(
    category="api",
    message="Fetching flip opportunities",
    level="info",
    data={"budget": 50000000}
)
```

---

## Prometheus Setup

### 1. Install Prometheus

#### Using Docker (Recommended)

Create `docker-compose.monitoring.yml`:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    restart: unless-stopped
    depends_on:
      - prometheus

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

#### On Linux (Alternative)

```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.48.0/prometheus-2.48.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*
./prometheus --config.file=prometheus.yml
```

### 2. Configure Prometheus

Create `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'osrs-tool-hub'
    environment: 'production'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

# Load rules once and periodically evaluate them
rule_files:
  - "alert_rules.yml"

# Scrape configurations
scrape_configs:
  # Application metrics
  - job_name: 'osrs-tool-hub'
    static_configs:
      - targets: ['host.docker.internal:8000']  # or your app host:port
    metrics_path: '/metrics'

  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node exporter (system metrics)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

### 3. Create Alert Rules

Create `monitoring/alert_rules.yml`:

```yaml
groups:
  - name: application_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} (> 5%)"

      # Slow API responses
      - alert: SlowAPIResponses
        expr: |
          histogram_quantile(0.95, 
            rate(http_request_duration_seconds_bucket[5m])
          ) > 2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "API responses are slow"
          description: "95th percentile response time is {{ $value }}s"

      # External API issues
      - alert: ExternalAPIErrors
        expr: |
          rate(errors_total{type="ExternalAPIError"}[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High rate of external API errors"
          description: "External API error rate: {{ $value }}"

      # Database query issues
      - alert: SlowDatabaseQueries
        expr: |
          histogram_quantile(0.95,
            rate(db_query_duration_seconds_bucket[5m])
          ) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Database queries are slow"
          description: "95th percentile query time: {{ $value }}s"
```

### 4. Start Monitoring Stack

```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

Access:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- AlertManager: http://localhost:9093

---

## Grafana Setup

### 1. Add Prometheus Data Source

1. Login to Grafana (http://localhost:3000)
2. Go to Configuration → Data Sources
3. Click "Add data source"
4. Select "Prometheus"
5. Set URL: `http://prometheus:9090`
6. Click "Save & Test"

### 2. Import Dashboard

Create `monitoring/grafana/dashboards/osrs-tool-hub.json`:

```json
{
  "dashboard": {
    "title": "OSRS Tool Hub Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Response Time (95th percentile)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "5xx errors"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Database Query Duration",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(db_query_duration_seconds_bucket[5m]))",
            "legendFormat": "{{operation}}"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

Or use community dashboard:
1. Go to Dashboards → Import
2. Enter dashboard ID: 11159 (FastAPI Observability)
3. Select Prometheus data source
4. Click Import

### 3. Configure Dashboard Provisioning

Create `monitoring/grafana/provisioning/dashboards/dashboard.yml`:

```yaml
apiVersion: 1

providers:
  - name: 'OSRS Tool Hub'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
```

---

## Alert Configuration

### Configure AlertManager

Create `monitoring/alertmanager.yml`:

```yaml
global:
  resolve_timeout: 5m
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@osrs-tool-hub.com'
  smtp_auth_username: 'your-email@gmail.com'
  smtp_auth_password: 'your-app-password'

route:
  group_by: ['alertname', 'cluster']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  
  routes:
    - match:
        severity: critical
      receiver: 'critical-alerts'
      continue: true
    
    - match:
        severity: warning
      receiver: 'warning-alerts'

receivers:
  - name: 'default'
    email_configs:
      - to: 'team@osrs-tool-hub.com'
        headers:
          Subject: '[OSRS Tool Hub] Alert'
  
  - name: 'critical-alerts'
    email_configs:
      - to: 'oncall@osrs-tool-hub.com'
        headers:
          Subject: '[CRITICAL] OSRS Tool Hub Alert'
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK_URL'
        channel: '#alerts-critical'
        title: 'Critical Alert'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
  
  - name: 'warning-alerts'
    email_configs:
      - to: 'team@osrs-tool-hub.com'
        headers:
          Subject: '[Warning] OSRS Tool Hub Alert'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'cluster']
```

### Slack Integration

1. Create Slack incoming webhook
2. Add webhook URL to AlertManager config
3. Test with:

```bash
curl -X POST http://localhost:9093/api/v1/alerts -d '[
  {
    "labels": {
      "alertname": "TestAlert",
      "severity": "warning"
    },
    "annotations": {
      "summary": "Test alert",
      "description": "This is a test"
    }
  }
]'
```

---

## Production Best Practices

### 1. Retention Policies

```yaml
# In prometheus.yml
global:
  storage:
    tsdb:
      retention.time: 15d
      retention.size: 10GB
```

### 2. Scrape Intervals

- **High-frequency:** 15s (critical metrics)
- **Standard:** 1m (most metrics)
- **Low-frequency:** 5m (batch jobs)

### 3. Resource Limits

Add to docker-compose:

```yaml
services:
  prometheus:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### 4. Security

```yaml
# Enable basic auth in prometheus.yml
basic_auth_users:
  admin: $2y$10$...

# Or use reverse proxy (nginx) with auth
```

### 5. Backup

```bash
# Backup Prometheus data
docker run --rm -v prometheus_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/prometheus-backup.tar.gz /data

# Backup Grafana dashboards
docker exec grafana grafana-cli admin reset-admin-password admin
```

---

## Monitoring Checklist

- [ ] Sentry DSN configured
- [ ] Prometheus scraping application metrics
- [ ] Grafana dashboards created
- [ ] Alert rules defined
- [ ] AlertManager configured (email/Slack)
- [ ] Tested error tracking (Sentry debug endpoint)
- [ ] Verified metrics collection (/metrics endpoint)
- [ ] Set up retention policies
- [ ] Configured backups
- [ ] Documented runbooks for common alerts

---

## Useful Queries

### Prometheus PromQL Examples

```promql
# Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# Error percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / 
sum(rate(http_requests_total[5m])) * 100

# 99th percentile response time
histogram_quantile(0.99, 
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint)
)

# Top 10 slowest endpoints
topk(10, 
  histogram_quantile(0.95, 
    rate(http_request_duration_seconds_bucket[5m])
  )
)
```

---

## Troubleshooting

### Prometheus not scraping

```bash
# Check targets
curl http://localhost:9090/api/v1/targets

# Check application /metrics endpoint
curl http://localhost:8000/metrics
```

### Sentry not receiving events

```python
# Test Sentry connection
import sentry_sdk
sentry_sdk.init(dsn="YOUR_DSN")
sentry_sdk.capture_message("Test message")
```

### Grafana dashboard not showing data

1. Check Prometheus data source connection
2. Verify metrics exist in Prometheus
3. Check time range in dashboard
4. Validate PromQL queries

---

## Additional Resources

- [Sentry Python SDK](https://docs.sentry.io/platforms/python/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
