from google.api_core.datetime_helpers import DatetimeWithNanoseconds
import datetime

tz_jst = datetime.timezone(datetime.timedelta(hours=9), name='JST')


def to_datetime(ts: DatetimeWithNanoseconds) -> datetime:
    """
    DatetimeWithNanosecondsをdatetimeに変換
    """
    return datetime.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second, ts.microsecond, tzinfo=tz_jst) + datetime.timedelta(hours=9)
