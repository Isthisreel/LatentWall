import requests
import time
import json

BASE_URL = "http://localhost:8000"

def ensure_stream():
    print("Initializing stream session...")
    try:
        resp = requests.post(f"{BASE_URL}/stream/start", json={"prompt": "abstract energy", "portrait": True})
        if resp.ok:
            print("Stream session established.")
            # Give it a moment to stabilize
            time.sleep(5)
            return True
        else:
            print(f"Failed to start stream: {resp.text}")
            return False
    except Exception as e:
        print(f"Error starting stream: {e}")
        return False

def run_test(text="dragon"):
    print(f"--- Testing with: '{text}' ---")
    url = f"{BASE_URL}/speech-to-video"
    payload = {"text": text}
    
    start_time = time.perf_counter()
    try:
        resp = requests.post(url, json=payload, timeout=15)
        end_time = time.perf_counter()
        
        if resp.ok:
            data = resp.json()
            print(f"Success! Status: {data.get('status')}")
            print(f"Roundtrip Latency: {(end_time - start_time)*1000:.1f}ms")
            return True
        else:
            print(f"Error: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    if ensure_stream():
        # Test multiple words to get an average
        words = ["dragon", "fire", "ocean"]
        for word in words:
            run_test(word)
            time.sleep(2) 
    else:
        print("Aborting tests: No stream connection.")
