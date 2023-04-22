import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {catchError} from "rxjs/operators";
import {WorkReportByCategory, WorkReportTotal} from './work';
import {Injectable} from '@angular/core';


@Injectable()
export class WorkService {
  workUrl = 'http://localhost:8000/api/work';
  // private handleError: HandleError;

  constructor(
    private http: HttpClient,
    // httpErrorHandler: HttpErrorHandler
  ) {
    // this.handleError = httpErrorHandler.createHandleError('HeroesService');
  }

  /** GET work report grouped by categories from the server */
  getWorkReportByCategory(): Observable<WorkReportByCategory[]> {
    return this.http.get<WorkReportByCategory[]>(`${this.workUrl}/report_by_category`)
      .pipe(
        // catchError(this.handleError('getHeroes', []))
      );
  }

  getWorkReportTotal(): Observable<WorkReportTotal> {
    return this.http.get<WorkReportTotal>(`${this.workUrl}/report_total`)
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

  startWork(taskId: number): void {
    console.log(`startWork(${taskId})`);
    const body = {
      task_id: taskId
    };
    this.http.post(`${this.workUrl}/start`, body).subscribe();
  }

  stopWorkCurrent(): void {
    console.log('stopWorkCurrent');
    this.http.post(`${this.workUrl}/stop_current`, {}).subscribe();
  }
}

