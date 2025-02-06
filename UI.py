import tkinter as tk


class MainWindow:
    def __init__(self, root, voice_recognizer, command_handler):
        self.root = root
        self.voice_recognizer = voice_recognizer
        self.command_handler = command_handler

        self.root.title("WinVoice")
        self.root.geometry("300x300")

        self.start_button = tk.Button(root, text="Start listening", command=self.toggle_listening, width=10, height=5)
        self.start_button.pack(pady=50)

        self.listening = False

        self.__update_output()

    def toggle_listening(self):
        self.__toggle_button()
        if not self.listening:
            self.listening = True
            self.voice_recognizer.listen()
            self.start_button["text"] = "Stop listening"
        else:
            self.listening = False
            self.voice_recognizer.stop_listening()
            self.start_button["text"] = "Start listening"

    def __update_output(self):
        text = self.voice_recognizer.get_result()
        if text:
            result = self.command_handler.handle_command(text)
            print(result[0])
        self.root.after(500, self.__update_output)

    def __toggle_button(self):
        if self.start_button["state"] == "normal":
            self.start_button["state"] = "disabled"
            self.root.after(2000, self.__toggle_button)
        else:
            self.start_button["state"] = "normal"

    def on_close(self):
        self.listening = False
        self.voice_recognizer.stop_listening()
        self.root.destroy()
        print("App closed.")
