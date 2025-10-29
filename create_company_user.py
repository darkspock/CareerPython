#!/usr/bin/env python3
"""
Script to create a company user for testing
"""
import requests
import json

# Configuration
API_BASE = "http://localhost:8000"
COMPANY_ID = "01K8S21N86MQQDG0B5KRK6YMB1"

def create_company_user():
    """Create a company user"""
    url = f"{API_BASE}/api/company-users/{COMPANY_ID}/users"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer test-token"
    }
    
    user_data = {
        "user_id": "01K8S21N86MQQDG0B5KRK6YMB1",  # Using company ID as user ID
        "role_id": "01K8S21N86MQQDG0B5KRK6YMB1",  # Using company ID as role ID
        "is_active": True
    }
    
    try:
        response = requests.post(url, json=user_data, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print(f"✅ Created company user: {result.get('id', 'unknown')}")
            return result
        else:
            print(f"❌ Failed to create company user: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating company user: {e}")
        return None

def main():
    print("🚀 Creating company user...")
    print(f"Company ID: {COMPANY_ID}")
    print(f"API Base: {API_BASE}")
    print("-" * 50)
    
    result = create_company_user()
    if result:
        print("✅ Company user created successfully!")
        print(f"User ID: {result.get('id')}")
    else:
        print("❌ Failed to create company user")

if __name__ == "__main__":
    main()