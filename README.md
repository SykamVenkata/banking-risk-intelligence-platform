# 🏦 Retail Banking & Risk Intelligence Platform

> **End-to-end enterprise BI portfolio project** — a parallel reference platform demonstrating the architecture, engineering, and banking domain expertise applied on a Tier-1 banking engagement (Citi, Irving TX).

[![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=white)](https://databricks.com)
[![Microsoft Fabric](https://img.shields.io/badge/Microsoft%20Fabric-0078D4?style=flat&logo=microsoft&logoColor=white)](https://fabric.microsoft.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Azure](https://img.shields.io/badge/Azure-0089D6?style=flat&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)

---

## 📋 Project Overview

A complete retail banking analytics platform built on a **medallion lakehouse architecture**, delivering four executive dashboards covering profitability, credit risk, deposits & lending, and regulatory compliance.

**Key banking metrics delivered:**
`NIM` · `Efficiency Ratio` · `NPL Ratio` · `Delinquency Roll Rates` · `CECL Staging` · `RWA` · `CET1` · `LDR` · `CASA` · `Cost of Funds`

> **Important:** Built on synthetic + public (FDIC) data. No real client data is used. This is a demonstrable reference platform that recreates the class of problem and technical stack of a real Tier-1 banking engagement.

---

## 🏗️ Architecture

```
┌─────────────────── DATA SOURCES ────────────────────────┐
│  FDIC BankFind API (real)  → institution financials      │
│  Kaggle lending (real)     → loan-level credit risk      │
│  Synthetic core banking    → transactions + balances     │
│  Synthetic stream          → near-real-time feed         │
└──────────────────────────┬──────────────────────────────┘
                           │
        ┌──────────────────▼──────────────────┐
        │           BRONZE LAYER              │
        │  Raw landing · Auto Loader          │
        │  Audit columns · Replayable         │
        └──────────────────┬──────────────────┘
                           │  PySpark / Databricks / Fabric
        ┌──────────────────▼──────────────────┐
        │           SILVER LAYER              │
        │  Cleansed · Typed · Deduped         │
        │  DQ quarantine · BCBS 239 lineage   │
        └──────────────────┬──────────────────┘
                           │
        ┌──────────────────▼──────────────────┐
        │            GOLD LAYER               │
        │  Kimball star schema                │
        │  Delinquency roll-rate matrix       │
        │  CECL staging · Z-ORDER optimize    │
        └──────────────────┬──────────────────┘
                           │  Direct Lake / Import
        ┌──────────────────▼──────────────────┐
        │         POWER BI SEMANTIC MODEL     │
        │  42 DAX measures · 13 relationships │
        │  RLS · Deployment Pipelines         │
        └──────────────────┬──────────────────┘
                           │
              ┌────────────▼────────────┐
              │    4 DASHBOARDS         │
              │  Executive · Risk       │
              │  Deposits · Regulatory  │
              └─────────────────────────┘
```

---

## 🗂️ Repository Structure

```
banking-risk-intelligence-platform/
│
├── data/
│   ├── generators/          # Python synthetic data generators
│   │   ├── generate_dimensions.py    # DimDate, Customer, Product, Branch
│   │   └── generate_facts.py         # FactTransaction + streaming sim
│   ├── ingestion/           # Real data source connectors
│   │   └── ingest_fdic.py            # FDIC BankFind API (no key required)
│   └── sample/              # 100-row samples for quick testing
│
├── notebooks/               # PySpark medallion notebooks
│   ├── 01_bronze_ingest.py           # Raw ingestion + Auto Loader
│   ├── 02_silver_transform.py        # Cleanse + DQ + conform
│   ├── 03_gold_star_schema.py        # Kimball star + aggregates
│   └── validate_pipeline.py          # Logic validation (pandas)
│
├── powerbi/                 # Power BI Project (.pbip format)
│   ├── BankingPlatform.pbip          # Open this in Power BI Desktop
│   ├── BankingPlatform.SemanticModel/
│   │   └── definition/
│   │       ├── model.tmdl            # Model settings
│   │       ├── relationships.tmdl   # 13 star-schema relationships
│   │       ├── expressions.tmdl     # DataFolder parameter
│   │       └── tables/              # 12 table TMDL definitions
│   │           └── _Measures.tmdl   # 42 DAX measures (5 display folders)
│   └── BankingPlatform.Report/
│       └── definition/report.json   # 4 report pages defined
│
├── model/
│   ├── measures.dax         # Full DAX measure library (reference)
│   └── validate_measures.py # Validates KPIs produce realistic numbers
│
└── docs/
    ├── PROBLEM_STATEMENT.md # Project charter + 4 problem statements
    ├── DOMAIN_RESEARCH.md   # JD analysis + banking KPI reference
    └── DASHBOARD_SPEC.md    # Exact visuals + fields per page
```

---

## 📊 The Four Dashboards

### 1. Executive Summary *(answers P1: Executive blind spots)*
| KPI | Measure | Realistic Value |
|-----|---------|-----------------|
| Net Interest Margin | `[NIM %]` | 3.08% |
| Efficiency Ratio | `[Efficiency Ratio %]` | 41.7% |
| ROA | `[ROA %]` | ~1.2% |
| Loan-to-Deposit Ratio | `[Loan to Deposit Ratio %]` | 74.3% |

### 2. Risk & Delinquency *(answers P2: Reactive credit risk)*
| KPI | Measure | Realistic Value |
|-----|---------|-----------------|
| NPL Ratio | `[NPL Ratio %]` | 0.39% |
| Roll Rate | `[Roll Rate %]` | ~5.3% |
| ECL Allowance | `[ECL Allowance Proxy]` | CECL-weighted |
| Coverage Ratio | `[Coverage Ratio %]` | 1.13% |

### 3. Deposits & Lending *(answers P3: No single source of truth)*
| KPI | Measure | Realistic Value |
|-----|---------|-----------------|
| CASA Ratio | `[CASA Ratio %]` | 61.2% |
| Cost of Funds | `[Cost of Funds %]` | 2.07% |
| Net Spread | `[Net Spread %]` | ~8% |

### 4. Regulatory View *(answers P4: Manual regulatory aggregation)*
| KPI | Measure | Realistic Value |
|-----|---------|-----------------|
| CET1 Ratio | `[CET1 Ratio %]` | 13.5% |
| Risk-Weighted Assets | `[Risk Weighted Assets]` | Basel standardized |
| AML Flagged Value | `[Flagged Transaction Value]` | ~0.2% of volume |

---

## 🚀 Quick Start

### Option A — Power BI Desktop (CSV import, works immediately)

```bash
# 1. Clone the repo
git clone https://github.com/SykamVenkata/banking-risk-intelligence-platform
cd banking-risk-intelligence-platform

# 2. Generate the full dataset (requires Python 3.8+)
pip install pandas numpy
python data/generators/generate_dimensions.py --out data/full --customers 5000
python data/generators/generate_facts.py --out data/full --months 18

# 3. Open in Power BI Desktop
# Enable: File > Options > Preview features > Power BI Project (.pbip)
# Open: powerbi/BankingPlatform.pbip
# Set DataFolder parameter to: C:\path\to\data\full\
# Refresh → build 4 pages from docs/DASHBOARD_SPEC.md
```

### Option B — Microsoft Fabric (Direct Lake, near-real-time)

```bash
# 1. Upload notebooks to Fabric workspace
# 2. Run in order: 01_bronze → 02_silver → 03_gold
# 3. Set PLATFORM = "fabric" in each notebook
# 4. Create semantic model pointing at Gold Delta tables
# 5. Enable Direct Lake → Automatic page refresh
```

### Option C — Azure Databricks + Power BI

```bash
# 1. Create Azure Databricks workspace
# 2. Upload notebooks (01, 02, 03)
# 3. Set PLATFORM = "databricks" in each notebook
# 4. Run via Databricks Workflows
# 5. Connect Power BI to Databricks SQL endpoint
```

---

## 🔧 Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Ingestion** | PySpark, Auto Loader, Structured Streaming, Azure Data Factory |
| **Storage** | Delta Lake, Azure Data Lake Storage Gen2, OneLake |
| **Transform** | PySpark, Python (pandas), Spark SQL |
| **Modeling** | Kimball Star Schema, SCD, conformed dimensions |
| **Semantic Model** | Power BI TMDL, DAX, Power Query M, Direct Lake |
| **Governance** | Unity Catalog, BCBS 239, SOX 404, RLS, RBAC |
| **Platforms** | Microsoft Fabric, Azure Databricks, Power BI Service |
| **DevOps** | Git, GitHub, Fabric Deployment Pipelines |

---

## 📚 Domain Coverage

**Regulatory Frameworks:** CCAR · DFAST · CECL · IFRS 9 · BCBS 239 · SR 11-7 · Basel III · SOX 404 · AML/KYC

**Banking KPIs:** NIM · NII · ROA · ROE · Efficiency Ratio · NPL · DPD Buckets · Roll Rates · CECL Staging · ECL · RWA · CET1 · LDR · CASA · Cost of Funds · Loan Yield

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**V N K Sykam** — Senior Power BI / BI & Analytics Engineer  
[Portfolio](https://sykamsolutions.com) · [LinkedIn](https://linkedin.com/in/vnksykam) · [GitHub](https://github.com/SykamVenkata)
