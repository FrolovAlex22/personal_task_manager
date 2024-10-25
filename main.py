from fastapi.responses import ORJSONResponse
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

# from app.db.database import create_model
from app.core.config import settings
from app.api.endpoints.tasks import router as task_router


http_bearer = HTTPBearer(auto_error=False)

app = FastAPI(
    title=settings.app_title,
    default_response_class=ORJSONResponse,)


app.include_router(task_router)


# @app.on_event("startup")
# async def startup_event():
#     await create_model()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.project_host,
        port=settings.project_port,
        reload=True,
    )