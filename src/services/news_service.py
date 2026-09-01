import logging
import requests
from src.models.article import Article
logger = logging.getLogger(__name__)

class NewsService:
    API_URL = "https://real-time-news-data.p.rapidapi.com/search"
    API_HOST = "real-time-news-data.p.rapidapi.com"
    DEFAULT_QUERY = "Artificial Intelligence, Programming, Machine Learning, Data Science, Python, Computer Engineering"

    def __init__(self, api_key: str, session: requests.Session | None = None) -> None:
        self.api_key = api_key
        self.session = session or requests.Session()

    def get_latest_articles(self) -> list[Article]:
        try:
            response = self.session.get(self.API_URL, headers={"X-RapidAPI-Key": self.api_key, "X-RapidAPI-Host": self.API_HOST}, params={"query": self.DEFAULT_QUERY, "lang": "en", "sort": "date"}, timeout=15)
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException:
            logger.exception("Failed to fetch news from the API.")
            return []
        raw_articles = payload.get("data", []) if isinstance(payload, dict) else payload if isinstance(payload, list) else []
        return [article for article in (Article.from_api(item) for item in raw_articles) if article.url]
