import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatInputModule} from '@angular/material/input';
import {MatTableModule} from '@angular/material/table';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatSortModule} from '@angular/material/sort';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatNativeDateModule} from '@angular/material/core';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatButtonModule} from '@angular/material/button';
import {MatBottomSheetModule} from '@angular/material/bottom-sheet';
import {MatButtonToggleModule} from '@angular/material/button-toggle';
import {MatDialogModule} from '@angular/material/dialog';
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
    MatNativeDateModule,
    MatInputModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatBottomSheetModule,
    MatButtonModule,
    MatButtonToggleModule,
    ReactiveFormsModule,
    MatDatepickerModule,
    MatDatepickerModule,
    MatDialogModule,
    //
    CategoryModule,
    TaskModule,
    SharedModule,
    WorkModule,
  ],
  providers: [MatDialogModule],
  bootstrap: [AppComponent]
})
export class AppModule { }
