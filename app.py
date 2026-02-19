from __future__ import annotations

import html
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from agents.runtime.cli import _run_single
from agents.runtime.implementations import AGENT_REGISTRY
from agents.runtime.models import TaskIntake

HOME_PATHS = {"/", "/index.html", "/preview", "/preview/"}


def _to_bool(form: dict[str, list[str]], key: str) -> bool:
    return key in form


def _first(form: dict[str, list[str]], key: str, default: str = "") -> str:
    values = form.get(key)
    return values[0] if values else default


def _build_intake(form: dict[str, list[str]], agent: str) -> TaskIntake:
    return TaskIntake(
        request_id=_first(form, "request_id", "WEB-REQ"),
        date=_first(form, "date", ""),
        requested_by=_first(form, "requested_by", ""),
        agent=agent,
        priority=_first(form, "priority", "Medium"),
        goal=_first(form, "goal", ""),
        context=_first(form, "context", ""),
        constraints=_first(form, "constraints", ""),
        structured_data=_first(form, "structured_data", ""),
        unstructured_notes=_first(form, "unstructured_notes", ""),
        output_format=_first(form, "output_format", "markdown"),
        contains_health_data=_to_bool(form, "contains_health_data"),
        external_communication=_to_bool(form, "external_communication"),
        needs_supervisor_approval=_to_bool(form, "needs_supervisor_approval"),
    )


def render_page(result: str = "") -> str:
    options = "".join([f'<option value="{k}">{k}</option>' for k in AGENT_REGISTRY])
    output_block = f"<h2>Output</h2><pre>{html.escape(result)}</pre>" if result else ""
    return f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Maharishi Agents Webapp</title>
<style>
body {{ font-family: Arial; max-width: 1000px; margin: 1rem auto; padding: 0 1rem; }}
textarea,input,select {{ width: 100%; margin: .25rem 0 .75rem; padding: .5rem; }}
pre {{ background:#111; color:#f5f5f5; padding:1rem; border-radius:8px; white-space:pre-wrap; }}
button {{ padding:.6rem 1rem; }}
small {{ color:#666; }}
</style></head>
<body>
<h1>Maharishi Mission Agents</h1>
<small>If preview opens /preview, this app supports it directly.</small>
<form method="post" action="/">
<label>Agent</label>
<select name="agent"><option value="all">all</option>{options}</select>
<label>Request ID</label><input name="request_id" value="WEB-REQ-001"/>
<label>Date</label><input name="date" value="2026-02-15"/>
<label>Requested By</label><input name="requested_by" value="Program Lead"/>
<label>Priority</label><select name="priority"><option>Low</option><option selected>Medium</option><option>High</option></select>
<label>Goal</label><input name="goal" value="Plan weekly operations and outreach actions"/>
<label>Context</label><textarea name="context" rows="2">Two community programs running in parallel.</textarea>
<label>Constraints</label><textarea name="constraints" rows="2">Small volunteer team, bilingual output needed.</textarea>
<label>Structured Data</label><textarea name="structured_data" rows="2">Task: finalize schedule; Owner: Ravi; Due: Friday</textarea>
<label>Unstructured Notes</label><textarea name="unstructured_notes" rows="2">Need tighter blocker tracking and weekly review cadence.</textarea>
<label>Output Format</label><input name="output_format" value="markdown"/>
<label><input type="checkbox" name="contains_health_data"/> Contains health data</label><br/>
<label><input type="checkbox" name="external_communication" checked/> External communication involved</label><br/>
<label><input type="checkbox" name="needs_supervisor_approval" checked/> Needs supervisor approval</label><br/><br/>
<button type="submit">Run Agent(s)</button>
</form>
{output_block}
</body></html>"""


class AgentWebHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, content: str, content_type: str = "text/html") -> None:
        payload = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self._send(200, '{"status":"ok"}', "application/json")
            return
        if path in HOME_PATHS:
            self._send(200, render_page())
            return
        self._send(404, "Not Found. Try / or /preview", "text/plain")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path not in HOME_PATHS:
            self._send(404, "Not Found. Submit form to /", "text/plain")
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        form = parse_qs(raw)
        selected_agent = _first(form, "agent", "operations")
        intake = _build_intake(form, selected_agent)

        if selected_agent == "all":
            sections = [_run_single(key, intake) for key in AGENT_REGISTRY]
            result = "\n\n---\n\n".join(sections)
        else:
            result = _run_single(selected_agent, intake)

        self._send(200, render_page(result))


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = HTTPServer((host, port), AgentWebHandler)
    print(f"Server running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    run_server(host=host, port=port)
