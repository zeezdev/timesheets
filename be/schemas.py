from datetime import datetime

from pydantic import BaseModel


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


class TaskIn(BaseModel):
    name: str
    category: CategoryMinimal


class TaskUpdate(BaseModel):
    name: str
    category: CategoryMinimal
    is_archived: bool


class TaskOut(BaseModel):
    id: int
    name: str
    category: CategoryMinimal
    is_current: int
    is_archived: bool


class TaskWithCategoryMinimal(BaseModel):
    id: int
    name: str
    category: CategoryMinimal


class WorkReportCategory(BaseModel):
    category: CategoryMinimal
    time: float


class WorkReportTask(BaseModel):
    task: TaskWithCategoryMinimal
    time: float


class WorkReportTotal(BaseModel):
    time: float


class WorkItemBase(BaseModel):
    task_id: int


class WorkItem(WorkItemBase):
    start_dt: datetime
    end_dt: datetime | None


class WorkItemOut(WorkItemBase):
    id: int
    start_dt: datetime
    end_dt: datetime | None


class WorkStart(WorkItemBase):
    start: int | None
