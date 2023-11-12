import { Component, OnInit } from '@angular/core';
import {Task} from '../services/task';
import {TaskService} from '../services/task.service';
import {WorkService} from '../../work/services/work.service';

@Component({
  selector: 'app-task',
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css']
})
export class TaskListComponent implements OnInit {
  tasks: Task[] = [];
  displayedColumns: string[] = ['id', 'name', 'category_id', 'actions'];
  hasActiveTask: boolean = false;

  constructor(private taskService: TaskService, private workService: WorkService) { }

  ngOnInit() {
    this.getTasks();
  }

  getTasks() {
    this.taskService.getTasks().subscribe(
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
    this.workService.startWork(id).subscribe(() => this.getTasks());
  }

  stopWork() {
    this.workService.stopWorkCurrent().subscribe(() => this.getTasks());
  }
}
