import os
import logging
import time
from datetime import datetime, tzinfo, timezone
from typing import Sequence, Type

from sqlalchemy import create_engine, Row, select, case, literal_column, and_, text
from sqlalchemy.orm import sessionmaker

from models import Task, Category, WorkItem

logger = logging.getLogger(__name__)


def get_database_name() -> str:
    return os.getenv('TIMESHEET_DB_FILENAME', '../db/timesheet.db')


engine = create_engine(f'sqlite:///{get_database_name()}', echo=True)
Session = sessionmaker(bind=engine)


def get_local_tz() -> tzinfo:
    return datetime.now().astimezone().tzinfo


def dt_to_ts(dt: datetime) -> int:
    """Convert a given datetime into the timestamp in UTC TZ."""
    if dt.tzinfo is None:
        # If dt is a naive (no tzinfo provided) then set up a local tz
        dt_without_tz = dt
        dt_with_tz = dt.replace(tzinfo=get_local_tz())
    else:
        dt_with_tz = dt
        dt_without_tz = dt.replace(tzinfo=None)

    utc_dt = dt_without_tz - dt_with_tz.utcoffset()
    timestamp = time.mktime(utc_dt.timetuple())
    return int(timestamp)


def ts_to_dt(ts: int) -> datetime:
    """Convert UTC ts to local dt."""
    return datetime.fromtimestamp(ts).replace(tzinfo=timezone.utc).astimezone()


def get_now_timestamp() -> int:
    """Return current timestamp in UTC TZ."""
    local_dt = datetime.now()
    utc_dt = local_dt - local_dt.astimezone().utcoffset()
    timestamp = time.mktime(utc_dt.timetuple())
    # TODO: utctimetuple ?
    return int(timestamp)


# CATEGORY

def category_create(name: str, description: str | None = None) -> Category:
    # return execute_statement('INSERT INTO main.categories (name, description) VALUES (?, ?)', name, description)
    session = Session()
    obj = Category(name=name, description=description)
    session.add(obj)
    session.commit()
    return obj


def category_delete(id_: int) -> None:
    """DELETE FROM main.categories WHERE id=?"""
    Session().query(Category).filter(Category.id == id_).delete()


def category_update(id_: int, name: str, description: str) -> Category | None:
    """UPDATE main.categories SET name=?, description=? WHERE id=?, name, description, id_"""
    session = Session()
    session.query(Category).filter(Category.id == id_).update({
        'name': name,
        'description': description,
    })
    session.commit()
    return category_read(id_)


def category_list() -> list[Type[Category]]:
    """SELECT id, name, description FROM categories ORDER BY id"""
    rows = Session().query(Category).order_by(Category.id).all()
    return rows


def category_read(id_: int) -> Category | None:
    """SELECT id, name, description FROM main.categories WHERE id=?, _id"""
    row = Session().query(Category).filter(Category.id == id_).one_or_none()
    return row


def category_print_all() -> None:
    """Deprecated. TODO: remove"""
    rows = category_list()
    for row in rows:
        print(row)


# TASK

def task_add(name: str, category_id: int) -> Task | None:
    """INSERT INTO main.tasks (name, category_id) VALUES (?, ?), name, category_id"""
    obj = Task(name=name, category_id=category_id)
    session = Session()
    session.add(obj)
    session.commit()
    return task_read(obj.id)


def task_delete(id_: int) -> None:
    """DELETE FROM main.tasks WHERE id=?, id_"""
    Session().query(Task).filter(Task.id == id_).delete()


def task_update(id_: int, name: str, category_id: int) -> Task | None:
    """UPDATE main.tasks SET name=?, category_id=? WHERE id=?, name, category_id, id_"""
    session = Session()
    session.query(Task).filter(Task.id == id_).update({
        'name': name,
        'category_id': category_id,
    })
    session.commit()
    return task_read(id_)


def task_print_all() -> None:
    rows = task_list()
    for row in rows:
        print(row)


def task_list() -> Sequence[Row]:
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
    rows = Session().execute(smth).all()
    return rows


def task_read(id_: int) -> Row[tuple] | None:
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
    row = Session().execute(smth).one_or_none()
    return row


# WORK

def work_list() -> list[Type[WorkItem]]:
    return Session().query(WorkItem).order_by(WorkItem.start_timestamp).all()


def work_read(id_: int) -> WorkItem | None:
    """
    SELECT id, task_id, start_timestamp, end_timestamp FROM main.work_items WHERE id=?, id_
    """
    return Session().query(WorkItem).filter(WorkItem.id == id_).one_or_none()


def work_start(task_id: int, start: int | None = None) -> WorkItem | None:
    """
    SELECT id FROM main.work_items WHERE end_timestamp IS NULL
    INSERT INTO main.work_items (task_id, start_timestamp) VALUES (?,?), task_id, start
    """
    session = Session()
    started_work_item = session.query(WorkItem).filter(WorkItem.end_timestamp.is_(None)).one_or_none()

    # Validate active work
    if started_work_item is not None:
        raise Exception('Cannont start work: already started')

    start = start or get_now_timestamp()
    obj = WorkItem(task_id=task_id, start_timestamp=start)
    session.add(obj)
    session.commit()
    return work_read(obj.id)


def work_stop_current() -> None:
    """
    SELECT * FROM main.work_items WHERE end_timestamp IS NULL ORDER BY start_timestamp DESC
    UPDATE main.work_items SET end_timestamp=? WHERE id=?, end_ts, id_
    """
    session = Session()
    res = session.query(WorkItem).filter(WorkItem.end_timestamp.is_(None)).one_or_none()
    # TODO: handle multiple objects error

    if res is None:
        raise Exception('There is no work item to stop!')

    res.end_timestamp = get_now_timestamp()
    session.commit()
    logger.info('Work stopped')


def work_add(start_dt: datetime, end_dt: datetime, task_id: int) -> WorkItem | None:
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
    session = Session()
    session.add(obj)
    session.commit()
    return work_read(obj.id)


def work_delete(id_: int) -> None:
    """DELETE FROM main.work_items WHERE id = ?, id_"""
    Session().query(WorkItem).filter(WorkItem.id == id_).delete()


def work_print_all():
    rows = work_list()
    for row in rows:
        print(row)


# Reporting

def work_get_report_category(start_dt: datetime, end_dt: datetime) -> Sequence[Row]:
    """
    category_id, catrgory_name, work_seconds
    """
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)
    now_ts = get_now_timestamp()

    return Session().execute(
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
        # start_ts, start_ts,  # WHEN (...) END start_ts
        # now_ts, end_ts,  # WHEN (...) END end_ts
        # end_ts, now_ts,  # THEN ? ELSE COALESCE(wi.end_timestamp, ?)
        # start_ts, end_ts,  # wi.start_timestamp >= ? AND wi.start_timestamp < ?
        # now_ts, start_ts, now_ts, end_ts,  # COALESCE(wi.end_timestamp, ?) > ? AND COALESCE(wi.end_timestamp, ?) <= ?
        # start_ts, end_ts,  # OR (wi.start_timestamp < ? AND wi.end_timestamp > ?)
    ).all()


def work_get_report_task(start_dt: datetime, end_dt: datetime) -> Sequence[Row]:
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)
    now_ts = get_now_timestamp()

    return Session().execute(text(
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
        # start_ts, start_ts,  # WHEN (...) END start_ts
        # now_ts, end_ts,  # WHEN (...) END end_ts
        # end_ts, now_ts,  # THEN ? ELSE COALESCE(wi.end_timestamp, ?)
        # start_ts, end_ts,  # wi.start_timestamp >= ? AND wi.start_timestamp < ?
        # now_ts, start_ts, now_ts, end_ts,  # COALESCE(wi.end_timestamp, ?) > ? AND COALESCE(wi.end_timestamp, ?) <= ?
        # start_ts, end_ts,  # OR (wi.start_timestamp < ? AND wi.end_timestamp > ?)
    ).all()


def work_get_report_total(start_dt: datetime, end_dt: datetime) -> Sequence[Row]:
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)
    now_ts = get_now_timestamp()

    return Session().execute(text(
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
               COALESCE(wi.end_timestamp, :now_ts) > :start_ts AND COALESCE(wi.end_timestamp, :now_ts <= :end_ts)
           ) OR (wi.start_timestamp < :start_ts AND wi.end_timestamp > :end_ts)
        ) ww
        """).bindparams(
            start_ts=start_ts,
            end_ts=end_ts,
            now_ts=now_ts,
        ),
        # start_ts, start_ts,  # WHEN (...) END start_ts
        # now_ts, end_ts,  # WHEN (...) END end_ts
        # end_ts, now_ts,  # THEN ? ELSE COALESCE(wi.end_timestamp, ?)
        # start_ts, end_ts,  # wi.start_timestamp >= ? AND wi.start_timestamp < ?
        # now_ts, start_ts, now_ts, end_ts,  # COALESCE(wi.end_timestamp, ?) > ? AND COALESCE(wi.end_timestamp, ?) <= ?
        # start_ts, end_ts,  # OR (wi.start_timestamp < ? AND wi.end_timestamp > ?)
    ).all()
