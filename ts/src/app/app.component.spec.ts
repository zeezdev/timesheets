import { TestBed, waitForAsync } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import {OverworkingWatcher} from "./work/services/overworking.service";
import {WorkService} from "./work/services/work.service";
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatIconModule} from "@angular/material/icon";
import {MatSidenavModule} from "@angular/material/sidenav";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {TodayCounterComponent} from "./main/today-counter/today-counter.component";
import {TaskService} from "./task/services/task.service";
import { NO_ERRORS_SCHEMA } from '@angular/core';
import {SettingsCache, SettingsService} from "./settings/services/settings.service";
import {of, Subject} from "rxjs";
import {Settings} from "./settings/services/settings";
import {MatMenuModule} from "@angular/material/menu";

describe('AppComponent', () => {
  let settingsCacheMock: any;
  let settingsServiceMock: any;
  let settingsSubject: Subject<Settings>;

  const mockSettings: Settings = {
    first_day_of_week: 1,
    first_day_of_month: 1
  };

  beforeEach(waitForAsync(() => {
    settingsSubject = new Subject<Settings>();
    settingsCacheMock = {
      settings$: settingsSubject.asObservable()
    };
    settingsServiceMock = {
      saveSettings: jasmine.createSpy('saveSettings').and.returnValue(of(mockSettings))
    };

    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
        MatToolbarModule,
        MatIconModule,
        MatSidenavModule,
        BrowserAnimationsModule,
        MatMenuModule,
      ],
      declarations: [
        AppComponent,
        TodayCounterComponent,
      ],
      providers: [
        OverworkingWatcher,
        WorkService,
        TaskService,
        { provide: SettingsCache, useValue: settingsCacheMock },
        { provide: SettingsService, useValue: settingsServiceMock },
      ],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();
  }));

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });
});
