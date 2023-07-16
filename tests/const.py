from datetime import datetime
from typing import Final


LOCAL_TZ = datetime.now().astimezone().tzinfo
FROZEN_DT: Final[datetime] = datetime(2023, 6, 11, 16, 33, 59, 123456, tzinfo=LOCAL_TZ)
FROZEN_TS: Final[int] = round(FROZEN_DT.timestamp())
