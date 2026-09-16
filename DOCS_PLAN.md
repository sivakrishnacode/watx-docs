# Watx docs — plan and progress

> Working file for the agents building `docs.watx.in` (this repo, Mintlify
> deployment `watx`). It holds the **map**, not the content: what pages exist,
> where the truth for each one lives in the product repo, the rules every page
> follows, and how far along we are. Keep it accurate; it is the only place
> progress is recorded. Not published (listed in `.mintignore`).

Owner: Fable (plan, navigation, validation, publishing). Writers: Opus
subagents, one per batch, writing MDX directly into this repo. Writers never
edit `docs.json` or this file — they report back and Fable updates both.

---

## 1. What we are documenting

**Watx** (`app.watx.in`) is a WhatsApp-first customer messaging and CRM
platform: one shared inbox for **WhatsApp** (official Meta Cloud API),
**Instagram** (DMs, story replies, comments) and a **website chat widget**,
with contacts and segments, deal pipelines, a no-code **automation** engine,
a visual WhatsApp **flow** builder, forms and bookings, **AI agents**, an
integrations layer (Shopify, WooCommerce, Razorpay, Google via Apps Script,
Zapier, n8n), sales documents (invoices, receipts, quotations), and a
public REST API with webhooks. Multi-tenant: a **workspace** per business,
a login may belong to several workspaces.

Product repo (source of truth): `/home/sivakrishna/Desktop/Watx/watx-app`.
Everything below refers to paths inside it unless stated.

Audience, in order: (1) a business owner or operator setting Watx up and
using it daily, (2) an agency running several workspaces, (3) a developer
integrating through the API and webhooks. Write for (1) by default.

### Out of scope — do not document
- **Voice / WhatsApp calling** — proposed only (`docs/whatsapp-calling.md`).
- **The admin panel** (`apps/admin-panel`) — internal operations tool.
- **Deployment, infrastructure, migrations, queues** — internal.
- Anything in `docs/marketing/roadmap.md` — it is not shipped.
- Internal warnings, file paths, migration numbers, class names and the
  reasoning notes in `CLAUDE.md`. Those explain *why* the product behaves
  as it does; the docs say *what it does* and *how to use it*.

---

## 2. Source of truth map

Read these before writing the pages they back. Product behaviour comes from
code; prose docs in `docs/` are reference and sometimes stale — when they
disagree, the code wins, and the writer says so in the report.

| Topic | Read |
| --- | --- |
| Everything, orientation | `CLAUDE.md` (long; skim the section for your batch), `docs/marketing/features.md` (what ships, in plain words — verified 12 Aug 2026) |
| Routes (what screens exist) | `apps/web/src/app/(dashboard)/**/page.tsx`, public routes under `apps/web/src/app/(public)`, `(auth)`, `(onboarding)` |
| Navigation labels | `apps/web/src/lib/nav/channels.ts`, `apps/web/src/components/settings/settings-sections.ts`, `apps/web/src/components/layout/app-sidebar.tsx` |
| Sign-up, login, Google, password reset, workspace selection | `apps/web/src/app/(auth)`, `apps/web/src/app/auth/callback/route.ts`, `(onboarding)/welcome`, `(onboarding)/select-workspace`, `(onboarding)/billing` |
| Multi-workspace, roles, invitations, members | CLAUDE.md "Multi-workspace"; `apps/api/src/account/**`, `apps/web/src/components/workspace/**`, `(dashboard)/members` |
| Plans, trial, billing, cancel, entitlement | CLAUDE.md "Plans & billing"; `apps/api/src/subscription/**`, `docs/razorpay-subscriptions.md`, `docs/subscription-setup.md`, `supabase/migrations/066_*.sql` (limits), `084_*.sql` (AI agent caps) — **never hard-code a price**; prices are edited live |
| WhatsApp connect (Embedded Signup), requirements | `docs/meta-platform-setup.md` §11 (customer connect flow) and §12 (policy constraints); `apps/api/src/whatsapp/services/connect-account.service.ts`; `(dashboard)/onboarding` (channel checklist) |
| WhatsApp templates (create, submit, variables, media, buttons, carousel, library) | `apps/web/src/lib/whatsapp/template-*.ts` (form, validators, slots, library, packs, store-template-bundle), `apps/api/src/whatsapp/controllers/whatsapp-templates.controller.ts`, CLAUDE.md "WhatsApp templates" |
| Broadcasts, campaigns, CTWA, catalog/orders, WhatsApp Flows, analytics, settings | `(dashboard)/channels/whatsapp/**`, `apps/api/src/whatsapp/**`, `apps/api/src/campaigns/**`, `docs/meta-flows-*` if present, `apps/web/src/lib/whatsapp/meta-api.ts` |
| The 24-hour window, messaging limits and quality | `apps/api/src/whatsapp/wa-window.util.ts`, `apps/api/src/whatsapp/services/messaging-limits.service.ts` |
| Instagram | `docs/instagram.md`, CLAUDE.md "Instagram — the creator surfaces", `apps/web/src/components/channels/instagram/**`, `apps/web/src/lib/instagram/**`, `apps/api/src/instagram/**` |
| Website widget | `docs/web-channel-plan.md` §7 (feature checklist), `apps/web/src/app/(dashboard)/channels/web/**`, `apps/web/src/app/(public)/widget/v1/frame`, `apps/web/public/widget/v1`, `apps/api/src/web/**` |
| Inbox | `apps/web/src/components/inbox/**` (composer, thread, bubble, sidebar), `apps/web/src/lib/inbox/**`, features.md §1 |
| Contacts, fields, tags, import, address, activity timeline | `(dashboard)/contacts`, `apps/web/src/components/contacts/**`, `apps/api/src/contacts/**`, CLAUDE.md "Contacts — the address and the activity timeline" |
| Segments | CLAUDE.md "Segments"; `apps/web/src/lib/segments/rules.ts`, `apps/web/src/components/segments/**` |
| Pipelines & deals, team performance, media library, notifications | `(dashboard)/pipelines`, `(dashboard)/team-performance`, `(dashboard)/media` + `apps/web/src/components/media/media-library.tsx` + CLAUDE.md "Media library", `(dashboard)/notifications` |
| Automations | CLAUDE.md "Automations"; `apps/web/src/lib/automations/step-meta.tsx` (every step + category), `trigger-catalog.tsx` (every trigger), `availability.ts`, `diagnostics.ts`, `app-presets.ts`; `apps/api/src/automations/**` (`automation-interpolation.util.ts` = tokens and filters), `docs/automation-canvas-design.md` |
| Flows | CLAUDE.md "Flows"; `apps/web/src/lib/flows/types.ts`, `apps/web/src/components/flows/shared.tsx` (node list), `apps/api/src/flows/**`, `apps/api/src/ai/lib/flow-draft.ts` |
| Forms & bookings | CLAUDE.md "Forms"; `apps/api/src/forms/form.types.ts` (field types, visibility, formats), `apps/web/src/components/forms/**`, `apps/web/src/lib/forms/**`, `(public)/f/[slug]`, `(public)/book/[slug]`, `book/manage/[token]` |
| AI agents | CLAUDE.md "AI agents"; `apps/api/src/ai/lib/skills.ts` (skill ids, config fields, defaults), `lib/tools/*`, `lib/defaults.ts`, `apps/web/src/components/agents/**`, `lib/agent-templates.ts`, `agent-readiness.tsx`, `apps/api/src/ai/credits/**` |
| Shopify / WooCommerce / store console / COD | `docs/shopify-connect-guide.md`, `docs/shopify-app.md`, CLAUDE.md "Connected stores"; `apps/web/src/components/stores/store-console.tsx`, `apps/api/src/ecommerce/**`, `apps/web/src/lib/ecommerce/store-recipes.ts` |
| Razorpay customer payments | `docs/razorpay-payments.md`, CLAUDE.md "Customer payments"; `apps/api/src/payments/**`, `apps/web/src/components/integrations/razorpay-card.tsx`, `(dashboard)/payments` |
| Sales documents (invoices, receipts, quotations…) | `docs/invoices.md`, CLAUDE.md "Invoices and GST bills"; `apps/api/src/invoices/**` (`lib/document-types.ts`, `lib/invoice-template.ts`, `lib/appearance.ts`), `apps/web/src/components/invoices/**` |
| Google (Apps Script bridge) | `docs/google-apps-script.md`, CLAUDE.md "Google — the Apps Script bridge"; `apps/api/src/google-script/google-script.catalog.ts` (every action and field), `apps/web/src/components/integrations/connected-apps.tsx` |
| Zapier, n8n, other services | CLAUDE.md "Outbound webhooks"; `apps/web/src/lib/webhooks/providers.ts`, `apps/web/src/components/settings/webhook-integration-config.tsx`, `apps/api/src/integrations/**`, `apps/web/src/lib/automations/app-presets.ts` |
| Public API & webhooks | `docs/public-api.md` (primary), `apps/api/src/v1/controllers/*.ts` (every route, body, query, response), `apps/api/src/auth/decorators/require-scope.decorator.ts` (scopes), `apps/api/src/v1/utils/webhooks.util.ts` (events, signing), `apps/api/src/auth/guards/api-key.guard.ts`, `apps/api/src/common/rate-limit*`; API keys UI: settings → API keys |
| Settings screens | `apps/web/src/components/settings/**` |
| Data deletion / privacy pages | `apps/web/src/app/instagram-data-deletion`, `meta-data-deletion`; Meta callbacks `apps/api/src/meta-privacy` (`https://api.watx.in/meta/privacy/*`) |

Fixed facts to use verbatim:
- App: `https://app.watx.in`. API host: `https://api.watx.in` (public API base path `/v1`; the app host also proxies `/api/*` — the API writer confirms which base URL to publish from `apps/web/next.config.*` and `docs/public-api.md`, and uses one consistently).
- Support: `support@watx.in`.
- Plans: **Starter**, **Growth**, **Enterprise**. One 15-day trial per workspace. Limits live in the product (contacts, messages/month, broadcasts/month, flows, team members, storage, AI agents: Starter 1 / Growth 5 / Enterprise unlimited). Link to the in-app pricing page for amounts.
- Roles: **owner**, **admin**, **agent**, **viewer**.
- Channels: WhatsApp, Instagram, Website. Nothing else.
- The invoicing integration is called **Sales documents** in the product.

---

## 3. Conventions every page follows

**Format.** Mintlify MDX. Frontmatter: `title`, `description` (one sentence,
what the reader gets), optional `sidebarTitle` when the title is long,
optional `icon`. Sentence-case headings. No H1 in the body (the title is
the H1). Start with one or two sentences saying what the page is for and
who it is for.

**Voice.** Second person, active, present tense. Short sentences. Bold UI
labels exactly as they appear in the product (**Settings → API keys**).
Code font for values, keys, paths, endpoints. No exclamation marks, no
marketing. Say what happens, including the limits and the failure cases —
"a message outside the 24-hour window is refused unless it is a template"
is more useful than "reach customers any time".

**Components** (Mintlify): `<Steps>`/`<Step>` for procedures, `<Note>`,
`<Tip>`, `<Warning>`, `<Info>` sparingly (one or two per page), `<Card>`/
`<CardGroup>` on overview pages, `<Tabs>` for alternatives (e.g. Shopify
OAuth vs custom app), `<Accordion>` for long optional detail, `<CodeGroup>`
for multi-language samples, `<ParamField>`/`<ResponseField>` on API pages.
No images: we have no screenshots yet, so do not reference any. No
`<Frame>` with a placeholder. Tables for catalogues (triggers, steps, node
types, skills, field types, scopes, events).

**Truth.** Every claim must be visible in the product or the code. If a
setting, label or limit cannot be verified, leave it out and list it under
"Unverified" in the report. Never invent a screen, a button label, a plan
amount, or a Meta policy detail. Prefer the code's own wording for labels.

**Links.** Root-relative to this repo (`/whatsapp/templates`). Link
generously between related pages; every catalogue entry that has its own
page links to it. External links only to Meta, Shopify, Razorpay, Google,
Zapier, n8n official docs.

**Names.** "workspace" (never "account" or "tenant"), "member", "contact",
"conversation" (never "chat" for the record; "chat" is fine for the
widget), "template" (WhatsApp message template), "WhatsApp Flow" (Meta's
native form) vs "flow" (Watx chatbot builder) — always disambiguate,
"automation", "agent" = AI agent; a human teammate is a "member" (the
role named `agent` is spelled out as "the Agent role"), "Sales documents".

**Length.** A how-to page is 300–900 words. A catalogue/reference page can
be longer. An overview page is short and made of cards.

---

## 4. Information architecture

Three tabs. Slugs are file paths under the repo root (`.mdx` omitted).
`index.mdx` is the site home.

### Tab: Guides

| Group | Slug | Title | What it covers | Batch |
| --- | --- | --- | --- | --- |
| Getting started | `index` | Introduction | What Watx is, who it is for, three channels, card grid into each section | A |
| Getting started | `getting-started/quickstart` | Quickstart | Sign up → name the workspace → pick a plan (trial) → connect WhatsApp → send the first message → invite a teammate | A |
| Getting started | `getting-started/concepts` | Core concepts | Workspace, members and roles, contacts, conversations, channels, templates and the 24-hour window, automations vs flows vs agents | A |
| Getting started | `getting-started/workspaces` | Workspaces | One login, several workspaces; the switcher; the no-workspace state; how membership is granted (invite or admin) | A |
| Getting started | `getting-started/plans-and-billing` | Plans and billing | Starter/Growth/Enterprise, the one trial, what counts against limits, automatic renewal via Razorpay mandate, dunning/past due, cancel at cycle end, who can pay (owner), Enterprise enquiry | A |
| Account | `account/sign-in` | Signing in | Email + password, Google, email confirmation, password reset, invited sign-up | A |
| Account | `account/security-and-privacy` | Security and privacy | Where credentials are stored (encrypted), what members can see, data deletion requests (Instagram / Meta), support contact | A |
| Settings | `settings/overview` | Settings | Map of the settings rail: account vs workspace groups, who sees what (admin-only, owner-only) | A |
| Settings | `settings/members-and-roles` | Members and roles | Roles and what each can do, inviting, changing a role, removing, transferring ownership | A |
| Settings | `settings/workspace` | Workspace settings | Fields & tags, canned replies, deals & currency, appearance | A |
| Settings | `contacts/team-performance` | Team performance | The report at the foot of Settings → Users & Roles and its metrics | B |
| Settings | `settings/api-keys` | API keys | Creating, scopes, revoking; links to the API tab | A |
| Inbox | `inbox/overview` | Inbox | The three panes, filters, search, unread, channels, realtime | B |
| Inbox | `inbox/conversations` | Working a conversation | Assign, presence, status (open/closed), close/reopen from the list, notes, tags from the sidebar, contact sidebar | B |
| Inbox | `inbox/sending` | Sending messages | Text, media, voice notes, reactions, quoted replies, templates outside the window, product cards, payment links, sales documents from the composer; per-channel differences | B |
| Inbox | `inbox/canned-replies` | Canned replies | Create, shortcuts, use in composer | B |
| Inbox | `inbox/notifications` | Notifications | What notifies, where, browser notifications | B |
| Contacts & CRM | `contacts/overview` | Contacts | List, search, filters, bulk actions, import CSV, sources, the contact drawer | B |
| Contacts & CRM | `contacts/fields-and-tags` | Fields and tags | Built-in fields, address, custom fields, tags; where they are edited | B |
| Contacts & CRM | `contacts/segments` | Segments | Static vs dynamic, rule vocabulary, incomplete rules, how segments are used (broadcasts, automations) | B |
| Contacts & CRM | `contacts/activity-timeline` | Activity timeline | What appears (orders, payments, carts, deals, notes, forms, broadcasts, message roll-ups) | B |
| Contacts & CRM | `contacts/pipelines-and-deals` | Pipelines and deals | Stages, creating deals, moving, value/currency, automation and agent hooks | B |
| Contacts & CRM | `contacts/media-library` | Media library | Uploads, reuse across composer/templates/flows/broadcasts, the storage meter | B |
| Automations | `automations/overview` | Automations | What an automation is (trigger → steps → branches), where they run, gallery, AI draft | C |
| Automations | `automations/editor` | The canvas editor | Adding steps, the inspector, branches, yes/no ports, continue edge, keys, layout, saving, activating | C |
| Automations | `automations/triggers` | Triggers | Every trigger with its category, channel-less triggers, keyword matching, time-based | C |
| Automations | `automations/steps` | Steps | Every step by category with config fields, what each publishes | C |
| Automations | `automations/expressions` | Variables and expressions | Namespaces (`contact`, `message`, `vars`, `steps`, `trigger`, `conversation`, `form`, `now`), filters, empty-token rule, type keeping | C |
| Automations | `automations/conditions` | Conditions and branching | Rules, all/any, random split, wait/wait until | C |
| Automations | `automations/channels-and-window` | Channels and the 24-hour window | Scoping to channels, partial support, templates outside the window, channel-less triggers | C |
| Automations | `automations/diagnostics-and-logs` | Diagnostics and logs | Pre-flight checks, activation validation, run logs, pending executions | C |
| Automations | `automations/templates-and-ai` | Templates gallery and Build with AI | Gallery, store recipes note, AI draft (metered), what it can and cannot do | C |
| Flows | `flows/overview` | Flows | WhatsApp-only chatbot builder; when to use a flow vs an automation; runs per contact | C |
| Flows | `flows/editor` | The flow editor | Palette, canvas, inspector, list view, entry node, saving, activating, how a flow starts | C |
| Flows | `flows/nodes` | Node types | All node types with config and ports | C |
| Flows | `flows/waits-and-runs` | Waits, hand-offs and runs | `wait` parking, 24-hour warning, handoff/ai_handoff, start_flow, one active run per contact, the runs screen | C |
| Flows | `flows/testing-and-ai` | Testing and Build with AI | The simulator, AI draft | C |
| Forms | `forms/overview` | Forms and bookings | What forms do, hosted links, where submissions go | D1 |
| Forms | `forms/builder` | The form builder | Tabs, adding fields, field key, half-width, page breaks, publishing | D1 |
| Forms | `forms/field-types` | Field types | Every type, validation formats, required, defaults, mapping to contact fields | D1 |
| Forms | `forms/conditional-logic` | Conditional logic and steps | visible_when, backwards rule, hidden fields, pages | D1 |
| Forms | `forms/appearance` | Appearance | Scheme, accent, preview | D1 |
| Forms | `forms/bookings` | Booking forms | Availability, slots, buffers, capacity, notice, manage link, triggers | D1 |
| Forms | `forms/sharing` | Sharing a form | `/f/<slug>`, `/book/<slug>`, in a chat, the send_form step | D1 |
| Forms | `forms/submissions` | Submissions and automation | Viewing, export, `form_submitted` trigger, webhook event | D1 |
| AI agents | `ai-agents/overview` | AI agents | What an agent does, several per workspace, for every kind of business, honest limits | D2 |
| AI agents | `ai-agents/create` | Create an agent | Blank or role template, plan cap, pause/activate | D2 |
| AI agents | `ai-agents/persona-and-behaviour` | Persona, voice and behaviour | Identity, business description, ground rules, voice, escalation, reply formatting per channel | D2 |
| AI agents | `ai-agents/knowledge` | Knowledge | Workspace library: uploads (PDF/DOCX/text), page crawling, chunks/reindex, per-agent selection | D2 |
| AI agents | `ai-agents/skills` | Skills | Every skill, what it unlocks, which need an integration, config fields and pickers | D2 |
| AI agents | `ai-agents/custom-actions` | Custom API actions | Defining an HTTP action, parameters, headers, linking to agents | D2 |
| AI agents | `ai-agents/routing` | Routing | Channels, priority order, stickiness, no fallback | D2 |
| AI agents | `ai-agents/testing` | Test mode and playground | Test numbers, the drawer, draft replies in the inbox | D2 |
| AI agents | `ai-agents/credits-and-byok` | Credits and your own key | Platform credits vs BYOK, metering, top-ups, model choice | D2 |
| AI agents | `ai-agents/readiness` | Why is my agent silent? | The readiness checklist mirrored from the runtime gates | D2 |
| Integrations | `integrations/overview` | Integrations | The directory page, statuses, card map | E |
| Integrations | `integrations/shopify` | Shopify | Two install methods, what each gives, connecting, reconnecting, disconnecting | E |
| Integrations | `integrations/woocommerce` | WooCommerce | Connecting, creating webhooks by hand, limits | E |
| Integrations | `integrations/store-console` | The store console | Overview · Orders · Carts · Catalogue · Messaging (recipes) · Cash on delivery | E |
| Integrations | `integrations/cash-on-delivery` | Cash on delivery confirmation | The flow, statuses, guardrail, replies, permissions | E |
| Integrations | `integrations/razorpay` | Razorpay payments | Connect keys, webhook, payment template, payment links from five surfaces, statuses, sweep | E |
| Integrations | `integrations/sales-documents` | Sales documents | Document types, enabling, company details, GST mode, numbering | E |
| Integrations | `integrations/sales-documents-sending` | Creating and sending | The four-step dialog, customer picker, payment, preview, sending on WhatsApp, the template and its 13 values, the public link | E |
| Integrations | `integrations/sales-documents-design` | Document design | Layouts, accent, density, paper, blocks, presets, preview | E |
| Integrations | `integrations/google` | Google (Apps Script bridge) | Why a script, the four-step setup, the secret, updating the script | E |
| Integrations | `integrations/google-actions` | Google actions | Every action (Gmail, Calendar, Sheets, Contacts, Docs, Tasks) with fields and outputs; what agents can use | E |
| Integrations | `integrations/zapier` | Zapier | Connect, events, test ping, disabling | E |
| Integrations | `integrations/n8n` | n8n | Connect, production vs test URL, events | E |
| Integrations | `integrations/other-services` | Other services | HTTP request presets (Slack, Notion, Airtable…) | E |
| Troubleshooting | `troubleshooting/whatsapp` | WhatsApp delivery | Window, template rejected/paused, media fetch, quality/limits | I |
| Troubleshooting | `troubleshooting/instagram` | Instagram | Token expiry, deleted comments, DM window | I |
| Troubleshooting | `troubleshooting/automations-and-agents` | Automations and agents | Silent failures, diagnostics, agent readiness, two-replies gate | I |
| Troubleshooting | `troubleshooting/integrations` | Integrations | Shopify secrets, webhook signature, Razorpay, Google 302/dev URL | I |
| Troubleshooting | `troubleshooting/faq` | FAQ | Short answers with links | I |

### Tab: Channels

| Group | Slug | Title | What it covers | Batch |
| --- | --- | --- | --- | --- |
| WhatsApp | `whatsapp/overview` | WhatsApp | What the channel gives, the sub-sections, requirements | F |
| WhatsApp | `whatsapp/connect` | Connect your number | Business portfolio, verification, Embedded Signup, display name, what happens after, the onboarding checklist | F |
| WhatsApp | `whatsapp/settings` | Channel settings | Everything on the settings page | F |
| WhatsApp | `whatsapp/messaging-window` | The 24-hour window | The rule, what counts as inbound, what can be sent outside, how Watx handles it everywhere | F |
| WhatsApp | `whatsapp/templates` | Message templates | Categories, creating, variables (positional/named), headers, buttons, carousels, submitting, statuses, editing/deleting, send-time values | F |
| WhatsApp | `whatsapp/template-library` | Template library and packs | Collections, starters, submitting a pack, the store bundle | F |
| WhatsApp | `whatsapp/broadcasts` | Broadcasts | Audience (tags/segments/exclusions), template, variables, media, when to send, drafts, duplicating, the four tabs, statuses, recipients, retries | F |
| WhatsApp | `whatsapp/scheduled-broadcasts` | Scheduled and repeating broadcasts | Schedule once, repeat (daily/weekly/monthly, time zone, ends), the Scheduled and Repeating tabs, send-time checks and failure reasons | F |
| WhatsApp | `whatsapp/catalog-and-orders` | Catalog and orders | Product catalog, product messages, orders | F |
| WhatsApp | `whatsapp/whatsapp-flows` | WhatsApp Flows | Meta's native forms: what they are, managing, sending | F |
| WhatsApp | `whatsapp/click-to-whatsapp` | Click-to-WhatsApp ads | Tracked ads, attribution | F |
| WhatsApp | `whatsapp/analytics` | Analytics | The overview metrics | F |
| WhatsApp | `whatsapp/limits-and-quality` | Messaging limits and quality | Tiers, quality rating, what Watx shows | F |
| Instagram | `instagram/overview` | Instagram | DMs, story replies, comments; how it differs from WhatsApp; the 7-day window | G |
| Instagram | `instagram/connect` | Connect Instagram | Business/creator account, Business Login, token refresh, reconnecting | G |
| Instagram | `instagram/posts` | Posts and automation | The grid, coverage, automating a post, bulk automate | G |
| Instagram | `instagram/comments` | Comments | Triage, filters, keyboard shortcuts, reply/hide/delete, private reply | G |
| Instagram | `instagram/comment-funnels` | Comment funnels | The editor rail, templates, results | G |
| Instagram | `instagram/dm-agents` | DM agents | Instagram-scoped AI agents | G |
| Instagram | `instagram/intents` | Intents | What the intents page does | G |
| Instagram | `instagram/settings-and-analytics` | Settings and analytics | Master switch, settings, analytics | G |
| Website | `website/overview` | Website chat | What the widget does, sessions, identity | G |
| Website | `website/install` | Install the widget | The embed snippet, where to paste, verifying | G |
| Website | `website/settings` | Widget settings | Appearance, greeting, hours, position, launcher | G |
| Website | `website/behaviour` | Behaviour | Whatever the behaviour page configures | G |
| Website | `website/sessions-and-analytics` | Sessions and analytics | Sessions list, analytics | G |

### Tab: API reference

| Group | Slug | Title | What it covers | Batch |
| --- | --- | --- | --- | --- |
| Overview | `api/introduction` | API introduction | Base URL, versioning, what you can do, quick example | H |
| Overview | `api/authentication` | Authentication | Creating a key in settings, bearer header, scopes table, revoking | H |
| Overview | `api/requests-and-responses` | Requests and responses | Envelope, errors, pagination, rate limits and headers, idempotency notes | H |
| Overview | `api/webhooks` | Webhooks | Events, endpoint management, payload, signature verification (with code), delivery/retries/auto-disable, Zapier/n8n note | H |
| Overview | `api/postman` | Postman collection | Download + import steps + variables; the file `postman/watx-api.postman_collection.json` is GENERATED from `openapi.yaml` by `scripts/build-postman.py` — regenerate after any spec change | Fable |
| Endpoints | `openapi.yaml` | (generated pages) | OpenAPI 3.1 spec covering every `v1/*` route with schemas and examples; Mintlify renders one page per operation | H |

`openapi.yaml` lives at the repo root. Navigation references operations as
`"GET /contacts"` strings (no `/v1` — the spec's server URL carries it); Fable wires them
from the writer's recommended list, grouped by tag.

---

## 5. Batches and progress

Legend: ⬜ not started · 🟡 writing · 🟢 written, unreviewed · ✅ reviewed and in nav · ⛔ blocked

| Batch | Pages | Writer | Status | Notes |
| --- | --- | --- | --- | --- |
| A — Getting started, Account, Settings | 11 | Opus | 🟢 | 11/11. Stripe and yearly billing omitted (disabled/unused in product); transfer ownership and leave have no UI; invitations are share links, not emails. |
| B — Inbox, Contacts & CRM | 12 | Opus | 🟢 | 12/12 written. No sales-document action in the composer (claim dropped). Team performance lives under Settings → Users & Roles; consider moving the page to the Settings group. |
| C — Automations, Flows | 14 | Opus | 🟢 | 14/14. Flow fallback policy, keyword `case_sensitive`, time-based `timezone` and Ask-node `regex` omitted: accepted by the API, no UI or ignored by the runner. |
| D1 — Forms | 8 | Opus | 🟢 | 8/8. `send_booking_link` step omitted (targets a table that no longer exists); form/booking webhook events are not subscribable, so not documented; editor tabs are Build / Settings / Availability / Share / Appointments / Submissions. |
| D2 — AI agents | 10 | Opus | 🟢 | 10/10. Pack sizes and model names not published (live/env-driven). Studio tab six is Routing; Provider & credits is a workspace drawer. |
| E — Integrations | 14 | Opus | 🟢 | 14/14. Google setup lists Calendar, People and Tasks services (the in-app dialog says Calendar only — product bug). Order: sales-documents → sending → design. |
| F — WhatsApp | 13 | Opus | 🟢 | 13/13. Pages say plainly: campaign schedules do not run, CTWA clicks are not captured automatically, sending a WhatsApp Flow is not implemented, products push to Meta only on Sync. |
| G — Instagram, Website | 13 | Opus | 🟢 | 13/13. Meta dashboard setup values omitted (operator-only). Website pages name the product screen they document (Channel Settings → install, Web Widget → settings). |
| H — API reference + openapi.yaml | 4 + spec | Opus | 🟢 | 4 pages + openapi.yaml (24 operations). Base URL published: `https://api.watx.in/v1`; `app.watx.in/api/v1` noted once as the older form. Nav strings are `METHOD /path` without `/v1` (paths are relative to the server). |
| I — Troubleshooting, FAQ | 5 | Opus | 🟢 | 5/5 (128 symptoms, 25 FAQ). The "Untitled" PDF symptom omitted: fixed in the product on 2026-09-15. |
| Nav, config, validation, publish | — | Fable | ✅ | `docs.json`, `AGENTS.md`, `mint` validation, commit, push |

Per-page status is tracked in §4 only at batch level to keep this file
short; a writer's report lists any page it could not finish and why, and
that note lands in the table above.

---

## 6. Writer report format (what each batch returns)

1. Files written (paths).
2. Suggested sidebar order if different from §4.
3. Unverified or deliberately omitted claims, each with the reason.
4. Places where `docs/*.md` and the code disagreed, and which was used.
5. Cross-links made to pages outside the batch (so Fable can check they exist).

---

## 7. Validation and publishing checklist (Fable)

- [x] Every slug in §4 exists as a file, or is marked omitted with a reason.
- [x] `docs.json` navigation lists every page exactly once; no orphans.
- [x] Frontmatter present on every page; no H1 in bodies; no image refs.
- [x] Internal links resolve (`scripts/lint-docs.py`, then `mint validate` and `mint broken-links`).
- [x] `openapi.yaml` validates; every operation appears in the API tab.
- [x] Site config: name, colours, logo, favicon, navbar (Dashboard →
      app.watx.in, Support → support@watx.in), footer, no Mintlify links left.
- [x] `AGENTS.md` carries the terminology and boundaries from §1–§3.
- [x] `git commit` on `main`, push → Mintlify deploys `watx`.

---

## 8. Product findings from writing (for the app repo, not the docs)

- `template_status` notifications are raised by the API but rejected by
  `notifications_type_check` (latest definition, migration 109) and swallowed.
- "Mark all as read" on notifications carries no account filter: on a
  multi-workspace login it clears every workspace's unread.
- Delete-pipeline dialog says deals are "archived"; they cascade-delete.
- Team performance tile "Team median reply" computes a weighted mean.
- "Weighted value" tooltip says "Won = 100%" but won deals are excluded.
- Activity timeline links to `/pipelines?deal=<id>`; the page ignores `deal`.
- `renameAsset()` exists but is not wired into the media library UI.
- Public API: `EntitlementGuard` throws a plain `HttpException`, so a 402 on
  `POST /messages` / `POST /contacts` loses its `code` in the v1 envelope.
- Public API: `type: product` / `product_list` on `POST /messages` always 400
  (`interactiveProductParams` never populated). Instagram sending via
  `conversation_id` is unreachable (only `to` is accepted, WhatsApp only).
- Public API: broadcast `suppressed` count computed but not returned;
  `expiresInDays` accepted by the key endpoint but the Settings dialog never
  sends it; a bare key without `Bearer ` is accepted.
- `docs/public-api.md` is stale: missing `contact.created` and every
  segments route; says webhooks are single-attempt (code retries 5×, disables
  after 15 consecutive failures); says the limiter is in-memory (it is Redis).
- Forms: `send_booking_link` step reads an `appointment_types` table that
  migration 055 removed, so its picker is empty and the step can only fail.
- Forms: `forms.notify` (email recipients) is saved but nothing sends;
  `captcha` setting has no UI or enforcement; `file` field has no upload
  endpoint; `checkbox` type renders a list but validates as yes/no.
- Forms: `form.submitted` / `booking.*` events are dispatched but rejected by
  `normalizeEvents`, so no customer can subscribe to them.
- Forms: the Availability tab still renders a dead Google Calendar card.
- Account: transfer ownership and leave workspace exist in the API with no
  web caller; API-key create/revoke role gate is UI-only (no `@RequireRole`);
  password minimum is 6 at signup/reset and 8 in Settings.
- AI agents: the test drawer really executes writing tools (Google, custom
  actions) — `mode: 'auto_reply'` — while its copy says nothing is sent.
- AI agents: draft mode carries no channel, so drafts use plain-text
  formatting instead of WhatsApp markup; playground does not render
  `credits_charged`; `GET /ai/credits/ledger` has no web caller; custom
  actions accept plain `http` although the form says https.
- ~~WhatsApp: `campaign_schedules` has no worker — schedules never run~~ —
  fixed 2026-09-16: scheduling moved into Broadcasts and a worker runs it.
  `retargeting_audiences` still has no code references.
- WhatsApp: the CTWA **Copy tracking link** points at `/ctwa/<id>`, a route
  that does not exist; clicks are recorded only through `POST /ctwa/track`
  behind dashboard auth, and the webhook ignores Meta's referral payload.
- WhatsApp: no way to SEND a WhatsApp Flow (no flow message helper, no FLOW
  button, no step or node). Product create/update toast "pushed to Meta
  Catalog" but only **Sync to Meta Catalog** pushes.
- Instagram: the DM agents page lists Flows first in "Who replies first" but
  the Instagram webhook never dispatches flows; the Intents page says keyword
  rules match comments, but comments only fire `instagram_comment`.
- `docs/web-channel-tracker.md` marks Phase 8 not started; the sessions,
  hours and analytics screens exist. `features.md` §6/§11/§13 overstate
  scheduled campaigns, CTWA attribution and where the tier card lives.
- Automations/flows: `on_unknown_reply` / `max_reprompts` / `on_timeout_hours` /
  `on_exhaust` on flows, `case_sensitive` on keyword triggers and `timezone`
  on `time_based` are accepted by the API but have no UI; the Ask-node
  `validation`/`regex` is accepted and ignored; `send_form` sends a text link
  on the web channel although types promise an inline card; form answers
  live at `form.<key>`, not `vars.form.<key>` as the types comment says;
  `flow-dispatch.service.ts` class comment still claims Instagram support.
- Google: the setup dialog's step 2 tells the merchant to add the Calendar
  service only; the served script's `authorizeOnce()` needs Calendar, People
  and Tasks, so setup fails at authorisation.
- Stores: `CodConfirmationService` builds a `ShopifyClient` unconditionally,
  so COD tagging and cancel-at-store cannot work on WooCommerce.
- `docs/invoices.md` still marks migrations 120/121 as not applied and calls
  the create dialog three-step in one place; the shipped UI is four steps.
- `store` appears as a contact source in the activity service but not in
  `ContactSource` / `CONTACT_SOURCE_META`, so it renders as Unknown.

## 8b. Log

- 2026-09-16 — Campaigns merged into Broadcasts in the product: the wizard's last step sends now, schedules once or repeats, and the Broadcasts page has History / Scheduled / Repeating / Drafts tabs. `whatsapp/campaigns` deleted and redirected to the new `whatsapp/scheduled-broadcasts`; broadcasts, troubleshooting, FAQ, overview, analytics, activity timeline, contacts, API keys and index updated. The CTWA page now says "tracked ad" rather than "campaign", matching the app. Nav regenerated.
- 2026-09-16 — Meta Ads Manager removed from the product. Dropped its out-of-scope entry (here and in `AGENTS.md`), its §8 finding and the **Facebook lead** contact source row; the CTWA page no longer points at Meta Ads Manager. Data-deletion source now `meta-data-deletion` and `/meta/privacy/*`. CTWA attribution pages unchanged. Nav untouched (no §4 row changed).
- 2026-09-15 — Verified with `mint dev`: pages and generated endpoint pages render; `.json`/`.yaml` files are NOT served as static assets (`.txt` and images are). The Postman page therefore links the raw GitHub URL (repo is public) and Postman imports it by link; `postman/` is in `.mintignore`.
- 2026-09-15 — Batch I reported: 5 pages. All 104 pages written; final lint/validate/links run; commit and push authorised by Siva.
- 2026-09-15 — Static `.json`/`.yaml` files are NOT served by the Mintlify dev server (`.txt`, images and `.svg` are). The Postman page therefore links the collection through the public GitHub repo's raw URL and offers Postman's **Import → Link**. `scripts/` moved into the repo; README rewritten.
- 2026-09-15 — Machine restarted mid batch I; only `troubleshooting/whatsapp.mdx` had landed. Writer resumed for the remaining four pages.
- 2026-09-15 — Batch E reported: 14 pages. All nine writing batches complete (99 pages + spec + Postman). Batch I launched.
- 2026-09-15 — Batch C reported: 14 pages.
- 2026-09-15 — Batches F and G reported: 13 + 13 pages.
- 2026-09-15 — `logo/light.svg` and `logo/dark.svg` replaced with the Watx wordmark (dark variant: white text, green mark); Mintlify placeholder `favicon.svg` removed; favicon stays on `images/watx-mark-*.png`.
- 2026-09-15 — Batch D2 reported: 10 pages.
- 2026-09-15 — Batches A and D1 reported. Postman collection generated (24 requests) and linked from the navbar via `/api/postman`.
- 2026-09-15 — Batch H reported: 4 pages + openapi.yaml.
- 2026-09-15 — Batch B reported: 12 pages written.
- 2026-09-15 — Wave 2 launched: batches D1, D2, E, G (Opus, parallel). Root `quickstart.mdx` removed.
- 2026-09-15 — Wave 1 launched: batches A, B, C, F, H (Opus, parallel).
- 2026-09-15 — Plan written. Repo was the untouched Mintlify starter
  (index, quickstart). Tooling decision: write files directly in this repo
  (parallel writers, git review, local validation); the Mintlify MCP is used
  only to inspect the deployment.
