from datetime import date, datetime
from enum import Enum, unique
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


# @unique
class StatusTaskEnum(enum.Enum):
    WAITING = "ожидает"
    IN_PROGRESS = "в процессе"
    DONE = "выполнена"
    IN_ARCHIVE = "в архиве"
    CANCEL = "cancel"


# @unique
class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"


class Base(DeclarativeBase):
    __abstract__ = True

    # def __repr__(self):
    #     return f"<{self.__class__.__name__} {self.id}>"
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(70), nullable=False)
    # role: Mapped[UserRole] = mapped_column(
    #     enum.Enum(UserRole), default=UserRole.USER
    # )

    tasks: Mapped[Optional[list["Task"]]] = relationship(
        back_populates="members",
        secondary="user_task",
    )


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[date] = mapped_column(
        server_default=func.now(),
        default=date.today,
    )
    deadline: Mapped[date] = mapped_column(nullable=True)
    # status: Mapped[StatusTaskEnum] = mapped_column(
    #     Enum(StatusTaskEnum),
    #     default=StatusTaskEnum.WAITING,
    #     # server_default="WAITING"
    # )
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    members: Mapped[list["User"]] = relationship(
        back_populates="tasks",
        secondary="user_task",
    )


class UserTask(Base):
    __tablename__ = "user_task"


    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE"), primary_key=True
    )

    comment: Mapped[Optional[str]]

    def __str__(self):
        return f"{self.user_id} - {self.task_id}"
