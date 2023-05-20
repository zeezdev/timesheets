import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TaskListComponent } from "./task/task-list/task-list.component";
import {TaskFormComponent} from "./task/task-form/task-form.component";
import {CategoryListComponent} from "./category/category-list/category-list.component";
import {CategoryFormComponent} from "./category/category-form/category-form.component";
import { WorkComponent } from "./work/work.component";

const routes: Routes = [
  {path: 'categories', component: CategoryListComponent},
  {path: 'categories/:id', component: CategoryFormComponent},
  {path: 'tasks', component: TaskListComponent},
  {path: 'tasks/:id', component: TaskFormComponent},
  {path: 'work', component: WorkComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
