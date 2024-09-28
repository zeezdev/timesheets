import {Injectable} from "@angular/core";
import {Subject} from "rxjs";

/**
 * TodayCounterSharedService makes it possible to call
 * `startCounter` & `stopCounter` methods of `TodayCounterComponent`
 * from another component.
 *
 * Usage:
 *  1. subscribe in the callable component:
 *  ```
 *  constructor(private todayCounterService: TodayCounterSharedService) { }
 *
 *  ngOnInit(): void {
 *   this.todayCounterService.startCall$.subscribe(() => {
 *     this.startCounter();
 *   });
 *   this.todayCounterService.stopCall$.subscribe(() => {
 *     this.stopCounter();
 *   });
 *   ...
 *  ```
 *  2. call in the another component:
 *  ```
 *  constructor(private todayCounterService: TodayCounterSharedService) { }
 *
 *  method(): void {
 *    this.todayCounterService.todayCounterStart();
 *  }
 *  ```
 */
@Injectable({
  providedIn: 'root',
})
export class TodayCounterSharedService {
  private startCallSource = new Subject<void>();
  private stopCallSource = new Subject<void>();
  startCall$ = this.startCallSource.asObservable();
  stopCall$ = this.stopCallSource.asObservable();

  todayCounterStart(): void {
    console.log('todayCounterStart');
    this.startCallSource.next();
  }

  todayCounterStop(): void {
    console.log('todayCounterStop');
    this.stopCallSource.next();
  }
}
