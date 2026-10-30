"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class GoogleTrendsRow(TypedDict, total=False):
    """One row of `google-trends trending` (google_trends v1.1.0)."""

    rank: int
    """Position in today's feed."""
    query: str
    """The trending search query."""
    approx_traffic: Optional[str]
    """Google's traffic band, e.g. "1000+"."""
    published: Optional[str]
    """When Google surfaced the trend."""
    image: Optional[str]
    """Representative image URL."""
    articles: List[Dict[str, Any]]
    """News stories attached to the trend ({ title, url, source })."""
    country: str
    """Country the feed was read for."""
    traffic_min: Optional[int]
    """approx_traffic as a number ("2000+" → 2000)."""
    published_at: Optional[str]
    """published as an ISO 8601 timestamp."""
    article_count: int
    """How many stories are attached."""

class InterestRow(TypedDict, total=False):
    """One row of `google-trends interest` (POST /v1/serp)."""

    date: str
    """Week as shown by Google Trends."""
    timestamp: int
    """Start of the week, Unix seconds."""
    value: int
    """Interest, 0 to 100 relative to the peak of the period."""
    partial: Optional[bool]
    """True for the current, incomplete week."""
