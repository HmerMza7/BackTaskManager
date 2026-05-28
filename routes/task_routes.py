from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.task_controller import TaskController
from pydantic import BaseModel, Field
from dependencies.auth import get_current_user_id
from typing import Optional

router = APIRouter(prefix="/tasks", tags=["Tasks"])

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    priority_id: int = Field(..., ge=1, le=3)
    state_id: int = 1

class TaskUpdate(BaseModel):
    title: str = Field(None, min_length=1)
    description: str = Field(None, min_length=1)
    priority_id: int = Field(None, ge=1, le=3)
    state_id: int = Field(None)


@router.get("/priorities")
def list_priorities(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return TaskController.get_priorities(db)

@router.get("/")
def list_tasks(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    state_id: Optional[int] = Query(None, description="Filter by state (1=pendiente, 2=completada)"),
    priority_id: Optional[int] = Query(None, description="Filter by priority (1=alta, 2=media, 3=baja)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Results per page"),
):
    return TaskController.get_tasks(db, user_id, state_id, priority_id, page, limit)

@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    task_data = task.dict()
    task_data["user_id"] = user_id
    return TaskController.create_task(db, task_data)

@router.put("/{task_id}")
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return TaskController.update_task(db, task_id, task.dict(exclude_unset=True), user_id)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return TaskController.delete_task(db, task_id, user_id)

@router.get("/states")
def list_states(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return TaskController.get_states(db)

