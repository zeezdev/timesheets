import {Injectable} from "@angular/core";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {WorkItem} from "./work-item";
import {catchError} from "rxjs/operators";
import {handleError} from "../../shared/utils";
import {AppSettings} from "../../app.settings";
import {Page, PageRequest} from "../../shared/pagination";
import {Router} from "@angular/router";


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
    private router: Router,
  ) { }

  private log(message: string) {
    console.log(`WorkItemService: ${message}`);
  }

  page(request: PageRequest<WorkItem>, query: WorkItemQuery): Observable<Page<WorkItem>> {
    const orderBy: string = `${request.sort.order == 'desc' ? '-' : ''}${request.sort.property}`;
    return this.http.get<Page<WorkItem>>(
      `${this.workItemsUrl}?page=${request.page}&size=${request.size}&order_by=${orderBy}`
    ).pipe(
        tap(page => this.log(`fetched work items page ${page}`)),
        catchError(handleError('page')),
      ) as Observable<Page<WorkItem>>;
  }

  addWorkItem(startDt: string, endDt: string, taskId: number): Observable<WorkItem> {
    const body = {
      start_dt: startDt,
      end_dt: endDt,
      task_id: taskId,
    };
    return this.http.post(
      this.workItemsUrl, body, this.httpOptions,
    ).pipe(
      tap(newWorkItem => {this.log(`created work item ${newWorkItem}`)}),
      catchError(handleError('Add work item')),
    ) as Observable<WorkItem>;
  }

  deleteWorkItem(id: number): Observable<Object> {
    return this.http.delete(
      `${this.workItemsUrl}/${id}`,
    ).pipe(
      tap(() => this.log(`Delete WorkItem ID=${id}`)),
      catchError(handleError('deleteWorkItem', this.router)),
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
