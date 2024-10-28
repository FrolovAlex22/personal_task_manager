from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.task import TaskCreate, TaskResponse
from app.db.database import get_db_session
from app.db.models import Task
# from schemas import STask, STaskAdd, STaskId


router = APIRouter(
    prefix="/tasks",
    tags=["taski"]
)

# @router.post("")
# async def get_task(task: Annotated[STaskAdd, Depends()]) -> STaskId:
#     task_id = await TaskRepository.add_one(task)
#     return{
#         "ok": True,
#         "task_id": task_id
#     }


# @router.get("")
# async def get_tasks() -> list[STask]:
#     task = await TaskRepository.find_all()
#     return task


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_db_session)
):
    todo = Task(**task_in.model_dump())
    session.add(todo)
    await session.commit()
    return todo
# @router.get("/list")
# async def get_files(
#     request: Request, current_user: Users = Depends(get_current_user)
# ):
#     files = await get_all_user_file(current_user)
#     return files


# @router.get("/download")
# async def download_file(
#     name: str, current_user: Users = Depends(get_current_user)
# ):
#     file = await get_file(name, current_user.id)
#     if not file:
#         return "File not found"
#     file_path = os.path.join(file.path, name)
#     media_type = file_path.split(".")[-1]
#     return FileResponse(
#         path=file_path, filename=name, media_type=media_type
#     )