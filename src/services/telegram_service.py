import logging

import requests

from src.config import Settings
from src.models.article import Article

logger = logging.getLogger(__name__)


class TelegramService:
    API_BASE_URL = "https://api.telegram.org"

    def __init__(
        self,
        settings: Settings,
        session: requests.Session | None = None,
    ) -> None:
        self.settings = settings
        self.session = session or requests.Session()

    @property
    def _base_url(self) -> str:
        return f"{self.API_BASE_URL}/bot{self.settings.telegram_bot_token}"

    def send_article(self, article: Article, message: str) -> bool:
        if article.image_url and self._send_photo(article.image_url, message):
            return True
        return self._send_message(message)

    def _send_photo(self, image_url: str, caption: str) -> bool:
        try:
            response = self.session.post(
                f"{self._base_url}/sendPhoto",
                json={
                    "chat_id": self.settings.telegram_chat_id,
                    "photo": image_url,
                    "caption": caption,
                    "parse_mode": "HTML",
                },
                timeout=30,
            )
            response.raise_for_status()
            return True
        except requests.RequestException:
            logger.warning("Sending photo failed; falling back to text message.")
            return False

    def _send_message(self, text: str) -> bool:
        try:
            response = self.session.post(
                f"{self._base_url}/sendMessage",
                json={
                    "chat_id": self.settings.telegram_chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False,
                },
                timeout=30,
            )
            response.raise_for_status()
            return True
        except requests.RequestException:
            logger.exception("Failed to send message to Telegram.")
            return False
