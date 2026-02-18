from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str = Field(..., example="john@123", description="User's email address")
    password: str = Field(..., example="strongpassword", description="User's password")

class RegisterRequest(LoginRequest):
    full_name: str | None = Field(default=None, example="John Doe", description="User's full name")