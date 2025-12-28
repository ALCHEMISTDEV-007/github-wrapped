from fastapi import FastAPI

app = FastAPI(title="GitHub Wrapped API")

@app.get("/")
def root():
    return {
        "message": "GitHub Wrapped API is running 🚀"
    }
