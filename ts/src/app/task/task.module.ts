import {NgModule} from "@angular/core";
import {TaskListComponent} from "./task-list/task-list.component";
import {TaskFormComponent} from "./task-form/task-form.component";
import {MatTableModule} from "@angular/material/table";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatInputModule} from "@angular/material/input";
import {NgClass, NgForOf, NgIf} from "@angular/common";
import {TaskService} from "./services/task.service";
import {MatCardModule} from "@angular/material/card";
import {WorkService} from "../work/services/work.service";
import {MatSelectModule} from "@angular/material/select";
import {MatOptionModule} from "@angular/material/core";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {MatCheckboxModule} from "@angular/material/checkbox";

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
    MatSelectModule,
    MatOptionModule,
    NgForOf,
    NgIf,
    ReactiveFormsModule,
    MatProgressSpinnerModule,
    MatCheckboxModule,
  ],
  providers: [TaskService, WorkService],
})
export class TaskModule {}
