from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional, Union

from biasAnalysis.BiasAnalyzer import BiasAnalyzer
from eventMapping.EventArticleIndex import EventArticleIndex, ArticleRecord


@dataclass
class TimePoint:
    timestamp: datetime
    value: float
    source: str
    event_id: str
    article_id: str


@dataclass
class SourceTimeSeries:
    source: str
    points: List[TimePoint] = field(default_factory=list)

    def sorted_points(self) -> List[TimePoint]:
        return sorted(self.points, key=lambda p: p.timestamp)


class TemporalAnalyzer:
    """
    Builds time series for source/article deviation and derives drift/burst signals.
    """

    def build_source_series(
        self,
        index: EventArticleIndex,
        bias: BiasAnalyzer,
    ) -> Dict[str, SourceTimeSeries]:
        series: Dict[str, SourceTimeSeries] = {}
        for event_id, article_ids in index.event_articles.items():
            centroid = bias.compute_event_centroid(index, event_id)
            if centroid is None:
                continue
            for article_id in article_ids:
                article = index.articles.get(article_id)
                if article is None:
                    continue
                deviation = bias.compute_article_deviation(article, centroid)
                if deviation is None:
                    continue
                ts = _coerce_datetime(article.published_at)
                if ts is None:
                    continue
                point = TimePoint(
                    timestamp=ts,
                    value=deviation,
                    source=article.source,
                    event_id=event_id,
                    article_id=article_id,
                )
                series.setdefault(article.source, SourceTimeSeries(article.source))
                series[article.source].points.append(point)
        return series

    def narrative_drift(self, source_series: SourceTimeSeries) -> List[TimePoint]:
        points = source_series.sorted_points()
        if len(points) < 2:
            return []
        drift_points: List[TimePoint] = []
        for prev, curr in zip(points, points[1:]):
            drift = abs(curr.value - prev.value)
            drift_points.append(
                TimePoint(
                    timestamp=curr.timestamp,
                    value=drift,
                    source=curr.source,
                    event_id=curr.event_id,
                    article_id=curr.article_id,
                )
            )
        return drift_points

    def rolling_average(
        self,
        points: Iterable[TimePoint],
        window_size: int,
    ) -> List[TimePoint]:
        points_list = sorted(points, key=lambda p: p.timestamp)
        if window_size <= 0:
            return []
        result: List[TimePoint] = []
        for i in range(len(points_list)):
            start = max(0, i - window_size + 1)
            window = points_list[start : i + 1]
            avg = sum(p.value for p in window) / len(window)
            p = points_list[i]
            result.append(
                TimePoint(
                    timestamp=p.timestamp,
                    value=avg,
                    source=p.source,
                    event_id=p.event_id,
                    article_id=p.article_id,
                )
            )
        return result

    def detect_bursts(
        self,
        points: Iterable[TimePoint],
        threshold: float,
    ) -> List[TimePoint]:
        return [p for p in points if p.value > threshold]

    def repetitive_burst_windows(
        self,
        points: Iterable[TimePoint],
        threshold: float,
        window: Union[timedelta, int, float],
        min_bursts: int = 2,
    ) -> List[List[TimePoint]]:
        """
        Detects windows with repeated high-deviation bursts.
        window can be timedelta or seconds.
        """
        points_list = sorted(points, key=lambda p: p.timestamp)
        if isinstance(window, (int, float)):
            window = timedelta(seconds=float(window))
        bursts = [p for p in points_list if p.value > threshold]
        windows: List[List[TimePoint]] = []
        for i, start in enumerate(bursts):
            current: List[TimePoint] = [start]
            for candidate in bursts[i + 1 :]:
                if candidate.timestamp - start.timestamp <= window:
                    current.append(candidate)
                else:
                    break
            if len(current) >= min_bursts:
                windows.append(current)
        return windows


def _coerce_datetime(value: Optional[Union[str, datetime]]) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None
