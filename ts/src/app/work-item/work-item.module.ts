import {NgModule} from "@angular/core";
import {WorkItemListComponent} from "./work-item-list/work-item-list.component";
import {MatTableModule} from "@angular/material/table";
import {WorkItemService} from "./services/work-item.service";
import {MatPaginatorModule} from "@angular/material/paginator";
import {AsyncPipe, NgIf} from "@angular/common";

@NgModule({
  declarations: [
    WorkItemListComponent,
  ],
  imports: [
    MatTableModule,
    MatPaginatorModule,
    AsyncPipe,
    NgIf
  ],
  providers: [WorkItemService]
})
export class WorkItemModule {}
