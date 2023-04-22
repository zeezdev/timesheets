import { Component, OnInit } from '@angular/core';
import {CategoryService} from "./category.service";
import {Category} from "./category";

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  providers: [CategoryService],
  styleUrls: ['./category.component.css']
})
export class CategoryComponent implements OnInit {
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
