from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/v1/debug", tags=["debug"])


def generate_html_table(data: list[dict], title: str) -> str:
    if not data:
        return f"<h3>{title}</h3><p><i>No data found</i></p>"

    headers = data[0].keys()
    rows = [
        "<tr>" + "".join(f"<td>{row.get(h, '')}</td>" for h in headers) + "</tr>"
        for row in data
    ]
    return f"""
    <h3 style='margin-top:2em;color:#2c3e50'>{title}</h3>
    <div style='overflow-x:auto;'>
    <table class='debug-table'>
        <thead><tr>{"".join(f"<th>{h}</th>" for h in headers)}</tr></thead>
        <tbody>{"".join(rows)}</tbody>
    </table>
    </div>
    <hr/>
    """


@router.get("/viewer", response_class=HTMLResponse)
async def debug_viewer(request: Request):
    repos = request.app.state.repos
    html = "<h2 style='color:#2980b9'>🛠️ YAML Repo Viewer</h2>"

    for name in ["member", "module", "product", "mapping"]:
        repo = repos[name]
        data = [item.model_dump() for item in repo]
        html += generate_html_table(data, name.title())

    return f"""
    <html>
    <head>
    <title>Debug Viewer</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f8f9fa; color: #222; }}
    h2 {{ margin-bottom: 1em; }}
    .debug-table {{
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        background: #fff;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px #0001;
        margin-bottom: 2em;
    }}
    .debug-table th, .debug-table td {{
        padding: 8px 14px;
        text-align: left;
    }}
    .debug-table th {{
        background: #2980b9;
        color: #fff;
        font-weight: 600;
    }}
    .debug-table tr:nth-child(even) {{ background: #f2f6fa; }}
    .debug-table tr:hover {{ background: #eaf6ff; }}
    @media (max-width: 700px) {{
        .debug-table th, .debug-table td {{ padding: 6px 8px; font-size: 13px; }}
        h2 {{ font-size: 1.2em; }}
    }}
    </style>
    </head>
    <body style='padding: 20px;'>
    {html}
    </body>
    </html>
    """
