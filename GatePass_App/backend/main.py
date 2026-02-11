from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ✅ FIXED IMPORTS (relative)
from .auth import router as auth_router
from .db import create_tables

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_router)

# Root check
@app.get("/")
def home():
    return {"message": "Gate Pass System Backend is Running 🚀"}

# Startup event
@app.on_event("startup")
def startup():
    create_tables()

# For local run only
if __name__ == "__main__":
    uvicorn.run("GatePass_App.backend.main:app", host="0.0.0.0", port=8000)
