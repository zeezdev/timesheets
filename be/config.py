import os


def get_database_name() -> str:
    name = os.getenv('TIMESHEET_DB_FILENAME', '../db/timesheet.db')
    return f'sqlite:///{name}'
