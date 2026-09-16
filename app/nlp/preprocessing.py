import re


class TextPreprocessor:
    """Basic NLP preprocessing suitable for a transparent lab demonstration."""

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s:.-]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    @staticmethod
    def tokenize(text: str) -> list[str]:
        return TextPreprocessor.normalize(text).split()

    @staticmethod
    def remove_fillers(text: str) -> str:
        fillers = {
            "please", "kindly", "can", "could", "would",
            "i", "want", "to", "my", "me"
        }
        tokens = TextPreprocessor.tokenize(text)
        return " ".join(token for token in tokens if token not in fillers)
