import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {Task} from "./task";
import {Injectable} from "@angular/core";
import {AppSettings} from "../../app.settings";
import {catchError} from "rxjs/operators";
import {handleError} from "../../shared/utils";
import {Router} from "@angular/router";


@Injectable()
export class TaskService {
  tasksUrl = `${AppSettings.API_URL}/tasks`;
  httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  }

  constructor(
    private http: HttpClient,
    private router: Router,
  ) { }

  /** GET tasks from the server */
  getTasks(isArchived?: boolean, isCurrent?: boolean): Observable<Task[]> {
    const params = {};
    if (isArchived !== undefined) {
      params['is_archived'] = isArchived;
    }
    if (isCurrent !== undefined) {
      params['is_current'] = isCurrent;
    }
    return this.http.get<Task[]>(this.tasksUrl, {params: params})
      .pipe(
        tap(tasks => this.log(`fetched tasks ${tasks}`)),
        catchError(handleError('getTasks'))
      ) as Observable<Task[]>;
  }

  /** GET a task from server */
  getTask(taskId: number): Observable<Task> {
    return this.http.get<Task>(`${this.tasksUrl}/${taskId}`)
      .pipe(
        tap(task => this.log(`fetched task ${task}`)),
        catchError(handleError('getTask', this.router))
      ) as Observable<Task>;
  }

  /** Update a task on the server */
  updateTask(task: Task): Observable<Task> {
    return this.http.put<Task>(`${this.tasksUrl}/${task.id}`, task, this.httpOptions)
      .pipe(
        tap(upTask => this.log(`updated task ${upTask}`)),
        catchError(handleError('updateTask'))
      ) as Observable<Task>;
  }

  /** Create a new task on the server */
  createTask(task: Task): Observable<Task> {
    return this.http.post<Task>(this.tasksUrl, task, this.httpOptions)
      .pipe(
        tap(newTask => this.log(`created task ${newTask}`)),
        catchError(handleError('createTask'))
      ) as Observable<Task>;
  }

  private log(message: string) {
    console.log(`TaskService: ${message}`);
  }
}
