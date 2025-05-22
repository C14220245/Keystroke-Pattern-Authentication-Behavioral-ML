import os
import json
import pandas as pd

USERNAME = input("Enter the username to process: ").strip()
PASSWORD = "BudiAji20"
DATA_DIR = f"user_data/{USERNAME}/"
OUTPUT_FILE = f"user_data/{USERNAME}_behav.csv"

def extract_features(session):
    character_events = []
    
    #SKIP non-char
    for event in session:
        if event["key"] in ["shift", "caps_lock", "ctrl", "alt"]:
            continue
            
        character_events.append(event)
    
    hold_times = []
    press_events = []
    
    for i, event in enumerate(character_events):
        if event["event"] == "press":
            press_events.append(event)
        elif event["event"] == "release" and "hold_duration" in event:
            hold_times.append(event["hold_duration"])
    
    press_times = [event["time"] for event in press_events]
    
    flight_times = []
    for i in range(len(press_times) - 1):
        flight_times.append(press_times[i+1] - press_times[i])
    
    target_hold_times = len(PASSWORD)
    target_flight_times = len(PASSWORD) - 1
    
    if hold_times:
        avg_hold = sum(hold_times) / len(hold_times)
        while len(hold_times) < target_hold_times:
            hold_times.append(avg_hold)
    
    if flight_times:
        avg_flight = sum(flight_times) / len(flight_times)
        while len(flight_times) < target_flight_times:
            flight_times.append(avg_flight)
    
    hold_times = hold_times[:target_hold_times]
    flight_times = flight_times[:target_flight_times]
    
    if not hold_times or not flight_times:
        print("⚠ Skipped a session due to missing data.")
        return None
        
    return hold_times + flight_times

def main():
    all_feature_rows = []

    for file in sorted(os.listdir(DATA_DIR)):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(DATA_DIR, file), "r") as f:
            session = json.load(f)

        features = extract_features(session)
        if features:
            features.append(USERNAME)  # Add label
            all_feature_rows.append(features)

    col_names = (
        [f"hold_{i+1}" for i in range(len(PASSWORD))] +
        [f"flight_{i+1}" for i in range(len(PASSWORD) - 1)] +
        ["label"]
    )

    df = pd.DataFrame(all_feature_rows, columns=col_names)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✓ Features saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
