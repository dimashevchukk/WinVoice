import tkinter as tk
from UI import App
from voice_recognition import VoiceRecognizer
from command_handler import CommandHandler


if __name__ == '__main__':
    root = tk.Tk()
    vr = VoiceRecognizer()
    ch = CommandHandler()
    app = App(root, vr, ch)
    app.start()
