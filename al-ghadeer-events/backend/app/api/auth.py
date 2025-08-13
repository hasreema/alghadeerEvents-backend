from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas import UserCreate, UserOut, TokenOut

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/ping")
def ping():
    return {"ok": True}


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        email=payload.email,
        username=payload.username,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role=payload.role or "staff",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenOut)
async def login(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("content-type", "").lower()

    email_or_username = None
    password = None

    if content_type.startswith("application/json"):
        data = await request.json()
        email_or_username = data.get("email") or data.get("username")
        password = data.get("password")
    else:
        form = await request.form()
        email_or_username = form.get("username") or form.get("email")
        password = form.get("password")

    if not email_or_username or not password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Missing credentials")

    user = db.query(User).filter(User.email == email_or_username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role},
        expires_minutes=settings.access_token_expires_minutes,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user