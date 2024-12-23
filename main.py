from contextlib import asynccontextmanager
from fastapi.responses import ORJSONResponse
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

# from app.db.database import create_model
from app.core.config import settings
from app.api.endpoints.tasks import router as task_router
from app.api.endpoints.users import router as user_router
from app.db.database import create_models, delete_models
from app.db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_models()
    # print("База очищена ")
    await create_models()
    print("База готова")
    yield
    print("Выключение")


app = FastAPI(
    lifespan=lifespan,
    title=settings.app_title,
    default_response_class=ORJSONResponse,)


app.include_router(task_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.MAIN.HOST,
        port=settings.MAIN.PORT,
        reload=True,
    )