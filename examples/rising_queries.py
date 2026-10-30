"""Top and rising Google Trends related queries for a list of seed keywords.

    python rising_queries.py "electric bike" "air fryer" --country us

For each seed, reads Google Trends and keeps the related queries of the full
response: "top" (the most searched together with the seed) and "rising" (the
fastest growing, labelled "Breakout" for the biggest jumps). Writes
related_queries.csv with seed, list, query, value and the value as Google
formats it.
"""

import argparse

from quanticdata_google_trends_scraper import GoogleTrends, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("seeds", nargs="+")
    parser.add_argument("--country", default="us")
    parser.add_argument("--out", default="related_queries.csv")
    args = parser.parse_args()

    trends = GoogleTrends()
    rows = []
    for seed in args.seeds:
        related = ((trends.interest(seed, country=args.country).meta.get("trends") or {})
                   .get("related_queries") or {})
        for kind in ("rising", "top"):
            for q in related.get(kind) or []:
                rows.append({"seed": seed, "list": kind, "query": q.get("query"),
                             "value": q.get("value"), "formatted": q.get("formatted")})
        rising = [q.get("query") for q in related.get("rising") or []][:5]
        print(f"{seed!r}: rising {', '.join(rising) or '-'}")

    write(rows, args.out)
    print(f"{len(rows)} related queries written to {args.out}")


if __name__ == "__main__":
    main()
