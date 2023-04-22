from datetime import datetime
from itertools import islice
from typing import Union, Optional

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import category_list, task_list, work_get_report_category, work_add, work_get_report_total, work_start as db_work_start, work_stop_current as db_work_stop_current


class Category(BaseModel):
    id: int
    name: str
    description: Union[str, None] = None


class Task(BaseModel):
    id: int
    name: str
    category_id: int


class WorkReportCategory(BaseModel):
    category_id: int
    category_name: str
    time: float


class WorkReportTotal(BaseModel):
    time: float


class WorkItem(BaseModel):
    start_dt: datetime
    end_dt: datetime
    task_id: int


class WorkStart(BaseModel):
    task_id: int
    start: Optional[int]


# https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    "http://localhost:4200",
]

router = APIRouter(prefix='/api')


@router.get('/categories')
def read_categories() -> list[Category]:
    rows = category_list()
    return [Category(
        id=row[0],
        name=row[1],
        description=row[2],
    ) for row in islice(rows, 1, None)]


@router.get('/tasks')
def read_tasks() -> list[Task]:
    rows = task_list()
    return [Task(
        id=row[0],
        name=row[1],
        category_id=row[2],
    ) for row in islice(rows, 1, None)]


@router.get('/work/report_by_category')
def get_work_report_by_category() -> list[WorkReportCategory]:
    curr_month = datetime.now().month
    curr_year = datetime.now().year
    curr_day = datetime.now().day  # FIXME:

    start_dt = datetime(curr_year, curr_month-1, 21, 0, 0, 0)
    end_dt = datetime(curr_year, curr_month, 20, 23, 59, 59)

    rows = work_get_report_category(start_dt, end_dt)
    return [WorkReportCategory(
        category_id=row[0],
        category_name=row[1],
        time=row[2],
    ) for row in islice(rows, 1, None)]


@router.get('/work/report_total')
def get_work_report_total() -> WorkReportTotal:
    """Last month"""
    curr_month = datetime.now().month
    curr_year = datetime.now().year
    curr_day = datetime.now().day  # FIXME:

    start_dt = datetime(curr_year, curr_month-1, 21, 0, 0, 0)
    end_dt = datetime(curr_year, curr_month, 20, 23, 59, 59)

    rows = work_get_report_total(start_dt, end_dt)
    rows = islice(rows, 1, None)
    row = next(rows)

    return WorkReportTotal(
        time=row[0],
    )


@router.post('/work/items/', status_code=201)
def work_items_add(work_item: WorkItem) -> WorkItem:
    work_add(work_item.start_dt, work_item.end_dt, work_item.task_id)
    return work_item


@router.post('/work/start', status_code=200)
def work_start(work_start: WorkStart) -> None:
    print(work_start)
    # TODO: handle 'Cannot start work: already started'
    db_work_start(work_start.task_id, start=work_start.start)


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
