import requests

BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = "cc8abc31dce6880188f6d71136717516e2697697"

HEADERS = {
    "Authorization": f"Token {TOKEN}"
}

def upload_csv(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/upload/",
            headers=HEADERS,
            files={"file": f}
        )
    response.raise_for_status()
    return response.json()

def get_history():
    response = requests.get(
        f"{BASE_URL}/history/",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()
