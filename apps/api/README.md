# KnowMesh API
FastAPI application with `/api/v1` resource routes for bundles, claims, evidence, nodes, federation, reputation, evolution, bounties, subscriptions, simulations, experiments and challenges.

Run: `pip install -e '.[test]'` then `uvicorn knowmesh_api.main:app --reload` from this directory. Browse `/docs`; health is `/health`.

The generic record API is a functional scaffold, not a finalized domain contract. Its thread-safe store is process-local memory and loses data on restart. Replace it with SQLAlchemy-backed repositories before multi-process/production use. Search is substring matching, not BM25/semantic retrieval. Authentication, authorization, rate limiting, audit persistence, domain validation and durable pagination are not implemented.
