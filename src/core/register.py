from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.api.v1.root_endpoint import root_routers
from src.core.config import settings
from src.db.database import Base, async_engine


async def create_tables():
    async_engine.echo = False
    try:
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
    finally:
        async_engine.echo = True


async def register_routes(app: FastAPI):
    for r in root_routers:
        app.include_router(r, prefix='/api/v1')


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await register_routes(app)
    yield


def register_app():
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=lifespan
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        error_details = [
            {
                "field": error['loc'][-1],
                "message": error['msg'],
            }
            for error in exc.errors()
        ]

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "errors": error_details
            },
        )

    return app
