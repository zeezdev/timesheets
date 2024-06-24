import {ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {WorkItemQuery, WorkItemService} from "../services/work-item.service";
import {WorkItem} from "../services/work-item";
import {Sort} from "../../shared/pagination";
import {PaginatedDataSource} from "../../shared/pagination";

const DEFAULT_PAGE_SIZE: number = 10;

@Component({
  selector: 'app-work-item',
  templateUrl: './work-item-list.component.html',
  styleUrls: ['./work-item-list.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class WorkItemListComponent {
  displayedColumns: string[] = ['id', 'task', 'start_dt', 'end_dt', 'actions'];
  initialSort: Sort<WorkItem> = {property: 'id', order: 'desc'}
  currentPageIndex: number = 1;

  data = new PaginatedDataSource<WorkItem, WorkItemQuery>(
    (request, query) => this.workItemService.page(request, query),
    this.initialSort,
    {search: ''},
    DEFAULT_PAGE_SIZE,
  )

  constructor(
    private workItemService: WorkItemService,
  ) {}

  doFetch(pageIndex: number) {
    this.currentPageIndex = pageIndex;
    this.data.fetch(this.currentPageIndex);
  }

  doDeleteWorkItem(element: WorkItem) {
    if (confirm(`Are you sure to delete the work item with ID=${element.id}`)) {
      console.log(`Delete work item ID=${element.id}`);
      this.workItemService.deleteWorkItem(element.id).subscribe(
        (res) => {
          this.doFetch(this.currentPageIndex);
        },
      );
    }
  }
}
