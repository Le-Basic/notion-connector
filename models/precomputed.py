import datetime
import pandas as pd


def compute_bricks_precomputed_fields(df_bricks: pd.DataFrame) -> pd.DataFrame:
    df_bricks = _compute_fields_presence(df_bricks)
    df_bricks = _compute_less_than_3_months_field(df_bricks)
    df_bricks = _compute_readiness(df_bricks)
    return df_bricks


def _compute_readiness(df_bricks: pd.DataFrame) -> pd.DataFrame:
    df_bricks["is_valid"] = df_bricks.apply(
        lambda row: (
            row["has_periode"]
            and row["has_role"]
            and row["has_allocation"]
            and row["has_responsable"]
        ),
        axis=1,
    )
    return df_bricks


def _compute_fields_presence(df_bricks: pd.DataFrame) -> pd.DataFrame:
    df_bricks["has_periode"] = df_bricks.apply(
        lambda row: (
            pd.notnull(row["notion_task_start_date"])
            and pd.notnull(row["notion_task_end_date"])
        ),
        axis=1,
    )
    df_bricks["has_role"] = df_bricks.apply(
        lambda row: pd.notnull(row["role_title"]),
        axis=1,
    )
    df_bricks["has_allocation"] = df_bricks.apply(
        lambda row: pd.notnull(row["notion_task_days_allocated"]),
        axis=1,
    )
    df_bricks["has_responsable"] = df_bricks.apply(
        lambda row: pd.notnull(row["responsable"]),
        axis=1,
    )
    return df_bricks


def _compute_less_than_3_months_field(df_bricks: pd.DataFrame) -> pd.DataFrame:
    three_months_from_now_ts = pd.Timestamp(
        datetime.datetime.now().date()
    ) + pd.DateOffset(months=3)
    df_bricks["is_in_less_than_3_months"] = df_bricks.apply(
        lambda row: (
            three_months_from_now_ts > row["notion_task_start_date"]
            if pd.notnull(row["notion_task_start_date"])
            else False
        ),
        axis=1,
    )
    return df_bricks
