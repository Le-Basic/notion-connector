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
    
    # selectionner les colonnes pertinentes


if __name__ == "__main__":
    # load_databases()
    create_model()
