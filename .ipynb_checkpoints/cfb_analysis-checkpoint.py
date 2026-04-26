import pandas as pd
import numpy as np

print("Loading data...")
rosters = pd.read_csv("cfb_rosters_2022_2025.csv")
transfers = pd.read_csv("cfb_transfers_2022_2025.csv")

transfers = transfers[transfers['destination'].notna()]

print("Generating Part 2: Transfer Class Breakdowns...")
transfer_breakdown = transfers.groupby(['destination', 'season']).agg(
    Total_Transfers_Incoming=('firstName', 'count')
).reset_index()

transfer_breakdown.rename(columns={'destination': 'School', 'season': 'Year'}, inplace=True)

transfer_breakdown.to_csv("Deliverable_2_Transfer_Breakdowns.csv", index=False)
print("  ✓ Saved Deliverable_2_Transfer_Breakdowns.csv")

print("Generating Part 1: Roster Breakdowns...")

if 'team' in rosters.columns:
    rosters.rename(columns={'team': 'School', 'roster_year': 'Year'}, inplace=True)

name_col = 'firstName' if 'firstName' in rosters.columns else 'first_name'
if name_col not in rosters.columns:
    name_col = rosters.columns[0]

class_col = 'year' if 'year' in rosters.columns else 'classification'

roster_breakdown = rosters.groupby(['School', 'Year']).agg(
    Total_Players=(name_col, 'count'),
    Underclassmen=(class_col, lambda x: x.isin([1, 2, '1', '2', 'FR', 'SO', 'Freshman', 'Sophomore']).sum()),
    Upperclassmen=(class_col, lambda x: x.isin([3, 4, 5, 6, 7, '3', '4', '5', '6', '7', 'JR', 'SR', 'Junior', 'Senior']).sum())
).reset_index()

roster_breakdown = pd.merge(roster_breakdown, transfer_breakdown, on=['School', 'Year'], how='left')

roster_breakdown['Total_Transfers_Incoming'] = roster_breakdown['Total_Transfers_Incoming'].fillna(0)

roster_breakdown['Pct_Transfers'] = (roster_breakdown['Total_Transfers_Incoming'] / roster_breakdown['Total_Players']) * 100
roster_breakdown['Pct_Non_Transfers'] = 100 - roster_breakdown['Pct_Transfers']

roster_breakdown.to_csv("Deliverable_1_Roster_Breakdowns.csv", index=False)
print("  ✓ Saved Deliverable_1_Roster_Breakdowns.csv")

print("\nAnalysis complete!")