import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkItemFormComponent } from './work-item-form.component';
import {ActivatedRoute, RouterLink} from "@angular/router";
import {of} from "rxjs";
import {WorkItemService} from "../services/work-item.service";
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {TaskService} from "../../task/services/task.service";
import {MatSnackBarModule} from "@angular/material/snack-bar";
import {MatDialogModule} from "@angular/material/dialog";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatCardModule} from "@angular/material/card";
import {MatInputModule} from "@angular/material/input";
import {MatTableModule} from "@angular/material/table";
import {MatPaginatorModule} from "@angular/material/paginator";
import {AsyncPipe, DatePipe, NgClass, NgForOf, NgIf} from "@angular/common";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatOptionModule} from "@angular/material/core";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {MatSelectModule} from "@angular/material/select";
import {NgxMatDatetimePickerModule, NgxMatNativeDateModule} from "@angular-material-components/datetime-picker";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

describe('WorkItemFormComponent', () => {
  let component: WorkItemFormComponent;
  let fixture: ComponentFixture<WorkItemFormComponent>;
  let mockRoute = null;

  beforeEach(async () => {
    mockRoute = jasmine.createSpyObj('', {}, {
      'paramMap': of( new Map([['id', '1']]))
    });
    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        MatSnackBarModule,
        MatDialogModule,
        FormsModule,
        BrowserAnimationsModule,
        // from work-item.module.ts
        MatTableModule,
        MatPaginatorModule,
        AsyncPipe,
        NgIf,
        RouterLink,
        MatButtonModule,
        MatIconModule,
        DatePipe,
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
      ],
      declarations: [WorkItemFormComponent],
      providers: [
        WorkItemService,
        TaskService,
        {provide: ActivatedRoute, useValue: mockRoute},
      ],
    })
    .compileComponents();

    fixture = TestBed.createComponent(WorkItemFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
