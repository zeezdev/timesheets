import {Component, OnInit} from '@angular/core';
import {map} from 'rxjs/operators';
import {FormGroup, FormControl} from '@angular/forms';
import {MomentDateAdapter, MAT_MOMENT_DATE_ADAPTER_OPTIONS} from '@angular/material-moment-adapter';
import {DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE} from '@angular/material/core';
import {AppSettings} from "../app.settings";
import {WorkService} from "./services/work.service";
import {WorkReportByCategory, WorkReportByTask, WorkReportTotal} from "./services/work";

// Depending on whether rollup is used, moment needs to be imported differently.
// Since Moment.js doesn't have a default export, we normally need to import using the `* as`
// syntax. However, rollup creates a synthetic default module and we thus need to import it using
// the `default as` syntax.
import * as _moment from 'moment';
// tslint:disable-next-line:no-duplicate-imports
import {default as _rollupMoment} from 'moment';

const moment = _rollupMoment || _moment;

// See the Moment.js docs for the meaning of these formats:
// https://momentjs.com/docs/#/displaying/format/
export const MY_FORMATS = {
  parse: {
    dateInput: 'YYYY/MM/DD',
  },
  display: {
    dateInput: 'YYYY/MM/DD',
    monthYearLabel: 'MMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY',
  },
};

// FIXME: may be incorrect if it works more than one day
const today = new Date();
const month = today.getMonth();
const year = today.getFullYear();
const day = today.getDate();

@Component({
  selector: 'app-work',
  templateUrl: './work.component.html',
  providers: [
    // `MomentDateAdapter` can be automatically provided by importing `MomentDateModule` in your
    // application's root module. We provide it at the component level here, due to limitations of
    // our example generation script.
    {
      provide: DateAdapter,
      useClass: MomentDateAdapter,
      deps: [MAT_DATE_LOCALE, MAT_MOMENT_DATE_ADAPTER_OPTIONS],
    },
    {provide: MAT_DATE_FORMATS, useValue: MY_FORMATS},
  ],
  styleUrls: ['./work.component.css']
})
export class WorkComponent implements OnInit {
  workReport: WorkReportByCategory[] = [];
  workReportByTask: WorkReportByTask[] = [];
  workTotal: string = null;
  displayedColumns: string[] = ['category_id', 'category_name', 'time'];
  displayedColumnsByTask: string[] = ['task_id', 'task_name', 'category_name', 'time'];
  range = new FormGroup({
    start: new FormControl(new Date(year, day>20 ? month : month-1, 21)),
    end: new FormControl(new Date(year, day>20 ? month+1 : month, 20))
  });

  constructor(private workService: WorkService) { }

  ngOnInit() {
    // TODO: send Date with TZ info
    const start = new Date(this.range.value.start);
    const end = new Date(this.range.value.end);

    this.getWorkReportByCategory(start, end);
    this.getWorkReportByTask(start, end);
    this.getWorkReportTotal(start, end);
  }

  getWorkReportByCategory(start: Date, end: Date) {
    this.workService.getWorkReportByCategory(start, end).pipe(
      map((report: WorkReportByCategory[]) =>
        report.map((rep: WorkReportByCategory) => {
          return {
            category: rep.category,
            time: (rep.time / AppSettings.DAY_SECONDS).toFixed(2)
          } as unknown as WorkReportByCategory;
        })
      )
    ).subscribe(
      workReport => this.workReport = workReport
    );
  }

  getWorkReportByTask(start: Date, end: Date) {
    this.workService.getWorkReportByTask(start, end).pipe(
      map((report: WorkReportByTask[]) =>
        report.map((rep: WorkReportByTask) => {
          return {
            task: rep.task,
            time: (rep.time / AppSettings.DAY_SECONDS).toFixed(2)
          } as unknown as WorkReportByTask;
        })
      )
    ).subscribe(
      workReport => this.workReportByTask = workReport
    );
  }

  getWorkReportTotal(start: Date, end: Date) {
    this.workService.getWorkReportTotal(start, end).pipe(
      map((report: WorkReportTotal) => {
        return (report.time / AppSettings.DAY_SECONDS).toFixed(2);
      })
    ).subscribe(
      workTotal => {this.workTotal = workTotal}
    );
  }

  dateRangeChange(dateRangeStart: HTMLInputElement, dateRangeEnd: HTMLInputElement) {
    if (this.range.value.start && this.range.value.end) {
      // TODO: send Date with TZ info
      const start = new Date(this.range.value.start);
      const end = new Date(this.range.value.end);

      console.log(`Date range changed: start=${start}, end=${end}`);
      this.getWorkReportByCategory(start, end);
      this.getWorkReportByTask(start, end);
      this.getWorkReportTotal(start, end);
    }
  }
}
