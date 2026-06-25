# Power BI Project — Retail Banking & Risk Intelligence Platform (.pbip)

Modern Power BI Project format (TMDL semantic model + report). Open in **Power BI
Desktop** (with *Preview features → Power BI Project (.pbip) save format* enabled).

## What's inside
```
BankingPlatform.pbip                     ← open THIS in Power BI Desktop
BankingPlatform.SemanticModel/           ← the model (TMDL)
  definition/
    model.tmdl, relationships.tmdl, expressions.tmdl
    tables/*.tmdl                         ← 12 tables incl. _Measures (42 measures)
BankingPlatform.Report/                  ← report shell (4 pages defined)
sample_data/*.csv                        ← Gold-layer data the model loads
```

## Setup (2 minutes)
1. Put `sample_data/` somewhere stable, e.g. `C:\BankingPlatform\sample_data\`.
2. Open `expressions.tmdl` and set the **DataFolder** parameter to that path
   (keep the trailing backslash):
   `expression DataFolder = "C:\BankingPlatform\sample_data\" ...`
   (Or, after opening in Desktop: Transform data → Edit Parameters → DataFolder.)
3. Open `BankingPlatform.pbip` in Power BI Desktop → it loads the model + measures.
4. Build the 4 pages following `../docs/DASHBOARD_SPEC.md` (fields/measures are exact;
   you just arrange the visuals).

## Switch to Direct Lake (Fabric) instead of CSV
Replace each table's M `partition` with a Lakehouse/Delta source, or recreate the model
on a Fabric Lakehouse pointing at the Gold Delta tables. The measures are unchanged —
they reference table/column names that match the Gold schema.

## The model at a glance
- **Star schema:** FactTransaction, FactLoanBalance + DimDate/Customer/Account/Product/Branch
- **Aggregates:** AggDailyDeposits, AggMonthlyLoans, AggMonthlyDeposits, AggDelinquencyRoll
- **42 measures** in `_Measures`, foldered by dashboard (Executive / Risk / Deposits & Lending / Regulatory / Near-Real-Time)
- **13 relationships**, single-direction fact→dim
