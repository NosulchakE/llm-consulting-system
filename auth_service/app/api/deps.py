from typing import Annotated
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase
from app.core.security import decode_token
from app.core.exceptions import InvalidTokenError
from jose import ExpiredSignatureError, JWTError

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

async def get_auth_uc(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    return AuthUseCase(user_repo)

async def get_current_user_id(
    authorization: Annotated[str | None, Header()] = None
) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise InvalidTokenError()
    
    token = authorization.split(" ")[1]
    
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenError()
        return int(user_id)
    except (ExpiredSignatureError, JWTError, ValueError):
        raise InvalidTokenError()
