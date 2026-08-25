# Google Trends — trending now API — examples

Today's trending searches for a country, with traffic band and attached news stories.

**Live page, full schema & pricing → [quanticdata.io/collectors/google-trends-api/](https://quanticdata.io/collectors/google-trends-api/)**

Reads Google Trends' trending-searches feed for a country and delivers one row per trend: the query, Google's approximate traffic band (Google publishes no exact number), when it surfaced, a representative image and the news articles Google attached. This is the daily-trending surface — historical interest-over-time for a keyword is not included.

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/google_trends/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "us", "max_results": 10}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `country` (string) — ISO 3166-1 alpha-2 code — which country's trending feed to read (default us).
- `max_results` (integer) — How many trends to deliver at most (1–20). You pay only for delivered trends.

## Output — one row per trend

| field | type | description |
|---|---|---|
| `rank` | integer | Position in today's feed. |
| `query` | string | The trending search query. |
| `approx_traffic` | string | Google's traffic band, e.g. "1000+". |
| `published` | string | When Google surfaced the trend. |
| `image` | string | Representative image URL. |
| `articles` | object[] | News stories attached to the trend ({ title, url, source }). |
| `country` | string | Country the feed was read for. |

## Pricing

**$0.0005 per delivered trend** ($0.5 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 4,000 trends — no card required.

## Links

- This collector: https://quanticdata.io/collectors/google-trends-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
