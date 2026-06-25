"""
Retail Banking & Risk Intelligence Platform
============================================
Synthetic DIMENSION generator.

Produces conformed dimensions for a Kimball star schema:
  DimDate, DimCustomer, DimAccount, DimProduct, DimBranch

100% synthetic data — safe for public portfolio use.

Usage:
    python generate_dimensions.py --out ../../data/full --customers 5000
"""
import argparse, os, random
from datetime import date, timedelta
import numpy as np
import pandas as pd

RNG_SEED = 42
random.seed(RNG_SEED)
np.random.seed(RNG_SEED)

# ── DimDate ──────────────────────────────────────────────────────────────────
def build_dim_date(start="2023-01-01", end="2025-12-31"):
    start_d, end_d = date.fromisoformat(start), date.fromisoformat(end)
    rows = []
    for i in range((end_d - start_d).days + 1):
        d = start_d + timedelta(days=i)
        rows.append({
            "DateKey":    int(d.strftime("%Y%m%d")),
            "Date":       d.isoformat(),
            "Year":       d.year,
            "Quarter":    f"Q{(d.month-1)//3+1}",
            "QuarterNo":  (d.month-1)//3+1,
            "Month":      d.month,
            "MonthName":  d.strftime("%B"),
            "MonthYear":  d.strftime("%b %Y"),
            "Day":        d.day,
            "DayOfWeek":  d.strftime("%A"),
            "IsWeekend":  d.weekday() >= 5,
            "IsMonthEnd": (d + timedelta(days=1)).month != d.month,
        })
    return pd.DataFrame(rows)

# ── DimBranch ─────────────────────────────────────────────────────────────────
REGIONS = ["Northeast","Southeast","Midwest","Southwest","West"]
CITIES  = {"Northeast":["New York","Boston","Philadelphia"],
           "Southeast":["Miami","Atlanta","Charlotte"],
           "Midwest":  ["Chicago","Detroit","Columbus"],
           "Southwest":["Dallas","Houston","Phoenix"],
           "West":     ["San Francisco","Los Angeles","Seattle"]}

def build_dim_branch(n=40):
    rows = []
    for i in range(1, n+1):
        r = random.choice(REGIONS); c = random.choice(CITIES[r])
        rows.append({"BranchKey": i, "BranchCode": f"BR{i:04d}",
                     "BranchName": f"{c} {random.choice(['Main','Downtown','Plaza','Center','West','East'])} Branch",
                     "City": c, "Region": r, "OpenedYear": random.randint(1995,2020)})
    return pd.DataFrame(rows)

# ── DimProduct ────────────────────────────────────────────────────────────────
def build_dim_product():
    products = [
        ("Everyday Checking",     "Deposit", "Retail Banking",   0.0010),
        ("Premium Checking",      "Deposit", "Wealth",           0.0020),
        ("High-Yield Savings",    "Deposit", "Retail Banking",   0.0330),
        ("Money Market",          "Deposit", "Wealth",           0.0300),
        ("12-Month CD",           "Deposit", "Retail Banking",   0.0400),
        ("Personal Loan",         "Lending", "Consumer Lending", 0.1050),
        ("Auto Loan",             "Lending", "Consumer Lending", 0.0689),
        ("Home Mortgage",         "Lending", "Mortgage",         0.0625),
        ("HELOC",                 "Lending", "Mortgage",         0.0750),
        ("Credit Card - Rewards", "Lending", "Cards",            0.1450),
        ("Credit Card - Secured", "Lending", "Cards",            0.1650),
        ("Small Business Line",   "Lending", "Business Banking", 0.0850),
    ]
    return pd.DataFrame([{"ProductKey":i,"ProductCode":f"P{i:03d}","ProductName":n,
                          "ProductCategory":c,"LineOfBusiness":l,"BaseRate":r}
                         for i,(n,c,l,r) in enumerate(products,1)])

# ── DimCustomer ───────────────────────────────────────────────────────────────
FIRST = ["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda",
         "David","Elizabeth","Maria","Jose","Wei","Priya","Ahmed","Sofia","Raj","Mei"]
LAST  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
         "Rodriguez","Martinez","Hernandez","Lopez","Patel","Nguyen","Kim","Chen"]
SEGS  = ["Mass Market","Affluent","High Net Worth","Small Business"]
SEG_W = [0.62, 0.24, 0.06, 0.08]

def build_dim_customer(n=5000, branch_keys=None):
    rows = []
    for i in range(1, n+1):
        seg   = np.random.choice(SEGS, p=SEG_W)
        mu    = {"High Net Worth":780,"Affluent":740,"Small Business":710,"Mass Market":690}[seg]
        score = int(np.clip(np.random.normal(mu, 55), 350, 850))
        risk  = "Low" if score>=740 else ("Medium" if score>=660 else "High")
        rows.append({
            "CustomerKey": i, "CustomerID": f"CUST{i:06d}",
            "FirstName": random.choice(FIRST), "LastName": random.choice(LAST),
            "CustomerSegment": seg, "CreditScore": score, "RiskBand": risk,
            "HomeBranchKey": int(random.choice(branch_keys)) if branch_keys else 1,
            "RelationshipStartYear": random.randint(2015,2024),
            "State": random.choice(["NY","CA","TX","FL","IL","WA","GA","MA","AZ","NC"]),
        })
    return pd.DataFrame(rows)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out",       default="../../data/full")
    ap.add_argument("--customers", type=int, default=5000)
    ap.add_argument("--branches",  type=int, default=40)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    dim_branch   = build_dim_branch(args.branches)
    dim_product  = build_dim_product()
    dim_date     = build_dim_date()
    dim_customer = build_dim_customer(args.customers, dim_branch.BranchKey.tolist())

    for name, df in [("DimDate",dim_date),("DimBranch",dim_branch),
                     ("DimProduct",dim_product),("DimCustomer",dim_customer)]:
        df.to_csv(f"{args.out}/{name}.csv", index=False)
        print(f"  {name:<14}: {len(df):>6} rows")

if __name__ == "__main__":
    main()
