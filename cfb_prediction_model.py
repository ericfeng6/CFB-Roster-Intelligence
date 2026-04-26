import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import sys

print("--- BIG TEN TRANSFER PREDICTION MODEL ---\n")

try:
    df = pd.read_csv("B1G_Transfer_Dataset.csv")
except FileNotFoundError:
    print("Error: Could not find B1G_Transfer_Dataset.csv. Run the matchmaker script first.")
    sys.exit()

features_df = df.drop(columns=['Player', 'Year', 'Destination', 'Success_In_B1G'])
target = df['Success_In_B1G']

X = pd.get_dummies(features_df)
y = target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions) * 100
print(f"Accuracy Score: {accuracy:.1f}%")

print("\n--- SCOUT A NEW TRANSFER ---")
player_name = input("Player Name: ").strip() or "Unknown Prospect"
origin_school = input("Origin School: ").strip()
position = input("Position (e.g., QB, WR, LB, DB): ").strip().upper()

pass_yds = rush_rec_yds = pass_ints = def_ints = tackles = sacks = 0.0

try:
    if position == 'QB':
        pass_yds = float(input("Passing/Rushing Yards: ") or 0)
        pass_ints = float(input("Interceptions Thrown: ") or 0)
    elif position in ['RB', 'WR', 'TE']:
        rush_rec_yds = float(input("Rushing/Receiving Yards: ") or 0)
    else: # Defensive players
        tackles = float(input("Total Tackles: ") or 0)
        sacks = float(input("Total Sacks: ") or 0)
        def_ints = float(input("Interceptions Caught: ") or 0)
except ValueError:
    print("\nError: Please enter numbers only for the stats!")
    sys.exit()

new_player_data = {
    f'Origin_{origin_school}': [1], 
    f'Position_{position}': [1],
    'Prev_Pass_Yds': [pass_yds],
    'Prev_Rush_Rec_Yds': [rush_rec_yds],
    'Prev_Pass_INTs': [pass_ints],
    'Prev_Def_INTs': [def_ints],
    'Prev_Tackles': [tackles],
    'Prev_Sacks': [sacks]
}
new_transfer = pd.DataFrame(new_player_data)
new_transfer = new_transfer.reindex(columns=X.columns, fill_value=0)

success_prob = model.predict_proba(new_transfer)[0][1] * 100
predicted_class = "SUCCESS" if success_prob > 50 else "FAILURE"

if position == 'QB':
    stat_string = f"{pass_yds} Yds | {pass_ints} INTs Thrown"
elif position in ['RB', 'WR', 'TE']:
    stat_string = f"{rush_rec_yds} Yds"
else:
    stat_string = f"{tackles} Tkls | {sacks} Sacks | {def_ints} INTs Caught"

print("\n==========================================")
print("             SCOUTING REPORT              ")
print("==========================================")
print(f"Player:          {player_name}")
print(f"Profile:         {position} from {origin_school}")
print(f"Prior Stats:     {stat_string}")
print(f"Prediction:      {predicted_class}")
print(f"B1G Success Likelihood: {success_prob:.1f}%")
print("==========================================\n")

with open("Deliverable_3_Prediction_Results.txt", "w") as file:
    file.write(f"Model Accuracy based on historical data: {accuracy:.1f}%\n\n")
    file.write("==========================================\n")
    file.write("             SCOUTING REPORT              \n")
    file.write("==========================================\n")
    file.write(f"Player:          {player_name}\n")
    file.write(f"Profile:         {position} from {origin_school}\n")
    file.write(f"Prior Stats:     {stat_string}\n")
    file.write(f"Prediction:      {predicted_class}\n")
    file.write(f"B1G Success Likelihood: {success_prob:.1f}%\n")
    file.write("==========================================\n")

print("  ✓ Saved final Deliverable_3_Prediction_Results.txt")