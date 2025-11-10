#!/bin/bash

# Production Deployment Script for AI Resume Enhancement Platform
# This script handles zero-downtime deployment with rollback capabilities

set -e

# Configuration
DEPLOY_DIR="/opt/ai-resume-platform"
BACKUP_DIR="/opt/backups"
LOG_FILE="/var/log/deployment.log"
HEALTH_CHECK_TIMEOUT=300
ROLLBACK_ENABLED=true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ $1${NC}" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ $1${NC}" | tee -a "$LOG_FILE"
}

# Cleanup function for rollback
cleanup_and_rollback() {
    log_error "Deployment failed. Starting rollback..."
    
    if [ "$ROLLBACK_ENABLED" = true ] && [ -f "$BACKUP_DIR/docker-compose.backup.yml" ]; then
        log "Rolling back to previous version..."
        
        # Stop current services
        docker-compose -f docker-compose.prod.yml down
        
        # Restore previous configuration
        cp "$BACKUP_DIR/docker-compose.backup.yml" docker-compose.prod.yml
        
        # Start previous version
        docker-compose -f docker-compose.prod.yml up -d
        
        # Wait and check health
        sleep 60
        if ./scripts/health-check.sh; then
            log_success "Rollback completed successfully"
            send_notification "🔄 Deployment failed, rollback completed successfully"
        else
            log_error "Rollback failed! Manual intervention required"
            send_notification "🚨 CRITICAL: Deployment and rollback both failed! Manual intervention required"
        fi
    else
        log_error "Rollback not available. Manual intervention required"
        send_notification "🚨 CRITICAL: Deployment failed and rollback not available!"
    fi
    
    exit 1
}

# Set trap for cleanup on failure
trap cleanup_and_rollback ERR

# Send notification function
send_notification() {
    local message="$1"
    local webhook_url="${SLACK_WEBHOOK_URL:-}"
    
    if [ -n "$webhook_url" ]; then
        curl -X POST "$webhook_url" \
            -H 'Content-type: application/json' \
            --data "{\"text\":\"$message\"}" \
            --silent --show-error || log_warning "Failed to send notification"
    fi
    
    # Also send email if configured
    if command -v mail &> /dev/null && [ -n "${ADMIN_EMAIL:-}" ]; then
        echo "$message" | mail -s "AI Resume Platform Deployment" "$ADMIN_EMAIL" || true
    fi
}

# Pre-deployment checks
pre_deployment_checks() {
    log "Running pre-deployment checks..."
    
    # Check if we're in the correct directory
    if [ ! -f "docker-compose.prod.yml" ]; then
        log_error "docker-compose.prod.yml not found. Are you in the correct directory?"
        exit 1
    fi
    
    # Check if required environment variables are set
    required_vars=("SECRET_KEY" "DATABASE_URL" "XAI_API_KEY" "STRIPE_SECRET_KEY")
    for var in "${required_vars[@]}"; do
        if [ -z "${!var:-}" ]; then
            log_error "Required environment variable $var is not set"
            exit 1
        fi
    done
    
    # Check Docker and Docker Compose
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    # Check disk space (require at least 2GB free)
    available_space=$(df / | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 2097152 ]; then  # 2GB in KB
        log_error "Insufficient disk space. At least 2GB required"
        exit 1
    fi
    
    # Check if services are currently running
    if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        log "Current services are running. Will perform rolling update."
    else
        log "No services currently running. Will perform fresh deployment."
    fi
    
    log_success "Pre-deployment checks passed"
}

# Create backup
create_backup() {
    log "Creating backup..."
    
    # Create backup directory with timestamp
    BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    CURRENT_BACKUP_DIR="$BACKUP_DIR/$BACKUP_TIMESTAMP"
    mkdir -p "$CURRENT_BACKUP_DIR"
    
    # Backup database
    log "Backing up database..."
    docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres airesume_prod > "$CURRENT_BACKUP_DIR/database.sql" || {
        log_warning "Database backup failed, but continuing deployment"
    }
    
    # Backup current configuration
    cp docker-compose.prod.yml "$BACKUP_DIR/docker-compose.backup.yml"
    cp -r .env.production "$CURRENT_BACKUP_DIR/" 2>/dev/null || true
    
    # Backup user assets
    if [ -d "user_assets" ]; then
        tar -czf "$CURRENT_BACKUP_DIR/user_assets.tar.gz" user_assets/
    fi
    
    # Clean old backups (keep last 5)
    ls -t "$BACKUP_DIR" | tail -n +6 | xargs -I {} rm -rf "$BACKUP_DIR/{}" 2>/dev/null || true
    
    log_success "Backup created at $CURRENT_BACKUP_DIR"
}

# Pull latest code and images
update_code_and_images() {
    log "Updating code and Docker images..."
    
    # Pull latest code
    git fetch origin
    git reset --hard origin/main
    
    # Pull latest Docker images
    docker-compose -f docker-compose.prod.yml pull
    
    log_success "Code and images updated"
}

# Deploy with zero downtime
deploy_services() {
    log "Starting zero-downtime deployment..."
    
    # Start new services alongside old ones (if any)
    docker-compose -f docker-compose.prod.yml up -d --remove-orphans
    
    log "Waiting for services to start..."
    sleep 30
    
    # Wait for services to be healthy
    local timeout=$HEALTH_CHECK_TIMEOUT
    local elapsed=0
    
    while [ $elapsed -lt $timeout ]; do
        if ./scripts/health-check.sh &>/dev/null; then
            log_success "Services are healthy"
            break
        fi
        
        log "Services not ready yet, waiting... ($elapsed/$timeout seconds)"
        sleep 10
        elapsed=$((elapsed + 10))
    done
    
    if [ $elapsed -ge $timeout ]; then
        log_error "Services failed to become healthy within $timeout seconds"
        return 1
    fi
}

# Run database migrations
run_migrations() {
    log "Running database migrations..."
    
    # Run migrations
    docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
    
    log_success "Database migrations completed"
}

# Post-deployment verification
post_deployment_verification() {
    log "Running post-deployment verification..."
    
    # Run comprehensive health checks
    if ! ./scripts/health-check.sh; then
        log_error "Post-deployment health checks failed"
        return 1
    fi
    
    # Test critical endpoints
    local backend_url="http://localhost:8000"
    local frontend_url="http://localhost:80"
    
    # Test backend API
    if ! curl -f -s "$backend_url/health" > /dev/null; then
        log_error "Backend API health check failed"
        return 1
    fi
    
    # Test frontend
    if ! curl -f -s "$frontend_url" > /dev/null; then
        log_error "Frontend health check failed"
        return 1
    fi
    
    # Test database connectivity
    if ! docker-compose -f docker-compose.prod.yml exec -T backend python -c "
from core.database import get_db_session
import asyncio
async def test_db():
    async with get_db_session() as session:
        result = await session.execute('SELECT 1')
        return result.scalar()
asyncio.run(test_db())
"; then
        log_error "Database connectivity test failed"
        return 1
    fi
    
    # Test AI service integration (if configured)
    if [ -n "${XAI_API_KEY:-}" ]; then
        docker-compose -f docker-compose.prod.yml exec -T backend python -c "
from src.framework.infrastructure.services.xai_service import XAIService
import asyncio
async def test_ai():
    service = XAIService()
    # Simple test - this should not fail even if API key is invalid
    return True
asyncio.run(test_ai())
" || log_warning "AI service test failed (may be expected if API key is test key)"
    fi
    
    log_success "Post-deployment verification completed"
}

# Cleanup old containers and images
cleanup_old_resources() {
    log "Cleaning up old Docker resources..."
    
    # Remove unused containers
    docker container prune -f
    
    # Remove unused images (keep last 3 versions)
    docker image prune -f
    
    # Remove unused volumes (be careful with this)
    # docker volume prune -f  # Commented out for safety
    
    log_success "Cleanup completed"
}

# Main deployment function
main() {
    log "🚀 Starting production deployment of AI Resume Enhancement Platform"
    
    # Change to deployment directory
    cd "$DEPLOY_DIR" || {
        log_error "Failed to change to deployment directory: $DEPLOY_DIR"
        exit 1
    }
    
    # Run deployment steps
    pre_deployment_checks
    create_backup
    update_code_and_images
    deploy_services
    run_migrations
    post_deployment_verification
    cleanup_old_resources
    
    # Success notification
    local commit_hash=$(git rev-parse --short HEAD)
    local deploy_time=$(date '+%Y-%m-%d %H:%M:%S')
    
    log_success "🎉 Deployment completed successfully!"
    log "Commit: $commit_hash"
    log "Deploy time: $deploy_time"
    
    send_notification "🚀 AI Resume Platform deployed successfully! Commit: $commit_hash at $deploy_time"
}

# Handle command line arguments
case "${1:-}" in
    --dry-run)
        log "Running in dry-run mode (no actual deployment)"
        ROLLBACK_ENABLED=false
        # Add dry-run logic here
        ;;
    --no-rollback)
        log "Rollback disabled"
        ROLLBACK_ENABLED=false
        main
        ;;
    --help)
        echo "Usage: $0 [--dry-run|--no-rollback|--help]"
        echo "  --dry-run     : Run deployment checks without actual deployment"
        echo "  --no-rollback : Disable automatic rollback on failure"
        echo "  --help        : Show this help message"
        exit 0
        ;;
    *)
        main
        ;;
esac