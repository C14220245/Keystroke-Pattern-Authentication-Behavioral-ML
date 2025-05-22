ROUGH PROTOTYPE OF KEYSTROKE PATTERN AUTHENTICATION USING IsolationForest
version: v0.10 (beta)
Made by: Malvinshu (GitHub)


How it works: Track delay/flight and hold times, compare with existing dataset

Cara pakai program:
A: Menggunakan aio.py
1. Run aio.py
2. Masukkan username
3. Ikuti petunjuk, ulangi input password sampai selesai (keluar pesan "Pre-training done" di terminal)
4. run train-model.py, masukkan username yang sama
5. run authenticate.py (untuk CLI) atau gui_authenticate.py (untuk GUI)
6. Masukkan password dengan keystroke serupa

FAQ:
Q: How to change the password/phrase?
A: Simply change the "PASSWORD" or "PASSWORDTESTVAR" variable in each code
Q: How to change the repetition amount of password input (default: 20)?
A: Change the NUM_REPEATS variable in aio.py or data-collection.py. Please consider changing the threshold scoring—The higher NUM_REPEATS, the higher the average score is likely to be
Q: How to change the scoring threshold?
A: Change "threshold" (ctrl+F) variable in authenticate.py
Q: Why automated input and authentication results are inconsistent?
A: Neatly arranged automated input with consistent hold and flight times might result in wildly inconsistent authentication due to scaling effect. Try randomizing the automated input flight and delay times to reflect real-usage condition
Q: Why authentication process always accept/decline my input? (Considering no change was made in the code)
A: Try modifying the threshold value (see: "Q: How to change the scoring threshold?"), and/or consider retraining with fresh dataset instead of pre-made
Q: Why authentication process always accept/decline my input? (Considering the value of NUM_REPEATS variable in aio.py data-collection.py have been changed, and the dataset also contains (NUM_REPEATS) amount of input repetition)
A: Higher amount of dataset inputs (NUM_REPEATS) usually ends up in higher authentication score. Consider changing the threshold variable
Q: Why I got "sklearn\base.py:493: UserWarning: X does not have valid feature names, but StandardScaler was fitted with feature names warnings.warn()" in my terminal after using gui_authenticate.py?
A: This warning doesn't affect the program functionality, nor reliability. This was mostly caused by the absence of naming in scaler input (numpy array unnamed)
Q: Why is the GUI laggy and/or unresponsive?
A: It was mostly due to the delays caused by tkinter


Troubleshooting:
PROB: Password dataset input was counted more than once in one 'enter'/line
FIX: Try changing "time.sleep()" function value in aio.py or data-collection.py (ctrl+F) to 0.5 up to 1.00. This value represents second(s)
PROB: Authentication always rejected/failed/marked as anomalous
FIX: Change the threshold, retrain with fresh dataset, and/or change NUM_REPEATS value
PROB: inconsistent authentication result for a consistent training input (automated input)
FIX: Change contamination_rate in train_model.py to a smaller value, and/or use randomized automated input instead of constant flight and hold times. Fix is in development progress
PROB: Normal dataset training returns inconsistent authentication result (human input)
FIX: Train with fresh dataset, and/or replace default NUM_REPEATS value with higher (>10) value
PROB: GUI crashes after 'enter' or 'authenticate' button usage
FIX: Check scaler.pkl and model.pkl presence in the base directory, absence of one of them could cause crash in the GUI without clear warning/error message; and/or increase delay reset GUI (ctrl+F -> self.after(500, self.self_reset)) value



Roadmap/Next improvements: 
- Flexible Scaler (Automated dataset input could result in consistent authentication result)
- Implementation of SQL query password verification
- Better Flight & Hold times measurement using OS hook (Windows)
- Usage of flexible threshold for higher NUM_REPEATS value
- Bug fixes

Further improvements:
- Usage of Extended Isolation Forest (EIF)
- model.pkl size reduction for mass adoption

For further question/information: contact malvinshu@gmail.com

Thank you