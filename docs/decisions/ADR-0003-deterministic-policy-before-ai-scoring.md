# ADR-0003: Deterministic Policy Before AI Scoring

## Status

Accepted

## Context

AI can help classify, cluster, summarize, and explain engineering systems.
However, opaque AI scoring is not appropriate for production safety,
governance enforcement, deletion recommendations, or high-risk operational
decisions.

## Decision

The product will use deterministic, explainable, evidence-backed policy before
AI-assisted scoring for enforcement and safety decisions.

AI may be used initially for:

- semantic grouping,
- duplicate suggestions,
- explanation,
- summarization,
- review assistance.

## Consequences

- Safety findings must cite evidence.
- High-risk actions require deterministic rule support.
- AI recommendations remain advisory until promoted through evidence-backed
  policy.
