import logging
from googletrans import Translator
logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self) -> None:
        self.translator = Translator()

    def translate(self, text: str) -> str:
        if not text:
            return ""
        try:
            result = self.translator.translate(text, src="en", dest="fa")
            return result.text if result and result.text else text
        except Exception:
            logger.exception("Translation failed.")
            return text
