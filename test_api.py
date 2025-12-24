#!/usr/bin/env python
"""
Simple API test script for KnowledgeHub
Run this after starting the development server to test basic functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_registration():
    """Test user registration"""
    url = f"{BASE_URL}/api/auth/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpass123",
        "password2": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Registration: {response.status_code}")
        if response.status_code == 201:
            print("✅ Registration successful")
            return True
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: python manage.py runserver")
        return False

def test_login():
    """Test user login"""
    url = f"{BASE_URL}/api/auth/login/"
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            token = response.json().get('access')
            print("✅ Login successful")
            return token
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Server not running")
        return None

def test_workspace_creation(token):
    """Test workspace creation"""
    url = f"{BASE_URL}/api/workspaces/create/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Test Workspace",
        "description": "A test workspace"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Workspace creation: {response.status_code}")
        if response.status_code == 201:
            workspace_id = response.json().get('id')
            print("✅ Workspace creation successful")
            return workspace_id
        else:
            print(f"❌ Workspace creation failed: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Server not running")
        return None

def main():
    print("🚀 Testing KnowledgeHub API...")
    print("=" * 50)
    
    # Test registration (might fail if user exists)
    test_registration()
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test workspace creation
    workspace_id = test_workspace_creation(token)
    if workspace_id:
        print(f"✅ Created workspace with ID: {workspace_id}")
    
    print("=" * 50)
    print("🎉 Basic API tests completed!")
    print("\nTo run full tests:")
    print("1. Start server: python manage.py runserver")
    print("2. Run this script: python test_api.py")

if __name__ == "__main__":
    main()