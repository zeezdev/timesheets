import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkItemFormComponent } from './work-item-form.component';

describe('WorkItemFormComponent', () => {
  let component: WorkItemFormComponent;
  let fixture: ComponentFixture<WorkItemFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WorkItemFormComponent ]
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
