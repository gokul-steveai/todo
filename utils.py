from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash
from jwt import encode, decode, DecodeError
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from typing import Annotated
from fastapi import Depends, status, HTTPException, Response
from models.connect import get_session
from models.user import User

password_hash = PasswordHash.recommended()

bearer_auth_scheme = HTTPBearer()

SECRET_KEY = "8f22a1ca554593d4120054c7675c0aaec3c31811c7aac2a7f46acf1732103604"
EXPIRY_TIME = 30 # minutes

def not_found_response(response: Response, message = "Not found"):
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": message}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def generate_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_TIME),
    }
    
    token = encode(payload=payload, key=SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token: str) -> int | None:
    try:
        payload = decode(jwt=token, key=SECRET_KEY, algorithms=["HS256"])
        if payload.get('exp') < datetime.now(tz=timezone.utc).timestamp():
            print("Token expired")
            return None
        return payload
    except DecodeError:
        print("Invalid token")
        return None

async def get_current_user_id(session: Annotated[Session, Depends(get_session)], credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_auth_scheme)]) -> int | None:
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = validate_token(token)
    if payload:
        user_id = session.exec(select(User.id).where(User.id == payload.get("user_id"))).first()
        if user_id:
            return user_id
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return None