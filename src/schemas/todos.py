from pydantic import BaseModel
from datetime import date, datetime

class TodosSchema(BaseModel):
    id: int
    title: str
    description: str
    due_date: date
    status: str
    created_at: datetime
