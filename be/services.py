import logging
from datetime import datetime
from typing import Sequence, Type

from sqlalchemy import Row, select, case, literal_column, and_, text
from sqlalchemy.orm import Session

from dt import dt_to_ts, get_now_timestamp

from models import Task, Category, WorkItem

logger = logging.getLogger(__name__)


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


def task_update(db_session: Session, id_: int, name: str, category_id: int) -> Task | None:
    """UPDATE main.tasks SET name=?, category_id=? WHERE id=?, name, category_id, id_"""
    db_session.query(Task).filter(Task.id == id_).update({
        'name': name,
        'category_id': category_id,
    })
    db_session.commit()
    return task_read(db_session, id_)


def task_list(db_session: Session) -> Sequence[Row]:
    """
    'SELECT t.id, t.name, t.category_id, c.name AS category_name,'
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
    ).order_by(Task.id)
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

def work_item_list(db_session: Session) -> list[Type[WorkItem]]:
    return db_session.query(WorkItem).order_by(WorkItem.start_timestamp).all()


def work_item_read(db_session: Session, id_: int) -> WorkItem | None:
    """
    SELECT id, task_id, start_timestamp, end_timestamp FROM main.work_items WHERE id=?, id_
    """
    return db_session.query(WorkItem).filter(WorkItem.id == id_).one_or_none()


def work_item_start(db_session: Session, task_id: int, start: int | None) -> WorkItem:
    """
    SELECT id FROM main.work_items WHERE end_timestamp IS NULL
    INSERT INTO main.work_items (task_id, start_timestamp) VALUES (?,?), task_id, start
    # FIXME: this the same as `work_item_create` but from now
    """
    started_work_item = db_session.query(WorkItem).filter(WorkItem.end_timestamp.is_(None)).one_or_none()

    # Validate active work
    if started_work_item is not None:
        raise Exception('Cannot start work: already started')

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


def work_item_create(db_session: Session, start_dt: datetime, end_dt: datetime, task_id: int) -> WorkItem:
    """
    INSERT INTO main.work_items (task_id, start_timestamp, end_timestamp) VALUES (?,?,?), task_id, start_ts, end_ts
    """
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)
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
    """DELETE FROM main.work_items WHERE id = ?, id_"""
    db_session.query(WorkItem).filter(WorkItem.id == id_).delete()
    db_session.flush()


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
