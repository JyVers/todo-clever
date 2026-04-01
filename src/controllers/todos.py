from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.todos import TodosSchema
from repositories.todos import TodosRepository


class TodosController:
    @staticmethod
    def get_all_todos(db: Session):
        return TodosRepository.get_all(db)

    @staticmethod
    def get_todo_by_id(db: Session, user_id: int):
        user = TodosRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    @staticmethod
    def create_todo(db: Session, todo: TodosSchema):
        return TodosRepository.create(db, todo)
