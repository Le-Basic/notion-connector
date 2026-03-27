import pandas as pd
import os
from pathlib import Path
from .connection import client

sharepoint_folder_path = "3%20-%20POLE%20DONNEES/Z%20-%20Divers%20Code%20et%20Programmation/Notion-connector/data"
local_folder = "exports"


def upload_as_csv(df: pd.DataFrame, file_name: str) -> None:
    Path(local_folder).mkdir(parents=True, exist_ok=True)
    _export_to_csv(df, file_name)
    _upload_csv(file_name)


def _export_to_csv(df: pd.DataFrame, file_name: str) -> None:
    df.loc[
        :,
        ~df.columns.isin(["dlt_id"]),
    ].to_csv(_get_local_csv_path(file_name), index=False)


def _upload_csv(file_name: str):
    local_path = _get_local_csv_path(file_name)
    target_folder = _get_target_folder()
    try:
        with open(local_path, "rb") as f:
            target_folder.upload_file(f).execute_query()
        print("File {0} has been uploaded".format(file_name))
    except Exception as e:
        print(f"Couldn't upload file {file_name}. Error : ${e}")


def _get_target_folder():
    site = _get_shared_file_site()
    root_folder = site.drive.root
    return root_folder.get_by_path(sharepoint_folder_path).get().execute_query()


def _get_shared_file_site():
    sites = client.sites.get().execute_query()
    return [
        site
        for site in sites
        if site.web_url == "https://lebasic.sharepoint.com/sites/Basic_shared_files"
    ][0]


def download_files(remote_folder, local_path):
    drive_items = remote_folder.children.get().execute_query()
    for drive_item in drive_items:
        if drive_item.file is not None:  # is file?
            # download file content
            with open(os.path.join(local_path, drive_item.name), "wb") as local_file:
                drive_item.download(local_file).execute_query()


def _get_local_csv_path(file_name: str):
    return f"{local_folder}/{file_name}"
