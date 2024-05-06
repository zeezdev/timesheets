import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkItemListComponent } from './work-item-list.component';

describe('WorkItemComponent', () => {
  let component: WorkItemListComponent;
  let fixture: ComponentFixture<WorkItemListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WorkItemListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WorkItemListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
