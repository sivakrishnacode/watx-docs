# Watx docs

Documentation for [Watx](https://app.watx.in), built on [Mintlify](https://mintlify.com)
and deployed from `main`.

- `DOCS_PLAN.md` — the map: audience, scope, source-of-truth references into the
  product repo, writing rules, page inventory, progress. Read it first.
- `AGENTS.md` — terminology, style and boundaries for anyone (or any agent) writing here.
- `docs.json` — site config and navigation. Navigation is **generated** from the
  page tables in `DOCS_PLAN.md`; edit the plan, then regenerate.
- `openapi.yaml` — the public API, rendered as one page per operation.
- `postman/watx-api.postman_collection.json` — generated from `openapi.yaml`.

## Scripts

```bash
python3 scripts/build-nav.py . --write --api-ops scripts/api-operations.txt   # docs.json navigation from DOCS_PLAN.md
python3 scripts/build-postman.py .                                           # Postman collection from openapi.yaml (needs PyYAML)
python3 scripts/lint-docs.py .                                               # frontmatter, H1s, images, links, internal leakage
```

## Preview and validate

```bash
npm i -g mint
mint dev            # http://localhost:3000
mint validate       # strict build check
mint broken-links
```
