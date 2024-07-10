import os

import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

AUDITIZE_URL = os.environ["AUDITIZE_URL"]
AUDITIZE_APIKEY = os.environ["AUDITIZE_APIKEY"]
AUDITIZE_REPO = os.environ["AUDITIZE_REPO"]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <script type="module" src="{base_url}/auditize-web-component.mjs"></script>
    </head>
    <body>
        <h1 style="text-align: center">Auditize Web Component Demo</h1>
        <auditize-logs
          repo-id="{repo_id}"
          access-token="{access_token}"
          base-url="{base_url}"
        />
    </body>
</html>
"""


def get_access_token():
    resp = requests.post(
        f"{AUDITIZE_URL}/api/auth/access-token",
        json={
            "permissions": {
                "logs": {"repos": [{"repo_id": AUDITIZE_REPO, "read": True}]}
            }
        },
        headers={
            "Authorization": f"Bearer {AUDITIZE_APIKEY}",
        }
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def generate_html():
    access_token = get_access_token()
    return HTML_TEMPLATE.format(
        base_url=AUDITIZE_URL,
        repo_id=AUDITIZE_REPO,
        access_token=access_token,
    )


app = FastAPI()


@app.get("/")
async def index():
    return HTMLResponse(content=generate_html())
