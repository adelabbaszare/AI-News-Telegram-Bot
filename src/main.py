import logging
import time

import schedule

from src.config import Settings
from src.repositories.sent_links_repository import SentLinksRepository
from src.services.news_service import NewsService
from src.services.telegram_service import TelegramService
from src.services.translation_service import TranslationService
from src.utils.formatter import build_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


class NewsBot:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.news_service = NewsService(settings.news_api_key)
        self.telegram_service = TelegramService(settings)
        self.translation_service = TranslationService()
        self.sent_links = SentLinksRepository()

    def run_once(self) -> None:
        logger.info("Checking for new articles.")
        sent = self.sent_links.load()

        for article in reversed(self.news_service.get_latest_articles()):
            if article.url in sent:
                continue

            title = self.translation_service.translate(article.title)
            snippet = self.translation_service.translate(article.snippet)
            message = build_message(article, title, snippet, self.settings)

            if self.telegram_service.send_article(article, message):
                self.sent_links.add(article.url)
                logger.info("Article sent successfully: %s", article.title)
                return

        logger.info("No new articles were sent.")


def main() -> None:
    settings = Settings.from_env()
    bot = NewsBot(settings)
    bot.run_once()
    schedule.every(settings.post_interval_minutes).minutes.do(bot.run_once)

    logger.info("Bot started. Interval: %s minutes.", settings.post_interval_minutes)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
