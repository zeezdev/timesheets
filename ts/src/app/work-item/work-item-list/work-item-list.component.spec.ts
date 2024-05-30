import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkItemListComponent } from './work-item-list.component';
import {WorkItemService} from "../services/work-item.service";
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {MatTableModule} from "@angular/material/table";

describe('WorkItemComponent', () => {
  let component: WorkItemListComponent;
  let fixture: ComponentFixture<WorkItemListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        MatTableModule,
      ],
      declarations: [WorkItemListComponent],
      providers: [WorkItemService],
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
