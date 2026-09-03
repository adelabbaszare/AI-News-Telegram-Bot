import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    news_api_key: str
    telegram_bot_token: str
    telegram_chat_id: str
    post_interval_minutes: int = 5
    channel_username: str = "@LearnwithAdel"

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        settings = cls(
            news_api_key=os.getenv("NEWS_API_KEY", ""),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
            post_interval_minutes=int(os.getenv("POST_INTERVAL_MINUTES", "5")),
            channel_username=os.getenv("CHANNEL_USERNAME", "@LearnwithAdel"),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        missing = [
            name
            for name, value in {
                "NEWS_API_KEY": self.news_api_key,
                "TELEGRAM_BOT_TOKEN": self.telegram_bot_token,
                "TELEGRAM_CHAT_ID": self.telegram_chat_id,
            }.items()
            if not value
        ]
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        if self.post_interval_minutes <= 0:
            raise ValueError("POST_INTERVAL_MINUTES must be greater than zero.")
