from fastapi import APIRouter, Depends, Request, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers.todos import TodosController
from schemas.todos import TodosSchema
from models.todos import StatusEnum

from sse_starlette.sse import EventSourceResponse
import asyncio, json
from controllers.sse import sse_manager
import os

router = APIRouter()

@router.post(
    "/todos",
    status_code=status.HTTP_201_CREATED,
    summary="Création d'une tâche",
    description="Crée une tâche",
    response_model=TodosSchema,
)
def create_city(todo: TodosSchema, db: Session = Depends(get_db)):
    if not todo.title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required"
        )

    return TodosController.create_todo(db, todo)

@router.get(
    "/todos",
    status_code=status.HTTP_200_OK,
    summary="Liste les tâches",
    description="Retrourne la liste des tâches",
)
def get_tasks(status: StatusEnum | None = None, db: Session = Depends(get_db)):
    return TodosController.get_all_todos(db, status)

@router.patch(
    "/todos/:id",
    status_code=status.HTTP_200_OK,
    summary="Liste les tâches",
    description="Retrourne la liste des tâches",
)
def patch_task(id: int, todo: TodosSchema, db: Session = Depends(get_db)):
    return TodosController.patch_todo(id, todo, db)

@router.delete(
    "/todos/:id",
    status_code=status.HTTP_200_OK,
    summary="Liste les tâches",
    description="Retrourne la liste des tâches",
)
def patch_task(id: int, db: Session = Depends(get_db)):
    return TodosController.delete_todo(id, db)

APP_NAME = os.getenv("APP_NAME", "")

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Santé du service",
    description="Retrourne la santé du service",
)
def get_health():
    return {
        "status": "ok",
        "app": APP_NAME,
        "database": "connected"
    }

@router.get(
    "/todos/overdue",
    status_code=status.HTTP_200_OK,
    summary="Liste les tâches overdue",
    description="Liste les tâches overdue",
)
def get_overdue(db: Session = Depends(get_db)) -> None:
    return TodosController.get_todo_overdue(db)

async def overdue_event_generator(request, db: Session):
    queue = sse_manager.add_listener()
    try:
        while True:
            if await request.is_disconnected():
                break
            try:
                data = await asyncio.wait_for(queue.get(), timeout=30)
                yield {"event": "todo_alert", "data": json.dumps(data)}
            except asyncio.TimeoutError:
                yield {"event": "ping", "data": ""}
    finally:
        sse_manager.remove_listener(queue)

@router.get("/alerts")
async def alerts(request: Request, db: Session = Depends(get_db)):
    return EventSourceResponse(overdue_event_generator(request, db))


@router.post("/todos/{id}/notify")
async def notify(id: int, db: Session = Depends(get_db)):
    todo = TodosController.get_todo_by_id(db, id)  # raise 404 si pas trouvé
    
    listeners = await sse_manager.broadcast({
        "id": todo.id,
        "title": todo.title,
        "status": todo.status.value,
        "due_date": str(todo.due_date)
    })
    return {"message": "Alerte envoyée", "listeners": listeners}