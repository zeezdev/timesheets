import {Component, OnInit} from '@angular/core';
import { Task } from '../services/task';
import {ActivatedRoute, ParamMap, Router} from "@angular/router";
import {TaskService} from "../services/task.service";
import {NotificationService} from "../../shared/notification.service";
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-task-form',
  templateUrl: './task-form.component.html',
  styleUrls: ['./task-form.component.css']
})
export class TaskFormComponent implements OnInit {
  task?: Task | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private service: TaskService,
    private notifications: NotificationService,
    private _snackBar: MatSnackBar,
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(
      (params: ParamMap) => {
        const taskId: string = params.get('id');
        if (taskId != 'add') {
          this.getTask(Number.parseInt(taskId));
        }
      }
    )
  }

  getTask(taskId: number) {
    this.service.getTask(taskId).subscribe(task => this.task = task);
  }

  onSubmit(form) {
    if (this.task !== null) {
      this.service.updateTask(this.task).subscribe(
        () => {
          console.info('Task updated.');
          this.notifications.success('Updated');
        }
      );
    } else {
      this.service.createTask({
        name: form.value.name, category_id: form.value.category_id
      }).subscribe(createdTask => {
        console.info('Task created');
        this.router.navigate(['/tasks', createdTask.id])
        this.notifications.success('Created');
      });
    }
  }
}
