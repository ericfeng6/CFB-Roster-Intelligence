import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# --- SETUP ---
API_KEY = os.getenv("CFBD_API_KEY")

if not API_KEY:
    print("Error: Could not find CFBD_API_KEY. Make sure your .env file is set up correctly.")
    exit()

BASE_URL = "https://api.collegefootballdata.com"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json"
}

YEARS = [2022, 2023, 2024, 2025]

def fetch_cfbd_data():
    all_rosters = []
    all_transfers = []
    
    print("Starting data pull from CFBD...")

    for year in YEARS:
        print(f"\nFetching data for {year}...")
        
        # 1. Fetch Rosters
        roster_url = f"{BASE_URL}/roster?year={year}"
        roster_response = requests.get(roster_url, headers=HEADERS)
        
        if roster_response.status_code == 200:
            year_roster = roster_response.json()
            for player in year_roster:
                player['roster_year'] = year
            all_rosters.extend(year_roster)
            print(f"  ✓ Pulled {len(year_roster)} roster records.")
        else:
            print(f"  X Failed to pull rosters for {year}: {roster_response.status_code}")
            
        time.sleep(0.5) 
        
        # 2. Fetch Transfer Portal Data (Using the corrected endpoint)
        transfer_url = f"{BASE_URL}/player/portal?year={year}"
        transfer_response = requests.get(transfer_url, headers=HEADERS)
        
        if transfer_response.status_code == 200:
            year_transfers = transfer_response.json()
            all_transfers.extend(year_transfers)
            print(f"  ✓ Pulled {len(year_transfers)} transfer portal records.")
        else:
            print(f"  X Failed to pull transfers for {year}: {transfer_response.status_code}")
            
        time.sleep(0.5)

    # --- SAVE TO CSV ---
    print("\nConverting to DataFrames and saving to CSV...")
    
    # Rosters
    if all_rosters:
        rosters_df = pd.DataFrame(all_rosters)
        rosters_df.to_csv("cfb_rosters_2022_2025.csv", index=False)
        print("  ✓ Saved cfb_rosters_2022_2025.csv")
        
    # Transfers
    if all_transfers:
        transfers_df = pd.DataFrame(all_transfers)
        transfers_df.to_csv("cfb_transfers_2022_2025.csv", index=False)
        print("  ✓ Saved cfb_transfers_2022_2025.csv")
        
    print("\nData collection complete! You are ready to start your analysis.")

if __name__ == "__main__":
    fetch_cfbd_data()