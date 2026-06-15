# Dashboard Spec

Required Layer-2 panels:
1. Latency P50/P95/P99
2. Traffic (request count or QPS)
3. Error rate with breakdown
4. Cost over time
5. Tokens in/out
6. Quality proxy (heuristic, thumbs, or regenerate rate)

Metric mapping from `/metrics`:
- Latency: `latency_p50_ms`, `latency_p95_ms`, `latency_p99_ms`
- Traffic: `request_count`
- Error rate: `error_rate_pct`, `error_breakdown`
- Cost: `hourly_cost_usd`, `daily_cost_usd`, `total_cost_usd`
- Tokens: `tokens_in_total`, `tokens_out_total`
- Quality: `quality_score_avg`

Quality bar:
- default time range = 1 hour
- auto refresh every 15-30 seconds
- visible threshold/SLO line
- units clearly labeled
- no more than 6-8 panels on the main layer
