import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {firstValueFrom, Observable, of} from "rxjs";
import {AppSettings} from "../../app.settings";
import {Settings} from "./settings";

@Injectable()
export class SettingsService {
  constructor(
    private http: HttpClient,
  ) { }

  getSettings(): Observable<Settings> {
    const utl = `${AppSettings.API_URL}/settings`;
    return this.http.get<Settings>(utl);
  }

  // loadSettings(): Promise<void> {
  //   const url = `${AppSettings.API_URL}/settings`;
  //   return firstValueFrom(this.http.get<Settings>(url))
  //     .then(data => {
  //       this.firstDayOfWeek = data.first_day_of_week;
  //       this.firstDayOfMonth = data.first_day_of_month;
  //     })
  //     .catch(() => {
  //       console.error('Failed to load app settings');
  //     });
  // }
  //
  // getFirstDayOfWeek(): number {
  //   return this.firstDayOfWeek;
  // }
  //
  // getFirstDayOfMonth(): number {
  //   return this.firstDayOfMonth;
  // }
}

@Injectable({
  providedIn: 'root'
})
export class SettingsCache {
  /**
   * TODO: replace this class with using the Store
   */
  private firstDayOfWeek: number;
  private firstDayOfMonth: number;

  constructor(
    private settingsService: SettingsService,
  ) { }

  loadSettings(): Promise<void> {
    return firstValueFrom(this.settingsService.getSettings())
      .then((data: Settings) => {
        this.firstDayOfWeek = data.first_day_of_week;
        this.firstDayOfMonth = data.first_day_of_month;
      })
      .catch(() => {
        console.error('Failed to load app settings');
      });
  }

  getFirstDayOfWeek(): number {
    return this.firstDayOfWeek;
  }

  getFirstDayOfMonth(): number {
    return this.firstDayOfMonth;
  }
}
