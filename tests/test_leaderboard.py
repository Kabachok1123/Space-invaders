from leaderboard import Leaderboard


def test_leaderboard_saves_entered_player_name(tmp_path) -> None:
    leaderboard = Leaderboard()
    leaderboard.path = tmp_path / "scores.json"
    leaderboard.entries = []

    leaderboard.add_score(" alex ", 12, 2)

    assert leaderboard.entries[0].name == "ALEX"


def test_leaderboard_uses_default_name_for_blank_input(tmp_path) -> None:
    leaderboard = Leaderboard()
    leaderboard.path = tmp_path / "scores.json"
    leaderboard.entries = []

    leaderboard.add_score("   ", 12, 2)

    assert leaderboard.entries[0].name == "PLAYER"
