import {Component, OnInit} from '@angular/core';
import {Task} from '../services/task';
import {ActivatedRoute, ParamMap, Router} from '@angular/router';
import {TaskService} from '../services/task.service';
import {NotificationService} from '../../shared/notification.service';
import {CategoryService} from "../../category/services/category.service";
import {Category} from "../../category/services/category";

@Component({
  selector: 'app-task-form',
  templateUrl: './task-form.component.html',
  styleUrls: ['./task-form.component.css'],
})
export class TaskFormComponent implements OnInit {
  task?: Task | null = null;
  categories: Category[] = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private service: TaskService,
    private categoryService: CategoryService,
    private notifications: NotificationService,
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
    this.service.getTask(taskId).subscribe(
      task => {
        this.categories = [{id: task.category.id, name: task.category.name}];
        this.task = task;
      }
    );
  }

  getCategories() {
    this.categoryService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories
      },
      error: () => {
        this.categories = null;
      },
    });
  }

  onSubmit(form) {
    if (this.task !== null) {
      // FIXME: this.task contains extra fields i.e. {is_current, category_name}
      this.service.updateTask(this.task).subscribe(
        () => {
          console.info('Task updated.');
          this.notifications.success('Updated');
        }
      );
    } else {
      const category = this.categories.find(c => {
        return c.id === form.value.category_id;
      });
      this.service.createTask({
        name: form.value.name,
        category: category,
      }).subscribe(createdTask => {
        console.info('Task created');
        this.router.navigate(['/tasks', createdTask.id])
        this.notifications.success('Created');
      });
    }
  }
}
