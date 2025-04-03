from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional

class UserRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    email: EmailStr

