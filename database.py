import contextlib
import importlib.util
import logging
import sqlite3
import time
from datetime import datetime, tzinfo, timezone
from itertools import chain
from pathlib import Path
from sqlite3 import Connection

logger = logging.getLogger(__name__)


def get_database_name() -> str:
    return 'timesheet.db'


def get_connection(database_name: str | None = None) -> Connection:
    database_name = database_name or get_database_name()
    con = sqlite3.connect(database_name)
    con.isolation_level = None
    return con


def get_cursor(con):
    cur = con.cursor()
    return cur


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


def get_header(cursor) -> tuple[str]:
    return tuple(i[0] for i in cursor.description)


def execute_statement(statement, *args):
    with contextlib.closing(get_connection()) as con: # auto-closes
        with con: # auto-commits
            with contextlib.closing(get_cursor(con)) as cursor: # auto-closes
                try:
                    res = cursor.execute(statement, tuple(args))
                except sqlite3.InterfaceError:
                    logger.exception('Failed to execute statement "%s" with args=%s', statement, args)

                if cursor.description is not None:
                    header = get_header(cursor)
                    return chain([header], res.fetchall())
                else:
                    return cursor.lastrowid  # always == 0 for update


# CATEGORY

def category_create(name: str, description: str | None = None) -> int:
    return execute_statement('INSERT INTO main.categories (name, description) VALUES (?, ?)', name, description)


def category_delete(_id: int) -> None:
    execute_statement('DELETE FROM main.categories WHERE id=?', _id)


def category_update(_id: int, name: str, description: str) -> None:
    execute_statement('UPDATE main.categories SET name=?, description=? WHERE id=?', name, description, _id)


def category_list() -> list:
    return execute_statement('SELECT id, name, description FROM categories ORDER BY id')


def category_read(_id: int) -> tuple:
    return execute_statement('SELECT id, name, description FROM main.categories WHERE id=?', _id)


def category_print_all() -> None:
    """Deprecated. TODO: remove"""
    res = execute_statement('SELECT * FROM main.categories ORDER BY id DESC')
    for row in res:
        print(row)


# TASK

def task_add(name: str, category_id: int) -> int:
    return execute_statement('INSERT INTO main.tasks (name, category_id) VALUES (?, ?)', name, category_id)


def task_remove_by_id(_id: int) -> None:
    execute_statement('DELETE FROM main.tasks WHERE id=?', _id)


def task_update(_id: int, name: str, category_id: int) -> None:
    execute_statement('UPDATE main.tasks SET name=?, category_id=? WHERE id=?', name, category_id, _id)


def task_print_all() -> None:
    res = execute_statement('SELECT * FROM main.tasks ORDER BY id DESC')
    for row in res:
        print(row)


def task_list() -> list:
    return execute_statement(
        'SELECT t.id, t.name, t.category_id, '
        'CASE WHEN w.id IS NULL THEN 0 ELSE 1 END is_current '
        'FROM main.tasks AS t '
        'LEFT JOIN main.work_items AS w '
        'ON (t.id = w.task_id AND w.end_timestamp is NULL)'
        'ORDER BY t.id'
    )


def task_read(_id: int) -> tuple:
    return execute_statement(
        'SELECT t.id, t.name, t.category_id, '
        'CASE WHEN w.id IS NULL THEN 0 ELSE 1 END is_current '
        'FROM main.tasks AS t '
        'LEFT JOIN main.work_items AS w '
        'ON (t.id = w.task_id AND w.end_timestamp is NULL)'
        'WHERE t.id=?',
        _id,
    )


# WORK

def work_read(_id: int) -> tuple:
    return execute_statement(
        'SELECT id, task_id, start_timestamp, end_timestamp FROM main.work_items WHERE id=?',
        _id,
    )


def work_start(task_id: int, start: int | None = None) -> int:
    # Validate active work
    res = list(execute_statement('SELECT id FROM main.work_items WHERE end_timestamp IS NULL'))
    if len(res) > 1:
        raise Exception('Cannot start work: already started')

    start = start or get_now_timestamp()
    return execute_statement('INSERT INTO main.work_items (task_id, start_timestamp) VALUES (?,?)', task_id, start)


def work_stop_current() -> None:
    res = execute_statement('SELECT * FROM main.work_items WHERE end_timestamp IS NULL ORDER BY start_timestamp DESC')
    res = list(res)[1:]

    if not res:
        print('No work for stop!')
        # TODO: add exception
    elif len(res) > 1:
        for row in res:
            print(row)
        raise Exception('More than one work items!')
    else:
        print(res)
        _id, task_id, start_ts, _ = res[0]
        end_ts = get_now_timestamp()
        execute_statement('UPDATE main.work_items SET end_timestamp = ? WHERE id = ?', end_ts, _id)
        print('Work spopped!')


def work_add(start_dt: datetime, end_dt: datetime, task_id: int) -> None:
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)
    execute_statement('INSERT INTO main.work_items (task_id, start_timestamp, end_timestamp) VALUES (?,?,?)', task_id, start_ts, end_ts)


def work_remove(_id: int):
    execute_statement('DELETE FROM main.work_items WHERE id = ?', _id)


def work_print_all():
    res = execute_statement('SELECT * FROM main.work_items ORDER BY end_timestamp DESC')
    for row in res:
        print(row)


def work_get_report_category(start_dt: datetime, end_dt: datetime) -> list:
    """
    TODO: rework calculation algorithm

    start_dt:__________:end_td
                  ^
           start_timestamp
    """
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)

    return execute_statement(
        'SELECT c.id AS category_id, c.name AS category_name, '
        'SUM(w.end_timestamp - w.start_timestamp) AS work_seconds '
        'FROM main.work_items w '
        'INNER JOIN main.tasks t '
        'ON (w.task_id = t.id) '
        'INNER JOIN main.categories c '
        'ON (t.category_id = c.id) '
        'WHERE w.start_timestamp >= ? AND w.start_timestamp <= ? '
        'GROUP BY c.id, c.name',
        start_ts, end_ts,
    )


def work_get_report_task(start_dt: datetime, end_dt: datetime) -> list:
    """
    TODO: rework calculation algorithm

    start_dt:__________:end_td
                  ^
           start_timestamp
    """
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)

    return execute_statement(
        'SELECT w.task_id AS task_id, t.name AS task_name, t.category_id AS category_id, '
        'SUM(w.end_timestamp - w.start_timestamp) AS work_seconds '
        'FROM main.work_items w '
        'INNER JOIN main.tasks t '
        'ON (w.task_id = t.id) '
        'WHERE w.start_timestamp >= ? AND w.start_timestamp <= ? '
        'GROUP BY w.task_id, t.name, t.category_id',
        start_ts, end_ts,
    )


def work_get_report_total(start_dt: datetime, end_dt: datetime) -> list:
    """
    TODO: rework calculation algorithm

    start_dt:__________:end_td
                  ^
           start_timestamp
    """
    start_ts = dt_to_ts(start_dt)
    end_ts = dt_to_ts(end_dt)

    return execute_statement(
        'SELECT SUM(w.end_timestamp - w.start_timestamp) AS work_seconds '
        'FROM main.work_items w '
        'WHERE w.start_timestamp >= ? AND w.start_timestamp <= ? ',
        start_ts, end_ts,
    )


# DATABASE UTILITY


def _execute_migration(name: str) -> None:
    root = Path(__file__).resolve().parent
    migrations = root / 'migrations'
    if not migrations.exists():
        raise FileNotFoundError('"migrations" folder does not exist')

    migration_files = list(migrations.glob(f'{name}_[a-z-]*.py'))
    if not migration_files:
        raise ValueError(f'Migration file with name "{name}" not found in: {migrations}')
    elif len(migration_files) > 1:
        raise ValueError(f'Multiple migration files for name "{name}": {migration_files}')

    migration_file = migration_files[0]

    logger.info(f'Apply migration "{name}" from file: {migration_file}')

    spec = importlib.util.spec_from_file_location(f'migration_{name}', str(migration_file))
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)


def migrate(name: str | None = None) -> None:
    logger.info('migrate')

    execute_statement('''
    CREATE TABLE IF NOT EXISTS main.categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT 
    )''')
    # Tasks TODO:
    #  - add title of task
    execute_statement('''
    CREATE TABLE IF NOT EXISTS main.tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category_id INTEGER,
    FOREIGN KEY (category_id) 
        REFERENCES categories(id) 
            ON DELETE CASCADE ON UPDATE NO ACTION
    )''')
    execute_statement('''
    CREATE TABLE IF NOT EXISTS main.work_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    -- comment TEXT,
    start_timestamp INTEGER NOT NULL,
    end_timestamp INTEGER DEFAULT NULL,
    FOREIGN KEY (task_id)
        REFERENCES tasks(id)
            ON DELETE CASCADE ON UPDATE NO ACTION
    )''')

    if name is not None:
        _execute_migration(name)
