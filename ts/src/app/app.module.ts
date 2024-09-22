import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {HttpClientModule} from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
// Custom
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {CategoryModule} from './category/category.module';
import {TaskModule} from './task/task.module';
import {SharedModule} from './shared/shared.module';
import {WorkModule} from './work/work.module';
import {WorkItemModule} from './work-item/work-item.module';
import {PageNotFoundModule} from "./page-not-found/page-not-found-module";
import {MatSidenavModule} from "@angular/material/sidenav";
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {MainModule} from "./main/main.module";

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    //
    CategoryModule,
    TaskModule,
    SharedModule,
    WorkModule,
    WorkItemModule,
    PageNotFoundModule,
    MainModule,
    MatSidenavModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
