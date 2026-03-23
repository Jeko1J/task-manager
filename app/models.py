from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


class TaskStatus(str, enum.Enum):
    NEW = "новая"
    IN_PROGRESS = "в работе"
    COMPLETED = "выполнена"


class TaskPriority(str, enum.Enum):
    LOW = "низкий"
    MEDIUM = "средний"
    HIGH = "высокий"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.NEW, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deadline = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Task {self.title}>"