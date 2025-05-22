import tkinter as UI
from tkinter import ttk
import time
import joblib
import numpy as np
import random
import os

class KeystrokeAuthenticator(UI.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Keystroke Pattern Authenticator")
        self.geometry("500x300")
        self.configure(padx=20, pady=20)
        
        #==========================PASSWORD SETTINGS===================================
        self.PASSWORD = "BudiAji20"
        self.EXPECTED_HOLDS = len(self.PASSWORD)
        self.EXPECTED_FLIGHTS = len(self.PASSWORD) - 1
        #=============================================================================
        
        # Store timing data
        self.timings = []
        self.press_times = {}
        self.hold_times = []
        self.flight_times = []
        self.last_press_time = None
        self.typed_text = ""
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        masked_pw = self.PASSWORD[0] + '*' * random.randint(5, 15)
        header = ttk.Label(self, text=f"Input password: \"{masked_pw}\"", font=("Arial", 12))
        header.pack(pady=(0, 20))
        
        # Password entry
        self.pw_var = UI.StringVar()
        self.pw_entry = ttk.Entry(self, textvariable=self.pw_var, show="*", font=("Arial", 12))
        self.pw_entry.pack(fill="x", pady=(0, 20))
        self.pw_entry.focus()
        
        # Bind key events
        self.pw_entry.bind("<KeyPress>", self.on_key_press)
        self.pw_entry.bind("<KeyRelease>", self.on_key_release)
        self.pw_entry.bind("<Return>", self.process_authentication)
        
        # Status frame
        status_frame = ttk.LabelFrame(self, text="Status")
        status_frame.pack(fill="x", pady=(0, 20))
        
        self.status_label = ttk.Label(status_frame, text="Input your password", font=("Arial", 10))
        self.status_label.pack(pady=10)
        
        self.score_label = ttk.Label(status_frame, text="", font=("Arial", 10))
        self.score_label.pack(pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x")
        
        self.auth_button = ttk.Button(button_frame, text="Authenticate", command=self.process_authentication)
        self.auth_button.pack(side="left", padx=(0, 10))
        
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side="left")
        
    #==========================KEY EVENT HANDLERS===================================
    def on_key_press(self, event):
        if event.keysym == "Return":
            return
        
        # Ignore modifier keys (Shift, Control, Alt, etc.)
        if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return
            
        key = event.char
        # Skip if empty character (likely a special key)
        if not key:
            return
            
        press_time = time.time()
        
        # Record press time (T0)
        self.press_times[key] = press_time
        
        # FLIGHT T0P1-TtP0
        if self.last_press_time is not None:
            flight_time = press_time - self.last_press_time
            self.flight_times.append(flight_time)
        
        self.last_press_time = press_time
        
        #DEBUG ONLY. Disable once stable
        print(f"Key pressed: {event.keysym}, Char: '{event.char}'")
        
    def on_key_release(self, event):
        if event.keysym == "Return":
            return
        
        # Bypass non-char
        if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return
            
        key = event.char
        # Skip if empty character
        if not key:
            return
            
        release_time = time.time()
        
        # HOLD Tt - T0
        if key in self.press_times:
            hold_time = release_time - self.press_times[key]
            self.hold_times.append(hold_time)
    #=============================================================================
            
    def process_authentication(self, event=None):
        entered_password = self.pw_var.get()
        if entered_password != self.PASSWORD:
            self.status_label.config(text="Incorrect password", foreground="red")
            self.after(500, self.self_reset)  # Kalau pass/input bocor, tambah parameter (delay) di depan. val 500-1000 (ms)
            return

        #==========================VARIATION UTK MACRO SAJA===================================
        # Uncomment to add random variation to times (for testing macro detection)
        # if self.hold_times:
        #     self.hold_times = [t + random.uniform(-0.008, 0.012) for t in self.hold_times]
        # 
        # if self.flight_times:
        #     self.flight_times = [t + random.uniform(-0.015, 0.02) for t in self.flight_times]
        #=================================================================================

        # AI GENERATED: Autofill hold times if needed
        if self.hold_times:
            avg_hold = sum(self.hold_times) / len(self.hold_times)
            while len(self.hold_times) < self.EXPECTED_HOLDS:
                self.hold_times.append(avg_hold)
        self.hold_times = self.hold_times[:self.EXPECTED_HOLDS]
        if self.flight_times:
            avg_flight = sum(self.flight_times) / len(self.flight_times)
            while len(self.flight_times) < self.EXPECTED_FLIGHTS:
                self.flight_times.append(avg_flight)
        self.flight_times = self.flight_times[:self.EXPECTED_FLIGHTS]
        
        
        # AI PHASE. 
        try:
            features = np.array(self.hold_times + self.flight_times).reshape(1, -1)
            
            model = joblib.load("model.pkl")
            scaler = joblib.load("scaler.pkl")
            features_scaled = scaler.transform(features)
            
            #==================SENSITIVITY========================
            threshold = 0.03 #SCORE LIMITER. default -0.05 @ 10 runs, 0 @ 20 runs. ANTIBOT: Cek avg score makro @64ms dan 96ms
            score = model.decision_function(features_scaled)[0]
            #=====================================================
            
            self.score_label.config(text=f"Score: {score:.4f} (Threshold: {threshold})")
            
            print(f"\nCurrent score: {score:.4f}")
            print(f"Score threshold: {threshold}")
            
            if score >= threshold:
                self.status_label.config(text="SUCCESS", foreground="green")
                print("\nSUCCESS")
            else:
                self.status_label.config(text="FAIL", foreground="red")
                print("\nFAIL")
                
            # Auto reset input fields but keep the result
            self.after(2000, self.self_reset)
                
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
            self.after(2000, self.self_reset)

    def self_reset(self):
        """Resets input fields and timing data while preserving results"""
        # Reset timing data
        self.timings = []
        self.press_times = {}
        self.hold_times = []
        self.flight_times = []
        self.last_press_time = None
        self.typed_text = ""
        
        # Reset only the input field
        self.pw_var.set("")
        self.pw_entry.focus()
        
    def reset(self):
        """Full reset including results display"""
        self.self_reset()
        # Additionally reset result displays
        self.status_label.config(text="Waiting for input...", foreground="black")
        self.score_label.config(text="")

if __name__ == "__main__":
    app = KeystrokeAuthenticator()
    app.mainloop()