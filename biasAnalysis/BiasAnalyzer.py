from typing import Dict, List, Optional, Union

from eventMapping.EventArticleIndex import EventArticleIndex, ArticleRecord

FeatureVector = Union[Dict[str, float], List[float]]


class BiasAnalyzer:
    """
    Computes event centroids, article deviations, and source-level bias metrics.
    """

    def compute_event_centroid(
        self,
        index: EventArticleIndex,
        event_id: str,
    ) -> Optional[FeatureVector]:
        articles = index.get_articles_for_event(event_id)
        vectors = [a.feature_vector for a in articles if a.feature_vector is not None]
        if not vectors:
            return None
        return _average_vectors(vectors)

    def compute_article_deviation(
        self,
        article: ArticleRecord,
        centroid: FeatureVector,
    ) -> Optional[float]:
        if article.feature_vector is None:
            return None
        return _euclidean_distance(article.feature_vector, centroid)

    def deviations_for_event(
        self,
        index: EventArticleIndex,
        event_id: str,
    ) -> Dict[str, float]:
        centroid = self.compute_event_centroid(index, event_id)
        if centroid is None:
            return {}
        deviations: Dict[str, float] = {}
        for article in index.get_articles_for_event(event_id):
            deviation = self.compute_article_deviation(article, centroid)
            if deviation is not None:
                deviations[article.article_id] = deviation
        return deviations

    def source_bias_fingerprint(
        self,
        index: EventArticleIndex,
        event_id: str,
    ) -> Dict[str, float]:
        deviations = self.deviations_for_event(index, event_id)
        if not deviations:
            return {}
        by_source: Dict[str, List[float]] = {}
        for article in index.get_articles_for_event(event_id):
            if article.article_id not in deviations:
                continue
            by_source.setdefault(article.source, []).append(deviations[article.article_id])
        return {source: sum(vals) / len(vals) for source, vals in by_source.items()}

    def flag_rumors(
        self,
        index: EventArticleIndex,
        event_id: str,
        threshold: float,
    ) -> List[str]:
        deviations = self.deviations_for_event(index, event_id)
        return [article_id for article_id, d in deviations.items() if d > threshold]


def _average_vectors(vectors: List[FeatureVector]) -> FeatureVector:
    if isinstance(vectors[0], dict):
        return _average_dict_vectors(vectors) 
    return _average_list_vectors(vectors)  


def _average_dict_vectors(vectors: List[Dict[str, float]]) -> Dict[str, float]:
    totals: Dict[str, float] = {}
    for vec in vectors:
        for key, value in vec.items():
            totals[key] = totals.get(key, 0.0) + value
    count = float(len(vectors))
    return {k: v / count for k, v in totals.items()}


def _average_list_vectors(vectors: List[List[float]]) -> List[float]:
    length = len(vectors[0])
    for vec in vectors:
        if len(vec) != length:
            raise ValueError("All vectors must have the same length.")
    totals = [0.0] * length
    for vec in vectors:
        for i, value in enumerate(vec):
            totals[i] += value
    count = float(len(vectors))
    return [v / count for v in totals]


def _euclidean_distance(a: FeatureVector, b: FeatureVector) -> float:
    if isinstance(a, dict) and isinstance(b, dict):
        keys = set(a.keys()) | set(b.keys())
        return sum((a.get(k, 0.0) - b.get(k, 0.0)) ** 2 for k in keys) ** 0.5
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            raise ValueError("Vectors must have the same length.")
        return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
    raise TypeError("Vector types must match (both dict or both list).")
