import {HttpClient} from '@angular/common/http';
import {Observable, tap} from 'rxjs';
import {catchError} from "rxjs/operators";
import {WorkReportByCategory, WorkReportByTask, WorkReportTotal} from './work';
import {Injectable} from '@angular/core';
import {AppSettings} from "../../app.settings";
import {handleError, pad} from "../../shared/utils";


@Injectable()
export class WorkService {
  workUrl = `${AppSettings.API_URL}/work`;

  constructor(
    private http: HttpClient,
  ) { }

  private getStartDateTime(start: Date): string {
    const startMonth = pad(start.getMonth() + 1);
    const startDay = pad(start.getDate());
    return `${start.getFullYear()}-${startMonth}-${startDay}T00:00:00`;
  }

  private getEndDateTime(end: Date): string {
    const realEnd = end;
    realEnd.setDate(realEnd.getDate() + 1);  // next day
    const endMonth = pad(realEnd.getMonth() + 1);
    const endDay = pad(realEnd.getDate());
    return `${realEnd.getFullYear()}-${endMonth}-${endDay}T00:00:00`;
  }

  /** GET a work report grouped by categories from the server */
  getWorkReportByCategory(start: Date, end: Date): Observable<WorkReportByCategory[]> {
    const startDateTime = this.getStartDateTime(start);
    const endDateTime = this.getEndDateTime(end);
    const url = `${this.workUrl}/report_by_category?start_datetime=${startDateTime}&end_datetime=${endDateTime}`;

    return this.http.get<WorkReportByCategory[]>(url)
      .pipe(
        tap(report => this.log(`fetched work report by category ${report}`)),
        catchError(handleError('getWorkReportByCategory'))
      ) as Observable<WorkReportByCategory[]>;
  }

  /** GET a work report grouped by tasks from the server */
  getWorkReportByTask(start: Date, end: Date): Observable<WorkReportByTask[]> {
    const startDateTime = this.getStartDateTime(start);
    const endDateTime = this.getEndDateTime(end);
    const url = `${this.workUrl}/report_by_task?start_datetime=${startDateTime}&end_datetime=${endDateTime}`;

    return this.http.get<WorkReportByTask[]>(url)
      .pipe(
        tap(report => this.log(`fetched work report by task ${report}`)),
        catchError(handleError('getWorkReportByTask'))
      ) as Observable<WorkReportByTask[]>;
  }

  /** GET a report of the total working time from the server */
  getWorkReportTotal(start: Date, end: Date): Observable<WorkReportTotal> {
    const startDateTime = this.getStartDateTime(start);
    const endDateTime = this.getEndDateTime(end);
    const url = `${this.workUrl}/report_total?start_datetime=${startDateTime}&end_datetime=${endDateTime}`;

    return this.http.get<WorkReportTotal>(url)
      .pipe(
        tap(report => this.log(`fetched total work report ${report}`)),
        catchError(handleError('getWorkReportTotal'))
      ) as Observable<WorkReportTotal>;
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

  private log(message: string) {
    console.log(`WorkService: ${message}`);
  }
}
