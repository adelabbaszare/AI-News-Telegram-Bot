from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Article:
    title: str
    url: str
    snippet: str = ""
    source: str = "Unknown Source"
    image_url: str | None = None
    related_topics: list[Any] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Article":
        return cls(
            title=data.get("title") or "No Title",
            url=data.get("link") or "",
            snippet=data.get("snippet") or "",
            source=data.get("source_name") or "Unknown Source",
            image_url=data.get("photo_url"),
            related_topics=data.get("related_topics") or [],
        )
