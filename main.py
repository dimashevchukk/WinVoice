import tkinter as tk
from UI import App
from voice_recognition import VoiceRecognition
from command_handler import CommandHandler


if __name__ == '__main__':
    root = tk.Tk()
    vr = VoiceRecognition()
    ch = CommandHandler()
    app = App(root, vr, ch)
    app.start()
