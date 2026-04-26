import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CFBD_API_KEY")

BASE_URL = "https://api.collegefootballdata.com"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json"
}

YEARS = [2021, 2022, 2023, 2024]

def pull_player_stats():
    all_stats = []
    print("Pulling player stats from CFBD (this might take a minute)...")

    for year in YEARS:
        print(f"  Fetching {year} stats...")
        url = f"{BASE_URL}/stats/player/season?year={year}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            for row in data:
                row['season'] = year
            all_stats.extend(data)
        else:
            print(f"  X Failed to pull {year} stats.")
            
        time.sleep(0.5)

    print("\nConverting and formatting the data...")
    df = pd.DataFrame(all_stats)
    
    df['stat'] = pd.to_numeric(df['stat'], errors='coerce') 
    
    pivot_df = df.pivot_table(
        index=['season', 'playerId', 'player', 'team', 'conference'], 
        columns='statType', 
        values='stat', 
        aggfunc='sum'
    ).reset_index()
    
    pivot_df = pivot_df.fillna(0)
    
    pivot_df.to_csv("cfb_player_stats.csv", index=False)
    print("  ✓ Saved cfb_player_stats.csv")

if __name__ == "__main__":
    pull_player_stats()