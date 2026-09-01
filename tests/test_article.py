from src.models.article import Article


def test_article_from_api_maps_expected_fields() -> None:
    article = Article.from_api(
        {
            "title": "AI breakthrough",
            "link": "https://example.com/article",
            "snippet": "Summary",
            "source_name": "Example News",
            "photo_url": "https://example.com/image.jpg",
            "related_topics": ["AI"],
        }
    )

    assert article.title == "AI breakthrough"
    assert article.url == "https://example.com/article"
    assert article.source == "Example News"
    assert article.related_topics == ["AI"]
