import os
import difflib


class CommandHandler:
    def __init__(self):
        self.commands = {
            "відкрити браузер": self.open_browser,
            "відкрити калькулятор": self.open_calculator,
            "відкрити блокнот": self.open_notepad,
            "відкрити провідник": self.open_explorer,
            "відкрити диспетчер завдань": self.open_task_manager,

            "вимкнути комп'ютер": self.shutdown,
            "перезавантажити комп'ютер": self.restart,
            "сплячий режим": self.sleep,
            "заблокувати комп'ютер": self.lock
        }

    def handle_command(self, command_text):
        command_text = command_text.lower()
        executed_commands = []

        for command, action in self.commands.items():
            # Use fuzzy matching with a similarity threshold
            if difflib.SequenceMatcher(None, command, command_text).ratio() > 0.7 or command in command_text:
                result = action()
                executed_commands.append(result)

        return executed_commands if executed_commands else ["No commands recognized"]

    def open_browser(self):
        os.system("start https://")
        return "Browser opened"

    def open_calculator(self):
        os.system("start calc")
        return "Calculator opened"

    def close_calculator(self):
        os.system("taskkill /IM CalculatorApp.exe /F")
        return "Calculator closed"

    def open_notepad(self):
        os.system("start notepad")
        return "Notepad opened"

    def close_notepad(self):
        os.system("taskkill /IM notepad.exe /F")
        return "Notepad closed"

    def open_explorer(self):
        os.system("start explorer")
        return "Explorer opened"

    def close_explorer(self):
        os.system("taskkill /IM explorer.exe /F && start explorer")
        return "Explorer restarted"

    def open_task_manager(self):
        os.system("start taskmgr")
        return "Task Manager opened"

    def close_task_manager(self):
        os.system("taskkill /IM taskmgr.exe /F")
        return "Task Manager closed"

    def shutdown(self):
        os.system("shutdown /s /t 1")
        return "Shutting down"

    def restart(self):
        os.system("shutdown /r /t 1")
        return "Restarting"

    def sleep(self):
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Sleep mode"

    def lock(self):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Computer locked"
