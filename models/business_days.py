import duckdb
import pandas as pd


def add_business_days_count(df_tasks: pd.DataFrame) -> pd.DataFrame:
    df_tasks["business_days_count"] = df_tasks.apply(
        lambda row: (
            pd.bdate_range(
                start=row["notion_task_start_date"],
                end=row["notion_task_end_date"],
            ).size
            if pd.notnull(row["notion_task_start_date"])
            and pd.notnull(row["notion_task_end_date"])
            else None
        ),
        axis=1,
    )
    return df_tasks


def compute_tasks_days(df_tasks: pd.DataFrame) -> pd.DataFrame:
    df_calendar = _create_calendar_df(df_tasks)

    df_brick = df_tasks[df_tasks["notion_task_level"] == "Brique"]

    df_task_days = df_brick.merge(df_calendar, how="cross")

    df_task_days = df_task_days[
        (df_task_days["date"] >= df_task_days["notion_task_start_date"])
        & (df_task_days["date"] <= df_task_days["notion_task_end_date"])
    ]
    return df_task_days


def _create_calendar_df(df_tasks: pd.DataFrame) -> pd.DataFrame:
    min_start_date = df_tasks["notion_task_start_date"].min()
    max_end_date = df_tasks["notion_task_end_date"].max()
    dates = pd.date_range(
        start=pd.to_datetime(min_start_date), end=pd.to_datetime(max_end_date), freq="D"
    )

    df_calendar = pd.DataFrame(
        {
            "date": dates,
            "weeknumber": dates.isocalendar().week,
            "year": dates.isocalendar().year,
        }
    )

    df_calendar["is_weekend"] = df_calendar["date"].dt.weekday >= 5
    df_calendar["first_day_of_the_week"] = df_calendar["date"] - pd.to_timedelta(
        df_calendar["date"].dt.weekday, unit="D"
    )

    return df_calendar
