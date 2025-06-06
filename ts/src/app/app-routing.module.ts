import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {TaskListComponent} from "./task/task-list/task-list.component";
import {TaskFormComponent} from "./task/task-form/task-form.component";
import {CategoryListComponent} from "./category/category-list/category-list.component";
import {CategoryFormComponent} from "./category/category-form/category-form.component";
import {WorkComponent} from "./work/work.component";
import {WorkItemListComponent} from './work-item/work-item-list/work-item-list.component';
import {WorkItemFormComponent} from './work-item/work-item-form/work-item-form.component';
import {PageNotFoundComponent} from "./page-not-found/page-not-found/page-not-found.component";
import {MainPageComponent} from "./main/main-page/main-page.component";
import {SettingsComponent} from "./settings/settings.component";

const routes: Routes = [
  {path: '', component: MainPageComponent},
  {path: 'categories', component: CategoryListComponent},
  {path: 'categories/:id', component: CategoryFormComponent},
  {path: 'tasks', component: TaskListComponent},
  {path: 'tasks/:id', component: TaskFormComponent},
  {path: 'work', component: WorkComponent},
  {path: 'work-items', component: WorkItemListComponent},
  {path: 'work-items/:id', component: WorkItemFormComponent},
  {path: 'settings', component: SettingsComponent},
  {path: 'not-found', component: PageNotFoundComponent},
  {path: '**', redirectTo: '/not-found'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
