import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {catchError} from "rxjs/operators";
import {Task} from "./task";
import {Injectable} from "@angular/core";


@Injectable()
export class TaskService {
  tasksUrl = 'http://localhost:8000/api/tasks';
  // private handleError: HandleError;

  constructor(
    private http: HttpClient,
    // httpErrorHandler: HttpErrorHandler
  ) {
    // this.handleError = httpErrorHandler.createHandleError('HeroesService');
  }

  /** GET heroes from the server */
  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(this.tasksUrl)
      .pipe(
        // catchError(this.handleError('getHeroes', []))
      );
  }

}
