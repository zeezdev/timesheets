import {CategoryService} from "./category.service";
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {Category} from "./category";
import {defer, of} from "rxjs";


/**
 * Create async observable error that errors
 * after a JS engine turn
 */
export function asyncError<T>(errorObject: any) {
  // TODO: move to shared
  return defer(() => Promise.reject(errorObject));
}


describe('CategoryService', () => {
  let httpClientSpy: jasmine.SpyObj<HttpClient>;
  let categoryService: CategoryService;

  beforeEach(() => {
    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);
    categoryService = new CategoryService(httpClientSpy);
  });

  it('should return expected categories (HttpClient called once)', (done: DoneFn) => {
    const expectedCategories: Category[] = [
      {id: 1, name: 'TestCategory1', description: 'Test category #1'},
    ];

    httpClientSpy.get.and.returnValue(of(expectedCategories));

    categoryService.getCategories().subscribe({
        next: categories => {
          expect(categories)
              .withContext('expected categories')
              .toEqual(expectedCategories);
          done();
        },
        error: done.fail
    });
    expect(httpClientSpy.get.calls.count())
        .withContext('one call')
        .toBe(1);
  });

  it('should return an error when the server returns a 404', (done: DoneFn) => {
    const errorResponse = new HttpErrorResponse({
        error: 'test 404 error',
        status: 404,
        statusText: 'Not Found',
    });

    httpClientSpy.get.and.returnValue(asyncError(errorResponse));

    categoryService.getCategories().subscribe({
        next: categories => done.fail('expected an error, not categories'),
        error: error => {
          expect(error.message).toContain('test 404 error');
          done();
        }
    });
  });
});
