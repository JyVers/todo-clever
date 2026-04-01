from typing import Optional, cast
from src.models.todos import Todos
from src.schemas.todos import TodosSchema
from sqlalchemy.orm import Session


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
    def create(db: Session, Todos: TodosSchema) -> Todos:
        db_Todos = Todos(**Todos.model_dump())  # convert schema → ORM instance
        db.add(db_Todos)
        db.commit()
        db.refresh(db_Todos)
        return db_Todos
