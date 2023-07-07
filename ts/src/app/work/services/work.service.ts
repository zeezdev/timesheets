import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
// import {catchError} from "rxjs/operators";
import {WorkReportByCategory, WorkReportByTask, WorkReportTotal} from './work';
import {Injectable} from '@angular/core';


@Injectable({providedIn: 'root'})
export class WorkService {
  workUrl = 'http://localhost:8874/api/work';
  // private handleError: HandleError;

  constructor(
    private http: HttpClient,
    // httpErrorHandler: HttpErrorHandler
  ) {
    // this.handleError = httpErrorHandler.createHandleError('HeroesService');
  }

  /** GET work report grouped by categories from the server */
  getWorkReportByCategory(start: Date, end: Date): Observable<WorkReportByCategory[]> {
    // TODO: maybe convert to UTC?
    const startMonth = String(start.getMonth() + 1).padStart(2, '0');
    const endMonth = String(end.getMonth() + 1).padStart(2, '0');
    const startDateTime = `${start.getFullYear()}-${startMonth}-${start.getDate()}T00:00:00`;
    const endDateTime = `${end.getFullYear()}-${endMonth}-${end.getDate()}T23:59:59`;
    const url = `${this.workUrl}/report_by_category?start_datetime=${startDateTime}&end_datetime=${endDateTime}`;

    return this.http.get<WorkReportByCategory[]>(url)
      .pipe(
        // catchError(this.handleError('getHeroes', []))
      );
  }

  /** GET work report grouped by categories from the server */
  getWorkReportByTask(start: Date, end: Date): Observable<WorkReportByTask[]> {
    // TODO: maybe convert to UTC?
    const startMonth = String(start.getMonth() + 1).padStart(2, '0');
    const endMonth = String(end.getMonth() + 1).padStart(2, '0');
    const startDateTime = `${start.getFullYear()}-${startMonth}-${start.getDate()}T00:00:00`;
    const endDateTime = `${end.getFullYear()}-${endMonth}-${end.getDate()}T23:59:59`;
    const url = `${this.workUrl}/report_by_task?start_datetime=${startDateTime}&end_datetime=${endDateTime}`;

    return this.http.get<WorkReportByTask[]>(url)
      .pipe(
        // catchError(this.handleError('getHeroes', []))
      );
  }

  getWorkReportTotal(start: Date, end: Date): Observable<WorkReportTotal> {
    // TODO: maybe convert to UTC?
    const startMonth = String(start.getMonth() + 1).padStart(2, '0');
    const endMonth = String(end.getMonth() + 1).padStart(2, '0');
    const startDateTime = `${start.getFullYear()}-${startMonth}-${start.getDate()}T00:00:00`;
    const endDateTime = `${end.getFullYear()}-${endMonth}-${end.getDate()}T23:59:59`;
    const url = `${this.workUrl}/report_total?start_datetime=${startDateTime}&end_datetime=${endDateTime}`;

    return this.http.get<WorkReportTotal>(url)
      .pipe(
        // catchError(this.handleError('getHeroes', []))
      );
  }

  addWorkItem(startDt: string, endDt: string, taskId: number): void {
    const body = {
      start_dt: startDt,
      end_dt: endDt,
      task_id: taskId,
    };
    this.http.post(`${this.workUrl}/items`, body);
  }

  startWork(taskId: number): Observable<any> {
    console.log(`startWork(${taskId})`);
    const body = {
      task_id: taskId
    };
    return this.http.post(`${this.workUrl}/start`, body);
  }

  stopWorkCurrent(): Observable<any> {
    console.log('stopWorkCurrent');
    return this.http.post(`${this.workUrl}/stop_current`, {});
  }
}


