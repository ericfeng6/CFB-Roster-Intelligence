import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import sys

print("--- BIG TEN TRANSFER PREDICTION MODEL ---\n")

try:
    df = pd.read_csv("B1G_Transfer_Dataset.csv")
    print(f"Successfully loaded {len(df)} historical transfers into the model!")
except FileNotFoundError:
    print("Error: Could not find B1G_Transfer_Dataset.csv. Run the matchmaker script first.")
    sys.exit()

if len(df) < 10:
    print("Warning: Dataset is very small. Model accuracy may vary.")


features_df = df.drop(columns=['Player', 'Year', 'Destination', 'Success_In_B1G'])
target = df['Success_In_B1G']

X = pd.get_dummies(features_df)
y = target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

print("\nTraining Random Forest Classifier on real historical stats...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions) * 100
print("\n--- MODEL ACCURACY ---")
print(f"Accuracy Score: {accuracy:.1f}%")

print("\n--- SCOUT A NEW TRANSFER ---")
print("Enter the player's stats from their previous season below:")

origin_school = input("Origin School: ")


try:
    yards = float(input("Total Yards (Enter 0 if defensive player): ") or 0)
    tackles = float(input("Total Tackles (Enter 0 if offensive player): ") or 0)
    sacks = float(input("Total Sacks: ") or 0)
    ints = float(input("Total Interceptions: ") or 0)
except ValueError:
    print("\nError: Please enter numbers only for the stats!")
    sys.exit()

new_player_data = {
    f'Origin_{origin_school}': [1], 
    'Prev_Yards': [yards],
    'Prev_Tackles': [tackles],
    'Prev_Sacks': [sacks],
    'Prev_INTs': [ints]
}
new_transfer = pd.DataFrame(new_player_data)

new_transfer = new_transfer.reindex(columns=X.columns, fill_value=0)

success_prob = model.predict_proba(new_transfer)[0][1] * 100
predicted_class = "SUCCESS" if success_prob > 50 else "FAILURE"

print("\n==========================================")
print("             SCOUTING REPORT              ")
print("==========================================")
print(f"Player Profile: Transfer from {origin_school}")
print(f"Prior Production: {yards} Yds | {tackles} Tkls | {sacks} Sacks | {ints} INTs")
print(f"Prediction: {predicted_class}")
print(f"Probability of Success in Big Ten: {success_prob:.1f}%")
print("==========================================\n")

# Save Deliverable 3
with open("Deliverable_3_Prediction_Results.txt", "w") as file:
    file.write(f"Model Accuracy based on historical data: {accuracy:.1f}%\n\n")
    file.write(f"Incoming Transfer Prediction: Transfer from {origin_school}\n")
    file.write(f"Prior Stats: {yards} Yds, {tackles} Tkls, {sacks} Sacks, {ints} INTs\n")
    file.write(f"Prediction: {predicted_class}\n")
    file.write(f"Probability of Success: {success_prob:.1f}%\n")

print("  ✓ Saved final Deliverable_3_Prediction_Results.txt")