from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def receive_event(request: Request):
    event_data = await request.json()
    print("Received event:", event_data)
    # You can store it in a database (e.g., MongoDB, PostgreSQL)
    return {"status": "success", "message": "Event received"}
