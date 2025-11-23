#!/usr/bin/env python3
import requests
import json

# Simple test
try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": "Say hello",
            "stream": False
        },
        timeout=10
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data.get('response', 'No response')[:100]}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")