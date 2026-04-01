from typing import Optional, cast
from models.todos import Todos
from schemas.todos import TodosSchema
from sqlalchemy.orm import Session
from datetime import datetime

class TodosRepository:
    @staticmethod
    def get_all(db: Session) -> list[Todos]:
        return cast(list[Todos], db.query(Todos).all())

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[Todos]:
        return cast(
            Optional[Todos],
            db.query(Todos).filter(Todos.id == id).first(),
        )

    @staticmethod
    def create(db: Session, todo: TodosSchema) -> Todos:
        new_todo = Todos(
        **todo.model_dump(),
        created_at=datetime.now()
        )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
