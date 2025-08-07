import { waitForAsync, ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkComponent } from './work.component';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {WorkService} from "./services/work.service";
import {RouterTestingModule} from "@angular/router/testing";
import {ReactiveFormsModule} from "@angular/forms";
import {MatInputModule} from "@angular/material/input";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {MatTableModule} from "@angular/material/table";
import { SettingsCache, SettingsService } from "../settings/services/settings.service";
import { NO_ERRORS_SCHEMA } from '@angular/core';

describe('WorkComponent', () => {
  let component: WorkComponent;
  let fixture: ComponentFixture<WorkComponent>;

  const mockSettings = { first_day_of_month: 1 };
  const settingsCacheMock = {
    settings: mockSettings
  };
  const settingsServiceMock = {};

  beforeEach(waitForAsync(() => {
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
      providers: [
        WorkService,
        { provide: SettingsCache, useValue: settingsCacheMock },
        { provide: SettingsService, useValue: settingsServiceMock }
      ],
      schemas: [NO_ERRORS_SCHEMA]
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
