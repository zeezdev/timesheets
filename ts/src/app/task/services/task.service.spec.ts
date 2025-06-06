import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {TaskService} from "./task.service";
import {of, throwError} from "rxjs";
import {Task} from "./task";
import {asyncError} from "../../shared/utils";
import {async, TestBed} from "@angular/core/testing";
import {Router} from "@angular/router";


describe('TaskService', () => {
  let httpClientSpy: jasmine.SpyObj<HttpClient>;
  let routerSpy: jasmine.SpyObj<Router>;
  let taskService: TaskService;

  beforeEach(() => {
    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get', 'put', 'post']);
    routerSpy = jasmine.createSpyObj('Router', ['navigate'])
    taskService = new TaskService(httpClientSpy, routerSpy);
  });

  it('should return expected tasks (HttpClient called once)', (done: DoneFn) => {
    const expectedTasks: Task[] = [
      {id: 1, name: 'TestTask1', category: {id: 1, name: 'TestCategory1'}, is_current: false, is_archived: true},
      {id: 2, name: 'TestTask2', category: {id: 1, name: 'TestCategory1'}, is_current: true, is_archived: false},
      {id: 3, name: 'TestTask3', category: {id: 2, name: 'TestCategory2'}, is_current: false, is_archived: false},
    ];

    httpClientSpy.get.and.returnValue(of(expectedTasks));

    taskService.getTasks().subscribe({
      next: tasks => {
        expect(tasks)
          .withContext('expected tasks')
          .toEqual(expectedTasks);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.get.calls.count())
      .withContext('one call')
      .toBe(1);
    expect(httpClientSpy.get)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(taskService.tasksUrl, {params: {}});
  });

  it('should return non archived tasks only (HttpClient called once)', (done: DoneFn) => {
    const expectedTasks: Task[] = [
      {id: 2, name: 'TestTask2', category: {id: 1, name: 'TestCategory1'}, is_current: true, is_archived: false},
      {id: 3, name: 'TestTask3', category: {id: 2, name: 'TestCategory2'}, is_current: false, is_archived: false},
    ];

    httpClientSpy.get.and.returnValue(of(expectedTasks));

    taskService.getTasks(false).subscribe({
      next: tasks => {
        expect(tasks)
          .withContext('expected tasks')
          .toEqual(expectedTasks);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.get.calls.count())
      .withContext('one call')
      .toBe(1);
    expect(httpClientSpy.get)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(taskService.tasksUrl, {params: {is_archived: false}});
  });

  it('should return current task only (HttpClient called once)', (done: DoneFn) => {
    const expectedTasks: Task[] = [
      {id: 2, name: 'TestTask2', category: {id: 1, name: 'TestCategory1'}, is_current: true, is_archived: false},
    ];

    httpClientSpy.get.and.returnValue(of(expectedTasks));

    taskService.getTasks(undefined, true).subscribe({
      next: tasks => {
        expect(tasks)
          .withContext('expected tasks')
          .toEqual(expectedTasks);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.get.calls.count())
      .withContext('one call')
      .toBe(1);
    expect(httpClientSpy.get)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(taskService.tasksUrl, {params: {is_current: true}});
  });

  it('should return an error when the server returns a 404', (done: DoneFn) => {
    const errorResponse = new HttpErrorResponse({
        error: 'test 404 error',
        status: 404,
        statusText: 'Not Found',
    });

    httpClientSpy.get.and.returnValue(asyncError(errorResponse));

    taskService.getTasks().subscribe({
      next: tasks => done.fail('expected an error, not tasks'),
      error: error => {
        expect(error.message).toContain('test 404 error');
        done();
      }
    });
  });

  it('should return expected task (HttpClient called once)', (done: DoneFn) => {
    const expectedTask: Task = {
      id: 2,
      name: 'TestTask2',
      category: {id: 1, name: 'TestCategory1'},
      is_current: true,
      is_archived: false,
    };

    httpClientSpy.get.and.returnValue(of(expectedTask));

    taskService.getTask(expectedTask.id).subscribe({
      next: task => {
        expect(task)
          .withContext('expected task')
          .toEqual(expectedTask);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.get.calls.count())
        .withContext('one call')
        .toBe(1);
    expect(httpClientSpy.get)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(`${taskService.tasksUrl}/${expectedTask.id}`);
  });

  it('should update and return expected task (HttpClient called once)', (done: DoneFn) => {
    const taskForUpdate: Task = {id: 2, name: 'TestTask2', category: {id: 1}, is_archived: false};
    const expectedTask: Task = {
      ...taskForUpdate,
      category: {id: 1, name: 'TestCategory1'},
      is_current: true,
      is_archived: false,
    };

    httpClientSpy.put.and.returnValue(of(expectedTask));

    taskService.updateTask(taskForUpdate).subscribe({
      next: task => {
        expect(task)
          .withContext('expected task')
          .toEqual(expectedTask);
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
        `${taskService.tasksUrl}/${taskForUpdate.id}`,
        taskForUpdate,
        taskService.httpOptions,
      );
  });

  it('should create and return expected task (HttpClient called once)', (done: DoneFn) => {
    const taskForCreate: Task = {id: null, name: 'New task', category: {id: 1}, is_archived: false};
    const expectedTask: Task = {
      ...taskForCreate,
      id: 1,
      category: {id: 1, name: 'TestCategory1'},
      is_current: false,
      is_archived: false,
    };

    httpClientSpy.post.and.returnValue(of(expectedTask));

    taskService.createTask(taskForCreate).subscribe({
      next: task => {
        expect(task)
          .withContext('expected task')
          .toEqual(expectedTask);
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
        taskService.tasksUrl,
        taskForCreate,
        taskService.httpOptions,
      );
  });

  it('should navigate to /not-found when task not found (404)', (done: DoneFn) => {
    const errorResponse = new HttpErrorResponse({
      error: '404 error',
      status: 404,
      statusText: 'Not Found'
    });

    httpClientSpy.get.and.returnValue(throwError(() => errorResponse));

    taskService.getTask(999).subscribe({
      next: () => done.fail('Expected an error, not a task'),
      error: () => {
        expect(routerSpy.navigate).toHaveBeenCalledOnceWith(['/not-found']);
        done();
      }
    });
  });
});
