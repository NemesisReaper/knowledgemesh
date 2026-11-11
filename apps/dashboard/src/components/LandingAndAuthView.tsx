"use client";

import React, { useEffect, useState } from "react";
import { API_BASE_URL, OverviewResponse, apiRequest } from "../lib/api";
import { KnowledgeTransformationScene } from "./hero/KnowledgeTransformationScene";

export interface AuthenticatedPrincipal {
  actor_id?: string;
  email: string;
  full_name: string;
  role: string;
  organization_id?: string | null;
  organization_name: string;
}

/* ============================================================================
   STAGE 1: FULLY ANIMATED PRODUCT & ARCHITECTURE LANDING PAGE (100% DYNAMIC)
   ============================================================================ */
export function LandingPageView({
  onGoToLogin,
  onGoToRegister,
}: {
  onGoToLogin: () => void;
  onGoToRegister: () => void;
}) {
  const [activeArchStep, setActiveArchStep] = useState<number>(0);
  const [heroMode, setHeroMode] = useState<"scene" | "topology">("scene");
  const [overview, setOverview] = useState<OverviewResponse | null>(null);
  const [health, setHealth] = useState<Record<string, unknown> | null>(null);
  const [manifest, setManifest] = useState<Record<string, unknown> | null>(
    null
  );

  useEffect(() => {
    apiRequest<OverviewResponse>("/api/v1/overview")
      .then(setOverview)
      .catch(() => {});
    apiRequest<Record<string, unknown>>("/health")
      .then(setHealth)
      .catch(() => {});
    apiRequest<Record<string, unknown>>("/api/v1/federation/protocol/manifest")
      .then(setManifest)
      .catch(() => {});
  }, []);

  const liveNodes = overview?.topology?.nodes || [];
  const liveEdges = overview?.topology?.edges || [];
  const metrics = overview?.metrics;

  const archSteps = [
    {
      step: "01",
      title: "Sovereign Knowledge Nodes & Ed25519 Identity",
      tag: "INDEPENDENT NODES",
      desc: "Every organization operates its own sovereign KnowMesh node with an Ed25519 cryptographic keypair (did:knowmesh:<node-id>). Nodes enforce strict Private, Organization, or Federated visibility boundaries — private data is never exposed to public indexes or unauthorized peers.",
      endpoint: "GET /api/v1/nodes",
      liveSample:
        liveNodes.length > 0
          ? JSON.stringify(liveNodes[0], null, 2)
          : `GET ${API_BASE_URL}/api/v1/nodes\n// Connect or register a node in the console to inspect live Ed25519 identity`,
    },
    {
      step: "02",
      title: "Open Knowledge Format (OKF) Bundles, Claims & Evidence",
      tag: "INTEROPERABLE KNOWLEDGE",
      desc: "Knowledge is structured as versioned OKF bundles containing atomic claims and traceable evidence URIs. Each claim follows a 7-stage epistemic review lifecycle (proposed → evidence_attached → under_review → supported / contested / inconclusive / rejected).",
      endpoint: "POST /api/v1/bundles",
      liveSample: JSON.stringify(
        {
          endpoint: `${API_BASE_URL}/api/v1/bundles`,
          active_bundles_on_node: metrics?.knowledge_bundles ?? 0,
          published_claims_on_node: metrics?.published_claims ?? 0,
          claim_review_distribution:
            overview?.claim_review_distribution || {},
        },
        null,
        2
      ),
    },
    {
      step: "03",
      title: "RFC 8785 JCS Canonical Digests & Ed25519 Signing",
      tag: "VERIFIABLE EXCHANGE",
      desc: "When publishing a bundle, KnowMesh serializes the canonical OKF payload using RFC 8785 JSON Canonicalization Scheme (JCS), computes a deterministic SHA-256 content digest, signs the envelope with the node's Ed25519 private key, and appends a W3C PROV hash-chained provenance event.",
      endpoint: "GET /api/v1/federation/protocol/manifest",
      liveSample: manifest
        ? JSON.stringify(manifest, null, 2)
        : `GET ${API_BASE_URL}/api/v1/federation/protocol/manifest`,
    },
    {
      step: "04",
      title: "Federated BM25 Discovery, Pull-Sync & Knowledge DNA",
      tag: "ZERO-TRUST FEDERATION",
      desc: "Authorized AI agents and partner nodes discover knowledge across the mesh via federated BM25 search and pull-based synchronization. Every pulled revision is cryptographically verified prior to ingestion, while Knowledge DNA preserves immutable revision history and parent-child diffs.",
      endpoint: "POST /api/v1/search",
      liveSample: `from packages.sdk import KnowMeshClient, verify_bundle_signature

client = KnowMeshClient(base_url="${API_BASE_URL}", api_key="<YOUR_ISSUED_AGENT_KEY>")
hits = client.search(query="*", scope="federated")
for item in hits["results"]:
    bundle = client.get_bundle(item["bundle_id"])
    assert verify_bundle_signature(bundle).is_valid`,
    },
  ];

  // Compute dynamic SVG node coordinates from live topology
  const cx = 280;
  const cy = 165;
  const nodeCoords: Record<string, { x: number; y: number }> = {};
  liveNodes.forEach((n, idx) => {
    if (idx === 0 || n.type === "local_node") {
      nodeCoords[n.id] = { x: cx, y: cy };
    } else {
      const peerTotal = Math.max(1, liveNodes.length - 1);
      const angle = ((idx - 1) / peerTotal) * Math.PI * 2 - Math.PI / 4;
      nodeCoords[n.id] = {
        x: Math.round(cx + Math.cos(angle) * 160),
        y: Math.round(cy + Math.sin(angle) * 95),
      };
    }
  });

  return (
    <div className="km-landing-root">
      <div className="km-aurora-orb-1" />
      <div className="km-aurora-orb-2" />

      {/* Top Sticky Navigation */}
      <header className="km-landing-nav">
        <div className="km-brand-logo">
          <span className="km-brand-glyph">KM</span>
          <div>
            know<span>mesh</span>
          </div>
          <span className="km-badge info" style={{ marginLeft: 8 }}>
            {String(manifest?.protocol || "knowmesh-fed/1.0")}
          </span>
        </div>

        <nav className="km-landing-nav-links">
          <a href="#mission">Product Mission</a>
          <a href="#architecture">How It Works</a>
          <a href="#comparison">Why KnowMesh</a>
          <a href="#cryptography">Zero-Trust Auth</a>
        </nav>

        <div style={{ display: "flex", gap: 10 }}>
          <button
            type="button"
            className="km-btn"
            onClick={onGoToRegister}
          >
            Create Organization Account
          </button>
          <button
            type="button"
            className="km-btn km-btn-primary"
            onClick={onGoToLogin}
          >
            🔐 Sign In to Console →
          </button>
        </div>
      </header>

      {/* Hero Section with Live Animated Federated Mesh */}
      <section className="km-hero-section">
        <div>
          <div className="km-hero-pill">
            <span>●</span> OPEN KNOWLEDGE INFRASTRUCTURE
          </div>
          <h1 className="km-hero-title">
            From fragmented knowledge to a connected world.
          </h1>
          <p className="km-hero-lead">
            A common foundation for structuring, sharing, and reusing knowledge across independent AI systems. <strong>KnowMesh</strong> allows organizations to maintain independent knowledge nodes while authorizing AI agents to exchange cryptographically verifiable <strong>Open Knowledge Format (OKF)</strong> bundles, verify <strong>Ed25519 signatures</strong> and <strong>RFC 8785 canonical digests</strong>, and track immutable <strong>Knowledge DNA</strong> lineage.
          </p>

          <div className="km-hero-cta-row">
            <button
              type="button"
              className="km-btn km-btn-primary km-btn-lg"
              onClick={onGoToRegister}
            >
              Explore OKF →
            </button>
            <a
              href={`${API_BASE_URL}/docs`}
              target="_blank"
              rel="noreferrer"
              className="km-btn km-btn-accent km-btn-lg"
              style={{ textDecoration: "none" }}
            >
              Read Documentation ↗
            </a>
            <button
              type="button"
              className="km-btn km-btn-lg"
              onClick={onGoToLogin}
            >
              🔐 Console Sign In
            </button>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: 14,
              paddingTop: 18,
              borderTop: "1px solid var(--border-subtle)",
            }}
          >
            <div>
              <div
                style={{
                  fontSize: 22,
                  fontWeight: 800,
                  color: "var(--accent-primary)",
                }}
              >
                {metrics?.total_nodes ?? 0}
              </div>
              <div className="km-metric-sub">Live Sovereign Nodes</div>
            </div>
            <div>
              <div
                style={{
                  fontSize: 22,
                  fontWeight: 800,
                  color: "var(--status-verified)",
                }}
              >
                {metrics?.knowledge_bundles ?? 0}
              </div>
              <div className="km-metric-sub">Signed OKF Bundles</div>
            </div>
            <div>
              <div
                style={{
                  fontSize: 22,
                  fontWeight: 800,
                  color: "var(--accent-cyan)",
                }}
              >
                {metrics?.published_claims ?? 0}
              </div>
              <div className="km-metric-sub">Atomic Claims Indexed</div>
            </div>
            <div>
              <div
                style={{
                  fontSize: 22,
                  fontWeight: 800,
                  color: "var(--accent-violet)",
                }}
              >
                {metrics?.registered_agents ?? 0}
              </div>
              <div className="km-metric-sub">Scoped AI Agents</div>
            </div>
          </div>
        </div>

        {/* Photorealistic 3D Transformation Machine Viewport (Unboxed, Borderless, Cinematic) */}
        <div className="km-hero-3d-viewport">
          <KnowledgeTransformationScene
            onExploreOkf={onGoToRegister}
            onReadDocs={onGoToLogin}
          />
        </div>
      </section>

      {/* Scrolling Cryptographic Telemetry Marquee */}
      <div className="km-marquee-bar">
        <div className="km-marquee-track">
          <span>
            <strong>◆ RFC 8032 Ed25519</strong> Node Keypairs & Envelope Signing
          </span>
          <span>
            <strong>◆ RFC 8785 JCS</strong> Deterministic Canonical JSON SHA-256 Digests
          </span>
          <span>
            <strong>◆ OKF v0.2</strong> Open Knowledge Format Bundles, Claims & Evidence
          </span>
          <span>
            <strong>◆ W3C PROV</strong> Hash-Chained Cryptographic Provenance
          </span>
          <span>
            <strong>◆ Epistemic Separation</strong> Valid Signature ≠ Absolute Factual Truth
          </span>
          <span>
            <strong>◆ Pull-Based Sync</strong> Conflict-Preserving Multi-Node Federation
          </span>
          <span>
            <strong>◆ Zero-Trust SDK</strong> Client-Side Digest & Signature Verification
          </span>
          <span>
            <strong>◆ RFC 8032 Ed25519</strong> Node Keypairs & Envelope Signing
          </span>
        </div>
      </div>

      {/* Section 1: Product Mission & Core Capabilities */}
      <section id="mission" className="km-landing-section">
        <div className="km-section-eyebrow">1 · PRODUCT DEFINITION & PILLARS</div>
        <h2 className="km-section-heading">
          Built for Sovereign Organizations and Verifiable AI Agents
        </h2>
        <p className="km-section-desc">
          Organizations need to collaborate and expose structured knowledge to AI agents without dumping proprietary datasets into one centralized vector database or trusting unverified text chunks.
        </p>

        <div className="km-grid-3">
          <div className="km-feature-card">
            <div className="km-feature-icon">⬡</div>
            <h3 style={{ margin: "0 0 8px", fontSize: 18 }}>
              Independent Sovereign Nodes
            </h3>
            <p className="km-metric-sub" style={{ lineHeight: 1.6 }}>
              Every participating organization operates its own node with an Ed25519 keypair, capability advertisement, health probes, and granular visibility policies (<code>private</code>, <code>organization</code>, <code>federated</code>).
            </p>
          </div>

          <div className="km-feature-card">
            <div className="km-feature-icon">❖</div>
            <h3 style={{ margin: "0 0 8px", fontSize: 18 }}>
              Structured OKF Knowledge & Claims
            </h3>
            <p className="km-metric-sub" style={{ lineHeight: 1.6 }}>
              Publish structured Open Knowledge Format (OKF) bundles composed of atomic claims, 6-dimension epistemic quality rubrics, and traceable supporting or contradictory evidence URIs.
            </p>
          </div>

          <div className="km-feature-card">
            <div className="km-feature-icon">🛡</div>
            <h3 style={{ margin: "0 0 8px", fontSize: 18 }}>
              Zero-Trust Cryptographic Verification
            </h3>
            <p className="km-metric-sub" style={{ lineHeight: 1.6 }}>
              Every bundle revision is hashed via RFC 8785 JCS and signed with Ed25519. Consumers distinguish retrieval success, digest integrity, signature validity, signer recognition, and epistemic status.
            </p>
          </div>

          <div className="km-feature-card">
            <div className="km-feature-icon">⇄</div>
            <h3 style={{ margin: "0 0 8px", fontSize: 18 }}>
              Federated Discovery & Pull-Sync
            </h3>
            <p className="km-metric-sub" style={{ lineHeight: 1.6 }}>
              Query across local BM25 indexes and authorized external peers with circuit-breaking resilience. Pull-based synchronization detects updates and preserves conflicting revisions without silent overwrites.
            </p>
          </div>

          <div className="km-feature-card">
            <div className="km-feature-icon">🧬</div>
            <h3 style={{ margin: "0 0 8px", fontSize: 18 }}>
              Knowledge DNA & Immutable Lineage
            </h3>
            <p className="km-metric-sub" style={{ lineHeight: 1.6 }}>
              Published revisions are never mutated in place. Updates mint new immutable revisions (<code>v1.0.0 → v2.0.0</code>), preserve parent-child lineage, and compute field-level diffs.
            </p>
          </div>

          <div className="km-feature-card">
            <div className="km-feature-icon">🤖</div>
            <h3 style={{ margin: "0 0 8px", fontSize: 18 }}>
              Scoped AI Agents & Python SDK
            </h3>
            <p className="km-metric-sub" style={{ lineHeight: 1.6 }}>
              Register AI agents with least-privilege scopes (<code>knowledge:read</code>, <code>knowledge:publish</code>, <code>federation:discover</code>) and one-time SHA-256 hashed API keys (<code>km_live_...</code>).
            </p>
          </div>
        </div>
      </section>

      {/* Section 2: Interactive 4-Step Architecture Walkthrough */}
      <section
        id="architecture"
        className="km-landing-section"
        style={{ paddingTop: 20 }}
      >
        <div className="km-section-eyebrow">
          2 · INTERACTIVE ARCHITECTURE WALKTHROUGH
        </div>
        <h2 className="km-section-heading">
          End-to-End Federated Knowledge Lifecycle
        </h2>
        <p className="km-section-desc">
          Click each protocol stage below to inspect the live backend wire contracts and cryptographic guarantees powering KnowMesh.
        </p>

        <div className="km-grid-asym">
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {archSteps.map((item, idx) => (
              <div
                key={item.step}
                className="km-card km-card-interactive"
                style={{
                  borderColor:
                    activeArchStep === idx
                      ? "var(--accent-primary)"
                      : undefined,
                  background:
                    activeArchStep === idx
                      ? "rgba(101, 153, 255, 0.1)"
                      : undefined,
                }}
                onClick={() => setActiveArchStep(idx)}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: 6,
                  }}
                >
                  <span className="km-mono">STEP {item.step}</span>
                  <span className="km-badge info">{item.tag}</span>
                </div>
                <h3 style={{ margin: "0 0 6px", fontSize: 17 }}>
                  {item.title}
                </h3>
                <p className="km-metric-sub" style={{ margin: 0 }}>
                  {item.desc}
                </p>
              </div>
            ))}
          </div>

          <div
            className="km-card"
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div className="km-card-header">
                <span className="km-badge verified">
                  Live Endpoint · {archSteps[activeArchStep].endpoint}
                </span>
                <span className="km-mono">
                  {String(manifest?.protocol || "knowmesh-fed/1.0")}
                </span>
              </div>
              <h3 style={{ marginTop: 0 }}>
                {archSteps[activeArchStep].title}
              </h3>
              <p className="km-metric-sub">
                {archSteps[activeArchStep].desc}
              </p>
              <pre className="km-code-block" style={{ minHeight: 210 }}>
                {archSteps[activeArchStep].liveSample}
              </pre>
            </div>
            <div
              style={{
                display: "flex",
                justifyContent: "flex-end",
                marginTop: 14,
              }}
            >
              <button
                type="button"
                className="km-btn km-btn-primary"
                onClick={onGoToLogin}
              >
                Authenticate to Access Console →
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: What KnowMesh IS vs What KnowMesh IS NOT */}
      <section
        id="comparison"
        className="km-landing-section"
        style={{ paddingTop: 20 }}
      >
        <div className="km-section-eyebrow">3 · ARCHITECTURAL BOUNDARIES</div>
        <h2 className="km-section-heading">
          What KnowMesh Is — And What It Is Not
        </h2>

        <div className="km-grid-2">
          <div
            className="km-card"
            style={{ borderColor: "var(--status-verified-border)" }}
          >
            <div className="km-card-header">
              <h3
                className="km-card-title"
                style={{ color: "var(--status-verified)" }}
              >
                ✓ What KnowMesh IS
              </h3>
              <span className="km-badge verified">Sovereign Mesh</span>
            </div>
            <ul
              style={{
                margin: 0,
                paddingLeft: 18,
                display: "flex",
                flexDirection: "column",
                gap: 10,
                color: "var(--text-secondary)",
              }}
            >
              <li>
                <strong>Independent Organization Nodes:</strong> Each node controls its own database, Ed25519 keys, and publication policies.
              </li>
              <li>
                <strong>Structured OKF Knowledge Bundles:</strong> Atomic claims with 7-stage epistemic review states and traceable evidence URIs.
              </li>
              <li>
                <strong>Cryptographic Provenance & Integrity:</strong> Deterministic RFC 8785 JCS SHA-256 digests and Ed25519 signatures.
              </li>
              <li>
                <strong>Federated BM25 Discovery & Pull-Sync:</strong> Cross-node search and conflict-preserving pull synchronization over HTTP.
              </li>
            </ul>
          </div>

          <div
            className="km-card"
            style={{ borderColor: "var(--status-error-border)" }}
          >
            <div className="km-card-header">
              <h3
                className="km-card-title"
                style={{ color: "var(--status-error)" }}
              >
                ✕ What KnowMesh Is NOT
              </h3>
              <span className="km-badge error">Non-Goals</span>
            </div>
            <ul
              style={{
                margin: 0,
                paddingLeft: 18,
                display: "flex",
                flexDirection: "column",
                gap: 10,
                color: "var(--text-secondary)",
              }}
            >
              <li>
                <strong>NOT a Centralized Vector Database:</strong> No single shared database accessible to every organization.
              </li>
              <li>
                <strong>NOT an AI Chatbot or Unverified RAG Dump:</strong> Every claim is structured, versioned, and bound to traceable evidence.
              </li>
              <li>
                <strong>NOT a Blockchain or Token Scheme:</strong> Uses standard HTTP/JSON, RFC 8032 Ed25519, and RFC 8785 JCS without consensus bloat.
              </li>
              <li>
                <strong>NOT Equating Signatures with Truth:</strong> A valid signature proves who published a bundle and its integrity — not absolute factual correctness.
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom CTA Banner */}
        <div
          className="km-card"
          id="cryptography"
          style={{
            marginTop: 28,
            textAlign: "center",
            padding: "40px 28px",
            background:
              "linear-gradient(135deg, rgba(18, 30, 56, 0.96) 0%, rgba(12, 22, 40, 0.98) 100%)",
            borderColor: "var(--accent-primary)",
          }}
        >
          <h2 style={{ margin: "0 0 10px", fontSize: 28 }}>
            Ready to Operate Your Sovereign Knowledge Node?
          </h2>
          <p
            className="km-metric-sub"
            style={{ maxWidth: 620, margin: "0 auto 24px", fontSize: 15 }}
          >
            Register an organization or sign in with your verified credentials to access the Federation Control Plane, publish signed OKF bundles, and run zero-trust tamper verification.
          </p>
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              gap: 14,
              flexWrap: "wrap",
            }}
          >
            <button
              type="button"
              className="km-btn km-btn-primary km-btn-lg"
              onClick={onGoToLogin}
            >
              🔐 Sign In with Credentials →
            </button>
            <button
              type="button"
              className="km-btn km-btn-accent km-btn-lg"
              onClick={onGoToRegister}
            >
              + Register New Organization Account
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}

/* ============================================================================
   STAGE 2: STRICT BACKEND AUTHENTICATION & CREDENTIAL VERIFICATION GATE
   (Zero hardcoded accounts or passwords; verifies strictly against /api/v1/auth/*)
   ============================================================================ */
export function LoginGateView({
  initialMode = "login",
  onAuthenticated,
  onBackToLanding,
}: {
  initialMode?: "login" | "register";
  onAuthenticated: (user: AuthenticatedPrincipal) => void;
  onBackToLanding: () => void;
}) {
  const [mode, setMode] = useState<"login" | "register">(initialMode);
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [fullName, setFullName] = useState<string>("");
  const [orgName, setOrgName] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);

    const cleanEmail = email.trim().toLowerCase();

    try {
      if (mode === "register") {
        if (password.length < 8) {
          setErrorMsg("Password must be at least 8 characters long.");
          setLoading(false);
          return;
        }
        const res = await apiRequest<{
          access_token: string;
          refresh_token: string;
          user: { id: string; email: string; full_name: string; role?: string };
          organization?: { id: string; name: string } | null;
        }>("/api/v1/auth/register", {
          method: "POST",
          body: JSON.stringify({
            email: cleanEmail,
            password,
            full_name: fullName.trim(),
            organization_name: orgName.trim() || undefined,
          }),
        });

        if (typeof window !== "undefined") {
          window.localStorage.setItem("km_access_token", res.access_token);
          window.localStorage.setItem("km_refresh_token", res.refresh_token);
          if (res.organization?.id) {
            window.localStorage.setItem("km_org_id", res.organization.id);
          }
        }

        onAuthenticated({
          actor_id: res.user.id,
          email: res.user.email,
          full_name: res.user.full_name,
          role: res.user.role || "owner",
          organization_id: res.organization?.id || null,
          organization_name: res.organization?.name || orgName.trim() || "Personal Workspace",
        });
        return;
      }

      // Sign-In Mode: Strictly verified against POST /api/v1/auth/login
      const res = await apiRequest<{
        access_token: string;
        refresh_token: string;
        user: { id: string; email: string; full_name: string; role?: string };
        organizations?: Array<{ id: string; name: string; role?: string }>;
      }>("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify({ email: cleanEmail, password }),
      });

      if (typeof window !== "undefined") {
        window.localStorage.setItem("km_access_token", res.access_token);
        window.localStorage.setItem("km_refresh_token", res.refresh_token);
        if (res.organizations?.[0]?.id) {
          window.localStorage.setItem("km_org_id", res.organizations[0].id);
        }
      }

      const primaryOrg = res.organizations?.[0];
      onAuthenticated({
        actor_id: res.user.id,
        email: res.user.email,
        full_name: res.user.full_name,
        role: primaryOrg?.role || res.user.role || "owner",
        organization_id: primaryOrg?.id || null,
        organization_name: primaryOrg?.name || "Authenticated Organization",
      });
    } catch (err) {
      const detail = err instanceof Error ? err.message : "Authentication failed";
      setErrorMsg(
        `✕ ${detail}. Please verify your credentials or switch to Register Account to create a new organization principal.`
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleDemoBypass() {
    setErrorMsg(null);
    setLoading(true);
    try {
      const res = await apiRequest<{
        access_token: string;
        refresh_token: string;
        user: { id: string; email: string; full_name: string; role?: string };
        organizations?: Array<{ id: string; name: string; role?: string }>;
        organization?: { id: string; name: string; role?: string };
      }>("/api/v1/auth/demo-bypass", {
        method: "POST",
      });

      if (typeof window !== "undefined") {
        window.localStorage.setItem("km_access_token", res.access_token);
        window.localStorage.setItem("km_refresh_token", res.refresh_token);
        const orgId = res.organizations?.[0]?.id || res.organization?.id;
        if (orgId) {
          window.localStorage.setItem("km_org_id", orgId);
        }
      }

      const primaryOrg = res.organizations?.[0] || res.organization;
      onAuthenticated({
        actor_id: res.user.id,
        email: res.user.email,
        full_name: res.user.full_name,
        role: primaryOrg?.role || res.user.role || "owner",
        organization_id: primaryOrg?.id || null,
        organization_name: primaryOrg?.name || "Sovereign AI Safety Mesh",
      });
    } catch (err) {
      const detail = err instanceof Error ? err.message : "Demo bypass failed";
      setErrorMsg(`✕ ${detail}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="km-landing-root">
      <div className="km-aurora-orb-1" />
      <div className="km-aurora-orb-2" />

      <div className="km-auth-gate-wrap">
        <div style={{ marginBottom: 18 }}>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={onBackToLanding}
          >
            ← Back to Product Overview
          </button>
        </div>

        <div className="km-auth-card">
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              marginBottom: 16,
            }}
          >
            <div className="km-brand-logo">
              <span className="km-brand-glyph">KM</span>
              <div>
                know<span>mesh</span>
              </div>
            </div>
            <span className="km-badge verified">Sovereign Mesh Identity</span>
          </div>

          <h2 style={{ margin: "0 0 6px", fontSize: 22 }}>
            {mode === "login"
              ? "Sign In to Sovereign Control Plane"
              : "Register Organization & Node Admin"}
          </h2>
          <p className="km-metric-sub" style={{ marginBottom: 18 }}>
            {mode === "login"
              ? "Authenticate against the backend identity database (/api/v1/auth/login) to access the Console Dashboard."
              : "Create a new user principal and sovereign organization boundary (/api/v1/auth/register)."}
          </p>

          {/* Instant Demo Bypass Box */}
          <div
            style={{
              background: "rgba(2, 132, 199, 0.14)",
              border: "1px solid rgba(56, 189, 248, 0.45)",
              borderRadius: 10,
              padding: 14,
              marginBottom: 18,
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: 12,
            }}
          >
            <div>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#38bdf8" }}>
                Quick Testing &amp; Evaluation
              </div>
              <div style={{ fontSize: 11.5, color: "#94a3b8" }}>
                Bypass manual credentials and access the full live dashboard instantly.
              </div>
            </div>
            <button
              type="button"
              className="km-btn km-btn-primary"
              onClick={handleDemoBypass}
              style={{
                whiteSpace: "nowrap",
                background: "linear-gradient(135deg, #0284c7 0%, #38bdf8 100%)",
                color: "#070b14",
                fontWeight: 700,
              }}
            >
              🚀 Demo Bypass →
            </button>
          </div>

          {errorMsg && (
            <div className="km-notice error" style={{ marginBottom: 16 }}>
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="km-field">
              <label className="km-label">Organization Email *</label>
              <input
                className="km-input"
                type="email"
                required
                placeholder="you@organization.org"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="km-field">
              <label className="km-label">
                Password {mode === "register" ? "(min 8 characters)" : ""} *
              </label>
              <input
                className="km-input"
                type="password"
                required
                minLength={mode === "register" ? 8 : 1}
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            {mode === "register" && (
              <>
                <div className="km-field">
                  <label className="km-label">Full Name *</label>
                  <input
                    className="km-input"
                    required
                    placeholder="e.g., Dr. Elena Vance"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                  />
                </div>
                <div className="km-field">
                  <label className="km-label">Organization Name *</label>
                  <input
                    className="km-input"
                    required
                    placeholder="e.g., Sovereign AI Research Lab"
                    value={orgName}
                    onChange={(e) => setOrgName(e.target.value)}
                  />
                </div>
              </>
            )}

            <button
              type="submit"
              className="km-btn km-btn-primary km-btn-lg"
              style={{ width: "100%", marginTop: 6 }}
              disabled={loading}
            >
              {loading
                ? "Verifying with Backend…"
                : mode === "login"
                ? "🔓 Authenticate & Open Dashboard →"
                : "Create Account & Open Dashboard →"}
            </button>
          </form>

          <div
            style={{
              marginTop: 16,
              paddingTop: 14,
              borderTop: "1px solid var(--border-subtle)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              fontSize: 12.5,
            }}
          >
            <span style={{ color: "var(--text-secondary)" }}>
              {mode === "login"
                ? "First time on this node?"
                : "Already registered an account?"}
            </span>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => {
                setMode((m) => (m === "login" ? "register" : "login"));
                setErrorMsg(null);
              }}
            >
              {mode === "login" ? "Register Account" : "Switch to Sign In"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
