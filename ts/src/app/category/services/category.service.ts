import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {catchError} from "rxjs/operators";
import {Category} from "./category";
import {Injectable} from "@angular/core";
import {AppSettings} from "../../app.settings";
import {handleError} from "../../shared/utils";
import {Router} from "@angular/router";


@Injectable()
export class CategoryService {
  categoriesUrl = `${AppSettings.API_URL}/categories`;
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient,
    private router: Router,
  ) { }

  /** GET a category list from the server */
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(this.categoriesUrl)
      .pipe(
        tap(categories => this.log(`fetched categories ${categories}`)),
        catchError(handleError('getCategories', this.router)),
      ) as Observable<Category[]>;
  }

  /** GET a category from the server **/
  getCategory(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.categoriesUrl}/${id}`)
      .pipe(
        tap(category => this.log(`fetched category ${category}`)),
        catchError(handleError('getCategory', this.router))
      ) as Observable<Category>;
  }

  /** Update a category on the server **/
  updateCategory(category: Category): Observable<Category> {
    return this.http.put<Category>(`${this.categoriesUrl}/${category.id}`, category, this.httpOptions)
      .pipe(
        tap(upCategory => this.log(`updated category ${upCategory}`)),
        catchError(handleError('updateCategory'))
      ) as Observable<Category>;
  }

  /** Create a new category on the server **/
  createCategory(category: Category): Observable<Category> {
    return this.http.post<Category>(this.categoriesUrl, category, this.httpOptions)
      .pipe(
        tap(newCategory => this.log(`created category ${newCategory}`)),
        catchError(handleError('createCategory'))
      ) as Observable<Category>;
  }

  private log(message: string) {
    console.log(`CategoryService: ${message}`);
  }
}
