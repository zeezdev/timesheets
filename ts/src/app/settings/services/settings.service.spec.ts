import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

import { SettingsService } from './settings.service';

describe('SettingsService', () => {
  let service: SettingsService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        SettingsService
      ]
    }).compileComponents();

    service = TestBed.inject(SettingsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
