#!/bin/bash

# Production Build Optimization Script for AI Resume Enhancement Platform
# This script optimizes both backend and frontend for production deployment

set -e

echo "🚀 Starting production build optimization..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        print_warning "Docker is not installed - skipping containerization"
    fi
    
    print_status "Dependencies check completed"
}

# Optimize Python backend
optimize_backend() {
    print_status "Optimizing Python backend..."
    
    # Create optimized requirements file
    print_status "Creating optimized requirements..."
    pip-compile requirements.txt --output-file requirements-prod.txt --no-emit-index-url
    
    # Remove development dependencies
    grep -v "pytest\|black\|mypy\|flake8" requirements-prod.txt > requirements-prod-clean.txt
    mv requirements-prod-clean.txt requirements-prod.txt
    
    # Compile Python files for faster startup
    print_status "Compiling Python bytecode..."
    python3 -m compileall -b .
    
    # Create production configuration
    cat > config/production.py << EOF
import os
from core.config import Settings

class ProductionSettings(Settings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/airesume_prod")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "").split(",")
    
    # Performance
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    MAX_CONNECTIONS: int = int(os.getenv("MAX_CONNECTIONS", "100"))
    
    # Caching
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "json"
    
    # AI Service
    XAI_API_KEY: str = os.getenv("XAI_API_KEY")
    XAI_RATE_LIMIT: int = int(os.getenv("XAI_RATE_LIMIT", "100"))
    
    # Email
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    
    # Payment
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    class Config:
        env_file = ".env.production"
EOF
    
    print_status "Backend optimization completed"
}

# Optimize React frontend
optimize_frontend() {
    print_status "Optimizing React frontend..."
    
    cd client
    
    # Install dependencies
    print_status "Installing frontend dependencies..."
    npm ci --production=false
    
    # Run type checking
    print_status "Running TypeScript type checking..."
    npm run type-check
    
    # Run linting
    print_status "Running ESLint..."
    npm run lint
    
    # Run tests
    print_status "Running frontend tests..."
    npm run test -- --coverage --watchAll=false
    
    # Build for production
    print_status "Building production bundle..."
    npm run build
    
    # Analyze bundle size
    print_status "Analyzing bundle size..."
    npm run analyze
    
    # Create optimized Dockerfile for frontend
    cat > Dockerfile.prod << EOF
# Multi-stage build for React frontend
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF
    
    # Create nginx configuration
    cat > nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # Handle client-side routing
        location / {
            try_files \$uri \$uri/ /index.html;
        }
        
        # API proxy
        location /api/ {
            proxy_pass http://backend:8000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF
    
    cd ..
    print_status "Frontend optimization completed"
}

# Create production Docker setup
create_docker_setup() {
    print_status "Creating production Docker setup..."
    
    # Backend Dockerfile
    cat > Dockerfile.backend << EOF
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . .
RUN chown -R app:app /app

# Switch to app user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "main:app"]
EOF
    
    # Production docker-compose
    cat > docker-compose.prod.yml << EOF
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/airesume_prod
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=\${SECRET_KEY}
      - XAI_API_KEY=\${XAI_API_KEY}
      - STRIPE_SECRET_KEY=\${STRIPE_SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    
  frontend:
    build:
      context: ./client
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
    
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=airesume_prod
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
EOF
    
    print_status "Docker setup created"
}

# Create performance monitoring setup
create_monitoring() {
    print_status "Setting up performance monitoring..."
    
    # Create monitoring docker-compose
    cat > docker-compose.monitoring.yml << EOF
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    restart: unless-stopped
    
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    restart: unless-stopped
    
  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
EOF
    
    # Create Prometheus configuration
    mkdir -p monitoring
    cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'ai-resume-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
      
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
EOF
    
    print_status "Monitoring setup created"
}

# Create deployment scripts
create_deployment_scripts() {
    print_status "Creating deployment scripts..."
    
    # Health check script
    cat > scripts/health-check.sh << 'EOF'
#!/bin/bash

# Health check script for production deployment

check_backend() {
    echo "Checking backend health..."
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
    if [ "$response" = "200" ]; then
        echo "✅ Backend is healthy"
        return 0
    else
        echo "❌ Backend health check failed (HTTP $response)"
        return 1
    fi
}

check_frontend() {
    echo "Checking frontend..."
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80)
    if [ "$response" = "200" ]; then
        echo "✅ Frontend is healthy"
        return 0
    else
        echo "❌ Frontend health check failed (HTTP $response)"
        return 1
    fi
}

check_database() {
    echo "Checking database connection..."
    if docker exec airesume_db_1 pg_isready -U postgres; then
        echo "✅ Database is healthy"
        return 0
    else
        echo "❌ Database health check failed"
        return 1
    fi
}

check_redis() {
    echo "Checking Redis connection..."
    if docker exec airesume_redis_1 redis-cli ping | grep -q PONG; then
        echo "✅ Redis is healthy"
        return 0
    else
        echo "❌ Redis health check failed"
        return 1
    fi
}

# Run all health checks
echo "🏥 Running health checks..."
failed=0

check_backend || failed=1
check_frontend || failed=1
check_database || failed=1
check_redis || failed=1

if [ $failed -eq 0 ]; then
    echo "🎉 All health checks passed!"
    exit 0
else
    echo "💥 Some health checks failed!"
    exit 1
fi
EOF
    
    # Backup script
    cat > scripts/backup.sh << 'EOF'
#!/bin/bash

# Backup script for production data

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "🗄️ Starting backup process..."

# Database backup
echo "Backing up database..."
docker exec airesume_db_1 pg_dump -U postgres airesume_prod > "$BACKUP_DIR/db_backup_$DATE.sql"

# User assets backup
echo "Backing up user assets..."
tar -czf "$BACKUP_DIR/assets_backup_$DATE.tar.gz" ./user_assets/

# Configuration backup
echo "Backing up configuration..."
tar -czf "$BACKUP_DIR/config_backup_$DATE.tar.gz" .env.production docker-compose.prod.yml

# Clean old backups (keep last 7 days)
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "✅ Backup completed: $DATE"
EOF
    
    # Deployment script
    cat > scripts/deploy.sh << 'EOF'
#!/bin/bash

# Production deployment script

set -e

echo "🚀 Starting production deployment..."

# Pull latest code
git pull origin main

# Build and deploy
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Run health checks
./scripts/health-check.sh

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

echo "✅ Deployment completed successfully!"
EOF
    
    chmod +x scripts/*.sh
    print_status "Deployment scripts created"
}

# Main execution
main() {
    check_dependencies
    optimize_backend
    optimize_frontend
    create_docker_setup
    create_monitoring
    create_deployment_scripts
    
    print_status "🎉 Production build optimization completed!"
    print_status "Next steps:"
    echo "  1. Set environment variables in .env.production"
    echo "  2. Configure SSL certificates"
    echo "  3. Run: docker-compose -f docker-compose.prod.yml up -d"
    echo "  4. Set up monitoring: docker-compose -f docker-compose.monitoring.yml up -d"
    echo "  5. Configure CI/CD pipeline"
}

# Run main function
main "$@"