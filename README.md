# Status Page Status Page

A review of how a public [Atlassian Statuspage](https://www.atlassian.com/software/statuspage) status page communicates, built around the 12 November 2026 Microsoft 365 outage as seen on [status.it.ubc.ca](https://status.it.ubc.ca).

It doesn't judge whether services worked. It looks at what readers were told, and when: open incidents, update timing and promises, maintenance windows, the page's clock, and how the Statuspage editor shapes all of that. Findings are framed as process, not people.

## How it fits together

Two repositories, both public:

| Repository | Job |
|---|---|
| **status-page-status-page** (this one) | The review: `index.html`, the data it shows, and the scripts that prepare it. |
| **status-page-status-page-data** | The collector: GitHub Actions saves the status page's public feeds every 10 minutes, keeping each version that changed. |

```
 status.it.ubc.ca public feeds
          │  every 10 min (GitHub Actions, data repository)
          ▼
 status-page-status-page-data/data/…        every changed version, as served
          │  scripts/import-collected.py   (this repository)
          ▼
 data/snapshots/  data/incidents/            what the review shows
          │  scripts/embed-snapshots.py
          ▼
 index.html                                  open it, or share it as one file
          ▲
          └── optional, never committed: GA4 traffic (ga4/ga4-data.js or CSVs dropped on the page)
```

### Refreshing the review

With both repositories cloned side by side:

```bash
cd status-page-status-page-data && git pull && cd ..
```

```bash
cd status-page-status-page
```

```bash
python3 scripts/import-collected.py ../status-page-status-page-data
```

```bash
python3 scripts/embed-snapshots.py
```

Open `index.html` to check, then commit `data/` and `index.html`.

## Open it

Open `index.html` in any browser. No server, no install, no build step, no network calls. It's one self-contained file, so it can also be attached or shared as is.

Pages: **Overview**, **Issues**, **Incidents**, **History**, **Maintenance**, **Traffic** (optional, see below), **Services**, **Method**. Each has its own link (`index.html#issues`).

## Data

| File | What it is |
|---|---|
| `data/snapshots/summary-2026-11-12.json` | Status page snapshot, 12 Nov 2026 22:36 PST. **Reconstructed** from a pasted copy; some text shortened. See `data/snapshots/NOTES.md`. |
| `data/snapshots/summary-2026-11-14.json` | Status page snapshot, 14 Nov 2026 22:09 PST. Statuses, times and texts as published; unused fields omitted. See `NOTES.md`. |
| `data/snapshots/summary-2026-11-17.json` | Status page snapshot, 17 Nov 2026 08:39 PST. **Raw, as published.** |
| `data/incidents/incidents-2026-11-17.json` | The page's incident history: the 50 most recent incidents (19 Jun to 16 Nov 2026), open and resolved, with every update. **Raw, as published.** See `data/incidents/NOTES.md`. |
| `data/snapshots/summary-YYYY-MM-DD.json` (imported) | Added by `scripts/import-collected.py`: the newest collected capture, and the newest from an earlier day. **Raw.** A capture dated the same as an existing file replaces it. |
| `data/incidents/incidents-merged.json` (imported) | Added by `scripts/import-collected.py`: the newest version of every incident across all captures, so the history grows past 50. **Derived**, labelled as such in the file and on the History page. |
| `data/history-titles.json` | Titles of recently resolved incidents, from the page's public history feed (`/history.atom`), so traffic to older incident pages can be named. |

All of it is public: it comes from `https://status.it.ubc.ca/api/v2/summary.json`, `/api/v2/incidents.json` and `/history.atom`.

`index.html` carries an embedded copy of these files, because a page opened from disk can't read other local files. The JSON files are the source of truth. After adding or changing a snapshot:

```bash
python3 scripts/embed-snapshots.py           # re-embed data/ into index.html
python3 scripts/embed-snapshots.py --check   # confirm index.html matches data/
```

The page also accepts a fresh `summary.json` or `incidents.json` through **Load a snapshot**. A summary is compared with the one shown; an incidents file replaces the history if it is newer.

## Collected history (separate data repository)

A companion repository, **status-page-status-page-data**, captures the page's public feeds every 10 minutes with GitHub Actions and keeps every changed version. Its README covers first-time setup. To bring its data in (see also *Refreshing the review* above):

```bash
python3 scripts/import-collected.py ../status-page-status-page-data
python3 scripts/embed-snapshots.py
```

This copies the newest `summary.json` (and the newest from an earlier day, for comparison) into `data/snapshots/`, and builds `data/incidents/incidents-merged.json`: the newest version of every incident across all captures. The page then shows a history that grows past the 50 incidents Statuspage lists.

## How findings are worked out

The **Method** page in the review is the full description. In short:

- **Affected now:** the services an incident's own latest update lists as not operational, checked against each service's current status.
- **Promises:** read from update text in five wordings ("next update …", "further / another update at …", "update will be provided at …", "check back at …", "update in N minutes"), with days such as "tomorrow", "Monday" or "July 13" and times such as "16:30", "2 pm" or "noon". Each promise shows which wording matched. Met = the next update came no more than 15 minutes after the promised time.
- **History checks:** incidents closed with notifications off after being announced with them; updates whose displayed time differs from their creation time by more than 10 minutes; incidents filed only under "Other"; impact "Maintenance" on unplanned incidents; placeholder update text.
- **Edited updates:** an update whose last-changed time is more than a minute after it was created.
- **Changes:** two snapshots compared item by item.
- Each issue is shown as *what the data shows / likely cause / suggested fix*, tagged **Confirmed** (in the data, or tested on a Statuspage account) or **Likely** (best reading, still to check).

## Traffic layer (GA4): local only

The Traffic page lines up Google Analytics (GA4) counts with the incident timeline. **Traffic data is never committed.** The repository contains only public status page data.

Two ways to load it:

1. **Local file.** Export CSVs from GA4, then:
   ```bash
   python3 scripts/ga4-to-js.py ~/Downloads/ga4-exports/
   ```
   This writes `ga4/ga4-data.js`, which `index.html` loads if it's present. `.gitignore` excludes it.
2. **In the browser.** Drop GA4 CSV exports on the Traffic page. They're read in memory and gone when the page closes.

Without traffic data, the Traffic page shows a short note and everything else is unchanged.

Exports the page recognises (by column names):

| Export | Where in GA4 |
|---|---|
| Views by day | Reports → Engagement → Pages and screens, dimension **Date** (up to 13 months) |
| Views by hour | Same report, dimension **Date + hour (YYYYMMDDHH)**, with Page path and screen class |
| Views by minute | GA4 Query Explorer: dimensions `dateHourMinute` (+ `pagePath`), metrics `screenPageViews`, `activeUsers` |
| Sources | Reports → Acquisition → Traffic acquisition, **Session source / medium** + Page path and screen class |
| Top pages | Pages and screens, Page path and screen class, no date dimension |

Notes:

- GA4 reports this property's hours in **PST (UTC−8)**. The page converts them to absolute times and shows PST with PCT (UTC−7) alongside.
- Missing days or minutes are shown as gaps, never filled in. Days cut off by the export's end are marked as partial.
- Hourly data can't show whether people arrived before the first post within the same hour. Minute data can.

## Caveats

- A single `summary.json` shows only what's open at that moment, and posted updates can be edited without a visible record. The collector addresses both from the day it starts; anything before that is limited to the files in `data/` and the 50 incidents the page listed on 17 Nov.
- The collector catches a change on its next run (about 10 minutes, sometimes later when GitHub is busy). Times inside the data come from the status page, so they are unaffected.
- "Last edited" on a service changes with any edit, not only status changes.
- "Likely" causes still need checking with the team that runs the page.
- See `data/snapshots/NOTES.md` and `data/incidents/NOTES.md` for exactly how each file was captured.

## Repository layout

```
index.html                 the review (self-contained)
data/snapshots/            status page snapshots + NOTES.md (provenance)
data/incidents/            incident history (incidents.json, plus incidents-merged.json once imported) + NOTES.md
data/history-titles.json   resolved incident titles from the public history feed
ga4/                       local traffic data goes here (not committed)
scripts/embed-snapshots.py re-embed and check the data in index.html
scripts/ga4-to-js.py       GA4 CSV exports → ga4/ga4-data.js
scripts/import-collected.py  collected data (from the data repository) → data/
```

Scripts need Python 3 and nothing else.

## Licence

MIT. See `LICENSE`.
