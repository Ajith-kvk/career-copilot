from app.schemas import SkillMatch
from app.scoring import compute_score


def m(status):
    return SkillMatch(skill="x", status=status)


def test_all_strong_is_100():
    assert compute_score([m("strong"), m("strong")]) == 100


def test_mixed_scores_average():
    assert compute_score([m("strong"), m("partial"), m("missing"), m("missing")]) == 38


def test_empty_is_zero():
    assert compute_score([]) == 0