from sqlalchemy import Column, Integer, String, Date, Enum, DateTime
from database import Base
import enum
from datetime import datetime


class StatusEnum(enum.Enum):
    pending = "pending"
    done = "done"


class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.pending)
    created_at = Column(DateTime, nullable=False, default=datetime)

    class Config:
        from_attributes = True
