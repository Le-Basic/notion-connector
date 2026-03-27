import duckdb
import pandas as pd
from .tasks import fetch_bricks
from .roles import populate_role_title
from .business_days import add_business_days_count, compute_tasks_days
from .projects import populate_project_fields
from .people import populate_accountables
from .precomputed import compute_bricks_precomputed_fields
from upload import upload_as_csv
import datetime


def create_models() -> None:
    con = duckdb.connect("notion.duckdb")

    df_bricks = fetch_bricks(con)
    df_bricks = populate_role_title(df_bricks, con)

    df_bricks = add_business_days_count(df_bricks)
    df_bricks_with_people = populate_accountables(df_bricks, con)
    df_bricks_with_project = populate_project_fields(df_bricks_with_people, con)
    df_bricks_filtered = filter_bricks(df_bricks_with_project)
    df_bricks_with_all_fields = compute_bricks_precomputed_fields(df_bricks_filtered)
    df_bricks_days = compute_tasks_days(df_bricks_with_all_fields)
    df_infos = create_df_infos()

    upload_as_csv(df_bricks_with_all_fields, "bricks.csv")
    upload_as_csv(df_bricks_days, "bricks_days.csv")
    upload_as_csv(df_infos, "dump_infos.csv")


def filter_bricks(df_bricks: pd.DataFrame) -> pd.DataFrame:
    df_bricks_without_over = df_bricks[
        ~(df_bricks["notion_task_status"].isin(["Annulé", "Terminé"]))
    ]
    inactive_project_statuses = [
        "Prospection",
        "TdR en cours",
        "Début de négociation",
        "Fin de négociation",
        "Dead",
        "Fini",
    ]
    df_bricks_without_inactive_projects = df_bricks_without_over[
        ~(df_bricks_without_over["project_status"].isin(inactive_project_statuses))
    ]
    return df_bricks_without_inactive_projects


def create_df_infos():
    return pd.DataFrame(
        [[1, str(datetime.datetime.now())]], columns=["id", "Update time"]
    )
