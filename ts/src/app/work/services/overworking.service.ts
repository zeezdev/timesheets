import {Injectable} from '@angular/core';
import {interval, Observable} from 'rxjs';
import {pad} from '../../shared/utils';
import {map} from 'rxjs/operators';
import {WorkReportTotal} from './work';
import {AppSettings} from '../../app.settings';
import {WorkService} from './work.service';

@Injectable()
export class OverworkingWatcher {
  private overworkInterval: Observable<number> = null;

  private getAlertKey(today: Date, percent: number): string {
    const percentStr = Math.trunc(percent).toString();
    const todayStr = `${today.getFullYear()}-${pad(today.getMonth())}-${pad(today.getDate())}`;
    return `overworkingwatcher-${todayStr}-${percentStr}`;
  }

  private setAlertKeyInLocalStorage(alertKey: string): void {
    localStorage.setItem(alertKey, 'ok');
  }

  private getAlertKeyFromLocalStorage(alertKey: string): boolean {
    return localStorage.getItem(alertKey) === 'ok';
  }

  private alertOverworking(percent: number): void {
    const percentStr = Math.trunc(percent).toString();
    alert(`Today you have already worked ${percentStr}% of the required time!`);
  }

  constructor(
    private workService: WorkService,
  ) {
    this.overworkInterval = interval(1000 * 60); // watch every minute
    this.overworkInterval.subscribe(
      x => {
        const today = new Date();
        const month = today.getMonth();
        const year = today.getFullYear();
        const day = today.getDate();

        const start = new Date(year, month, day);
        const end = new Date(year, month, day, 23, 59, 59, 999);

        this.workService.getWorkReportTotal(start, end).pipe(
          map((report: WorkReportTotal) => {
            return report.time / AppSettings.DAY_SECONDS * 100;
          })
        ).subscribe(
          workTotalPercent => {
            const percent = (
              workTotalPercent - (workTotalPercent % AppSettings.OVERWORKING_ALERT_STEP_PERCENT)
            ); // stepped percent: 86.67 => 85 (86.67 - 1.67)

            if (percent >= AppSettings.OVERWORKING_ALERT_START_PERCENT) {
              const alertKey = this.getAlertKey(today, percent);
              if (!this.getAlertKeyFromLocalStorage(alertKey)) {
                this.setAlertKeyInLocalStorage(alertKey);
                this.alertOverworking(workTotalPercent);
              }
            }
          }
        );
      }
    );
  }
}
