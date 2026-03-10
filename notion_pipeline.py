import dlt
import duckdb
from notion import notion_databases


def load_databases() -> None:
    """Loads all databases from a Notion workspace which have been shared with
    an integration.
    """
    pipeline = dlt.pipeline(
        pipeline_name="notion",
        destination="duckdb",
        dataset_name="notion_data",
    )
    selected_database_ids = [
        {"id": "66861714ea264e4cb4c65e1b0f278dde"},
        {"id": "17d6afc9ad648062a313c378efefbf70"},
    ]

    data = notion_databases(database_ids=selected_database_ids)

    info = pipeline.run(data)
    print(info)


def create_model() -> None:
    # load duckdb table
    con = duckdb.connect("notion.duckdb")

    df_taches = con.execute("SELECT * FROM notion_data.t_ches").fetchdf()

    # TODO: filtre les archives et les deletes
    # selectionner les colonnes pertinentes
    df_taches = df_taches.rename(
        columns={
            "_dlt_id": "dlt_id",
            "id": "notion_task_id",
            "url": "notion_task_url",
            "properties__niveau_de_t_che__formula__string": "notion_task_level",
            "properties__etat__status__name": "notion_task_status",
            "properties__p_riode__date__start": "notion_task_start_date",
            "properties__p_riode__date__end": "notion_task_end_date",
            "properties__jours_pass_s__number": "notion_task_days_passed",
            "properties__jours_allou_s__number": "notion_task_days_allocated",
        }
    ).loc[
        :,
        [
            "dlt_id",
            "notion_task_id",
            "notion_task_url",
            "notion_task_level",
            "notion_task_status",
            "notion_task_start_date",
            "notion_task_end_date",
            "notion_task_days_passed",
            "notion_task_days_allocated",
        ],
    ]

    # joindre avec les rôles


if __name__ == "__main__":
    # load_databases()
    create_model()
