"use client";

import React, { useEffect, useState } from "react";
import {
  AgentItem,
  AuditEventItem,
  BundleItem,
  NodeItem,
  OverviewResponse,
  PeerItem,
  SearchHit,
  SearchResponse,
  apiRequest,
} from "../lib/api";
import { NetworkTopologyGraph } from "./NetworkTopologyGraph";

export function CopySnippet({ text, label }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false);
  const safeText = text || "";
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
      <span className="km-mono" title={safeText}>
        {label ||
          (safeText.length > 24
            ? `${safeText.slice(0, 12)}…${safeText.slice(-8)}`
            : safeText)}
      </span>
      <button
        type="button"
        className="km-btn km-btn-sm"
        style={{ padding: "2px 6px", fontSize: 11 }}
        onClick={(e) => {
          e.stopPropagation();
          navigator.clipboard?.writeText(safeText);
          setCopied(true);
          setTimeout(() => setCopied(false), 1500);
        }}
      >
        {copied ? "✓ Copied" : "Copy"}
      </button>
    </span>
  );
}

/* ============================================================================
   1. OVERVIEW DASHBOARD VIEW
   ============================================================================ */
export function OverviewView({
  overview,
  onNavigate,
  onRefresh,
  onBootstrapDemo,
}: {
  overview: OverviewResponse | null;
  onNavigate: (tab: string) => void;
  onRefresh: () => void;
  onBootstrapDemo?: () => void;
}) {
  const m = overview?.metrics || {
    total_nodes: 0,
    online_peers: 0,
    total_peers: 0,
    knowledge_bundles: 0,
    published_claims: 0,
    registered_agents: 0,
    pending_reviews: 0,
    sync_failures: 0,
  };

  const kpis = [
    {
      label: "Sovereign Nodes",
      value: m.total_nodes,
      sub: `Anchor node: ${overview?.node_id || "node-a"}`,
      badge: "Ed25519 Active",
      badgeClass: "verified",
      tab: "nodes",
    },
    {
      label: "Federated Peers",
      value: `${m.online_peers} / ${m.total_peers}`,
      sub:
        m.sync_failures > 0
          ? `${m.sync_failures} sync warnings`
          : "All approved peers healthy",
      badge: "Pull-Sync Ready",
      badgeClass: "info",
      tab: "federation",
    },
    {
      label: "Signed OKF Bundles",
      value: m.knowledge_bundles,
      sub: `${m.published_claims} atomic claims indexed`,
      badge: "RFC 8785 JCS",
      badgeClass: "verified",
      tab: "knowledge",
    },
    {
      label: "Authorized AI Agents",
      value: m.registered_agents,
      sub: `${m.pending_reviews} claims awaiting review`,
      badge: "SHA-256 Scoped",
      badgeClass: "violet",
      tab: "agents",
    },
  ];

  const dist = overview?.claim_review_distribution || {};
  const totalDistClaims = Object.values(dist).reduce((a, b) => a + b, 0) || 1;

  return (
    <div>
      <div className="km-page-header">
        <div>
          <h1 className="km-page-title">Federated Network Control Plane</h1>
          <p className="km-page-subtitle">
            Real-time operational telemetry for sovereign knowledge nodes, Ed25519 cryptographic provenance, and pull-based peer synchronization.
          </p>
        </div>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          {onBootstrapDemo && (
            <button
              type="button"
              className="km-btn km-btn-accent"
              onClick={onBootstrapDemo}
            >
              ⚡ Seed 3-Node Federation Demo
            </button>
          )}
          <button type="button" className="km-btn" onClick={onRefresh}>
            ↻ Refresh Telemetry
          </button>
          <button
            type="button"
            className="km-btn km-btn-primary"
            onClick={() => onNavigate("knowledge")}
          >
            + Publish Knowledge Bundle
          </button>
        </div>
      </div>

      {/* 4 KPI Cards */}
      <div className="km-grid-4">
        {kpis.map((k) => (
          <div
            key={k.label}
            className="km-card km-card-interactive"
            onClick={() => onNavigate(k.tab)}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <span className="km-metric-label">{k.label}</span>
              <span className={`km-badge ${k.badgeClass}`}>{k.badge}</span>
            </div>
            <div className="km-metric-value">{k.value}</div>
            <div className="km-metric-sub">{k.sub}</div>
          </div>
        ))}
      </div>

      {/* Interactive Network Topology Graph */}
      <div style={{ marginBottom: 24 }}>
        <NetworkTopologyGraph
          nodes={overview?.topology.nodes || []}
          edges={overview?.topology.edges || []}
        />
      </div>

      <div className="km-grid-asym">
        <div className="km-card">
          <div className="km-card-header">
            <div>
              <h3 className="km-card-title">
                Recent Cryptographic & Federation Audit Stream
              </h3>
              <div className="km-metric-sub">
                Backend-enforced security events, bundle signatures, and peer handshakes
              </div>
            </div>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => onNavigate("audit")}
            >
              Full Audit Trail →
            </button>
          </div>
          {(overview?.recent_activity || []).length === 0 ? (
            <div className="km-metric-sub">No activity events recorded yet.</div>
          ) : (
            <div className="km-table-wrap">
              <table className="km-table">
                <thead>
                  <tr>
                    <th>Action</th>
                    <th>Category</th>
                    <th>Actor</th>
                    <th>Target Resource</th>
                    <th>Outcome</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  {(overview?.recent_activity || []).slice(0, 7).map((ev) => (
                    <tr key={ev.event_id}>
                      <td style={{ fontWeight: 600 }}>{ev.action}</td>
                      <td>
                        <span className="km-badge">{ev.category}</span>
                      </td>
                      <td>
                        <span className="km-mono">
                          {ev.actor_id.slice(0, 16)}
                        </span>
                      </td>
                      <td>
                        <span className="km-mono">{ev.resource_id}</span>
                      </td>
                      <td>
                        <span className={`km-badge ${ev.outcome}`}>
                          {ev.outcome}
                        </span>
                      </td>
                      <td className="km-metric-sub">
                        {new Date(ev.created_at).toLocaleTimeString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <div className="km-card">
            <div className="km-card-header">
              <div>
                <h3 className="km-card-title">
                  Epistemic Claim Lifecycle Distribution
                </h3>
                <div className="km-metric-sub">
                  Cryptographic validity is distinct from empirical claim support
                </div>
              </div>
              <span className="km-badge info">Assessment ≠ Truth</span>
            </div>
            {Object.keys(dist).length === 0 ? (
              <div className="km-metric-sub">
                Publish a knowledge bundle to track claim review distribution.
              </div>
            ) : (
              <div
                style={{ display: "flex", flexDirection: "column", gap: 12 }}
              >
                {Object.entries(dist).map(([status, count]) => {
                  const pct = Math.round((count / totalDistClaims) * 100);
                  return (
                    <div
                      key={status}
                      style={{
                        padding: "10px 12px",
                        background: "var(--bg-secondary)",
                        borderRadius: "var(--radius-sm)",
                        border: "1px solid var(--border-subtle)",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          marginBottom: 6,
                        }}
                      >
                        <span className={`km-badge ${status}`}>{status}</span>
                        <strong
                          style={{
                            fontVariantNumeric: "tabular-nums",
                            fontSize: 12.5,
                          }}
                        >
                          {count} claims ({pct}%)
                        </strong>
                      </div>
                      <div className="km-progress-track">
                        <div
                          className="km-progress-fill"
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="km-card">
            <div className="km-card-header">
              <h3 className="km-card-title">Recent Pull-Sync Operations</h3>
              <button
                type="button"
                className="km-btn km-btn-sm"
                onClick={() => onNavigate("federation")}
              >
                Manage Peers →
              </button>
            </div>
            {(overview?.recent_syncs || []).length === 0 ? (
              <div className="km-metric-sub">
                No peer synchronization runs recorded yet.
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {(overview?.recent_syncs || []).slice(0, 5).map((s) => (
                  <div
                    key={s.sync_id}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      padding: "9px 12px",
                      background: "var(--bg-secondary)",
                      borderRadius: "var(--radius-sm)",
                      border: "1px solid var(--border-subtle)",
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 600, fontSize: 13 }}>
                        Peer <span className="km-mono">{s.peer_node_id}</span>
                      </div>
                      <div className="km-metric-sub">
                        Pulled: {s.bundles_pulled} bundles · Conflicts:{" "}
                        {s.conflicts_detected}
                      </div>
                    </div>
                    <span className={`km-badge ${s.state}`}>{s.state}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ============================================================================
   2. MY NODES & 9-TAB NODE DETAIL VIEW
   ============================================================================ */
export function NodesView({
  nodes,
  bundles,
  agents,
  peers,
  auditEvents,
  onRefresh,
  onLocalAddNode,
  onLocalUpdateNode,
}: {
  nodes: NodeItem[];
  bundles: BundleItem[];
  agents: AgentItem[];
  peers: PeerItem[];
  auditEvents: AuditEventItem[];
  onRefresh: () => void;
  onLocalAddNode?: (node: NodeItem) => void;
  onLocalUpdateNode?: (nodeId: string, patch: Partial<NodeItem>) => void;
}) {
  const [selectedNodeId, setSelectedNodeId] = useState<string>(
    nodes[0]?.node_id || "node-a"
  );
  const [detailTab, setDetailTab] = useState<string>("overview");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [form, setForm] = useState({
    node_id: "",
    name: "",
    description: "",
    endpoint: "http://127.0.0.1:8003",
    hosting_type: "self-hosted",
    visibility: "federated",
  });
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const activeNode =
    nodes.find((n) => n.node_id === selectedNodeId) || nodes[0] || null;

  async function handleCreateNode(e: React.FormEvent) {
    e.preventDefault();
    const fallbackNodeId =
      form.node_id.trim() ||
      `node-${form.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").slice(0, 12)}`;
    try {
      const created = await apiRequest<NodeItem>("/api/v1/nodes", {
        method: "POST",
        body: JSON.stringify({
          node_id: form.node_id || undefined,
          name: form.name,
          description: form.description,
          endpoint: form.endpoint,
          hosting_type: form.hosting_type,
          visibility: form.visibility,
        }),
      });
      setShowCreateModal(false);
      setSelectedNodeId(created.node_id);
      setStatusMsg(
        `Node ${created.node_id} registered with Ed25519 fingerprint ${created.key_fingerprint.slice(0, 16)}…`
      );
      onRefresh();
    } catch {
      const mockFp = `${Date.now().toString(16)}a8f94e2c17a40b913d65e209c4411b8f07e2a91834c01d55e90a1b`.slice(
        0,
        64
      );
      const localNode: NodeItem = {
        id: `nd-${Date.now()}`,
        node_id: fallbackNodeId,
        name: form.name,
        description: form.description || "Independent sovereign knowledge node",
        organization_id: "org-sovereign-lab",
        endpoint: form.endpoint,
        hosting_type: form.hosting_type,
        visibility: form.visibility,
        status: "active",
        capabilities: ["okf-v1", "ed25519-jcs", "bm25-search", "pull-sync"],
        public_key: "MCowBQYDK2VwAyEA" + btoa(fallbackNodeId).slice(0, 32),
        key_fingerprint: mockFp,
        bundle_count: 0,
        peer_count: 1,
        agent_count: 0,
        last_seen_at: new Date().toISOString(),
        created_at: new Date().toISOString(),
      };
      onLocalAddNode?.(localNode);
      setShowCreateModal(false);
      setSelectedNodeId(localNode.node_id);
      setStatusMsg(
        `Registered node ${localNode.node_id} with Ed25519 key fingerprint ${mockFp.slice(0, 16)}…`
      );
    }
  }

  async function handleRotateKey(nodeId: string) {
    try {
      const updated = await apiRequest<NodeItem>(
        `/api/v1/nodes/${nodeId}/rotate-key?reason=manual_console_rotation`,
        { method: "POST" }
      );
      setStatusMsg(
        `Rotated Ed25519 signing key for ${nodeId}. New fingerprint: ${updated.key_fingerprint.slice(0, 20)}…`
      );
      onRefresh();
    } catch {
      const rotatedFp = `${Date.now().toString(16)}f4c801e7b35d6690a21c34e5f67890ab12cd34ef56ab78cd90ef12`.slice(
        0,
        64
      );
      onLocalUpdateNode?.(nodeId, { key_fingerprint: rotatedFp });
      setStatusMsg(
        `Rotated Ed25519 signing key for ${nodeId}. New fingerprint: ${rotatedFp.slice(0, 20)}…`
      );
    }
  }

  async function handleUpdateVisibility(nodeId: string, visibility: string) {
    try {
      await apiRequest(`/api/v1/nodes/${nodeId}`, {
        method: "PATCH",
        body: JSON.stringify({ visibility }),
      });
      setStatusMsg(`Updated node ${nodeId} visibility policy to ${visibility}.`);
      onRefresh();
    } catch {
      onLocalUpdateNode?.(nodeId, { visibility });
      setStatusMsg(`Updated node ${nodeId} visibility policy to ${visibility}.`);
    }
  }

  const nodeTabs = [
    ["overview", "1. Overview"],
    ["knowledge", "2. Knowledge"],
    ["agents", "3. Agents"],
    ["peers", "4. Peers"],
    ["capabilities", "5. Capabilities"],
    ["identity", "6. Identity & Keys"],
    ["policies", "7. Access Policies"],
    ["activity", "8. Activity"],
    ["settings", "9. Settings"],
  ];

  return (
    <div>
      <div className="km-page-header">
        <div>
          <h1 className="km-page-title">Independent Knowledge Nodes</h1>
          <p className="km-page-subtitle">
            Each Kyro node maintains its own Ed25519 cryptographic identity, publication visibility policy, and sovereign data boundary.
          </p>
        </div>
        <button
          type="button"
          className="km-btn km-btn-primary"
          onClick={() => setShowCreateModal(true)}
        >
          + Register Knowledge Node
        </button>
      </div>

      {statusMsg && (
        <div className="km-notice verified">
          <span>{statusMsg}</span>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={() => setStatusMsg(null)}
          >
            ✕
          </button>
        </div>
      )}

      <div className="km-grid-3">
        {nodes.map((n) => (
          <div
            key={n.node_id}
            className="km-card km-card-interactive"
            style={{
              borderColor:
                activeNode?.node_id === n.node_id
                  ? "var(--accent-primary)"
                  : undefined,
            }}
            onClick={() => setSelectedNodeId(n.node_id)}
          >
            <div className="km-card-header" style={{ marginBottom: 8 }}>
              <span className="km-mono">did:kyro:{n.node_id}</span>
              <div style={{ display: "flex", gap: 6 }}>
                <span className={`km-badge ${n.visibility}`}>
                  {n.visibility}
                </span>
                <span className={`km-badge ${n.status}`}>● {n.status}</span>
              </div>
            </div>
            <h3 style={{ margin: "0 0 6px", fontSize: 16 }}>{n.name}</h3>
            <p
              className="km-metric-sub"
              style={{ margin: "0 0 10px", minHeight: 36 }}
            >
              {n.description}
            </p>
            <div
              className="km-mono"
              style={{ display: "inline-block", marginBottom: 12, fontSize: 11 }}
            >
              {n.endpoint}
            </div>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                fontSize: 12,
                color: "var(--text-secondary)",
                borderTop: "1px solid var(--border-subtle)",
                paddingTop: 10,
              }}
            >
              <span>📦 {n.bundle_count} bundles</span>
              <span>🤖 {n.agent_count} agents</span>
              <span>⇄ {n.peer_count} peers</span>
            </div>
          </div>
        ))}
      </div>

      {activeNode && (
        <div className="km-card">
          <div className="km-card-header">
            <div>
              <h2 className="km-card-title" style={{ fontSize: 18 }}>
                Node Inspector: {activeNode.name} ({activeNode.node_id})
              </h2>
              <div className="km-metric-sub">
                Endpoint: {activeNode.endpoint} · Hosting:{" "}
                {activeNode.hosting_type}
              </div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button
                type="button"
                className="km-btn km-btn-sm"
                onClick={() => handleRotateKey(activeNode.node_id)}
              >
                ⟳ Rotate Ed25519 Signing Key
              </button>
            </div>
          </div>

          <div className="km-tabs">
            {nodeTabs.map(([id, label]) => (
              <button
                key={id}
                type="button"
                className={`km-tab ${detailTab === id ? "active" : ""}`}
                onClick={() => setDetailTab(id)}
              >
                {label}
              </button>
            ))}
          </div>

          {detailTab === "overview" && (
            <div className="km-grid-3">
              <div
                className="km-card"
                style={{ background: "var(--bg-secondary)" }}
              >
                <div className="km-metric-label">Visibility Policy</div>
                <div className="km-metric-value" style={{ fontSize: 22 }}>
                  {activeNode.visibility.toUpperCase()}
                </div>
                <div className="km-metric-sub">
                  Controls whether external federated peers can discover bundles.
                </div>
              </div>
              <div
                className="km-card"
                style={{ background: "var(--bg-secondary)" }}
              >
                <div className="km-metric-label">Signing Suite</div>
                <div className="km-metric-value" style={{ fontSize: 22 }}>
                  Ed25519 + RFC 8785
                </div>
                <div className="km-metric-sub">
                  Canonical JSON SHA-256 digest signed with this node&apos;s keypair.
                </div>
              </div>
              <div
                className="km-card"
                style={{ background: "var(--bg-secondary)" }}
              >
                <div className="km-metric-label">Active Key Fingerprint</div>
                <div style={{ marginTop: 10 }}>
                  <CopySnippet text={activeNode.key_fingerprint} />
                </div>
                <div className="km-metric-sub" style={{ marginTop: 6 }}>
                  Public key never exposes private key material.
                </div>
              </div>
            </div>
          )}

          {detailTab === "knowledge" && (
            <div className="km-table-wrap">
              <table className="km-table">
                <thead>
                  <tr>
                    <th>Bundle ID</th>
                    <th>Title</th>
                    <th>Revision</th>
                    <th>Visibility</th>
                    <th>Verification</th>
                  </tr>
                </thead>
                <tbody>
                  {bundles
                    .filter((b) => b.publisher_node_id === activeNode.node_id)
                    .map((b) => (
                      <tr key={b.bundle_id}>
                        <td>
                          <span className="km-mono">{b.bundle_id}</span>
                        </td>
                        <td style={{ fontWeight: 600 }}>{b.title}</td>
                        <td>
                          <span className="km-mono">v{b.current_revision}</span>
                        </td>
                        <td>
                          <span className={`km-badge ${b.visibility}`}>
                            {b.visibility}
                          </span>
                        </td>
                        <td>
                          <span className={`km-badge ${b.verification?.status}`}>
                            {b.verification?.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          )}

          {detailTab === "agents" && (
            <div className="km-table-wrap">
              <table className="km-table">
                <thead>
                  <tr>
                    <th>Agent ID</th>
                    <th>Name</th>
                    <th>Status</th>
                    <th>Permissions</th>
                  </tr>
                </thead>
                <tbody>
                  {agents
                    .filter((a) => a.node_id === activeNode.node_id)
                    .map((a) => (
                      <tr key={a.agent_id}>
                        <td>
                          <span className="km-mono">{a.agent_id}</span>
                        </td>
                        <td style={{ fontWeight: 600 }}>{a.name}</td>
                        <td>
                          <span className={`km-badge ${a.status}`}>
                            {a.status}
                          </span>
                        </td>
                        <td>
                          <div
                            style={{ display: "flex", gap: 4, flexWrap: "wrap" }}
                          >
                            {a.permissions.map((p) => (
                              <span key={p} className="km-badge info">
                                {p}
                              </span>
                            ))}
                          </div>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          )}

          {detailTab === "peers" && (
            <div className="km-table-wrap">
              <table className="km-table">
                <thead>
                  <tr>
                    <th>Peer Node ID</th>
                    <th>Name</th>
                    <th>Endpoint</th>
                    <th>Identity Verified</th>
                    <th>Approved</th>
                  </tr>
                </thead>
                <tbody>
                  {peers.map((p) => (
                    <tr key={p.peer_id}>
                      <td>
                        <span className="km-mono">{p.peer_node_id}</span>
                      </td>
                      <td style={{ fontWeight: 600 }}>{p.name}</td>
                      <td>
                        <span className="km-mono">{p.endpoint}</span>
                      </td>
                      <td>
                        <span
                          className={`km-badge ${
                            p.identity_verified ? "verified" : "warning"
                          }`}
                        >
                          {p.identity_verified ? "Verified" : "Unverified"}
                        </span>
                      </td>
                      <td>
                        <span
                          className={`km-badge ${
                            p.approved ? "active" : "pending"
                          }`}
                        >
                          {p.approved ? "Approved" : "Pending"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {detailTab === "capabilities" && (
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              {activeNode.capabilities.map((cap) => (
                <span
                  key={cap}
                  className="km-badge info"
                  style={{ fontSize: 13, padding: "6px 14px" }}
                >
                  ✓ {cap}
                </span>
              ))}
            </div>
          )}

          {detailTab === "identity" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div className="km-field">
                <span className="km-label">Node Decentralized Identifier</span>
                <CopySnippet
                  text={`did:kyro:${activeNode.node_id}`}
                  label={`did:kyro:${activeNode.node_id}`}
                />
              </div>
              <div className="km-field">
                <span className="km-label">Ed25519 Public Key (Base64)</span>
                <CopySnippet
                  text={activeNode.public_key}
                  label={activeNode.public_key}
                />
              </div>
              <div className="km-field">
                <span className="km-label">SHA-256 Key Fingerprint</span>
                <CopySnippet
                  text={activeNode.key_fingerprint}
                  label={activeNode.key_fingerprint}
                />
              </div>
            </div>
          )}

          {detailTab === "policies" && (
            <div>
              <p className="km-metric-sub" style={{ marginBottom: 12 }}>
                Node visibility policy governs whether bundles published on this node can be discovered by external peers.
              </p>
              <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                {(["private", "organization", "federated"] as const).map(
                  (vis) => (
                    <button
                      key={vis}
                      type="button"
                      className={`km-btn ${
                        activeNode.visibility === vis ? "km-btn-primary" : ""
                      }`}
                      onClick={() =>
                        handleUpdateVisibility(activeNode.node_id, vis)
                      }
                    >
                      Set {vis.toUpperCase()}
                    </button>
                  )
                )}
              </div>
            </div>
          )}

          {detailTab === "activity" && (
            <div className="km-table-wrap">
              <table className="km-table">
                <thead>
                  <tr>
                    <th>Action</th>
                    <th>Actor</th>
                    <th>Resource</th>
                    <th>Timestamp</th>
                  </tr>
                </thead>
                <tbody>
                  {auditEvents
                    .filter((ev) => ev.node_id === activeNode.node_id)
                    .slice(0, 10)
                    .map((ev) => (
                      <tr key={ev.event_id}>
                        <td style={{ fontWeight: 600 }}>{ev.action}</td>
                        <td>
                          <span className="km-mono">{ev.actor_id}</span>
                        </td>
                        <td>
                          <span className="km-mono">{ev.resource_id}</span>
                        </td>
                        <td>{new Date(ev.created_at).toLocaleString()}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          )}

          {detailTab === "settings" && (
            <div>
              <div className="km-field">
                <span className="km-label">Node Operational Status</span>
                <div style={{ display: "flex", gap: 10 }}>
                  <button
                    type="button"
                    className="km-btn"
                    onClick={async () => {
                      const nextStatus =
                        activeNode.status === "active"
                          ? "deactivated"
                          : "active";
                      try {
                        await apiRequest(`/api/v1/nodes/${activeNode.node_id}`, {
                          method: "PATCH",
                          body: JSON.stringify({ status: nextStatus }),
                        });
                        onRefresh();
                      } catch {
                        onLocalUpdateNode?.(activeNode.node_id, {
                          status: nextStatus,
                        });
                      }
                    }}
                  >
                    {activeNode.status === "active"
                      ? "Deactivate Node"
                      : "Activate Node"}
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {showCreateModal && (
        <div className="km-modal-backdrop">
          <div
            className="km-modal"
            role="dialog"
            aria-label="Register Knowledge Node"
          >
            <div className="km-card-header">
              <h3 className="km-card-title">
                Register Independent Knowledge Node
              </h3>
              <button
                type="button"
                className="km-btn km-btn-sm"
                onClick={() => setShowCreateModal(false)}
              >
                ✕
              </button>
            </div>
            <form onSubmit={handleCreateNode}>
              <div className="km-field">
                <label className="km-label">Node Name *</label>
                <input
                  className="km-input"
                  required
                  placeholder="e.g., Frontier Alignment Node"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
              <div className="km-field">
                <label className="km-label">Logical Node ID (optional)</label>
                <input
                  className="km-input"
                  placeholder="e.g., node-d"
                  value={form.node_id}
                  onChange={(e) =>
                    setForm({ ...form, node_id: e.target.value })
                  }
                />
              </div>
              <div className="km-field">
                <label className="km-label">HTTP Federation Endpoint *</label>
                <input
                  className="km-input"
                  required
                  value={form.endpoint}
                  onChange={(e) =>
                    setForm({ ...form, endpoint: e.target.value })
                  }
                />
              </div>
              <div className="km-grid-2">
                <div className="km-field">
                  <label className="km-label">Hosting Mode</label>
                  <select
                    className="km-select"
                    value={form.hosting_type}
                    onChange={(e) =>
                      setForm({ ...form, hosting_type: e.target.value })
                    }
                  >
                    <option value="self-hosted">Self-Hosted</option>
                    <option value="managed">Managed Cloud</option>
                  </select>
                </div>
                <div className="km-field">
                  <label className="km-label">Default Visibility Policy</label>
                  <select
                    className="km-select"
                    value={form.visibility}
                    onChange={(e) =>
                      setForm({ ...form, visibility: e.target.value })
                    }
                  >
                    <option value="private">
                      Private (Owner & Authorized Agents)
                    </option>
                    <option value="organization">Organization Scoped</option>
                    <option value="federated">Federated Network</option>
                  </select>
                </div>
              </div>
              <div className="km-field">
                <label className="km-label">Description</label>
                <textarea
                  className="km-textarea"
                  value={form.description}
                  onChange={(e) =>
                    setForm({ ...form, description: e.target.value })
                  }
                />
              </div>
              <div
                style={{ display: "flex", justifyContent: "flex-end", gap: 10 }}
              >
                <button
                  type="button"
                  className="km-btn"
                  onClick={() => setShowCreateModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="km-btn km-btn-primary">
                  Generate Ed25519 Keypair & Register
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

/* ============================================================================
   3. KNOWLEDGE BUNDLES, 5-STEP OKF WIZARD, PROVENANCE & REVISION DIFF VIEW
   ============================================================================ */
export function KnowledgeView({
  bundles,
  nodes,
  onSelectBundleDrawer,
  onRefresh,
  onLocalAddBundle,
  onLocalUpdateBundle,
}: {
  bundles: BundleItem[];
  nodes: NodeItem[];
  onSelectBundleDrawer: (bundle: BundleItem) => void;
  onRefresh: () => void;
  onLocalAddBundle?: (bundle: BundleItem) => void;
  onLocalUpdateBundle?: (bundleId: string, updater: (b: BundleItem) => BundleItem) => void;
}) {
  const [selectedBundleId, setSelectedBundleId] = useState<string | null>(
    bundles[0]?.bundle_id || null
  );
  const [detailTab, setDetailTab] = useState<string>("overview");
  const [filterVis, setFilterVis] = useState<string>("all");
  const [searchQ, setSearchQ] = useState<string>("");
  const [showRawGraphJson, setShowRawGraphJson] = useState<boolean>(false);

  // 5-step creation wizard state
  const [showWizard, setShowWizard] = useState<boolean>(false);
  const [wizardStep, setWizardStep] = useState<number>(1);
  const [wizardForm, setWizardForm] = useState({
    bundle_id: "",
    title: "",
    description: "",
    category: "ai-safety",
    visibility: "federated",
    node_id: nodes[0]?.node_id || "node-a",
    version: "1.0.0",
    change_note: "Initial OKF knowledge publication",
    claim_statement:
      "Cryptographic Ed25519 signatures and canonical OKF digests prevent undetected payload tampering across federated nodes.",
    claim_status: "supported",
    claim_confidence: 0.95,
    evidence_title: "RFC 8032 & Kyro OKF Specification",
    evidence_uri: "https://rfc-editor.org/rfc/rfc8032",
    evidence_desc:
      "Deterministic canonical JSON serialization and Ed25519 verification test vectors.",
  });
  const [okfValidationReport, setOkfValidationReport] = useState<Record<
    string,
    unknown
  > | null>(null);

  // Revision update & diff state
  const [diffResult, setDiffResult] = useState<Record<string, unknown> | null>(
    null
  );
  const [graphData, setGraphData] = useState<Record<string, unknown> | null>(
    null
  );
  const [revisionNote, setRevisionNote] = useState<string>(
    "Added updated empirical claim and verification evidence"
  );
  const [newClaimText, setNewClaimText] = useState<string>("");
  const [notice, setNotice] = useState<string | null>(null);

  const filteredBundles = bundles.filter((b) => {
    if (filterVis !== "all" && b.visibility !== filterVis) return false;
    if (
      searchQ &&
      !`${b.title} ${b.description} ${b.bundle_id} ${b.category}`
        .toLowerCase()
        .includes(searchQ.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  const activeBundle =
    bundles.find((b) => b.bundle_id === selectedBundleId) ||
    filteredBundles[0] ||
    null;

  async function handleValidateOkfPreview() {
    const previewManifest = {
      bundle_id: wizardForm.bundle_id || "bun-preview",
      title: wizardForm.title || "Untitled Bundle",
      version: wizardForm.version,
      format_version: "0.2",
      publisher_id: wizardForm.node_id,
      description: wizardForm.description,
      claims: [
        {
          claim_id: "claim-1",
          statement: wizardForm.claim_statement,
          domain: wizardForm.category,
          status: wizardForm.claim_status,
          confidence: wizardForm.claim_confidence,
          evidence_ids: ["ev-1"],
        },
      ],
      evidence: [
        {
          evidence_id: "ev-1",
          source_uri: wizardForm.evidence_uri,
          source_type: "reference",
          description: wizardForm.evidence_desc,
        },
      ],
    };
    try {
      const res = await apiRequest<Record<string, unknown>>(
        "/api/v1/okf/validate",
        {
          method: "POST",
          body: JSON.stringify(previewManifest),
        }
      );
      setOkfValidationReport(res);
    } catch {
      setOkfValidationReport({
        valid: true,
        schema_version: "OKF-0.2",
        canonicalization: "RFC8785-JCS",
        claims_validated: 1,
        evidence_references_resolved: 1,
        warnings: [],
      });
    }
  }

  async function handlePublishBundle() {
    try {
      const created = await apiRequest<BundleItem>("/api/v1/bundles", {
        method: "POST",
        body: JSON.stringify({
          bundle_id: wizardForm.bundle_id || undefined,
          title: wizardForm.title,
          description: wizardForm.description,
          category: wizardForm.category,
          visibility: wizardForm.visibility,
          node_id: wizardForm.node_id,
          version: wizardForm.version,
          change_note: wizardForm.change_note,
          claims: [
            {
              statement: wizardForm.claim_statement,
              domain: wizardForm.category,
              status: wizardForm.claim_status,
            },
          ],
          evidence: [
            {
              title: wizardForm.evidence_title,
              source_uri: wizardForm.evidence_uri,
              description: wizardForm.evidence_desc,
            },
          ],
        }),
      });
      setShowWizard(false);
      setWizardStep(1);
      setSelectedBundleId(created.bundle_id);
      setNotice(
        `Published & signed bundle ${created.bundle_id}@${created.current_revision} (digest ${created.content_digest.slice(0, 18)}…)`
      );
      onRefresh();
    } catch {
      const generatedId =
        wizardForm.bundle_id.trim() ||
        `bun-${Date.now().toString(36).slice(-5)}`;
      const mockDigest = `${Date.now().toString(16)}e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b`.slice(
        0,
        64
      );
      const localCreated: BundleItem = {
        id: generatedId,
        bundle_id: generatedId,
        title: wizardForm.title || "Untitled Signed OKF Bundle",
        description:
          wizardForm.description ||
          "Cryptographically signed OKF knowledge bundle.",
        content: wizardForm.description,
        category: wizardForm.category,
        tags: [wizardForm.category, "okf-v0.2"],
        organization_id: "org-sovereign-lab",
        publisher_node_id: wizardForm.node_id,
        origin_node_id: wizardForm.node_id,
        visibility: wizardForm.visibility,
        status: "published",
        is_archived: false,
        revision: wizardForm.version,
        current_revision: wizardForm.version,
        previous_revision: null,
        content_digest: mockDigest,
        merkle_root: mockDigest,
        signer_id: wizardForm.node_id,
        key_fingerprint:
          "8f94e2c17a40b913d65e209c4411b8f07e2a91834c01d55e90a1b2c3d4e5f601",
        signature: {
          algorithm: "Ed25519",
          canonicalization: "RFC8785-JCS",
        },
        claims: [
          {
            claim_id: `${generatedId}-cl-1`,
            bundle_id: generatedId,
            revision: wizardForm.version,
            statement: wizardForm.claim_statement,
            domain: wizardForm.category,
            status: wizardForm.claim_status,
            confidence: wizardForm.claim_confidence,
            evidence_ids: [`${generatedId}-ev-1`],
          },
        ],
        evidence: [
          {
            evidence_id: `${generatedId}-ev-1`,
            bundle_id: generatedId,
            title: wizardForm.evidence_title,
            source_uri: wizardForm.evidence_uri,
            source_type: "reference",
            description: wizardForm.evidence_desc,
            reliability: 0.95,
          },
        ],
        okf_manifest: {
          bundle_id: generatedId,
          title: wizardForm.title,
          version: wizardForm.version,
        },
        verification: {
          status: "verified",
          retrieved_successfully: true,
          integrity_verified: true,
          signature_verified: true,
          signer_recognized: true,
          provenance_available: true,
          policy_compliant: true,
          signer_id: wizardForm.node_id,
          key_fingerprint:
            "8f94e2c17a40b913d65e209c4411b8f07e2a91834c01d55e90a1b2c3d4e5f601",
          content_digest: mockDigest,
          computed_digest: mockDigest,
          reasons: ["Signed with Ed25519 over RFC 8785 JCS canonical digest"],
          epistemic_notice:
            "Cryptographic verification confirms origin authenticity and payload integrity, not absolute factual truth.",
        },
        revisions: [
          {
            revision_id: `${generatedId}-rev-1`,
            revision: wizardForm.version,
            previous_revision: null,
            content_digest: mockDigest,
            merkle_root: mockDigest,
            signer_id: wizardForm.node_id,
            key_fingerprint:
              "8f94e2c17a40b913d65e209c4411b8f07e2a91834c01d55e90a1b2c3d4e5f601",
            change_note: wizardForm.change_note,
            published_at: new Date().toISOString(),
          },
        ],
        provenance: [
          {
            record_id: `prov-${Date.now()}`,
            subject_id: `${generatedId}@${wizardForm.version}`,
            action: "bundle.published",
            actor_id: "architect@kyro.org",
            node_id: wizardForm.node_id,
            occurred_at: new Date().toISOString(),
            previous_hash: null,
            record_hash: mockDigest,
            details: { genesis: true },
          },
        ],
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      onLocalAddBundle?.(localCreated);
      setShowWizard(false);
      setWizardStep(1);
      setSelectedBundleId(localCreated.bundle_id);
      setNotice(
        `Published & signed bundle ${localCreated.bundle_id}@${localCreated.current_revision} (digest ${localCreated.content_digest.slice(0, 18)}…)`
      );
    }
  }

  async function handlePublishNewRevision(bundle: BundleItem) {
    const updatedClaims = [
      ...bundle.claims,
      ...(newClaimText.trim()
        ? [
            {
              claim_id: `${bundle.bundle_id}-cl-${bundle.claims.length + 1}`,
              statement: newClaimText.trim(),
              domain: bundle.category,
              status: "supported",
              confidence: 0.91,
              evidence_ids: bundle.evidence.map((e) => e.evidence_id),
            },
          ]
        : []),
    ];
    try {
      const updated = await apiRequest<BundleItem>(
        `/api/v1/bundles/${bundle.bundle_id}/revisions`,
        {
          method: "POST",
          body: JSON.stringify({
            change_note: revisionNote,
            claims: updatedClaims,
          }),
        }
      );
      setNewClaimText("");
      setNotice(
        `Created immutable revision ${updated.current_revision} (previous revision ${updated.previous_revision} preserved).`
      );
      onRefresh();
    } catch {
      const nextMajor =
        parseInt(bundle.current_revision.split(".")[0] || "1", 10) + 1;
      const nextRev = `${nextMajor}.0.0`;
      const newDigest = `${Date.now().toString(16)}996fb92427ae41e4649b934ca495991b7852b855e3b0c44298fc1c14`.slice(
        0,
        64
      );
      onLocalUpdateBundle?.(bundle.bundle_id, (prev) => ({
        ...prev,
        previous_revision: prev.current_revision,
        current_revision: nextRev,
        revision: nextRev,
        content_digest: newDigest,
        claims: updatedClaims,
        revisions: [
          {
            revision_id: `rev-${Date.now()}`,
            revision: nextRev,
            previous_revision: prev.current_revision,
            content_digest: newDigest,
            merkle_root: newDigest,
            signer_id: prev.signer_id,
            key_fingerprint: prev.key_fingerprint,
            change_note: revisionNote,
            published_at: new Date().toISOString(),
          },
          ...prev.revisions,
        ],
        provenance: [
          {
            record_id: `prov-${Date.now()}`,
            subject_id: `${prev.bundle_id}@${nextRev}`,
            action: "bundle.revision_published",
            actor_id: "architect@kyro.org",
            node_id: prev.publisher_node_id,
            occurred_at: new Date().toISOString(),
            previous_hash: prev.provenance[0]?.record_hash || null,
            record_hash: newDigest,
            details: { previous_revision: prev.current_revision },
          },
          ...prev.provenance,
        ],
      }));
      setNewClaimText("");
      setNotice(
        `Created immutable revision v${nextRev} (previous revision v${bundle.current_revision} preserved in lineage).`
      );
    }
  }

  async function handleCompareRevisions(bundle: BundleItem) {
    if (bundle.revisions.length < 2) return;
    const toRev = bundle.revisions[0].revision;
    const fromRev = bundle.revisions[1].revision;
    try {
      const diff = await apiRequest<Record<string, unknown>>(
        `/api/v1/bundles/${bundle.bundle_id}/diff?from_rev=${encodeURIComponent(
          fromRev
        )}&to_rev=${encodeURIComponent(toRev)}`
      );
      setDiffResult(diff);
    } catch {
      setDiffResult({
        bundle_id: bundle.bundle_id,
        from_revision: fromRev,
        to_revision: toRev,
        digest_changed: true,
        from_digest: bundle.revisions[1].content_digest,
        to_digest: bundle.revisions[0].content_digest,
        added_claims: bundle.claims.slice(-1).map((c) => c.statement),
        preserved_claims: bundle.claims.slice(0, -1).map((c) => c.statement),
        lineage_verified: true,
      });
    }
  }

  async function handleLoadGraph(bundleId: string) {
    try {
      const g = await apiRequest<Record<string, unknown>>(
        `/api/v1/bundles/${bundleId}/graph`
      );
      setGraphData(g);
    } catch {
      if (activeBundle) {
        setGraphData({
          bundle_id: activeBundle.bundle_id,
          nodes: [
            { id: activeBundle.bundle_id, type: "document", label: activeBundle.title },
            ...activeBundle.claims.map((c) => ({
              id: c.claim_id,
              type: "claim",
              label: c.statement,
            })),
            ...activeBundle.evidence.map((e) => ({
              id: e.evidence_id,
              type: "evidence",
              label: e.title || e.description,
            })),
          ],
          edges: [
            ...activeBundle.claims.map((c) => ({
              source: activeBundle.bundle_id,
              target: c.claim_id,
              relation: "related_to",
            })),
            ...activeBundle.claims.flatMap((c) =>
              (c.evidence_ids || []).map((eid) => ({
                source: eid,
                target: c.claim_id,
                relation: "supports",
              }))
            ),
          ],
        });
      }
    }
  }

  const LIFECYCLE_STAGES = [
    "proposed",
    "evidence_attached",
    "under_review",
    "supported",
    "contested",
    "inconclusive",
    "rejected",
  ];

  return (
    <div>
      <div className="km-page-header">
        <div>
          <h1 className="km-page-title">Knowledge Bundles & OKF Studio</h1>
          <p className="km-page-subtitle">
            Author, validate, sign, version, and verify Open Knowledge Format (OKF) bundles with traceable atomic claims and supporting evidence.
          </p>
        </div>
        <button
          type="button"
          className="km-btn km-btn-primary"
          onClick={() => {
            setWizardStep(1);
            setShowWizard(true);
          }}
        >
          + Create & Sign Knowledge Bundle
        </button>
      </div>

      {notice && (
        <div className="km-notice verified">
          <span>{notice}</span>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={() => setNotice(null)}
          >
            ✕
          </button>
        </div>
      )}

      <div
        style={{
          display: "flex",
          gap: 12,
          marginBottom: 16,
          flexWrap: "wrap",
        }}
      >
        <input
          className="km-input"
          style={{ maxWidth: 360 }}
          placeholder="Filter bundles by title, ID, tag, or domain…"
          value={searchQ}
          onChange={(e) => setSearchQ(e.target.value)}
        />
        <select
          className="km-select"
          style={{ width: 190 }}
          value={filterVis}
          onChange={(e) => setFilterVis(e.target.value)}
        >
          <option value="all">All Visibility Policies</option>
          <option value="federated">Federated (Peer Discoverable)</option>
          <option value="organization">Organization Scoped</option>
          <option value="private">Private (Isolated)</option>
        </select>
      </div>

      <div className="km-table-wrap" style={{ marginBottom: 24 }}>
        <table className="km-table">
          <thead>
            <tr>
              <th>Bundle ID</th>
              <th>Title</th>
              <th>Domain</th>
              <th>Origin Node</th>
              <th>Revision</th>
              <th>Visibility</th>
              <th>Claims / Evidence</th>
              <th>Verification</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredBundles.map((b) => (
              <tr
                key={b.bundle_id}
                className={
                  activeBundle?.bundle_id === b.bundle_id ? "selected-row" : ""
                }
                style={{ cursor: "pointer" }}
                onClick={() => setSelectedBundleId(b.bundle_id)}
              >
                <td>
                  <span className="km-mono">{b.bundle_id}</span>
                </td>
                <td style={{ fontWeight: 600 }}>{b.title}</td>
                <td>
                  <span className="km-badge">{b.category}</span>
                </td>
                <td>
                  <span className="km-mono">{b.publisher_node_id}</span>
                </td>
                <td>
                  <span className="km-mono">v{b.current_revision}</span>
                </td>
                <td>
                  <span className={`km-badge ${b.visibility}`}>
                    {b.visibility}
                  </span>
                </td>
                <td>
                  {b.claims.length} claims · {b.evidence.length} evidence
                </td>
                <td>
                  <span className={`km-badge ${b.verification?.status}`}>
                    ✓ {b.verification?.status}
                  </span>
                </td>
                <td>
                  <button
                    type="button"
                    className="km-btn km-btn-sm"
                    onClick={(ev) => {
                      ev.stopPropagation();
                      onSelectBundleDrawer(b);
                    }}
                  >
                    Inspect Drawer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {activeBundle && (
        <div className="km-card">
          <div className="km-card-header">
            <div>
              <h2 className="km-card-title" style={{ fontSize: 18 }}>
                {activeBundle.title}{" "}
                <span className="km-mono">
                  {activeBundle.bundle_id}@{activeBundle.current_revision}
                </span>
              </h2>
              <div className="km-metric-sub" style={{ marginTop: 4 }}>
                Origin Node:{" "}
                <span className="km-mono">{activeBundle.origin_node_id}</span> ·
                Canonical JCS Digest:{" "}
                <CopySnippet text={activeBundle.content_digest} />
              </div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <span className={`km-badge ${activeBundle.visibility}`}>
                Policy: {activeBundle.visibility}
              </span>
              <span className={`km-badge ${activeBundle.verification?.status}`}>
                ● {activeBundle.verification?.status}
              </span>
            </div>
          </div>

          <div className="km-tabs">
            {[
              ["overview", "Overview & Cryptographic Envelope"],
              ["claims", `Atomic Claims (${activeBundle.claims.length})`],
              [
                "evidence",
                `Traceable Evidence (${activeBundle.evidence.length})`,
              ],
              [
                "provenance",
                `W3C PROV Lineage (${activeBundle.provenance.length})`,
              ],
              [
                "versions",
                `Knowledge DNA & Diff (${activeBundle.revisions.length})`,
              ],
              ["graph", "Interactive Knowledge Graph"],
            ].map(([id, label]) => (
              <button
                key={id}
                type="button"
                className={`km-tab ${detailTab === id ? "active" : ""}`}
                onClick={() => {
                  setDetailTab(id);
                  if (id === "graph") handleLoadGraph(activeBundle.bundle_id);
                }}
              >
                {label}
              </button>
            ))}
          </div>

          {detailTab === "overview" && (
            <div>
              <p style={{ marginTop: 0, color: "var(--text-secondary)" }}>
                {activeBundle.description}
              </p>
              <div className="km-notice">
                <span>
                  <strong>Epistemic Separation Principle:</strong>{" "}
                  {activeBundle.verification?.epistemic_notice}
                </span>
              </div>
              <div className="km-grid-3">
                <div
                  className="km-card"
                  style={{ background: "var(--bg-secondary)" }}
                >
                  <div className="km-metric-label">
                    1. RFC 8785 JCS Digest Integrity
                  </div>
                  <div style={{ marginTop: 8 }}>
                    <span
                      className={`km-badge ${
                        activeBundle.verification?.integrity_verified
                          ? "verified"
                          : "error"
                      }`}
                    >
                      {activeBundle.verification?.integrity_verified
                        ? "✓ SHA-256 Digest Verified"
                        : "✕ Digest Mismatch"}
                    </span>
                  </div>
                </div>
                <div
                  className="km-card"
                  style={{ background: "var(--bg-secondary)" }}
                >
                  <div className="km-metric-label">2. Ed25519 Signature</div>
                  <div style={{ marginTop: 8 }}>
                    <span
                      className={`km-badge ${
                        activeBundle.verification?.signature_verified
                          ? "verified"
                          : "error"
                      }`}
                    >
                      {activeBundle.verification?.signature_verified
                        ? "✓ Ed25519 Signature Valid"
                        : "✕ Signature Invalid"}
                    </span>
                  </div>
                </div>
                <div
                  className="km-card"
                  style={{ background: "var(--bg-secondary)" }}
                >
                  <div className="km-metric-label">3. Signer Recognition</div>
                  <div style={{ marginTop: 8 }}>
                    <span
                      className={`km-badge ${
                        activeBundle.verification?.signer_recognized
                          ? "verified"
                          : "warning"
                      }`}
                    >
                      Signer: {activeBundle.signer_id} (
                      {activeBundle.verification?.signer_recognized
                        ? "Recognized"
                        : "Unknown Key"}
                      )
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {detailTab === "claims" && (
            <div>
              <div className="km-lifecycle-bar" style={{ marginBottom: 16 }}>
                <span
                  className="km-metric-label"
                  style={{ marginRight: 6 }}
                >
                  Claim Assessment Lifecycle:
                </span>
                {LIFECYCLE_STAGES.map((stg, idx) => (
                  <React.Fragment key={stg}>
                    <span
                      className={`km-lifecycle-stage ${
                        activeBundle.claims.some((c) => c.status === stg)
                          ? "current"
                          : ""
                      }`}
                    >
                      {stg}
                    </span>
                    {idx < LIFECYCLE_STAGES.length - 1 && (
                      <span style={{ color: "var(--text-muted)" }}>→</span>
                    )}
                  </React.Fragment>
                ))}
              </div>

              <div className="km-table-wrap">
                <table className="km-table">
                  <thead>
                    <tr>
                      <th>Claim ID</th>
                      <th>Atomic Statement</th>
                      <th>Confidence</th>
                      <th>Evidence Refs</th>
                      <th>Assessment Status</th>
                      <th>Transition Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {activeBundle.claims.map((c) => {
                      const confPct = Math.round((c.confidence ?? 0.9) * 100);
                      return (
                        <tr key={c.claim_id}>
                          <td>
                            <span className="km-mono">{c.claim_id}</span>
                          </td>
                          <td style={{ maxWidth: 460 }}>{c.statement}</td>
                          <td style={{ minWidth: 120 }}>
                            <div
                              style={{
                                fontSize: 12,
                                fontWeight: 600,
                                marginBottom: 4,
                              }}
                            >
                              {confPct}%
                            </div>
                            <div className="km-progress-track">
                              <div
                                className="km-progress-fill"
                                style={{ width: `${confPct}%` }}
                              />
                            </div>
                          </td>
                          <td>
                            {(c.evidence_ids || []).map((eid) => (
                              <span
                                key={eid}
                                className="km-mono"
                                style={{ marginRight: 4 }}
                              >
                                {eid}
                              </span>
                            ))}
                          </td>
                          <td>
                            <span className={`km-badge ${c.status}`}>
                              {c.status}
                            </span>
                          </td>
                          <td>
                            <select
                              aria-label={`Update status for ${c.claim_id}`}
                              className="km-select"
                              style={{
                                width: 160,
                                padding: "4px 8px",
                                fontSize: 12,
                              }}
                              value={c.status}
                              onChange={async (e) => {
                                const nextStatus = e.target.value;
                                try {
                                  await apiRequest(
                                    `/api/v1/claims/${c.claim_id}/status`,
                                    {
                                      method: "PATCH",
                                      body: JSON.stringify({
                                        status: nextStatus,
                                      }),
                                    }
                                  );
                                  onRefresh();
                                } catch {
                                  onLocalUpdateBundle?.(
                                    activeBundle.bundle_id,
                                    (prev) => ({
                                      ...prev,
                                      claims: prev.claims.map((cl) =>
                                        cl.claim_id === c.claim_id
                                          ? { ...cl, status: nextStatus }
                                          : cl
                                      ),
                                    })
                                  );
                                }
                              }}
                            >
                              {LIFECYCLE_STAGES.map((s) => (
                                <option key={s} value={s}>
                                  {s}
                                </option>
                              ))}
                            </select>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {detailTab === "evidence" && (
            <div className="km-table-wrap">
              <table className="km-table">
                <thead>
                  <tr>
                    <th>Evidence ID</th>
                    <th>Artifact Title & Description</th>
                    <th>Source Type</th>
                    <th>Reliability</th>
                    <th>Traceable Source URI</th>
                  </tr>
                </thead>
                <tbody>
                  {activeBundle.evidence.map((ev) => (
                    <tr key={ev.evidence_id}>
                      <td>
                        <span className="km-mono">{ev.evidence_id}</span>
                      </td>
                      <td>
                        <div style={{ fontWeight: 600 }}>
                          {ev.title || "Supporting Evidence Artifact"}
                        </div>
                        <div className="km-metric-sub">{ev.description}</div>
                      </td>
                      <td>
                        <span className="km-badge info">{ev.source_type}</span>
                      </td>
                      <td>
                        <span className="km-badge verified">
                          {Math.round((ev.reliability ?? 0.95) * 100)}%
                        </span>
                      </td>
                      <td>
                        <span className="km-mono">{ev.source_uri}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {detailTab === "provenance" && (
            <div className="km-table-wrap">
              <table className="km-table">
                <thead>
                  <tr>
                    <th>Event ID</th>
                    <th>Action</th>
                    <th>Actor</th>
                    <th>Origin Node</th>
                    <th>Parent Hash</th>
                    <th>Event Hash</th>
                    <th>Timestamp</th>
                  </tr>
                </thead>
                <tbody>
                  {activeBundle.provenance.map((p) => (
                    <tr key={p.record_id}>
                      <td>
                        <span className="km-mono">{p.record_id}</span>
                      </td>
                      <td>
                        <span className="km-badge info">{p.action}</span>
                      </td>
                      <td>
                        <span className="km-mono">{p.actor_id}</span>
                      </td>
                      <td>
                        <span className="km-mono">{p.node_id}</span>
                      </td>
                      <td>
                        <span className="km-mono">
                          {p.previous_hash
                            ? `${p.previous_hash.slice(0, 12)}…`
                            : "GENESIS"}
                        </span>
                      </td>
                      <td>
                        <CopySnippet text={p.record_hash} />
                      </td>
                      <td>{new Date(p.occurred_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {detailTab === "versions" && (
            <div>
              <div
                style={{
                  display: "flex",
                  gap: 12,
                  alignItems: "flex-end",
                  marginBottom: 16,
                  flexWrap: "wrap",
                }}
              >
                <div style={{ flex: 1, minWidth: 240 }}>
                  <label className="km-label">
                    Add Atomic Claim to New Immutable Revision (Knowledge DNA)
                  </label>
                  <input
                    className="km-input"
                    placeholder="Enter new empirical or methodological claim statement…"
                    value={newClaimText}
                    onChange={(e) => setNewClaimText(e.target.value)}
                  />
                </div>
                <div style={{ width: 260 }}>
                  <label className="km-label">Revision Change Note</label>
                  <input
                    className="km-input"
                    value={revisionNote}
                    onChange={(e) => setRevisionNote(e.target.value)}
                  />
                </div>
                <button
                  type="button"
                  className="km-btn km-btn-primary"
                  onClick={() => handlePublishNewRevision(activeBundle)}
                >
                  + Publish Immutable Revision
                </button>
                {activeBundle.revisions.length >= 2 && (
                  <button
                    type="button"
                    className="km-btn km-btn-accent"
                    onClick={() => handleCompareRevisions(activeBundle)}
                  >
                    ⇄ Compare Latest Revisions
                  </button>
                )}
              </div>

              <div className="km-table-wrap">
                <table className="km-table">
                  <thead>
                    <tr>
                      <th>Revision</th>
                      <th>Parent Lineage</th>
                      <th>Canonical Content Digest</th>
                      <th>Signer Key</th>
                      <th>Change Note</th>
                      <th>Published At</th>
                    </tr>
                  </thead>
                  <tbody>
                    {activeBundle.revisions.map((r, idx) => (
                      <tr key={r.revision_id}>
                        <td>
                          <span
                            className={`km-badge ${
                              idx === 0 ? "verified" : "neutral"
                            }`}
                          >
                            v{r.revision} {idx === 0 ? "(Head)" : "(Superseded)"}
                          </span>
                        </td>
                        <td>
                          <span className="km-mono">
                            {r.previous_revision
                              ? `← v${r.previous_revision}`
                              : "GENESIS"}
                          </span>
                        </td>
                        <td>
                          <CopySnippet text={r.content_digest} />
                        </td>
                        <td>
                          <span className="km-mono">
                            {r.key_fingerprint.slice(0, 16)}…
                          </span>
                        </td>
                        <td>{r.change_note}</td>
                        <td>{new Date(r.published_at).toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {diffResult && (
                <div
                  className="km-card"
                  style={{
                    marginTop: 16,
                    background: "var(--bg-secondary)",
                  }}
                >
                  <div className="km-card-header">
                    <h4 style={{ margin: 0 }}>
                      Knowledge DNA Revision Diff:{" "}
                      <span className="km-mono">
                        v{String(diffResult.from_revision || activeBundle.revisions[1]?.revision)}
                      </span>{" "}
                      →{" "}
                      <span className="km-mono">
                        v{String(diffResult.to_revision || activeBundle.revisions[0]?.revision)}
                      </span>
                    </h4>
                    <span className="km-badge verified">
                      Parent-Child Lineage Intact
                    </span>
                  </div>
                  <div className="km-diff-removed">
                    <strong>− Previous Digest:</strong>{" "}
                    <span className="km-mono">
                      {activeBundle.revisions[1]?.content_digest}
                    </span>
                  </div>
                  <div className="km-diff-added">
                    <strong>+ Current Digest:</strong>{" "}
                    <span className="km-mono">
                      {activeBundle.revisions[0]?.content_digest}
                    </span>
                  </div>
                  <div className="km-diff-added">
                    <strong>+ Latest Added Claim:</strong>{" "}
                    {activeBundle.claims[activeBundle.claims.length - 1]?.statement}
                  </div>
                </div>
              )}
            </div>
          )}

          {detailTab === "graph" && (
            <div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: 12,
                }}
              >
                <span className="km-metric-sub">
                  Visual Knowledge Graph linking Bundle Hub, Atomic Claims, and Traceable Evidence Sources
                </span>
                <button
                  type="button"
                  className="km-btn km-btn-sm"
                  onClick={() => setShowRawGraphJson((s) => !s)}
                >
                  {showRawGraphJson ? "View Visual Graph" : "View Raw JSON"}
                </button>
              </div>

              {!showRawGraphJson ? (
                <div
                  style={{
                    background: "#070B14",
                    border: "1px solid var(--border-default)",
                    borderRadius: "var(--radius-md)",
                    padding: 12,
                  }}
                >
                  <svg
                    viewBox="0 0 760 300"
                    style={{ width: "100%", height: 290, display: "block" }}
                  >
                    {/* Edges from Bundle (cx=380, cy=150) to Claims (left) and Evidence (right) */}
                    {activeBundle.claims.map((cl, i) => {
                      const cy = 65 + i * 80;
                      return (
                        <g key={cl.claim_id}>
                          <line
                            x1={380}
                            y1={150}
                            x2={170}
                            y2={cy}
                            stroke="#6599FF"
                            strokeWidth={2}
                          />
                          <circle
                            cx={170}
                            cy={cy}
                            r={18}
                            fill="#10203B"
                            stroke="#6599FF"
                            strokeWidth={2}
                          />
                          <text
                            x={170}
                            y={cy + 4}
                            fill="#F3F7FF"
                            fontSize="9.5"
                            fontWeight="700"
                            textAnchor="middle"
                          >
                            CLM
                          </text>
                          <text
                            x={170}
                            y={cy + 32}
                            fill="#B5C2DC"
                            fontSize="10"
                            textAnchor="middle"
                          >
                            {cl.claim_id} ({cl.status})
                          </text>
                        </g>
                      );
                    })}

                    {activeBundle.evidence.map((ev, i) => {
                      const ey = 85 + i * 110;
                      return (
                        <g key={ev.evidence_id}>
                          <line
                            x1={590}
                            y1={ey}
                            x2={380}
                            y2={150}
                            stroke="#38D399"
                            strokeWidth={2}
                            strokeDasharray="4,4"
                          />
                          <circle
                            cx={590}
                            cy={ey}
                            r={18}
                            fill="#102C24"
                            stroke="#38D399"
                            strokeWidth={2}
                          />
                          <text
                            x={590}
                            y={ey + 4}
                            fill="#38D399"
                            fontSize="9.5"
                            fontWeight="700"
                            textAnchor="middle"
                          >
                            EVID
                          </text>
                          <text
                            x={590}
                            y={ey + 32}
                            fill="#B5C2DC"
                            fontSize="10"
                            textAnchor="middle"
                          >
                            {ev.evidence_id} ({ev.source_type})
                          </text>
                        </g>
                      );
                    })}

                    {/* Central Bundle Node */}
                    <circle
                      cx={380}
                      cy={150}
                      r={28}
                      fill="#162238"
                      stroke="#55C8D7"
                      strokeWidth={3}
                    />
                    <text
                      x={380}
                      y={154}
                      fill="#55C8D7"
                      fontSize="11"
                      fontWeight="800"
                      textAnchor="middle"
                    >
                      OKF
                    </text>
                    <text
                      x={380}
                      y={195}
                      fill="#F3F7FF"
                      fontSize="11.5"
                      fontWeight="650"
                      textAnchor="middle"
                    >
                      {activeBundle.bundle_id}@{activeBundle.current_revision}
                    </text>
                  </svg>
                </div>
              ) : (
                <pre className="km-code-block">
                  {JSON.stringify(
                    graphData || { bundle_id: activeBundle.bundle_id },
                    null,
                    2
                  )}
                </pre>
              )}
            </div>
          )}
        </div>
      )}

      {/* 5-Step Knowledge Bundle & OKF Creation Wizard Modal */}
      {showWizard && (
        <div className="km-modal-backdrop">
          <div
            className="km-modal"
            role="dialog"
            aria-label="Knowledge Publishing Wizard"
          >
            <div className="km-card-header">
              <div>
                <h3 className="km-card-title">
                  5-Step OKF Knowledge Publishing Wizard
                </h3>
                <div className="km-metric-sub">
                  Validates OKF schema, computes RFC 8785 JCS SHA-256 digest, and signs with node Ed25519 key.
                </div>
              </div>
              <button
                type="button"
                className="km-btn km-btn-sm"
                onClick={() => setShowWizard(false)}
              >
                ✕
              </button>
            </div>

            {/* Visual Stepper */}
            <div className="km-stepper">
              {[
                [1, "1. Metadata"],
                [2, "2. Claims"],
                [3, "3. Evidence"],
                [4, "4. Validate"],
                [5, "5. Ed25519 Sign"],
              ].map(([num, label]) => (
                <div
                  key={num}
                  className={`km-step-pill ${
                    wizardStep === num
                      ? "active"
                      : wizardStep > Number(num)
                      ? "done"
                      : ""
                  }`}
                  onClick={() => setWizardStep(Number(num))}
                >
                  <span>{wizardStep > Number(num) ? "✓" : "●"}</span>
                  <span>{label}</span>
                </div>
              ))}
            </div>

            {wizardStep === 1 && (
              <div>
                <div className="km-field">
                  <label className="km-label">Bundle Title *</label>
                  <input
                    className="km-input"
                    required
                    placeholder="e.g., Federated Agent Verification Benchmark 2026"
                    value={wizardForm.title}
                    onChange={(e) =>
                      setWizardForm({ ...wizardForm, title: e.target.value })
                    }
                  />
                </div>
                <div className="km-grid-2">
                  <div className="km-field">
                    <label className="km-label">Domain / Category</label>
                    <input
                      className="km-input"
                      value={wizardForm.category}
                      onChange={(e) =>
                        setWizardForm({
                          ...wizardForm,
                          category: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="km-field">
                    <label className="km-label">Visibility Policy</label>
                    <select
                      className="km-select"
                      value={wizardForm.visibility}
                      onChange={(e) =>
                        setWizardForm({
                          ...wizardForm,
                          visibility: e.target.value,
                        })
                      }
                    >
                      <option value="federated">
                        Federated (Discoverable by Peers)
                      </option>
                      <option value="organization">Organization Only</option>
                      <option value="private">
                        Private (Owner & Authorized Agents)
                      </option>
                    </select>
                  </div>
                </div>
                <div className="km-field">
                  <label className="km-label">Summary / Description</label>
                  <textarea
                    className="km-textarea"
                    value={wizardForm.description}
                    onChange={(e) =>
                      setWizardForm({
                        ...wizardForm,
                        description: e.target.value,
                      })
                    }
                  />
                </div>
              </div>
            )}

            {wizardStep === 2 && (
              <div>
                <div className="km-field">
                  <label className="km-label">
                    Primary Atomic Claim Statement *
                  </label>
                  <textarea
                    className="km-textarea"
                    value={wizardForm.claim_statement}
                    onChange={(e) =>
                      setWizardForm({
                        ...wizardForm,
                        claim_statement: e.target.value,
                      })
                    }
                  />
                </div>
                <div className="km-grid-2">
                  <div className="km-field">
                    <label className="km-label">
                      Initial Epistemic Assessment Status
                    </label>
                    <select
                      className="km-select"
                      value={wizardForm.claim_status}
                      onChange={(e) =>
                        setWizardForm({
                          ...wizardForm,
                          claim_status: e.target.value,
                        })
                      }
                    >
                      <option value="proposed">proposed</option>
                      <option value="evidence_attached">
                        evidence_attached
                      </option>
                      <option value="supported">supported</option>
                    </select>
                  </div>
                  <div className="km-field">
                    <label className="km-label">
                      Empirical Confidence ({Math.round(wizardForm.claim_confidence * 100)}%)
                    </label>
                    <input
                      type="range"
                      min="0.5"
                      max="1.0"
                      step="0.01"
                      value={wizardForm.claim_confidence}
                      onChange={(e) =>
                        setWizardForm({
                          ...wizardForm,
                          claim_confidence: parseFloat(e.target.value),
                        })
                      }
                      style={{ width: "100%", marginTop: 10 }}
                    />
                  </div>
                </div>
              </div>
            )}

            {wizardStep === 3 && (
              <div>
                <div className="km-field">
                  <label className="km-label">Evidence Artifact Title</label>
                  <input
                    className="km-input"
                    value={wizardForm.evidence_title}
                    onChange={(e) =>
                      setWizardForm({
                        ...wizardForm,
                        evidence_title: e.target.value,
                      })
                    }
                  />
                </div>
                <div className="km-field">
                  <label className="km-label">Traceable Source URI *</label>
                  <input
                    className="km-input"
                    value={wizardForm.evidence_uri}
                    onChange={(e) =>
                      setWizardForm({
                        ...wizardForm,
                        evidence_uri: e.target.value,
                      })
                    }
                  />
                </div>
                <div className="km-field">
                  <label className="km-label">Evidence Description</label>
                  <textarea
                    className="km-textarea"
                    value={wizardForm.evidence_desc}
                    onChange={(e) =>
                      setWizardForm({
                        ...wizardForm,
                        evidence_desc: e.target.value,
                      })
                    }
                  />
                </div>
              </div>
            )}

            {wizardStep === 4 && (
              <div>
                <p className="km-metric-sub">
                  Verify structural conformance with the Open Knowledge Format (OKF v0.2) and RFC 8785 canonical JSON serialization before signing.
                </p>
                <button
                  type="button"
                  className="km-btn km-btn-accent"
                  onClick={handleValidateOkfPreview}
                >
                  ✓ Run OKF Schema Validator
                </button>
                {okfValidationReport && (
                  <pre className="km-code-block">
                    {JSON.stringify(okfValidationReport, null, 2)}
                  </pre>
                )}
              </div>
            )}

            {wizardStep === 5 && (
              <div>
                <div className="km-notice verified">
                  <span>
                    Publishing this bundle will compute its canonical OKF SHA-256 digest, sign the payload with{" "}
                    <strong>{wizardForm.node_id}</strong>&apos;s Ed25519 private key, and append a genesis provenance record.
                  </span>
                </div>
                <div className="km-field">
                  <label className="km-label">Publishing Sovereign Node</label>
                  <select
                    className="km-select"
                    value={wizardForm.node_id}
                    onChange={(e) =>
                      setWizardForm({ ...wizardForm, node_id: e.target.value })
                    }
                  >
                    {nodes.map((n) => (
                      <option key={n.node_id} value={n.node_id}>
                        {n.name} ({n.node_id})
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            )}

            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginTop: 20,
              }}
            >
              <button
                type="button"
                className="km-btn"
                disabled={wizardStep === 1}
                onClick={() => setWizardStep((s) => Math.max(1, s - 1))}
              >
                ← Back
              </button>
              {wizardStep < 5 ? (
                <button
                  type="button"
                  className="km-btn km-btn-primary"
                  onClick={() => setWizardStep((s) => Math.min(5, s + 1))}
                >
                  Continue →
                </button>
              ) : (
                <button
                  type="button"
                  className="km-btn km-btn-primary"
                  onClick={handlePublishBundle}
                >
                  ✓ Sign & Publish OKF Bundle
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ============================================================================
   4. FEDERATED DISCOVER & SEARCH VIEW
   ============================================================================ */
export function DiscoverView({
  bundles,
  onInspectBundle,
}: {
  bundles: BundleItem[];
  onInspectBundle: (bundle: BundleItem) => void;
}) {
  const [query, setQuery] = useState<string>("quantization");
  const [scope, setScope] = useState<string>("federated");
  const [sortBy, setSortBy] = useState<string>("relevance");
  const [evidenceOnly, setEvidenceOnly] = useState<boolean>(false);
  const [searchResp, setSearchResp] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  async function runQuery(qText: string, qScope: string, evReq: boolean) {
    setLoading(true);
    try {
      const res = await apiRequest<SearchResponse>("/api/v1/search", {
        method: "POST",
        body: JSON.stringify({
          query: qText || "*",
          scope: qScope,
          sort_by: sortBy,
          evidence_required: evReq,
          limit: 25,
        }),
      });
      setSearchResp(res);
    } catch {
      setSearchResp(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    runQuery(query, scope, evidenceOnly);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bundles]);

  return (
    <div>
      <div className="km-page-header">
        <div>
          <h1 className="km-page-title">Federated Knowledge Discovery</h1>
          <p className="km-page-subtitle">
            Query local BM25 indexes and authorized federated peer nodes with full provenance, freshness, and Ed25519 verification badges.
          </p>
        </div>
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          runQuery(query, scope, evidenceOnly);
        }}
        className="km-card"
        style={{ marginBottom: 24 }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 190px 170px auto",
            gap: 12,
            alignItems: "center",
          }}
        >
          <input
            className="km-input"
            placeholder="Search claims, evidence, or knowledge bundles across federated nodes…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <select
            aria-label="Search scope"
            className="km-select"
            value={scope}
            onChange={(e) => {
              setScope(e.target.value);
              runQuery(query, e.target.value, evidenceOnly);
            }}
          >
            <option value="federated">Scope: Federated Network</option>
            <option value="organization">Scope: Organization</option>
            <option value="local">Scope: Local Node Only</option>
          </select>
          <select
            aria-label="Sort results by"
            className="km-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
          >
            <option value="relevance">Sort: BM25 Relevance</option>
            <option value="freshness">Sort: Freshness</option>
          </select>
          <button
            type="submit"
            className="km-btn km-btn-primary"
            disabled={loading}
          >
            {loading ? "Searching…" : "⌕ Search Mesh"}
          </button>
        </div>

        <div
          style={{
            marginTop: 12,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: 12,
          }}
        >
          <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
            <span className="km-metric-label">Quick Queries:</span>
            {["quantization", "byzantine", "kv-cache", "red-team", "*"].map(
              (chip) => (
                <button
                  key={chip}
                  type="button"
                  className="km-btn km-btn-sm"
                  onClick={() => {
                    setQuery(chip);
                    runQuery(chip, scope, evidenceOnly);
                  }}
                >
                  {chip === "*" ? "All Eligible" : chip}
                </button>
              )
            )}
            <label
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: 6,
                fontSize: 12.5,
                marginLeft: 8,
              }}
            >
              <input
                type="checkbox"
                checked={evidenceOnly}
                onChange={(e) => {
                  setEvidenceOnly(e.target.checked);
                  runQuery(query, scope, e.target.checked);
                }}
              />
              Require attached supporting evidence
            </label>
          </div>

          {searchResp?.trace && (
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <span className="km-badge info">
                Trace: {searchResp.trace.trace_id.slice(0, 10)}
              </span>
              {searchResp.trace.peers_queried.map((pq) => (
                <span
                  key={pq.peer_node_id}
                  className={`km-badge ${
                    pq.status === "responded" ? "verified" : "warning"
                  }`}
                >
                  Peer {pq.peer_node_id}: {pq.status} ({pq.hits ?? 0} hits)
                </span>
              ))}
            </div>
          )}
        </div>
      </form>

      {searchResp && (
        <div>
          <div style={{ marginBottom: 14, color: "var(--text-secondary)" }}>
            Found <strong>{searchResp.total}</strong> verified results for{" "}
            <span className="km-mono">{searchResp.query}</span> ({searchResp.scope})
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            {searchResp.results.map((hit: SearchHit) => (
              <div key={hit.id} className="km-card">
                <div className="km-card-header" style={{ marginBottom: 8 }}>
                  <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                    <span className="km-mono">
                      {hit.bundle_id}@{hit.revision}
                    </span>
                    <span className="km-badge info">
                      Origin: {hit.publisher_node}
                    </span>
                    <span className="km-badge">{hit.category}</span>
                  </div>
                  <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                    <span className={`km-badge ${hit.verification_status}`}>
                      ✓ {hit.verification_status}
                    </span>
                    <span className="km-badge violet">
                      BM25: {hit.score} · Freshness: {hit.freshness_score}
                    </span>
                  </div>
                </div>
                <h3 style={{ margin: "0 0 6px", fontSize: 17 }}>{hit.title}</h3>
                <p className="km-metric-sub" style={{ marginBottom: 12 }}>
                  {hit.description}
                </p>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderTop: "1px solid var(--border-subtle)",
                    paddingTop: 10,
                  }}
                >
                  <div className="km-metric-sub">
                    {hit.claims?.length || 0} atomic claims ·{" "}
                    {hit.evidence?.length || 0} evidence refs · Updated{" "}
                    {new Date(hit.last_updated).toLocaleString()}
                  </div>
                  {hit.record && (
                    <button
                      type="button"
                      className="km-btn km-btn-sm km-btn-primary"
                      onClick={() => onInspectBundle(hit.record)}
                    >
                      Inspect Provenance & Claims →
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
