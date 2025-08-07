import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {BehaviorSubject, firstValueFrom, Observable, of, tap} from "rxjs";
import {AppSettings} from "../../app.settings";
import {Settings} from "./settings";
import {Task} from "../../task/services/task";
import {catchError} from "rxjs/operators";
import {handleError} from "../../shared/utils";

@Injectable()
export class SettingsService {
  private settingsApiUrl = `${AppSettings.API_URL}/settings`;

  httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  }

  constructor(
    private http: HttpClient,
  ) { }

  getSettings(): Observable<Settings> {
    return this.http.get<Settings>(this.settingsApiUrl);
  }

  saveSettings(settings: Settings): Observable<Settings> {
    return this.http.put<Task>(this.settingsApiUrl, settings, this.httpOptions)
      .pipe(
        tap(upSettings => this.log(`updated settings ${upSettings}`)),
        catchError(handleError('updateSettings'))
      ) as Observable<Settings>;
  }

  private log(message: string) {
    console.log(`SettingsService: ${message}`);
  }
}

@Injectable({
  providedIn: 'root'
})
export class SettingsCache {
  private settingsSubject = new BehaviorSubject<Settings | null>(null);

  constructor(
    private settingsService: SettingsService,
  ) {}

  loadSettings(): Promise<void> {
    return firstValueFrom(this.settingsService.getSettings())
      .then((settings: Settings) => {
          this.settingsSubject.next(settings);
      })
      .catch(() => {
        console.error('Failed to load app settings');
      });
  }

  get settings$() {
    return this.settingsSubject.asObservable();
  }

  get settings(): Settings | null {
    return this.settingsSubject.value;
  }
}
