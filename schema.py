# schema.py

from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str = None

class TaskCreate(TaskBase):
     title: str
     description: str
     completed: bool
     
class Task(TaskBase):
    id: int
    completed: bool

    class Config:
       from_attributes = True
