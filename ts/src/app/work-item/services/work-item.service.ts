import {Injectable} from "@angular/core";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {WorkItem} from "./work-item";
import {catchError} from "rxjs/operators";
import {handleError} from "../../shared/utils";
import {AppSettings} from "../../app.settings";
import {Page, PageRequest} from "../../shared/pagination";


export interface WorkItemQuery {
  search: string;
  // registration: Date;
}

@Injectable()
export class WorkItemService {
  workItemsUrl = `${AppSettings.API_URL}/work/items`;
  httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  }

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

    /**
   * TODO: move into WorkItemService
   * @param startDt
   * @param endDt
   * @param taskId
   */
  addWorkItem(startDt: string, endDt: string, taskId: number): Observable<Object> {
    const body = {
      start_dt: startDt,
      end_dt: endDt,
      task_id: taskId,
    };
    return this.http.post(this.workItemsUrl, body, this.httpOptions);
  }

  deleteWorkItem(id: number): Observable<Object> {
    return this.http.delete(
      `${this.workItemsUrl}/${id}`,
    ).pipe(
      tap(() => this.log(`Delete WorkItem ID=${id}`)),
      catchError(handleError('deleteWorkItem')),
    );
  }

  getWorkItem(id: number): Observable<WorkItem> {
    return this.http.get(
      `${this.workItemsUrl}/${id}`,
    ).pipe(
      tap((res) => this.log(`Fetch WorkItem: ${res}`)),
      catchError(handleError('getWorkItem')),
    ) as Observable<WorkItem>;
  }

  updateWorkItem(workItem: WorkItem): Observable<WorkItem> {
    return this.http.put<WorkItem>(`${this.workItemsUrl}/${workItem.id}`, workItem, this.httpOptions)
      .pipe(
        tap(upWorkItem => {this.log(`updated work item ${upWorkItem}`)}),
        catchError(handleError('Update work item')),
      ) as Observable<WorkItem>;
  }
}
