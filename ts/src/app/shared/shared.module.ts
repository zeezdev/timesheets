import {NgModule} from "@angular/core";
import {AlertDialog, ConfirmationDialog} from "./notification.service";
import {MatDialogModule} from "@angular/material/dialog";
import {MatButtonModule} from "@angular/material/button";
import {MatSnackBarModule} from "@angular/material/snack-bar";

@NgModule({
  imports: [
    MatDialogModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  declarations: [
    AlertDialog,
    ConfirmationDialog,
  ]
})
export class SharedModule { }
