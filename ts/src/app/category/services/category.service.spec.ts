import {CategoryService} from "./category.service";
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {Category} from "./category";
import {of} from "rxjs";
import {asyncError} from "../../shared/utils";


describe('CategoryService', () => {
  let httpClientSpy: jasmine.SpyObj<HttpClient>;
  let categoryService: CategoryService;

  beforeEach(() => {
    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get', 'put', 'post']);
    categoryService = new CategoryService(httpClientSpy);
  });

  it('should return expected categories (HttpClient called once)', (done: DoneFn) => {
    const expectedCategories: Category[] = [
      {id: 1, name: 'TestCategory1', description: 'Test category #1'},
      {id: 2, name: 'TestCategory2', description: 'Test category #2'},
      {id: 3, name: 'TestCategory3', description: 'Test category #3'},
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
    expect(httpClientSpy.get)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(categoryService.categoriesUrl);
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

  it('should return expected category (HttpClient called once)', (done: DoneFn) => {
    const expectedCategory: Category = {id: 1, name: 'TestCategory1', description: 'Test category #1'};

    httpClientSpy.get.and.returnValue(of(expectedCategory));

    categoryService.getCategory(expectedCategory.id).subscribe({
      next: category => {
        expect(category)
          .withContext('expected category')
          .toEqual(expectedCategory);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.get.calls.count())
        .withContext('one call')
        .toBe(1);
    expect(httpClientSpy.get)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(`${categoryService.categoriesUrl}/${expectedCategory.id}`);
  });

  it('should update and return expected category (HttpClient called once)', (done: DoneFn) => {
    const categoryForUpdate: Category = {id: 1, name: 'TestCategory1', description: 'Updated description'};
    const expectedCategory: Category = {...categoryForUpdate};

    httpClientSpy.put.and.returnValue(of(expectedCategory));

    categoryService.updateCategory(categoryForUpdate).subscribe({
      next: category => {
        expect(category)
          .withContext('expected category')
          .toEqual(expectedCategory);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.put.calls.count())
      .withContext('one call')
      .toBe(1);
    expect(httpClientSpy.put)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(
        `${categoryService.categoriesUrl}/${categoryForUpdate.id}`,
        categoryForUpdate,
        categoryService.httpOptions,
      );
  });

  it('should create and return expected category (HttpClient called once)', (done: DoneFn) => {
    const categoryForCreate: Category = {id: null, name: 'TestCategory1', description: 'Updated description'};
    const expectedCategory: Category = {...categoryForCreate, id: 1};

    httpClientSpy.post.and.returnValue(of(expectedCategory));

    categoryService.createCategory(categoryForCreate).subscribe({
      next: category => {
        expect(category)
          .withContext('expected category')
          .toEqual(expectedCategory);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.post.calls.count())
      .withContext('one call')
      .toBe(1);
    expect(httpClientSpy.post)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(
        categoryService.categoriesUrl,
        categoryForCreate,
        categoryService.httpOptions,
      );
  });
});
