#!/usr/bin/env python
"""
Test script to verify API endpoints are working correctly.
"""

import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    """Test all the required endpoints."""
    
    print("Testing API endpoints...")
    
    # Test 1: Books list (should work without authentication)
    print("\n1. Testing GET /api/books/ (should work without auth)")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/books/")
        print(f"   Status: {response.status}")
        if response.status == 200:
            print("   ✓ Books list endpoint working")
        else:
            print(f"   ✗ Failed: {response.read().decode()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 2: Books update (should require authentication)
    print("\n2. Testing PUT /api/books/update/ (should require auth)")
    try:
        data = json.dumps({"title": "Test Book", "publication_year": 2020, "author": 1}).encode('utf-8')
        req = urllib.request.Request(
            f"{BASE_URL}/books/update/",
            data=data,
            method='PUT',
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req)
        print(f"   Status: {response.status}")
        print(f"   ✗ Unexpected success: {response.read().decode()}")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print(f"   Status: {e.code}")
            print("   ✓ Update endpoint properly requires authentication")
        else:
            print(f"   ✗ Unexpected status: {e.code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 3: Books delete (should require authentication)
    print("\n3. Testing DELETE /api/books/delete/ (should require auth)")
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/books/delete/",
            method='DELETE'
        )
        response = urllib.request.urlopen(req)
        print(f"   Status: {response.status}")
        print(f"   ✗ Unexpected success: {response.read().decode()}")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print(f"   Status: {e.code}")
            print("   ✓ Delete endpoint properly requires authentication")
        else:
            print(f"   ✗ Unexpected status: {e.code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 4: Books create (should require authentication)
    print("\n4. Testing POST /api/books/create/ (should require auth)")
    try:
        data = json.dumps({"title": "Test Book", "publication_year": 2020, "author": 1}).encode('utf-8')
        req = urllib.request.Request(
            f"{BASE_URL}/books/create/",
            data=data,
            method='POST',
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req)
        print(f"   Status: {response.status}")
        print(f"   ✗ Unexpected success: {response.read().decode()}")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print(f"   Status: {e.code}")
            print("   ✓ Create endpoint properly requires authentication")
        else:
            print(f"   ✗ Unexpected status: {e.code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 5: Books detail (should work without authentication)
    print("\n5. Testing GET /api/books/1/ (should work without auth)")
    try:
        response = urllib.request.urlopen(f"{BASE_URL}/books/1/")
        print(f"   Status: {response.status}")
        if response.status == 200:
            print("   ✓ Books detail endpoint working")
        else:
            print(f"   ✗ Failed: {response.read().decode()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "="*50)
    print("API Endpoint Testing Complete!")
    print("="*50)

if __name__ == "__main__":
    test_endpoints() 