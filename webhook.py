import httpx
import base64
from fastapi import FastAPI, Request

app = FastAPI()

UNOMI_URL = "https://cce8-14-97-189-166.ngrok-free.app/cxs/profiles"  # Apache Unomi Profiles Endpoint

# Encode Basic Auth (username:password -> karaf:karaf)
auth_header = f"Basic {base64.b64encode(b'karaf:karaf').decode()}"

@app.post("/webhook")
async def receive_event(request: Request):
    try:
        event_data = await request.json()
        print("Received event from SendGrid:", event_data)

        # Construct Unomi-compatible payload
        unomi_payload = {
            "itemId": "clickedPolicydata",
            "itemType": "profile",
            "version": 2,
            "properties": event_data
        }

        # Set headers with Authorization
        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json"
        }

        # Send data to Apache Unomi
        async with httpx.AsyncClient() as client:
            response = await client.post(UNOMI_URL, json=unomi_payload, headers=headers)

            if response.status_code in [200, 201]:
                print("Data successfully saved to Unomi:", response.json())
                return {"status": "success", "message": "Event received and saved to Unomi"}
            else:
                print("Failed to save data to Unomi. Status:", response.status_code, response.text)
                return {"status": "error", "message": response.text}

    except Exception as e:
        print("Error:", str(e))
        return {"status": "error", "message": str(e)}
