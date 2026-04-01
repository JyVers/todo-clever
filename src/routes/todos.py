from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from controllers.todos import TodosController
from schemas.todos import TodosSchema

router = APIRouter()


# @router.post(
#     "/todo",
#     status_code=status.HTTP_201_CREATED,
#     summary="Création d'une nouvelle une ville",
#     description="Crée une ville",
#     response_model=CitySchema,
# )
# def create_city(city: CitySchema, db: Session = Depends(get_db)):
#     return UserController.create_user(db, city)


@router.get(
    "/todos",
    status_code=status.HTTP_200_OK,
    summary="Liste les tâches",
    description="Retrourne la liste des tâches",
)
def get_tasks(db: Session = Depends(get_db)):
    return TodosController.get_all_todos(db)


@router.get(
    "/_health",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Santé du service",
    description="Retrourne la santé du service",
)
def get_health() -> None:
    return
