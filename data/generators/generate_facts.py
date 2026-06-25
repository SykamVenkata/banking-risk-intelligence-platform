"""
Retail Banking & Risk Intelligence Platform
============================================
Synthetic FACT generator + near-real-time streaming simulator.

Produces:
  DimAccount        - account master (all customers x products)
  FactTransaction   - transaction events (streaming showcase)
  FactLoanBalance   - monthly loan snapshots + DPD/CECL

Streaming mode (--stream):
  Appends micro-batches of transactions every N seconds,
  emulating a near-real-time Bronze landing feed.

Usage (batch):
    python generate_facts.py --out ../../data/full --months 18

Usage (streaming):
    python generate_facts.py --stream --interval 5 --batch 200 --out ../../data/full
"""
import argparse, os, time, uuid
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

np.random.seed(7)

TXN_TYPES   = ["POS Purchase","ATM Withdrawal","ACH Credit","ACH Debit",
               "Wire Transfer","Mobile Deposit","Bill Pay","Card Payment",
               "Interest Credit","Fee"]
TXN_WEIGHTS = [0.34,0.10,0.12,0.12,0.03,0.06,0.09,0.08,0.04,0.02]
CHANNELS    = ["Card","Online","Mobile","Branch","ATM","ACH"]
MERCH_CATS  = ["Grocery","Fuel","Restaurant","Retail","Travel","Utilities",
               "Healthcare","Entertainment","Transfer","Other"]

def _load_dims(data_dir):
    return (pd.read_csv(f"{data_dir}/DimCustomer.csv"),
            pd.read_csv(f"{data_dir}/DimProduct.csv"),
            pd.read_csv(f"{data_dir}/DimBranch.csv"))

# ── DimAccount ────────────────────────────────────────────────────────────────
def build_accounts(cust, prod, out_dir):
    dep_p  = prod[prod.ProductCategory=="Deposit"].ProductKey.tolist()
    lend_p = prod[prod.ProductCategory=="Lending"].ProductKey.tolist()
    rows, akey = [], 1
    for _, c in cust.iterrows():
        n_dep  = np.random.choice([1,2,2,3,3,4], p=[0.15,0.25,0.25,0.15,0.12,0.08])
        n_lend = np.random.choice([0,0,1,1,2],   p=[0.40,0.22,0.22,0.10,0.06])
        for _ in range(n_dep):
            rows.append(_acct(akey, c, int(np.random.choice(dep_p)),  "Deposit"));  akey+=1
        for _ in range(n_lend):
            rows.append(_acct(akey, c, int(np.random.choice(lend_p)), "Lending")); akey+=1
    df = pd.DataFrame(rows)
    df.to_csv(f"{out_dir}/DimAccount.csv", index=False)
    print(f"  DimAccount    : {len(df):>7} rows"); return df

def _acct(akey, c, pk, cat):
    oy  = int(c.RelationshipStartYear)
    bal = (float(np.round(np.random.lognormal(8.55,1.15),2)) if cat=="Deposit"
           else float(np.round(np.random.lognormal(10.05,1.0),2)))
    return {"AccountKey":akey,"AccountID":f"ACCT{akey:08d}",
            "CustomerKey":int(c.CustomerKey),"ProductKey":pk,"AccountCategory":cat,
            "OpenDate":date(oy,np.random.randint(1,13),np.random.randint(1,28)).isoformat(),
            "Status":np.random.choice(["Active","Active","Active","Dormant","Closed"],p=[0.8,0.08,0.05,0.04,0.03]),
            "OpeningBalance":bal,"HomeBranchKey":int(c.HomeBranchKey)}

# ── FactLoanBalance ───────────────────────────────────────────────────────────
def build_loan_balances(accts, cust, months, out_dir):
    loans = accts[accts.AccountCategory=="Lending"].merge(
        cust[["CustomerKey","RiskBand"]], on="CustomerKey")
    end = date.today().replace(day=1)
    periods = [(end-timedelta(days=30*i)).replace(day=1) for i in range(months)][::-1]
    rows = []
    for _, ln in loans.iterrows():
        bal, dpd = ln.OpeningBalance, 0
        base_p   = {"Low":0.015,"Medium":0.05,"High":0.13}.get(ln.RiskBand,0.05)
        for ps in periods:
            bal = max(0.0, bal*(1-np.random.uniform(0.005,0.02)))
            if np.random.random() < base_p:    dpd = min(120, dpd+30)
            elif dpd>0 and np.random.random()<0.55: dpd = max(0, dpd-30)
            bucket = ("Current" if dpd==0 else "30 DPD" if dpd==30
                      else "60 DPD" if dpd==60 else "90 DPD" if dpd==90 else "120+ DPD")
            rows.append({"DateKey":int(ps.strftime("%Y%m%d")),"AccountKey":int(ln.AccountKey),
                         "CustomerKey":int(ln.CustomerKey),"ProductKey":int(ln.ProductKey),
                         "BranchKey":int(ln.HomeBranchKey),"EndingBalance":round(bal,2),
                         "DaysPastDue":dpd,"DelinquencyBucket":bucket,"IsNonPerforming":dpd>=90})
    df = pd.DataFrame(rows)
    # Add Gold-layer derived columns so .pbip works standalone
    df = df.sort_values(["AccountKey","DateKey"])
    df["PrevDPD"]    = df.groupby("AccountKey").DaysPastDue.shift(1)
    df["RollStatus"] = np.select([df.PrevDPD.isna(),df.DaysPastDue>df.PrevDPD,df.DaysPastDue<df.PrevDPD],
                                  ["New","Worsened","Cured"],default="Stable")
    df["CECLStage"]  = np.select([df.DaysPastDue>=90,df.DaysPastDue>=30],
                                  ["Stage 3 - Impaired","Stage 2 - SICR"],default="Stage 1 - Performing")
    df.drop(columns=["PrevDPD"]).to_csv(f"{out_dir}/FactLoanBalance.csv",index=False)
    print(f"  FactLoanBalance: {len(df):>7} rows"); return df

# ── FactTransaction ───────────────────────────────────────────────────────────
def _make_txn(dep_accts, ts=None):
    a    = dep_accts.sample(1).iloc[0]
    tt   = np.random.choice(TXN_TYPES, p=TXN_WEIGHTS)
    sign = -1 if tt in ("POS Purchase","ATM Withdrawal","ACH Debit","Bill Pay","Card Payment","Fee","Wire Transfer") else 1
    amt  = (round(np.random.choice([2.5,3.0,12.0,35.0]),2) if tt=="Fee"
            else round(float(np.random.uniform(0.1,25.0)),2) if tt=="Interest Credit"
            else round(float(np.random.lognormal(3.6,1.1)),2))
    ts   = ts or datetime.now()
    return {"TransactionID":str(uuid.uuid4()),"DateKey":int(ts.strftime("%Y%m%d")),
            "TxnTimestamp":ts.isoformat(timespec="seconds"),
            "AccountKey":int(a.AccountKey),"CustomerKey":int(a.CustomerKey),
            "ProductKey":int(a.ProductKey),"BranchKey":int(a.HomeBranchKey),
            "TransactionType":tt,"Channel":np.random.choice(CHANNELS),
            "MerchantCategory":np.random.choice(MERCH_CATS),
            "Amount":round(sign*amt,2),"Direction":"Debit" if sign==-1 else "Credit",
            "AbsAmount":amt,"IsFraudFlag":bool(np.random.random()<0.002)}

def build_transactions(accts, months, out_dir, per_day=1500):
    dep  = accts[(accts.AccountCategory=="Deposit")&(accts.Status=="Active")]
    end  = datetime.now(); start = end - timedelta(days=30*months)
    rows = []; day = start
    while day <= end:
        for _ in range(np.random.poisson(per_day)):
            ts = datetime(day.year,day.month,day.day)+timedelta(seconds=np.random.randint(0,86400))
            rows.append(_make_txn(dep, ts))
        day += timedelta(days=1)
    df = pd.DataFrame(rows)
    df.to_csv(f"{out_dir}/FactTransaction.csv",index=False)
    print(f"  FactTransaction: {len(df):>7} rows"); return df

# ── Streaming simulator ───────────────────────────────────────────────────────
def stream(out_dir, interval, batch):
    cust,prod,_ = _load_dims(out_dir)
    accts = pd.read_csv(f"{out_dir}/DimAccount.csv")
    dep   = accts[(accts.AccountCategory=="Deposit")&(accts.Status=="Active")]
    path  = f"{out_dir}/stream_FactTransaction.csv"
    written = os.path.exists(path)
    print(f"Streaming {batch} txns every {interval}s → {path}\nCtrl+C to stop\n")
    try:
        while True:
            now   = datetime.now()
            micro = pd.DataFrame([_make_txn(dep,now) for _ in range(batch)])
            micro.to_csv(path,mode="a",header=not written,index=False)
            written=True
            print(f"  [{now:%H:%M:%S}] +{batch} txns (net ${micro.Amount.sum():,.2f})")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stream stopped.")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out",      default="../../data/full")
    ap.add_argument("--months",   type=int, default=18)
    ap.add_argument("--per-day",  type=int, default=1500)
    ap.add_argument("--stream",   action="store_true")
    ap.add_argument("--interval", type=int, default=5)
    ap.add_argument("--batch",    type=int, default=200)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    if args.stream:
        stream(args.out, args.interval, args.batch); return
    cust,prod,_ = _load_dims(args.out)
    print("Building synthetic facts...")
    accts = build_accounts(cust, prod, args.out)
    build_loan_balances(accts, cust, args.months, args.out)
    build_transactions(accts, args.months, args.out, args.per_day)
    print("Done.")

if __name__ == "__main__":
    main()
