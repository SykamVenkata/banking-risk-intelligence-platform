# Project Charter — Retail Banking & Risk Intelligence Platform

> Parallel reference platform built on synthetic + FDIC public data.
> Recreates the class of problem and technical stack of a real Tier-1 banking engagement.

## Overarching Problem Statement

The bank's retail and risk teams lacked a single, governed, near-real-time view of
deposits, lending, and credit risk. Fragmented manual reporting, overnight refresh
latency, and inconsistent KPI definitions slowed monthly business reviews, delayed
risk escalation, and created reconciliation gaps — a BCBS 239 and SOX 404 concern.

## Four Sub-Problems → Four Dashboards

### P1 — Executive blind spots (→ Executive Summary dashboard)
Leaders couldn't see consolidated NIM, efficiency ratio, ROA/ROE, and deposit/loan
growth in one place. Numbers were stitched manually, often inconsistent, arrived late.
Solution: One certified executive scorecard, refreshed near-real-time.

### P2 — Reactive, lagging credit risk (→ Risk & Delinquency dashboard)
Delinquency and roll-rate analysis ran on overnight batches. No consistent DPD bucket
view, NPL ratio, vintage curves, or CECL staging to feed loss forecasting.
Solution: Near-real-time delinquency monitoring with CECL/IFRS 9 staging.

### P3 — No single source of truth (→ Deposits & Lending dashboard)
Deposit growth, CASA, LDR, Cost of Funds lived in separate spreadsheets per region,
making cross-comparison impossible and masking funding risk.
Solution: Conformed deposits-and-lending model spanning all branches + products.

### P4 — Manual regulatory aggregation (→ Regulatory View dashboard)
CCAR schedule and CECL allowance inputs assembled by hand, weak lineage and
reconciliation — a control and audit risk.
Solution: Governed, auditable regulatory aggregates with BCBS 239-aligned lineage.

## Objectives & Success Criteria

| Objective | Target |
|---|---|
| Reduce dashboard load time | ~45% faster via Direct Lake |
| Cut reporting latency | Overnight → minutes (near-real-time) |
| Consolidate legacy reporting | 6 Excel/Access processes → 1 workspace |
| Reduce ad-hoc requests | ~30% fewer |
| Data quality | DQ quarantine + reconciliation Bronze→Gold |
