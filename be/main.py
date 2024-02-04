#!/usr/bin/env python3
import logging
from argparse import ArgumentParser
from datetime import datetime

import services
from database import get_db, init_db

HOURS_IN_WORKING_DAY = 8


def category_print_all() -> None:
    """Deprecated. TODO: remove"""
    rows = services.category_list(get_db())
    for row in rows:
        print(row)


def task_print_all() -> None:
    rows = services.task_list(get_db())
    for row in rows:
        print(row)


def work_print_all():
    rows = services.work_item_list(get_db())
    for row in rows:
        print(row)


def _work_print_report_category(start_dt: datetime, end_dt: datetime) -> None:
    res = services.work_get_report_category(get_db(), start_dt, end_dt)

    for i, row in enumerate(res):
        category_id, category_name, time_days = row
        if i > 0:
            time_days = time_days / 60 / 60 / HOURS_IN_WORKING_DAY
            # time_days = round(time_days, 2)

        print(f'{category_id}, {category_name}, {time_days}')


def _init_db(mgrt):
    init_db()


def _category(category):
    action, *cmd_args = category
    if action == 'add':
        name, description = cmd_args
        services.category_create(get_db(), name, description)
    elif action == 'remove':
        _id = cmd_args[0]
        services.category_delete(get_db(), _id)
    elif action == 'update':
        _id, new_name, new_description = cmd_args
        services.category_update(get_db(), _id, new_name, new_description)
    elif action == 'show':
        category_print_all()
    else:
        raise Exception(f'Unknown action for category command: {action}')


def _task(task):
    action, *cmd_args = task
    if action == 'add':
        name, category_id = cmd_args
        services.task_create(get_db(), name, category_id)
    elif action == 'remove':
        _id = cmd_args[0]
        services.task_delete(get_db(), _id)
    elif action == 'update':
        _id, new_id, new_category_id = cmd_args
        services.task_update(get_db(), _id, new_id, new_category_id)
    elif action == 'show':
        task_print_all()
    else:
        raise Exception(f'Unknown action for task command: {action}')


def _work(work):
    action, *cmd_args = work
    if action == 'start':
        task_id = cmd_args[0]
        services.work_item_start(get_db(), task_id, None)
    elif action == 'stop':
        services.work_item_stop_current(get_db())
    elif action == 'add':
        start, end, task_id = cmd_args
        start_dt = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        end_dt = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        services.work_item_create(get_db(), start_dt, end_dt, int(task_id))
    elif action == 'remove':
        id_ = cmd_args[0]
        services.work_item_delete(get_db(), int(id_))
    elif action == 'show':
        work_print_all()
    elif action == 'report':
        if len(cmd_args) < 3:
            print(f'Not enough arguments: {cmd_args}')
        start, end, report_type, *cmd_args = cmd_args
        start_dt = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        end_dt = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        if report_type == 'category':
            _work_print_report_category(start_dt, end_dt)
        else:
            raise Exception(f'Unknown report type for work command and action report: {report_type}')
    else:
        raise Exception(f'Unknown action for work command: {action}')


def work(args):
    logging.info(args)

    if args.init is not None:
        _init_db(args.init)
    elif args.category is not None:
        if any([args.task is not None, args.work is not None]):
            raise Exception('--category is not compatible with --task and/or --work')

        _category(args.category)
    elif args.task is not None:
        _task(args.task)
    elif args.work is not None:
        _work(args.work)


def main():
    parser = ArgumentParser()
    category_help = """
    (add):
        <name> <description>
    (remove):
        <id>
    (update):
        <id> <new_name> <new_description>
    (show):
        no args
    """
    parser.add_argument('-c', '--category', nargs='+', help=category_help)

    task_help = """
    (add):
        <name> <category_id>
    (remove):
        <id>
    (update):
        <id> <new_name> <new_category_id>
    (show):
        no args
    """
    parser.add_argument('-t', '--task', nargs='+', help=task_help)
    work_help = """
    (start):
        <task_id>
    (stop):
        no args
    (add):
        <start:yyyy-mm-ddThh:mm:ss> <end:yyyy-mm-ddThh:mm:ss> <task_id>
    (remove):
        <id>
    (report):
        <start:yyyy-mm-ddThh:mm:ss> <end:yyyy-mm-ddThh:mm:ss> <report_type:category|?>
    """
    parser.add_argument('-w', '--work', nargs='+', help=work_help)

    init_help = """Initialize the DB schema"""
    parser.add_argument('-i', '--init', nargs='*', help=init_help)

    args = parser.parse_args()

    work(args)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # TODO: Consider to use `click` for CLI
    #   https://click.palletsprojects.com/en/8.1.x/
    main()
