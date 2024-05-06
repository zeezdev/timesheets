import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {WorkItem} from "./work-item";
import {catchError} from "rxjs/operators";
import {handleError} from "../../shared/utils";
import {AppSettings} from "../../app.settings";
import {Page, PageRequest} from "./page";


export interface WorkItemQuery {
  search: string;
  // registration: Date;
}

@Injectable()
export class WorkItemService {
  workItemsUrl = `${AppSettings.API_URL}/work/items`;
  constructor(
    private http: HttpClient,
  ) { }

  // getWorkItems(): Observable<PaginatedResponse<WorkItem>> {
  //   return this.http.get<PaginatedResponse<WorkItem>>(`${this.workItemsUrl}?order_by=-start_dt`)
  //     .pipe(
  //       tap(workItems => this.log(`fetched work items ${workItems}`)),
  //       catchError(handleError('getWorkItems'))
  //     ) as Observable<PaginatedResponse<WorkItem>>;
  // }

  private log(message: string) {
    console.log(`WorkItemService: ${message}`);
  }

  page(request: PageRequest<WorkItem>, query: WorkItemQuery): Observable<Page<WorkItem>> {
    return this.http.get<Page<WorkItem>>(
      `${this.workItemsUrl}?page=${request.page}&size=${request.size}&order_by=-id`
    ).pipe(
        tap(page => this.log(`fetched work items page ${page}`)),
        catchError(handleError('page')),
      ) as Observable<Page<WorkItem>>;
  }
}
