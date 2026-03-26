import os
from dotenv import load_dotenv
import msal
from office365.graph_client import GraphClient

load_dotenv()
CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
SITE_URL = "https://lebasic.sharepoint.com/sites/Basic_shared_files"


def acquire_token_func():
    """
    Acquire token via MSAL
    """
    authority_url = "https://lebasic.ciamlogin.com"
    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
    )
    token = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    return token


client = GraphClient(token_callback=acquire_token_func, tenant="lebasic")
