import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {TaskListComponent} from "./task/task-list/task-list.component";
import {TaskFormComponent} from "./task/task-form/task-form.component";
import {CategoryListComponent} from "./category/category-list/category-list.component";
import {CategoryFormComponent} from "./category/category-form/category-form.component";
import {WorkComponent} from "./work/work.component";
import {WorkItemListComponent} from './work-item/work-item-list/work-item-list.component';
import {WorkItemFormComponent} from './work-item/work-item-form/work-item-form.component';

const routes: Routes = [
  {path: 'categories', component: CategoryListComponent},
  {path: 'categories/:id', component: CategoryFormComponent},
  {path: 'tasks', component: TaskListComponent},
  {path: 'tasks/:id', component: TaskFormComponent},
  {path: 'work', component: WorkComponent},
  {path: 'work-items', component: WorkItemListComponent},
  {path: 'work-items/:id', component: WorkItemFormComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
