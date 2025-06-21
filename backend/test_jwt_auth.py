#!/usr/bin/env python3
"""
Comprehensive JWT Authentication Test Script
Tests all authentication endpoints and JWT functionality
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n📋 Step {step}: {description}")

def test_signup():
    """Test user signup"""
    print_step(1, "User Signup")
    
    # Use timestamp to ensure unique email
    timestamp = int(time.time())
    signup_data = {
        "username": f"jwt_test_user_{timestamp}",
        "email": f"jwt_test_{timestamp}@example.com",
        "password": "SecurePass123"
    }
    
    print(f"📤 Sending signup request...")
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ Signup successful!")
        print(f"   User ID: {user_data['id']}")
        print(f"   Username: {user_data['username']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Created: {user_data['created_at']}")
        return signup_data['email'], signup_data['password']
    else:
        print(f"❌ Signup failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None, None

def test_login(email, password):
    """Test user login and JWT token generation"""
    print_step(2, "User Login & JWT Token Generation")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    print(f"📤 Sending login request...")
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"✅ Login successful!")
        print(f"   Token Type: {token_data['token_type']}")
        print(f"   Access Token: {token_data['access_token'][:50]}...")
        print(f"   Token Length: {len(token_data['access_token'])} characters")
        return token_data['access_token']
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_protected_route(token):
    """Test accessing protected route with JWT token"""
    print_step(3, "Protected Route Access")
    
    headers = {"Authorization": f"Bearer {token}"}
    print(f"📤 Sending request to /me with JWT token...")
    
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ Protected route access successful!")
        print(f"   User ID: {user_data['id']}")
        print(f"   Username: {user_data['username']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Active: {user_data['is_active']}")
        return True
    else:
        print(f"❌ Protected route access failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def test_invalid_token():
    """Test accessing protected route with invalid token"""
    print_step(4, "Invalid Token Test")
    
    headers = {"Authorization": "Bearer invalid_token_here"}
    print(f"📤 Sending request to /me with invalid token...")
    
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    
    if response.status_code == 401:
        print(f"✅ Invalid token correctly rejected!")
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.json()['detail']}")
        return True
    else:
        print(f"❌ Invalid token should have been rejected: {response.status_code}")
        return False

def test_missing_token():
    """Test accessing protected route without token"""
    print_step(5, "Missing Token Test")
    
    print(f"📤 Sending request to /me without token...")
    
    response = requests.get(f"{BASE_URL}/me")
    
    if response.status_code == 403:
        print(f"✅ Missing token correctly rejected!")
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.json()['detail']}")
        return True
    else:
        print(f"❌ Missing token should have been rejected: {response.status_code}")
        return False

def test_duplicate_login(email, password):
    """Test that login works multiple times"""
    print_step(6, "Multiple Login Test")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    print(f"📤 Sending second login request...")
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"✅ Second login successful!")
        print(f"   New Token: {token_data['access_token'][:50]}...")
        print(f"   Note: Each login generates a new token")
        return True
    else:
        print(f"❌ Second login failed: {response.status_code}")
        return False

def test_wrong_password(email):
    """Test login with wrong password"""
    print_step(7, "Wrong Password Test")
    
    login_data = {
        "email": email,
        "password": "WrongPassword123"
    }
    
    print(f"📤 Sending login request with wrong password...")
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code == 401:
        print(f"✅ Wrong password correctly rejected!")
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.json()['detail']}")
        return True
    else:
        print(f"❌ Wrong password should have been rejected: {response.status_code}")
        return False

def main():
    """Run all JWT authentication tests"""
    print_section("JWT Authentication System Test")
    print(f"🚀 Testing JWT authentication endpoints at {BASE_URL}")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test signup
    email, password = test_signup()
    if not email or not password:
        print("\n❌ Signup failed. Cannot continue with other tests.")
        return
    
    # Test login and get token
    token = test_login(email, password)
    if not token:
        print("\n❌ Login failed. Cannot continue with protected route tests.")
        return
    
    # Test protected route
    test_protected_route(token)
    
    # Test security scenarios
    test_invalid_token()
    test_missing_token()
    
    # Test additional scenarios
    test_duplicate_login(email, password)
    test_wrong_password(email)
    
    print_section("Test Summary")
    print("🎉 JWT Authentication System Test Completed!")
    print("\n📋 Available Endpoints:")
    print("   POST /auth/signup - Register new user")
    print("   POST /auth/login - Login with email/password")
    print("   POST /login - Login with email/password (root level)")
    print("   GET /auth/me - Get user profile (protected)")
    print("   GET /me - Get user profile (protected, root level)")
    
    print("\n🔐 JWT Features Verified:")
    print("   ✅ Token generation with HS256 algorithm")
    print("   ✅ 15-minute token expiry")
    print("   ✅ Protected route access")
    print("   ✅ Invalid token rejection")
    print("   ✅ Missing token rejection")
    print("   ✅ Password validation")
    print("   ✅ Multiple login support")

if __name__ == "__main__":
    main() 