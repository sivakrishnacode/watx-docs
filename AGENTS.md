# Documentation project instructions

## About this project

- This is the documentation site for **Watx** (`app.watx.in`), a WhatsApp-first
  customer messaging and CRM platform, built on [Mintlify](https://mintlify.com).
- Pages are MDX files with YAML frontmatter. Configuration lives in `docs.json`.
- `DOCS_PLAN.md` is the map: audience, what is out of scope, where the truth for
  every page lives in the product repo, writing conventions, the page inventory
  and progress. Read it before writing or restructuring anything.
- The product source code is the source of truth. Prose notes in the product
  repo's `docs/` folder are reference and can be stale; when they disagree with
  the code, the code wins.

## Terminology

- **workspace** — one business's tenant. Never "account" or "tenant".
- **member** — a person in a workspace. Roles: **owner**, **admin**, **agent**,
  **viewer**. Spell the role as "the Agent role" so it is never confused with an
  AI agent.
- **agent** — an AI agent. A human teammate is a member.
- **contact**, **conversation** — the CRM record and the thread. "chat" is only
  used for the website widget.
- **template** — a WhatsApp message template approved by Meta.
- **WhatsApp Flow** — Meta's native form screens. **flow** (lowercase) — the Watx
  chatbot builder. Always disambiguate.
- **automation** — a trigger-and-steps rule in the automations engine.
- **Sales documents** — the invoicing integration (invoices, receipts,
  quotations, and so on).
- Channels are exactly **WhatsApp**, **Instagram** and **Website**.

## Style preferences

- Active voice, second person ("you"), present tense.
- Keep sentences concise — one idea per sentence.
- Sentence case for headings. No H1 in the body; the title is the H1.
- Bold for UI elements exactly as the product labels them: Click **Settings → API keys**.
- Code formatting for values, keys, endpoints and paths.
- Say what the product does, including limits and failure cases. No marketing.
- No images until we have real screenshots. Do not reference any.
- Links are root-relative (`/whatsapp/templates`).
- Never hard-code a plan price; link to the in-app pricing page.

## Content boundaries

- Do not document: Meta Ads Manager (gated, unreleased), voice or calling
  (not built), the internal admin panel, deployment or infrastructure, or
  anything on the roadmap.
- Do not copy internal file paths, migration numbers, class names or the
  warning notes from the product repo's `CLAUDE.md` into public pages.
- Do not invent a screen, a label, a limit or a Meta policy detail. If it
  cannot be verified in the code, leave it out.
