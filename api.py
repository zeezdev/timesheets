from datetime import datetime
from itertools import islice
from typing import Union, Annotated

from fastapi import FastAPI, APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import (
    category_list,
    category_create,
    category_read,
    task_list,
    work_get_report_category,
    work_add,
    work_get_report_total,
    work_start as db_work_start,
    work_stop_current as db_work_stop_current, category_update, work_get_report_task, task_read, task_update, task_add,
    work_read, ts_to_dt,
)


class CategoryBase(BaseModel):
    name: str
    description: Union[str, None] = None


class CategoryIn(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int


class TaskBase(BaseModel):
    name: str
    category_id: int


class TaskIn(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    is_current: int


class WorkReportCategory(BaseModel):
    category_id: int
    category_name: str
    time: float


class WorkReportTask(BaseModel):
    task_id: int
    task_name: str
    category_id: int
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


@router.get('/categories')
def categories_list() -> list[CategoryOut]:
    """Returns the list of categories"""
    rows = category_list()
    return [CategoryOut(
        id=row[0],
        name=row[1],
        description=row[2],
    ) for row in islice(rows, 1, None)]


@router.post('/categories', response_model=CategoryOut, status_code=201)
def categories_add(category: CategoryIn) -> CategoryOut:
    """Creates a new category"""
    result = category_create(name=category.name, description=category.description)
    rows = category_read(_id=result)
    rows = islice(rows, 1, None)  # exclude header
    new_category = next(rows)
    return CategoryOut(
        id=new_category[0],
        name=new_category[1],
        description=new_category[2],
    )


@router.get('/categories/{category_id}')
def categories_retrieve(category_id: int) -> CategoryOut:
    """Retrieves a category"""
    rows = category_read(_id=category_id)
    rows = islice(rows, 1, None)  # exclude header
    category = next(rows)
    return CategoryOut(
        id=category[0],
        name=category[1],
        description=category[2],
    )


@router.put('/categories/{category_id}', response_model=CategoryOut)
def categories_save(category_id: int, category: CategoryOut) -> CategoryOut:
    """Updates a category instance"""
    # TODO: use CategoryIn
    category_update(category_id, category.name, category.description)
    # Retrieve
    rows = category_read(_id=category_id)
    rows = islice(rows, 1, None)  # exclude header
    category = next(rows)
    return CategoryOut(
        id=category[0],
        name=category[1],
        description=category[2],
    )


@router.get('/tasks')
def tasks_list() -> list[TaskOut]:
    rows = task_list()
    return [TaskOut(
        id=row[0],
        name=row[1],
        category_id=row[2],
        is_current=row[3],
    ) for row in islice(rows, 1, None)]


@router.post('/tasks', response_model=TaskOut, status_code=201)
def tasks_add(task: TaskIn) -> TaskOut:
    """Creates a new task"""
    result = task_add(name=task.name, category_id=task.category_id)

    rows = task_read(_id=result)
    rows = islice(rows, 1, None)  # exclude header
    new_task = next(rows)
    return TaskOut(
        id=new_task[0],
        name=new_task[1],
        category_id=new_task[2],
        is_current=new_task[3],
    )


@router.get('/tasks/{task_id}', response_model=TaskOut)
def tasks_retrieve(task_id: int) -> TaskOut:
    """Retrieves a task"""
    rows = task_read(_id=task_id)
    rows = islice(rows, 1, None)  # exclude header
    task = next(rows)
    return TaskOut(
        id=task[0],
        name=task[1],
        category_id=task[2],
        is_current=task[3],
    )


@router.put('/tasks/{task_id}', response_model=TaskOut)
def tasks_save(task_id: int, task: TaskOut) -> TaskOut:
    """Updates a task instance"""
    task_update(task_id, task.name, task.category_id)
    # Retrieve
    rows = task_read(_id=task_id)
    rows = islice(rows, 1, None)  # exclude header
    task = next(rows)
    return TaskOut(
        id=task[0],
        name=task[1],
        category_id=task[2],
        is_current=task[3],
    )


@router.get('/work/report_by_category')
def get_work_report_by_category(
    start_datetime: Annotated[datetime | None, Body()] = None,
    end_datetime: Annotated[datetime | None, Body()] = None,
) -> list[WorkReportCategory]:
    assert start_datetime and end_datetime or (not start_datetime and not end_datetime)  # FIXME: 400

    if not start_datetime and not end_datetime:
        curr_month = datetime.now().month
        curr_year = datetime.now().year
        curr_day = datetime.now().day  # FIXME:

        start_datetime = datetime(curr_year, curr_month-1, 21, 0, 0, 0)
        end_datetime = datetime(curr_year, curr_month, 20, 23, 59, 59)

    rows = work_get_report_category(start_datetime, end_datetime)
    return [WorkReportCategory(
        category_id=row[0],
        category_name=row[1],
        time=row[2],
    ) for row in islice(rows, 1, None)]


@router.get('/work/report_by_task')
def get_work_report_by_task(
    start_datetime: Annotated[datetime | None, Body()] = None,
    end_datetime: Annotated[datetime | None, Body()] = None,
) -> list[WorkReportTask]:
    assert start_datetime and end_datetime or (not start_datetime and not end_datetime)  # FIXME: 400

    if not start_datetime and not end_datetime:
        curr_month = datetime.now().month
        curr_year = datetime.now().year
        curr_day = datetime.now().day  # FIXME:

        start_datetime = datetime(curr_year, curr_month-1, 21, 0, 0, 0)
        end_datetime = datetime(curr_year, curr_month, 20, 23, 59, 59)

    rows = work_get_report_task(start_datetime, end_datetime)
    return [WorkReportTask(
        task_id=row[0],
        task_name=row[1],
        category_id=row[2],
        time=row[3],
    ) for row in islice(rows, 1, None)]


@router.get('/work/report_total')
def get_work_report_total(
    start_datetime: Annotated[datetime | None, Body()] = None,
    end_datetime: Annotated[datetime | None, Body()] = None,
) -> WorkReportTotal:
    assert start_datetime and end_datetime or (not start_datetime and not end_datetime)  # FIXME: 400

    if not start_datetime and not end_datetime:
        # Get report for the last month
        curr_month = datetime.now().month
        curr_year = datetime.now().year
        curr_day = datetime.now().day  # FIXME:

        start_datetime = datetime(curr_year, curr_month-1, 21, 0, 0, 0)
        end_datetime = datetime(curr_year, curr_month, 20, 23, 59, 59)

    rows = work_get_report_total(start_datetime, end_datetime)
    rows = islice(rows, 1, None)
    row = next(rows)

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
    result = db_work_start(work_start.task_id, start=work_start.start)

    rows = work_read(_id=result)
    rows = islice(rows, 1, None)  # exclude header
    started_work_item = next(rows)
    start_dt = ts_to_dt(started_work_item[2])

    return WorkItemOut(
        id=started_work_item[0],
        task_id=started_work_item[1],
        start_dt=start_dt,
        end_dt=None,  # end dt of the started work item always is None
    )


@router.post('/work/stop_current', status_code=200)
def work_stop_current() -> None:
    # TODO: handle error
    db_work_stop_current()


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
    uvicorn.run(app, host='localhost', port=8874)
