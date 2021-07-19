from google.api_core.datetime_helpers import DatetimeWithNanoseconds
import datetime

td_jst = datetime.timedelta(hours=9)
tz_jst = datetime.timezone(td_jst, name='JST')


def to_datetime(ts: DatetimeWithNanoseconds) -> datetime:
    """
    DatetimeWithNanosecondsをdatetimeに変換
    """
    return datetime.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second, ts.microsecond, tzinfo=tz_jst) + td_jst
