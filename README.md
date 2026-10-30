# Google Trends Scraper

[![ci](https://github.com/quantumproxies/google-trends-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/google-trends-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Google Trends data from Python or the command line: today's trending searches in a country, with Google's traffic band and the news stories attached to each one, and the weekly interest of any keyword over the last 12 months, with its top and rising related queries. The code is free and open source (MIT). It runs on the QuanticData Data API, so there is no Google API key to request and no proxy to rotate: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/google-trends-scraper
google-trends login
google-trends trending us --max-results 20 -o trending.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=google-trends-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `google-trends trending` | country code (optional) | Query, traffic band, publish time, news stories, 10 fields per row ([fields and price](https://quanticdata.io/collectors/google-trends-api/?utm_source=github&utm_medium=readme&utm_campaign=google-trends-scraper)) | up to 20 |
| `google-trends interest` | keyword | Week, interest value (0 to 100), 4 fields per row ([docs and price](https://quanticdata.io/serp-api/?utm_source=github&utm_medium=readme&utm_campaign=google-trends-scraper)) | one year of weekly values |

`trending` takes the country as an ISO code (`us`, `gb`, `de`, `it`...; default `us`). `interest` reads one keyword over the last 12 months, in weekly points from 0 to 100 relative to that keyword's own peak in the period; `-o interest.json` also keeps the related queries.

## Sample output

A real row from `google-trends trending us --max-results 3` (2026-10-23):

```json
{
  "rank": 2,
  "image": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSIdQSuPGnh1O1NxE23EkAd08UNFhsMcCadYyY6kNU7Lpsd_9S41kSphuCaQ-k",
  "query": "nyt connections hints",
  "country": "US",
  "articles": [
    {
      "url": "https://www.nytimes.com/2026/10/22/crosswords/connections-companion-1230.html",
      "title": "NYT Connections Answers for Friday, October 23, 2026",
      "source": "The New York Times"
    },
    {
      "url": "https://mashable.com/entertainment/nyt-connections-hints-meanings-october-19-2026",
      "title": "NYT Connections hints today: Meanings for each word for Oct. 19, 2026",
      "source": "Mashable"
    },
    {
      "url": "https://www.rockpapershotgun.com/connections-hint-answers-16-10-26",
      "title": "Here's your NYT Connections hint for Friday Oct 16",
      "source": "Rock Paper Shotgun"
    }
  ],
  "published": "Fri, 23 Oct 2026 02:20:00 -0700",
  "traffic_min": 100,
  "published_at": "2026-10-23T09:20:00.000Z",
  "article_count": 3,
  "approx_traffic": "100+"
}
```

## Python

```python
from quanticdata_google_trends_scraper import GoogleTrends

trends = GoogleTrends()  # saved login, or QUANTICDATA_API_KEY

today = trends.trending("us", max_results=20)
for t in today:
    print(t["rank"], t["approx_traffic"], t["query"], t["article_count"])

bike = trends.interest("electric bike", country="us")
for week in bike:
    print(week["date"], week["value"])
related = bike.meta["trends"]["related_queries"]
print([q["query"] for q in related["rising"]])
bike.to_csv("electric_bike_interest.csv")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Daily trending log**: Save the trending searches of a few countries every morning, with traffic band and the top news story of each, and keep the history in one CSV. See [`examples/daily_trending.py`](examples/daily_trending.py).
- **Keyword interest comparison**: Weekly interest for a list of keywords in one long-format CSV, with each keyword's peak week printed, ready for a chart. See [`examples/compare_interest.py`](examples/compare_interest.py).
- **Rising query ideas**: Collect the top and rising related queries of a list of seed keywords in one CSV, a quick source of content and ad ideas. See [`examples/rising_queries.py`](examples/rising_queries.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `google-trends run <id> -o out.csv` collects it later.

### `google-trends trending`

Today's trending searches for a country: the query, Google's traffic band, when it surfaced and the news stories attached to it.

```
google-trends trending [COUNTRY] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `COUNTRY` | string |  | Country whose trending feed to read, as an ISO code: us, gb, de, it... (default us). |
| `--max-results` | integer | `10` | How many trends to deliver at most (1–20). You pay only for delivered trends. |

### `google-trends interest`

Google Trends for a keyword: weekly interest over the last 12 months (0 to 100), plus the top and rising related queries in the full response.

```
google-trends interest QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Keyword to read in Google Trends, e.g. "electric bike". |
| `--country` | string |  | Country to read the interest in, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | UI language, e.g. `en`, `it`. |

Sent with every call: `engine=google`, `search_type=trends`.

## Output fields

<details><summary><code>google-trends trending</code>: 10 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Position in today's feed. |
| `query` | string | The trending search query. |
| `approx_traffic` | string or null | Google's traffic band, e.g. "1000+". |
| `published` | string or null | When Google surfaced the trend. |
| `image` | string or null | Representative image URL. |
| `articles` | object[] | News stories attached to the trend ({ title, url, source }). |
| `country` | string | Country the feed was read for. |
| `traffic_min` | integer or null | approx_traffic as a number ("2000+" → 2000). |
| `published_at` | string or null | published as an ISO 8601 timestamp. |
| `article_count` | integer | How many stories are attached. |

</details>

<details><summary><code>google-trends interest</code>: 4 fields</summary>

| Field | Type | Description |
|---|---|---|
| `date` | string | Week as shown by Google Trends. |
| `timestamp` | integer | Start of the week, Unix seconds. |
| `value` | integer | Interest, 0 to 100 relative to the peak of the period. |
| `partial` | boolean or null | True for the current, incomplete week. |

</details>

## Sign-in and API keys

- `google-trends login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `google-trends login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `google-trends login --api-key`.
- `google-trends logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. `trending` is billed per delivered trend at the price on its collector page, `interest` per call at the price on the SERP API page, both linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=google-trends-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/google_trends/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"country": "us", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=google-trends-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=google-trends-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Google Trends scraper free?**

The code is free and MIT-licensed. Calls run on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered trend or per Trends call, at the prices on the pages linked above. Failed runs are never billed.

**Do I need a Google Trends API key or proxies?**

No. There is no Google Cloud project or key to set up and no proxy to configure: you send a country code or a keyword and get rows back; the requests run on QuanticData's side.

**What does one call return?**

trending returns up to 20 trends per run (--max-results), each with its traffic band and news stories. interest returns the last 12 months as weekly points, and the full response (-o interest.json in the CLI, .meta in Python) also carries the top and rising related queries.

**Can I read another country?**

Yes: google-trends trending gb, google-trends trending it, and --country for interest (google-trends interest "electric bike" --country de).

**Can I export to CSV?**

Add -o trending.csv or -o interest.csv (or .json, .jsonl). The news stories of a trend are kept in one JSON column, so the CSV still has one row per trend.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/daily_trending.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Google SERP API](https://github.com/quantumproxies/google-serp-api): Google SERP API for Python and the command line.
- [Keyword Research Tool](https://github.com/quantumproxies/keyword-research-tool): Keyword research tool for Python and the command line.
- [Bing Search API](https://github.com/quantumproxies/bing-search-api): Bing Search API alternative for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=google-trends-scraper).
