# Architecture

LLMgram OSS demonstrates a source-to-signal architecture: collect public AI inputs, score them, keep provenance, let humans review the ranking, then publish a compressed feed.

![LLMgram architecture](assets/llmgram-architecture.svg)

## Core loop

```text
sources → collectors → AI triage → editorial ranking → public outputs
```

## Layers

### 1. Source ingest

Inputs can include:

- public social posts;
- GitHub repositories, releases and PRs;
- research papers;
- product changelogs;
- manual links from trusted curators.

### 2. Triage

Model-assisted triage should produce structured fields:

- category;
- novelty;
- builder value;
- impact;
- risk/safety flag;
- confidence;
- source provenance.

### 3. Editorial core

Humans review and rank the signal:

- reject hype;
- merge duplicates;
- preserve source links;
- write a concise takeaway;
- decide whether the item belongs in weekly, API feed, radar or archive.

### 4. Publishing

Outputs:

- website;
- JSON API;
- RSS/newsletter;
- weekly digest;
- company/lab radars;
- downstream knowledge base.

## Demo implementation

The public repo uses:

```text
sample_data/signals.json
sample_data/weekly.json
sample_data/sources.json
```

Production deployments should replace these files with a database + collector/queue pipeline while preserving the API contract in `openapi.yaml`.
