from pydantic import BaseModel
from typing import Optional
from models.todos import StatusEnum
from datetime import date

class TodosSchema(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: StatusEnum = StatusEnum.pending