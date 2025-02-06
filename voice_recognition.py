import queue
import speech_recognition


class VoiceRecognition:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()

        self.commands = queue.Queue()
        self.stop_listening_func = None
        self.listening = False

        with self.microphone as source:
            print("Microphone setting up.")
            self.recognizer.adjust_for_ambient_noise(source)
            print(f"Set minimum energy threshold to {self.recognizer.energy_threshold}")

    def listen(self):
        if not self.listening:
            print("Starting listening.")
            self.listening = True
            self.stop_listening_func = self.recognizer.listen_in_background(self.microphone, self.__callback)

    def __callback(self, recognizer, audio):
        if self.listening:
            try:
                print("Recognizing...")
                text = recognizer.recognize_google(audio, language='uk-UA')
                self.commands.put(text)
                print(f"Recognized: {text}")
            except speech_recognition.UnknownValueError:
                print("Didn't catch that.")
            except speech_recognition.RequestError as e:
                print(f"Couldn't request results from Google Speech Recognition service; {e}")

    def get_result(self):
        if not self.commands.empty():
            return self.commands.get()
        return None

    def stop_listening(self):
        if self.stop_listening_func and self.listening:
            print("Stopping background listening.")
            self.stop_listening_func(wait_for_stop=False)
            self.stop_listening_func = None
            self.commands.queue.clear()
            self.listening = False
