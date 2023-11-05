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

  /** GET tasks from the server */
  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(this.tasksUrl)
      .pipe(
        tap(tasks => this.log(`fetched tasks ${tasks}`)),
        catchError(this.handleError('getTasks'))
      ) as Observable<Task[]>;
  }

  /** GET a task from server */
  getTask(taskId: number): Observable<Task> {
    return this.http.get<Task>(`${this.tasksUrl}/${taskId}`)
      .pipe(
        tap(task => this.log(`fetched task ${task}`)),
        catchError(this.handleError('getTask'))
      ) as Observable<Task>;
  }

  /** Update a task on the server */
  updateTask(task: Task): Observable<Task> {
    return this.http.put<Task>(`${this.tasksUrl}/${task.id}`, task, this.httpOptions)
      .pipe(
        tap(task => this.log(`updated task ${task}`)),
        catchError(this.handleError('updateTask'))
      ) as Observable<Task>;
  }

  /** Create a new task on the server */
  createTask(task: Task): Observable<Task> {
    return this.http.post<Task>(this.tasksUrl, task, this.httpOptions)
      .pipe(
        tap(task => this.log(`created task ${task}`)),
        catchError(this.handleError('createTask'))
      ) as Observable<Task>;
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
