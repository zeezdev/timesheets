import {HttpClient} from "@angular/common/http";
import {CategoryService} from "../../category/services/category.service";
import {Category} from "../../category/services/category";
import {of} from "rxjs";
import {WorkService} from "./work.service";
import {WorkReportByCategory, WorkReportByTask, WorkReportTotal} from "./work";

describe('WorkService', () => {
  let httpClientSpy: jasmine.SpyObj<HttpClient>;
  let workService: WorkService;

  beforeEach(() => {
    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get', 'post']);
    workService = new WorkService(httpClientSpy);
  });

  it('should return expected work report by category (HttpClient called once)', (done: DoneFn) => {
    const expectedReport: WorkReportByCategory[] = [
      {category_id: 1, category_name: 'Category1', time: 100.0},
      {category_id: 2, category_name: 'Category2', time: 200.0},
      {category_id: 3, category_name: 'Category3', time: 300.0},
    ];
    // Get report for one day
    const startDate = new Date(2023, 10, 9);
    const endDate = new Date(2023, 10, 9);
    const expectedUrl = `${workService.workUrl}/report_by_category?start_datetime=2023-11-09T00:00:00&end_datetime=2023-11-10T00:00:00`;

    httpClientSpy.get.and.returnValue(of(expectedReport));

    workService.getWorkReportByCategory(startDate, endDate).subscribe({
      next: report => {
        expect(report)
          .withContext('expected report')
          .toEqual(expectedReport);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.get.calls.count())
      .withContext('one call')
      .toBe(1);
    expect(httpClientSpy.get)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(expectedUrl);
  });

  it('should return expected work report by task (HttpClient called once)', (done: DoneFn) => {
    const expectedReport: WorkReportByTask[] = [
      {task_id: 1, task_name: 'Task1', category_id: 1, time: 100.0},
      {task_id: 2, task_name: 'Task2', category_id: 1, time: 200.0},
      {task_id: 3, task_name: 'Task3', category_id: 2, time: 300.0},
    ];
    // Get report for one day
    const startDate = new Date(2023, 10, 9);
    const endDate = new Date(2023, 10, 9);
    const expectedUrl = `${workService.workUrl}/report_by_task?start_datetime=2023-11-09T00:00:00&end_datetime=2023-11-10T00:00:00`;

    httpClientSpy.get.and.returnValue(of(expectedReport));

    workService.getWorkReportByTask(startDate, endDate).subscribe({
      next: report => {
        expect(report)
          .withContext('expected report')
          .toEqual(expectedReport);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.get.calls.count())
      .withContext('one call')
      .toBe(1);
    expect(httpClientSpy.get)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(expectedUrl);
  });

  it('should return expected total work report (HttpClient called once)', (done: DoneFn) => {
    const expectedReport: WorkReportTotal = {time: 300.0};
    // Get report for one day
    const startDate = new Date(2023, 10, 9);
    const endDate = new Date(2023, 10, 9);
    const expectedUrl = `${workService.workUrl}/report_total?start_datetime=2023-11-09T00:00:00&end_datetime=2023-11-10T00:00:00`;

    httpClientSpy.get.and.returnValue(of(expectedReport));

    workService.getWorkReportTotal(startDate, endDate).subscribe({
      next: report => {
        expect(report)
          .withContext('expected report')
          .toEqual(expectedReport);
        done();
      },
      error: done.fail
    });
    expect(httpClientSpy.get.calls.count())
      .withContext('one call')
      .toBe(1);
    expect(httpClientSpy.get)
      .withContext('called once with')
      .toHaveBeenCalledOnceWith(expectedUrl);
  });
});
