from typing import Optional, cast
from models.todos import Todos
from schemas.todos import TodosSchema
from sqlalchemy.orm import Session
from datetime import datetime, date
from models.todos import StatusEnum

class TodosRepository:

    # GET
    @staticmethod
    def get_all(db: Session, status: StatusEnum | None = None) -> list[Todos]:
        if status:
            return cast(list[Todos], db.query(Todos).filter(Todos.status == status).all())
        return cast(list[Todos], db.query(Todos).all())

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[Todos]:
        return cast(
            Optional[Todos],
            db.query(Todos).filter(Todos.id == id).first(),
        )
    
    @staticmethod
    def get_overdue(db: Session) -> list[Todos]:
        today = date.today()
        return (
            db.query(Todos)
            .filter(Todos.status == StatusEnum.pending, Todos.due_date < today)
            .all()
        )

    ###

    @staticmethod
    def patch(id: int, todo: TodosSchema, db: Session):
        db_todo = db.query(Todos).filter(Todos.id == id).first()
    
        if not db_todo:
            return None
        
        # Only update fields that were explicitly provided
        update_data = todo.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        
        db.commit()
        db.refresh(db_todo)
        return db_todo 

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

    @staticmethod
    def delete(id: int, db: Session) -> bool:
        db_todo = db.query(Todos).filter(Todos.id == id).first()
        
        if not db_todo:
            return False
        
        db.delete(db_todo)
        db.commit()
        return True
    