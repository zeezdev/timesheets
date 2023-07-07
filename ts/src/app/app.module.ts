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
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
