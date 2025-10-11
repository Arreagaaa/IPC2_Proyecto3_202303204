"""
Test script for backend API
Run manually after starting backend with: python backend/app.py
"""
import requests
import time

print("=" * 60)
print("TEST A: Sending example_config.xml to backend")
print("=" * 60)

# Read example XML
with open('backend/instance/data/example_config.xml', 'rb') as f:
    xml_content = f.read()

# Send to backend
try:
    response = requests.post(
        'http://127.0.0.1:5001/api/crearConfiguracion',
        data=xml_content,
        headers={'Content-Type': 'application/xml'},
        timeout=5
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    
    # Check db.xml
    print("\n" + "=" * 60)
    print("DATABASE CONTENT (db.xml)")
    print("=" * 60)
    try:
        with open('backend/instance/data/db.xml', 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print("db.xml not found yet")
    
    print("\nTEST A: PASSED")
    
except requests.exceptions.ConnectionError:
    print("\nERROR: Could not connect to backend.")
    print("Make sure backend is running: python backend/app.py")
    print("TEST A: FAILED")
except Exception as e:
    print(f"\nERROR: {e}")
    print("TEST A: FAILED")
