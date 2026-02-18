from fastapi import APIRouter, status, Depends, Response
from typing import Annotated
from schemas.auth import LoginRequest, RegisterRequest
from models.user import User
from models.connect import get_session
from schemas.user import UserResponse
from sqlmodel import Session, select
from utils import get_password_hash, verify_password, generate_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginRequest, session: Annotated[Session, Depends(get_session)], response: Response):
    user = session.exec(select(User).where(User.email == body.email)).first()
    
    print("User found:", user)
    if not user or not verify_password(body.password, user.hashed_password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid email or password"}
    
    token = generate_token(user.id)

    return {"message": "Login successful", "user": UserResponse(**user.model_dump()), "token": token}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, session: Annotated[Session, Depends(get_session)]):
    user = User(**body.model_dump(), hashed_password= get_password_hash(body.password))
    session.add(user)
    session.commit()
    
    session.refresh(user)
    return {"message": "Registration successful", "user": UserResponse(**user.model_dump())}