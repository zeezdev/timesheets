import {Component, OnInit} from '@angular/core';
import {WorkService} from "../../work/services/work.service";
import {WorkReportTotal} from "../../work/services/work";
import {interval} from "rxjs";
import {TaskService} from "../../task/services/task.service";
import { Task } from 'src/app/task/services/task';
import {TodayCounterSharedService} from "./services/today-counter-shared.service";

@Component({
  selector: 'app-today-counter',
  templateUrl: './today-counter.component.html',
  styleUrls: ['./today-counter.component.css']
})
export class TodayCounterComponent implements OnInit {
  counterSeconds: number = null;
  counterIntervalSubscription = null;

  constructor(
    private workService: WorkService,
    private taskService: TaskService,
    private todayCounterService: TodayCounterSharedService,
  ) {}

  get displayValue() {
    return this.secondsToHHMMSS(this.counterSeconds);
  }

  private secondsToHHMMSS(seconds: number | null): string {
    if (!seconds) {
      return '00:00:00';
    }

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    const paddedHours = String(hours).padStart(2, '0');
    const paddedMinutes = String(minutes).padStart(2, '0');
    const paddedSeconds = String(secs).padStart(2, '0');

    return `${paddedHours}:${paddedMinutes}:${paddedSeconds}`;
  }

  startCounter(): void {
    console.log('startCounter()');
    const counterInterval = interval(1000);
    this.counterIntervalSubscription = counterInterval.subscribe(
      () => this.counterSeconds++
    );
  }

  stopCounter(): void {
    console.log('stopCounter()');
    if (this.counterIntervalSubscription !== null) {
      this.counterIntervalSubscription.unsubscribe();
    }
  }

  initCounter(): void {
    // Time range for today
    const start = new Date();
    start.setHours(0, 0, 0, 0);
    const end = new Date();
    end.setHours(23, 59, 59, 999);

    this.workService.getWorkReportTotal(start, end).subscribe(
      (report: WorkReportTotal) => {
        this.counterSeconds = report.time;

        // check if is an active work (Task.isCurrent==True) to start increment
        this.taskService.getTasks(undefined, true).subscribe(
          (tasks: Task[]) => {
            if (tasks.length > 0) {
              this.startCounter();
            }
          }
        )
      }
    );
  }

  ngOnInit(): void {
    this.initCounter();
    this.todayCounterService.startCall$.subscribe(() => {
      this.startCounter();
    });
    this.todayCounterService.stopCall$.subscribe(() => {
      this.stopCounter();
    });
  }
}
