from typing import List
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    desc: str
    status: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskInDB(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
