# JevZoo site

[简体中文](README_zh.md) · [Information architecture](../docs/site/ARCHITECTURE.md) · [Reference analysis](../docs/site/REFERENCE_ANALYSIS.md)

This is a working bilingual static discovery surface for the existing JevZoo platform. Python 3.10+ generates HTML; native JavaScript provides search, filtering and pagination. No Node packages, accounts, backend, tracking, model execution or commercial inference are required. The site works under a static-host subpath.

```bash
python site/build.py --output /absolute/path/outside/git/jevzoo-site --readmes
python site/check.py
python -m unittest discover -s site -p 'test_*.py' -v
python site/audit.py --output /absolute/path/outside/git/jevzoo-site
python -m http.server 8766 --bind 127.0.0.1 --directory /absolute/path/outside/git/jevzoo-site
```

Browse `http://127.0.0.1:8766/en/` or `/zh/`. Use HTTP for the interactive catalog; opening a file directly cannot fetch the generated JSON reliably. Homepages and resource details are prerendered. Slash focuses search, native controls support the keyboard, and URL parameters preserve filters/page across language switching. No scripts execute evaluation commands.

## Update once, generate consistently

Edit **existing** `catalog/catalog.json`, not generated HTML, READMEs or `assets/catalog.json`. Keep stable IDs, a primary resource type, bilingual descriptions, component terms and identifiable sources. Add `related_ids`, source links and aliases to connect paper, code, checkpoints, data and recipes. Purposes are many-to-many; type counts are exclusive. Generated canonical mappings retain legacy `discovery_id` and `curated_ids` fields.

`site/enrich_catalog.py` is an optional metadata-import tool for a pinned reference source and an existing verified review. It reads public text and GitHub metadata only. Preserve manual editorial changes when reimporting; review its audit/diff before accepting imports. Routine edits need only the offline build. The existing `jevzoo catalog` renderer invokes the site builder after its legacy cards; upstream refresh preserves editorial metadata, removed/failed entries and added assets, and flags changed text for translation review. It may still scan historical runs in its legacy step: use the standalone site build while evaluations are active.

Source availability, primary capability claims, visible loaders, adapter implementation, smoke and full evaluation are different evidence. Link checks never grant runnable badges. Upstream claims remain claims. Public-site result rows must match exact approved release hashes **and** checkpoint/dataset revisions; mismatching pending summaries are omitted. `site/approved-results-manifest.json` is a hash projection of an existing approved release, not a new approval. Change it only from a valid approval receipt/candidate and rerun tests; never approve results by editing this file. Formal training recipes remain pending; two Lab recipes have smoke evidence and require Lab access.

## Hosting and publication

The output directory is a self-contained static artifact. A reviewed deployment can use GitHub Pages, Cloudflare Pages or any static HTTP host. No DNS, hosting configuration or deployment has been changed by this work. Configure compressed delivery and caching for `assets/catalog.json` (roughly 2.3 MB uncompressed; fetched only by catalog pages). Resource HTML stays directly navigable.

The existing release contract remains authoritative: a reviewed, committed clean Lab, passing current checks, public-baseline validation, an explicit file whitelist and approval of the exact release ID/content hash precede publication. `scripts/public_manifest.py` now includes site source/docs; it does not authorize deployment. The formal candidate is prepared from a checked, committed isolated Lab branch using the existing release prepare command. Its exact file hashes bind the publication scope. The active evaluation checkout and unrelated WIP remain untouched. Public source synchronization and deployment wait for exact-release approval.

## Attribution and limits

English/Chinese upstream catalog descriptions derive from `heyjunpenn/awesome-jev@39854d858fff73bf3172949c9f968c6cb12beafa` under MIT. Its notice remains in `NOTICE` and `licenses/awesome-jev-MIT.txt`. JevZoo’s UI/build code and favicon are original. No upstream logos, videos, screenshots or paid sponsor backend are distributed. Model/data/component licenses remain their own terms. ETHACC stays an unresolved keyword. Most broad entries have link evidence, not application execution or independent capability verification.

## Fixed deployment payload

`site/deployment-manifest.json` contains SHA-256 for every static file and is itself whitelisted, so the formal release hash also binds the website payload. Run `python site/deployment.py verify --output /absolute/path/outside/git/jevzoo-site` after rebuilding; `archive` produces a stable ZIP. Diagnostic reports/timestamps are excluded; `.nojekyll` is included. `--no-source-write` supports verification from a clean committed branch.

Proposed target: `https://jinlong17.github.io/Jev-Zoo/`, root of the public repository's `gh-pages` branch. No branch or Pages settings have been changed. Branch-based GitHub Pages still uses a deployment workflow; the effect of existing account Billing on Pages is unverified, so no live deployment is claimed. After approval deploy only matching bytes, then verify the remote URL, locales and catalog JSON.

Pinned approved evidence: 120 summaries (110 smoke + ten JevBench public full). Builds prefer the committed hash projection and do not relabel results when a newer public release marker appears. New full results require separate review and an explicit projection update.
