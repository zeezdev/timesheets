import {NgModule} from "@angular/core";
import {MainPageComponent} from "./main-page/main-page.component";
import {MatIconModule} from "@angular/material/icon";

@NgModule({
  imports: [
    MatIconModule
  ],
  declarations: [MainPageComponent]
})
export class MainModule {}
