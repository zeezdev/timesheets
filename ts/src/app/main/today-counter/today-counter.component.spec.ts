import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TodayCounterComponent } from './today-counter.component';
import {WorkService} from "../../work/services/work.service";
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {TaskService} from "../../task/services/task.service";

describe('TodayCounterComponent', () => {
  let component: TodayCounterComponent;
  let fixture: ComponentFixture<TodayCounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      declarations: [
        TodayCounterComponent,
      ],
      providers: [
        WorkService,
        TaskService,
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TodayCounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // TODO: test 'should display time if there is work'

  // TODO: test 'should display 00:00:00 if there is no work'
});
