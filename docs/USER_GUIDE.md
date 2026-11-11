# KnowMesh User Guide

Welcome to the **KnowMesh Organization Console**. This guide explains how administrators, knowledge curators, and developers operate independent knowledge nodes, publish verifiable OKF bundles, manage claims and evidence, and synchronize knowledge across federated peers.

---

## 1. Getting Started & Demo Mode

1. Start the backend API (`http://localhost:8000`) and the Next.js console (`http://localhost:3000`).
2. Click **Bootstrap 3-Node Federation Demo** in the top bar (or on the **Overview** screen) to provision:
   - **Organization A** (`Node A` — Federated Research Node) with a published signed OKF knowledge bundle, atomic claims, and attached evidence.
   - **Organization B** (`Node B` — Partner Discovery Node) peered with Node A and authorized for federated discovery and synchronization.
   - **Organization C** (`Node C` — Independent Validator Node) operating with independent policy boundaries.
3. Alternatively, register a new user account via `POST /api/v1/auth/register` or sign in from the top header bar.

---

## 2. Navigation & Console Workspaces

### 2.1 Overview
- Displays live operational telemetry: registered organizations, active knowledge nodes, published OKF bundles, atomic claims, peer health, and recent audit events.
- Includes an interactive **Network Topology Graph** showing local nodes, federated peers, trust scores, and bundle counts.

### 2.2 Organizations & Access Control
- Create organizations (`POST /api/v1/organizations`) with unique slugs.
- View and add organization members with RBAC roles:
  - `owner`: Full administrative control over organization settings, nodes, members, and policies.
  - `admin`: Can register nodes, configure peers, manage agents, and publish knowledge.
  - `curator`: Can create/publish OKF bundles, evaluate claims, and attach evidence.
  - `developer`: Can register AI agents, rotate API keys, and test SDK queries.
  - `member`: Read-only access to organization bundles, search, and verification inspector.

### 2.3 My Nodes
- Register independent knowledge nodes (`POST /api/v1/nodes`).
- Each node automatically generates an **Ed25519 keypair** (`did:knowmesh:<slug>-<hash>`) upon registration.
- Configure node visibility:
  - `private`: Accessible only to owning organization and explicitly authorized agents.
  - `organization`: Accessible to all members and agents of the owning organization.
  - `federated`: Eligible published bundles can be discovered and retrieved by authorized external peers.
- Activate or deactivate nodes at any time.

### 2.4 Knowledge & Publishing Studio
- Browse published, draft, superseded, archived, or withdrawn knowledge bundles.
- **Publish New Bundle**:
  1. Select the publishing node, visibility (`private`, `organization`, `federated`), domain, and tags.
  2. Define one or more atomic claims (`empirical`, `theoretical`, `methodological`, `statistical`, `observational`, `normative`) with confidence scores (`0.0`–`1.0`).
  3. Attach traceable evidence records (`dataset`, `experiment`, `citation`, `computation`, `observation`, `expert_review`) linked to claim IDs.
  4. Click **Validate, Sign & Publish**. The node validates the OKF schema, computes the RFC 8785 JCS SHA-256 content digest, signs the canonical payload with its Ed25519 private key, records provenance, and emits a `bundle.published` event.
- **Create Revision (`v2`, `v3`, ...)**:
  - Select an existing bundle to publish an updated revision. KnowMesh preserves parent-child lineage (`previous_revision_id`, `previous_digest`), computes field-level diffs via `knowledge_dna`, and marks the prior revision as `superseded` without mutating it in place.

### 2.5 Claims & Evidence Inspector
- Inspect atomic claims across bundles along with their multi-dimensional quality rubric evaluation (`clarity`, `specificity`, `evidence_support`, `falsifiability`, `source_credibility`, `methodological_rigor`).
- Transition claim lifecycle states:
  `proposed` → `evidence_attached` → `under_review` → `supported` / `contested` / `inconclusive` / `rejected` → `superseded` / `archived`.

### 2.6 Discover (Local & Federated Search)
- Switch between `Local`, `Federated`, or `Hybrid` search scopes.
- Filter by domain, visibility, minimum confidence, or verification status.
- Inspect the **Federated Search Trace** Drawer to see per-node latency, result counts, and graceful degradation when any peer is unreachable.

### 2.7 Verification & Provenance Inspector
- Verify any bundle or revision on demand (`GET /api/v1/bundles/{bundle_id}/verify` or `POST /api/v1/verify`).
- Review distinct cryptographic and trust statuses:
  - `retrieved`: Bundle payload retrieved.
  - `digest_verified`: Canonical SHA-256 content digest matches the OKF payload.
  - `signature_verified`: Ed25519 signature over `${bundle_id}:${revision_number}:${content_digest}` is valid.
  - `signer_recognized`: Publishing node's public key is registered and recognized.
  - `provenance_available`: W3C PROV-inspired provenance chain is intact.
- Use the **Tamper Simulation** toggle in the Verification Inspector to alter a claim in memory and watch digest/signature verification immediately fail with `verification_failed`.

### 2.8 Federation & Peers
- Register remote peer endpoints (`POST /api/v1/federation/peers`) with SSRF validation.
- Trigger pull-based synchronization (`POST /api/v1/federation/peers/{peer_id}/sync`) to compare revision cursors, transfer new federated bundles, verify signatures prior to ingestion, and detect revision conflicts.

### 2.9 Agents & Developer Platform
- Register AI agents (`POST /api/v1/agents`) bound to an organization and optional node with granular permissions (`knowledge:read`, `knowledge:search`, `knowledge:publish`, `knowledge:update`, `federation:discover`, `federation:retrieve`, `verification:read`).
- Issue, rotate, or revoke API credentials (`km_live_...`). Copy the secret immediately upon creation—KnowMesh stores only its SHA-256 hash at rest and never returns the plaintext secret again.

