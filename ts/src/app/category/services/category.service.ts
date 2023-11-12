import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {catchError} from "rxjs/operators";
import {Category} from "./category";
import {Injectable} from "@angular/core";
import {AppSettings} from "../../app.settings";
import {handleError} from "../../shared/utils";


@Injectable()
export class CategoryService {
  categoriesUrl = `${AppSettings.API_URL}/categories`;
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient,
  ) { }

  /** GET a category list from the server */
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(this.categoriesUrl)
      .pipe(
        tap(categories => this.log(`fetched categories ${categories}`)),
        catchError(handleError('getCategories'))
      ) as Observable<Category[]>;
  }

  /** GET a category from the server **/
  getCategory(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.categoriesUrl}/${id}`)
      .pipe(
        tap(() => this.log(`fetched category ${id}`)),
        catchError(handleError('getCategory'))
      ) as Observable<Category>;
  }

  /** Update a category on the server **/
  updateCategory(category: Category): Observable<Category> {
    return this.http.put<Category>(`${this.categoriesUrl}/${category.id}`, category, this.httpOptions)
      .pipe(
        tap(() => this.log(`updated category ${category}`)),
        catchError(handleError('updateCategory'))
      ) as Observable<Category>;
  }

  /** Create a new category on the server **/
  createCategory(category: Category): Observable<Category> {
    return this.http.post<Category>(this.categoriesUrl, category, this.httpOptions)
      .pipe(
        tap(() => this.log(`created category ${category}`)),
        catchError(handleError('createCategory'))
      ) as Observable<Category>;
  }

  private log(message: string) {
    console.log(`CategoryService: ${message}`);
  }
}
