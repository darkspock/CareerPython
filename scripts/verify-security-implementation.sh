#!/bin/bash

# Security Implementation Verification Script
# Verifies that all security enhancements for task 18 are properly implemented

set -e

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
    echo -e "${GREEN}[✅ PASS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️  WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌ FAIL]${NC} $1"
}

# Verification results
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Function to verify file exists and has content
verify_file() {
    local file_path="$1"
    local description="$2"
    local required_content="$3"
    
    ((TOTAL_CHECKS++))
    
    if [ ! -f "$file_path" ]; then
        print_error "$description - File not found: $file_path"
        ((FAILED_CHECKS++))
        return 1
    fi
    
    if [ ! -s "$file_path" ]; then
        print_error "$description - File is empty: $file_path"
        ((FAILED_CHECKS++))
        return 1
    fi
    
    if [ -n "$required_content" ]; then
        if ! grep -q "$required_content" "$file_path"; then
            print_error "$description - Required content not found in: $file_path"
            ((FAILED_CHECKS++))
            return 1
        fi
    fi
    
    print_success "$description"
    ((PASSED_CHECKS++))
    return 0
}

# Function to verify Docker setup
verify_docker_setup() {
    local description="$1"
    
    ((TOTAL_CHECKS++))
    
    if ! command -v docker &> /dev/null; then
        print_error "$description - Docker not installed"
        ((FAILED_CHECKS++))
        return 1
    fi
    
    if ! docker info > /dev/null 2>&1; then
        print_error "$description - Docker not running"
        ((FAILED_CHECKS++))
        return 1
    fi
    
    print_success "$description"
    ((PASSED_CHECKS++))
    return 0
}

print_status "🔒 Security Implementation Verification"
print_status "======================================"

# 1. Verify subscription-based authorization files
print_status "1. Verifying Subscription-Based Authorization Implementation"
verify_file "src/shared/infrastructure/security/subscription_authorization.py" \
    "Subscription Authorization Service" \
    "SubscriptionAuthorizationService"

verify_file "src/auth/application/auth.py" \
    "Enhanced Auth Service with Subscription Support" \
    "create_access_token_with_subscription"

# 2. Verify AI content validation files
print_status "2. Verifying AI Content Validation Implementation"
verify_file "src/shared/infrastructure/security/ai_content_validator.py" \
    "AI Content Validator" \
    "AIContentValidator"

# 3. Verify enhanced middleware
print_status "3. Verifying Enhanced Middleware Implementation"
verify_file "presentation/middleware/subscription_middleware.py" \
    "Enhanced Subscription Middleware" \
    "EnhancedSubscriptionMiddleware"

# 4. Verify data retention policies
print_status "4. Verifying Data Retention Policy Implementation"
verify_file "src/shared/infrastructure/security/data_retention_policy.py" \
    "Data Retention Policy Service" \
    "DataRetentionPolicyService"

# 5. Verify test files
print_status "5. Verifying Security Test Implementation"
verify_file "tests/unit/shared/test_subscription_security.py" \
    "Subscription Security Unit Tests" \
    "TestSubscriptionAuthorizationService"

verify_file "tests/integration/test_enhanced_security_middleware.py" \
    "Enhanced Security Middleware Integration Tests" \
    "TestEnhancedSubscriptionMiddleware"

# 6. Verify Docker test setup
print_status "6. Verifying Docker Test Configuration"
verify_file "docker-compose.test.yml" \
    "Docker Compose Test Configuration" \
    "test-runner"

verify_file "docker/testing/Dockerfile.test" \
    "Docker Test Image Configuration" \
    "pytest"

verify_file "requirements-test.txt" \
    "Test Dependencies" \
    "pytest"

# 7. Verify test scripts
print_status "7. Verifying Test Scripts"
verify_file "scripts/run-tests.sh" \
    "Enhanced Test Runner Script" \
    "docker-compose"

verify_file "scripts/run-ai-tests.sh" \
    "AI Test Runner Script with Docker" \
    "docker-compose"

verify_file "Makefile.test" \
    "Test Makefile" \
    "test-security"

# 8. Verify documentation
print_status "8. Verifying Security Documentation"
verify_file "docs/SECURITY_ENHANCEMENTS.md" \
    "Security Enhancements Documentation" \
    "Subscription-Based Authorization"

# 9. Verify Docker environment
print_status "9. Verifying Docker Environment"
verify_docker_setup "Docker Installation and Status"

# 10. Verify specific security implementations
print_status "10. Verifying Specific Security Features"

# Check for subscription authorization in auth service
if grep -q "validate_subscription_access" "src/auth/application/auth.py"; then
    print_success "Subscription validation in auth service"
    ((PASSED_CHECKS++))
else
    print_error "Subscription validation missing in auth service"
    ((FAILED_CHECKS++))
fi
((TOTAL_CHECKS++))

# Check for content validation patterns
if grep -q "SECURITY_PATTERNS" "src/shared/infrastructure/security/ai_content_validator.py"; then
    print_success "Security patterns in content validator"
    ((PASSED_CHECKS++))
else
    print_error "Security patterns missing in content validator"
    ((FAILED_CHECKS++))
fi
((TOTAL_CHECKS++))

# Check for rate limiting in middleware
if grep -q "_check_rate_limit" "presentation/middleware/subscription_middleware.py"; then
    print_success "Rate limiting in enhanced middleware"
    ((PASSED_CHECKS++))
else
    print_error "Rate limiting missing in enhanced middleware"
    ((FAILED_CHECKS++))
fi
((TOTAL_CHECKS++))

# Check for data retention policies
if grep -q "DEFAULT_POLICIES" "src/shared/infrastructure/security/data_retention_policy.py"; then
    print_success "Default retention policies defined"
    ((PASSED_CHECKS++))
else
    print_error "Default retention policies missing"
    ((FAILED_CHECKS++))
fi
((TOTAL_CHECKS++))

# 11. Run a quick syntax check on key files
print_status "11. Running Syntax Validation"

key_files=(
    "src/shared/infrastructure/security/subscription_authorization.py"
    "src/shared/infrastructure/security/ai_content_validator.py"
    "src/shared/infrastructure/security/data_retention_policy.py"
    "presentation/middleware/subscription_middleware.py"
)

for file in "${key_files[@]}"; do
    ((TOTAL_CHECKS++))
    if python -m py_compile "$file" 2>/dev/null; then
        print_success "Syntax check: $(basename "$file")"
        ((PASSED_CHECKS++))
    else
        print_error "Syntax error in: $file"
        ((FAILED_CHECKS++))
    fi
done

# 12. Verify test execution capability
print_status "12. Verifying Test Execution Capability"

((TOTAL_CHECKS++))
if [ -x "scripts/run-tests.sh" ]; then
    print_success "Test runner script is executable"
    ((PASSED_CHECKS++))
else
    print_error "Test runner script is not executable"
    ((FAILED_CHECKS++))
fi

((TOTAL_CHECKS++))
if [ -x "scripts/run-ai-tests.sh" ]; then
    print_success "AI test runner script is executable"
    ((PASSED_CHECKS++))
else
    print_error "AI test runner script is not executable"
    ((FAILED_CHECKS++))
fi

# Generate summary report
print_status ""
print_status "Verification Summary"
print_status "==================="
echo "Total checks: $TOTAL_CHECKS"
echo "Passed: $PASSED_CHECKS"
echo "Failed: $FAILED_CHECKS"

if [ $FAILED_CHECKS -eq 0 ]; then
    print_success "🎉 All security implementation checks passed!"
    print_status ""
    print_status "Next steps:"
    echo "1. Run security tests: make test-security"
    echo "2. Run AI tests: make test-ai"
    echo "3. Run full test suite: make test-all"
    echo "4. View test results: make viewer"
    print_status ""
    print_status "Task 18 implementation appears to be complete! ✅"
    exit 0
else
    print_error "❌ Some security implementation checks failed!"
    print_status ""
    print_status "Please address the failed checks above before proceeding."
    print_status "Failed checks: $FAILED_CHECKS/$TOTAL_CHECKS"
    exit 1
fi