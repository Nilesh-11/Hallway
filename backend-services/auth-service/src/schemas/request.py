from pydantic import BaseModel, Field, field_validator, EmailStr
from src.utils.sanitation import validate_password
from typing import Optional

class googleSignupRequest(BaseModel):
    username: str
    password: str = Field(..., min_length=8, max_length=50)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password(value)

class ResendOtpRequest(BaseModel):
    email:EmailStr
    ip_addr: Optional[str] = None
    user_agent: Optional[str] = None

class VerifyotpRequest(BaseModel):
    otp_code: str = Field(..., min_length=6, max_length=6, pattern="^[0-9]+$")
    email: EmailStr

class UserSignupRequest(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=30, pattern="^[a-zA-Z]+$")
    last_name: str = Field(..., min_length=3, max_length=30, pattern="^[a-zA-Z]+$")
    password: str = Field(..., min_length=8, max_length=50)
    email: EmailStr
    ip_addr: Optional[str] = None
    user_agent: Optional[str] = None
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password(value)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password(value)