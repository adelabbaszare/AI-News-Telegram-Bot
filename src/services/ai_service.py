from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Protocol

import requests

from src.config import Settings
from src.models.article import Article

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class AIResult:
    title_fa: str
    summary_fa: str
    tags_fa: tuple[str, ...]
    provider: str

class AIProvider(Protocol):
    name: str

    def transform(self, article: Article) -> AIResult:
        ...

SYSTEM_PROMPT = '''
تو یک ویراستار علمی فارسی هستی.
فقط بر اساس متن ورودی ترجمه و خلاصه کن و هیچ واقعیت یا عددی را تغییر نده.
'''

def _parse_result(content: str, provider: str) -> AIResult:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
        cleaned = cleaned.removesuffix("```").strip()
    data = json.loads(cleaned)
    title = str(data["title_fa"]).strip()
    summary = str(data["summary_fa"]).strip()
    tags = tuple(str(item).strip() for item in data.get("tags_fa", []) if str(item).strip())
    if not title or not summary:
        raise ValueError("AI response did not contain a usable title and summary.")
    return AIResult(title_fa=title, summary_fa=summary, tags_fa=tags[:5], provider=provider)