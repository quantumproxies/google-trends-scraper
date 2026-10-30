"""Google Trends Scraper: Google Trends scraper and API for Python and the command line: today's trending searches per country with traffic band and news stories, and 12 months of weekly interest with top and rising related queries for any keyword, as JSON or CSV. Free and open source; no Google API key or proxies needed.

    from quanticdata_google_trends_scraper import GoogleTrends

    scraper = GoogleTrends()   # saved login (`google-trends login`) or QUANTICDATA_API_KEY
    run = scraper.trending(...)   # today's trending searches in a country
    run = scraper.interest(...)   # weekly interest over time and related queries for a keyword
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["GoogleTrends", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class GoogleTrends:
    """Google Trends Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="google-trends/0.1.0 (+https://github.com/quantumproxies/google-trends-scraper)", timeout=timeout)

    def trending(
        self, country: Optional[str] = None,
        *,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Today's trending searches for a country: the query, Google's traffic band, when it surfaced and the news stories attached to it.

        Args:
            country: Country whose trending feed to read, as an ISO code: us, gb, de, it... (default us).
            max_results: How many trends to deliver at most (1–20). You pay only for delivered trends.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 20 rows, one per trend: see ``types.GoogleTrendsRow``.
        """
        payload = {
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("google_trends", payload, wait=wait, timeout=timeout)

    def interest(
        self, query: str,
        *,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        timeout: float = 1800.0,
    ) -> Run:
        """Google Trends for a keyword: weekly interest over the last 12 months (0 to 100), plus the top and rising related queries in the full response.

        Args:
            query: Keyword to read in Google Trends, e.g. "electric bike".
            country: Country to read the interest in, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: UI language, e.g. `en`, `it`.
            timeout: seconds to wait before giving up.

        Returns a Run: ``meta`` is the whole response, ``rows`` its ``trends.interest_over_time`` list (see ``types.InterestRow``).
        """
        payload = {
            "query": query,
            "country": country,
            "lang": lang,
        }
        return self.client.layer("serp", {**{'engine': 'google', 'search_type': 'trends'}, **payload}, rows_key='trends.interest_over_time', row_field='value', timeout=timeout)
