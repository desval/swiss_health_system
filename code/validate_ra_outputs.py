"""Quick validation of consolidated Statistik-RA outputs."""
import pandas as pd, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "output", "data")

mf = pd.read_csv(os.path.join(D, "source_manifest.csv"))
cg = pd.read_csv(os.path.join(D, "canton_risk_group.csv"))
ch = pd.read_csv(os.path.join(D, "switzerland_summary.csv"))

print("=== source_manifest ===")
print(f"Total files: {len(mf)}")
can_per_year = mf[mf.is_canonical].groupby("year").size()
print(f"Canonical per year — min={can_per_year.min()} max={can_per_year.max()} (all should be 1)")
print(f"Years: {mf['year'].min()}–{mf['year'].max()}")

print("\n=== canton_risk_group ===")
print(f"Total rows: {len(cg)}")
print(f"Years: {sorted(cg.year.unique())}")
print(f"Null cantons: {cg.canton.isna().sum()}")
cost_by_year = cg.groupby("year")["total_cost_chf"].sum() / 1e9
print("Total cost CHF bn by year:")
print(cost_by_year.to_string())

print("\n=== switzerland_summary ===")
print(f"Total rows: {len(ch)}")
print(f"Years: {sorted(ch.year.unique())}")
print(f"Column count: {len(ch.columns)}")
print(f"First 10 cols: {list(ch.columns[:10])}")
