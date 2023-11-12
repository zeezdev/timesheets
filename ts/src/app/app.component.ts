import {Component} from '@angular/core';

import {OverworkingWatcher} from './work/services/overworking.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'TimeSheets';

  constructor(
    private overWorkingWatcher: OverworkingWatcher,
  ) {
    overWorkingWatcher.start();
  }
}
