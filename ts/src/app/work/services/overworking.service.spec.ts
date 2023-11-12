import {OverworkingWatcher} from "./overworking.service";
import {WorkService} from "./work.service";

describe('OverworkingWatcher', () => {
  let workService: jasmine.SpyObj<WorkService>;
  let overworkingWatcher: OverworkingWatcher;
  let store = {};

  beforeEach(() => {
    workService = jasmine.createSpyObj('WorkService', ['getWorkReportTotal']);
    overworkingWatcher = new OverworkingWatcher(workService);
    const mockLocalStorage = {
      getItem: (key: string): string => {
        return key in store ? store[key] : null;
      },
      setItem: (key: string, value: string) => {
        store[key] = `${value}`;
      },
      removeItem: (key: string) => {
        delete store[key];
      },
      clear: () => {
        store = {};
      }
    };
    spyOn(localStorage, 'getItem').and.callFake(mockLocalStorage.getItem);
    spyOn(localStorage, 'setItem').and.callFake(mockLocalStorage.setItem);
  });

  it('should return a correct alert key', () => {
    const today = new Date(2023, 11, 12, 18, 46, 32);
    const alertKey = overworkingWatcher['getAlertKey'](today, 85);
    const expectedAlertKey = 'overworkingwatcher-2023-11-12-85';

    expect(alertKey).toEqual(expectedAlertKey);
  });

  it('should set alert key in localStorage', () => {
    const expectedAlertKey = 'overworkingwatcher-2023-11-13-85';
    overworkingWatcher['setAlertKeyInLocalStorage'](expectedAlertKey);

    expect(store[expectedAlertKey]).toEqual('ok');
  });

  it('should get alert key from localStorage', () => {
    const existedAlertKey = 'overworkingwatcher-2023-11-14-90';
    const unexpectedAlertKey = 'overworkingwatcher-2023-11-14-95';
    store[existedAlertKey] = 'ok';

    expect(
      overworkingWatcher['getAlertKeyFromLocalStorage'](existedAlertKey)
    ).toEqual(true);
    expect(
      overworkingWatcher['getAlertKeyFromLocalStorage'](unexpectedAlertKey)
    ).toEqual(false);
  });
});
