import {Component, OnInit} from '@angular/core';
import {SettingsCache, SettingsService} from "./services/settings.service";
import {Settings} from "./services/settings";
import {NotificationService} from "../shared/notification.service";

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
  settings: Settings = null;

  constructor(
    private settingsCache: SettingsCache,
    private settingsService: SettingsService,
    private notifications: NotificationService,
  ) { }

  ngOnInit(): void {
    this.settingsCache.settings$.subscribe(settings =>{
      this.settings = settings;
    });
  }

  onSubmit(form) {
    this.settingsService.saveSettings({
      first_day_of_week: this.settings.first_day_of_week,
      first_day_of_month: this.settings.first_day_of_month,
    }).subscribe(updatedSettings => {
      console.info('Settings updated successfully.');
      this.notifications.success('Settings updated successfully.');
    });
  }

  onChangeFirstDayOfMonth($event, firstDayOfMonth) {
    this.settings.first_day_of_month = $event;
    if(!firstDayOfMonth.control.touched){
      firstDayOfMonth.control.markAsTouched();
    }
  }

  getErrorMessageForFirstDayOfMonth(errors: any): string {
    if (!errors) return '';

    if (errors.required) return 'This field is required.';
    if (errors.min) return `Value cannot be less than ${errors.min.min}.`;
    if (errors.max) return `Value cannot be greater than ${errors.max.max}.`;

    return 'Invalid value.';
  }
}
