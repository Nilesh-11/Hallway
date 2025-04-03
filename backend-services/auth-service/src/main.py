from fastapi import FastAPI
from src.routes import user, googleauth
from src.database.connection import Base, engine

app = FastAPI(title="Auth Service")

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/user")
app.include_router(googleauth.router, prefix="/google")

@app.get("/")
def health_check():
    return {"status": "Auth Service is running"}
