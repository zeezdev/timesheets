import { Component, OnInit } from '@angular/core';
import {WorkService} from './work.service';
import {WorkReportByCategory, WorkReportTotal} from './work';
import {map} from 'rxjs/operators';
import {FormControl} from '@angular/forms';
import {DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE} from '@angular/material/core';

@Component({
  selector: 'app-work',
  templateUrl: './work.component.html',
  providers: [
    WorkService,
    // `MomentDateAdapter` can be automatically provided by importing `MomentDateModule` in your
    // application's root module. We provide it at the component level here, due to limitations of
    // our example generation script.
  ],
  styleUrls: ['./work.component.css']
})
export class WorkComponent implements OnInit {
  workReport: { category_id: number, category_name: string, time: string }[] = [];
  workTotal: string = null;
  // workReport: any[] = [];
  // workReport: WorkReportByCategory[] = [];
  displayedColumns: string[] = ['category_id', 'category_name', 'time'];

  constructor(private workService: WorkService) { }

  ngOnInit() {
    this.getWorkReportByCategory();
    this.getWorkReportTotal();
  }

  getWorkReportByCategory() {
    this.workService.getWorkReportByCategory().pipe(
      map((report: WorkReportByCategory[]) =>
        report.map((rep: WorkReportByCategory) => {
          return {
            category_id: rep.category_id,
            category_name: rep.category_name,
            time: (rep.time / 60 / 60 / 8).toFixed(2)
          };
        })
      )
    ).subscribe(
      workReport => {this.workReport = workReport}
    );
  }

  getWorkReportTotal() {
    this.workService.getWorkReportTotal().pipe(
      map((report: WorkReportTotal) => {
        return (report.time / 60 / 60 / 8).toFixed(2);
      })
    ).subscribe(
      workTotal => {this.workTotal = workTotal}
    );
  }

}
