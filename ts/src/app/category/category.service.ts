import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {catchError} from "rxjs/operators";
import {Category} from "./category";
import {Injectable} from "@angular/core";


@Injectable()
export class CategoryService {
  categoriesUrl = 'http://localhost:8000/api/categories';
  // private handleError: HandleError;

  constructor(
    private http: HttpClient,
    // httpErrorHandler: HttpErrorHandler
  ) {
    // this.handleError = httpErrorHandler.createHandleError('HeroesService');
  }

  /** GET heroes from the server */
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(this.categoriesUrl)
      .pipe(
        // catchError(this.handleError('getHeroes', []))
      );
  }

}
