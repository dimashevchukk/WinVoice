import tkinter as tk
from tkinter import ttk


class App:
    def __init__(self, root, voice_recognizer, command_handler):
        self.voice_recognizer = voice_recognizer
        self.command_handler = command_handler
        self.listening = False

        self.language = tk.StringVar(value="uk")

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

        self.__update_output()
        self.__main_menu()

    def start(self):
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
                                         width=10, height=3, command=self.__settings)
        self.settings_button.pack(side="bottom", pady=30)

    def __toggle_listening(self):
        self.__toggle_button()
        if not self.listening:
            self.listening = True
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

    def __settings(self):
        for widget in self.settings_frame.winfo_children():
            widget.destroy()

        self.main_frame.pack_forget()
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        tk.Button(self.settings_frame, text="Back", font=("Arial", 10), width=7, height=1,
                  command=self.__main_menu).place(x=10, y=10)

        language_frame = tk.Frame(self.settings_frame, bg="#2c3e50")
        language_frame.pack(pady=50)

        tk.Label(language_frame, text="Language:", bg="#2c3e50", fg="white", font=("Arial", 11)).pack(side=tk.LEFT, padx=10)

        language_options = ["Українська", "English"]
        self.language_dropdown = ttk.Combobox(language_frame, values=language_options, state="readonly", font=("Arial", 10), width=15)
        self.language_dropdown.set("Українська" if self.language.get() == "uk" else "English")
        self.language_dropdown.pack(side=tk.LEFT)
        self.language_dropdown.bind("<<ComboboxSelected>>", self.__apply_language)
    
    def __apply_language(self):
        selected_language = self.language_dropdown.get()
        lang_code = "uk" if selected_language == "Українська" else "en"
        self.language.set(lang_code)
        self.command_handler.switch_language(lang_code)
        print(f"Language switched to: {lang_code}")

    def __update_output(self):
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
