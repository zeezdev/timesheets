import time
from datetime import tzinfo, datetime, timezone


def get_local_tz() -> tzinfo:
    return datetime.now().astimezone().tzinfo


def dt_to_ts(dt: datetime) -> int:
    """Convert a given datetime into the timestamp in UTC TZ."""
    if dt.tzinfo is None:
        # If dt is a naive (no tzinfo provided) then set up a local tz
        dt_without_tz = dt
        dt_with_tz = dt.replace(tzinfo=get_local_tz())
    else:
        dt_with_tz = dt
        dt_without_tz = dt.replace(tzinfo=None)

    utc_dt = dt_without_tz - dt_with_tz.utcoffset()
    timestamp = time.mktime(utc_dt.timetuple())
    return int(timestamp)


def ts_to_dt(ts: int) -> datetime:
    """Convert UTC ts to local dt."""
    return datetime.fromtimestamp(ts).replace(tzinfo=timezone.utc).astimezone()


def get_now_timestamp() -> int:
    """Return current timestamp in UTC TZ."""
    local_dt = datetime.now()
    utc_dt = local_dt - local_dt.astimezone().utcoffset()
    timestamp = time.mktime(utc_dt.timetuple())
    # TODO: utctimetuple ?
    return int(timestamp)
