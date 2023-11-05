import {HttpClient, HttpErrorResponse, HttpHeaders} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {Task} from "./task";
import {Injectable} from "@angular/core";
import {AppSettings} from "../../app.settings";
import {catchError} from "rxjs/operators";


@Injectable()
export class TaskService {
  tasksUrl = `${AppSettings.API_URL}/tasks`;
  httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  }

  constructor(
    private http: HttpClient,
  ) { }

  /** GET heroes from the server */
  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(this.tasksUrl)
    .pipe(
      tap(() => this.log),
      catchError(this.handleError('getTasks'))
    ) as Observable<Task[]>;
  }

  getTask(taskId: number): Observable<Task> {
    return this.http.get<Task>(`${this.tasksUrl}/${taskId}`).pipe(
      // catchError(this.handleError('getTask', []))
    );
  }

  updateTask(task: Task): Observable<Task> {
    return this.http.put<Task>(`${this.tasksUrl}/${task.id}`, task, this.httpOptions).pipe(
      // catchError(this.handleError('updateTask', []))
    );
  }

  createTask(task: Task): Observable<Task> {
    return this.http.post<Task>(this.tasksUrl, task, this.httpOptions);
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   *
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation') {
    return (error: HttpErrorResponse): Observable<T> => {
      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // If a native error is caught, do not transform it. We only want to
      // transform response errors that are not wrapped in an `Error`.
      if (error.error instanceof Event) {
        throw error.error;
      }

      const message = `server returned code ${error.status} with body "${error.error}"`;
      // TODO: better job of transforming error for user consumption
      throw new Error(`${operation} failed: ${message}`);
    };
  }

  private log(message: string) {
    console.log(`TaskService: ${message}`);
  }
}
