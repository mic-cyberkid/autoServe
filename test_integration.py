# test_integration.py
import subprocess
import time
import requests
import sys
import os

def start_server():
    """Start Flask server as a real subprocess"""
    print("Starting Flask server...")
    # Use python -m flask or direct script
    cmd = [sys.executable, "app.py"]
    env = os.environ.copy()
    env["FLASK_ENV"] = "production"  # Optional
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

def wait_for_server(url="http://127.0.0.1:5000/health", timeout=30):
    print(f"Waiting for server at {url}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                print("Server is ready!")
                return True
        except:
            time.sleep(0.5)
    print("Server did not start in time.")
    return False

def run_client_tests():
    print("Running client tests...")
    try:
        r = requests.get("http://127.0.0.1:5000/")
        assert r.status_code == 200
        data = r.json()
        expected = "Hello from Windows CI!" if "Windows" in os.name else "Hello from Flask!"
        assert data.get("message") == expected
        print("Home endpoint: PASS")

        h = requests.get("http://127.0.0.1:5000/health")
        assert h.status_code == 200
        assert h.json().get("status") == "ok"
        print("Health endpoint: PASS")

        print("ALL TESTS PASSED!")
        return True
    except Exception as e:
        print(f"TEST FAILED: {e}")
        return False

if __name__ == "__main__":
    # 1. Start server as subprocess
    server = start_server()

    # 2. Stream logs in real-time
    def stream_logs():
        for line in server.stdout:
            print(line.rstrip())

    import threading
    log_thread = threading.Thread(target=stream_logs, daemon=True)
    log_thread.start()

    # 3. Wait for health
    if not wait_for_server():
        server.terminate()
        sys.exit(1)

    # 4. Run client
    success = run_client_tests()

    # 5. Cleanup
    server.terminate()
    try:
        server.wait(timeout=5)
    except:
        server.kill()

    sys.exit(0 if success else 1)
