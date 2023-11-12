import {NgModule} from "@angular/core";
import {CategoryListComponent} from "./category-list/category-list.component";
import {CategoryFormComponent} from "./category-form/category-form.component";
import {MatTableModule} from "@angular/material/table";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {MatInputModule} from "@angular/material/input";
import {MatCardModule} from "@angular/material/card";
import {MatButtonModule} from "@angular/material/button";
import {FormsModule} from "@angular/forms";
import {MatSnackBarModule} from "@angular/material/snack-bar";
import {NgClass} from "@angular/common";
import {CategoryService} from "./services/category.service";

@NgModule({
  declarations: [
    CategoryListComponent,
    CategoryFormComponent,
  ],
  imports: [
    MatTableModule,
    RouterLink,
    MatInputModule,
    MatCardModule,
    MatButtonModule,
    FormsModule,
    MatSnackBarModule,
    RouterLinkActive,
    NgClass,
  ],
  providers: [CategoryService],
})
export class CategoryModule { }
