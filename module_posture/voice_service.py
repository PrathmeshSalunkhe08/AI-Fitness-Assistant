import pyttsx3
import queue
import threading
import time

class VoiceService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)
        self.queue = queue.Queue()
        self.last_spoken = 0
        self.interval = 2  # seconds between reminders

        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        while True:
            text = self.queue.get()
            if text:
                self.engine.say(text)
                self.engine.runAndWait()

    def speak_if_needed(self, text):
        now = time.time()
        if now - self.last_spoken >= self.interval:
            self.queue.put(text)
            self.last_spoken = now


# SINGLE GLOBAL INSTANCE
voice_service = VoiceService()
