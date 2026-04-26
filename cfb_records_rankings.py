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

YEARS = [2022, 2023, 2024, 2025]

def get_records_and_rankings():
    all_team_data = []

    print("Fetching Records and Rankings from CFBD...")

    for year in YEARS:
        print(f"  Fetching {year}...")
        
        records_url = f"{BASE_URL}/records?year={year}"
        rec_resp = requests.get(records_url, headers=HEADERS)
        records_data = rec_resp.json() if rec_resp.status_code == 200 else []
        
        rank_url = f"{BASE_URL}/rankings?year={year}"
        rank_resp = requests.get(rank_url, headers=HEADERS)
        rankings_data = rank_resp.json() if rank_resp.status_code == 200 else []
        
        final_ap_poll = {}
        if rankings_data:
            for week_data in reversed(rankings_data):
                found_ap = False
                for poll in week_data.get('polls', []):
                    if poll.get('poll') == 'AP Top 25':
                        for rank_item in poll.get('ranks', []):
                            final_ap_poll[rank_item['school']] = rank_item['rank']
                        found_ap = True
                        break
                if found_ap:
                    break 
                    
        for team in records_data:
            school = team.get('team')
            conf = team.get('conference', 'Independent')
            
            total_wins = team.get('total', {}).get('wins', 0)
            total_losses = team.get('total', {}).get('losses', 0)
            team_record = f"{total_wins}-{total_losses}"
            
            ap_rank = final_ap_poll.get(school, "N/A")
            
            all_team_data.append({
                'School': school,
                'Year': year,
                'Conference': conf,
                'Team_Record': team_record,
                'End_of_Year_AP_Rank': ap_rank,
                'Conference_Champ': "TBD" 
            })
            
        time.sleep(0.5)
        
    df_records = pd.DataFrame(all_team_data)
    
    print("\nMerging with Deliverable_1_Roster_Breakdowns.csv...")
    try:
        roster_df = pd.read_csv("Deliverable_1_Roster_Breakdowns.csv")
        
        final_deliverable = pd.merge(
            roster_df, 
            df_records, 
            on=['School', 'Year'], 
            how='left'
        )
        
        preferred_order = [
            'School', 'Conference', 'Year', 'Team_Record', 'Conference_Champ', 
            'End_of_Year_AP_Rank', 'Total_Players', 'Underclassmen', 'Upperclassmen', 
            'Pct_Non_Transfers', 'Total_Transfers_Incoming', 'Pct_Transfers'
        ]
        
        existing_cols = [c for c in preferred_order if c in final_deliverable.columns]
        remaining_cols = [c for c in final_deliverable.columns if c not in existing_cols]
        final_order = existing_cols + remaining_cols
        
        final_deliverable = final_deliverable[final_order]
        
        final_deliverable.to_csv("Deliverable_1_FINAL.csv", index=False)
        print("  ✓ Saved Deliverable_1_FINAL.csv")
        print("\ncomplete!")
        
    except FileNotFoundError:
        print("  X Could not find Deliverable_1_Roster_Breakdowns.csv. Make sure it is in the same folder.")

if __name__ == "__main__":
    get_records_and_rankings()