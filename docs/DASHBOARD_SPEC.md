# Dashboard Build Spec — 4 Pages

After importing the `.pbip` (semantic model loads with all tables, relationships, and
measures), build the four report pages below. Each maps to a problem statement from
`PROBLEM_STATEMENT.md`. Visual positions are yours to arrange; the fields/measures are exact.

> Tip: the measures are pre-organized into **display folders** (0 Foundation, 1 Executive,
> 2 Risk, 3 Deposits & Lending, 4 Regulatory, 5 Near Real-Time) in the `_Measures` table —
> so each page's measures are easy to find.

---

## Page 1 — Executive Summary  (answers P1)

**Goal:** one certified executive scorecard.

**KPI cards (top row):**
| Card | Measure |
|---|---|
| Net Interest Margin | `[NIM %]` |
| Efficiency Ratio | `[Efficiency Ratio %]` |
| ROA | `[ROA %]` |
| Total Deposits | `[Total Deposits]` |
| Total Loans | `[Total Loans]` |
| Net Interest Income | `[Net Interest Income]` |

**Visuals:**
- **Line chart** — Deposit & Loan trend. Axis: `DimDate[MonthYear]` · Values: `[Total Deposits]`, `[Total Loans]`
- **Clustered column** — NII by month. Axis: `DimDate[MonthYear]` · Value: `[Net Interest Income]`
- **Bar chart** — Deposit Growth by Region. Axis: `DimBranch[Region]` · Value: `[Deposit Growth %]`
- **Donut** — Deposit mix by product. Legend: `DimProduct[ProductName]` (Deposit only) · Value: `[Total Deposits]`

**Slicers:** `DimDate[Year]`, `DimDate[Quarter]`, `DimBranch[Region]`

---

## Page 2 — Risk & Delinquency  (answers P2)

**Goal:** near-real-time credit-risk monitoring.

**KPI cards:**
| Card | Measure |
|---|---|
| NPL Ratio | `[NPL Ratio %]` |
| Delinquency Rate | `[Delinquency Rate %]` |
| Roll Rate | `[Roll Rate %]` |
| ECL Allowance | `[ECL Allowance Proxy]` |
| Coverage Ratio | `[Coverage Ratio %]` |

**Visuals:**
- **Stacked column (100%)** — DPD bucket mix over time. Axis: `DimDate[MonthYear]` · Legend: `FactLoanBalance[DelinquencyBucket]` · Value: `[Total Loans]`
- **Matrix** — Roll-rate matrix. Rows: `AggDelinquencyRoll[PrevBucket]` · Columns: `AggDelinquencyRoll[DelinquencyBucket]` · Values: `SUM(AggDelinquencyRoll[BalanceMoved])`
- **Donut** — CECL staging. Legend: `FactLoanBalance[CECLStage]` · Values: `[Stage 1 Balance]`, `[Stage 2 Balance]`, `[Stage 3 Balance]`
- **Bar** — NPL Ratio by LOB. Axis: `DimProduct[LineOfBusiness]` · Value: `[NPL Ratio %]`
- **Table** — High-risk customers. `DimCustomer[CustomerID]`, `DimCustomer[RiskBand]`, `DimCustomer[CreditScore]`, `[NPL Balance]`

**Slicers:** `DimCustomer[RiskBand]`, `DimProduct[LineOfBusiness]`, `DimDate[MonthYear]`

---

## Page 3 — Deposits & Lending  (answers P3)

**Goal:** single source of truth for deposits & lending.

**KPI cards:**
| Card | Measure |
|---|---|
| Loan-to-Deposit Ratio | `[Loan to Deposit Ratio %]` |
| CASA Ratio | `[CASA Ratio %]` |
| Cost of Funds | `[Cost of Funds %]` |
| Loan Yield | `[Loan Yield %]` |
| Net Spread | `[Net Spread %]` |

**Visuals:**
- **Line + clustered column combo** — Deposits (column) vs LDR (line) by month
- **Treemap** — Deposit balance by product. Group: `DimProduct[ProductName]` · Value: `[Total Deposits]`
- **Bar** — Branch performance. Axis: `DimBranch[BranchName]` · Value: `[Total Deposits]` (Top N 10)
- **Map** — Deposits by Region. Location: `DimBranch[Region]` · Bubble size: `[Total Deposits]`
- **Bar** — Loan Yield vs Cost of Funds by LOB

**Slicers:** `DimProduct[ProductCategory]`, `DimBranch[Region]`, `DimCustomer[CustomerSegment]`

---

## Page 4 — Regulatory View  (answers P4)

**Goal:** governed, auditable regulatory aggregates.

**KPI cards:**
| Card | Measure |
|---|---|
| Risk-Weighted Assets | `[Risk Weighted Assets]` |
| CET1 Ratio | `[CET1 Ratio %]` |
| Total Exposure | `[Total Exposure]` |
| Flagged (AML) Value | `[Flagged Transaction Value]` |
| Flagged Count | `[Flagged Transaction Count]` |

**Visuals:**
- **Bar** — RWA by Line of Business. Axis: `DimProduct[LineOfBusiness]` · Value: `[Risk Weighted Assets]`
- **Matrix** — CCAR-style exposure schedule. Rows: `DimProduct[LineOfBusiness]` · Columns: `FactLoanBalance[CECLStage]` · Values: `[Total Exposure]`, `[ECL Allowance Proxy]`
- **Gauge** — CET1 Ratio vs 4.5% regulatory minimum. Value: `[CET1 Ratio %]` · Target: 0.045
- **Table** — AML flagged transactions. `FactTransaction[TransactionType]`, `DimBranch[Region]`, `[Flagged Transaction Value]`, `[Flagged Transaction Count]`

**Slicers:** `DimProduct[LineOfBusiness]`, `DimDate[Quarter]`

---

## Near-Real-Time strip (any page footer)
- **Card** — `[Last Transaction Time]`  ("Data as of …")
- **Card** — `[Txns Last Hour]`
- **Card** — `[Net Flow Today]`
- Set page/visual refresh: enable **Automatic page refresh** (in Power BI Service / Direct Lake)
  so the near-real-time feed updates these live.

---

## Suggested theme (matches your portfolio)
- Accent: cyan `#0891B2` → violet `#7C3AED`
- Background: light `#F4F7FB`, cards white with soft shadow
- One agreed font (Segoe UI / your portfolio's Lexend feel)
