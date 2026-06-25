# Medallion Notebooks

Run in this order on Databricks or Microsoft Fabric:

| # | Notebook | Layer | What it does |
|---|----------|-------|-------------|
| 01 | `01_bronze_ingest.py` | Bronze | Raw ingestion + Auto Loader streaming |
| 02 | `02_silver_transform.py` | Silver | Cleanse + DQ + conform |
| 03 | `03_gold_star_schema.py` | Gold | Kimball star + delinquency roll-rate + CECL |
| - | `validate_pipeline.py` | Local | Validates KPIs (pandas, no Spark needed) |

## Platform Switch

Each notebook has at the top:
```python
PLATFORM = "databricks"  # or "fabric"
```
This controls catalog paths and storage locations. Everything else is identical.

## Running on Databricks
1. Upload notebooks to your Workspace
2. Attach to a cluster (DBR 13.3 LTS or later)
3. Set PLATFORM = "databricks"
4. Run 01 → 02 → 03

## Running on Microsoft Fabric
1. Upload notebooks to your Fabric workspace
2. Attach to a Lakehouse
3. Set PLATFORM = "fabric"
4. Run 01 → 02 → 03
