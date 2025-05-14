import json
import os
import tkinter as tk
from tkinter import ttk


class App:
    def __init__(self, root, voice_recognizer, command_handler):
        self.settings_file = 'settings.json'
        self.__create_settings_file()

        self.voice_recognizer = voice_recognizer
        self.command_handler = command_handler
        self.listening = False

        self.root = root
        self.root.title("WinVoice")
        self.root.geometry("300x300")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.__on_close)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.main_frame = tk.Frame(root, bg="#2c3e50")
        self.settings_frame = tk.Frame(root, bg="#2c3e50")

        self.start_button = None
        self.settings_button = None

    def start(self):
        self.__main_menu()
        self.root.mainloop()

    def __main_menu(self):
        self.settings_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.start_button = tk.Button(self.main_frame, text="Start listening" if not self.listening else "Stop listening",
                                      font=("Arial", 12), width=20, height=4, command=self.__toggle_listening)
        self.start_button.pack(side="top", pady=50)

        self.settings_button = tk.Button(self.main_frame, text="Settings", font=("Arial", 10),
                                         width=10, height=3, command=self.__settings_window)
        self.settings_button.pack(side="bottom", pady=30)

    def __toggle_listening(self):
        self.__toggle_button()
        if not self.listening:
            self.listening = True
            self.__update_output()
            self.voice_recognizer.listen()
            self.start_button["text"] = "Stop listening"
        else:
            self.listening = False
            self.voice_recognizer.stop_listening()
            self.start_button["text"] = "Start listening"

    def __toggle_button(self):
        if self.start_button["state"] == "normal":
            self.start_button["state"] = "disabled"
            self.root.after(2000, self.__toggle_button)
        else:
            self.start_button["state"] = "normal"

    def __create_settings_file(self) -> None:
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'w') as f:
                settings = {
                    "language": "uk-UA",
                    "volume_step": 10,
                    "brightness_step": 10
                }
                f.write(json.dumps(settings))

    def __read_settings_file(self) -> dict | None:
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                return settings

    def __rewrite_settings_file(self, settings: dict) -> None:
        with open(self.settings_file, 'w') as f:
            f.write(json.dumps(settings, ensure_ascii=False))

    def __settings_window(self):
        settings = self.__read_settings_file()
        lang_code = settings['language']
        volume_step = settings['volume_step']
        brightness_step = settings['brightness_step']

        for widget in self.settings_frame.winfo_children():
            widget.destroy()

        self.main_frame.pack_forget()
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        tk.Button(self.settings_frame, text="Back", font=("Arial", 10), width=7, height=1,
                  command=self.__save_settings_button).place(x=10, y=10)

        settings_group = tk.Frame(self.settings_frame, bg="#2c3e50")
        settings_group.pack(pady=50, padx=20, anchor="w")

        tk.Label(settings_group, text="Language:", bg="#2c3e50", fg="white", font=("Arial", 11)).pack(anchor="w", pady=5)
        language_options = ["Українська", "English"]
        self.language_dropdown = ttk.Combobox(settings_group, values=language_options, state="readonly",
                                              font=("Arial", 10), width=20)
        self.language_dropdown.set("English" if lang_code == "en-US" else "Українська")
        self.language_dropdown.pack(anchor="w")

        tk.Label(settings_group, text="Volume step (1-100):", bg="#2c3e50", fg="white", font=("Arial", 11)).pack(anchor="w", pady=5)
        self.volume_entry = tk.Entry(settings_group, font=("Arial", 10), width=10)
        self.volume_entry.insert(0, str(volume_step))
        self.volume_entry.pack(anchor="w")

        tk.Label(settings_group, text="Brightness step (1-100):", bg="#2c3e50", fg="white", font=("Arial", 11)).pack(anchor="w", pady=5)
        self.brightness_entry = tk.Entry(settings_group, font=("Arial", 10), width=10)
        self.brightness_entry.insert(0, str(brightness_step))
        self.brightness_entry.pack(anchor="w")

    def __save_settings_button(self) -> None:
        language = self.language_dropdown.get()
        lang_code = 'en-US' if language == 'English' else 'uk-UA'
        volume_step = self.volume_entry.get()
        brightness_step = self.brightness_entry.get()
        settings = {'language': lang_code,
                    'volume_step': volume_step,
                    'brightness_step': brightness_step}

        self.command_handler.change_settings(settings)
        self.voice_recognizer.switch_language(lang_code)
        self.__rewrite_settings_file(settings)
        self.__main_menu()
        print('Settings saved')

    def __update_output(self):
        if not self.listening:
            return

        text = self.voice_recognizer.get_result()
        if text:
            result = self.command_handler.handle_command(text)
            for r in result:
                print(r)
                if r == "Listening stopped":
                    self.__toggle_listening()
                elif r == "Application closed":
                    self.__on_close()

        self.root.after(500, self.__update_output)

    def __on_close(self):
        self.listening = False
        self.voice_recognizer.stop_listening()
        self.root.destroy()
        print("App closed")
