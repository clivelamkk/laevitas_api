from datetime import datetime
import pytz
import pandas as pd

def is_option(instrument):
    r = True
    if "-" not in instrument:
        r = False
    else:
        code = instrument.split("-")[-1]
        r = code in ["P", "C"]
    return r

def generate_all_daily_dates(start_date, end_date):
    # Generate all dates from start_date to end_date as a pandas DatetimeIndex
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    # Convert to list of strings in YYYY-MM-DD format
    return date_range.strftime('%Y-%m-%d').tolist()

def to_timestamp(dt_str=None, is_utc=False, unit="ms"):
    """
    hkt to unix timestamp
    dt2=to_timestamp('2025-01-07 09:32:36') #1736242356
    dt1=to_timestamp('2025-01-07 01:32:36', is_utc=True) #1736213556 # HKT 9:32 , so this input is UTC
    assert(dt1==dt2)
    convert_uxtimestamp_to_hkt(dt2) #Timestamp('2025-01-07 09:25:36')
    """
    if dt_str is None:
        dt_str = datetime.now()
    dt = pd.to_datetime(dt_str)
    if unit == "ms":
        multiplier = 1000
    elif unit == "ns":
        multiplier = 1000000000
    if is_utc:
        return int(dt.timestamp() * multiplier)
    else:
        ts = pd.Timestamp(dt, tz="Asia/Hong_Kong").timestamp()
        return int(ts * multiplier)

def convert_to_hkt(dt: datetime, original_tz="US/Eastern"):
    """convert_to_hkt(datetime(2021, 3, 25, 17, 0))"""
    if isinstance(dt, str):
        dt = pd.to_datetime(dt)
    o_tz = pytz.timezone(original_tz)
    return dt.astimezone(tz=o_tz).replace(tzinfo=None)

def convert_uxtimestamp_to_hkt(ts: pd.Timestamp, unit="ms"):
    """
    TEST:
    this should return about time now
    convert_uxtimestamp_to_hkt(to_timestamp(datetime.now()))
    convert_uxtimestamp_to_hkt(1736244000000) # '2025-01-07 18:00:00'
    """
    dt = (
        pd.to_datetime(int(ts), unit=unit, utc=True, errors="coerce")
        .tz_convert("Asia/Hong_Kong")
        .tz_localize(None)
    )
    if pd.isnull(dt):
        return None
    else:
        return dt

def convert_df_uxtimestamp_column(df, column_name, unit="ms"):
    return df.apply(
        lambda x: convert_uxtimestamp_to_hkt(x[column_name], unit=unit), axis=1
    )

def get_dates_since_start(start_dt, end_dt=None, hours=24):
    dates = []
    current_dt = pd.to_datetime(start_dt)
    if end_dt is None:
        end_dt = datetime.now()
    else:
        end_dt = pd.to_datetime(end_dt)
    while current_dt <= end_dt:
        dates.append(current_dt.strftime("%Y-%m-%d %H:%M"))
        current_dt += pd.Timedelta(hours=hours)
    return dates

def convert_option_name(instrument):
    ex = get_option_exchange(instrument)
    result = instrument
    if ex == "BINANCE":
        l = instrument.split("-")
        dt = datetime.strptime(l[1], "%y%m%d").strftime("%d%b%y")
        l[1] = dt
        result = "-".join(l)
    return result

def get_option_exchange(instrument):
    dt = instrument.split("-")[1]
    if dt.isnumeric():
        return "BINANCE"
    else:
        return "DERIBIT"