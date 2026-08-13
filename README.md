# Approved Tasks Report (2026-08-11)

Static HTML gallery of approved BrowserGym breaker tasks (UI-oracle + Sol agent screenshots).

## View online

**Live:** https://deccanai-org.github.io/approved-tasks-report/

**Dossier (breakers only):** https://deccanai-org.github.io/approved-tasks-report/dossier/

**mail_002 Sol seed0 trajectory (0fff244a):** https://deccanai-org.github.io/approved-tasks-report/mail002-0fff244a/

Relative image paths work there. Repo: https://github.com/deccanai-org/approved-tasks-report

## Local viewing

**Do not open the HTML file alone.** Screenshots live in a sibling assets folder.

Correct layout:

```text
APPROVED_TASKS_REPORT_2026-08-11.html   # or index.html
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
