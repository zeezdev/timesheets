from datetime import datetime
from typing import Final


FROZEN_DT: Final[datetime] = datetime(2023, 6, 11, 16, 33, 59, 123456)
FROZEN_TS: Final[int] = round(FROZEN_DT.timestamp())
DT_FORMAT: Final[str] = '%Y-%m-%dT%H:%M:%S'

