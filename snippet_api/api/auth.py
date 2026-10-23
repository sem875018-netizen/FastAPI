import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from schemas.user import UserCreate, UserRead
from services.auth import register_user, authenticate_user
from core.security import create_access_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await register_user(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form.username, form.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверное имя пользователя или пароль",
                            headers={"WWW-Authenticate": "Bearer"})
    logger.info("User %s authenticated", user.username)
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}
