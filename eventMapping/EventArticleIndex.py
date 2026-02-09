from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Union


@dataclass
class EventRecord:
    event_id: str
    title: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    entities: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    metadata: Dict[str, Union[str, float, int, bool]] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        data = asdict(self)
        if self.start_time:
            data["start_time"] = self.start_time.isoformat()
        if self.end_time:
            data["end_time"] = self.end_time.isoformat()
        return data


@dataclass
class ArticleRecord:
    article_id: str
    source: str
    published_at: Optional[Union[datetime, str]] = None
    url: Optional[str] = None
    event_ids: List[str] = field(default_factory=list)
    feature_vector: Optional[Union[Dict[str, float], List[float]]] = None
    metadata: Dict[str, Union[str, float, int, bool]] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        data = asdict(self)
        if self.published_at:
            if isinstance(self.published_at, datetime):
                data["published_at"] = self.published_at.isoformat()
            else:
                data["published_at"] = self.published_at
        return data


class EventArticleIndex:
    """
    Maintains a bidirectional map between events and articles.
    """

    def __init__(self) -> None:
        self.events: Dict[str, EventRecord] = {}
        self.articles: Dict[str, ArticleRecord] = {}
        self.event_articles: Dict[str, List[str]] = {}
        self.article_events: Dict[str, List[str]] = {}

    def add_event(self, event: EventRecord) -> None:
        self.events[event.event_id] = event
        self.event_articles.setdefault(event.event_id, [])

    def add_article(self, article: ArticleRecord) -> None:
        self.articles[article.article_id] = article
        self.article_events.setdefault(article.article_id, [])
        for event_id in article.event_ids:
            self.link_article_to_event(article.article_id, event_id)

    def link_article_to_event(self, article_id: str, event_id: str) -> None:
        if event_id not in self.events:
            self.add_event(EventRecord(event_id=event_id, title=event_id))
        self.event_articles.setdefault(event_id, [])
        self.article_events.setdefault(article_id, [])
        if article_id not in self.event_articles[event_id]:
            self.event_articles[event_id].append(article_id)
        if event_id not in self.article_events[article_id]:
            self.article_events[article_id].append(event_id)
        if article_id in self.articles:
            if event_id not in self.articles[article_id].event_ids:
                self.articles[article_id].event_ids.append(event_id)

    def get_articles_for_event(self, event_id: str) -> List[ArticleRecord]:
        ids = self.event_articles.get(event_id, [])
        return [self.articles[a_id] for a_id in ids if a_id in self.articles]

    def get_events_for_article(self, article_id: str) -> List[EventRecord]:
        ids = self.article_events.get(article_id, [])
        return [self.events[e_id] for e_id in ids if e_id in self.events]

    def to_dict(self) -> Dict:
        return {
            "events": {k: v.to_dict() for k, v in self.events.items()},
            "articles": {k: v.to_dict() for k, v in self.articles.items()},
            "event_articles": self.event_articles,
            "article_events": self.article_events,
        }
