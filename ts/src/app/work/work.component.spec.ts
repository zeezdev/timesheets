import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkComponent } from './work.component';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {WorkService} from "./services/work.service";
import {RouterTestingModule} from "@angular/router/testing";
import {ReactiveFormsModule} from "@angular/forms";
import {MatInputModule} from "@angular/material/input";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {MatTableModule} from "@angular/material/table";

describe('WorkComponent', () => {
  let component: WorkComponent;
  let fixture: ComponentFixture<WorkComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
        MatInputModule,
        MatDatepickerModule,
        ReactiveFormsModule,
        MatTableModule,
        BrowserAnimationsModule,
      ],
      declarations: [WorkComponent],
      providers: [WorkService]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WorkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
