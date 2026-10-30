"""Log today's Google Trends trending searches for a few countries.

    python daily_trending.py us gb de --top 20

Appends one row per trend to trending_history.csv: the day, the country, rank,
query, traffic band (and its numeric floor), when Google surfaced it and the
first news story attached to it. Run it every morning from cron to build a
history of what each country searched for:

    0 7 * * *  cd /path/to/here && python daily_trending.py us gb de

Needs a login (`google-trends login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_google_trends_scraper import GoogleTrends

FIELDS = ["day", "country", "rank", "query", "approx_traffic", "traffic_min", "published_at",
          "article_count", "top_story", "top_story_source", "top_story_url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("countries", nargs="+", help="ISO country codes, e.g. us gb de")
    parser.add_argument("--top", type=int, default=20, help="trends per country (max 20)")
    parser.add_argument("--out", default="trending_history.csv")
    args = parser.parse_args()

    trends = GoogleTrends()
    day = datetime.now(timezone.utc).date().isoformat()
    new_file = not os.path.exists(args.out)
    written = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        for country in args.countries:
            run = trends.trending(country, max_results=args.top)
            for t in run:
                story = (t.get("articles") or [{}])[0]
                writer.writerow({
                    "day": day, "country": country, "rank": t["rank"], "query": t["query"],
                    "approx_traffic": t.get("approx_traffic"), "traffic_min": t.get("traffic_min"),
                    "published_at": t.get("published_at"), "article_count": t.get("article_count"),
                    "top_story": story.get("title"), "top_story_source": story.get("source"),
                    "top_story_url": story.get("url"),
                })
                written += 1
            print(f"{country}: {len(run)} trends")
    print(f"{written} rows appended to {args.out}")


if __name__ == "__main__":
    main()
