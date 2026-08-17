# Approved Tasks Report (2026-08-11)

Static HTML gallery of approved BrowserGym breaker tasks (UI-oracle + Sol agent screenshots).

## View online

**Breaker-7 verification pack (dedicated, not the 115-card hub):** https://deccanai-org.github.io/approved-tasks-report/breaker-10/

**Hub (all tasks, three sections):** https://deccanai-org.github.io/approved-tasks-report/  
same catalog: https://deccanai-org.github.io/approved-tasks-report/hub/

**UI series — ui_031–ui_060 (Tentative, Sol seed0 14 Aug):** https://deccanai-org.github.io/approved-tasks-report/dossier/ui031-ui060.html

**D series — D460–D481 (Tentative, Sol seed0 13 Aug):** https://deccanai-org.github.io/approved-tasks-report/dossier/d460-d481.html

Hub cards and both set pages include expandable **text step trajectories** (action / page / reasoning) plus eval gold/forbidden. Screenshots stay optional and are not required.

**Dossier (breakers only):** https://deccanai-org.github.io/approved-tasks-report/dossier/

**QA prompt-review set (13 Aug, env-audited):** https://deccanai-org.github.io/approved-tasks-report/dossier-qa/

Each QA task page has an **Oracle path** (tip gold-path film) and an **Agent/Sol path** (every seed0 step, thumbnail + lightbox + model reasoning). Assets live under `dossier-qa/assets/` (relative URLs). Raw PNG/tars in `dossier-qa/_raw/` are not published.

**N440–N449 Sol seed0 set:** https://deccanai-org.github.io/approved-tasks-report/dossier/n440-n449.html

**mail_002 Sol seed0 trajectory (0fff244a):** https://deccanai-org.github.io/approved-tasks-report/mail002-0fff244a/

Relative image paths work there. Repo: https://github.com/deccanai-org/approved-tasks-report

## Local viewing

**Do not open the HTML file alone.** Screenshots live in a sibling assets folder.

Correct layout:

```text
APPROVED_TASKS_REPORT_2026-08-11.html   # 11 Aug screenshot gallery (index.html is now the hub)
APPROVED_TASKS_REPORT_2026-08-11_assets/
  mail_002/oracle/thumbs/...
  mail_002/oracle/full/...
  ...
```

If you only receive/email the `.html` file (without the `_assets` folder), browsers show **beige placeholders** with alt text — images are not embedded in the HTML.

Also keep the HTML and `_assets` folder next to each other (same directory). Moving or renaming only the HTML breaks relative `src` / lightbox `href` paths.

## What’s included

- Gallery thumbs + full-resolution lightbox JPEGs for each task
- `_raw` PNG dumps from the original audit are **not** published here (not referenced by the HTML; keeps the repo under size limits)
