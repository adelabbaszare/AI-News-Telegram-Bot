import requests
import os
import schedule
import time
import html
import jdatetime
from datetime import datetime
import asyncio
from googletrans import Translator
from dotenv import load_dotenv

# --- بارگذاری متغیرهای محیطی ---
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SENT_LINKS_FILE = "sent_links.txt"

if not all([NEWS_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    print("خطا: یک یا چند متغیر محیطی (API Key, Bot Token, Chat ID) تنظیم نشده‌اند.")
    exit()

# --- صف سراسری برای نگهداری مقالات ---
article_queue = []
RLM = "\u200f"  # کاراکتر راست‌چین‌سازی


# --- توابع مدیریت فایل، ترجمه، دریافت اخبار، هشتگ (بدون تغییر) ---

def load_sent_links():
    if not os.path.exists(SENT_LINKS_FILE):
        return set()
    with open(SENT_LINKS_FILE, "r", encoding='utf-8') as f:
        return set(line.strip() for line in f)


def save_sent_link(link):
    with open(SENT_LINKS_FILE, "a", encoding='utf-8') as f:
        f.write(link + "\n")


async def _translate_texts_parallel(texts_to_translate):
    translator = Translator()
    tasks = [translator.translate(text, src='en', dest='fa') for text in texts_to_translate if text]
    translations = await asyncio.gather(*tasks)
    return [t.text for t in translations]


def translate_article_details(title, snippet):
    try:
        results = asyncio.run(_translate_texts_parallel([title, snippet]))
        persian_title = results[0] if len(results) > 0 else title
        persian_snippet = results[1] if len(results) > 1 else snippet
        return persian_title, persian_snippet
    except Exception as e:
        print(f"خطا در هنگام ترجمه موازی: {e}")
        return title, snippet


def get_latest_ai_news():
    url = "https://real-time-news-data.p.rapidapi.com/search"
    host = "real-time-news-data.p.rapidapi.com"
    search_query = "Artificial Intelligence, Programming, Machine Learning, Data Science, Python, Computer Engineering"
    querystring = {"query": search_query, "lang": "en", "sort": "date"}
    headers = {"X-RapidAPI-Key": NEWS_API_KEY, "X-RapidAPI-Host": host}
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles_list = data.get('data', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        if not articles_list:
            print("API call successful, but no articles were found.")
            return []
        processed_articles = []
        for article in articles_list:
            processed_articles.append({
                "title": article.get('title', 'No Title'),
                "link": article.get('link', '#'),
                "snippet": article.get('snippet', ''),
                "publisher": article.get('source_name', 'Unknown Source'),
                "image_url": article.get('photo_url'),
                "related_topics": article.get('related_topics', [])
            })
        return processed_articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


def generate_hashtags(topics):
    if not topics or not isinstance(topics, list):
        return ""
    hashtags = []
    for topic in topics[:5]:
        topic_name = ""
        if isinstance(topic, str):
            topic_name = topic
        elif isinstance(topic, dict) and 'name' in topic:
            topic_name = topic['name']
        if topic_name:
            clean_tag = topic_name.replace(' ', '_').replace('-', '_')
            clean_tag = ''.join(c for c in clean_tag if c.isalnum() or c == '_')
            if clean_tag:
                hashtags.append(f"#{clean_tag}")
    return " ".join(hashtags)


def send_article_to_telegram(details, persian_title, persian_snippet):
    now_shamsi = jdatetime.datetime.now()
    current_shamsi_datetime_str = now_shamsi.strftime("%Y/%m/%d %H:%M")
    safe_title = html.escape(persian_title)
    safe_snippet = html.escape(persian_snippet)
    safe_publisher = html.escape(details.get('publisher', 'Unknown Source'))
    hashtags = generate_hashtags(details.get('related_topics', []))

    message_text = (
        f"{RLM}🎨 <b>{safe_title}</b>\n\n"
        f"● {safe_snippet}...\n\n"
        f"☑️ <b>جزئیات بیشتر:</b>\n"
        f"● <b>منبع:</b> {safe_publisher}\n"
        f"● <b>تاریخ:</b> {current_shamsi_datetime_str}\n\n"
        f"┌ 🔗 <b>لینک اصلی</b>\n"
        f"└ 🌐 <a href=\"{details['link']}\">مشاهده متن کامل مقاله</a>\n\n"
        f"{hashtags}\n"
        f"<b>🫟@LearnwithAdel</b>"
    )
    image_url = details.get('image_url')
    if image_url:
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
                json={"chat_id": TELEGRAM_CHAT_ID, "photo": image_url, "caption": message_text, "parse_mode": "HTML"},
                timeout=30
            )
            response.raise_for_status()
            print(f"Article '{safe_title}' sent successfully (with photo).")
            return True
        except requests.exceptions.RequestException:
            print(f"Failed to send with photo. Trying as text message...")

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message_text, "parse_mode": "HTML",
                  "disable_web_page_preview": False},
            timeout=20
        )
        response.raise_for_status()
        print(f"Article '{safe_title}' sent successfully (as text).")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending text message to Telegram: {e}")
        return False


# --- بخش جدید: توابع مدیریت صف ---

def fill_queue_if_empty():
    """
    اگر صف خالی باشد، API را چک کرده و مقالات جدید را به صف اضافه می‌کند.
    """
    global article_queue

    # فقط اگر صف خالی است، مقالات جدید را واکشی کن
    if not article_queue:
        print("صف خالی است. در حال بررسی برای مقالات جدید...")
        sent_links = load_sent_links()
        articles_to_check = get_latest_ai_news()

        if not articles_to_check:
            print("مقاله‌ای برای افزودن به صف پیدا نشد.")
            return

        new_articles_to_queue = []
        for article in articles_to_check:
            article_link = article.get("link")
            if not article_link or article_link == '#':
                continue
            if article_link in sent_links:
                continue

            # اگر مقاله جدید بود، آن را به لیست موقت اضافه کن
            new_articles_to_queue.append(article)

        # مقالات را معکوس کنید تا قدیمی‌ترین خبر (که در انتهای لیست API است)
        # اول ارسال شود.
        new_articles_to_queue.reverse()
        article_queue = new_articles_to_queue

        if article_queue:
            print(f"{len(article_queue)} مقاله جدید به صف اضافه شد.")
        else:
            print("مقاله جدیدی (که قبلا ارسال نشده باشد) پیدا نشد.")
    else:
        print(f"{len(article_queue)} مقاله از قبل در صف وجود دارد. از واکشی صرف نظر شد.")


def process_one_article_from_queue():
    """
    یک مقاله از صف برداشته، ترجمه و ارسال می‌کند.
    """
    global article_queue

    if not article_queue:
        print("صف خالی است. مقاله‌ای برای ارسال وجود ندارد.")
        return

    # اولین مقاله را از صف بردار (FIFO)
    article = article_queue.pop(0)
    article_link = article.get("link")

    print(f"در حال پردازش مقاله از صف: '{article['title']}'")

    # اطمینان مجدد از اینکه لینک قبلا ارسال نشده
    # (برای مواقعی که ربات ریستارت می‌شود و فایل لینک‌ها آپدیت شده)
    sent_links = load_sent_links()
    if article_link in sent_links:
        print("این مقاله در فایل sent_links موجود بود. رد شدن...")
        return

    print("در حال ترجمه محتوا...")
    persian_title, persian_snippet = translate_article_details(
        article.get('title', 'No Title'),
        article.get('snippet', '')
    )

    success = send_article_to_telegram(article, persian_title, persian_snippet)

    if success:
        save_sent_link(article_link)
        print("مقاله با موفقیت ارسال و لینک ذخیره شد.")
    else:
        print(f"خطا در ارسال مقاله: '{persian_title}'.")
        # اگر ارسال ناموفق بود، آن را به ابتدای صف برگردان تا دوباره تلاش شود
        article_queue.insert(0, article)
        print("مقاله به ابتدای صف بازگردانده شد تا در چرخه بعدی مجددا تلاش شود.")


# --- تابع اصلی زمان‌بندی (جدید) ---
def main_task_to_schedule():
    """
    این تابع اصلی است که توسط schedule اجرا می‌شود.
    ابتدا صف را در صورت نیاز پر می‌کند، سپس یک آیتم را ارسال می‌کند.
    """
    print(f"--- اجرای وظیفه زمان‌بندی شده در {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    try:
        fill_queue_if_empty()
        process_one_article_from_queue()
    except Exception as e:
        print(f"خطای عمومی در اجرای وظیفه اصلی: {e}")
    print("--- وظیفه زمان‌بندی شده کامل شد ---")


if __name__ == "__main__":

    # --- ⚙️ بخش تنظیمات شما ---
    # در اینجا مشخص کنید که هر چند دقیقه یک پست ارسال شود
    POST_INTERVAL_MINUTES = 1
    # ---------------------------

    print("ربات با موفقیت شروع به کار کرد.")
    print(f"شناسه چت: {TELEGRAM_CHAT_ID}")
    print(f"تنظیم زمان‌بندی: ارسال یک پست در هر {POST_INTERVAL_MINUTES} دقیقه.")

    # --- حذف اجرای فوری ---
    # دیگر main_job() را بلافاصله اجرا نمی‌کنیم
    # print("Running the first check immediately...")
    # main_job() # <<< این خط حذف شد

    # زمان‌بندی وظیفه اصلی بر اساس تنظیمات شما
    schedule.every(POST_INTERVAL_MINUTES).minutes.do(main_task_to_schedule)

    print("زمان‌بندی کامل شد. ربات در حال اجراست و منتظر زمان اولین ارسال...")

    while True:
        schedule.run_pending()
        time.sleep(1)