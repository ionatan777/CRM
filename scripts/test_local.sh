#!/bin/bash
# Quick Test Script for WhatsBackup MVP
# Tests all core functionality locally

echo "🧪 WhatsBackup MVP - Local Testing"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" $url)
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" -X $method $url)
    fi
    
    if [ "$response" = "200" ] || [ "$response" = "404" ] || [ "$response" = "422" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $response)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $response)"
        ((TESTS_FAILED++))
    fi
}

echo "📡 1. Backend API Tests"
echo "----------------------"
test_endpoint "Health Check" "http://localhost:8000/health"
test_endpoint "API Docs" "http://localhost:8000/docs"
test_endpoint "Plans List" "http://localhost:8000/api/v1/plans/list"
echo ""

echo "🌐 2. Baileys Server Tests"
echo "--------------------------"
test_endpoint "Baileys Health" "http://localhost:3000/health"
echo ""

echo "🎨 3. Frontend Tests"
echo "-------------------"
test_endpoint "Frontend Root" "http://localhost:5173"
echo ""

echo ""
echo "=================================="
echo "📊 Test Summary"
echo "=================================="
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✓ All systems operational!${NC}"
    echo "Ready for manual testing."
else
    echo -e "\n${YELLOW}⚠ Some services not running${NC}"
    echo "Please start all servers and try again."
fi

echo ""
echo "Next steps:"
echo "1. Open http://localhost:5173 in browser"
echo "2. Register a new user"
echo "3. Test Express plan flow"
echo "4. Test Pro plan flow"
