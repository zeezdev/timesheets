import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TodayCounterComponent } from './today-counter.component';

describe('TodayCounterComponent', () => {
  let component: TodayCounterComponent;
  let fixture: ComponentFixture<TodayCounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TodayCounterComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TodayCounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
