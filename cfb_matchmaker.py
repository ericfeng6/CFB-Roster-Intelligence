import pandas as pd
import numpy as np

print("Loading raw data...")
transfers = pd.read_csv("cfb_transfers_2022_2025.csv")
stats = pd.read_csv("cfb_player_stats.csv")

transfers = transfers.dropna(subset=['origin', 'destination', 'season'])

b1g_teams = [
    'Michigan', 'Ohio State', 'Penn State', 'Wisconsin', 'Iowa', 
    'Minnesota', 'Nebraska', 'Purdue', 'Illinois', 'Northwestern', 
    'Michigan State', 'Indiana', 'Rutgers', 'Maryland',
    'USC', 'UCLA', 'Oregon', 'Washington'
]

b1g_transfers = transfers[transfers['destination'].isin(b1g_teams)].copy()
print(f"Found {len(b1g_transfers)} players who transferred to the Big Ten. Searching for stats...")

dataset_rows = []

for index, row in b1g_transfers.iterrows():
    first_name = str(row.get('firstName', '')).strip()
    last_name = str(row.get('lastName', '')).strip()
    full_name = f"{first_name} {last_name}"
    
    position = str(row.get('position', 'UNKNOWN')).strip().upper()
    
    transfer_year = int(row['season'])
    prev_year = transfer_year - 1
    origin_school = row['origin']
    dest_school = row['destination']

    prev_stats = stats[(stats['season'] == prev_year) & 
                       (stats['team'] == origin_school) & 
                       (stats['player'] == full_name)]
    
    b1g_stats = stats[(stats['season'] == transfer_year) & 
                      (stats['team'] == dest_school) & 
                      (stats['player'] == full_name)]

    if not prev_stats.empty and not b1g_stats.empty:
        p_stats = prev_stats.iloc[0]
        b_stats = b1g_stats.iloc[0]
        
        prev_yards = p_stats.get('YDS', 0) 
        prev_tackles = p_stats.get('TOT', 0)
        prev_ints = p_stats.get('INT', 0)
        prev_sacks = p_stats.get('SACKS', 0)
        
        b1g_yards = b_stats.get('YDS', 0)
        b1g_tackles = b_stats.get('TOT', 0)
        b1g_sacks = b_stats.get('SACKS', 0)
        b1g_ints = b_stats.get('INT', 0)

        
        is_success = 0
        if position == 'QB':
            if b1g_yards > 1200: is_success = 1 # QBs need a lot of yards
        elif position in ['RB', 'WR', 'TE']:
            if b1g_yards > 300: is_success = 1  
        elif position in ['LB', 'DB', 'CB', 'S', 'SAF', 'DL', 'DE', 'DT', 'EDGE']:
            if b1g_tackles > 25 or b1g_sacks >= 3 or b1g_ints >= 1: is_success = 1 
        else: 
            if b1g_yards > 300 or b1g_tackles > 25: is_success = 1

        dataset_rows.append({
            'Player': full_name,
            'Position': position, 
            'Year': transfer_year,
            'Origin': origin_school,
            'Destination': dest_school,
            'Prev_Yards': prev_yards,
            'Prev_Tackles': prev_tackles,
            'Prev_Sacks': prev_sacks,
            'Prev_INTs': prev_ints,
            'Success_In_B1G': is_success
        })

final_df = pd.DataFrame(dataset_rows)
final_df = final_df.fillna(0)

final_df.to_csv("B1G_Transfer_Dataset.csv", index=False)
print(f"\nMatchmaker complete! Successfully linked {len(final_df)} players with full before/after stats.")
print("  ✓ Saved as B1G_Transfer_Dataset.csv")