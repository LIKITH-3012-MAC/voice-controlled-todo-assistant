import logging

logger = logging.getLogger(__name__)


class TextToSpeech:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.engine = None
        if enabled:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 165)
            except Exception:
                logger.warning("TTS unavailable; continuing in text-only mode.")
                self.engine = None

    def speak(self, text: str) -> None:
        print(f"🤖 Assistant: {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                logger.exception("TTS playback failed")
