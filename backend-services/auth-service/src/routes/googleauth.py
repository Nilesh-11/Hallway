from fastapi import APIRouter, HTTPException, Depends
from authlib.integrations.starlette_client import OAuth
from src.config.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
from sqlalchemy.orm import Session
from src.database.connection import get_db

router = APIRouter()
oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    userinfo_url="https://www.googleapis.com/oauth2/v3/userinfo",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/")
def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&scope=email profile openid"
    )
    return {"auth_url": google_auth_url}

@router.get("/callback")
async def auth_callback(code: str, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)
        return {"message": "User logged in", "user": user_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))