# CFB Roster Intelligence: Big Ten Transfer Predictor

This project analyzes College Football Data (CFBD) to evaluate roster construction and predict the success of players transferring into the Big Ten conference. It utilizes a Random Forest classifier to determine the likelihood of a transfer being a "success" based on their historical performance metrics at their origin school.

## Project Overview
The repository contains a suite of tools to:
1.  Fetch historical roster and transfer portal data.
2.  Aggregate season-level player statistics.
3.  Perform "matchmaking" to link a player's pre-transfer stats with their post-transfer outcomes.
4.  Predict the success probability of new transfer prospects.

## Execution Order
To ensure the data flows correctly between scripts, you must run the files in the following order:

### Phase 1: Data Collection
1.  **`cfb_data_pull.py`**: Fetches raw roster and transfer portal records for the 2022–2025 seasons.
    * *Output:* `cfb_rosters_2022_2025.csv`, `cfb_transfers_2022_2025.csv`
2.  **`cfb_pull_stats.py`**: Downloads performance statistics for all players across multiple seasons.
    * *Output:* `cfb_player_stats.csv`

### Phase 2: Processing & Analysis
3.  **`cfb_analysis.py`**: Breaks down rosters by classification (Upperclassmen vs. Underclassmen) and calculates transfer percentages.
    * *Output:* `Deliverable_1_Roster_Breakdowns.csv`, `Deliverable_2_Transfer_Breakdowns.csv`
4.  **`cfb_records_rankings.py`**: Merges team records and AP Top 25 rankings with the roster breakdowns.
    * *Output:* `Deliverable_1_FINAL.csv`
5.  **`cfb_matchmaker.py`**: The core data processing script that aligns transfer history with performance stats to create a training dataset.
    * *Output:* `B1G_Transfer_Dataset.csv`

### Phase 3: Modeling
6.  **`cfb_prediction_model.py`**: Trains the Random Forest model and provides a CLI for scouting new prospects.
    * *Output:* `Deliverable_3_Prediction_Results.txt`

## Requirements
- Python 3.x
- Pandas, Numpy, Scikit-learn, Requests
- A valid **CFBD API Key** stored in a `.env` file:
  ```text
  CFBD_API_KEY=your_api_key_here