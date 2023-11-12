import { Component, OnInit } from '@angular/core';
import {CategoryService} from '../services/category.service';
import {Category} from '../services/category';


@Component({
  selector: 'app-category',
  templateUrl: './category-list.component.html',
  styleUrls: ['./category-list.component.css']
})
export class CategoryListComponent implements OnInit {
  // https://v7.material.angular.io/components/table/overview
  // https://blog.angular-university.io/angular-material-data-table/
  categories: Category[] = [];
  displayedColumns: string[] = ['id', 'name', 'description'];

  constructor(private categoryService: CategoryService) { }

  ngOnInit() {
    this.getCategories();
  }

  getCategories() {
    this.categoryService.getCategories().subscribe(categories => (this.categories = categories));
  }
}
