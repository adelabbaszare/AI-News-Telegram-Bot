from pathlib import Path


class SentLinksRepository:
    def __init__(self, path: str | Path = "sent_links.txt") -> None:
        self.path = Path(path)

    def load(self) -> set[str]:
        if not self.path.exists():
            return set()

        return {
            line.strip()
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    def contains(self, url: str) -> bool:
        return url in self.load()

    def add(self, url: str) -> None:
        with self.path.open("a", encoding="utf-8") as file:
            file.write(f"{url}\n")
