from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, InvalidTokenError
from src.db.schemas.users import UserBase
from src.common.security.jwt_encode import decode_access_token
from src.core.config import bearer_scheme
from src.cruds.user import UserCRUD


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> UserBase:
    if not token or not token.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен аутентификации не предоставлен",
        )

    try:
        payload = decode_access_token(token.credentials)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Не удалось проверить учетные данные",
            )

        user = await UserCRUD.get_user_by_id(payload.id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        return user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истёк",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен",
        )
