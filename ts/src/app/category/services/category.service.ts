import {HttpClient, HttpErrorResponse, HttpHeaders} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {catchError} from "rxjs/operators";
import {Category} from "./category";
import {Injectable} from "@angular/core";
import {AppSettings} from "../../app.settings";


@Injectable()
export class CategoryService {
  categoriesUrl = `${AppSettings.API_URL}/categories`;
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };
  // private handleError: HandleError;

  constructor(
    private http: HttpClient,
    // httpErrorHandler: HttpErrorHandler
  ) {
    // this.handleError = httpErrorHandler.createHandleError('CategoryService');
  }

  /** GET a category list from the server */
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(this.categoriesUrl)
      .pipe(
        tap(categories => this.log('fetched categories')),
        catchError(this.handleError('getCategories'))
      ) as Observable<Category[]>;
  }

  /** GET a category from the server **/
  getCategory(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.categoriesUrl}/${id}`)
      .pipe(
        // catchError(this.handleError('getCategory', []))
      );
  }

  updateCategory(category: Category): Observable<Category> {
    return this.http.put<Category>(`${this.categoriesUrl}/${category.id}`, category, this.httpOptions)
      .pipe(
        // catchError(this.handleError('getHeroes', []))
      );
  }

  createCategory(category: Category): Observable<Category> {
    return this.http.post<Category>(this.categoriesUrl, category, this.httpOptions).pipe(
      // catchError(this.handleError('getHeroes', []))
    );
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
    console.log('CategoryService: ' + message);
  }
}
