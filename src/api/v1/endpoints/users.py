from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse

import src.db.schemas.tokens as tokens_schemas
import src.db.schemas.users as users_schemas
from src.api.dependencies import get_current_user
from src.services.domain.user import UserService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/sign-in', response_model=tokens_schemas.Token, status_code=status.HTTP_201_CREATED)
async def sign_in(form_data: users_schemas.UserInLogin):
    try:
        db_user = await UserService.authenticate_user(form_data.telephone_number, form_data.password)
        if isinstance(db_user, JSONResponse):
            return db_user
        tokens = UserService.create_tokens_for_user(db_user)
        return tokens
    except HTTPException as he:
        raise he
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post('/sign-up', response_model=tokens_schemas.Token, status_code=status.HTTP_201_CREATED)
async def sign_up(form_data: users_schemas.UserInRegister):
    try:
        response = await UserService.register_user(form_data)
        if isinstance(response, JSONResponse):
            return response

        db_user = await UserService.authenticate_user(form_data.telephone_number, form_data.password)
        tokens = UserService.create_tokens_for_user(db_user)
        return tokens
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post('/refresh-token', response_model=tokens_schemas.Token, status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token: str = Header(...)):
    try:
        response = await UserService.refresh_access_token(refresh_token)
        if isinstance(response, JSONResponse):
            return response
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to refresh access token")


@router.get('/me', response_model=users_schemas.UserBase, status_code=status.HTTP_200_OK)
async def get_user_profile(user: users_schemas.UserBase = Depends(get_current_user)):
    try:
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get current user")
