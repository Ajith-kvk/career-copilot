from app.schemas import SkillMatch

WEIGHTS = {"strong": 1.0, "partial": 0.5, "missing": 0.0}


def compute_score(matches: list[SkillMatch]) -> int:
    if not matches:
        return 0
    total = sum(WEIGHTS[m.status] for m in matches)
    return round(100 * total / len(matches))