import sys
import os
import time
from threading import Thread
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QSlider, QVBoxLayout, QWidget, QFileDialog
)
from PyQt5.QtCore import Qt
import pygame

class StwetchApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stwetch")
        self.setGeometry(100, 100, 250, 200)

        # Initialize pygame mixer
        pygame.mixer.init()
        
        self.running = False
        self.custom_sound_path = None

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Apply dark theme with forest green accents
        self.setStyleSheet(
            "background-color: #1a1a1a; color: white;"
            "QLabel { font-size: 16px; font-weight: bold; }"
            "QPushButton { background-color: #2e3d2f; color: white; font-size: 14px; border: 1px solid #3a5a40; border-radius: 5px; padding: 5px; }"
            "QPushButton:hover { background-color: #3a5a40; }"
            "QSlider::groove:horizontal { background-color: #2e3d2f; height: 8px; border-radius: 4px; }"
            "QSlider::handle:horizontal { background-color: #3a5a40; width: 16px; height: 16px; border-radius: 8px; margin: -4px 0; }"
            "QSlider::sub-page:horizontal { background-color: #3a5a40; border-radius: 4px; }"
        )

        # Title label
        self.label = QLabel("STWETCH THAT BODY", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Timer status label
        self.status_label = QLabel("Status: Stopped", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)

        # Start button
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_reminder)
        layout.addWidget(self.start_button)

        # Stop button
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_reminder)
        layout.addWidget(self.stop_button)

        # Choose sound button
        self.sound_button = QPushButton("Choose Sound", self)
        self.sound_button.clicked.connect(self.choose_sound)
        layout.addWidget(self.sound_button)

        # Volume slider and label
        self.volume_label = QLabel("Volume: 50%", self)
        self.volume_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)  # Default volume
        self.volume_slider.valueChanged.connect(self.set_volume)
        layout.addWidget(self.volume_slider)

    def play_sound(self):
        try:
            if self.custom_sound_path and os.path.exists(self.custom_sound_path):
                pygame.mixer.music.load(self.custom_sound_path)
                pygame.mixer.music.play()
            else:
                print("No custom sound selected or file not found.")
        except Exception as e:
            print("Error playing sound:", e)

    def set_volume(self, value):
        volume = value / 100.0
        pygame.mixer.music.set_volume(volume)
        self.volume_label.setText(f"Volume: {value}%")

    def reminder(self):
        while self.running:
            time.sleep(30 * 60)  # 30 minutes
            if self.running:
                self.play_sound()

    def start_reminder(self):
        if not self.running:
            self.running = True
            self.status_label.setText("Status: Running")
            self.status_label.setStyleSheet("color: #3a5a40;")
            self.thread = Thread(target=self.reminder, daemon=True)
            self.thread.start()

    def stop_reminder(self):
        self.running = False
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet("color: red;")

    def choose_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Sound File", "", "Audio Files (*.wav *.mp3 *.ogg)")
        if file_path:
            self.custom_sound_path = file_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StwetchApp()
    window.show()
    sys.exit(app.exec_())
