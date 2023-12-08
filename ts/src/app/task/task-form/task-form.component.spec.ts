import {ComponentFixture, inject, TestBed, waitForAsync} from '@angular/core/testing';

import {TaskFormComponent} from './task-form.component';
import {RouterTestingModule} from '@angular/router/testing';
import {TaskService} from '../services/task.service';
import {HttpClientTestingModule} from '@angular/common/http/testing';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatDialogModule} from '@angular/material/dialog';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatCardModule} from '@angular/material/card';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {CategoryService} from "../../category/services/category.service";
import {MatOptionModule} from "@angular/material/core";
import {MatSelectModule} from "@angular/material/select";
import {NgForOf, NgIf} from "@angular/common";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {OverlayContainer} from "@angular/cdk/overlay";
import {of} from "rxjs";
import {Category} from "../../category/services/category";

fdescribe('TaskFormComponent', () => {
  let component: TaskFormComponent;
  let fixture: ComponentFixture<TaskFormComponent>;
  let inputId: HTMLInputElement;
  let inputName: HTMLInputElement;
  let inputCategory: HTMLSelectElement;
  let submitButton: HTMLButtonElement;
  // Overlay
  let container: OverlayContainer;
  let containerElement: HTMLElement;
  // Data
  const existedCategories: Category[] = [
    {id: 1, name: 'MyCategory#1'},
    {id: 2, name: 'MyCategory#2'},
    {id: 3, name: 'MyCategory#3'},
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
        MatSnackBarModule,
        MatDialogModule,
        FormsModule,
        MatCardModule,
        MatInputModule,
        BrowserAnimationsModule,
        MatSelectModule,
        MatOptionModule,
        NgForOf,
        NgIf,
        ReactiveFormsModule,
        MatProgressSpinnerModule,
      ],
      declarations: [TaskFormComponent],
      providers: [
        TaskService,
        {
          provide: CategoryService,
          useValue: {
            getCategories: () => of(existedCategories)
          }
        }
      ],
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskFormComponent);
    component = fixture.componentInstance;
    inputId = fixture.nativeElement.querySelector('#id');
    inputName = fixture.nativeElement.querySelector('#name');
    inputCategory = fixture.nativeElement.querySelector('#category_id');
    submitButton = fixture.nativeElement.querySelector('#task-submit');

    inject([OverlayContainer], (oc: OverlayContainer) => {
        container = oc;
        containerElement = oc.getContainerElement();
    })();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show existed task', waitForAsync(() => {
    component.task = {id: 9, name: 'MyTask#9', category: {id: 2, name: 'MyCategory#2'}};
    component.categories = [{id: 2, name: 'MyCategory#2'}];
    fixture.detectChanges();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      expect(inputId.value).toEqual('9');
      expect(inputName.value).toEqual('MyTask#9');
      expect(inputCategory.textContent).toEqual('MyCategory#2');
    });
  }));

  it('should show categories on click categories list', waitForAsync(() => {
    component.task = {id: 9, name: 'MyTask#9', category: {id: 2, name: 'MyCategory#2'}};
    component.categories = [{id: 2, name: 'MyCategory#2'}];
    fixture.detectChanges();

    inputCategory.click();
    fixture.detectChanges();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      let options = Array.from(
        containerElement.querySelectorAll('mat-option') as NodeListOf<HTMLElement>
      );

      expect(options).toHaveSize(existedCategories.length);
      options.forEach((opt, index) => {
          const expectedTextContent = existedCategories[index].name;
          expect(opt.textContent.trim()).toEqual(expectedTextContent);
      });

      // Selected option
      expect(options[1].textContent.trim()).toEqual(existedCategories[1].name);
      expect(options[1]).toHaveClass('mdc-list-item--selected');

      // Select a new option
      options[2].click();
      fixture.detectChanges();

      expect(inputCategory.textContent.trim()).toEqual(existedCategories[2].name);
    });
  }));

  it('should show option \'Loading...\' when categories being loading', () => {
    component.task = {id: 9, name: 'MyTask#9', category: {id: 2, name: 'MyCategory#2'}};
    component.categories = null;
    fixture.detectChanges();

    inputCategory.click();
    fixture.detectChanges();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      let options = Array.from(
        containerElement.querySelectorAll('mat-option') as NodeListOf<HTMLElement>
      );

      expect(options).toHaveSize(1);
      expect(options[0].textContent.trim()).toEqual('Loading...');
    });
  });

  it('should show empty elements for new task', waitForAsync(() => {
    component.task = null;
    component.categories = [{id: 2, name: 'MyCategory#2'}];
    fixture.detectChanges();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      expect(inputId.value).toEqual('');
      expect(inputName.value).toEqual('');
      expect(inputCategory.textContent).toEqual('');
    });
  }));

  it('should show option \`No categories have been created yet.\'', () => {
    component.task = null;
    component.categories = [];
    fixture.detectChanges();

    inputCategory.click();
    fixture.detectChanges();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      let options = Array.from(
        containerElement.querySelectorAll('mat-option') as NodeListOf<HTMLElement>
      );

      expect(options).toHaveSize(1);
      expect(options[0].textContent.trim()).toEqual('No categories have been created yet.');
    });
  });

  it('should create new task on submit', waitForAsync(() => {
    spyOn(component, 'onSubmit');
    component.task = null;
    component.categories = existedCategories;
    fixture.detectChanges();
    inputName.value = 'NewTask';
    inputCategory.selectedIndex = 3;

    submitButton.click();

    fixture.whenStable().then(() => {
      // TODO: validate a call of the service
      expect(component.onSubmit).toHaveBeenCalled();
    });
  }));

  it('should update existed task on submit', waitForAsync(() => {
    spyOn(component, 'onSubmit');
    component.task = {id: 9, name: 'MyTask#9', category: {id: 2, name: 'MyCategory#2'}};
    component.categories = existedCategories;
    fixture.detectChanges();
    inputName.value = 'UpdatedTask';
    inputCategory.selectedIndex = 3;

    submitButton.click();

    fixture.whenStable().then(() => {
      // TODO: validate a call of the service
      expect(component.onSubmit).toHaveBeenCalled();
    });
  }));
});
