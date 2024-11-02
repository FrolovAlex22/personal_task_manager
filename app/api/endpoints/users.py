from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.task import TaskCompleteStatus, TaskCreate, TaskDelete, TaskResponse, TaskUpdate
from app.api.schemas.user import UserCreate, UserResponse
from app.db.database import get_db_session
from app.db.models import Task, User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
        "/register/",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED,
    )
async def create_user(
    user: UserCreate, session: AsyncSession = Depends(get_db_session)
):
    add_user = User(**user.model_dump())
    session.add(add_user)
    await session.commit()
    session.refresh(add_user)

    return add_user


@router.get(
        "/list",
        status_code=status.HTTP_200_OK,
        response_model=list[UserResponse])
async def get_tasks(
    session: AsyncSession = Depends(get_db_session),
    # current_user: Users = Depends(get_current_user)
):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()

    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_task_id(
    user_id: int, session: AsyncSession = Depends(get_db_session)
):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user_by_id = result.scalar_one_or_none()
    if user_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_by_id


# @router.put("/update/{task_id}", response_model=TaskResponse)
# async def get_task_id(
#     task_id: int,
#     task_update: TaskUpdate,
#     session: AsyncSession = Depends(get_db_session)
# ):
#     query = select(Task).where(Task.id == task_id)
#     result = await session.execute(query)
#     db_task = result.scalar_one_or_none()
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     for key, value in task_update.model_dump().items():
#         setattr(db_task, key, value)
#     await session.commit()

#     return db_task


@router.delete(
        "/delete/{user_id}",
        response_model=UserResponse,
        status_code=status.HTTP_200_OK,
    )
async def delete_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        await session.delete(user)
        await session.commit()

        return user
    except Exception as e:
        await session.rollback()
        raise e


@router.put("/update/{user_id}", response_model=UserResponse)
async def update_user_id(
    user_id: int,
    user_update: UserCreate,
    session: AsyncSession = Depends(get_db_session)
):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.model_dump().items():
        setattr(user, key, value)
    await session.commit()

    return user
