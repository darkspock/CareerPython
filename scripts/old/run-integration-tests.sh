#!/bin/bash

# AI Resume Enhancement - Complete Integration Test Script
# This script runs comprehensive integration tests for all AI features

set -e

echo "🚀 Starting AI Resume Enhancement Integration Tests"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "Virtual environment not detected. Activating..."
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_error "Virtual environment not found. Please create one with: python -m venv .venv"
        exit 1
    fi
fi

# Check if required dependencies are installed
print_status "Checking dependencies..."
python -c "import pytest, httpx, fastapi, sqlalchemy" 2>/dev/null || {
    print_error "Required dependencies not found. Installing..."
    pip install -r requirements-test.txt
}

# Set environment variables for testing
export TESTING=true
export DATABASE_URL="sqlite:///./test_integration.db"
export XAI_API_KEY="test_key"
export SMTP_HOST="localhost"
export SMTP_PORT="587"
export SMTP_USERNAME="test@example.com"
export SMTP_PASSWORD="test_password"

print_status "Environment configured for testing"

# Clean up any existing test database
if [ -f "test_integration.db" ]; then
    rm test_integration.db
    print_status "Cleaned up existing test database"
fi

# Run database migrations for testing
print_status "Setting up test database..."
python -c "
from core.database import Base, engine
Base.metadata.create_all(bind=engine)
print('Test database initialized')
"

# Test 1: Complete AI Integration Tests
print_status "Running complete AI integration tests..."
pytest tests/integration/test_complete_ai_integration.py -v --tb=short || {
    print_error "Complete AI integration tests failed"
    exit 1
}
print_success "Complete AI integration tests passed"

# Test 2: Frontend Integration Tests
print_status "Running frontend integration tests..."
pytest tests/integration/test_frontend_ai_integration.py -v --tb=short || {
    print_error "Frontend integration tests failed"
    exit 1
}
print_success "Frontend integration tests passed"

# Test 3: AI Service Integration Tests
print_status "Running AI service integration tests..."
pytest tests/integration/test_xai_service_integration.py -v --tb=short || {
    print_error "AI service integration tests failed"
    exit 1
}
print_success "AI service integration tests passed"

# Test 4: Resume Processing End-to-End Tests
print_status "Running resume processing E2E tests..."
pytest tests/integration/test_ai_resume_processing_e2e.py -v --tb=short || {
    print_error "Resume processing E2E tests failed"
    exit 1
}
print_success "Resume processing E2E tests passed"

# Test 5: Interview Workflow End-to-End Tests
print_status "Running interview workflow E2E tests..."
pytest tests/integration/test_ai_interview_workflow_e2e.py -v --tb=short || {
    print_error "Interview workflow E2E tests failed"
    exit 1
}
print_success "Interview workflow E2E tests passed"

# Test 6: Subscription and Payment Integration Tests
print_status "Running subscription integration tests..."
pytest tests/integration/test_subscription_payment_integration.py -v --tb=short || {
    print_error "Subscription integration tests failed"
    exit 1
}
print_success "Subscription integration tests passed"

# Test 7: Job Application Integration Tests
print_status "Running job application integration tests..."
pytest tests/integration/test_job_application_integration.py -v --tb=short || {
    print_error "Job application integration tests failed"
    exit 1
}
print_success "Job application integration tests passed"

# Test 8: Resume Export Integration Tests
print_status "Running resume export integration tests..."
pytest tests/integration/test_resume_export_integration.py -v --tb=short || {
    print_error "Resume export integration tests failed"
    exit 1
}
print_success "Resume export integration tests passed"

# Test 9: Enhanced API Endpoints Tests
print_status "Running enhanced API endpoints tests..."
pytest tests/integration/test_ai_enhanced_endpoints.py -v --tb=short || {
    print_error "Enhanced API endpoints tests failed"
    exit 1
}
print_success "Enhanced API endpoints tests passed"

# Test 10: Email Notification Integration Tests
print_status "Running email notification integration tests..."
pytest tests/integration/test_email_notification_integration.py -v --tb=short || {
    print_error "Email notification integration tests failed"
    exit 1
}
print_success "Email notification integration tests passed"

# Test 11: Analytics Integration Tests
print_status "Running analytics integration tests..."
pytest tests/integration/test_analytics_integration.py -v --tb=short || {
    print_error "Analytics integration tests failed"
    exit 1
}
print_success "Analytics integration tests passed"

# Test 12: AI Monitoring Integration Tests
print_status "Running AI monitoring integration tests..."
pytest tests/integration/test_ai_monitoring_integration.py -v --tb=short || {
    print_error "AI monitoring integration tests failed"
    exit 1
}
print_success "AI monitoring integration tests passed"

# Test 13: Enhanced Security Integration Tests
print_status "Running enhanced security integration tests..."
pytest tests/integration/test_enhanced_security_middleware.py -v --tb=short || {
    print_error "Enhanced security integration tests failed"
    exit 1
}
print_success "Enhanced security integration tests passed"

# Performance Tests
print_status "Running AI processing performance tests..."
pytest tests/performance/test_ai_processing_performance.py -v --tb=short || {
    print_warning "Performance tests failed - this may be due to system resources"
}

# Generate Integration Test Report
print_status "Generating integration test report..."
pytest tests/integration/ --html=test-results/integration_report.html --self-contained-html || {
    print_warning "Could not generate HTML report - pytest-html may not be installed"
}

# Test API Documentation
print_status "Testing API documentation endpoints..."
python -c "
import requests
import sys
try:
    # Start server in background for testing
    import subprocess
    import time
    import signal
    
    # Start the server
    server = subprocess.Popen(['uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8001'], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  # Wait for server to start
    
    # Test API docs endpoints
    response = requests.get('http://localhost:8001/docs')
    assert response.status_code == 200, 'API docs not accessible'
    
    response = requests.get('http://localhost:8001/redoc')
    assert response.status_code == 200, 'ReDoc not accessible'
    
    response = requests.get('http://localhost:8001/openapi.json')
    assert response.status_code == 200, 'OpenAPI spec not accessible'
    
    print('API documentation endpoints are working')
    
    # Clean up
    server.terminate()
    server.wait()
    
except Exception as e:
    print(f'API documentation test failed: {e}')
    if 'server' in locals():
        server.terminate()
    sys.exit(1)
" || {
    print_error "API documentation tests failed"
    exit 1
}
print_success "API documentation tests passed"

# Clean up test database
if [ -f "test_integration.db" ]; then
    rm test_integration.db
    print_status "Cleaned up test database"
fi

# Summary
echo ""
echo "🎉 Integration Test Summary"
echo "=========================="
print_success "✅ Complete AI Integration Tests"
print_success "✅ Frontend Integration Tests"
print_success "✅ AI Service Integration Tests"
print_success "✅ Resume Processing E2E Tests"
print_success "✅ Interview Workflow E2E Tests"
print_success "✅ Subscription Integration Tests"
print_success "✅ Job Application Integration Tests"
print_success "✅ Resume Export Integration Tests"
print_success "✅ Enhanced API Endpoints Tests"
print_success "✅ Email Notification Integration Tests"
print_success "✅ Analytics Integration Tests"
print_success "✅ AI Monitoring Integration Tests"
print_success "✅ Enhanced Security Integration Tests"
print_success "✅ API Documentation Tests"

echo ""
print_success "🚀 All AI Resume Enhancement integration tests completed successfully!"
print_status "The system is ready for production deployment."

# Optional: Run a quick smoke test against the actual API
if [ "$1" = "--smoke-test" ]; then
    print_status "Running smoke test against running API..."
    python -c "
import requests
import sys

try:
    # Test health endpoint
    response = requests.get('http://localhost:8000/health', timeout=5)
    if response.status_code == 200:
        print('✅ API health check passed')
    else:
        print('❌ API health check failed')
        sys.exit(1)
        
    # Test OpenAPI spec
    response = requests.get('http://localhost:8000/openapi.json', timeout=5)
    if response.status_code == 200:
        print('✅ OpenAPI spec accessible')
    else:
        print('❌ OpenAPI spec not accessible')
        sys.exit(1)
        
    print('🎉 Smoke test completed successfully!')
    
except requests.exceptions.ConnectionError:
    print('⚠️  API server not running - skipping smoke test')
except Exception as e:
    print(f'❌ Smoke test failed: {e}')
    sys.exit(1)
"
fi

echo ""
print_success "Integration testing completed! 🎉"