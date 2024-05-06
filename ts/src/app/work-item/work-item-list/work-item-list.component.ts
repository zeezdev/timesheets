import {ChangeDetectionStrategy, Component, OnInit} from '@angular/core';
import {WorkItemQuery, WorkItemService} from "../services/work-item.service";
import {WorkItem} from "../services/work-item";
import {Sort} from "../services/page";
import {PaginatedDataSource} from "../services/paginated-datasource";

@Component({
  selector: 'app-work-item',
  templateUrl: './work-item-list.component.html',
  styleUrls: ['./work-item-list.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class WorkItemListComponent implements OnInit {
  workItems: WorkItem[] = [];
  displayedColumns: string[] = ['id', 'task_id', 'start_dt', 'end_dt'];

  initialSort: Sort<WorkItem> = {property: 'id', order: 'desc'}

  data = new PaginatedDataSource<WorkItem, WorkItemQuery>(
    (request, query) => this.workItemService.page(request, query),
    this.initialSort,
    {search: ''},
    10,
  )

  constructor(private workItemService: WorkItemService) {}

  ngOnInit() {
    // this.getWorkItems();
  }

  // getWorkItems() {
  //   this.workItemService.getWorkItems().subscribe(workItemsPage => {
  //     this.workItems = workItemsPage.items;
  //   });
  // }
}

