from datetime import datetime
from typing import Annotated

from fastapi.params import Query
from pydantic import BaseModel


#
# Category
#

class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryIn(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class CategoryMinimal(BaseModel):
    id: int
    name: str | None = None


#
# Task
#

class TaskIn(BaseModel):
    name: str
    category: CategoryMinimal


class TaskUpdate(BaseModel):
    name: str
    category: CategoryMinimal
    is_archived: bool


class TaskFilterParams(BaseModel):
    is_current: bool | None = None
    is_archived: bool | None = None


class TaskOut(BaseModel):
    id: int
    name: str
    category: CategoryMinimal
    is_current: bool
    is_archived: bool


class TaskMinimal(BaseModel):
    id: int
    name: str | None = None


class TaskWithCategoryMinimal(BaseModel):
    id: int
    name: str
    category: CategoryMinimal


#
# WorkReport
#

class WorkReportCategory(BaseModel):
    category: CategoryMinimal
    time: float


class WorkReportTask(BaseModel):
    task: TaskWithCategoryMinimal
    time: float


class WorkReportTotal(BaseModel):
    time: float


#
# WorkItem
#

class WorkItemIn(BaseModel):
    task_id: int
    start_dt: datetime
    end_dt: datetime | None


class WorkItemOut(BaseModel):
    id: int
    task: TaskMinimal
    start_dt: datetime
    end_dt: datetime | None


class WorkItemPartialUpdate(BaseModel):
    id: int | None = None
    task: TaskMinimal | None = None
    start_dt: datetime | None = None
    end_dt: datetime | None = None


class WorkStart(BaseModel):
    task_id: int
    start: int | None
