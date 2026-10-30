"""Compare the Google Trends interest of several keywords, week by week.

    python compare_interest.py "electric bike" "electric scooter" "ebike" --country us

Reads the last 12 months of weekly interest for each keyword and writes them in
long format (keyword, week, value, partial) to interest.csv, ready for a pivot
table or a line chart. Each keyword is read on its own, so its values run from
0 to 100 relative to its own peak; the peak week of each one is printed.
"""

import argparse

from quanticdata_google_trends_scraper import GoogleTrends, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--country", default="us")
    parser.add_argument("--out", default="interest.csv")
    args = parser.parse_args()

    trends = GoogleTrends()
    rows = []
    for keyword in args.keywords:
        series = trends.interest(keyword, country=args.country)
        points = [p for p in series if p.get("value") is not None]
        rows.extend({"keyword": keyword, "week": p["date"], "timestamp": p.get("timestamp"),
                     "value": p["value"], "partial": bool(p.get("partial"))} for p in points)
        if points:
            peak = max(points, key=lambda p: p["value"])
            latest = points[-1]
            print(f"{keyword!r}: {len(points)} weeks, peak {peak['date']}, latest {latest['value']} ({latest['date']})")
        else:
            print(f"{keyword!r}: no data")

    write(rows, args.out)
    print(f"{len(rows)} rows written to {args.out}")


if __name__ == "__main__":
    main()
