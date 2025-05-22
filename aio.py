#Keystroke rec. -> Timing calc. -> vectorization -> CSV

from pynput import keyboard
import time
import json
import os
import random
import pandas as pd
import sys

# Constants
PASSWORD = "BudiAji20"
NUM_REPEATS = 20 #Semakin banyak -> Semakin konsisten

def collect_data():
    USER = input("Username: ").strip()
    DATA_DIR = f"user_data/{USER}/"
    os.makedirs(DATA_DIR, exist_ok=True)

    print(f"\nPassword: \"{PASSWORD[0]}"+ '*' * random.randint(5, 12) + "\"")
    print(f"Repeat {NUM_REPEATS} times, then ENTER.\n")

    session_data = []

    def record_typing():
        timings = []
        pressed_keys = {}
        #typed_text = ""  
        
        def on_press(key):
            current_time = time.time()
            
            # Handle display and tracking
            if hasattr(key, 'char'):
                k = key.char
                #typed_text = k
                #AI GENERATED. Tampilkan karakter
                sys.stdout.write(k)
                sys.stdout.flush()
            elif key == keyboard.Key.enter:
                sys.stdout.write('\n')
                sys.stdout.flush()
                return False
            else:
                k = str(key).replace('Key.', '')
            
            pressed_keys[str(key)] = current_time
            
            timings.append({
                "key": k,
                "event": "press",
                "time": current_time
            })

        def on_release(key):
            current_time = time.time()
            
            if hasattr(key, 'char'):
                k = key.char
            elif key == keyboard.Key.enter:
                return False
            else:
                k = str(key).replace('Key.', '')
            
            hold_duration = None
            if str(key) in pressed_keys:
                hold_duration = current_time - pressed_keys[str(key)]
                pressed_keys.pop(str(key), None)
            
            event_data = {
                "key": k,
                "event": "release",
                "time": current_time
            }
            
            if hold_duration is not None:
                event_data["hold_duration"] = hold_duration
                
            timings.append(event_data)

        print("Start typing and press ENTER after you're done: ", end='', flush=True)
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        # AI GENERATED. Clear input buffer to prevent leaking
        if os.name == 'nt': 
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import termios
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        
        return timings


    for i in range(NUM_REPEATS):
        print(f"[{i+1}/{NUM_REPEATS}] Get ready...")
        #FIX INPUT BOCOR KE NEXT PHASE
        time.sleep(0.3)
        
        timings = record_typing()
        session_data.append(timings)
        
        
        with open(f"{DATA_DIR}/session_{i+1}.json", "w") as f:
            json.dump(timings, f, indent=2)

        print(f"✓ Session {i+1} saved.\n")

    print(f"All {NUM_REPEATS} sessions recorded for user '{USER}' in {DATA_DIR}")
    return USER


def extract_features(session):
    # Build lists of press and release events
    character_events = []
    
    # Bypass shift, alt, ctrl, etc.-
    for event in session:
        if event["key"] in ["shift", "caps_lock", "ctrl", "alt"]:
            continue
            
        character_events.append(event)
    
    # Calculation Tt - T0
    hold_times = []
    press_events = []
    
    for i, event in enumerate(character_events):
        if event["event"] == "press":
            press_events.append(event)
        elif event["event"] == "release" and "hold_duration" in event:
            hold_times.append(event["hold_duration"])
    
    press_times = [event["time"] for event in press_events]
    
    # delay T0P1 - TtP0
    flight_times = []
    for i in range(len(press_times) - 1):
        flight_times.append(press_times[i+1] - press_times[i])
    
    #AI GENERATED. Autofill data kosong/rusak
    # Pad or truncate to expected dimensions
    target_hold_times = len(PASSWORD)
    target_flight_times = len(PASSWORD) - 1
    
    # If we have too few values, pad with averages
    if hold_times:
        avg_hold = sum(hold_times) / len(hold_times)
        while len(hold_times) < target_hold_times:
            hold_times.append(avg_hold)
    
    if flight_times:
        avg_flight = sum(flight_times) / len(flight_times)
        while len(flight_times) < target_flight_times:
            flight_times.append(avg_flight)
    
    # If we have too many values, truncate
    hold_times = hold_times[:target_hold_times]
    flight_times = flight_times[:target_flight_times]
    
    if not hold_times or not flight_times:
        print("⚠ Skipped a session due to missing data.")
        return None
        
    return hold_times + flight_times


def process_data(username):
    DATA_DIR = f"user_data/{username}/"
    OUTPUT_FILE = f"user_data/{username}_behav.csv"
    
    all_feature_rows = []

    for file in sorted(os.listdir(DATA_DIR)):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(DATA_DIR, file), "r") as f:
            session = json.load(f)

        features = extract_features(session)
        if features:
            features.append(username)  # Add label
            all_feature_rows.append(features)

    col_names = (
        [f"hold_{i+1}" for i in range(len(PASSWORD))] +
        [f"flight_{i+1}" for i in range(len(PASSWORD) - 1)] +
        ["label"]
    )

    df = pd.DataFrame(all_feature_rows, columns=col_names)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✓ Features saved to {OUTPUT_FILE}")
    return OUTPUT_FILE

def main():
    print("Keystroke Pattern Input")
    print("==========================================")
    
    username = collect_data()

    print("\nProcessing")
    process_data(username)
    
    print("\nPre-training done")

if __name__ == "__main__":
    main()