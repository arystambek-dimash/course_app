import src.db.schemas.users as users_schemas
import src.db.schemas.tokens as tokens_schemas
from src.common.security import jwt_encode
from src.common.security.encrypt import verify_password, get_password_hash
from src.common.security.jwt_encode import decode_refresh_token, create_access_token, create_refresh_token
from src.core.config import settings
from src.cruds.blacklisttoken import BlacklistTokenCRUD
from src.cruds.user import UserCRUD
from fastapi.responses import JSONResponse
from starlette import status


class UserService:
    @staticmethod
    async def authenticate_user(phone_number: str, password: str):
        db_user = await UserCRUD.get_user_with_password(phone_number)
        if not db_user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No user with such number"})
        if not verify_password(password, db_user.password):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Wrong password"})

        return db_user

    @staticmethod
    def create_tokens_for_user(db_user: users_schemas.UserBase):
        payload = tokens_schemas.Payload(
            _id=db_user.id,
            exp=settings.JWT_ACCESS_TOKEN_EXPIRES
        )
        refresh_payload = tokens_schemas.Payload(
            _id=db_user.id,
            exp=settings.JWT_REFRESH_TOKEN_EXPIRES
        )

        access_token = jwt_encode.create_access_token(payload)
        refresh_token = jwt_encode.create_refresh_token(refresh_payload)

        return tokens_schemas.Token(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def register_user(form_data: users_schemas.UserInRegister):
        try:
            existing_user = await UserCRUD.get_user_by_number(form_data.telephone_number)
            if existing_user:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content={"message": "User with this phone number already exists"})

            hashed_password = get_password_hash(form_data.password)
            creating_user_data = form_data.copy(update={"password": hashed_password})
            print(creating_user_data)
            await UserCRUD.create_user(creating_user_data)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content={"message": "User registered successfully"})

        except Exception:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content={"error": "Internal server error"})

    @staticmethod
    def verify_refresh_token(refresh_token: str):
        try:
            payload = decode_refresh_token(refresh_token)
            return payload
        except Exception as e:
            print(e)
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content={"message": "Invalid or expired refresh token"})

    @staticmethod
    async def refresh_access_token(refresh_token: str):
        try:
            db_token = await BlacklistTokenCRUD.get_token(refresh_token)
            if db_token:
                return JSONResponse(content={"message": "This token has already been used"},
                                    status_code=status.HTTP_400_BAD_REQUEST)

            payload = UserService.verify_refresh_token(refresh_token)
            if isinstance(payload, JSONResponse):
                return payload

            await BlacklistTokenCRUD.create_token(refresh_token)
            new_access_token = create_access_token(payload)
            new_refresh_token = create_refresh_token(payload)
            return tokens_schemas.Token(access_token=new_access_token, refresh_token=new_refresh_token)
        except Exception as e:
            print(e)
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content={"error": "Failed to refresh access token"})
