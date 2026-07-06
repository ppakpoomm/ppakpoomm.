# AGENTS.md

## Cursor Cloud specific instructions

This repo (`ppakpoomm/ppakpoomm.`) is primarily a **central workspace hub** (README + `repos.json` + `docs/WORKSPACE.md`). Most linked repositories live elsewhere on GitHub. The only runnable application checked into this repo is **`projects/EMS_Quality_Awards`**.

### EMS_Quality_Awards (Python CLI + static web dashboard)

Standard commands live in `projects/EMS_Quality_Awards/Makefile` and `README.md`. Non-obvious caveats:

- **Dashboard server must run from the project root, not `dashboard/`.** The dashboard JS (`dashboard/js/app.js`) fetches data via the relative path `../data/*.json`. Start the server from `projects/EMS_Quality_Awards` (`make serve`, i.e. `python3 -m http.server 8080`) and open **`http://localhost:8080/dashboard/`** — opening the site root or serving from inside `dashboard/` breaks the data fetch.
- **Charts need runtime internet.** `dashboard/index.html` loads Chart.js from the jsdelivr CDN, so the three charts only render when the browser has outbound network access. Metric cards and the table work offline.
- **`make validate` exits non-zero by design.** `scripts/validate_data.py` returns exit code 1 whenever it finds data-quality issues in `data/rsvp_responses.json` (currently ~25). A non-zero exit here reflects the data, not a broken environment.
- **`make summary` and `make validate` use only the Python standard library.** No third-party packages are required to run them or the dashboard.
- **`make sync` requires more than the update script installs.** It needs `pandas`/`openpyxl`/`gdown` (installed by the update script) **and** network access to a specific Google Drive spreadsheet, so it generally cannot run in an isolated cloud VM without that file. To exercise `scripts/sync_from_sheet.py` offline, pass a local `.xlsx` with a `Form Responses 3` sheet.

### Tests / lint

There is no automated test suite and no linter configuration in this repo; "testing" is running the CLI tools and viewing the dashboard as above.
