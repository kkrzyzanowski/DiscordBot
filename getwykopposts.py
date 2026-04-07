import requests
import os

CLIENT_ID = os.getenv("WYKOP_CLIENT_ID")
CLIENT_SECRET = os.getenv("WYKOP_CLIENT_SECRET")

print(f"CLIENT_ID: {CLIENT_ID}")
print(f"CLIENT_SECRET: {CLIENT_SECRET}")

def get_wykop_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("WYKOP_CLIENT_ID lub WYKOP_CLIENT_SECRET nie jest ustawione.")

    response = requests.post(
        "https://wykop.pl/api/v3/auth",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        },
        json={
            "data": {
                "key": CLIENT_ID,
                "secret": CLIENT_SECRET
            }
        }
    )

    try:
        payload = response.json()
    except ValueError:
        raise ValueError(f"Nieprawidłowa odpowiedź Wykop podczas logowania: {response.text}")

    if response.status_code != 200 or "data" not in payload:
        error_message = payload.get("error") or payload
        raise ValueError(f"Błąd autoryzacji Wykop: {error_message}")

    return payload["data"]["token"]


def get_top_wykop_entries(limit=5):
    token = get_wykop_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }

    response = requests.get(
        "https://wykop.pl/api/v3/entries?page=1&limit=5&multimedia=false",
        headers=headers
    )

    try:
        data = response.json()
    except ValueError:
        raise ValueError(f"Nieprawidłowa odpowiedź Wykop przy pobieraniu wpisów: {response.text}")

    if response.status_code != 200 or "data" not in data:
        error_message = data.get("error") or data
        raise ValueError(f"Błąd pobierania wpisów Wykop: {error_message}")

    entries = data["data"]

    top_entries = sorted(
        entries,
        key=lambda e: e["votes"]["up"],
        reverse=True
    )[:limit]

    return top_entries