import {NgModule} from "@angular/core";
import {WorkItemListComponent} from "./work-item-list/work-item-list.component";
import {MatTableModule} from "@angular/material/table";
import {WorkItemService} from "./services/work-item.service";
import {MatPaginatorModule} from "@angular/material/paginator";
import {AsyncPipe, DatePipe, NgClass, NgForOf, NgIf} from "@angular/common";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import { WorkItemFormComponent } from './work-item-form/work-item-form.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatCardModule} from "@angular/material/card";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {MatOptionModule} from "@angular/material/core";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {MatSelectModule} from "@angular/material/select";
import {NgxMatDatetimePickerModule, NgxMatNativeDateModule} from "@angular-material-components/datetime-picker";
import {MatDatepickerModule} from "@angular/material/datepicker";

@NgModule({
  declarations: [
    WorkItemListComponent,
    WorkItemFormComponent,
  ],
    imports: [
        MatTableModule,
        MatPaginatorModule,
        AsyncPipe,
        NgIf,
        RouterLink,
        MatButtonModule,
        MatIconModule,
        DatePipe,
        FormsModule,
        MatCardModule,
        MatCheckboxModule,
        MatFormFieldModule,
        MatInputModule,
        MatOptionModule,
        MatProgressSpinnerModule,
        MatSelectModule,
        NgForOf,
        ReactiveFormsModule,
        NgClass,
        NgxMatDatetimePickerModule,
        MatDatepickerModule,
        NgxMatNativeDateModule,
        RouterLinkActive,
    ],
  providers: [WorkItemService]
})
export class WorkItemModule {}
