from src.config import AUTH_SERVICE_URL
import httpx
from src.config import AUTH_SERVICE_URL

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}

async def forward_auth_request(path: str, data):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{AUTH_SERVICE_URL}{path}", json=data, headers=headers)
        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()
        else:
            print("Invalid response format from auth service")
            return {'type': "error", "details": "An error occurred", "status_code": response.status_code}
    except Exception as e:
        print("Failed to connect to auth service: ", e)
        return {'type':"error", 'details': f"An error occured", 'status_code': 503}
