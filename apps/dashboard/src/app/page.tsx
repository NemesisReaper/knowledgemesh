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

export default function KyroConsolePage() {
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
        `✕ Could not bootstrap demo state: ${err instanceof Error ? err.message : "Backend error"
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
          icon: "⊞",
          label: "Knowledge Bundles",
          count: bundles.length,
        },
        {
          id: "claims",
          icon: "§",
          label: "Claims & 6-D Rubric",
          count: totalClaimsCount,
        },
        {
          id: "okf-graph",
          icon: "☍",
          label: "OKF Graph Workspace",
          count: undefined,
        },
        { id: "discover", icon: "⌕", label: "Discover", count: undefined },
      ],
    },
    {
      group: "Federation & Trust",
      items: [
        { id: "agents", icon: "▲", label: "AI Agents", count: agents.length },
        {
          id: "federation",
          icon: "⇄",
          label: "Federation & Peers",
          count: peers.length,
        },
        {
          id: "trust",
          icon: "✓",
          label: "Trust & Verifier",
          count: undefined,
        },
        {
          id: "bounties",
          icon: "✦",
          label: "Reputation & Bounties",
          count: bountiesCount,
        },
        {
          id: "audit",
          icon: "≡",
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
          icon: "⎈",
          label: "Organizations & RBAC",
          count: undefined,
        },
      ],
    },
  ];

  const primaryNode = nodes[0] || null;
  const userInitials = (currentUser.full_name || currentUser.email || "KM")
    .split(" ")
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div className="km-shell">
      {/* Left Navigation Sidebar */}
      <aside
        className={`km-sidebar ${sidebarCollapsed ? "collapsed" : ""}`}
        aria-label="Primary Navigation"
      >
        <div className="km-brand-bar">
          <div className="km-brand-logo" style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <img
              src="/kyro-logo.png"
              alt="Kyro Logo"
              style={{
                height: 28,
                width: 28,
                objectFit: "contain",
                borderRadius: 6,
              }}
            />
            {!sidebarCollapsed && (
              <span style={{ fontSize: 18, fontWeight: 800, color: "#0A0F1D", letterSpacing: "-0.03em", display: "flex", alignItems: "center", gap: 6 }}>
                kyro
                <span
                  style={{
                    fontSize: 10,
                    fontWeight: 700,
                    color: "#6366F1",
                    backgroundColor: "rgba(99, 102, 241, 0.08)",
                    padding: "2px 6px",
                    borderRadius: 999,
                    border: "1px solid rgba(99, 102, 241, 0.2)",
                  }}
                >
                  CONSOLE
                </span>
              </span>
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
                className={`km-nav-item ${activeTab === item.id ? "active" : ""
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
              padding: "16px",
              borderTop: "1px solid #E2E8F0",
              backgroundColor: "#F8FAFC",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
              <div
                style={{
                  width: 34,
                  height: 34,
                  borderRadius: "50%",
                  background: "linear-gradient(135deg, #6366F1 0%, #EC4899 100%)",
                  color: "#FFFFFF",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontWeight: 750,
                  fontSize: 12,
                  boxShadow: "0 2px 6px rgba(99, 102, 241, 0.25)",
                  flexShrink: 0,
                }}
              >
                {userInitials}
              </div>
              <div style={{ minWidth: 0, flex: 1 }}>
                <div style={{ fontWeight: 700, color: "#0A0F1D", fontSize: 13, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {currentUser.full_name}
                </div>
                <div style={{ fontSize: 11, color: "#64748B", display: "flex", alignItems: "center", gap: 6 }}>
                  <span style={{ textTransform: "capitalize" }}>{currentUser.role}</span>
                  <span>·</span>
                  <span style={{ color: "#10B981", fontWeight: 600 }}>Active</span>
                </div>
              </div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button
                type="button"
                className="km-btn km-btn-sm"
                style={{ flex: 1 }}
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
              style={{ padding: "4px 12px" }}
            >
              <span
                style={{
                  width: 7,
                  height: 7,
                  borderRadius: "50%",
                  backgroundColor: apiConnected ? "#10B981" : "#F59E0B",
                  boxShadow: apiConnected ? "0 0 8px rgba(16, 185, 129, 0.6)" : "none",
                  display: "inline-block",
                  marginRight: 4,
                }}
              />
              {apiConnected
                ? `Live Mesh · ${liveOverview?.node_id || "node-a"}`
                : "Backend Disconnected"}
            </span>
            <span className="km-badge info" style={{ padding: "4px 12px" }}>
              {currentUser.organization_name}
            </span>
            {primaryNode && (
              <span
                className="km-mono"
                title={primaryNode.key_fingerprint}
                style={{ fontSize: 11.5, padding: "3px 8px" }}
              >
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
              <span style={{ fontSize: 11, color: "#64748B" }}>⌘K</span> Quick Action
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm km-btn-accent"
              onClick={handleBootstrapDemo}
            >
              Seed 3-Node State
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
              Tamper Verifier
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

      {/* Quick Actions Search Popup (Cmd/Ctrl+K) */}
      {showCommandPalette && (
        <div
          className="km-modal-backdrop"
          onClick={() => setShowCommandPalette(false)}
        >
          <div
            className="km-modal"
            style={{ width: 560, padding: "24px 28px" }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="km-card-header" style={{ marginBottom: 14 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: 16 }}>⌘</span>
                <h3 className="km-card-title">Quick Actions</h3>
              </div>
              <button
                type="button"
                className="km-modal-close"
                onClick={() => setShowCommandPalette(false)}
                title="Close (ESC)"
              >
                ✕
              </button>
            </div>
            <div style={{ position: "relative", marginBottom: 14 }}>
              <input
                autoFocus
                className="km-input"
                placeholder="Type to search or jump to a section…"
                value={commandQuery}
                onChange={(e) => setCommandQuery(e.target.value)}
                style={{ paddingLeft: 36, height: 42, fontSize: 13.5 }}
              />
              <span style={{ position: "absolute", left: 12, top: 12, color: "#94A3B8", fontSize: 14 }}>
                ⌕
              </span>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 4, maxHeight: 360, overflowY: "auto" }}>
              {[
                {
                  icon: "◈",
                  label: "Overview Dashboard",
                  sub: "View network health and live statistics",
                  action: () => setActiveTab("overview"),
                },
                {
                  icon: "⊞",
                  label: "Create Knowledge Document",
                  sub: "Write, verify and publish verified content",
                  action: () => setActiveTab("knowledge"),
                },
                {
                  icon: "⌕",
                  label: "Search Network",
                  sub: "Find claims, documents and evidence",
                  action: () => setActiveTab("discover"),
                },
                {
                  icon: "✓",
                  label: "Verify Document Signatures",
                  sub: "Validate integrity and test tampering",
                  action: () => setActiveTab("trust"),
                },
                {
                  icon: "⇄",
                  label: "Connected Nodes & Sync",
                  sub: "Manage federated peer connections",
                  action: () => setActiveTab("federation"),
                },
                {
                  icon: "▲",
                  label: "AI Agents & API Keys",
                  sub: "Configure agent access and credentials",
                  action: () => setActiveTab("agents"),
                },
                {
                  icon: "⌘",
                  label: "Developer Tools & API",
                  sub: "Python SDK snippets and live request runner",
                  action: () => setActiveTab("developer"),
                },
                {
                  icon: "●",
                  label: "Load Sample Demo Nodes",
                  sub: "Quickly populate sample mesh nodes",
                  action: () => handleBootstrapDemo(),
                },
              ]
                .filter((item) =>
                  item.label.toLowerCase().includes(commandQuery.toLowerCase()) ||
                  item.sub.toLowerCase().includes(commandQuery.toLowerCase())
                )
                .map((item) => (
                  <button
                    key={item.label}
                    type="button"
                    className="km-btn"
                    style={{
                      justifyContent: "space-between",
                      padding: "10px 14px",
                      borderRadius: "10px",
                      border: "1px solid transparent",
                      background: "transparent",
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = "#F8FAFC";
                      e.currentTarget.style.borderColor = "#E2E8F0";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = "transparent";
                      e.currentTarget.style.borderColor = "transparent";
                    }}
                    onClick={() => {
                      item.action();
                      setShowCommandPalette(false);
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                      <span style={{ fontSize: 15, color: "#6366F1", width: 18, textAlign: "center" }}>
                        {item.icon}
                      </span>
                      <div style={{ textAlign: "left" }}>
                        <div style={{ fontWeight: 650, color: "#0A0F1D", fontSize: 13 }}>
                          {item.label}
                        </div>
                        <div style={{ fontSize: 11.5, color: "#64748B" }}>
                          {item.sub}
                        </div>
                      </div>
                    </div>
                    <span style={{ fontSize: 11, color: "#94A3B8" }}>→</span>
                  </button>
                ))}
            </div>
          </div>
        </div>
      )}

      {/* Modern Slide-out Document Details Drawer */}
      {drawerBundle && (
        <div
          className="km-drawer-backdrop"
          onClick={() => setDrawerBundle(null)}
        >
          <aside
            className="km-drawer"
            role="dialog"
            aria-label="Document Details"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="km-card-header" style={{ marginBottom: 20 }}>
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                  <span
                    style={{
                      fontSize: 11,
                      fontWeight: 700,
                      color: "#6366F1",
                      backgroundColor: "rgba(99, 102, 241, 0.08)",
                      padding: "2px 8px",
                      borderRadius: 999,
                      border: "1px solid rgba(99, 102, 241, 0.2)",
                    }}
                  >
                    Revision {drawerBundle.current_revision || "1"}
                  </span>
                  <span style={{ fontSize: 12, color: "#64748B" }}>
                    ID: {drawerBundle.bundle_id}
                  </span>
                </div>
                <h3 style={{ margin: 0, fontSize: 19, fontWeight: 750, color: "#0A0F1D" }}>
                  {drawerBundle.title}
                </h3>
              </div>
              <button
                type="button"
                className="km-modal-close"
                onClick={() => setDrawerBundle(null)}
                title="Close"
              >
                ✕
              </button>
            </div>

            {/* Verification Status Overview */}
            <div
              style={{
                backgroundColor: "#F8FAFC",
                border: "1px solid #E2E8F0",
                borderRadius: "12px",
                padding: "14px 16px",
                marginBottom: 20,
              }}
            >
              <div style={{ fontSize: 11.5, fontWeight: 700, color: "#64748B", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 8 }}>
                Verification & Trust Status
              </div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
                <span className="km-badge verified">
                  ✓ Digital Signature Verified
                </span>
                <span className="km-badge verified">
                  ✓ Content Untampered
                </span>
                <span className="km-badge info">
                  {drawerBundle.verification?.signer_recognized ? "Verified Signer" : "Known Key"}
                </span>
              </div>
              {drawerBundle.verification?.epistemic_notice && (
                <div style={{ fontSize: 12, color: "#475569", lineHeight: 1.45, borderTop: "1px solid #E2E8F0", paddingTop: 8 }}>
                  {drawerBundle.verification.epistemic_notice}
                </div>
              )}
            </div>

            {/* Content Checksum / Hash */}
            <div className="km-field" style={{ marginBottom: 20 }}>
              <span className="km-label">Content Checksum</span>
              <CopySnippet
                text={drawerBundle.content_digest}
                label={drawerBundle.content_digest ? `${drawerBundle.content_digest.slice(0, 16)}…${drawerBundle.content_digest.slice(-12)}` : ""}
              />
            </div>

            {/* Key Statements */}
            <div className="km-field" style={{ marginBottom: 20 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                <span className="km-label" style={{ margin: 0 }}>
                  Key Statements ({drawerBundle.claims.length})
                </span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {drawerBundle.claims.map((c) => (
                  <div
                    key={c.claim_id}
                    style={{
                      padding: "12px 14px",
                      backgroundColor: "#FFFFFF",
                      border: "1px solid #E2E8F0",
                      borderRadius: "10px",
                      boxShadow: "0 1px 2px rgba(0,0,0,0.02)",
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                      <span style={{ fontSize: 11.5, fontWeight: 650, color: "#64748B" }}>
                        {c.domain || "Fact"}
                      </span>
                      <span className={`km-badge ${c.status}`}>
                        {c.status === "verified" ? "Verified" : c.status}
                      </span>
                    </div>
                    <div style={{ fontSize: 13, color: "#0A0F1D", lineHeight: 1.45 }}>
                      {c.statement}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Sources & Citations */}
            <div className="km-field">
              <span className="km-label">
                Sources & Citations ({drawerBundle.evidence.length})
              </span>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {drawerBundle.evidence.map((ev) => (
                  <div
                    key={ev.evidence_id}
                    style={{
                      padding: "12px 14px",
                      backgroundColor: "#FFFFFF",
                      border: "1px solid #E2E8F0",
                      borderRadius: "10px",
                      boxShadow: "0 1px 2px rgba(0,0,0,0.02)",
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                      <span style={{ fontWeight: 650, color: "#0A0F1D", fontSize: 13 }}>
                        {ev.title || ev.description}
                      </span>
                      <span className="km-badge info" style={{ fontSize: 11 }}>
                        {ev.source_type}
                      </span>
                    </div>
                    {ev.source_uri && (
                      <div style={{ fontSize: 11.5, color: "#64748B", wordBreak: "break-all" }}>
                        {ev.source_uri}
                      </div>
                    )}
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
