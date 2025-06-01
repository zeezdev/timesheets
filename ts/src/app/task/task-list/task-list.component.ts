import { Component, OnInit } from '@angular/core';
import {Task} from '../services/task';
import {TaskService} from '../services/task.service';
import {WorkService} from '../../work/services/work.service';
import {NotificationService} from "../../shared/notification.service";
import {TodayCounterSharedService} from "../../main/today-counter/services/today-counter-shared.service";

@Component({
  selector: 'app-task',
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css']
})
export class TaskListComponent implements OnInit {
  tasks: Task[] = [];
  displayedColumns: string[] = ['id', 'name', 'category_name', 'actions'];
  hasActiveTask: boolean = false;
  showArchived: boolean = false;

  constructor(
    private taskService: TaskService,
    private workService: WorkService,
    private notifications: NotificationService,
    private todayCounterService: TodayCounterSharedService,
  ) { }

  ngOnInit() {
    this.getTasks();
  }

  getTasks() {
    const isArchived = this.showArchived ? undefined : false;
    this.taskService.getTasks(isArchived).subscribe(
      tasks => {
        this.hasActiveTask = false;
        for (const task of tasks) {
          if (task.is_current) {
            this.hasActiveTask = true;
            break;
          }
        }
        this.tasks = tasks;
      });
  }

  startWork(id) {
    console.log(`Start work for ${id}`);
    this.workService.startWork(id).subscribe({
      next: () => {
        this.getTasks();
        this.todayCounterService.todayCounterStart();
      },
      error: err => {
        this.notifications.error(`Error: (${err.status}) ${err.error}.`)
      },
    });
  }

  stopWork() {
    this.workService.stopWorkCurrent().subscribe({
      next: () => {
        this.getTasks();
        this.todayCounterService.todayCounterStop();
      },
      error: err => {
        this.notifications.error(`Error: (${err.status}) ${err.error}.`)
      },
    });
  }
}
