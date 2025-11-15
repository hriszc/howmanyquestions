# Repository Guidelines

## Project Structure & Module Organization
Each calculator lives in a folder named after the original query (for example `how many cups in a quart/`), and all UI plus logic stays inside that folder’s `index.html` with any notes beside it. Root-level assets include the navigation landing page (`index.html`), menu data (`navigation_data.json`), sharing utilities (`share-utils.js`, `add-sharing-to-pages.js`), and automation scripts (`navigation_generator.py`, `sitemap_generator.py`, `navigation_updater.sh`, `update_sitemap.sh`). Generated files (`sitemap.xml`, `robots.txt`, backups, `cron.log`) should never be edited manually.

## Build, Test, and Development Commands
- `python3 navigation_generator.py` — scans the repository for `*/index.html`, refreshes `navigation_data.json`, and prints a status table.
- `bash navigation_updater.sh` — cron-ready wrapper that backs up `navigation_data.json`, runs the generator, logs to `cron.log`, and commits when new tools are found.
- `python3 sitemap_generator.py` or `bash update_sitemap.sh` — rebuilds `sitemap.xml`; the shell script also reports URL counts and pending git changes.
- `python3 -m http.server 8000` — quick local preview; navigate to `http://localhost:8000/<folder-name>/`.

## Coding Style & Naming Conventions
HTML, CSS, and vanilla ES6 JavaScript use four-space indentation, CSS custom properties for the iOS gray palette, and descriptive classes such as `.calculator-card` or `.share-section`. Prefer `const`/`let`, camelCase helpers, and keep shared utilities at the repo root. Folder names mirror the query string—including spaces or zero-width characters—because automation keys off `folder_name`, so copy the existing spelling when duplicating a tool.

## Testing Guidelines
No automated framework exists, so rely on repeatable manual checks. After editing a calculator, load it through the local dev server and verify inputs, outputs, and share buttons. Exercise the sharing module via `test-sharing.html`, then run the navigation and sitemap generators and inspect the diffs for malformed URLs or stray whitespace before committing.

## Commit & Pull Request Guidelines
Commits use short imperative titles similar to recent history (`update sitemap`, `add:how many ounces in a pint`); include the tool or script name when possible (`nav: refresh categories`). Pull requests should summarize scope, list commands executed (generators, sitemap, manual QA), link any planning issue or markdown doc, and attach screenshots when UI changes. Avoid bundling unrelated calculators, and flag if automation constants like `PROJECT_DIR` inside `navigation_updater.sh` require operator updates.

## Automation & Security Notes
Cron tasks depend on absolute paths inside `navigation_updater.sh`, so adjust them whenever the repo moves. Keep scripts idempotent (`set -e`, backups before writes) and never store credentials—the tooling only touches local files and git. Log operational output to `cron.log` for traceability instead of stdout.
