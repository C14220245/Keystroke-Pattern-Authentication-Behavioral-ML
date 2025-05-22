from pynput import keyboard
import time
import json
import os
import random

PASSWORDTESTVAR = "BudiAji20" #Bisa diubah jadi SQL query kl dalam web
NUM_REPEATS = 10
USER = input("Enter your username: ").strip() #Bisa dihapus atau tukar pakai query username
DATA_DIR = f"user_data/{USER}/" #TEST DIR
os.makedirs(DATA_DIR, exist_ok=True)

print(f"\nType your password: \"{PASSWORDTESTVAR[0]}"+ '*' * random.randint(5, 12) + "\"")
print(f"Repeat {NUM_REPEATS} times. Press ENTER afterwards.\n")

session_data = []

def record_typing():
    timings = []
    pressed_keys = {}
    
    def on_press(key):
        #timer 0
        current_time = time.time()
        if hasattr(key, 'char'):
            k = key.char
        elif key == keyboard.Key.enter:
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

    print("Start typing and press ENTER after you're done.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    return timings

for i in range(NUM_REPEATS):
    print(f"[{i+1}/{NUM_REPEATS}] Get ready...")
    time.sleep(1)
    
    timings = record_typing()
    
    session_data.append(timings)
    with open(f"{DATA_DIR}/session_{i+1}.json", "w") as f:
        json.dump(timings, f, indent=2)

    print(f"✓ Session {i+1} saved.\n")

print(f"All {NUM_REPEATS} sessions recorded for user '{USER}' in {DATA_DIR}")
