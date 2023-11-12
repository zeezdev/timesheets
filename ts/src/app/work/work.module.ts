import {NgModule} from "@angular/core";
import {WorkComponent} from "./work.component";
import {MatInputModule} from "@angular/material/input";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {ReactiveFormsModule} from "@angular/forms";
import {MatTableModule} from "@angular/material/table";
import {WorkService} from "./services/work.service";
import {OverworkingWatcher} from "./services/overworking.service";

@NgModule({
  declarations: [
    WorkComponent,
  ],
  imports: [
    MatInputModule,
    MatDatepickerModule,
    ReactiveFormsModule,
    MatTableModule,
  ],
  providers: [WorkService, OverworkingWatcher]
})
export class WorkModule {}
