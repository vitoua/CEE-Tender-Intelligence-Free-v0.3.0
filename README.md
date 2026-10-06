# CEE Tender Intelligence Free v0.3.0

Free Render edition with Prozorro and TED, manual refresh, in-memory cache, Excel export, and UI in Ukrainian, Polish and English.

## Fixes in 0.3
- TED: corrected `paginationMode` from invalid `PAGE` to documented `PAGE_NUMBER`, uses `onlyLatestVersions`, valid response fields, a full-text query and a CPV fallback, and shows the API error body.
- Prozorro: uses `public-api.prozorro.gov.ua`, follows `next_page.uri`, downloads up to 200 tender details, and no longer discards non-matching tenders during import.
- Dashboard: default minimum score is 0, shows fetched and relevant counts separately, adds text search and language switcher.

## Render
Push all files to GitHub, choose New > Blueprint, select the repository, enter `ADMIN_EMAIL` and `ADMIN_PASSWORD`, and apply. No PostgreSQL, disk, or cron job is created.
