# Incident history provenance

## incidents-2026-11-17.json: raw, as published

- Source: `https://status.it.ubc.ca/api/v2/incidents.json`, saved unchanged.
- Captured: page `updated_at` 2026-11-17 08:39:22 PST.
- SHA-256: `ada6b011581054988ecc54448ad078fba5dd84a435ca2fee0a61eb93de11afbe`
- Contents: the 50 most recent incidents (opened 19 Jun to 16 Nov 2026), open and resolved, with all 144 updates. Each update carries its created, updated and display times, its affected services with old and new status, and whether subscribers were notified.
- Not included by Statuspage in this file: scheduled maintenance (that is `/api/v2/scheduled-maintenances.json`) and anything older than the 50 most recent incidents.

## Adding a newer copy

```bash
curl -s https://status.it.ubc.ca/api/v2/incidents.json -o data/incidents/incidents-$(date +%Y-%m-%d).json
python3 scripts/embed-snapshots.py
```

The page uses the newest file. Keep older files: incidents drop out of the 50 as new ones arrive, and updates can be edited later, so each saved copy is a record.

## incidents-merged.json (when present): derived, not raw

Built by `scripts/import-collected.py` from every incidents capture in the data repository plus the raw files here. It holds the newest version of each incident ever seen and records the capture range in `_merged`. Statuspage does not serve this file; the raw captures are in the data repository.
