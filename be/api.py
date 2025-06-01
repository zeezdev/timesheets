import re
from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, APIRouter, Query, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination, Page
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import schemas
from database import get_db
from dt import ts_to_dt
from schemas import TaskFilterParams
from services import (
    category_list,
    category_create,
    category_read,
    task_list,
    work_item_create,
    work_item_start,
    work_item_stop_current,
    category_update,
    task_read,
    task_update,
    task_create,
    work_get_report_category,
    work_get_report_task,
    work_get_report_total,
    work_item_list,
    work_item_delete, work_item_read, work_item_update, work_item_update_partial, BaseServiceError,
)

origins = [
    "http://localhost:4200",
]

router = APIRouter(prefix='/api')


# Dependency
DbSession = Annotated[Session, Depends(get_db)]


def _get_default_report_datetime_range() -> tuple[datetime, datetime]:
    """
    Makes range for the last month, from start of 21th to end of 20th.

    FIXME: make start day configurable
    """
    # Get the report for the last month
    now = datetime.now()
    curr_month = now.month
    curr_year = now.year
    start = datetime(curr_year, curr_month-1, 21, 0, 0, 0)
    end = datetime(curr_year, curr_month, 20, 23, 59, 59)

    return start, end


@router.get('/categories', response_model=list[schemas.CategoryOut], summary='Get all categories.')
def categories_list(db_session: DbSession):
    """Returns the list of categories"""
    return category_list(db_session)


@router.post('/categories', response_model=schemas.CategoryOut, status_code=201)
def categories_add(category: schemas.CategoryIn, db_session: DbSession):
    """Creates a new category"""
    return category_create(db_session, category.name, category.description)


@router.get('/categories/{category_id}', response_model=schemas.CategoryOut)
def categories_retrieve(category_id: int, db_session: DbSession):
    """Retrieves a category"""
    category = category_read(db_session, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail='Not found')

    return category


@router.put('/categories/{category_id}', response_model=schemas.CategoryOut)
def categories_save(category_id: int, category: schemas.CategoryOut, db_session: DbSession):
    """Updates a category instance"""
    # TODO: use CategoryIn
    updated_category = category_update(db_session, category_id, category.name, category.description)
    return updated_category


@router.get('/tasks', response_model=list[schemas.TaskOut])
def tasks_list(db_session: DbSession, filter_query: TaskFilterParams = Depends()):
    rows = task_list(
        db_session,
        is_archived=filter_query.is_archived,
        is_current=filter_query.is_current,
    )
    return [schemas.TaskOut(
        id=row.id,
        name=row.name,
        category=schemas.CategoryMinimal(
            id=row.category_id,
            name=row.category_name,
        ),
        is_current=row.is_current,
        is_archived=row.is_archived,
    ) for row in rows]


@router.post('/tasks', response_model=schemas.TaskOut, status_code=201)
def tasks_add(task: schemas.TaskIn, db_session: DbSession):
    """Creates a new task"""
    new_task = task_create(db_session, task.name, task.category.id)
    return schemas.TaskOut(
        id=new_task.id,
        name=new_task.name,
        category=schemas.CategoryMinimal(
            id=new_task.category_id,
            name=new_task.category_name,
        ),
        is_current=new_task.is_current,
        is_archived=new_task.is_archived,
    )


@router.get('/tasks/{task_id}', response_model=schemas.TaskOut)
def tasks_retrieve(task_id: int, db_session: DbSession):
    """Retrieves a task"""
    task = task_read(db_session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Not found')

    return schemas.TaskOut(
        id=task.id,
        name=task.name,
        category=schemas.CategoryMinimal(
            id=task.category_id,
            name=task.category_name,
        ),
        is_current=task.is_current,
        is_archived=task.is_archived,
    )


@router.put('/tasks/{task_id}', response_model=schemas.TaskOut)
def tasks_save(task_id: int, task: schemas.TaskUpdate, db_session: DbSession):
    """Updates a task instance"""
    updated_task = task_update(db_session, task_id, task.name, task.category.id, task.is_archived)
    return schemas.TaskOut(
        id=updated_task.id,
        name=updated_task.name,
        category=schemas.CategoryMinimal(
            id=updated_task.category_id,
            name=updated_task.category_name,
        ),
        is_current=updated_task.is_current,
        is_archived=updated_task.is_archived,
    )


@router.get('/work/report_by_category', response_model=list[schemas.WorkReportCategory])
def get_work_report_by_category(
    db_session: DbSession,
    start_datetime: Annotated[datetime | None, Query()] = None,
    end_datetime: Annotated[datetime | None, Query()] = None,
):
    assert start_datetime and end_datetime or (not start_datetime and not end_datetime)  # FIXME: 400

    if start_datetime is None and end_datetime is None:
        start_datetime, end_datetime = _get_default_report_datetime_range()

    rows = work_get_report_category(db_session, start_datetime, end_datetime)
    return [schemas.WorkReportCategory(
        category=schemas.CategoryMinimal(
            id=row[0],
            name=row[1],
        ),
        time=row[2],
    ) for row in rows]


@router.get('/work/report_by_task', response_model=list[schemas.WorkReportTask])
def get_work_report_by_task(
    db_session: DbSession,
    start_datetime: Annotated[datetime | None, Query()] = None,
    end_datetime: Annotated[datetime | None, Query()] = None,
):
    assert start_datetime and end_datetime or (not start_datetime and not end_datetime)  # FIXME: 400

    if start_datetime is None and end_datetime is None:
        start_datetime, end_datetime = _get_default_report_datetime_range()

    rows = work_get_report_task(db_session, start_datetime, end_datetime)
    return [schemas.WorkReportTask(
        task=schemas.TaskWithCategoryMinimal(
            id=row[0],
            name=row[1],
            category=schemas.CategoryMinimal(
                id=row[2],
                name=row[3],
            )
        ),
        time=row[4],
    ) for row in rows]


@router.get('/work/report_total', response_model=schemas.WorkReportTotal)
def get_work_report_total(
    db_session: DbSession,
    start_datetime: Annotated[datetime | None, Query()] = None,
    end_datetime: Annotated[datetime | None, Query()] = None,
):
    assert start_datetime and end_datetime or (not start_datetime and not end_datetime)  # FIXME: 400

    if start_datetime is None and end_datetime is None:
        start_datetime, end_datetime = _get_default_report_datetime_range()

    rows = work_get_report_total(db_session, start_datetime, end_datetime)
    row = rows[0]

    return schemas.WorkReportTotal(
        time=row[0],
    )


@router.post('/work/items/', response_model=schemas.WorkItemOut, status_code=201)
def work_items_add(work_item: schemas.WorkItemIn, db_session: DbSession):
    created_work_item = work_item_create(
        db_session,
        work_item.start_dt,
        work_item.end_dt,
        work_item.task_id,
    )
    return schemas.WorkItemOut(
        id=created_work_item.id,
        start_dt=ts_to_dt(created_work_item.start_timestamp),
        end_dt=created_work_item.end_timestamp and ts_to_dt(created_work_item.end_timestamp),
        task=schemas.TaskMinimal(
            id=created_work_item.task.id,
            name=created_work_item.task.name,
        ),
    )


@router.get('/work/items/', response_model=Page[schemas.WorkItemOut], summary='Get all work items')
def work_items_list(db_session: DbSession, order_by: list[str] = Query(None)):
    order_by_map = {
        'start_dt': 'start_timestamp',
        'end_dt': 'end_timestamp',
    }
    service_order_by = []
    for ob in order_by or []:
        order_by_match = re.match(r'([+-]?)(\w+)', ob)
        if order_by_match is None:
            raise ValueError(f'Incorrect `order_by`: {ob}')
        direction, order_field = order_by_match.groups()
        service_field = f'{direction}{order_by_map.get(order_field, order_field)}'
        service_order_by.append(service_field)

    page = work_item_list(
        db_session,
        service_order_by,
        transformer=lambda items: [{
            'id': item.id,
            'task': {
                'id': item.task_id,
                'name': item.task_name,
            },
            'start_dt': ts_to_dt(item.start_timestamp),
            'end_dt': item.end_timestamp and ts_to_dt(item.end_timestamp),
        } for item in items],
    )
    return page


@router.delete('/work/items/{work_item_id}', status_code=204)
def work_items_remove(work_item_id: int, db_session: DbSession):
    work_item_delete(db_session, work_item_id)


@router.get('/work/items/{work_item_id}', response_model=schemas.WorkItemOut)
def work_items_retrieve(work_item_id: int, db_session: DbSession):
    work_item = work_item_read(db_session, work_item_id)
    return schemas.WorkItemOut(
        id=work_item.id,
        task=schemas.TaskMinimal(
            id=work_item.task.id,
            name=work_item.task.name,
        ),
        start_dt=ts_to_dt(work_item.start_timestamp),
        end_dt=work_item.end_timestamp and ts_to_dt(work_item.end_timestamp),
    )


@router.put('/work/items/{work_item_id}', response_model=schemas.WorkItemOut)
def work_item_save(work_item_id: int, work_item: schemas.WorkItemOut, db_session: DbSession):
    """Updates a work item instance"""
    updated_work_item = work_item_update(
        db_session,
        work_item_id,
        work_item.task.id,
        start=work_item.start_dt,
        end=work_item.end_dt,
    )
    return schemas.WorkItemOut(
        id=updated_work_item.id,
        task=schemas.TaskMinimal(
            id=updated_work_item.task.id,
            name=updated_work_item.task.name,
        ),
        start_dt=ts_to_dt(updated_work_item.start_timestamp),
        end_dt=updated_work_item.end_timestamp and ts_to_dt(updated_work_item.end_timestamp),
    )


@router.patch('/work/items/{work_item_id}', response_model=schemas.WorkItemOut)
def work_item_save_partial(work_item_id: int, work_item: schemas.WorkItemPartialUpdate, db_session: DbSession):
    """Updates a work item instance"""
    updated_work_item = work_item_update_partial(
        db_session,
        work_item_id,
        work_item.task.id,
        start=work_item.start_dt,
        end=work_item.end_dt,
    )
    return schemas.WorkItemOut(
        id=updated_work_item.id,
        task=schemas.TaskMinimal(
            id=updated_work_item.task.id,
            name=updated_work_item.task.name,
        ),
        start_dt=ts_to_dt(updated_work_item.start_timestamp),
        end_dt=updated_work_item.end_timestamp and ts_to_dt(updated_work_item.end_timestamp),
    )


@router.post('/work/start', response_model=schemas.WorkItemOut, status_code=201)
def work_start(work_start: schemas.WorkStart, db_session: DbSession):
    started_work_item = work_item_start(db_session, work_start.task_id, start=work_start.start)

    return schemas.WorkItemOut(
        id=started_work_item.id,
        task=schemas.TaskMinimal(
            id=started_work_item.task.id,
            name=started_work_item.task.name,
        ),
        start_dt=ts_to_dt(started_work_item.start_timestamp),
        end_dt=None,  # end dt of the started work item always is None
    )


@router.post('/work/stop_current', status_code=200)
def work_stop_current(db_session: DbSession):
    # TODO: handle error
    work_item_stop_current(db_session)


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
add_pagination(app)


@app.exception_handler(BaseServiceError)
async def service_error_handler(request: Request, exc: BaseServiceError):
    return JSONResponse(
        status_code=400,
        content=str(exc),
    )


if __name__ == '__main__':  # for debug
    import uvicorn
    uvicorn.run('api:app', host='0.0.0.0', port=8874, reload=True)
