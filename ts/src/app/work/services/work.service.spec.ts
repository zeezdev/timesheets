import {HttpClient} from "@angular/common/http";
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
      {category: {id: 1, name: 'Category1'}, time: 100.0},
      {category: {id: 2, name: 'Category2'}, time: 200.0},
      {category: {id: 3, name: 'Category3'}, time: 300.0},
    ];
    // Get the report for one day
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
      {task: {id: 1, name: 'Task1', category: {id: 1, name: 'Category1'}}, time: 100.0},
      {task: {id: 2, name: 'Task2', category: {id: 1, name: 'Category1'}}, time: 200.0},
      {task: {id: 3, name: 'Task3', category: {id: 2, name: 'Category2'}}, time: 300.0},
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

  it('should return expected end datetime each time', () => {
    const endRangeDate = new Date('2023-11-21T09:45:00');

    expect(workService['getEndDateTime'](endRangeDate)).toEqual('2023-11-22T00:00:00');
    // repeat to be sure we'll get the same result
    expect(workService['getEndDateTime'](endRangeDate)).toEqual('2023-11-22T00:00:00');
  });
});
