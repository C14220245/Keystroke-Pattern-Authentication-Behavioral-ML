from pynput import keyboard
import time
import joblib
import numpy as np
import random
import sys

#setel tkinter utk input GUI. Cek .bind() utk alt. listener

PASSWORDTESTVAR = "BudiAji20"
EXPECTED_HOLDS = len(PASSWORDTESTVAR)
EXPECTED_FLIGHTS = len(PASSWORDTESTVAR) - 1

print(f"\nInput password: \"{PASSWORDTESTVAR[0]}"+ '*' * random.randint(5, 15) + "\"")

# Store timing data
timings = []
press_times = []
hold_times = []
pressed_keys = {}
typed_text = ""

# input phase
print("Start typing (press Enter when done): ", end="", flush=True)

def on_press(key):
    #AI GENERATED. Show char in term
    global typed_text
    try:
        k = key.char
        typed_text += k
        sys.stdout.write(k)
        sys.stdout.flush()
    except AttributeError:
        if key == keyboard.Key.backspace:
            if typed_text:
                typed_text = typed_text[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        elif key == keyboard.Key.space:
            typed_text += ' '
            sys.stdout.write(' ')
            sys.stdout.flush()
        return
    
    press_time = time.time()
    pressed_keys[k] = press_time
    press_times.append(press_time)
    timings.append((k, "press", press_time))

def on_release(key):
    try:
        k = key.char
    except AttributeError:
        if key == keyboard.Key.enter:
            return False
        elif key == keyboard.Key.space:
            k = ' '
        else:
            return

    release_time = time.time()
    if k in pressed_keys:
        #Tt - T0
        hold = release_time - pressed_keys[k]
        hold_times.append(hold)
        timings.append((k, "release", release_time))
        pressed_keys.pop(k, None)

    if key == keyboard.Key.enter:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# delay T0P1 - TtP0
flight_times = []
for i in range(len(press_times) - 1):
    flight_times.append(press_times[i+1] - press_times[i])

#==========================VARIATION UTK MACRO SAJA===================================
# if hold_times:
#     hold_times = [t + random.uniform(-0.008, 0.012) for t in hold_times]
    
# if flight_times:
#     flight_times = [t + random.uniform(-0.015, 0.02) for t in flight_times]
#=====================================================================================

# AI ENERATED. Autofill (cek aio/datColl)
if hold_times:
    avg_hold = sum(hold_times) / len(hold_times)
    while len(hold_times) < EXPECTED_HOLDS:
        hold_times.append(avg_hold)
hold_times = hold_times[:EXPECTED_HOLDS]

if flight_times:
    avg_flight = sum(flight_times) / len(flight_times)
    while len(flight_times) < EXPECTED_FLIGHTS:
        flight_times.append(avg_flight)
flight_times = flight_times[:EXPECTED_FLIGHTS]

# AI Phase
features = np.array(hold_times + flight_times).reshape(1, -1)

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
features_scaled = scaler.transform(features)

#==================SENSITIVITY========================
score = model.decision_function(features_scaled)[0]
threshold = 0.1  # cutoff decision maker: higher = stricter. default = -0.05 @ 10 runs
#=====================================================

print(f"\nCurrent score: {score:.4f}")
print(f"Score threshold: {threshold}")

if score >= threshold:
    print("\nSUCCESS")
else:
    print("\nFAIL")

# Terminal clear (AI generated)
import os
import sys

if os.name == 'nt': 
    import msvcrt
    while msvcrt.kbhit():
        msvcrt.getch()
else:
    import termios
    termios.tcflush(sys.stdin, termios.TCIFLUSH)


input("\nPress Enter to exit")
