from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# --- ADD THIS BLOCK ---
@app.get("/")
async def health_check():
    print("Health check received!")
    return {"status": "ok"}
# ----------------------

@app.post("/receive")
async def receive_event(request: Request):
    data = await request.json()
    print(f"Event received: {data}")
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6000)
