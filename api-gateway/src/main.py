from fastapi import FastAPI
# from src.routes import chat, files, study_rooms
from src.routes import auth

app = FastAPI(title="API Gateway")

app.include_router(auth.router, prefix="/api/auth")

@app.get("/")
def health_check():
    return {"status": "API Gateway is running"}
