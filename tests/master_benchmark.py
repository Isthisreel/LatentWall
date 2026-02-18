import requests
import time
import os
import json

BASE_URL = "http://localhost:8000"

def setup_session():
    print("🚀 Initializing Odyssey Stream...")
    try:
        resp = requests.post(f"{BASE_URL}/stream/start", json={"prompt": "benchmark run", "portrait": True})
        if resp.ok:
            print("✅ Stream initialized. Waiting 10s for stability...")
            time.sleep(10)
            return True
        print(f"❌ Failed to start: {resp.text}")
        return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def set_turbo(enabled):
    requests.post(f"{BASE_URL}/turbo", params={"enabled": enabled})
    print(f"⚙️ Mode set to: {'Turbo (Nano)' if enabled else 'Normal'}")

def run_benchmark():
    print("🧪 Triggering internal metrics capture...")
    resp = requests.post(f"{BASE_URL}/benchmark")
    if resp.ok:
        data = resp.json()
        print(f"✅ Results: {json.dumps(data.get('results'), indent=2)}")
    else:
        print(f"❌ Benchmark failed: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    # Clear old results
    if os.path.exists("latency.txt"):
        os.remove("latency.txt")
        
    if setup_session():
        # Test 1: Super Turbo
        set_turbo(True)
        run_benchmark()
        
        # Test 2: Normal
        set_turbo(False)
        run_benchmark()
        
        print("\n🏁 BENCHMARK COMPLETE. Results in latency.txt")
    else:
        print("Aborting: Could not establish session.")
