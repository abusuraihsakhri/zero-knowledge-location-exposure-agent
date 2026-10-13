# Zero Knowledge Location Exposure Agent

A Python rule-evaluation demonstration with two compatible command-line interfaces, an HMAC-SHA256 in-memory audit chain, a local FastAPI service, and a static browser console.

> **Scope:** Despite its historical name, this repository does **not** implement zero-knowledge proofs, geohash contact matching, blinded Bloom filters, or real clinical exposure estimation. The current domain-specific classes evaluate configurable numeric thresholds and status keywords. Outputs are illustrative, not validated medical decisions.

## Browser console

The static application is in [`web/index.html`](web/index.html). It uses [`web/logic.mjs`](web/logic.mjs) to execute the same three threshold rules as `agents/workers.py`, without a server or Python runtime. Open it through a local static HTTP server:

```bash
python -m http.server 8080
# Visit http://127.0.0.1:8080/web/
```

The page displays a rule-based dossier and supports JSON download. Values stay in memory in your browser; the page does not upload data. **Do not enter personal, location, patient, or other sensitive information.** Downloaded reports are saved locally. A GitHub Pages deployment is provided by the `pages.yml` workflow if repository Pages permissions and deployment settings permit it; live availability must be checked separately.

## Install

Python 3.9 or newer is supported by the package metadata. The project CI checks Python 3.10–3.12.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[server,dev]"
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export API_ACCESS_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

The audit key is mandatory for the primary supervisor. Keep both secrets private, use unique values for each deployment, and never commit them.

## CLI

```bash
python cli.py audit --task-id DEMO-001 --target SYNTHETIC-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
python cli.py chat "What is the system status?"
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
python simulator.py 100
```

The packaged `location-exposure-console` command calls `cli.py`. The historical `zero-knowledge-location-exposure-engine` command and `python zk_contact_trace_app.py` remain available for the legacy `zk_contact_trace` workflow. The primary Python rules trigger elevated status when the primary metric is greater than 25, when the secondary metric is greater than 12, or when selected anomaly keywords appear. A critical flag raises critical urgency.

CSV batch inputs must be within the current working directory. `is_critical_flag` accepts true/false, yes/no, and 1/0; malformed values are rejected. The `verify-audit` command checks **only the current process's in-memory log**, not previously run commands or a durable external ledger.

## Local API

```bash
python cli.py serve --host 127.0.0.1 --port 8000
curl -s http://127.0.0.1:8000/health
curl -s -H "X-API-Key: $API_ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"task_id":"DEMO-001","target_identifier":"SYNTHETIC-01","primary_metric":28.5}' \
  http://127.0.0.1:8000/api/audit
```

Operational routes (`/api/audit`, `/api/chat`, `/api/audit/logs`, `/metrics`) require `X-API-Key` and an `API_ACCESS_TOKEN` of at least 16 characters. `/health` is public. Use a TLS-enabled reverse proxy and proper network access controls for any shared deployment. The API is not intended to process real patient data.

The audit chain verifies HMAC signatures only while the process is alive and does not provide durable/nonrepudiable auditing. Identifier pattern screening is best-effort and is **not** a HIPAA de-identification or PHI assurance system. The `/metrics` endpoint returns JSON counters, not Prometheus text.

## Docker

```bash
# With AUDIT_SECRET_KEY and API_ACCESS_TOKEN already exported:
docker compose up --build
```

Compose binds port 8000 to localhost only, requires both secrets from the environment, and does not embed default production credentials. If the previously committed compose key was used anywhere, rotate it: it remains visible in Git history.

## Tests

```bash
python -m pytest -q
node --test web/logic.test.mjs
```

GitHub Actions runs the Python tests and browser-engine unit tests. No geohash/ZK proof tests are present because those systems are not implemented.

## Technology and licensing

Python, Pydantic 2, FastAPI/Uvicorn (optional API), standard browser JavaScript modules, and Docker. The browser interface targets current evergreen desktop and mobile browsers supporting ES modules. See [LICENSE](LICENSE) for MIT terms.
