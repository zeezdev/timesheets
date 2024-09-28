import {NgModule} from "@angular/core";
import {MainPageComponent} from "./main-page/main-page.component";
import {MatIconModule} from "@angular/material/icon";
import {TodayCounterComponent} from './today-counter/today-counter.component';

@NgModule({
  declarations: [
    MainPageComponent,
    TodayCounterComponent,
  ],
  imports: [
    MatIconModule,
  ],
  exports: [
    TodayCounterComponent,
  ]
})
export class MainModule {}
