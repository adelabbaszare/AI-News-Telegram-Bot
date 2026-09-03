import html

import jdatetime

from src.config import Settings
from src.models.article import Article


def generate_hashtags(topics: list[object], limit: int = 5) -> str:
    hashtags: list[str] = []
    for topic in topics[:limit]:
        if isinstance(topic, str):
            name = topic
        elif isinstance(topic, dict):
            name = topic.get("name", "")
        else:
            name = ""

        normalized_chars = []
        for character in name.replace(" ", "_").replace("-", "_"):
            if character.isalnum() or character == "_":
                normalized_chars.append(character)

        normalized = "".join(normalized_chars)
        if normalized:
            hashtags.append(f"#{normalized}")
    return " ".join(hashtags)


def build_message(
    article: Article,
    translated_title: str,
    translated_snippet: str,
    settings: Settings,
) -> str:
    date = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    title = html.escape(translated_title)
    snippet = html.escape(translated_snippet)
    source = html.escape(article.source)
    url = html.escape(article.url, quote=True)
    hashtags = generate_hashtags(article.related_topics)

    return (
        f"🎨 <b>{title}</b>\n\n● {snippet}\n\n"
        f"☑️ <b>جزئیات بیشتر:</b>\n"
        f"● <b>منبع:</b> {source}\n"
        f"● <b>تاریخ:</b> {date}\n\n"
        f"┌ 🔗 <b>لینک اصلی</b>\n"
        f'└ 🌐 <a href="{url}">مشاهده متن کامل مقاله</a>\n\n'
        f"{hashtags}\n"
        f"<b>🫟{html.escape(settings.channel_username)}</b>"
    )
