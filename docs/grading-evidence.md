# Individual Evidence Checklist

Use this checklist for the final individual submission. Save screenshots under `docs/evidence/` and paste the final paths into `docs/blueprint-template.md`.

## 1. Required Screenshots

| Evidence | Screenshot path placeholder | What it must show | Rubric mapping |
|---|---|---|---|
| Validate logs score | `docs/evidence/validate-logs-100.png` | `Estimated Score: 100/100` from `python scripts\validate_logs.py` | Group A1: auto-verified implementation |
| Langfuse trace list | `docs/evidence/langfuse-trace-list.png` | At least 10 traces from `/chat` requests | Group A1: Logging & Tracing, Passing Criteria |
| Langfuse trace waterfall | `docs/evidence/langfuse-trace-waterfall.png` | One full trace with `LabAgent.run`, `retrieve`, and `generate` spans | Group A1, A2: tracing and incident debugging |
| Correlation ID logs | `docs/evidence/correlation-id.png` | JSON log lines with `correlation_id`, ideally matching `x-request-id` | Group A1: JSON schema and correlation ID |
| PII redaction logs | `docs/evidence/pii-redaction.png` | Log line where email/phone/card is replaced with `[REDACTED_*]` | Group A1: Alerts & PII |
| Dashboard 6 panels | `docs/evidence/dashboard-6-panels.png` | Latency, traffic, error rate, cost, tokens, quality | Group A1: Dashboard & SLO |
| Alert rules | `docs/evidence/alert-rules.png` | 3 alert rules and runbook links | Group A1: Alerts & PII |
| Incident before/after | `docs/evidence/rag-slow-before-after.png` | Baseline latency vs `rag_slow` latency spike and recovery | Group A2: Incident Response |

## 2. File Evidence

| File | What it proves | Rubric mapping |
|---|---|---|
| `app/middleware.py` | Request-scoped correlation ID, context clearing, response headers | Group A1: Logging & Tracing |
| `app/main.py` | Log enrichment with `user_id_hash`, `session_id`, `feature`, `model`, `env` | Group A1: Logging & Tracing |
| `app/logging_config.py` | JSONL logging and registered PII scrubbing processor | Group A1: Logging & PII |
| `app/pii.py` | PII patterns for email, VN phone, CCCD, credit card, passport, address | Group A1: Alerts & PII |
| `app/tracing.py` | Langfuse tracing support and fallback behavior | Group A1: Logging & Tracing |
| `app/mock_rag.py` | `rag_slow` incident injection and `retrieve` trace span | Group A2: Incident Response |
| `app/mock_llm.py` | LLM generation trace span and `cost_spike` behavior | Group A1/A2 |
| `app/metrics.py` | Metrics for all 6 dashboard panels and SLO/alert fields | Group A1: Dashboard & SLO |
| `config/slo.yaml` | SLO targets for latency, error rate, cost, quality | Group A1: Dashboard & SLO |
| `config/alert_rules.yaml` | 3 alert rules with runbook links | Group A1: Alerts |
| `docs/alerts.md` | Runbook steps for latency, error rate, and cost alerts | Group A1/A2 |
| `docs/dashboard-spec.md` | 6-panel dashboard checklist and metric mapping | Group A1: Dashboard |
| `docs/blueprint-template.md` | Individual report, incident RCA, evidence links | Individual B1: Report Quality |
| `tests/test_pii.py` | Automated PII scrubbing checks | Group A1 and Individual B1 |

## 3. Commands Already Run

Record these in the report or demo notes.

```powershell
python -m pytest
```

Observed result:

```text
7 passed
```

```powershell
python scripts\validate_logs.py
```

Observed result:

```text
Estimated Score: 100/100
Potential PII leaks detected: 0
```

Manual/TestClient checks already performed:

```text
GET /health returned x-request-id and x-response-time-ms headers.
POST /chat generated enriched request_received and response_sent logs.
tool_fail generated enriched request_failed logs.
PII requests generated redacted logs for email, phone, CCCD, credit card, passport, and address.
rag_slow increased latency from about 150ms to about 2650ms.
```

## 4. Demo Commands To Run Live

Start the app:

```powershell
uvicorn app.main:app --reload
```

Generate normal traffic:

```powershell
python scripts\load_test.py --concurrency 1
```

Generate enough traces for passing criteria:

```powershell
python scripts\load_test.py --concurrency 5
```

Check metrics:

```powershell
curl http://127.0.0.1:8000/metrics
```

Enable and test `rag_slow`:

```powershell
python scripts\inject_incident.py --scenario rag_slow
python scripts\load_test.py --concurrency 5
curl http://127.0.0.1:8000/metrics
```

Disable incident:

```powershell
python scripts\inject_incident.py --scenario rag_slow --disable
```

Validate final logs:

```powershell
python scripts\validate_logs.py
```

## 5. Rubric Mapping

### Group Score - 60 pts

| Rubric item | Evidence to submit |
|---|---|
| A1 Logging & Tracing - 10 pts | `validate_logs.py` 100/100, `correlation-id.png`, `langfuse-trace-list.png`, `langfuse-trace-waterfall.png`, files `app/middleware.py`, `app/main.py`, `app/tracing.py` |
| A1 Dashboard & SLO - 10 pts | `dashboard-6-panels.png`, `/metrics` output, `config/slo.yaml`, `docs/dashboard-spec.md` |
| A1 Alerts & PII - 10 pts | `pii-redaction.png`, `alert-rules.png`, `config/alert_rules.yaml`, `docs/alerts.md`, `tests/test_pii.py` |
| A2 Incident Response - 10 pts | `rag-slow-before-after.png`, Langfuse waterfall showing slow `retrieve`, logs with `incident_enabled`, report section `[ROOT_CAUSE_PROVED_BY]` |
| A3 Live Demo - 20 pts | App running, load test output, `/metrics`, incident enable/disable commands, clear explanation of middleware and logging pipeline |

### Individual Score - 40 pts

| Rubric item | Evidence to submit |
|---|---|
| B1 Individual Report - 20 pts | Completed `docs/blueprint-template.md` with all TODO placeholders replaced before submission |
| B2 Git Evidence - 20 pts | Commit hash, PR URL, or Git history showing changes across app, config, docs, and tests |

## 6. Final TODO Before Submission

- [ ] Paste repository URL into `[REPO_URL]`.
- [ ] Run load test until Langfuse shows at least 10 traces.
- [ ] Fill `[TOTAL_TRACES_COUNT]`.
- [ ] Capture all required screenshots into `docs/evidence/`.
- [ ] Paste screenshot paths into `docs/blueprint-template.md`.
- [ ] Paste one Langfuse trace ID or log timestamp into `[ROOT_CAUSE_PROVED_BY]`.
- [ ] Paste commit hash or PR URL into `[EVIDENCE_LINK]`.
- [ ] Run `python -m pytest`.
- [ ] Run `python scripts\validate_logs.py`.
