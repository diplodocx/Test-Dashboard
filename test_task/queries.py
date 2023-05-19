import pandas as pd

DB_URI = "sqlite:///../testDB.db"


def read_data():
    df = pd.read_sql('sources', DB_URI)
    df['shift_day'] = df['shift_day'].apply(format_date)
    df['state_begin'] = df['state_begin'].apply(format_time)
    df['state_end'] = df['state_end'].apply(format_time)
    return df


def format_date(date):
    return date.strftime('%Y-%m-%d')


def format_time(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')