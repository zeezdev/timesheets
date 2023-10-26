import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
// import {catchError} from "rxjs/operators";
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
        // catchError(this.handleError('getCategories', []))
      );
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
}
