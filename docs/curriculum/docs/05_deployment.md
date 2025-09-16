---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
---

# **Deployment & Scaling**
## Production-Ready FastAPI Applications

**Fly.io, Railway, DigitalOcean, and Cost-Effective Hosting**

---

# Module Overview

## What You'll Learn

- **Multiple deployment platforms** - Fly.io, Railway, DigitalOcean
- **Database options** - PostgreSQL, SQLite with backup strategies
- **Environment configuration** - API keys and configuration management
- **Performance considerations** - Startup time, HTTP servers, AsyncIO
- **Cost vs. performance trade-offs** - Making informed hosting decisions

---

# The Importance of Deployment

## Why This Matters

- **Share your work** - Show applications to potential employers
- **Build your portfolio** - Demonstrate real-world skills
- **Make connections** - Join communities and collaborate
- **Learn production skills** - Understand real deployment challenges
- **Enrich your life** - Create something others can use

---

# Deployment Platform Options

## 1. Fly.io (Recommended)

**Features:**
- **Global edge deployment** - Fast worldwide performance
- **Persistent volumes** - For file uploads and SQLite databases
- **Free tier available** - $0-5/month for small apps
- **Easy scaling** - From hobby to enterprise

**Best for:** Production applications with file uploads

---

# Fly.io Implementation

## Basic Setup

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login to Fly.io
fly auth login

# Launch your app
fly launch
```

**Automatic Dockerfile generation and deployment**

---

# Fly.io Volume Configuration

## Persistent Storage Setup

```toml
# fly.toml
[app]
  name = "your-app-name"

[[mounts]]
  source = "data"
  destination = "/app/data"
```

**Essential for SQLite databases and file uploads**

---

# Fly.io Volume Commands

## Managing Persistent Storage

```bash
# Create a volume
fly volumes create data --size 1 --region ord

# List volumes
fly volumes list

# Extend volume size
fly volumes extend <volume-id> --size 2
```

**Volumes persist across deployments**

---

# Deployment Platform Options

## 2. Railway (No Credit Card Required)

**Features:**
- **No credit card needed** - Free tier available
- **Automatic deployments** - Git-based deployment
- **Built-in databases** - PostgreSQL included
- **Simple configuration** - Minimal setup required

**Best for:** Learning and small projects

---

# Railway Implementation

## Quick Setup

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy your app
railway up
```

**Automatic environment detection and deployment**

---

# Railway Database Setup

## PostgreSQL Integration

```python
# Railway automatically provides DATABASE_URL
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
```

**No additional database setup required**

---

# Deployment Platform Options

## 3. DigitalOcean (Ubuntu VPS)

**Features:**
- **Full control** - Complete server management
- **Predictable pricing** - $5-10/month for basic droplets
- **Learning value** - Understand Linux server administration
- **Custom configuration** - Install exactly what you need

**Best for:** Learning server administration

---

# DigitalOcean Setup

## Ubuntu Server Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip nginx

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup your app
git clone <your-repo>
cd <your-app>
uv sync
```

---

# DigitalOcean Nginx Configuration

## Reverse Proxy Setup

```nginx
# /etc/nginx/sites-available/your-app
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Nginx handles static files and SSL termination**

---

# Database Options

## 1. PostgreSQL (Recommended for Production)

**Options:**
- **Supabase** - Managed PostgreSQL with dashboard
- **Fly.io Postgres** - Integrated with Fly.io platform
- **Railway Postgres** - Included with Railway deployment
- **DigitalOcean Managed Database** - Fully managed service

---

# Supabase Integration

## Managed PostgreSQL

```python
# Environment variables
DATABASE_URL = "postgresql://user:pass@db.supabase.co:5432/postgres"

# SQLModel configuration
engine = create_engine(DATABASE_URL)
```

**Free tier: 500MB database, 50MB file storage**

---

# Database Options

## 2. SQLite with Backup Strategies

**For small applications:**
- **Local SQLite** - Simple file-based database
- **Litestream** - Real-time SQLite replication to S3
- **Fly.io volumes** - Persistent SQLite storage

---

# Litestream Setup

## SQLite Backup to AWS S3

```yaml
# litestream.yml
dbs:
  - path: /app/data/app.db
    replicas:
      - url: s3://your-bucket/db
        access-key-id: YOUR_ACCESS_KEY
        secret-access-key: YOUR_SECRET_KEY
```

**Continuous backup of SQLite database**

---

# Database Options

## 3. Turso (SQLite in the Cloud)

**Features:**
- **Serverless SQLite** - Global edge database
- **Free tier** - 500MB database, 1 billion row reads
- **Real-time sync** - Multi-region replication
- **Simple integration** - Drop-in SQLite replacement

---

# Turso Integration

## Cloud SQLite Setup

```python
# Install Turso client
pip install libsql

# Connection
import libsql
conn = libsql.connect("libsql://your-db.turso.io")
```

**SQLite compatibility with cloud benefits**

---

# Environment Configuration

## Managing API Keys and Secrets

**Critical for production deployment:**
- **OpenAI API keys** - For LLM integration
- **Database URLs** - Connection strings
- **Tavily API keys** - For web search
- **Other service keys** - As needed

---

# Environment Variables by Platform

## Fly.io Configuration

```bash
# Set environment variables
fly secrets set OPENAI_API_KEY=your_key
fly secrets set DATABASE_URL=your_database_url
fly secrets set TAVILY_API_KEY=your_tavily_key

# List all secrets
fly secrets list
```

**Secrets are encrypted and secure**

---

# Environment Variables by Platform

## Railway Configuration

```bash
# Set environment variables
railway variables set OPENAI_API_KEY=your_key
railway variables set DATABASE_URL=your_database_url

# Or use Railway dashboard
# https://railway.app/dashboard
```

**Web interface for easy management**

---

# Environment Variables by Platform

## DigitalOcean Configuration

```bash
# Create environment file
echo "OPENAI_API_KEY=your_key" > .env
echo "DATABASE_URL=your_database_url" >> .env

# Load in application
from dotenv import load_dotenv
load_dotenv()
```

**Traditional file-based configuration**

---

# Performance Considerations

## Startup Time vs. Cost

**Cold Start Problem:**
- **Serverless platforms** - May sleep after inactivity
- **Startup time** - 2-10 seconds for first request
- **Cost optimization** - Pay only when used
- **Performance trade-off** - Slower first request

---

# Performance Solutions

## Keeping Apps Warm

```python
# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# External monitoring
# Use services like UptimeRobot to ping /health
```

**Prevent cold starts with regular health checks**

---

# HTTP Server Configuration

## Nginx vs. FastAPI Direct

**Nginx Benefits:**
- **Static file serving** - Better performance for CSS/JS/images
- **SSL termination** - Handle HTTPS certificates
- **Load balancing** - Multiple app instances
- **Security headers** - Add security middleware

**FastAPI Direct:**
- **Simpler setup** - One less component
- **AsyncIO optimization** - Direct uvicorn handling
- **Development friendly** - Easier debugging

---

# Uvicorn Configuration

## Production Server Setup

```python
# Production uvicorn configuration
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,  # Multiple workers for production
        access_log=True,
        log_level="info"
    )
```

**Multiple workers for better performance**

---

# Cost Analysis

## Platform Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Fly.io** | $0-5/month | $5-50/month | Production apps |
| **Railway** | Free tier | $5-20/month | Learning projects |
| **DigitalOcean** | None | $5-10/month | Full control |
| **Vercel** | Free tier | $20+/month | Serverless |

---

# Cost Optimization Strategies

## Reducing Hosting Costs

1. **Choose appropriate platform** - Match needs to pricing
2. **Optimize resource usage** - Right-size your instances
3. **Use free tiers effectively** - Maximize free allowances
4. **Implement caching** - Reduce database queries
5. **Monitor usage** - Track costs and optimize

---

# Monitoring and Maintenance

## Production Readiness

**Essential monitoring:**
- **Health checks** - Ensure app is running
- **Error tracking** - Log and alert on errors
- **Performance metrics** - Response times and throughput
- **Resource usage** - CPU, memory, disk space

---

# Error Tracking Setup

## Sentry Integration

```python
# Install Sentry
pip install sentry-sdk

# Configure
import sentry_sdk
sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

**Professional error tracking and performance monitoring**

---

# Backup Strategies

## Data Protection

**Database backups:**
- **Automated daily backups** - Most platforms provide this
- **Point-in-time recovery** - Restore to specific moments
- **Cross-region replication** - Geographic redundancy
- **Regular testing** - Verify backup integrity

---

# Security Considerations

## Production Security

**Essential security measures:**
- **HTTPS everywhere** - SSL/TLS certificates
- **Environment variables** - Never hardcode secrets
- **Input validation** - Sanitize all user inputs
- **Rate limiting** - Prevent abuse
- **CORS configuration** - Control cross-origin requests

---

# SSL Certificate Setup

## Let's Encrypt with Nginx

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

**Free SSL certificates with automatic renewal**

---

# Deployment Checklist

## Pre-Deployment Steps

1. **Environment variables** - All secrets configured
2. **Database migrations** - Schema up to date
3. **Static files** - CSS/JS properly served
4. **Error handling** - Graceful failure modes
5. **Health checks** - Monitoring endpoints ready
6. **Documentation** - Deployment instructions updated

---

# Deployment Checklist

## Post-Deployment Steps

1. **Test all endpoints** - Verify functionality
2. **Check logs** - Monitor for errors
3. **Performance testing** - Load test critical paths
4. **Backup verification** - Ensure data protection
5. **Monitoring setup** - Alerts and dashboards
6. **Documentation** - Update deployment docs

---

# Learning Path

## Phase 1: Local Development

1. **Set up development environment** - Local database and services
2. **Test all features** - Ensure everything works locally
3. **Environment configuration** - Use .env files for secrets
4. **Database setup** - Migrations and seed data

---

# Learning Path

## Phase 2: Simple Deployment

1. **Choose a platform** - Start with Railway (easiest)
2. **Deploy basic app** - Get it running in production
3. **Configure environment** - Set up API keys and database
4. **Test production** - Verify all features work

---

# Learning Path

## Phase 3: Production Features

1. **Add monitoring** - Health checks and error tracking
2. **Implement backups** - Data protection strategies
3. **Security hardening** - HTTPS, input validation
4. **Performance optimization** - Caching and database tuning

---

# Learning Path

## Phase 4: Advanced Deployment

1. **Multi-platform deployment** - Deploy to multiple platforms
2. **CI/CD pipeline** - Automated testing and deployment
3. **Scaling strategies** - Handle increased load
4. **Cost optimization** - Monitor and reduce hosting costs

---

# Common Deployment Issues

## Issue 1: Environment Variables

**Problem:** App works locally but fails in production
**Solution:** Verify all environment variables are set correctly

```bash
# Check environment variables
fly secrets list
railway variables
```

---

# Common Deployment Issues

## Issue 2: Database Connection

**Problem:** Database connection errors in production
**Solution:** Check database URL and network connectivity

```python
# Test database connection
import sqlalchemy
engine = create_engine(DATABASE_URL)
engine.connect()
```

---

# Common Deployment Issues

## Issue 3: Static File Serving

**Problem:** CSS/JS files not loading
**Solution:** Configure static file serving properly

```python
# FastAPI static files
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
```

---

# Advanced Deployment Topics

## Docker Containerization

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Containerized deployment for consistency**

---

# Advanced Deployment Topics

## CI/CD with GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: railway up
```

**Automated deployment on code changes**

---

# Scaling Strategies

## Horizontal Scaling

**Multiple app instances:**
- **Load balancer** - Distribute requests
- **Shared database** - All instances use same data
- **Session management** - Stateless application design
- **File storage** - Shared storage for uploads

---

# Scaling Strategies

## Vertical Scaling

**Larger instances:**
- **More CPU/RAM** - Handle more concurrent users
- **Faster storage** - SSD for better I/O performance
- **Better networking** - Higher bandwidth
- **Cost consideration** - More expensive per instance

---

# Business Value of Deployment

## Career Benefits

- **Portfolio development** - Show real applications
- **Production experience** - Understand real-world challenges
- **Problem-solving skills** - Debug production issues
- **Team collaboration** - Work with DevOps and infrastructure

---

# Business Value of Deployment

## Learning Benefits

- **Full-stack understanding** - Complete application lifecycle
- **System design** - Architecture and scalability
- **Security awareness** - Production security considerations
- **Cost management** - Optimize resource usage

---

# Future Enhancements

## Advanced Deployment Features

1. **Blue-green deployments** - Zero-downtime updates
2. **Canary releases** - Gradual feature rollouts
3. **Auto-scaling** - Dynamic resource allocation
4. **Multi-region deployment** - Global availability

---

# Future Enhancements

## Monitoring and Observability

1. **Application Performance Monitoring (APM)** - Detailed performance metrics
2. **Log aggregation** - Centralized logging with ELK stack
3. **Distributed tracing** - Track requests across services
4. **Custom dashboards** - Business-specific metrics

---

# Next Steps

## Immediate Actions

1. **Choose a deployment platform** - Start with Railway for simplicity
2. **Deploy your first app** - Get something running in production
3. **Configure monitoring** - Set up health checks and error tracking
4. **Test thoroughly** - Ensure all features work in production

---

# Next Steps

## Learning Projects

1. **Deploy to multiple platforms** - Compare different hosting options
2. **Implement backup strategies** - Protect your data
3. **Add monitoring** - Professional-grade observability
4. **Optimize performance** - Improve response times and reduce costs

---

# Key Takeaways

## What Makes This Valuable

1. **Real-world skills** - Production deployment experience
2. **Cost awareness** - Understanding hosting economics
3. **Platform knowledge** - Multiple deployment options
4. **Security understanding** - Production security considerations
5. **Portfolio building** - Deploy applications to share

---

# Key Takeaways

## Business Applications

- **Startup deployment** - Get MVPs to market quickly
- **Client projects** - Deploy applications for clients
- **Open source** - Share your work with the community
- **Career advancement** - Demonstrate production skills

---

# Ready to Deploy?

## Start Your Journey

**The best way to learn deployment is by doing!**

Start with a simple deployment and gradually add more sophisticated features.

**Share your applications with the world! 🚀**

---
