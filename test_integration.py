# test_integration.py
import threading
import time
import requests
import sys
from app import app  # <-- your Flask app

def run_server():
    """Run Flask in a thread"""
    app.run(host="127.0.0.1", port=5000, use_reloader=False, debug=False)

def wait_for_server(url="http://127.0.0.1:5000/health", timeout=30):
    """Wait until /health returns 200"""
    print(f"Waiting for server at {url}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                print("Server is ready!")
                return True
        except:
            time.sleep(0.5)
    print("Server failed to start in time.")
    return False

def run_client_tests():
    """Your actual client logic"""
    print("Running client tests...")
    try:
        r = requests.get("http://127.0.0.1:5000/")
        assert r.status_code == 200
        assert r.json()["message"] == "Hello from Windows CI!"
        print("Home endpoint: PASS")

        h = requests.get("http://127.0.0.1:5000/health")
        assert h.status_code == 200
        assert h.json()["status"] == "ok"
        print("Health endpoint: PASS")

        print("ALL TESTS PASSED!")
        return True
    except Exception as e:
        print(f"TEST FAILED: {e}")
        return False

if __name__ == "__main__":
    # 1. Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # 2. Wait for it to be ready
    if not wait_for_server():
        sys.exit(1)

    # 3. Run client tests
    if not run_client_tests():
        sys.exit(1)

    # 4. Done — thread exits with process
    sys.exit(0)
