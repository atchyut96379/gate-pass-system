from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .db import create_tables;

# ✅ Correct relative import
from .auth import router as auth_router

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

# Root endpoint
@app.get("/")
def home():
    return {"message": "Gate Pass System Backend is Running 🚀"}

# Local run
if __name__ == "__main__":
    uvicorn.run("GatePass_App.backend.main:app", host="0.0.0.0", port=8000)

create_tables()
