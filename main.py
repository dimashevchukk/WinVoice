import tkinter as tk
import customtkinter as ctk
from UI import MainWindow
from voice_recognition import VoiceRecognition
from command_handler import CommandHandler

if __name__ == '__main__':
    root = ctk.CTk()
    vr = VoiceRecognition()
    ch = CommandHandler()
    app = MainWindow(root, vr, ch)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
