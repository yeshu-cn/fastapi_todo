from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import task as task_service
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskInDB
from app.database import SessionLocal
from typing import List
from app.services.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TaskInDB)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_service.create_task(db=db, task=task, owner_id=current_user.id)

@router.put("/{task_id}", response_model=TaskInDB)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = task_service.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}", response_model=int)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_task_id = task_service.delete_task(db, task_id)
    if deleted_task_id is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task_id

@router.get("/", response_model=List[TaskInDB])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = task_service.get_tasks_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return tasks
