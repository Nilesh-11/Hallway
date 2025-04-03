from src.utils.auth import hash_password
from src.utils.jwt import create_jwt
from src.config.config import otp_expiration_time, otp_resend_time
from src.models.user import User, Otp
from src.schemas.request import UserSignupRequest, VerifyotpRequest, ResendOtpRequest, LoginRequest
from src.database.connection import get_db
from src.utils.mail import send_gmail_otp
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import datetime

router = APIRouter()

@router.post("/signup")
def signupwithCredentials(data: UserSignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    first_name = data.first_name
    last_name = data.last_name
    password = data.password
    email = data.email
    ip_addr = data.ip_addr
    user_agent = data.user_agent
    hashed_password = hash_password(password)
    
    try:
        existing_otp = db.query(Otp).filter(Otp.email == email, Otp.is_used == False).first()
        if existing_otp:
            if existing_otp.exp_time <= datetime.datetime.utcnow():
                db.delete(existing_otp)
                db.commit()
            else:
                return {"type": "invalid", 'status_code': 400, "detail": "Otp already sent, check email"}
        
        mail_response = send_gmail_otp(email)
        if mail_response['type'] != 'ok':
            return {"type": "error", 'status_code': 400, "detail": "Otp not sent, check the input and try again"}
        
        otp_code = mail_response['otp']
        exp_time = datetime.datetime.utcnow() + otp_expiration_time

        new_otp = Otp(
            otp_code=otp_code,
            otp_type="email",
            is_used=False,
            created_at=datetime.datetime.utcnow(),
            exp_time=exp_time,
            attempts=0,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=hashed_password,
            ip_addr=ip_addr,
            user_agent=user_agent
        )
        db.add(new_otp)
        db.commit()
        return {'type': "ok"}
    except Exception as e:
        print("Error in signup with credentials:", e)
        return {"type": "error", 'status_code': 500, "detail": "An error occurred with signup"}

@router.post("/verify-otp")
def verify_otp(data: VerifyotpRequest, db: Session = Depends(get_db)):
    otp_code = data.otp_code
    email = data.email
    try:
        existing_otp = db.query(Otp).filter(Otp.email == email, Otp.is_used == False).first()
        if not existing_otp:
            return {'type':"error", 'status_code':400, 'detail':"Invalid or expired OTP, retry"}
        if datetime.datetime.utcnow() > existing_otp.exp_time:
            return {'type':"error", 'status_code':400, 'detail':"OTP has expired, request a new otp"}

        if existing_otp.otp_code != otp_code:
            existing_otp.attempts += 1
            db.commit()
            if existing_otp.attempts >= 5:
                return {'type':"error", 'status_code':400, 'detail':"Too many incorrect attempts. Request a new OTP."}
            return {'type':"invalid", 'status_code':400, 'detail':"Invalid OTP"}

        existing_otp.is_used = True
        existing_otp.verified_at = datetime.datetime.utcnow()

        new_user = User(
            first_name=existing_otp.first_name,
            last_name=existing_otp.last_name,
            password_hash=existing_otp.password_hash,
            registered_date=datetime.datetime.utcnow(),
            email=email
        )
        db.add(new_user)
        db.commit()
        return {'type': "ok", 'details': "User created successfully."}
    except Exception as e:
        print("Error in verifying otp:", e)
        return {"type": "error", 'status_code': 500, "detail": "An error occurred with verifying otp"}

@router.post("/resend-otp")
def resend_otp(data: ResendOtpRequest, db: Session = Depends(get_db)):
    email = data.email
    ip_addr = data.ip_addr
    user_agent = data.user_agent
    
    try:
        existing_otp = db.query(Otp).filter(Otp.email == email, Otp.is_used == False).first()

        if existing_otp:
            if existing_otp.lock_until and datetime.datetime.utcnow() < existing_otp.lock_until:
                return {"type": "error", "detail": "Wait for a while before sending a request"}
            elif existing_otp.resend_count >= 3:
                existing_otp.lock_until = datetime.datetime.utcnow() + otp_resend_time
                existing_otp.resend_count = 0
                return {"type": "error", "detail": "OTP resend limit exceeded. Try again later."}
            existing_otp.resend_count += 1
            db.commit()

        mail_response = send_gmail_otp(email)
        if mail_response['type'] != 'ok':
            raise HTTPException(status_code=500, detail="Failed to send OTP")

        existing_otp.otp_code = mail_response['otp']
        existing_otp.exp_time = datetime.datetime.utcnow() + otp_expiration_time
        existing_otp.otp_type = "email"
        existing_otp.is_used = False
        existing_otp.created_at = datetime.datetime.utcnow()
        existing_otp.attempts = 0
        existing_otp.resend_count = 0
        existing_otp.ip_addr = ip_addr
        existing_otp.user_agent = user_agent
        db.commit()
        return {"type": "ok", "detail": "OTP resent successfully"}
    except Exception as e:
        print("Error in resending otp:", e)
        return {"type": "error", "detail": "An error occurred with resending otp", 'status_code': 500}

@router.post("/login")
def user_login(data: LoginRequest, db: Session = Depends(get_db)):
    email = data.email
    password = data.password
    password_hash = hash_password(password)
    try:
        existing_user = db.query(User).filter(User.email == email, User.password_hash == password_hash).first()
        if not existing_user:
            return {'type': "error", 'details': "User not found"}
        token = create_jwt(existing_user.first_name)
        return {'type': "ok", 'token': token}
    except Exception as e:
        print("Error in log in:", e)
        return {"type": "error", "detail": "An error occurred with login", 'status_code': 500}
        pass
    pass