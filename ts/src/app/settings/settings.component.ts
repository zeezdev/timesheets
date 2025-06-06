import {Component, OnInit} from '@angular/core';
import {SettingsService} from "./services/settings.service";
import {Settings} from "./services/settings";

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
  settings: Settings;

  constructor(
    private settingsService: SettingsService,
  ) { }

  ngOnInit(): void {
    this.settingsService.getSettings().subscribe(
      settings => this.settings = settings
    );
  }

  onSubmit(form) {

  }
}
