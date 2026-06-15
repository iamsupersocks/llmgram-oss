# Production Blueprint

LLMgram OSS is a demo. The production version should be treated as an **AI media intelligence operating layer**, not a static website.

## Target shape

```text
Collectors
  ├─ public social sources
  ├─ GitHub repositories / releases / PRs
  ├─ research papers
  ├─ product changelogs
  └─ manual trusted links
        │
        ▼
Queue + dedupe
  ├─ stable source IDs
  ├─ URL canonicalization
  ├─ duplicate clustering
  └─ retry / failure states
        │
        ▼
AI triage
  ├─ relevance classifier
  ├─ novelty score
  ├─ builder-value score
  ├─ safety/risk flags
  └─ structured summary
        │
        ▼
Editorial core
  ├─ human review
  ├─ ranking
  ├─ source-grounded takeaways
  └─ weekly synthesis
        │
        ▼
Publishing
  ├─ website
  ├─ JSON API / RSS
  ├─ weekly digest
  ├─ lab/company radars
  └─ knowledge base
```

## Database model

Recommended minimum tables:

```sql
sources(id, kind, name, url, refresh_interval, visibility, created_at, updated_at)
raw_items(id, source_id, canonical_url, raw_text, raw_json, raw_hash, captured_at)
signals(id, raw_item_id, title, summary, category, score, confidence, impact, status, created_at, updated_at)
signal_tags(signal_id, tag)
reviews(id, signal_id, reviewer_id, decision, notes, created_at)
weekly_issues(id, week, title, status, published_at)
weekly_items(issue_id, signal_id, rank, takeaway)
audit_events(id, actor_type, actor_id, action, entity_type, entity_id, payload_json, created_at)
```

## Agent workflow

Agents are useful for triage and drafting, but should not silently publish.

Recommended path:

```text
collector stores raw item
  → classifier proposes category + score
  → summarizer drafts builder-focused takeaway
  → deduper links related items
  → human editor approves/ranks
  → publisher builds API/RSS/site/weekly
```

For Mistral/open-weight deployments:

- use local/open models for cheap first-pass classification;
- keep a stronger model or human for ambiguous editorial judgment;
- log model name, prompt version and output hash;
- evaluate on a golden set before changing prompts/models.

## Scoring

Keep scoring interpretable:

```text
signal_score = weighted(
  novelty,
  builder_impact,
  source_quality,
  market_relevance,
  actionability,
  hype_penalty
)
```

Store component scores so a user can understand why an item ranked high.

## Source traceability

Every summary should map back to a source item:

```json
{
  "signal_id": "sig-workbench-agents",
  "source_id": "src-papers",
  "raw_item_id": "raw-2026-06-14-001",
  "claim": "Task completion rates improved but harmful actions remain a blocker",
  "extracted_by": "agent:mistral-large",
  "reviewed_by": "human:editor",
  "confidence": 0.81
}
```

## Publishing boundaries

Public outputs can include:

- titles;
- summaries;
- source URLs;
- scores and categories;
- weekly digests.

Private/internal outputs should include:

- credentials;
- private DMs;
- raw auth state;
- editorial drafts not approved;
- subscriber data;
- analytics secrets;
- bot deployment details.

## Deployment

Simple deployment:

```text
Caddy/nginx → Gunicorn/Flask → PostgreSQL → scheduled collectors → static site/API
```

More serious deployment:

```text
CDN
  → API gateway
  → LLMgram API service
  → Postgres + object storage
  → worker queue for collectors/triage
  → observability + alerting
```

## Product narrative

Position it as:

> An AI-native editorial intelligence stack: public sources go in, model-assisted triage and human review compress the firehose into a trustworthy signal feed.

The impressive part is the operating system:

- collectors;
- dedupe;
- provenance;
- scoring;
- human review;
- weekly synthesis;
- APIs/RSS/radars;
- knowledge-base handoff.
