import logging

logger = logging.getLogger(__name__)


class SpeechToText:
    def __init__(self):
        try:
            import speech_recognition as sr
            self.sr = sr
            self.recognizer = sr.Recognizer()
        except ImportError as exc:
            raise RuntimeError(
                "SpeechRecognition is not installed. Run: pip install -r requirements.txt"
            ) from exc

    def listen(self) -> str:
        with self.sr.Microphone() as source:
            print("\n🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"🗣️  You said: {text}")
            return text
        except self.sr.UnknownValueError:
            print("⚠️  I could not understand the speech.")
            return ""
        except self.sr.RequestError as exc:
            logger.exception("Speech recognition service unavailable")
            print(f"⚠️  Speech service error: {exc}")
            return ""
