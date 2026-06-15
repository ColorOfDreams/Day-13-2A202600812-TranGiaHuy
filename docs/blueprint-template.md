# Day 13 Observability Lab Report - Individual Submission

> **Instruction**: This report is adapted for an individual submission. The original grading tags are preserved so an automated grading assistant can still parse the file.

## 1. Team Metadata
- [GROUP_NAME]: Individual Submission - Tran Gia Huy
- [REPO_URL]: [PENDING: paste repository URL before submission]
- [MEMBERS]:
  - Member A: Tran Gia Huy | Role: Logging & PII, Tracing & Enrichment, SLO & Alerts, Load Test & Dashboard, Demo & Report
  - Member B: N/A | Role: Covered by Member A
  - Member C: N/A | Role: Covered by Member A
  - Member D: N/A | Role: Covered by Member A
  - Member E: N/A | Role: Covered by Member A

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: [PENDING: fill after Langfuse run, minimum required: 10]
- [PII_LEAKS_FOUND]: 0

Verification command:

```powershell
python scripts\validate_logs.py
```

Latest observed result:

```text
Estimated Score: 100/100
Potential PII leaks detected: 0
```

Evidence screenshot: docs/evidence/validate-logs-100.png

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/evidence/correlation-id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/evidence/pii-redaction.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/evidence/langfuse-trace-waterfall.png
- [TRACE_WATERFALL_EXPLANATION]: The trace waterfall should show the main `LabAgent.run` operation plus child observations for `retrieve` and `generate`. During the `rag_slow` incident, the `retrieve` span is expected to dominate latency, proving that the slowdown is in the RAG retrieval layer rather than the LLM generation layer.

Implementation summary:
- Correlation IDs are handled in `app/middleware.py`. Each request receives an `x-request-id`, either from the incoming header or generated as `req-<8 hex chars>`.
- Structured JSON logs are written through `app/logging_config.py` to `data/logs.jsonl`.
- Request logs are enriched in `app/main.py` with `user_id_hash`, `session_id`, `feature`, `model`, and `env`.
- PII scrubbing is implemented in `app/pii.py` and registered in the structlog processor chain.
- Langfuse tracing helpers are in `app/tracing.py`; `LabAgent.run`, `retrieve`, and `FakeLLM.generate` are instrumented with `@observe()`.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: docs/evidence/dashboard-6-panels.png
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 151.0ms |
| Error Rate | < 2% | 28d | 0.0% |
| Cost Budget | < $2.5/day | 1d | $0.0055 |
| Quality Score Avg | >= 0.75 | 28d | 0.9 |

Required dashboard panels and metric sources:
- Latency P50/P95/P99: `latency_p50_ms`, `latency_p95_ms`, `latency_p99_ms`
- Traffic: `request_count`
- Error rate with breakdown: `error_rate_pct`, `error_breakdown`
- Cost over time: `hourly_cost_usd`, `daily_cost_usd`, `total_cost_usd`
- Tokens in/out: `tokens_in_total`, `tokens_out_total`
- Quality proxy: `quality_score_avg`

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: docs/evidence/alert-rules.png
- [SAMPLE_RUNBOOK_LINK]: docs/alerts.md#1-high-latency-p95

Configured alert rules:
- `high_latency_p95`: triggers when `latency_p95_ms > 5000 for 30m`
- `high_error_rate`: triggers when `error_rate_pct > 5 for 5m`
- `cost_budget_spike`: triggers when `hourly_cost_usd > 2x_baseline for 15m`

Runbook file:
- `docs/alerts.md`

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: After enabling `rag_slow`, request latency increases from the normal baseline of about 150ms to about 2650ms. The `/metrics` endpoint shows elevated `latency_p95_ms`, and `data/logs.jsonl` contains `response_sent` events with high `latency_ms`.
- [ROOT_CAUSE_PROVED_BY]: [PENDING: paste Langfuse Trace ID and/or log line timestamp before submission]. The trace waterfall should show the `retrieve` span taking most of the request time while `generate` remains near normal latency. Logs also show the `incident_enabled` event for `rag_slow` before the slow requests.
- [FIX_ACTION]: Disable the incident with `python scripts\inject_incident.py --scenario rag_slow --disable`. In a real system, mitigation would include fallback retrieval, query truncation, timeout control, or routing to a healthier retrieval source.
- [PREVENTIVE_MEASURE]: Keep latency SLOs and the `high_latency_p95` alert active, inspect RAG spans during tail latency spikes, and add runbook steps for checking retrieval dependencies before changing LLM settings.

Demo commands:

```powershell
uvicorn app.main:app --reload
python scripts\load_test.py --concurrency 1
python scripts\inject_incident.py --scenario rag_slow
python scripts\load_test.py --concurrency 5
curl http://127.0.0.1:8000/metrics
python scripts\inject_incident.py --scenario rag_slow --disable
```

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: Tran Gia Huy completed the full individual implementation: correlation ID middleware, structured log enrichment, PII scrubbing, Langfuse tracing instrumentation, metrics alignment, SLO and alert configuration, dashboard metric mapping, incident injection validation, and report preparation.
- [EVIDENCE_LINK]: [PENDING: paste commit hash, PR URL, or GitHub compare link before submission]

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: N/A - individual submission, all work covered by Member A.
- [EVIDENCE_LINK]: N/A

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: N/A - individual submission, all work covered by Member A.
- [EVIDENCE_LINK]: N/A

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: N/A - individual submission, all work covered by Member A.
- [EVIDENCE_LINK]: N/A

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: N/A - individual submission, all work covered by Member A.
- [EVIDENCE_LINK]: N/A

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: N/A
- [BONUS_AUDIT_LOGS]: N/A
- [BONUS_CUSTOM_METRIC]: Added dashboard-ready aliases in `/metrics`, including `error_rate_pct`, `quality_score_avg`, `daily_cost_usd`, and latency metrics with `_ms` units. Evidence: docs/evidence/metrics-output.png
