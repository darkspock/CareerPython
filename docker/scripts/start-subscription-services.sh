#!/bin/bash

# Start subscription and payment services with Docker

set -e

echo "Starting AI Resume Enhancement Platform with Subscription Services..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    exit 1
fi

# Load environment variables
if [ -f .env.docker ]; then
    echo "Loading environment variables from .env.docker"
    export $(cat .env.docker | grep -v '^#' | xargs)
else
    echo "Warning: .env.docker file not found. Using default values."
fi

# Create necessary directories
mkdir -p docker/nginx/ssl
mkdir -p logs

# Build and start services
echo "Building and starting services..."
docker-compose -f docker/docker-compose.subscription.yml up --build -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check service health
echo "Checking service health..."

# Check main app
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Main application is healthy"
else
    echo "✗ Main application is not responding"
fi

# Check payment service
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✓ Payment service is healthy"
else
    echo "✗ Payment service is not responding"
fi

# Check email service
if curl -f http://localhost:8002/health > /dev/null 2>&1; then
    echo "✓ Email service is healthy"
else
    echo "✗ Email service is not responding"
fi

# Check database
if docker-compose -f docker/docker-compose.subscription.yml exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "✓ PostgreSQL database is ready"
else
    echo "✗ PostgreSQL database is not ready"
fi

# Check Redis
if docker-compose -f docker/docker-compose.subscription.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✓ Redis is ready"
else
    echo "✗ Redis is not ready"
fi

echo ""
echo "Services started successfully!"
echo ""
echo "Available endpoints:"
echo "  Main Application: http://localhost:8000"
echo "  Payment Service:  http://localhost:8001"
echo "  Email Service:    http://localhost:8002"
echo "  PostgreSQL:       localhost:5432"
echo "  Redis:            localhost:6379"
echo ""
echo "To view logs: docker-compose -f docker/docker-compose.subscription.yml logs -f"
echo "To stop services: docker-compose -f docker/docker-compose.subscription.yml down"
echo ""

# Run database migrations
echo "Running database migrations..."
docker-compose -f docker/docker-compose.subscription.yml exec app alembic upgrade head

echo "Setup complete! The subscription and payment system is ready."