import {NgModule} from "@angular/core";
import {PageNotFoundComponent} from "./page-not-found/page-not-found.component";
import {MatIconModule} from "@angular/material/icon";

@NgModule({
  imports: [
    MatIconModule
  ],
  declarations: [PageNotFoundComponent]
})
export class PageNotFoundModule {}
