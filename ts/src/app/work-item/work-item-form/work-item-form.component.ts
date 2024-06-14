import { Component } from '@angular/core';
import {WorkItem} from "../services/work-item";
import {ActivatedRoute, ParamMap, Router} from "@angular/router";
import {WorkItemService} from "../services/work-item.service";
import {NotificationService} from "../../shared/notification.service";
import { Task } from 'src/app/task/services/task';
import {TaskService} from "../../task/services/task.service";

import { NgxMatMomentAdapter, NGX_MAT_MOMENT_DATE_ADAPTER_OPTIONS } from '@angular-material-components/moment-adapter';
import { NGX_MAT_DATE_FORMATS, NgxMatDateAdapter } from '@angular-material-components/datetime-picker';


export const CUSTOM_MOMENT_FORMATS  = {
  parse: {
    dateInput: 'YYYY/MM/DD',
  },
  display: {
    dateInput: 'YYYY/MM/DD HH:mm:ss',
    monthYearLabel: "MMM YYYY",
    dateA11yLabel: "LL",
    monthYearA11yLabel: "MMMM YYYY"
  }
};


@Component({
  selector: 'app-work-item-form',
  templateUrl: './work-item-form.component.html',
  styleUrls: ['./work-item-form.component.css'],
  providers: [
    { provide: NGX_MAT_MOMENT_DATE_ADAPTER_OPTIONS, useValue: { useUtc: true } },
    { provide: NGX_MAT_DATE_FORMATS, useValue: CUSTOM_MOMENT_FORMATS },
    { provide: NgxMatDateAdapter, useClass: NgxMatMomentAdapter },
  ]
})
export class WorkItemFormComponent {
  workItem?: WorkItem | null = null;
  tasks: Task[] = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private workItemService: WorkItemService,
    private taskService: TaskService,
    private notifications: NotificationService,
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(
      (params: ParamMap) => {
        const workItemId: string = params.get('id');
        if (workItemId != 'add') {
          this.getWorkItem(Number.parseInt(workItemId));
        }
      }
    );
  }

  getWorkItem(workItemId: number): void {
    this.workItemService.getWorkItem(workItemId).subscribe(
      workItem => {
        this.tasks = [{id: workItem.task.id, name: workItem.task.name}];
        this.workItem = workItem;
      }
    );
  }

  onSubmit(form) {
    if (this.workItem !== null) {
      this.workItemService.updateWorkItem(this.workItem).subscribe(
        () => {
          console.info('Work items updated.');
          this.notifications.success('Updated');
        }
      );
    } else {
      // TODO: implement WorkItem creation
    }
  }

  getTasks() {
    this.taskService.getTasks().subscribe({
      next: (tasks) => {
        this.tasks = tasks;
      },
      error: () => {
        this.tasks = null;
      },
    });
  }
}
