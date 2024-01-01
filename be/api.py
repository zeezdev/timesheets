from datetime import datetime
from typing import Union, Annotated

from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database_ import (
    category_list,
    category_create,
    category_read,
    task_list,
    work_add,
    work_start as db_work_start,
    work_stop_current as db_work_stop_current,
    category_update,
    task_read,
    task_update,
    task_add,
    ts_to_dt,
    engine,
    work_get_report_category,
    work_get_report_task,
    work_get_report_total,
)
from models import Base


class CategoryBase(BaseModel):
    name: str
    description: Union[str, None] = None


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


class TaskOut(BaseModel):
    id: int
    name: str
    is_current: int
    category: CategoryMinimal


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


class WorkItem(BaseModel):
    start_dt: datetime
    end_dt: datetime | None
    task_id: int


class WorkItemOut(WorkItem):
    id: int


class WorkStart(BaseModel):
    task_id: int
    start: int | None


# https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    "http://localhost:4200",
]

router = APIRouter(prefix='/api')


def _get_default_report_datetime_range() -> tuple[datetime, datetime]:
    """
    Makes range for the last month, from start of 21th to end of 20th.

    FIXME: make start day configurable
    """
    # Get report for the last month
    now = datetime.now()
    curr_month = now.month
    curr_year = now.year
    start = datetime(curr_year, curr_month-1, 21, 0, 0, 0)
    end = datetime(curr_year, curr_month, 20, 23, 59, 59)

    return start, end


@router.get('/categories')
def categories_list() -> list[CategoryOut]:
    """Returns the list of categories"""
    rows = category_list()
    return [CategoryOut(
        id=row.id,
        name=row.name,
        description=row.description,
    ) for row in rows]


@router.post('/categories', response_model=CategoryOut, status_code=201)
def categories_add(category: CategoryIn) -> CategoryOut:
    """Creates a new category"""
    category = category_create(name=category.name, description=category.description)
    return CategoryOut(
        id=category.id,
        name=category.name,
        description=category.description,
    )


@router.get('/categories/{category_id}')
def categories_retrieve(category_id: int) -> CategoryOut:
    """Retrieves a category"""
    category = category_read(_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail='Not found')

    return CategoryOut(
        id=category.id,
        name=category.name,
        description=category.description,
    )


@router.put('/categories/{category_id}', response_model=CategoryOut)
def categories_save(category_id: int, category: CategoryOut) -> CategoryOut:
    """Updates a category instance"""
    # TODO: use CategoryIn
    updated_category = category_update(category_id, category.name, category.description)
    return CategoryOut(
        id=updated_category.id,
        name=updated_category.name,
        description=updated_category.description,
    )


@router.get('/tasks')
def tasks_list() -> list[TaskOut]:
    rows = task_list()
    return [TaskOut(
        id=row.id,
        name=row.name,
        category=CategoryMinimal(
            id=row.category_id,
            name=row.category_name,
        ),
        is_current=row.is_current,
    ) for row in rows]


@router.post('/tasks', response_model=TaskOut, status_code=201)
def tasks_add(task: TaskIn) -> TaskOut:
    """Creates a new task"""
    new_task = task_add(name=task.name, category_id=task.category.id)
    return TaskOut(
        id=new_task.id,
        name=new_task.name,
        category=CategoryMinimal(
            id=new_task.category_id,
            name=new_task.category_name,
        ),
        is_current=new_task.is_current,
    )


@router.get('/tasks/{task_id}', response_model=TaskOut)
def tasks_retrieve(task_id: int) -> TaskOut:
    """Retrieves a task"""
    task = task_read(id_=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Not found')

    return TaskOut(
        id=task.id,
        name=task.name,
        category=CategoryMinimal(
            id=task.category_id,
            name=task.category_name,
        ),
        is_current=task.is_current,
    )


@router.put('/tasks/{task_id}', response_model=TaskOut)
def tasks_save(task_id: int, task: TaskIn) -> TaskOut:
    """Updates a task instance"""
    updated_task = task_update(task_id, task.name, task.category.id)
    return TaskOut(
        id=updated_task.id,
        name=updated_task.name,
        category=CategoryMinimal(
            id=updated_task.category_id,
            name=updated_task.category_name,
        ),
        is_current=updated_task.is_current,
    )


@router.get('/work/report_by_category')
def get_work_report_by_category(
    start_datetime: Annotated[datetime | None, Query()] = None,
    end_datetime: Annotated[datetime | None, Query()] = None,
) -> list[WorkReportCategory]:
    assert start_datetime and end_datetime or (not start_datetime and not end_datetime)  # FIXME: 400

    if start_datetime is None and end_datetime is None:
        start_datetime, end_datetime = _get_default_report_datetime_range()

    rows = work_get_report_category(start_datetime, end_datetime)
    return [WorkReportCategory(
        category=CategoryMinimal(
            id=row[0],
            name=row[1],
        ),
        time=row[2],
    ) for row in rows]


@router.get('/work/report_by_task')
def get_work_report_by_task(
    start_datetime: Annotated[datetime | None, Query()] = None,
    end_datetime: Annotated[datetime | None, Query()] = None,
) -> list[WorkReportTask]:
    assert start_datetime and end_datetime or (not start_datetime and not end_datetime)  # FIXME: 400

    if start_datetime is None and end_datetime is None:
        start_datetime, end_datetime = _get_default_report_datetime_range()

    rows = work_get_report_task(start_datetime, end_datetime)
    return [WorkReportTask(
        task=TaskWithCategoryMinimal(
            id=row[0],
            name=row[1],
            category=CategoryMinimal(
                id=row[2],
                name=row[3],
            )
        ),
        time=row[4],
    ) for row in rows]


@router.get('/work/report_total')
def get_work_report_total(
    start_datetime: Annotated[datetime | None, Query()] = None,
    end_datetime: Annotated[datetime | None, Query()] = None,
) -> WorkReportTotal:
    assert start_datetime and end_datetime or (not start_datetime and not end_datetime)  # FIXME: 400

    if start_datetime is None and end_datetime is None:
        start_datetime, end_datetime = _get_default_report_datetime_range()

    rows = work_get_report_total(start_datetime, end_datetime)
    row = rows[0]

    return WorkReportTotal(
        time=row[0],
    )


@router.post('/work/items/', status_code=201)
def work_items_add(work_item: WorkItem) -> WorkItem:
    work_add(work_item.start_dt, work_item.end_dt, work_item.task_id)
    return work_item


@router.post('/work/start', response_model=WorkItemOut, status_code=201)
def work_start(work_start: WorkStart) -> WorkItemOut:
    print(work_start)
    # TODO: handle 'Cannot start work: already started'
    started_work_item = db_work_start(work_start.task_id, start=work_start.start)
    start_dt = ts_to_dt(started_work_item.start_timestamp)

    return WorkItemOut(
        id=started_work_item.id,
        task_id=started_work_item.task_id,
        start_dt=start_dt,
        end_dt=None,  # end dt of the started work item always is None
    )


@router.post('/work/stop_current', status_code=200)
def work_stop_current() -> None:
    # TODO: handle error
    db_work_stop_current()


# Initialize the DB
Base.metadata.create_all(bind=engine)
# Initialize API
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


if __name__ == '__main__':  # for debug
    import uvicorn
    uvicorn.run('api:app', host='0.0.0.0', port=8874, reload=True)
