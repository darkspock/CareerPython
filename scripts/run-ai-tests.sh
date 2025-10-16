#!/bin/bash

# AI Features Test Runner Script with Docker
# This script runs comprehensive tests for AI-enhanced features using Docker containers

set -e  # Exit on any error

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

# Function to run tests with timing
run_test_suite() {
    local test_name="$1"
    local test_command="$2"
    local start_time=$(date +%s)
    
    print_status "Running $test_name..."
    
    if eval "$test_command"; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        print_success "$test_name completed in ${duration}s"
        return 0
    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        print_error "$test_name failed after ${duration}s"
        return 1
    fi
}

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "docker-compose.test.yml" ]; then
    print_error "docker-compose.test.yml not found. Please run this script from the project root directory."
    exit 1
fi

print_status "Starting AI Features Test Suite"
print_status "================================"

# Initialize test results
total_tests=0
passed_tests=0
failed_tests=0

# Test configuration
TEST_RESULTS_DIR="test-results"
mkdir -p "$TEST_RESULTS_DIR" coverage-reports security-reports performance-reports

# Cleanup function
cleanup() {
    print_status "Cleaning up Docker containers..."
    docker-compose -f docker-compose.test.yml down --volumes --remove-orphans > /dev/null 2>&1 || true
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Parse command line arguments
RUN_UNIT=true
RUN_INTEGRATION=true
RUN_PERFORMANCE=false
RUN_E2E=false
VERBOSE=false
COVERAGE=false
PARALLEL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --unit-only)
            RUN_UNIT=true
            RUN_INTEGRATION=false
            RUN_PERFORMANCE=false
            RUN_E2E=false
            shift
            ;;
        --integration-only)
            RUN_UNIT=false
            RUN_INTEGRATION=true
            RUN_PERFORMANCE=false
            RUN_E2E=false
            shift
            ;;
        --performance)
            RUN_PERFORMANCE=true
            shift
            ;;
        --e2e)
            RUN_E2E=true
            shift
            ;;
        --all)
            RUN_UNIT=true
            RUN_INTEGRATION=true
            RUN_PERFORMANCE=true
            RUN_E2E=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --coverage)
            COVERAGE=true
            shift
            ;;
        --parallel)
            PARALLEL=true
            shift
            ;;
        --help)
            echo "AI Features Test Runner"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --unit-only      Run only unit tests"
            echo "  --integration-only Run only integration tests"
            echo "  --performance    Include performance tests"
            echo "  --e2e           Include end-to-end tests"
            echo "  --all           Run all test types"
            echo "  --verbose       Verbose output"
            echo "  --coverage      Generate coverage report"
            echo "  --parallel      Run tests in parallel"
            echo "  --help          Show this help message"
            echo ""
            echo "Default: Runs unit and integration tests"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Build Docker test command options
DOCKER_PYTEST_OPTS=""
if [ "$VERBOSE" = true ]; then
    DOCKER_PYTEST_OPTS="$DOCKER_PYTEST_OPTS -v"
fi

if [ "$COVERAGE" = true ]; then
    DOCKER_PYTEST_OPTS="$DOCKER_PYTEST_OPTS --cov=src --cov-report=html:/app/coverage-reports/ai --cov-report=term"
fi

if [ "$PARALLEL" = true ]; then
    DOCKER_PYTEST_OPTS="$DOCKER_PYTEST_OPTS -n auto"
fi

# Start required services
print_status "Starting Docker services for AI tests..."
docker-compose -f docker-compose.test.yml up -d test-db test-redis mock-ai-service mock-email-service
sleep 15  # Wait for services to be ready

# 1. Unit Tests for AI-Enhanced Domain Entities and Services
if [ "$RUN_UNIT" = true ]; then
    print_status "Phase 1: Unit Tests for AI-Enhanced Features"
    print_status "============================================="
    
    # AI-Enhanced Domain Entities
    if run_test_suite "AI-Enhanced Domain Entities" \
        "docker-compose -f docker-compose.test.yml run --rm test-runner python -m pytest $DOCKER_PYTEST_OPTS tests/unit/shared/test_ai_enhanced_domain_entities.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # AI-Enhanced Services
    if run_test_suite "AI-Enhanced Services" \
        "docker-compose -f docker-compose.test.yml run --rm test-runner python -m pytest $DOCKER_PYTEST_OPTS tests/unit/shared/test_ai_enhanced_services.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # XAI Service Unit Tests
    if run_test_suite "XAI Service Unit Tests" \
        "docker-compose -f docker-compose.test.yml run --rm test-runner python -m pytest $DOCKER_PYTEST_OPTS tests/unit/test_xai_service.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Subscription Security Tests
    if run_test_suite "Subscription Security Tests" \
        "docker-compose -f docker-compose.test.yml run --rm test-runner python -m pytest $DOCKER_PYTEST_OPTS tests/unit/shared/test_subscription_security.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Resume Processing Service
    if run_test_suite "Resume Processing Service" \
        "docker-compose -f docker-compose.test.yml run --rm test-runner python -m pytest $DOCKER_PYTEST_OPTS tests/unit/candidate/test_resume_processing_service.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # AI Interview Service
    if run_test_suite "AI Interview Service" \
        "docker-compose -f docker-compose.test.yml run --rm test-runner python -m pytest $DOCKER_PYTEST_OPTS tests/unit/interview/test_ai_interview_service.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    print_status "Unit tests phase completed"
    echo ""
fi

# 2. Integration Tests for XAI Service Interactions
if [ "$RUN_INTEGRATION" = true ]; then
    print_status "Phase 2: Integration Tests for XAI Service Interactions"
    print_status "======================================================="
    
    # Basic XAI Service Integration
    if run_test_suite "XAI Service Integration" \
        "docker-compose -f docker-compose.test.yml run --rm integration-tests python -m pytest $DOCKER_PYTEST_OPTS tests/integration/test_xai_service_integration.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Extended XAI Service Integration
    if run_test_suite "Extended XAI Service Integration" \
        "docker-compose -f docker-compose.test.yml run --rm integration-tests python -m pytest $DOCKER_PYTEST_OPTS tests/integration/test_xai_service_extended_integration.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Enhanced Security Middleware
    if run_test_suite "Enhanced Security Middleware" \
        "docker-compose -f docker-compose.test.yml run --rm integration-tests python -m pytest $DOCKER_PYTEST_OPTS tests/integration/test_enhanced_security_middleware.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Resume Processing Integration
    if run_test_suite "Resume Processing Integration" \
        "docker-compose -f docker-compose.test.yml run --rm integration-tests python -m pytest $DOCKER_PYTEST_OPTS tests/integration/test_resume_processing_integration.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # AI Interview Integration
    if run_test_suite "AI Interview Integration" \
        "docker-compose -f docker-compose.test.yml run --rm integration-tests python -m pytest $DOCKER_PYTEST_OPTS tests/integration/test_ai_interview_integration.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    print_status "Integration tests phase completed"
    echo ""
fi

# 3. End-to-End Tests for Resume Processing and Interview Workflows
if [ "$RUN_E2E" = true ]; then
    print_status "Phase 3: End-to-End Workflow Tests"
    print_status "==================================="
    
    # Resume Processing E2E
    if run_test_suite "Resume Processing E2E Workflow" \
        "docker-compose -f docker-compose.test.yml run --rm integration-tests python -m pytest $DOCKER_PYTEST_OPTS tests/integration/test_ai_resume_processing_e2e.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    # Interview Workflow E2E
    if run_test_suite "AI Interview Workflow E2E" \
        "docker-compose -f docker-compose.test.yml run --rm integration-tests python -m pytest $DOCKER_PYTEST_OPTS tests/integration/test_ai_interview_workflow_e2e.py"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    print_status "End-to-end tests phase completed"
    echo ""
fi

# 4. Performance Tests for AI Processing
if [ "$RUN_PERFORMANCE" = true ]; then
    print_status "Phase 4: Performance Tests for AI Processing"
    print_status "============================================="
    
    print_warning "Performance tests may take longer to complete..."
    
    if run_test_suite "AI Processing Performance Tests" \
        "docker-compose -f docker-compose.test.yml run --rm performance-tests python -m pytest $DOCKER_PYTEST_OPTS tests/performance/test_ai_processing_performance.py --timeout=300"; then
        ((passed_tests++))
    else
        ((failed_tests++))
    fi
    ((total_tests++))
    
    print_status "Performance tests phase completed"
    echo ""
fi

# Generate test summary
print_status "Test Summary"
print_status "============"
echo "Total test suites: $total_tests"
echo "Passed: $passed_tests"
echo "Failed: $failed_tests"

if [ $failed_tests -eq 0 ]; then
    print_success "All test suites passed! ✅"
    
    # Generate additional reports if coverage was enabled
    if [ "$COVERAGE" = true ]; then
        print_status "Coverage report generated at: $TEST_RESULTS_DIR/coverage/index.html"
    fi
    
    # Run a quick smoke test to verify AI features are working
    print_status "Running AI features smoke test..."
    if docker-compose -f docker-compose.test.yml run --rm test-runner python -m pytest tests/unit/test_xai_service.py::TestXAIService::test_init_with_valid_config -q; then
        print_success "AI features smoke test passed ✅"
    else
        print_warning "AI features smoke test failed ⚠️"
    fi
    
    # Show Docker test results locations
    print_status "Docker test results available at:"
    echo "  - Coverage reports: ./coverage-reports/"
    echo "  - Security reports: ./security-reports/"
    echo "  - Performance reports: ./performance-reports/"
    echo "  - Test results: ./test-results/"
    echo ""
    echo "View reports in browser:"
    echo "  docker-compose -f docker-compose.test.yml up test-viewer"
    echo "  Then open: http://localhost:8090"
    
    exit 0
else
    print_error "Some test suites failed! ❌"
    echo ""
    print_status "Failed test suites need attention before deployment."
    
    # Suggest next steps
    echo ""
    print_status "Suggested next steps:"
    echo "1. Review failed test output above"
    echo "2. Fix failing tests"
    echo "3. Re-run tests with --verbose for more details"
    echo "4. Check test logs in $TEST_RESULTS_DIR/"
    
    exit 1
fi