#!/usr/bin/env python
"""
Test script to verify all UniQuest APIs are working correctly.
Tests camelCase JSON conversion and authentication disabled.
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_endpoint(method, url, data=None, expected_status=200, description=""):
    """Test an API endpoint."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{method} {url}")
    if data:
        print(f"Request Body: {json.dumps(data, indent=2)}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"}, timeout=5)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers={"Content-Type": "application/json"}, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, headers={"Content-Type": "application/json"}, timeout=5)
        else:
            print(f"❌ Unknown method: {method}")
            return False
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"✅ PASS - Status {response.status_code}")
            try:
                response_json = response.json()
                print(f"Response: {json.dumps(response_json, indent=2)[:500]}...")
                
                # Check if response uses camelCase
                if isinstance(response_json, dict):
                    has_camel_case = any(key[0].islower() and any(c.isupper() for c in key[1:]) for key in response_json.keys())
                    if has_camel_case:
                        print("✅ PASS - Response uses camelCase")
                    else:
                        print("⚠️  WARNING - Response might not use camelCase (could be empty or simple keys)")
                
                return True
            except json.JSONDecodeError:
                print(f"Response: {response.text[:200]}")
                return True
        else:
            print(f"❌ FAIL - Expected {expected_status}, got {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ FAIL - Cannot connect to server. Is it running on {BASE_URL}?")
        return False
    except Exception as e:
        print(f"❌ FAIL - Error: {str(e)}")
        return False

def main():
    """Run all API tests."""
    print("="*60)
    print("UniQuest API Test Suite")
    print("Testing camelCase JSON and authentication disabled")
    print("="*60)
    
    results = []
    
    # Test 1: Health Check
    results.append((
        test_endpoint("GET", f"{BASE_URL}/healthz/", expected_status=200, description="Health Check"),
        "Health Check"
    ))
    
    # Test 2: Get Student Profile (should work without auth)
    results.append((
        test_endpoint("GET", f"{BASE_URL}/students/me/", expected_status=200, description="Get Student Profile"),
        "Get Student Profile"
    ))
    
    # Test 3: Create/Update Student Profile with camelCase
    profile_data = {
        "academicLevel": "bachelors",
        "gpa": 3.8,
        "academicBackground": [
            {
                "id": "101",
                "level": "high-school",
                "course": "Science Stream",
                "institution": "Test School",
                "yearOfCompletion": "2024",
                "gpa": 3.8
            }
        ],
        "workExperience": [],
        "testScores": [
            {
                "examName": "IELTS",
                "score": 7.5,
                "testDate": "2024-06"
            }
        ],
        "interests": "Computer Science",
        "preferredPrograms": ["Computer Science", "Engineering"],
        "goals": "To study computer science",
        "preferredRegions": ["US", "CA"],
        "preferredCountries": ["United States", "Canada"],
        "countryPreference": "US",
        "campusPreference": ["Urban"],
        "budgetCurrency": "USD",
        "budgetMin": 0,
        "budgetMax": 40000
    }
    results.append((
        test_endpoint("PATCH", f"{BASE_URL}/students/me/", data=profile_data, expected_status=200, description="Update Student Profile (camelCase)"),
        "Update Student Profile (camelCase)"
    ))
    
    # Test 4: Get Preferences
    results.append((
        test_endpoint("GET", f"{BASE_URL}/students/preferences/", expected_status=200, description="Get Preferences"),
        "Get Preferences"
    ))
    
    # Test 5: Update Preferences with camelCase
    preferences_data = {
        "weights": {
            "academics": 0.35,
            "interests": 0.25,
            "career": 0.20,
            "location": 0.10,
            "budget": 0.05,
            "ranking": 0.03,
            "researchActivity": 0.02
        }
    }
    results.append((
        test_endpoint("PUT", f"{BASE_URL}/students/preferences/", data=preferences_data, expected_status=200, description="Update Preferences (camelCase)"),
        "Update Preferences (camelCase)"
    ))
    
    # Test 6: Search Universities
    results.append((
        test_endpoint("GET", f"{BASE_URL}/universities/?q=stanford&limit=5", expected_status=200, description="Search Universities"),
        "Search Universities"
    ))
    
    # Test 7: Get Recommendations List
    results.append((
        test_endpoint("GET", f"{BASE_URL}/recommendations/", expected_status=200, description="List Recommendations"),
        "List Recommendations"
    ))
    
    # Test 8: Generate Recommendations with camelCase
    recommendation_data = {
        "filters": {
            "countries": ["US"],
            "maxRank": 500,
            "budgetMax": 50000
        },
        "weights": {
            "academics": 0.30,
            "interests": 0.20,
            "career": 0.20,
            "location": 0.15,
            "budget": 0.10,
            "ranking": 0.03,
            "researchActivity": 0.02
        },
        "topN": 5
    }
    results.append((
        test_endpoint("POST", f"{BASE_URL}/recommendations/run/", data=recommendation_data, expected_status=200, description="Generate Recommendations (camelCase)"),
        "Generate Recommendations (camelCase)"
    ))
    
    # Test 9: Get Feedback List
    results.append((
        test_endpoint("GET", f"{BASE_URL}/feedback/", expected_status=200, description="List Feedback"),
        "List Feedback"
    ))
    
    # Test 10: Get Ingestion Runs
    results.append((
        test_endpoint("GET", f"{BASE_URL}/ingestion/runs/", expected_status=200, description="List Ingestion Runs"),
        "List Ingestion Runs"
    ))
    
    # Test 11: API Schema
    results.append((
        test_endpoint("GET", f"{BASE_URL}/schema/", expected_status=200, description="Get API Schema"),
        "Get API Schema"
    ))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for result, _ in results if result)
    total = len(results)
    
    for result, name in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

