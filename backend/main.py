from fastapi import FastAPI
from dotenv import load_dotenv
import os
from auth import router as auth_router

load_dotenv()

app = FastAPI(title="Wrapped for GitHub")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Wrapped for GitHub API running 🚀"}

@app.get("/health")
def health():
    return {
        "client_id_loaded": bool(os.getenv("GITHUB_CLIENT_ID")),
        "client_secret_loaded": bool(os.getenv("GITHUB_CLIENT_SECRET"))
    }

