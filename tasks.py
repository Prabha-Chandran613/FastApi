# tasks.py

from typing import List
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
import models
from database import get_db
from schema import Task, TaskCreate
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://0.0.0.0:8080/realms/fastApi_realm/protocol/openid-connect/token")

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)

@router.get('/getall', response_model=List[Task])
def get_tasks(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    tasks = db.query(models.Task).all()
    return tasks

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=List[Task])
def create_task(task: TaskCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return [new_task]

@router.get('/{task_id}', response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    return task

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    db.delete(db_task)
    db.commit()
    return None
@router.put('/{task_id}', response_model=Task)
def update_task(task_id: int, update_task: TaskCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")

    # Update the task attributes
    db_task.title = update_task.title
    db_task.description = update_task.description

    # Optional: If 'completed' is part of the Task model, update it if it exists in the update_task model
    if hasattr(update_task, 'completed'):
        db_task.completed = update_task.completed

    # Commit the changes to the database
    db.commit()

    # Return the updated task
    return db_task