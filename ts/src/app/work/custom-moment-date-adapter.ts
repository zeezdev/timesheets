import {Inject, Injectable, Optional} from "@angular/core";
import {MAT_MOMENT_DATE_ADAPTER_OPTIONS, MomentDateAdapter} from "@angular/material-moment-adapter";
import {MAT_DATE_LOCALE} from "@angular/material/core";
import {SettingsCache} from "../settings/services/settings.service";


@Injectable()
export class CustomMomentDateAdapter extends MomentDateAdapter {
  constructor(
    @Optional() @Inject(MAT_DATE_LOCALE) dateLocale: string,
    @Optional() @Inject(MAT_MOMENT_DATE_ADAPTER_OPTIONS) options: any,
    private settingsCache: SettingsCache,
  ) {
    super(dateLocale, options);
  }

  override getFirstDayOfWeek(): number {
    return this.settingsCache.getFirstDayOfWeek();
  }
}
