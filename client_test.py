import requests

def test_server():
    response = requests.get("http://localhost:5000/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello from Flask!"

    health = requests.get("http://localhost:5000/health")
    assert health.json()["status"] == "ok"

if __name__ == "__main__":
    test_server()
    print("All tests passed!")
