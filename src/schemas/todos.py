from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from models.todos import StatusEnum

class TodosSchema(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: StatusEnum = StatusEnum.pending