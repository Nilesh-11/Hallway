from src.database.connection import Base
from src.config.config import otp_expiration_time
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
import datetime
from datetime import timedelta
import enum

class OtpTypeEnum(enum.Enum):
    email = "email"
    sms = "sms"
    auth_app = "auth_app"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name=Column(String)
    last_name=Column(String)
    registered_date=Column(DateTime, default=datetime.datetime.utcnow())
    email = Column(String, unique=True, index=True, nullable=False)
    google_id = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)

class Otp(Base):
    __tablename__ = "otp"
    
    id = Column(Integer, primary_key=True, index=True)
    otp_code = Column(String, nullable=False)
    otp_type = Column(Enum(OtpTypeEnum, name="otp_type_enum"), nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    exp_time = Column(DateTime, default=lambda: datetime.datetime.utcnow() + otp_expiration_time)
    attempts = Column(Integer, default=0)
    resend_count = Column(Integer, default=0)
    verified_at = Column(DateTime, nullable=True)
    lock_until = Column(DateTime, nullable=True)
    ip_addr = Column(String)
    user_agent = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)