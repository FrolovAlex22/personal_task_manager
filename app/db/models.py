from datetime import datetime
import enum
from typing import Optional

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime


class StatusTaskEnum(str, enum.Enum):
    WAITING = "ожидает"
    IN_PROGRESS = "в процессе"
    DONE = "выполнена"
    IN_ARCHIVE = "в архиве"


class Base(DeclarativeBase):
    __abstract__ = True

    # def __repr__(self):
    #     return f"<{self.__class__.__name__} {self.id}>"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(70), nullable=False)

    # tasks: Mapped[Optional[list["Task"]]] = relationship(
    #     back_populates="members",
    #     secondary="user_task",
    # )


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
#     completed: Mapped[bool] = mapped_column(default=False)
#     profession: Mapped[StatusTaskEnum] = mapped_column(
#         default=StatusTaskEnum.WAITING
#     )
#     members: Mapped[list] = mapped_column(default=[])
#     owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

#     members: Mapped[list["User"]] = relationship(
#         back_populates="tasks",
#         secondary="user_task",
#     )


# class UserTask(Base):
#     __tablename__ = "user_task"

#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
#     )
#     task_id: Mapped[int] = mapped_column(
#         ForeignKey("task.id", ondelete="CASCADE"), primary_key=True
#     )

#     comment: Mapped[Optional[str]]
