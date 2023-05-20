import {Component, OnInit} from '@angular/core';
import {Category} from "../services/category";
import {ActivatedRoute, ParamMap, Router} from "@angular/router";
import {CategoryService} from "../services/category.service";
import {NotificationService} from "../../shared/notification.service";
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-category-form',
  templateUrl: './category-form.component.html',
  providers: [CategoryService, NotificationService],
  styleUrls: ['./category-form.component.css']
})
export class CategoryFormComponent implements OnInit {
  category?: Category|null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private service: CategoryService,
    private notifications: NotificationService,
    private _snackBar: MatSnackBar,
  ) {}

  getCategory(categoryId: number) {
    this.service.getCategory(categoryId).subscribe(category => this.category = category);
  }

  ngOnInit() {
    this.route.paramMap.subscribe(
        (params: ParamMap) => {
          const categoryId: string = params.get('id');
          if (categoryId != 'add') {
            this.getCategory(Number.parseInt(categoryId!));
          }
        }
    );
  }

  onSubmit(form) {
    if (this.category !== null) {
      this.service.updateCategory(this.category).subscribe(
        () => {
          console.info('Category saved.');
          this.notifications.success('Saved');
        }
      );
    } else {
      this.service.createCategory(
        {id: null, name: form.value.name, description: form.value.description}
      ).subscribe(
        (createdCategory: Category) => {
          console.info('Category created');
          this.router.navigate(['/categories', createdCategory.id]);
          this.notifications.success('Created');
        }
      );
    }
  }
}
