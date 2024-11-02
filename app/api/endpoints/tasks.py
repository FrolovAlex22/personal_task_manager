from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.task import TaskCompleteStatus, TaskCreate, TaskDelete, TaskResponse, TaskUpdate
from app.db.database import get_db_session
from app.db.models import Task


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
        "/create",
        status_code=status.HTTP_201_CREATED,
        response_model=TaskResponse
    )
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_db_session)
):
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    return task


@router.get(
        "/list",
        status_code=status.HTTP_200_OK,
        response_model=list[TaskResponse])
async def get_tasks(
    session: AsyncSession = Depends(get_db_session),
    # current_user: Users = Depends(get_current_user)
):
    query = select(Task)
    result = await session.execute(query)
    tasks = result.scalars().all()

    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_id(
    task_id: int, session: AsyncSession = Depends(get_db_session)
):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task_by_id = result.scalar_one_or_none()
    if task_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task_by_id


@router.put("/update/{task_id}", response_model=TaskResponse)
async def get_task_id(
    task_id: int,
    task_update: TaskUpdate,
    session: AsyncSession = Depends(get_db_session)
):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.model_dump().items():
        setattr(db_task, key, value)
    await session.commit()

    return db_task


@router.delete("/delete/{task_id}", response_model=TaskDelete)
async def get_task_id(
    task_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        await session.delete(task)
        await session.commit()

        return task
    except Exception as e:
        await session.rollback()
        raise e


@router.put("/update/{task_id}", response_model=TaskResponse)
async def update_task_id(
    task_id: int,
    task_update: TaskUpdate,
    session: AsyncSession = Depends(get_db_session)
):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.model_dump().items():
        setattr(db_task, key, value)
    await session.commit()

    return db_task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def change_task_status(
    task_id: int,
    complteted_status: TaskCompleteStatus,
    session: AsyncSession = Depends(get_db_session)
):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = complteted_status.completed
    await session.commit()

    return task
