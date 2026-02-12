from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .db import create_tables
from .auth import router as auth_router

app = FastAPI()

# ✅ Correct CORS Configuration
origins = [
    "https://dashing-brigadeiros-a3f53c.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Gate Pass System Backend is Running 🚀"}

# Create tables when app starts
@app.on_event("startup")
def startup_event():
    create_tables()

# Local run
if __name__ == "__main__":
    uvicorn.run("GatePass_App.backend.main:app", host="0.0.0.0", port=8000)