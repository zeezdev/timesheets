# FIXME: try to use `orm_mode = True` in models
from datetime import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str | None = None

    # class Config:
    #     orm_mode = True


class CategoryIn(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int


class CategoryMinimal(BaseModel):
    id: int
    name: str | None = None


class TaskIn(BaseModel):
    name: str
    category: CategoryMinimal

    # class Config:
    #     orm_mode = True


class TaskOut(BaseModel):
    id: int
    name: str
    is_current: int
    category: CategoryMinimal

    # class Config:
    #     orm_mode = True


class TaskWithCategoryMinimal(BaseModel):
    id: int
    name: str
    category: CategoryMinimal

    # class Config:
    #     orm_mode = True


class WorkReportCategory(BaseModel):
    category: CategoryMinimal
    time: float

    # class Config:
    #     orm_mode = True


class WorkReportTask(BaseModel):
    task: TaskWithCategoryMinimal
    time: float

    # class Config:
    #     orm_mode = True


class WorkReportTotal(BaseModel):
    time: float

    # class Config:
    #     orm_mode = True


class WorkItem(BaseModel):
    start_dt: datetime
    end_dt: datetime | None
    task_id: int

    # class Config:
    #     orm_mode = True


class WorkItemOut(WorkItem):
    id: int


class WorkStart(BaseModel):
    task_id: int
    start: int | None
