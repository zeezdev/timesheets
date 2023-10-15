import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {catchError} from "rxjs/operators";
import {Task} from "./task";
import {Injectable} from "@angular/core";
import {AppSettings} from "../../app.settings";


@Injectable()
export class TaskService {
  tasksUrl = `${AppSettings.API_URL}/tasks`;
  httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  }
  // private handleError: HandleError;

  constructor(
    private http: HttpClient,
    // httpErrorHandler: HttpErrorHandler
  ) {
    // this.handleError = httpErrorHandler.createHandleError('TaskService');
  }

  /** GET heroes from the server */
  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(this.tasksUrl, this.httpOptions)
      .pipe(
        // catchError(this.handleError('getTasks', []))
      );
  }

  getTask(taskId: number): Observable<Task> {
    return this.http.get<Task>(`${this.tasksUrl}/${taskId}`, this.httpOptions).pipe(
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
}
