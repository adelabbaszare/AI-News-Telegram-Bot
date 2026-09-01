from src.repositories.sent_links_repository import SentLinksRepository


def test_sent_links_repository_persists_links(tmp_path) -> None:
    path = tmp_path / "sent_links.txt"
    repository = SentLinksRepository(path)

    repository.add("https://example.com/article")

    assert repository.contains("https://example.com/article")
    assert repository.load() == {"https://example.com/article"}
