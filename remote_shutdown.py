"""
Remote Graceful Shutdown Script for Koyeb Deployment
Triggers shutdown via HTTP endpoint
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def trigger_shutdown():
    backend_url = os.getenv("BACKEND_URL", "https://fiscal-darice-atoolworker-26d3b1bc.koyeb.app")
    admin_secret = os.getenv("ADMIN_SECRET")
    
    if not admin_secret:
        print("❌ ERROR: ADMIN_SECRET not set in environment")
        print("Set ADMIN_SECRET in your .env file")
        return False
    
    shutdown_url = f"{backend_url}/admin/shutdown"
    
    print("="*60)
    print("REMOTE GRACEFUL SHUTDOWN")
    print("="*60)
    print(f"Target: {backend_url}")
    print("="*60)
    
    confirm = input("\nTrigger graceful shutdown? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Shutdown cancelled.")
        return False
    
    print("\nSending shutdown request...")
    
    try:
        response = requests.post(
            shutdown_url,
            headers={
                "Authorization": f"Bearer {admin_secret}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS")
            print(f"Message: {data.get('message')}")
            print("\nBackend will:")
            print("1. Activate maintenance mode (no new jobs)")
            print("2. Wait for running jobs to complete")
            print("3. Shut down gracefully")
            return True
        else:
            print(f"\n❌ FAILED: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend")
        print(f"Check if {backend_url} is accessible")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    trigger_shutdown()
