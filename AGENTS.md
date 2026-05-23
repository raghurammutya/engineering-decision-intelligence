# Codex Instructions

This repository defines a reusable Engineering Decision Intelligence product.

## Product Direction

- Build toward continuous reconciliation of intended engineering policy and
  observed operational reality.
- Treat registries, dashboards, audit packs, and markdown reports as generated
  materialized views, not authoritative truth.
- Keep the initial ontology small and operationally useful.
- Prefer deterministic, evidence-backed policy for enforcement.
- Use AI initially for summarization, clustering, explanation, and review
  assistance, not opaque safety decisions.

## Self-Governance Rule

Every capability this platform applies to other systems should eventually apply
to itself:

- scanners must be discoverable,
- policies must be versioned,
- generated views must declare inputs,
- risk decisions must cite evidence,
- automation that mutates state must be classified and owner-reviewed.

## First Pilot

The ML system is the first pilot/customer system. Product logic belongs here;
ML-specific generated findings and evidence belong in the ML repository unless
explicitly being converted into reusable product examples.
