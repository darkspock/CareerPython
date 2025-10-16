#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Default test type
TEST_TYPE=${1:-"all"}

print_status "🧪 Running AI Resume Enhancement Tests with Docker"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Function to run specific test type
run_tests() {
    local test_type=$1
    
    case $test_type in
        "unit")
            print_status "Running unit tests..."
            docker-compose -f docker-compose.test.yml up --build unit-tests
            ;;
        "integration")
            print_status "Running integration tests..."
            docker-compose -f docker-compose.test.yml up --build integration-tests
            ;;
        "security")
            print_status "Running security tests..."
            docker-compose -f docker-compose.test.yml up --build security-tests
            ;;
        "performance")
            print_status "Running performance tests..."
            docker-compose -f docker-compose.test.yml up --build performance-tests
            ;;
        "all")
            print_status "Running all tests..."
            docker-compose -f docker-compose.test.yml up --build test-runner unit-tests integration-tests security-tests
            ;;
        "quick")
            print_status "Running quick test suite (unit + security)..."
            docker-compose -f docker-compose.test.yml up --build unit-tests security-tests
            ;;
        *)
            print_error "Unknown test type: $test_type"
            echo "Available options: unit, integration, security, performance, all, quick"
            exit 1
            ;;
    esac
}

# Cleanup function
cleanup() {
    print_status "Cleaning up Docker containers..."
    docker-compose -f docker-compose.test.yml down --volumes --remove-orphans
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Create necessary directories
mkdir -p test-results coverage-reports security-reports performance-reports

# Run the tests
run_tests $TEST_TYPE

# Check exit codes
if [ $? -eq 0 ]; then
    print_success "All tests completed successfully!"
    
    # Show results location
    print_status "Test results available at:"
    echo "  - Coverage reports: ./coverage-reports/"
    echo "  - Security reports: ./security-reports/"
    echo "  - Performance reports: ./performance-reports/"
    echo "  - Test results: ./test-results/"
    echo ""
    echo "View reports in browser:"
    echo "  docker-compose -f docker-compose.test.yml up test-viewer"
    echo "  Then open: http://localhost:8090"
    
else
    print_error "Some tests failed. Check the output above for details."
    exit 1
fi