# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hi Autonex Backend")

# Allow cross-origin requests from Electron's renderer (file://) and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, lock this down.
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/hello")
async def hello():
    return {"message": "Hi Autonex"}
