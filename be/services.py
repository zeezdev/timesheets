import logging
import re
from collections.abc import Callable
from datetime import datetime
from typing import Sequence, Type, Any

from fastapi import HTTPException
from sqlalchemy import Row, select, case, literal_column, and_, text, desc, or_, Boolean
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from dt import dt_to_ts, get_now_timestamp

from models import Task, Category, WorkItem

logger = logging.getLogger(__name__)


class BaseServiceError(Exception):
    pass


class WorkItemStartAlreadyStartedError(BaseServiceError):
    pass


class WorkItemDtRangeValidationError(BaseServiceError):
    def __init__(self, message: str):
        super().__init__(message)


# CATEGORY

def category_create(db_session: Session, name: str, description: str | None) -> Category:
    # return execute_statement('INSERT INTO main.categories (name, description) VALUES (?, ?)', name, description)
    obj = Category(name=name, description=description)
    db_session.add(obj)
    db_session.flush()
    db_session.refresh(obj)
    return obj


def category_delete(db_session: Session, id_: int) -> None:
    """DELETE FROM main.categories WHERE id=?"""
    db_session.query(Category).filter(Category.id == id_).delete()


def category_update(db_session: Session, id_: int, name: str, description: str) -> Category | None:
    """UPDATE main.categories SET name=?, description=? WHERE id=?, name, description, id_"""
    db_session.query(Category).filter(Category.id == id_).update({
        'name': name,
        'description': description,
    })
    db_session.flush()
    return category_read(db_session, id_)


def category_list(db_session: Session) -> list[Type[Category]]:
    """SELECT id, name, description FROM categories ORDER BY id"""
    rows = db_session.query(Category).order_by(Category.id).all()
    return rows


def category_read(db_session: Session, id_: int) -> Category | None:
    """SELECT id, name, description FROM main.categories WHERE id=?, _id"""
    row = db_session.query(Category).filter(Category.id == id_).one_or_none()
    return row


# TASK

def task_create(db_session: Session, name: str, category_id: int) -> Task | None:
    """INSERT INTO main.tasks (name, category_id) VALUES (?, ?), name, category_id"""
    obj = Task(name=name, category_id=category_id)
    db_session.add(obj)
    db_session.flush()
    return task_read(db_session, obj.id)


def task_delete(db_session: Session, id_: int) -> None:
    """DELETE FROM main.tasks WHERE id=?, id_"""
    db_session.query(Task).filter(Task.id == id_).delete()


def task_update(db_session: Session, id_: int, name: str, category_id: int, is_archived: bool) -> Row[tuple]:
    """Update name, category_id, is_archived of the task by id_"""
    db_session.query(Task).filter(Task.id == id_).update({
        'name': name,
        'category_id': category_id,
        'is_archived': is_archived,  # TODO: validate current task cannot be archived
    })
    db_session.commit()
    return task_read(db_session, id_)


def task_list(
        db_session: Session,
        is_archived: bool | None = None,
        is_current: bool | None = None,
) -> Sequence[Row]:
    """
    'SELECT t.id, t.name, t.category_id, c.name AS category_name, t.is_archived, '
    'CASE WHEN w.id IS NULL THEN 0 ELSE 1 END is_current '
    'FROM main.tasks AS t '
    'LEFT JOIN main.work_items AS w ON (t.id = w.task_id AND w.end_timestamp is NULL)'
    'JOIN main.categories AS c ON (t.category_id = c.id)'
    'ORDER BY t.id'
    """
    smth = select(
        Task.id,
        Task.name,
        Task.category_id,
        Category.name.label('category_name'),
        Task.is_archived,
        case(
            (
                WorkItem.id.is_(None),
                literal_column('FALSE', Boolean),
            ),
            else_=literal_column('TRUE', Boolean)
        ).label('is_current'),
    ).join(
        Task.category
    ).join(
        WorkItem,
        onclause=and_(Task.id == WorkItem.task_id, WorkItem.end_timestamp.is_(None)),
        isouter=True,  # LEFT OUTER JOIN
    ).order_by(desc(Task.id))
    # Filtration
    if is_archived is not None:
        smth = smth.filter(Task.is_archived == is_archived)
    if is_current is not None:
        smth = smth.filter(literal_column('is_current', Boolean) == is_current)

    rows = db_session.execute(smth).all()
    return rows


def task_read(db_session: Session, id_: int) -> Row[tuple] | None:
    """
    'SELECT t.id, t.name, t.category_id, c.name AS category_name, '
    'CASE WHEN w.id IS NULL THEN 0 ELSE 1 END is_current '
    'FROM main.tasks AS t '
    'LEFT JOIN main.work_items AS w ON (t.id = w.task_id AND w.end_timestamp is NULL)'
    'JOIN main.categories AS c ON (t.category_id = c.id)'
    'WHERE t.id=?',
    id_,
    """
    smth = select(
        Task.id,
        Task.name,
        Task.category_id,
        Category.name.label('category_name'),
        Task.is_archived,
        case(
            (
                WorkItem.id.is_(None),
                literal_column('0'),
            ),
            else_=literal_column('1')
        ).label('is_current'),
    ).join(
        Task.category
    ).join(
        WorkItem,
        onclause=and_(Task.id == WorkItem.task_id, WorkItem.end_timestamp.is_(None)),
        isouter=True,  # LEFT OUTER JOIN
    ).filter(Task.id == id_)
    row = db_session.execute(smth).one_or_none()
    return row


# WORK

def work_item_list(db_session: Session, order_by: list[str], transformer: Callable) -> Any:
    # order_by expression processing
    ordering = []
    for ob in order_by:
        order_by_match = re.match(r'([+-]?)(\w+)', ob)
        if order_by_match is None:
            raise ValueError(f'Incorrect `order_by` element: {ob}')
        direction, order_field = order_by_match.groups()
        model_column = getattr(WorkItem, order_field, None)
        if model_column is None:
            raise ValueError(f'Cannot find model column for `order_by` element: {ob}')

        if direction == '-':
            model_column = desc(model_column)
        ordering.append(model_column)

    return paginate(
        db_session,
        select(
            WorkItem.id,
            WorkItem.task_id,
            Task.name.label('task_name'),
            WorkItem.start_timestamp,
            WorkItem.end_timestamp,
        ).join(
            WorkItem.task,
        ).order_by(*ordering),
        transformer=transformer,
    )


def work_item_read(db_session: Session, id_: int) -> WorkItem | None:
    return db_session.query(WorkItem).filter(WorkItem.id == id_).one_or_none()
    # work_item = db_session.get(WorkItem, id_)
    # if work_item is None:
    #     raise HTTPException(status_code=404, detail='WorkItem not found')
    # return work_item


def work_item_start(db_session: Session, task_id: int, start: int | None) -> WorkItem:
    """
    SELECT id FROM main.work_items WHERE end_timestamp IS NULL
    INSERT INTO main.work_items (task_id, start_timestamp) VALUES (?,?), task_id, start
    # FIXME: this the same as `work_item_create` but from now
    """
    started_work_item = db_session.query(WorkItem).filter(WorkItem.end_timestamp.is_(None)).one_or_none()

    # Validate active work
    if started_work_item is not None:
        raise WorkItemStartAlreadyStartedError('Cannot start work: already started')

    start = start or get_now_timestamp()
    obj = WorkItem(task_id=task_id, start_timestamp=start)
    db_session.add(obj)
    db_session.flush()
    db_session.refresh(obj)
    return obj


def work_item_stop_current(db_session: Session) -> None:
    """
    SELECT * FROM main.work_items WHERE end_timestamp IS NULL ORDER BY start_timestamp DESC
    UPDATE main.work_items SET end_timestamp=? WHERE id=?, end_ts, id_
    """
    res = db_session.query(WorkItem).filter(WorkItem.end_timestamp.is_(None)).one_or_none()
    # TODO: handle multiple objects error

    if res is None:
        raise Exception('There is no work item to stop!')

    res.end_timestamp = get_now_timestamp()
    db_session.flush()
    logger.info('Work stopped')


def _work_item_dt_range_validation(
    db_session: Session,
    object_id: int | None,
    start_ts: int,
    end_ts: int | None,
) -> None:
    # 1. Validate
    if end_ts is not None and start_ts >= end_ts:
        raise WorkItemDtRangeValidationError(
            'The start date and time of the work element must be before its end.'
        )

    # 2. Validate existing work items
    conditions = [
        # for all work items
        and_(WorkItem.start_timestamp <= start_ts, WorkItem.end_timestamp >= start_ts),
    ]
    if end_ts is None:
        conditions.append(WorkItem.end_timestamp == None)  # only one current WI is available
    else:
        conditions.extend([
            # for finished work items
            and_(WorkItem.start_timestamp <= end_ts, WorkItem.end_timestamp >= end_ts),
            # for current work item (if exists)
            and_(WorkItem.end_timestamp == None, WorkItem.start_timestamp <= end_ts),
        ])

    filters = [
        or_(*conditions),
    ]
    if object_id is not None:  # on create
        filters.append(WorkItem.id != object_id)

    result = db_session.query(WorkItem).filter(*filters).one_or_none()
    if result is not None:
        raise WorkItemDtRangeValidationError('The work item with this date and time range already exists.')


def work_item_create(db_session: Session, start_dt: datetime, end_dt: datetime | None, task_id: int) -> WorkItem:
    start_ts = dt_to_ts(start_dt)
    end_ts = end_dt and dt_to_ts(end_dt)
    _work_item_dt_range_validation(db_session, None, start_ts, end_ts)

    obj = WorkItem(
        task_id=task_id,
        start_timestamp=start_ts,
        end_timestamp=end_ts,
    )
    db_session.add(obj)
    db_session.flush()
    db_session.refresh(obj)
    return obj


def work_item_delete(db_session: Session, id_: int) -> None:
    work_item = db_session.get(WorkItem, id_)
    if work_item is None:
        raise HTTPException(status_code=404, detail='WorkItem not found')
    db_session.delete(work_item)
    db_session.commit()


def work_item_update(db_session: Session, id_: int, task_id: int, start: datetime, end: datetime | None) -> WorkItem:
    start_ts = dt_to_ts(start)
    end_ts = end and dt_to_ts(end)
    _work_item_dt_range_validation(db_session, id_, start_ts, end_ts)

    db_session.query(WorkItem).filter(WorkItem.id == id_).update({
        'task_id': task_id,
        'start_timestamp': start_ts,
        'end_timestamp': end_ts,
    })
    db_session.commit()
    return work_item_read(db_session, id_)


def work_item_update_partial(
    db_session: Session,
    id_: int,
    task_id: int | None,
    start: datetime | None,
    end: datetime | None,
) -> WorkItem:
    work_item = work_item_read(db_session, id_)

    if task_id is not None:
        work_item.task_id = task_id
    if start is not None:
        work_item.start_timestamp = dt_to_ts(start)
    if end is not None:
        work_item.end_timestamp = dt_to_ts(end)

    _work_item_dt_range_validation(
        db_session,
        id_,
        work_item.start_timestamp,
        work_item.end_timestamp,
    )

    db_session.commit()

    return work_item


# Reporting

def work_get_report_category(db_session: Session, start_dt: datetime, end_dt: datetime) -> Sequence[Row]:
    """
    category_id, category_name, work_seconds
    """
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)
    now_ts = get_now_timestamp()

    return db_session.execute(
        text(
        """
        SELECT t.category_id, c.name AS catrgory_name,
        COALESCE(SUM(ww.end_ts - ww.start_ts), 0) AS work_seconds 
        FROM (
           SELECT wi.task_id,
               CASE 
                   WHEN (wi.start_timestamp < :start_ts) THEN :start_ts ELSE wi.start_timestamp
               END start_ts,
               CASE 
                   WHEN (COALESCE(wi.end_timestamp, :now_ts) > :end_ts) THEN :end_ts ELSE COALESCE(wi.end_timestamp, :now_ts)
               END end_ts
           FROM main.work_items wi
           WHERE (
               wi.start_timestamp >= :start_ts AND wi.start_timestamp < :end_ts
           ) OR (
               COALESCE(wi.end_timestamp, :now_ts) > :start_ts AND COALESCE(wi.end_timestamp, :now_ts) <= :end_ts
           ) OR (wi.start_timestamp < :start_ts AND wi.end_timestamp > :end_ts)
        ) ww 
        INNER JOIN main.tasks t ON (ww.task_id = t.id) 
        INNER JOIN main.categories c ON (t.category_id = c.id) 
        GROUP BY t.category_id, c.name
        """).bindparams(**{
            'start_ts': start_ts,
            'now_ts': now_ts,
            'end_ts': end_ts,
        }),
    ).all()


def work_get_report_task(db_session: Session, start_dt: datetime, end_dt: datetime) -> Sequence[Row]:
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)
    now_ts = get_now_timestamp()

    return db_session.execute(text(
        """
        SELECT ww.task_id, t.name AS task_name, t.category_id, c.name AS category_name,
        COALESCE(SUM(ww.end_ts - ww.start_ts), 0) AS work_seconds 
        FROM (
           SELECT wi.task_id,
               CASE 
                   WHEN (wi.start_timestamp < :start_ts) THEN :start_ts ELSE wi.start_timestamp
               END start_ts,
               CASE 
                   WHEN (COALESCE(wi.end_timestamp, :now_ts) > :end_ts) THEN :end_ts ELSE COALESCE(wi.end_timestamp, :now_ts)
               END end_ts
           FROM main.work_items wi
           WHERE (
               wi.start_timestamp >= :start_ts AND wi.start_timestamp < :end_ts
           ) OR (
               COALESCE(wi.end_timestamp, :now_ts) > :start_ts AND COALESCE(wi.end_timestamp, :now_ts) <= :end_ts
           ) OR (wi.start_timestamp < :start_ts AND wi.end_timestamp > :end_ts)
        ) ww 
        INNER JOIN main.tasks t ON (ww.task_id = t.id) 
        JOIN main.categories c ON (t.category_id = c.id) 
        GROUP BY ww.task_id, t.name, t.category_id
        """).bindparams(
            start_ts=start_ts,
            end_ts=end_ts,
            now_ts=now_ts,
        ),
    ).all()


def work_get_report_total(db_session: Session, start_dt: datetime, end_dt: datetime) -> Sequence[Row]:
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)
    now_ts = get_now_timestamp()

    return db_session.execute(text(
        """
        SELECT COALESCE(SUM(ww.end_ts - ww.start_ts), 0) AS work_seconds
        FROM (
           SELECT 
               CASE 
                   WHEN (wi.start_timestamp < :start_ts) THEN :start_ts ELSE wi.start_timestamp
               END start_ts,
               CASE 
                   WHEN (COALESCE(wi.end_timestamp, :now_ts) > :end_ts) THEN :end_ts ELSE COALESCE(wi.end_timestamp, :now_ts)
               END end_ts
           FROM main.work_items wi
           WHERE (
               wi.start_timestamp >= :start_ts AND wi.start_timestamp < :end_ts
           ) OR (
               COALESCE(wi.end_timestamp, :now_ts) > :start_ts AND COALESCE(wi.end_timestamp, :now_ts) <= :end_ts
           ) OR (wi.start_timestamp < :start_ts AND wi.end_timestamp > :end_ts)
        ) ww
        """).bindparams(
            start_ts=start_ts,
            end_ts=end_ts,
            now_ts=now_ts,
        ),
    ).all()
