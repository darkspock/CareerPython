#!/bin/bash

# Development startup script for AI Resume Enhancement Platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AI Resume Enhancement Platform - Development Setup${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}📝 Please update .env with your configuration before continuing.${NC}"
    echo -e "${YELLOW}   Especially set your XAI_API_KEY for AI features to work.${NC}"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit and configure .env first..."
else
    echo -e "${GREEN}✅ Using existing .env configuration${NC}"
fi

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p uploads
mkdir -p backups
mkdir -p logs

# Start services
echo -e "${BLUE}🔨 Building and starting services...${NC}"
docker-compose up -d --build

# Wait for services to be healthy
echo -e "${BLUE}⏳ Waiting for services to be ready...${NC}"

# Wait for database
echo -n "  Database: "
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ready${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# Wait for Redis
echo -n "  Redis: "
for i in {1..30}; do
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ready${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# Wait for web service
echo -n "  Backend API: "
for i in {1..60}; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ready${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

echo ""
echo -e "${GREEN}🎉 Development environment is ready!${NC}"
echo ""
echo -e "${BLUE}📋 Available Services:${NC}"
echo -e "  🌐 Backend API:     ${GREEN}http://localhost:8000${NC}"
echo -e "  📚 API Docs:        ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  🗄️  Database:        ${GREEN}localhost:5432${NC}"
echo -e "  🔴 Redis:           ${GREEN}localhost:6379${NC}"
echo -e "  🛠️  DB Admin:        ${GREEN}http://localhost:8080${NC}"
echo ""
echo -e "${BLUE}🔧 Useful Commands:${NC}"
echo -e "  ${YELLOW}make logs${NC}     - View application logs"
echo -e "  ${YELLOW}make shell${NC}    - Access backend shell"
echo -e "  ${YELLOW}make stop${NC}     - Stop all services"
echo -e "  ${YELLOW}make restart${NC}  - Restart services"
echo -e "  ${YELLOW}make test${NC}     - Run tests"
echo ""
echo -e "${BLUE}📝 Next Steps:${NC}"
echo -e "  1. Update your .env file with proper API keys"
echo -e "  2. Visit ${GREEN}http://localhost:8000/docs${NC} to explore the API"
echo -e "  3. Check logs with ${YELLOW}make logs${NC} if you encounter issues"
echo ""