#!/bin/bash
# Test script for all UniQuest APIs
# Tests camelCase JSON and authentication disabled

BASE_URL="http://localhost:8000/api"

echo "=========================================="
echo "UniQuest API Test Suite"
echo "Testing camelCase JSON and no authentication"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

test_endpoint() {
    local method=$1
    local url=$2
    local data=$3
    local description=$4
    local expected_status=${5:-200}
    
    echo "----------------------------------------"
    echo "Testing: $description"
    echo "$method $url"
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            -d "$data" 2>/dev/null)
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" 2>/dev/null)
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC} - Status $http_code"
        echo "Response: $(echo "$body" | head -c 200)..."
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} - Expected $expected_status, got $http_code"
        echo "Response: $body"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# Check if server is running
echo "Checking if server is running..."
if ! curl -s "$BASE_URL/healthz/" > /dev/null 2>&1; then
    echo -e "${RED}❌ Server is not running on $BASE_URL${NC}"
    echo "Please start the server with: python manage.py runserver"
    exit 1
fi
echo -e "${GREEN}✅ Server is running${NC}"
echo ""

# Test 1: Health Check
test_endpoint "GET" "$BASE_URL/healthz/" "" "Health Check" 200

# Test 2: Get Student Profile
test_endpoint "GET" "$BASE_URL/students/me/" "" "Get Student Profile" 200

# Test 3: Update Student Profile (camelCase)
PROFILE_DATA='{
  "academicLevel": "bachelors",
  "gpa": 3.8,
  "testScores": [
    {
      "examName": "IELTS",
      "score": 7.5,
      "testDate": "2024-06"
    }
  ],
  "preferredPrograms": ["Computer Science"],
  "budgetCurrency": "USD",
  "budgetMax": 40000
}'
test_endpoint "PATCH" "$BASE_URL/students/me/" "$PROFILE_DATA" "Update Student Profile (camelCase)" 200

# Test 4: Get Preferences
test_endpoint "GET" "$BASE_URL/students/preferences/" "" "Get Preferences" 200

# Test 5: Update Preferences (camelCase)
PREF_DATA='{
  "weights": {
    "academics": 0.35,
    "interests": 0.25,
    "career": 0.20,
    "location": 0.10,
    "budget": 0.05,
    "ranking": 0.03,
    "researchActivity": 0.02
  }
}'
test_endpoint "PUT" "$BASE_URL/students/preferences/" "$PREF_DATA" "Update Preferences (camelCase)" 200

# Test 6: Search Universities
test_endpoint "GET" "$BASE_URL/universities/?q=stanford&limit=5" "" "Search Universities" 200

# Test 7: List Recommendations
test_endpoint "GET" "$BASE_URL/recommendations/" "" "List Recommendations" 200

# Test 8: Generate Recommendations (camelCase)
REC_DATA='{
  "filters": {
    "countries": ["US"],
    "maxRank": 500,
    "budgetMax": 50000
  },
  "weights": {
    "academics": 0.30,
    "interests": 0.20,
    "researchActivity": 0.05
  },
  "topN": 5
}'
test_endpoint "POST" "$BASE_URL/recommendations/run/" "$REC_DATA" "Generate Recommendations (camelCase)" 200

# Test 9: List Feedback
test_endpoint "GET" "$BASE_URL/feedback/" "" "List Feedback" 200

# Test 10: List Ingestion Runs
test_endpoint "GET" "$BASE_URL/ingestion/runs/" "" "List Ingestion Runs" 200

# Test 11: Get API Schema
test_endpoint "GET" "$BASE_URL/schema/" "" "Get API Schema" 200

# Summary
echo ""
echo "=========================================="
echo "TEST SUMMARY"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Total: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some tests failed${NC}"
    exit 1
fi

