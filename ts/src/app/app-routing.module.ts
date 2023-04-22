import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CategoryComponent } from "./category/category.component";
import { TaskComponent } from "./task/task.component";
import { WorkComponent } from "./work/work.component";

const routes: Routes = [
  {path: 'categories', component: CategoryComponent},
  {path: 'tasks', component: TaskComponent},
  {path: 'work', component: WorkComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
