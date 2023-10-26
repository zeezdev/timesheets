import {NgModule} from "@angular/core";
import {TaskListComponent} from "./task-list/task-list.component";
import {TaskFormComponent} from "./task-form/task-form.component";
import {MatTableModule} from "@angular/material/table";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {FormsModule} from "@angular/forms";
import {MatInputModule} from "@angular/material/input";
import {NgClass} from "@angular/common";
import {TaskService} from "./services/task.service";
import {MatCardModule} from "@angular/material/card";
import {WorkService} from "../work/services/work.service";

@NgModule({
  declarations: [
    TaskListComponent,
    TaskFormComponent,
  ],
  imports: [
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    RouterLink,
    RouterLinkActive,
    FormsModule,
    MatInputModule,
    NgClass,
    MatCardModule,
  ],
  providers: [TaskService, WorkService],
})
export class TaskModule {}
