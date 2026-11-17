# Changelog

## v3.2 (17 Nov 2026)

- Companion data repository with a collector (`status-page-status-page-data`): GitHub Actions saves the three public feeds every 10 minutes, only when they change.
- `scripts/import-collected.py`: brings collected captures in, including a merged incident history that keeps incidents after they drop out of the page's 50 most recent.
- History page labels a merged history as merged, with the capture range.

## v3.1 (17 Nov 2026)

- Incident history: reads the page's `incidents.json` (the 50 most recent incidents, resolved ones included). Stored raw in `data/incidents/`, embedded like the snapshots, and loadable through **Load a snapshot**.
- New **History** page: every incident with time open, impact, services, tags and full updates, plus summary tiles.
- Promise detection widened from "next update …" to five wordings, with weekdays, dates, "noon", am/pm and relative minutes. Each promise is labelled with the wording that matched. "PT" and unzoned times use Pacific time as it was on the day of posting.
- Update promises now cover every incident in the history, and are judged against the newest data loaded.
- Five new checks over the history, added after the existing ones (existing checks unchanged): closed without notifying subscribers, re-dated updates, incidents filed only under "Other", impact "Maintenance" on unplanned incidents, placeholder update text.
- Third snapshot, `summary-2026-11-17.json`, stored raw. The page now shows 17 Nov and compares it with 14 Nov; closed incidents show when they were resolved and whether subscribers were notified.
- Fix: the overnight views-per-user finding on the Traffic page looked at 16:00–22:00 PST instead of 00:00–06:00 PST (time zone sign error).

## v3 (16 Nov 2026)

- Repository layout: snapshots as separate JSON files in `data/snapshots/` with provenance notes; `index.html` embeds a copy, checked by `scripts/embed-snapshots.py --check`.
- New **Traffic** page with an optional, local-only GA4 layer: loads `ga4/ga4-data.js` if present, or GA4 CSVs dropped on the page. No traffic data in the repository.
- Traffic views: views by day (gaps hatched, partial days marked), hourly views around the incident with update and promise markers, minute-level view around the first post when that data is loaded, sources, most-viewed incident pages.
- "Typical" traffic now compares weekdays with weekdays and weekends with weekends. v1 compared against all earlier days, which understated how unusual a weekday spike was.
- The "before the first post" finding is worded for what hourly data can show, and uses minute data when it's available.
- Method page: section on the traffic layer, its sources and limits.
- `scripts/ga4-to-js.py` builds the local traffic file from GA4 exports.
- Renamed to Status Page Status Page.

## v2 (14 Nov 2026)

- Split into pages: Overview, Issues, Incidents, Maintenance, Services, Method, each with its own link.
- Plain institutional styling, system fonts, Canadian spelling, neutral wording.
- Issues shown as evidence / likely cause / suggested fix, tagged Confirmed or Likely.
- Second snapshot (14 Nov) and a "What changed" comparison between snapshots.
- New checks: updates edited after posting, "As at" times later than the post, start time later than the opening time, promises naming a weekday.
- Expandable full update history per incident, with each time shown in PCT and as the page displays it (PST).
- GA4 traffic left out of this version.

## v1 (13 Nov 2026)

- First single-page prototype from the 12 Nov snapshot: headline, tiles, review list, open incidents timeline, update promises, the PST/PCT clock mismatch, maintenance calendar, services by group.
- Load another `summary.json` by drop, file picker or paste.
- v1.1 added a GA4 traffic section with the data embedded. Not carried into the repository; v3 reintroduces traffic as a local-only layer.
