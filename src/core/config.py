from datetime import timedelta
from pathlib import Path

from fastapi.security import HTTPBearer
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

bearer_scheme = HTTPBearer()


class Settings(BaseSettings):
    DB_HOST: str  # Адрес хоста базы данных
    DB_PORT: int  # Порт базы данных
    DB_USER: str  # Пользователь базы данных
    DB_PASSWORD: str  # Пароль для подключения к базе данных
    DB_NAME: str  # Имя базы данных

    # FastAPI configuration
    TITLE: str = "Тест Центр"  # Название приложения
    VERSION: str = "1.0.0"  # Версия приложения
    DESCRIPTION: str = "Thats my mommy quizz application"  # Описание приложения
    DOCS_URL: str = "/api/docs"  # URL для документации Swagger UI
    REDOCS_URL: str = "/api/redoc"  # URL для документации ReDoc
    OPENAPI_URL: str = "/openapi.json"  # URL для схемы OpenAPI

    # JWT configuration
    JWT_ACCESS_TOKEN: str
    JWT_REFRESH_TOKEN: str
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=3)

    # AWS configuration
    AWS_SECRET_KEY: str
    AWS_ACCESS_KEY: str
    AWS_BUCKET_NAME: str
    AWS_REGION: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = BASE_DIR / '.env'


def get_settings():
    return Settings()


settings = get_settings()
