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
import {Task} from "../services/task";
import {ActivatedRoute} from "@angular/router";
import {MatCheckboxModule} from "@angular/material/checkbox";

describe('TaskFormComponent', () => {
  let component: TaskFormComponent;
  let fixture: ComponentFixture<TaskFormComponent>;
  let inputId: HTMLInputElement;
  let inputName: HTMLInputElement;
  let inputCategory: HTMLSelectElement;
  let submitButton: HTMLButtonElement;
  // Overlay
  let containerElement: HTMLElement;
  // Data
  const existedCategories: Category[] = [
    {id: 1, name: 'MyCategory#1'},
    {id: 2, name: 'MyCategory#2'},
    {id: 3, name: 'MyCategory#3'},
  ];
  // Mock objects
  let mockTaskService = null;
  let mockRoute = null;
  let mockCategoryService = null;

  beforeEach(async () => {
    mockTaskService = jasmine.createSpyObj(['getTask', 'createTask', 'updateTask']);
    mockTaskService.getTask.and.returnValue(of({
      id: 9, name: 'MyTask#9', category: {id: 2, name: 'MyCategory#2'}, is_archived: false
    } as Task));
    mockTaskService.updateTask.and.returnValue(of({
      id: 9, name: 'UpdatedTask', category: {id: 3, name: 'MyCategory#3'}, is_archived: false
    } as Task));
    mockTaskService.createTask.and.returnValue(of({
      id: 9, name: 'NewTask', category: {id: 1, name: 'MyCategory#1'}, is_archived: false
    } as Task));
    mockRoute = jasmine.createSpyObj('', {}, {
      'paramMap': of( new Map([['id', '9']]))
    });
    mockCategoryService = jasmine.createSpyObj(['getCategories']);
    mockCategoryService.getCategories.and.returnValue(of(existedCategories));

    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterTestingModule.withRoutes(
          // Redirect after creation
          [{path: 'tasks/9', redirectTo: ''}]
        ),
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
        MatCheckboxModule,
      ],
      declarations: [TaskFormComponent],
      providers: [
        {
          provide: TaskService,
          useValue: mockTaskService,
        },
        {
          provide: CategoryService,
          useValue: mockCategoryService,
        },
        {
          provide: ActivatedRoute,
          useValue: mockRoute,
        },
      ],
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskFormComponent);
    component = fixture.componentInstance;
    inputId = fixture.nativeElement.querySelector('#id');
    inputName = fixture.nativeElement.querySelector('#name');
    inputCategory = fixture.nativeElement.querySelector('#category_id');
    submitButton = fixture.nativeElement.querySelector('#task-submit');
    // TODO: is_archived

    inject([OverlayContainer], (oc: OverlayContainer) => {
        containerElement = oc.getContainerElement();
    })();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show existed task', waitForAsync(() => {
    fixture.detectChanges();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      expect(inputId.value).toEqual('9');
      expect(inputName.value).toEqual('MyTask#9');
      expect(inputCategory.textContent).toEqual('MyCategory#2');
    });
  }));

  it('should show categories on click categories list', waitForAsync(() => {
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

  it('should show option \'Loading...\' when categories being loading', waitForAsync(() => {
    mockCategoryService.getCategories.and.returnValue(of(null));
    fixture.detectChanges();

    inputCategory.click();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      let options = Array.from(
        containerElement.querySelectorAll('mat-option') as NodeListOf<HTMLElement>
      );

      expect(options).toHaveSize(1);
      expect(options[0].textContent.trim()).toEqual('Loading...');
    });
  }));

  it('should show empty elements for new task', waitForAsync(() => {
    fixture.detectChanges();
    component.task = null;
    fixture.detectChanges();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      expect(inputId.value).toEqual('');
      expect(inputName.value).toEqual('');
      expect(inputCategory.textContent).toEqual('');
    });
  }));

  it('should show option \`No categories have been created yet.\'', waitForAsync(() => {
    component.task = null;
    mockCategoryService.getCategories.and.returnValue(of([]));
    fixture.detectChanges();

    inputCategory.click();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      let options = Array.from(
        containerElement.querySelectorAll('mat-option') as NodeListOf<HTMLElement>
      );

      expect(options).toHaveSize(1);
      expect(options[0].textContent.trim()).toEqual('No categories have been created yet.');
    });
  }));

  it('should create new task on submit', waitForAsync(() => {
    fixture.detectChanges();
    component.task = null;
    // Open categories drop-down list
    inputCategory.click();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      // Update name
      inputName.value = 'NewTask';
      inputName.dispatchEvent(new Event('input'));
      // Update category (select option)
      let options = Array.from(
        containerElement.querySelectorAll('mat-option') as NodeListOf<HTMLElement>
      );
      options[0].click();
      inputCategory.dispatchEvent(new Event('selectionChange'));

      submitButton.click();

      expect(mockTaskService.createTask).toHaveBeenCalledOnceWith({
        name: 'NewTask',
        category: {
          id: 1,
          name: 'MyCategory#1',
        }
      } as Task);
    });
  }));

  it('should update existed task on submit', waitForAsync(() => {
    fixture.detectChanges();
    // Open categories drop-down list
    inputCategory.click();
    fixture.detectChanges();

    fixture.whenStable().then(() => {
      fixture.detectChanges();
      // Update name
      inputName.value = 'UpdatedTask';
      inputName.dispatchEvent(new Event('input'));
      // Update category (select option)
      let options = Array.from(
        containerElement.querySelectorAll('mat-option') as NodeListOf<HTMLElement>
      );
      options[2].click();

      submitButton.click();

      expect(mockTaskService.updateTask).toHaveBeenCalledOnceWith({
        id: 9,
        name: 'UpdatedTask',
        category: {
          id: 3,
          name: 'MyCategory#2', // FIXME
        },
        is_archived: false,
      } as Task);
    });
  }));
});
