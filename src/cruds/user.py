import typing
from sqlalchemy import select, insert, update
import src.db.schemas.users as user_schema
from src.db.database import async_session
from src.db.models.users import UsersOrm


class UserCRUD:
    @staticmethod
    def _exclude_password(user: UsersOrm) -> dict:
        user_dict = user.__dict__.copy()
        user_dict.pop('password', None)
        return user_dict

    @staticmethod
    async def get_user_by_number(telephone_number: str) -> typing.Optional[user_schema.UserBase]:
        async with async_session() as session:
            query = select(UsersOrm).where(UsersOrm.telephone_number == telephone_number)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return user_schema.UserBase(**UserCRUD._exclude_password(user))
            return None

    @staticmethod
    async def get_user_by_id(user_id: int) -> typing.Optional[user_schema.UserBase]:
        async with async_session() as session:
            query = select(UsersOrm).where(UsersOrm.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return user_schema.UserBase(**UserCRUD._exclude_password(user))
            return None

    @staticmethod
    async def get_user_with_password(telephone_number: str) -> typing.Optional[user_schema.UserBaseWithPassword]:
        async with async_session() as session:
            query = select(UsersOrm).where(UsersOrm.telephone_number == telephone_number)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return user_schema.UserBaseWithPassword.from_orm(user)
            return None

    @staticmethod
    async def get_all_users() -> typing.List[user_schema.UserBase]:
        async with async_session() as session:
            query = select(UsersOrm)
            result = await session.execute(query)
            users = result.scalars().all()
            return [user_schema.UserBase.from_orm(user) for user in users]

    @staticmethod
    async def create_user(user: user_schema.UserInRegister) -> typing.Optional[user_schema.UserBase]:
        try:
            async with async_session() as session:
                query = insert(UsersOrm).values(**user.dict())
                result = await session.execute(query)
                await session.commit()

                created_user_id = result.inserted_primary_key[0]
                created_user = await session.get(UsersOrm, created_user_id)
                return user_schema.UserBase.from_orm(created_user) if created_user else None
        except Exception as e:
            await session.rollback()
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    async def update_user(user_id: int, user: user_schema.UserInUpdate) -> typing.Optional[user_schema.UserBase]:
        try:
            async with async_session() as session:
                user_data = user.dict(exclude={'id'}, by_alias=False, exclude_none=True)
                query = update(UsersOrm).where(UsersOrm.id == user_id).values(**user_data)
                await session.execute(query)
                await session.commit()
                updated_user = await session.get(UsersOrm, user_id)
                return user_schema.UserBase.from_orm(updated_user) if updated_user else None
        except Exception as e:
            await session.rollback()
            print(f"Error updating user: {e}")
            return None
