import {HttpClient} from '@angular/common/http';
import {interval, Observable} from 'rxjs';
// import {catchError} from "rxjs/operators";
import {WorkReportByCategory, WorkReportByTask, WorkReportTotal} from './work';
import {Injectable} from '@angular/core';
import {map} from "rxjs/operators";
import {AppSettings} from "../app.settings";
import {pad} from "../shared/utils";


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


@Injectable({providedIn: 'root'})
export class OverworkingWatcher {
  private overworkInterval: Observable<number> = null;

  private getAlertKey(today: Date, percent: number): string {
    const percentStr = Math.trunc(percent).toString();
    const todayStr = `${today.getFullYear()}-${pad(today.getMonth())}-${pad(today.getDay())}`;
    return `overworkingwatcher-${todayStr}-${percentStr}`;
  }

  private setAlertKeyInLocalStorage(alertKey: string): void {
    localStorage.setItem(alertKey, 'ok');
  }

  private getAlertKeyFromLocalStorage(alertKey: string): boolean {
    return localStorage.getItem(alertKey) === 'ok';
  }

  private alertOverworking(percent: number): void {
    const percentStr = Math.trunc(percent).toString();
    alert(`Today you have already worked ${percentStr}% of the required time!`);
  }

  constructor(
    private workService: WorkService,
  ) {
    this.overworkInterval = interval(1000 * 60); // watch every minute
    this.overworkInterval.subscribe(
      x => {
        const today = new Date();
        const month = today.getMonth();
        const year = today.getFullYear();
        const day = today.getDate();

        const start = new Date(year, month, day);
        const end = new Date(year, month, day, 23, 59, 59, 999);

        this.workService.getWorkReportTotal(start, end).pipe(
          map((report: WorkReportTotal) => {
            return report.time / AppSettings.DAY_SECONDS * 100;
          })
        ).subscribe(
          workTotalPercent => {
            const percent = (
              workTotalPercent - (workTotalPercent % AppSettings.OVERWORKING_ALERT_STEP_PERCENT)
            ); // stepped percent: 86.67 => 85 (86.67 - 1.67)

            if (percent >= AppSettings.OVERWORKING_ALERT_START_PERCENT) {
              const alertKey = this.getAlertKey(today, percent);
              if (!this.getAlertKeyFromLocalStorage(alertKey)) {
                this.setAlertKeyInLocalStorage(alertKey);
                this.alertOverworking(workTotalPercent);
              }
            }
          }
        );
      }
    );
  }
}
