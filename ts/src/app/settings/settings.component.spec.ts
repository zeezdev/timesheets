import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import { FormsModule } from '@angular/forms';

import { SettingsComponent } from './settings.component';
import { SettingsCache, SettingsService } from './services/settings.service';
import { NotificationService } from '../shared/notification.service';
import { Settings } from './services/settings';

describe('SettingsComponent', () => {
  let component: SettingsComponent;
  let fixture: ComponentFixture<SettingsComponent>;
  let settingsCacheMock: any;
  let settingsServiceMock: any;
  let notificationServiceMock: any;
  let settingsSubject: Subject<Settings>;

  const mockSettings: Settings = {
    first_day_of_week: 1,
    first_day_of_month: 1
  };

  beforeEach(async () => {
    settingsSubject = new Subject<Settings>();
    settingsCacheMock = {
      settings$: settingsSubject.asObservable()
    };
    settingsServiceMock = {
      saveSettings: jasmine.createSpy('saveSettings').and.returnValue(of(mockSettings))
    };
    notificationServiceMock = {
      success: jasmine.createSpy('success')
    };

    await TestBed.configureTestingModule({
      imports: [FormsModule],
      declarations: [ SettingsComponent ],
      providers: [
        { provide: SettingsCache, useValue: settingsCacheMock },
        { provide: SettingsService, useValue: settingsServiceMock },
        { provide: NotificationService, useValue: notificationServiceMock }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SettingsComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  it('should subscribe to settings on init', () => {
    fixture.detectChanges();
    settingsSubject.next(mockSettings);
    expect(component.settings).toEqual(mockSettings);
  });

  it('should call saveSettings and show notification on submit', () => {
    component.settings = { ...mockSettings };
    const formMock = { valid: true };
    component.onSubmit(formMock);
    expect(settingsServiceMock.saveSettings).toHaveBeenCalledWith({
      first_day_of_week: mockSettings.first_day_of_week,
      first_day_of_month: mockSettings.first_day_of_month
    });
    expect(notificationServiceMock.success).toHaveBeenCalledWith('Settings updated successfully.');
  });

  it('should update first_day_of_month and mark as touched if not touched', () => {
    component.settings = { ...mockSettings };
    const firstDayOfMonthMock = { control: { touched: false, markAsTouched: jasmine.createSpy('markAsTouched') } };
    component.onChangeFirstDayOfMonth(5, firstDayOfMonthMock);
    expect(component.settings.first_day_of_month).toBe(5);
    expect(firstDayOfMonthMock.control.markAsTouched).toHaveBeenCalled();
  });

  it('should not mark as touched if already touched', () => {
    component.settings = { ...mockSettings };
    const firstDayOfMonthMock = { control: { touched: true, markAsTouched: jasmine.createSpy('markAsTouched') } };
    component.onChangeFirstDayOfMonth(10, firstDayOfMonthMock);
    expect(component.settings.first_day_of_month).toBe(10);
    expect(firstDayOfMonthMock.control.markAsTouched).not.toHaveBeenCalled();
  });

  describe('getErrorMessageForFirstDayOfMonth', () => {
    it('should return empty string if no errors', () => {
      expect(component.getErrorMessageForFirstDayOfMonth(null)).toBe('');
    });
    it('should return required message', () => {
      expect(component.getErrorMessageForFirstDayOfMonth({ required: true })).toBe('This field is required.');
    });
    it('should return min message', () => {
      expect(component.getErrorMessageForFirstDayOfMonth({ min: { min: 1 } })).toBe('Value cannot be less than 1.');
    });
    it('should return max message', () => {
      expect(component.getErrorMessageForFirstDayOfMonth({ max: { max: 31 } })).toBe('Value cannot be greater than 31.');
    });
    it('should return default message', () => {
      expect(component.getErrorMessageForFirstDayOfMonth({ other: true })).toBe('Invalid value.');
    });
  });
});
