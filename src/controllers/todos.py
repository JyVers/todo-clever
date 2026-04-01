from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.todos import TodosSchema
from repositories.todos import TodosRepository
from models.todos import StatusEnum
from controllers.sse import SSEManager

class TodosController:
    # GET
    @staticmethod
    def get_all_todos(db: Session, status: StatusEnum):
        return TodosRepository.get_all(db, status)

    @staticmethod
    def get_todo_by_id(db: Session, id: int):
        todo = TodosRepository.get_by_id(db, id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        return todo
    
    @staticmethod
    def get_todo_overdue(db: Session):
        return TodosRepository.get_overdue(db)

    ###

    @staticmethod
    def create_todo(db: Session, todo: TodosSchema):
        return TodosRepository.create(db, todo)

    @staticmethod
    def patch_todo(id: int, todo: TodosSchema, db: Session):
        todo = TodosRepository.patch(id, todo, db)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        return todo
    
    @staticmethod
    def delete_todo(id: int, db: Session):
        deleted = TodosRepository.delete(id, db)
        if not deleted:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        return {"Task successfully deleted."}
