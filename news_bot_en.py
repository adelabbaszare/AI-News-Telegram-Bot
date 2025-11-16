# ~~~{"variant": "standard", "title": "Complete AI News Telegram Bot", "id": "81123"}
import os
import requests
import html
import jdatetime
from datetime import datetime
from time import sleep
from pathlib import Path
import logging
from googletrans import Translator
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "REPLACE_WITH_ENV")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "REPLACE_WITH_ENV")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "REPLACE_WITH_ENV")
SENT_LINKS_FILE = Path("sent_links.txt")

# --- Logging setup ---
logger = logging.getLogger("ai_news_bot")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# --- HTTP session ---
session = requests.Session()


# --- Utility functions ---
def load_sent_links():
    if not SENT_LINKS_FILE.exists():
        return set()
    return set(line.strip() for line in SENT_LINKS_FILE.read_text(encoding="utf-8").splitlines() if line.strip())


def save_sent_link(link):
    with SENT_LINKS_FILE.open("a", encoding="utf-8") as f:
        f.write(link + "\n")


def translate_to_persian(text_to_translate):
    """Translate English text to Persian (Farsi) using googletrans."""
    if not text_to_translate or not isinstance(text_to_translate, str):
        return ""
    try:
        translator = Translator()
        result = translator.translate(text_to_translate, src="en", dest="fa")
        return result.text if result and hasattr(result, "text") else text_to_translate
    except Exception as e:
        logger.error("Translation failed: %s", e)
        return text_to_translate


def is_image_url_ok(url, timeout=8):
    try:
        resp = session.head(url, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return False
        ct = resp.headers.get("Content-Type", "")
        return ct.startswith("image/")
    except Exception as e:
        logger.debug("Image URL check failed: %s", e)
        return False


# --- Core functions ---
def get_latest_ai_news():
    """Fetch latest AI-related news articles from RapidAPI."""
    url = "https://real-time-news-data.p.rapidapi.com/search"
    host = "real-time-news-data.p.rapidapi.com"
    search_query = "Artificial Intelligence, Programming, Machine Learning, Data Science, Python, Computer Engineering"
    querystring = {"query": search_query, "lang": "en", "sort": "date"}
    headers = {"X-RapidAPI-Key": NEWS_API_KEY, "X-RapidAPI-Host": host}
    try:
        resp = session.get(url, headers=headers, params=querystring, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        articles_list = []
        if isinstance(data, dict) and 'data' in data and isinstance(data['data'], list):
            articles_list = data['data']
        elif isinstance(data, list):
            articles_list = data
        else:
            logger.debug("News API JSON keys: %s", list(data.keys()) if isinstance(data, dict) else type(data))
        return articles_list
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching news: %s", e)
        return []
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return []


def format_caption(details):
    """Format HTML caption for Telegram."""
    now_shamsi = jdatetime.datetime.now()
    current_shamsi_datetime_str = now_shamsi.strftime("%Y/%m/%d %H:%M:%S")

    original_title = details.get("title", "No Title")
    original_snippet = details.get("snippet", "")
    persian_title = translate_to_persian(original_title)
    persian_snippet = translate_to_persian(original_snippet)

    safe_title = html.escape(persian_title)
    safe_snippet = html.escape(persian_snippet)
    safe_publisher = html.escape(details.get("source_name", "Unknown Source"))
    link = details.get("link", "")
    safe_link = html.escape(link, quote=True)

    caption = (
        f"📰 <b>{safe_title}</b>\n\n"
        f"📝 {safe_snippet}\n\n"
        f"🌐 <a href=\"{safe_link}\"><b>متن کامل مقاله</b></a>\n"
        f"<b>✍🏻 منبع:</b> {safe_publisher}\n"
        f"<b>🕰 تاریخ:</b> {current_shamsi_datetime_str}\n"
        f"🆔 <a href=\"https://t.me/LearnwithAdel\"><b>LearnwithAdel</b></a>"
    )
    # Telegram caption limit
    if len(caption) > 1024:
        caption = caption[:1020] + "..."
    return caption


def send_photo_to_telegram(details):
    """Send article image and caption to Telegram."""
    image_url = details.get("photo_url")
    if not image_url or not is_image_url_ok(image_url):
        logger.info("Skipping article, no valid image: '%s'", details.get("title"))
        return False

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": image_url,
        "caption": format_caption(details),
        "parse_mode": "HTML"
    }
    try:
        resp = session.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto", json=payload, timeout=30)
        resp.raise_for_status()
        logger.info("Photo sent successfully to Telegram!")
        return True
    except requests.exceptions.RequestException as e:
        logger.error("Error sending photo: %s", e)
        return False


def main_job():
    """Main job: fetch news, check sent links, send new articles to Telegram."""
    logger.info("=== Running main job at %s ===", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sent_links = load_sent_links()
    articles = get_latest_ai_news()
    if not articles:
        logger.warning("No articles retrieved from API.")
        return
    for article in articles:
        link = article.get("link")
        if not link or link in sent_links:
            continue
        success = send_photo_to_telegram(article)
        if success:
            save_sent_link(link)
            break  # send one per run


# --- Run bot ---
if __name__ == "__main__":
    logger.info("Bot started successfully.")
    # first immediate run
    main_job()

    # schedule periodic run
    import schedule

    schedule.every(2).minutes.do(main_job)
    logger.info("Scheduling every 2 minutes...")

    while True:
        schedule.run_pending()
        sleep(60)

