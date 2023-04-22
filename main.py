#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime

from database import migrate, category_add, task_add, category_print_all, category_remove_by_id, \
    work_start, work_stop_current, work_add, task_print_all, work_print_all, work_get_report_category, \
    category_update, task_remove_by_id, task_update, work_remove

HOURS_IN_WORKING_DAY = 8


def _work_print_report_category(start_dt: datetime, end_dt: datetime) -> None:
    res = work_get_report_category(start_dt, end_dt)

    for i, row in enumerate(res):
        category_id, category_name, time_days = row
        if i > 0:
            time_days = time_days / 60 / 60 / HOURS_IN_WORKING_DAY
            # time_days = round(time_days, 2)

        print(f'{category_id}, {category_name}, {time_days}')


def _category(category):
    action, *cmd_args = category
    if action == 'add':
        name, description = cmd_args
        category_add(name, description)
    elif action == 'remove':
        _id = cmd_args[0]
        category_remove_by_id(_id)
    elif action == 'update':
        _id, new_name, new_description = cmd_args
        category_update(_id, new_name, new_description)
    elif action == 'show':
        category_print_all()
    else:
        raise Exception(f'Unknown action for category command: {action}')


def _task(task):
    action, *cmd_args = task
    if action == 'add':
        name, category_id = cmd_args
        task_add(name, category_id)
    elif action == 'remove':
        _id = cmd_args[0]
        task_remove_by_id(_id)
    elif action == 'update':
        _id, new_id, new_category_id = cmd_args
        task_update(_id, new_id, new_category_id)
    elif action == 'show':
        task_print_all()
    else:
        raise Exception(f'Unknown action for task command: {action}')


def _work(work):
    action, *cmd_args = work
    if action == 'start':
        task_id = cmd_args[0]
        work_start(task_id)
    elif action == 'stop':
        work_stop_current()
    elif action == 'add':
        start, end, task_id = cmd_args
        start_dt = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        end_dt = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        work_add(start_dt, end_dt, int(task_id))
    elif action == 'remove':
        _id = cmd_args[0]
        work_remove(int(_id))
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
    print(args)

    if args.category:
        if any([args.task, args.work]):
            raise Exception('--category is not compatible with --task and/or --work')

        _category(args.category)
    elif args.task:
        _task(args.task)
    elif args.work:
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

    args = parser.parse_args()

    # con = sqlite3.connect('timesheet.db')
    migrate()
    work(args)


if __name__ == '__main__':
    # app = TimeSheetApp()
    # app.run()
    main()
