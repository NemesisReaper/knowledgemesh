"use client";

import React, { useCallback, useEffect, useMemo, useState } from "react";
import {
  API_BASE_URL,
  AgentItem,
  AuditEventItem,
  BundleItem,
  CredentialItem,
  NodeItem,
  OverviewResponse,
  PeerItem,
  apiRequest,
} from "../lib/api";
import {
  AuthenticatedPrincipal,
  LandingPageView,
  LoginGateView,
} from "../components/LandingAndAuthView";
import {
  CopySnippet,
  DiscoverView,
  KnowledgeView,
  NodesView,
  OverviewView,
} from "../components/ConsoleViews";
import {
  AgentsView,
  AuditLogsView,
  DeveloperPortalView,
  FederationView,
  SettingsView,
  TrustSecurityView,
} from "../components/OperationsViews";
import {
  BountyRecord,
  ClaimsRubricView,
  ReputationBountiesView,
} from "../components/ResearchViews";
import { OKFGraphWorkspace } from "../components/OKFGraphWorkspace";

export default function KnowMeshConsolePage() {
  const [stage, setStage] = useState<"landing" | "login" | "dashboard">(
    "landing"
  );
  const [authInitialMode, setAuthInitialMode] = useState<"login" | "register">(
    "login"
  );
  const [currentUser, setCurrentUser] =
    useState<AuthenticatedPrincipal | null>(null);

  const [activeTab, setActiveTab] = useState<string>("overview");
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(false);
  const [showCommandPalette, setShowCommandPalette] = useState<boolean>(false);
  const [commandQuery, setCommandQuery] = useState<string>("");
  const [topBanner, setTopBanner] = useState<string | null>(null);

  // 100% Dynamic Backend State (Zero hardcoded arrays)
  const [apiConnected, setApiConnected] = useState<boolean>(false);
  const [nodes, setNodes] = useState<NodeItem[]>([]);
  const [bundles, setBundles] = useState<BundleItem[]>([]);
  const [agents, setAgents] = useState<AgentItem[]>([]);
  const [credentials, setCredentials] = useState<CredentialItem[]>([]);
  const [peers, setPeers] = useState<PeerItem[]>([]);
  const [auditEvents, setAuditEvents] = useState<AuditEventItem[]>([]);
  const [bountiesCount, setBountiesCount] = useState<number>(0);
  const [liveOverview, setLiveOverview] = useState<OverviewResponse | null>(
    null
  );
  const [drawerBundle, setDrawerBundle] = useState<BundleItem | null>(null);

  // Check if user already has a valid backend JWT session on mount
  useEffect(() => {
    const token =
      typeof window !== "undefined"
        ? window.localStorage.getItem("km_access_token")
        : null;
    if (!token) return;

    apiRequest<{
      actor_id: string;
      role: string;
      organization_id: string | null;
      organizations: Array<{ id: string; name: string }>;
    }>("/api/v1/auth/me")
      .then((me) => {
        if (me && me.actor_id && me.actor_id !== "anonymous") {
          setCurrentUser({
            actor_id: me.actor_id,
            email: me.actor_id,
            full_name: me.actor_id,
            role: me.role || "member",
            organization_id: me.organization_id,
            organization_name:
              me.organizations?.[0]?.name || "Authenticated Organization",
          });
          setStage("dashboard");
        }
      })
      .catch(() => {
        if (typeof window !== "undefined") {
          window.localStorage.removeItem("km_access_token");
        }
      });
  }, []);

  const loadConsoleState = useCallback(async () => {
    try {
      const [ov, nd, bd, ag, cr, pr, au, bnt] = await Promise.all([
        apiRequest<OverviewResponse>("/api/v1/overview"),
        apiRequest<{ items: NodeItem[] }>("/api/v1/nodes"),
        apiRequest<{ items: BundleItem[] }>("/api/v1/bundles"),
        apiRequest<{ items: AgentItem[] }>("/api/v1/agents"),
        apiRequest<{ items: CredentialItem[] }>("/api/v1/credentials"),
        apiRequest<{ items: PeerItem[] }>("/api/v1/federation/peers"),
        apiRequest<{ items: AuditEventItem[] }>("/api/v1/audit"),
        apiRequest<{ items: BountyRecord[] }>("/api/v1/bounties"),
      ]);
      setLiveOverview(ov);
      setNodes(nd.items || []);
      setBundles(bd.items || []);
      setAgents(ag.items || []);
      setCredentials(cr.items || []);
      setPeers(pr.items || []);
      setAuditEvents(au.items || []);
      setBountiesCount((bnt.items || []).length);
      setApiConnected(true);
    } catch {
      setApiConnected(false);
    }
  }, []);

  useEffect(() => {
    if (stage === "dashboard") {
      loadConsoleState();
    }
  }, [stage, loadConsoleState]);

  // Keyboard shortcut Ctrl+K / Cmd+K for Command Palette
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setShowCommandPalette((s) => !s);
      } else if (e.key === "Escape") {
        setShowCommandPalette(false);
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  async function handleBootstrapDemo() {
    try {
      await apiRequest("/api/v1/demo/bootstrap", { method: "POST" });
      await loadConsoleState();
      setTopBanner(
        "✓ Bootstrapped 3-Node Federation State on live FastAPI backend (Node A, Node B, Node C)."
      );
    } catch (err) {
      setTopBanner(
        `✕ Could not bootstrap demo state: ${
          err instanceof Error ? err.message : "Backend error"
        }`
      );
    }
  }

  async function handleSignOut() {
    try {
      await apiRequest("/api/v1/auth/logout", { method: "POST" });
    } catch {
      // ignore
    }
    if (typeof window !== "undefined") {
      window.localStorage.removeItem("km_access_token");
      window.localStorage.removeItem("km_refresh_token");
      window.localStorage.removeItem("km_org_id");
    }
    setCurrentUser(null);
    setStage("landing");
  }

  const totalClaimsCount = useMemo(
    () => bundles.reduce((acc, b) => acc + b.claims.length, 0),
    [bundles]
  );

  // STAGE 1: Animated Landing Page
  if (stage === "landing") {
    return (
      <LandingPageView
        onGoToLogin={() => {
          setAuthInitialMode("login");
          setStage("login");
        }}
        onGoToRegister={() => {
          setAuthInitialMode("register");
          setStage("login");
        }}
      />
    );
  }

  // STAGE 2: Strict Backend Authentication Gate
  if (stage === "login" || !currentUser) {
    return (
      <LoginGateView
        initialMode={authInitialMode}
        onBackToLanding={() => setStage("landing")}
        onAuthenticated={(principal) => {
          setCurrentUser(principal);
          setStage("dashboard");
        }}
      />
    );
  }

  // STAGE 3: Authenticated Organization Console & Developer Platform
  const navGroups = [
    {
      group: "Control Plane",
      items: [
        { id: "overview", icon: "◈", label: "Overview", count: undefined },
        { id: "nodes", icon: "⬡", label: "My Nodes", count: nodes.length },
        {
          id: "knowledge",
          icon: "❖",
          label: "Knowledge Bundles",
          count: bundles.length,
        },
        {
          id: "claims",
          icon: "⚖",
          label: "Claims & 6-D Rubric",
          count: totalClaimsCount,
        },
        {
          id: "okf-graph",
          icon: "🕸",
          label: "OKF Graph Workspace",
          count: undefined,
        },
        { id: "discover", icon: "⌕", label: "Discover", count: undefined },
      ],
    },
    {
      group: "Federation & Trust",
      items: [
        { id: "agents", icon: "🤖", label: "AI Agents", count: agents.length },
        {
          id: "federation",
          icon: "⇄",
          label: "Federation & Peers",
          count: peers.length,
        },
        {
          id: "trust",
          icon: "🛡",
          label: "Trust & Verifier",
          count: undefined,
        },
        {
          id: "bounties",
          icon: "★",
          label: "Reputation & Bounties",
          count: bountiesCount,
        },
        {
          id: "audit",
          icon: "📋",
          label: "Activity & Audit",
          count: auditEvents.length,
        },
      ],
    },
    {
      group: "Platform",
      items: [
        {
          id: "developer",
          icon: "⌘",
          label: "Developer Portal",
          count: undefined,
        },
        {
          id: "settings",
          icon: "⚙",
          label: "Organizations & RBAC",
          count: undefined,
        },
      ],
    },
  ];

  const primaryNode = nodes[0] || null;

  return (
    <div className="km-shell">
      {/* Left Navigation Sidebar */}
      <aside
        className={`km-sidebar ${sidebarCollapsed ? "collapsed" : ""}`}
        aria-label="Primary Navigation"
      >
        <div className="km-brand-bar">
          <div className="km-brand-logo">
            <span className="km-brand-glyph">KM</span>
            {!sidebarCollapsed && (
              <div>
                know<span>mesh</span>
              </div>
            )}
          </div>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={() => setSidebarCollapsed((c) => !c)}
            title="Toggle navigation rail"
          >
            {sidebarCollapsed ? "»" : "«"}
          </button>
        </div>

        {navGroups.map((grp) => (
          <div key={grp.group} className="km-nav-group">
            {!sidebarCollapsed && (
              <div className="km-nav-label">{grp.group}</div>
            )}
            {grp.items.map((item) => (
              <button
                key={item.id}
                type="button"
                className={`km-nav-item ${
                  activeTab === item.id ? "active" : ""
                }`}
                onClick={() => setActiveTab(item.id)}
              >
                <span className="km-nav-item-left">
                  <span className="km-nav-icon">{item.icon}</span>
                  {!sidebarCollapsed && <span>{item.label}</span>}
                </span>
                {!sidebarCollapsed && item.count !== undefined && (
                  <span className="km-nav-count">{item.count}</span>
                )}
              </button>
            ))}
          </div>
        ))}

        {!sidebarCollapsed && (
          <div
            style={{
              marginTop: "auto",
              padding: 16,
              borderTop: "1px solid var(--border-subtle)",
              fontSize: 11.5,
              color: "var(--text-muted)",
            }}
          >
            <div style={{ fontWeight: 600, color: "var(--text-secondary)" }}>
              Principal: {currentUser.full_name}
            </div>
            <div>Role: {currentUser.role.toUpperCase()}</div>
            <div style={{ marginTop: 8, display: "flex", gap: 6 }}>
              <button
                type="button"
                className="km-btn km-btn-sm"
                onClick={() => setStage("landing")}
              >
                Product Info
              </button>
              <button
                type="button"
                className="km-btn km-btn-sm km-btn-danger"
                onClick={handleSignOut}
              >
                Sign Out
              </button>
            </div>
          </div>
        )}
      </aside>

      {/* Main Workspace */}
      <div className="km-workspace">
        {/* Top Command & Telemetry Bar */}
        <header className="km-topbar">
          <div className="km-topbar-left">
            <span
              className={`km-badge ${apiConnected ? "verified" : "warning"}`}
              title={`Connected to ${API_BASE_URL}`}
            >
              ●{" "}
              {apiConnected
                ? `Live Backend · ${liveOverview?.node_id || "node-a"}`
                : "Backend Disconnected"}
            </span>
            <span className="km-badge info">
              {currentUser.organization_name} · {currentUser.role}
            </span>
            {primaryNode && (
              <span className="km-mono" title={primaryNode.key_fingerprint}>
                Ed25519: {primaryNode.key_fingerprint.slice(0, 14)}…
              </span>
            )}
          </div>

          <div className="km-topbar-right">
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => setShowCommandPalette(true)}
            >
              ⌘K Quick Command
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm km-btn-accent"
              onClick={handleBootstrapDemo}
            >
              ⚡ Seed 3-Node State
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => setActiveTab("discover")}
            >
              ⌕ Federated Search
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => setActiveTab("trust")}
            >
              🛡 Tamper Verifier
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm km-btn-danger"
              onClick={handleSignOut}
            >
              Sign Out
            </button>
          </div>
        </header>

        <main className="km-main">
          {topBanner && (
            <div className="km-notice verified">
              <span>{topBanner}</span>
              <button
                type="button"
                className="km-btn km-btn-sm"
                onClick={() => setTopBanner(null)}
              >
                ✕
              </button>
            </div>
          )}

          {activeTab === "overview" && (
            <OverviewView
              overview={liveOverview}
              onNavigate={setActiveTab}
              onRefresh={loadConsoleState}
              onBootstrapDemo={handleBootstrapDemo}
            />
          )}
          {activeTab === "nodes" && (
            <NodesView
              nodes={nodes}
              bundles={bundles}
              agents={agents}
              peers={peers}
              auditEvents={auditEvents}
              onRefresh={loadConsoleState}
            />
          )}
          {activeTab === "knowledge" && (
            <KnowledgeView
              bundles={bundles}
              nodes={nodes}
              onSelectBundleDrawer={(b) => setDrawerBundle(b)}
              onRefresh={loadConsoleState}
            />
          )}
          {activeTab === "okf-graph" && (
            <OKFGraphWorkspace onNavigateTab={setActiveTab} />
          )}
          {activeTab === "discover" && (
            <DiscoverView
              bundles={bundles}
              onInspectBundle={(b) => setDrawerBundle(b)}
            />
          )}
          {activeTab === "agents" && (
            <AgentsView
              agents={agents}
              credentials={credentials}
              nodes={nodes}
              onRefresh={loadConsoleState}
            />
          )}
          {activeTab === "federation" && (
            <FederationView
              overview={liveOverview}
              peers={peers}
              onRefresh={loadConsoleState}
            />
          )}
          {activeTab === "trust" && <TrustSecurityView bundles={bundles} />}
          {activeTab === "claims" && (
            <ClaimsRubricView
              bundles={bundles}
              onSelectBundleDrawer={(b) => setDrawerBundle(b)}
              onRefresh={loadConsoleState}
            />
          )}
          {activeTab === "bounties" && (
            <ReputationBountiesView nodes={nodes} />
          )}
          {activeTab === "audit" && (
            <AuditLogsView auditEvents={auditEvents} />
          )}
          {activeTab === "developer" && (
            <DeveloperPortalView node={primaryNode} />
          )}
          {activeTab === "settings" && (
            <SettingsView onAuthChanged={loadConsoleState} />
          )}
        </main>
      </div>

      {/* Quick Command Palette Modal (Cmd/Ctrl+K) */}
      {showCommandPalette && (
        <div
          className="km-modal-backdrop"
          onClick={() => setShowCommandPalette(false)}
        >
          <div
            className="km-modal"
            style={{ width: 560 }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="km-card-header">
              <h3 className="km-card-title">KnowMesh Quick Command Palette</h3>
              <button
                type="button"
                className="km-btn km-btn-sm"
                onClick={() => setShowCommandPalette(false)}
              >
                ESC
              </button>
            </div>
            <input
              autoFocus
              className="km-input"
              placeholder="Jump to workspace, bundle, or cryptographic action…"
              value={commandQuery}
              onChange={(e) => setCommandQuery(e.target.value)}
              style={{ marginBottom: 14 }}
            />
            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              {[
                {
                  label: "◈ Go to Network Control Plane Overview",
                  action: () => setActiveTab("overview"),
                },
                {
                  label: "❖ Publish & Sign New OKF Knowledge Bundle",
                  action: () => setActiveTab("knowledge"),
                },
                {
                  label: "⌕ Run Federated BM25 Discovery Search",
                  action: () => setActiveTab("discover"),
                },
                {
                  label: "🛡 Open Zero-Trust Tamper & Signature Verifier",
                  action: () => setActiveTab("trust"),
                },
                {
                  label: "⇄ Inspect Federated Peers & Run Pull-Sync",
                  action: () => setActiveTab("federation"),
                },
                {
                  label: "🤖 Manage AI Agents & Rotate SHA-256 Keys",
                  action: () => setActiveTab("agents"),
                },
                {
                  label: "⌘ Open Python SDK & Live API Playground",
                  action: () => setActiveTab("developer"),
                },
                {
                  label: "⚡ Seed 3-Node Federation State on Backend",
                  action: () => handleBootstrapDemo(),
                },
              ]
                .filter((item) =>
                  item.label.toLowerCase().includes(commandQuery.toLowerCase())
                )
                .map((item) => (
                  <button
                    key={item.label}
                    type="button"
                    className="km-btn"
                    style={{ justifyContent: "flex-start", padding: "10px 14px" }}
                    onClick={() => {
                      item.action();
                      setShowCommandPalette(false);
                    }}
                  >
                    {item.label}
                  </button>
                ))}
            </div>
          </div>
        </div>
      )}

      {/* Slide-out Bundle Provenance & Verification Drawer */}
      {drawerBundle && (
        <div
          className="km-drawer-backdrop"
          onClick={() => setDrawerBundle(null)}
        >
          <aside
            className="km-drawer"
            role="dialog"
            aria-label="Knowledge Bundle Inspection Drawer"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="km-card-header">
              <div>
                <span className="km-mono">
                  {drawerBundle.bundle_id}@{drawerBundle.current_revision}
                </span>
                <h3 style={{ margin: "6px 0 0", fontSize: 18 }}>
                  {drawerBundle.title}
                </h3>
              </div>
              <button
                type="button"
                className="km-btn km-btn-sm"
                onClick={() => setDrawerBundle(null)}
              >
                ✕ Close
              </button>
            </div>

            <div className="km-notice">
              <span>
                <strong>Epistemic Separation:</strong>{" "}
                {drawerBundle.verification?.epistemic_notice}
              </span>
            </div>

            <div className="km-field">
              <span className="km-label">
                Cryptographic Verification Breakdown
              </span>
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                <span
                  className={`km-badge ${
                    drawerBundle.verification?.integrity_verified
                      ? "verified"
                      : "error"
                  }`}
                >
                  JCS Digest:{" "}
                  {drawerBundle.verification?.integrity_verified
                    ? "Verified"
                    : "Failed"}
                </span>
                <span
                  className={`km-badge ${
                    drawerBundle.verification?.signature_verified
                      ? "verified"
                      : "error"
                  }`}
                >
                  Ed25519:{" "}
                  {drawerBundle.verification?.signature_verified
                    ? "Valid"
                    : "Invalid"}
                </span>
                <span
                  className={`km-badge ${
                    drawerBundle.verification?.signer_recognized
                      ? "verified"
                      : "warning"
                  }`}
                >
                  Signer:{" "}
                  {drawerBundle.verification?.signer_recognized
                    ? "Recognized"
                    : "Unknown"}
                </span>
              </div>
            </div>

            <div className="km-field">
              <span className="km-label">
                Canonical Content Digest (RFC 8785 JCS SHA-256)
              </span>
              <CopySnippet
                text={drawerBundle.content_digest}
                label={drawerBundle.content_digest}
              />
            </div>

            <div className="km-field">
              <span className="km-label">
                Atomic Claims ({drawerBundle.claims.length})
              </span>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {drawerBundle.claims.map((c) => (
                  <div
                    key={c.claim_id}
                    style={{
                      padding: 12,
                      background: "var(--bg-secondary)",
                      border: "1px solid var(--border-subtle)",
                      borderRadius: "var(--radius-sm)",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        marginBottom: 6,
                      }}
                    >
                      <span className="km-mono">{c.claim_id}</span>
                      <span className={`km-badge ${c.status}`}>{c.status}</span>
                    </div>
                    <div style={{ fontSize: 13.5 }}>{c.statement}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="km-field">
              <span className="km-label">
                Supporting Evidence ({drawerBundle.evidence.length})
              </span>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {drawerBundle.evidence.map((ev) => (
                  <div
                    key={ev.evidence_id}
                    style={{
                      padding: 12,
                      background: "var(--bg-secondary)",
                      border: "1px solid var(--border-subtle)",
                      borderRadius: "var(--radius-sm)",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        marginBottom: 4,
                      }}
                    >
                      <span className="km-mono">{ev.evidence_id}</span>
                      <span className="km-badge info">{ev.source_type}</span>
                    </div>
                    <div style={{ fontWeight: 600 }}>
                      {ev.title || ev.description}
                    </div>
                    <div className="km-metric-sub">{ev.source_uri}</div>
                  </div>
                ))}
              </div>
            </div>
          </aside>
        </div>
      )}
    </div>
  );
}
