import {NgModule} from "@angular/core";
import {WorkItemListComponent} from "./work-item-list/work-item-list.component";
import {MatTableModule} from "@angular/material/table";
import {WorkItemService} from "./services/work-item.service";
import {MatPaginatorModule} from "@angular/material/paginator";
import {AsyncPipe, DatePipe, NgIf} from "@angular/common";
import {RouterLink} from "@angular/router";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";

@NgModule({
  declarations: [
    WorkItemListComponent,
  ],
  imports: [
    MatTableModule,
    MatPaginatorModule,
    AsyncPipe,
    NgIf,
    RouterLink,
    MatButtonModule,
    MatIconModule,
    DatePipe
  ],
  providers: [WorkItemService]
})
export class WorkItemModule {}
