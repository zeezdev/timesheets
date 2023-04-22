import { Component, OnInit } from '@angular/core';
import {Task} from './task';
import {TaskService} from './task.service';
import {WorkService} from '../work/work.service';

@Component({
  selector: 'app-task',
  templateUrl: './task.component.html',
  providers: [TaskService, WorkService],
  styleUrls: ['./task.component.css']
})
export class TaskComponent implements OnInit {
  tasks: Task[] = [];
  displayedColumns: string[] = ['id', 'name', 'category_id', 'actions'];

  constructor(private taskService: TaskService, private workService: WorkService) { }

  ngOnInit() {
    this.getTasks();
  }

  getTasks() {
    this.taskService.getTasks().subscribe(tasks => (this.tasks = tasks));
  }

  startWork(id) {
    console.log(`Start work for ${id}`);
    this.workService.startWork(id);
  }

  stopWork() {
    this.workService.stopWorkCurrent();
  }
}
