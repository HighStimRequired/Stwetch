import tkinter as tk
from tkinter import ttk, filedialog
from threading import Thread
import time
import winsound
import os

class StwetchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stwetch")
        self.root.geometry("240x320")
        
        # Cozy dark theme setup
        self.root.configure(bg="#111111")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#111111", foreground="white", font=("Helvetica", 12), padding=10)
        style.map("TButton", background=[("active", "#111111")])

        style.configure("TLabel", background="#111111", foreground="white", font=("Helvetica", 14))

        self.running = False
        self.custom_sound_path = None
        
        # Label
        self.label = ttk.Label(root, text="STWETCH THAT BODY", anchor="center")
        self.label.pack(pady=20)

        # Timer status label
        self.status_label = ttk.Label(root, text="Status: Stopped", anchor="center", foreground="red")
        self.status_label.pack(pady=10)

        # Buttons
        self.start_button = ttk.Button(root, text="Start", command=self.start_reminder)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_reminder)
        self.stop_button.pack(pady=10)

        self.sound_button = ttk.Button(root, text="Choose Sound", command=self.choose_sound)
        self.sound_button.pack(pady=10)

        # Thread to handle the timer
        self.thread = None

    def play_sound(self):
        try:
            if self.custom_sound_path and os.path.exists(self.custom_sound_path):
                winsound.PlaySound(self.custom_sound_path, winsound.SND_FILENAME)
            else:
                winsound.Beep(440, 500)  # Default beep sound
        except Exception as e:
            print("Error playing sound:", e)

    def reminder(self):
        while self.running:
            time.sleep(30 * 60)  # 30 minutes
            if self.running:
                self.play_sound()

    def start_reminder(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: Running", foreground="green")
            self.thread = Thread(target=self.reminder, daemon=True)
            self.thread.start()

    def stop_reminder(self):
        self.running = False
        self.status_label.config(text="Status: Stopped", foreground="red")

    def choose_sound(self):
        file_path = filedialog.askopenfilename(title="Select Sound File", filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.custom_sound_path = file_path

if __name__ == "__main__":
    root = tk.Tk()
    app = StwetchApp(root)
    root.mainloop()
