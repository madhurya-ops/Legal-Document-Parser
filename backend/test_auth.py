#!/usr/bin/env python3
"""
Test script for authentication endpoints
Run this after starting the server to test the authentication system
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    """Test user signup"""
    print("Testing signup...")
    
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    
    if response.status_code == 200:
        print("✅ Signup successful!")
        print(f"Response: {response.json()}")
        return True
    else:
        print(f"❌ Signup failed: {response.status_code}")
        print(f"Error: {response.text}")
        return False

def test_login():
    """Test user login"""
    print("\nTesting login...")
    
    login_data = {
        "email": "test@example.com",
        "password": "TestPass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        print("✅ Login successful!")
        token_data = response.json()
        print(f"Token: {token_data['access_token'][:50]}...")
        return token_data['access_token']
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Error: {response.text}")
        return None

def test_profile(token):
    """Test getting user profile"""
    print("\nTesting profile retrieval...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    if response.status_code == 200:
        print("✅ Profile retrieval successful!")
        print(f"User data: {response.json()}")
        return True
    else:
        print(f"❌ Profile retrieval failed: {response.status_code}")
        print(f"Error: {response.text}")
        return False

def test_duplicate_signup():
    """Test duplicate signup (should fail)"""
    print("\nTesting duplicate signup...")
    
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    
    if response.status_code == 400:
        print("✅ Duplicate signup correctly rejected!")
        return True
    else:
        print(f"❌ Duplicate signup should have failed: {response.status_code}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Authentication System")
    print("=" * 40)
    
    # Test signup
    if not test_signup():
        return
    
    # Test duplicate signup
    test_duplicate_signup()
    
    # Test login
    token = test_login()
    if not token:
        return
    
    # Test profile
    test_profile(token)
    
    print("\n" + "=" * 40)
    print("🎉 All tests completed!")

if __name__ == "__main__":
    main() 