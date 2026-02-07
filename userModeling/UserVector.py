
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Union


@dataclass
class StanceEntry:
    """One stance: value (required) and optional confidence."""
    value: float  # -1 (against) to 1 (for)
    confidence: float = 1.0  # 0 to 1

    def __post_init__(self):
        self.value = max(-1.0, min(1.0, self.value))
        self.confidence = max(0.0, min(1.0, self.confidence))


# Decay: learning rate = decay_constant / (decay_constant + n_engaged).
# More engagements -> smaller updates. Tune as needed.
_DECAY_CONSTANT = 2.0
_DISLIKE_STRENGTH_FACTOR = 0.6  # Dislike moves less than like (avoid over-interpreting)


class UserVector:
    """
    User vector: user_id + a map of stances.
    stances: entity/topic name -> StanceEntry
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.stances: Dict[str, StanceEntry] = {}
        self.n_articles_engaged: int = 0  # Number of like/dislike so far (for decay)

    def set_stance(self, entity: str, value: float, confidence: float = 1.0) -> None:
        """Set (or overwrite) stance for an entity."""
        self.stances[entity] = StanceEntry(value=value, confidence=confidence)

    def get_stance(self, entity: str) -> Optional[StanceEntry]:
        """Get stance entry for an entity, or None."""
        return self.stances.get(entity)

    def get_value(self, entity: str, default: float = 0.0) -> float:
        """Get stance value for an entity, or default."""
        entry = self.stances.get(entity)
        return entry.value if entry else default

    def distance_to(self, article_stances: Dict[str, float]) -> float:
        """
        Euclidean distance to an article's stance vector.
        Only dimensions present in both user and article are used.
        Lower = more similar. Returns inf if no overlap.
        """
        if not article_stances:
            return float("inf")
        common = set(self.stances.keys()) & set(article_stances.keys())
        if not common:
            return float("inf")
        diff_sq = sum(
            (self.get_value(e) - article_stances[e]) ** 2 for e in common
        )
        return diff_sq ** 0.5

    def top_k(
        self,
        articles: Union[Dict, List[Dict[str, float]]],
        k: int,
        *,
        closest: bool = True,
        farthest: bool = True,
    ) -> Dict[str, List[tuple]]:
        """
        Find the top k closest and/or farthest articles to this user's vector.

        Args:
            articles: Either a dict mapping article_id -> stance_dict, or a list
                      of stance dicts (article_id = index).
            k: Number of articles to return for each side.
            closest: If True, include top k closest (most agreeable).
            farthest: If True, include top k farthest (most disagreeable).

        Returns:
            Dict with "closest" and/or "farthest", each a list of (article_id, distance).
        """
        # Normalize to list of (id, stance_dict)
        if isinstance(articles, dict):
            items = list(articles.items())
        else:
            items = list(enumerate(articles))

        with_distance = [(aid, self.distance_to(stances)) for aid, stances in items]
        # Drop inf (no overlap) so they don't dominate
        with_distance = [(aid, d) for aid, d in with_distance if d != float("inf")]
        with_distance.sort(key=lambda x: x[1])

        result = {}
        if closest:
            result["closest"] = with_distance[:k]
        if farthest:
            result["farthest"] = with_distance[-k:][::-1]  # farthest first
        return result

    def _learning_rate(self) -> float:
        """Learning rate from number of engagements: smaller as n grows."""
        return _DECAY_CONSTANT / (_DECAY_CONSTANT + self.n_articles_engaged)

    def like(
        self,
        article_stances: Dict[str, float],
        strength: Optional[float] = None,
    ) -> None:
        """
        User liked the article: nudge stances toward the article's stances.
        Uses learning rate (decay with n_articles_engaged) and optional strength.
        """
        if not article_stances:
            return
        if strength is None:
            strength = sum(abs(v) for v in article_stances.values()) / len(article_stances)
        strength = max(0.0, min(1.0, strength))
        alpha = self._learning_rate()

        for entity, article_val in article_stances.items():
            u = self.get_value(entity)
            move = alpha * strength * (article_val - u)
            new_val = max(-1.0, min(1.0, u + move))
            # Slight confidence bump when we have feedback (cap at 1)
            entry = self.stances.get(entity)
            conf = entry.confidence if entry else 0.5
            conf = min(1.0, conf + 0.05)
            self.set_stance(entity, new_val, confidence=conf)
        self.n_articles_engaged += 1

    def dislike(
        self,
        article_stances: Dict[str, float],
        strength: Optional[float] = None,
    ) -> None:
        """
        User disliked the article: nudge stances away from the article (toward opposite).
        Uses a smaller factor than like so we don't over-interpret dislike.
        """
        if not article_stances:
            return
        if strength is None:
            strength = sum(abs(v) for v in article_stances.values()) / len(article_stances)
        strength = max(0.0, min(1.0, strength)) * _DISLIKE_STRENGTH_FACTOR
        alpha = self._learning_rate()

        for entity, article_val in article_stances.items():
            u = self.get_value(entity)
            target = -article_val  # opposite of article
            move = alpha * strength * (target - u)
            new_val = max(-1.0, min(1.0, u + move))
            entry = self.stances.get(entity)
            conf = entry.confidence if entry else 0.5
            conf = min(1.0, conf + 0.05)
            self.set_stance(entity, new_val, confidence=conf)
        self.n_articles_engaged += 1

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "stances": {e: asdict(s) for e, s in self.stances.items()},
            "n_articles_engaged": self.n_articles_engaged,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "UserVector":
        uv = cls(data["user_id"])
        uv.stances = {
            e: StanceEntry(**s) for e, s in data.get("stances", {}).items()
        }
        uv.n_articles_engaged = data.get("n_articles_engaged", 0)
        return uv

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "UserVector":
        with open(path, "r") as f:
            return cls.from_dict(json.load(f))


