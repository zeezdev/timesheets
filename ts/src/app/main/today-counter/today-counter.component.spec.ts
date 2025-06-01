import {ComponentFixture, fakeAsync, TestBed, tick} from '@angular/core/testing';

import { TodayCounterComponent } from './today-counter.component';
import {WorkService} from "../../work/services/work.service";
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {TaskService} from "../../task/services/task.service";
import {Task} from "../../task/services/task";
import {WorkReportTotal} from "../../work/services/work";
import {of, Subject, Subscription} from "rxjs";
import {TodayCounterSharedService} from "./services/today-counter-shared.service";

describe('TodayCounterComponent', () => {
  let component: TodayCounterComponent;
  let fixture: ComponentFixture<TodayCounterComponent>;
  let workService: jasmine.SpyObj<WorkService>;
  let taskService: jasmine.SpyObj<TaskService>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      declarations: [
        TodayCounterComponent,
      ],
      providers: [
        {
          provide: WorkService,
          useValue: jasmine.createSpyObj('WorkService', ['getWorkReportTotal'])
        },
        {
          provide: TaskService,
          useValue: jasmine.createSpyObj('TaskService', ['getTasks'])
        },
        {
          provide: TodayCounterSharedService,
          useValue: {
            startCall$: new Subject<void>(),
            stopCall$: new Subject<void>()
          }
        }
      ],
    })
    .compileComponents();

    fixture = TestBed.createComponent(TodayCounterComponent);
    component = fixture.componentInstance;

    workService = TestBed.inject(WorkService) as jasmine.SpyObj<WorkService>;
    taskService = TestBed.inject(TaskService) as jasmine.SpyObj<TaskService>;
    workService.getWorkReportTotal.and.returnValue(of({ time: 0 } as WorkReportTotal));
    taskService.getTasks.and.returnValue(of([]));
  });

  it('should create', () => {
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  it('should display time if there is work', () => {
    component.counterSeconds = 3661;
    expect(component.displayValue).toBe('01:01:01');
  });

  it('should display 00:00:00 if there is no work', () => {
    component.counterSeconds = null;
    expect(component.displayValue).toBe('00:00:00');
    component.counterSeconds = 0;
    expect(component.displayValue).toBe('00:00:00');
  });

  it('should start counter and increment counterSeconds every second', fakeAsync(() => {
    component.counterSeconds = 0;
    component.startCounter();
    tick(3000);
    expect(component.counterSeconds).toBe(3);
    component.stopCounter(); // cleanup
  }));

  it('should stop counter when stopCounter is called', fakeAsync(() => {
    component.counterSeconds = 0;
    component.startCounter();
    tick(2000);
    component.stopCounter();
    const secondsAtStop = component.counterSeconds;
    tick(3000);
    expect(component.counterSeconds).toBe(secondsAtStop);
  }));

  it('should init counter with work time and start counter if tasks are active', fakeAsync(() => {
    const mockReport = { time: 120 } as WorkReportTotal;
    workService.getWorkReportTotal.and.returnValue(of(mockReport));
    const mockTasks = [{ id: 1, name: 'Test Task' }] as Task[];
    taskService.getTasks.and.returnValue(of(mockTasks));

    spyOn(component, 'startCounter').and.callThrough();

    component.initCounter();

    tick(); // for getWorkReportTotal
    tick(); // for getTasks

    expect(component.counterSeconds).toBe(120);
    expect(component.startCounter).toHaveBeenCalled();
    expect(component.counterIntervalSubscription).not.toBeNull();

    component.stopCounter();
  }));

  it('should unsubscribe from interval when stopCounter is called', () => {
    const mockSubscription = jasmine.createSpyObj<Subscription>('Subscription', ['unsubscribe']);
    component.counterIntervalSubscription = mockSubscription;
    component.stopCounter();
    expect(mockSubscription.unsubscribe).toHaveBeenCalled();
  });
});
