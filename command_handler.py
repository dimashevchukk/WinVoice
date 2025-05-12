import os
import difflib
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc


class CommandHandler:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        self.commands_ua = {
            # Browser
            "відкрити браузер": self.open_browser,
            "оновити сторінку": self.browser_refresh,
            "домашня сторінка": self.browser_home,
            "вперед": self.browser_forward,
            "назад": self.browser_back,

            # Standard apps
            "відкрити калькулятор": self.open_calculator,
            "закрити калькулятор": self.close_calculator,
            "відкрити блокнот": self.open_notepad,
            "закрити блокнот": self.close_notepad,
            "відкрити провідник": self.open_explorer,
            "закрити провідник": self.close_explorer,
            "відкрити диспетчер завдань": self.open_task_manager,
            "закрити диспетчер завдань": self.close_task_manager,

            # Window control
            "згорнути вікно": self.min_window,
            "розкрити вікно": self.expand_window,
            "закрити вікно": self.close_window,
            "перемкнути вікно": self.switch_window,
            "робочий стіл": self.desktop,  # problem

            # Application
            "зупинити прослуховування": self.stop_listening,
            "закрити додаток": self.close_application,

            # Screenshots
            "знімок екрану": self.take_screenshot,
            "знімок вікна": self.take_screenshot_window,

            # CTRL C/V, clipboard
            "копіювати": self.copy,
            "вставити": self.paste,
            "буфер обміну": self.clipboard,

            # Media
            "пауза": self.pause,
            "наступний трек": self.next_track,
            "попередній трек": self.prev_track,

            # Volume
            "вимкнути звук": self.mute_volume,
            "увімкнути звук": self.unmute_volume,
            "збільшити гучність": self.increase_volume,
            "зменшити гучність": self.decrease_volume,
            "максимальна гучність": self.max_volume,
            "мінімальна гучність": self.min_volume,

            # Brightness
            "максимальна яскравість": self.max_brightness,
            "мінімальна яскравість": self.min_brightness,
            "збільшити яскравість": self.increase_brightness,
            "зменшити яскравість": self.decrease_brightness,

            # Keyboard
            "escape": self.esc,
            "enter": self.enter,
            "capslock": self.capslock,
            "видалити": self.delete,
            "стерти": self.backspace,
            "вирізати": self.cut,
            "відмінити": self.undo,
            "повторно виконати": self.redo,
            "стрілка вгору": self.up,
            "стрілка вниз": self.down,
            "стрілка вліво": self.left,
            "стрілка вправо": self.right,

            # Mouse
            "права кнопка миші": self.click_lmb,
            "ліва кнопка миші": self.click_rmb,
            "середня кнопка миші": self.click_mmb,
            "вгору": self.scroll_up,
            "вниз": self.scroll_down,

            # Power
            "вимкнути комп'ютер": self.shutdown,
            "перезавантажити комп'ютер": self.restart,
            "сплячий режим": self.sleep,
            "заблокувати комп'ютер": self.lock
        }

        self.commands_en = {
            "open browser": self.open_browser,
            "open calculator": self.open_calculator,
            "open notepad": self.open_notepad,
            "open explorer": self.open_explorer,
            "open task_manager": self.open_task_manager,
            "close task_manager": self.close_task_manager,
            "stop listening": self.stop_listening,
            "close application": self.close_application,
            "mute volume": self.mute_volume,
            "unmute volume": self.unmute_volume,
            "increase volume": self.increase_brightness,
        }

        self.commands = self.commands_ua

    def handle_command(self, command_text: str) -> list[str]:
        command_text = command_text.lower()
        executed_commands = []

        exact_matches = [command for command in self.commands.keys() if command in command_text]

        if exact_matches:
            for command in exact_matches:
                result = self.commands[command]()
                executed_commands.append(result)
        else:
            for command, action in self.commands.items():
                if difflib.SequenceMatcher(None, command, command_text).ratio() > 0.85:
                    result = action()
                    executed_commands.append(result)

        return executed_commands if executed_commands else ["No commands recognized"]

    def switch_language(self, lang: str) -> None:
        self.commands = self.commands_ua if lang == 'uk-UA' else self.commands_en

    def open_browser(self):
        os.system("start https://")
        return "Browser opened"

    def browser_refresh(self):
        pyautogui.hotkey("browserrefresh")
        return "Browser Refreshed"

    def browser_home(self):
        pyautogui.hotkey("browserhome")
        return "Browser homepage opened"

    def browser_forward(self):
        pyautogui.hotkey("browserforward")
        return "Browser forward"

    def browser_back(self):
        pyautogui.hotkey("browserback")
        return "Browser back"

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
        # os.system("taskkill /IM taskmgr.exe /F") # works only with admin rights
        os.system("wmic process where name='Taskmgr.exe' call terminate")
        return "Task Manager closed"

    def min_window(self):
        pyautogui.hotkey('win', 'down')
        return "Window minimised"

    def expand_window(self):
        pyautogui.hotkey('win', 'up')
        return "Window expanded"

    def close_window(self):
        pyautogui.hotkey('alt', 'f4')
        return "Window closed"

    def switch_window(self):
        pyautogui.hotkey('alt', 'tab')
        return "Window switched"

    def desktop(self):
        pyautogui.hotkey("win", "d")
        return "Desktop showed"

    def stop_listening(self):
        return "Listening stopped"

    def close_application(self):
        return "Application closed"

    def take_screenshot(self):
        pyautogui.hotkey("printscreen")
        return "Made screenshot of screen"

    def take_screenshot_window(self):
        pyautogui.hotkey("alt", "printscreen")
        return "Made screenshot of window"

    def copy(self):
        pyautogui.hotkey('ctrl', 'c')
        return "Copied"

    def paste(self):
        pyautogui.hotkey('ctrl', 'v')
        return "Pasted"

    def clipboard(self):
        pyautogui.hotkey("win", "v")
        return "Clipboard opened"

    def pause(self):
        pyautogui.press('playpause')
        return "Paused"

    def next_track(self):
        pyautogui.press('nexttrack')
        return "Next track"

    def prev_track(self):
        pyautogui.press('prevtrack')
        return "Previous track"

    def mute_volume(self):
        self.volume.SetMute(1, None)
        return "Volume muted"

    def unmute_volume(self):
        self.volume.SetMute(0, None)
        return "Volume unmuted"

    def increase_volume(self, step=10):
        current = self.volume.GetMasterVolumeLevelScalar() * 100
        new_volume = min(current + step, 100)
        self.volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
        return f"Volume increased to {new_volume}%"

    def decrease_volume(self, step=10):
        current = self.volume.GetMasterVolumeLevelScalar() * 100
        new_volume = max(current - step, 0)
        self.volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
        return f"Volume decreased to {new_volume}%"

    def max_volume(self):
        self.volume.SetMasterVolumeLevelScalar(1.0, None)
        return "Volume set to maximum"

    def min_volume(self):
        self.volume.SetMasterVolumeLevelScalar(0.0, None)
        return "Volume set to minimum"

    def max_brightness(self):
        sbc.set_brightness(100)
        return "Brightness set to maximum"

    def min_brightness(self):
        sbc.set_brightness(0)
        return "Brightness set to minimum"

    def increase_brightness(self, step=10):
        current = sbc.get_brightness()[0]
        new_brightness = min(current + step, 100)
        sbc.set_brightness(new_brightness)
        return f"Brightness increased to {new_brightness}%"

    def decrease_brightness(self, step=10):
        current = sbc.get_brightness()[0]
        new_brightness = max(current - step, 0)
        sbc.set_brightness(new_brightness)
        return f"Brightness decreased to {new_brightness}%"

    def esc(self):
        pyautogui.hotkey('esc')
        return "Esc pressed"

    def enter(self):
        pyautogui.hotkey('enter')
        return "Enter pressed"

    def capslock(self):
        pyautogui.hotkey("capslock")
        return "Capslock pressed"

    def delete(self):
        pyautogui.hotkey("delete")
        return "Delete pressed"

    def backspace(self):
        pyautogui.hotkey("backspace")
        return "Backspace pressed"

    def cut(self):
        pyautogui.hotkey("ctrl", "x")
        return "Cut"

    def undo(self):
        pyautogui.hotkey("ctrl", "z")
        return "Undo"

    def redo(self):
        pyautogui.hotkey("ctrl", "y")
        return "Redo"

    def up(self):
        pyautogui.hotkey("up")
        return "Up arrow pressed"

    def down(self):
        pyautogui.hotkey("down")
        return "Down arrow pressed"

    def left(self):
        pyautogui.hotkey("left")
        return "Left arrow pressed"

    def right(self):
        pyautogui.hotkey("right")
        return "Right arrow pressed"

    def click_lmb(self):
        pyautogui.leftClick()
        return "LMB clicked"

    def click_rmb(self):
        pyautogui.rightClick()
        return "RMB clicked"

    def click_mmb(self):
        pyautogui.middleClick()
        return "MMB clicked"

    def scroll_up(self):
        pyautogui.scroll(300)
        return "Scroll up"

    def scroll_down(self):
        pyautogui.scroll(-300)
        return "Scroll down"

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
