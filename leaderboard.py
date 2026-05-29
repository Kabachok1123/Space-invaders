import json
from dataclasses import asdict, dataclass
from pathlib import Path

from config import LEADERBOARD_FILE, LEADERBOARD_LIMIT


@dataclass(frozen=True)
class ScoreEntry:
    name: str
    score: int
    level: int


class Leaderboard:
    def __init__(self) -> None:
        self.path = Path(LEADERBOARD_FILE)
        self.entries = self.load()

    def add_score(self, name: str, score: int, level: int) -> None:
        if score <= 0:
            return
        saved_name = name.strip()[:10].upper() or "PLAYER"
        self.entries.append(ScoreEntry(saved_name, score, level))
        self.entries = sorted(self.entries, key=lambda entry: entry.score, reverse=True)[:LEADERBOARD_LIMIT]
        self.save()

    def load(self) -> list[ScoreEntry]:
        if not self.path.exists():
            return []
        try:
            raw_entries = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        return [
            ScoreEntry(str(item["name"]), int(item["score"]), int(item["level"]))
            for item in raw_entries
            if isinstance(item, dict) and "name" in item and "score" in item and "level" in item
        ]

    def save(self) -> None:
        data = [asdict(entry) for entry in self.entries]
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
