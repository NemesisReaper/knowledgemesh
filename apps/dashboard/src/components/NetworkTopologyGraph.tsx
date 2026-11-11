"use client";

import React, { useEffect, useMemo, useState } from "react";

export interface TopologyNode {
  id: string;
  label: string;
  type: string;
  status: string;
  endpoint: string;
  visibility: string;
  fingerprint: string;
  bundles?: number;
  claims?: number;
  capabilities?: string[];
}

export interface TopologyEdge {
  id: string;
  source: string;
  target: string;
  status: string;
  verified: boolean;
  approved: boolean;
  latency_ms: number | null;
}

interface Props {
  nodes: TopologyNode[];
  edges: TopologyEdge[];
  onSelectNode?: (node: TopologyNode) => void;
}

export function NetworkTopologyGraph({ nodes, edges, onSelectNode }: Props) {
  const [zoom, setZoom] = useState<number>(1);
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [simulationMode, setSimulationMode] = useState<
    "idle" | "query_fanout" | "pull_sync"
  >("query_fanout");
  const [showTable, setShowTable] = useState<boolean>(false);
  const [copiedFp, setCopiedFp] = useState<boolean>(false);
  const [selectedId, setSelectedId] = useState<string | null>(
    nodes[0]?.id || null
  );

  useEffect(() => {
    if (!selectedId && nodes[0]?.id) {
      setSelectedId(nodes[0].id);
    }
  }, [nodes, selectedId]);

  const filteredNodes = useMemo(() => {
    if (statusFilter === "all") return nodes;
    return nodes.filter((n) => n.status === statusFilter);
  }, [nodes, statusFilter]);

  const positions = useMemo(() => {
    const map: Record<string, { x: number; y: number }> = {};
    const cx = 370;
    const cy = 195;

    // Place the single local anchor node strictly at center
    const localNode =
      filteredNodes.find((n) => n.type === "local_node") || filteredNodes[0];
    const peerNodes = filteredNodes.filter((n) => n.id !== localNode?.id);

    if (localNode) {
      map[localNode.id] = { x: cx, y: cy };
    }

    // Evenly distribute peer nodes in an orbit ring to prevent any overlapping
    const count = peerNodes.length;
    peerNodes.forEach((n, idx) => {
      const angle =
        count === 1
          ? -Math.PI / 4
          : (idx / Math.max(1, count)) * Math.PI * 2 - Math.PI / 2;
      const radius = count <= 2 ? 140 : 155;
      map[n.id] = {
        x: Math.round(cx + Math.cos(angle) * radius * 1.35),
        y: Math.round(cy + Math.sin(angle) * radius * 0.85),
      };
    });

    return map;
  }, [filteredNodes]);

  const uniqueDisplayEdges = useMemo(() => {
    const seen = new Set<string>();
    const result: TopologyEdge[] = [];
    for (const edge of edges) {
      if (edge.source === edge.target) continue;
      const pairKey = [edge.source, edge.target].sort().join("___");
      if (!seen.has(pairKey)) {
        seen.add(pairKey);
        result.push(edge);
      }
    }
    return result;
  }, [edges]);

  const selectedNode = useMemo(
    () =>
      filteredNodes.find((n) => n.id === selectedId) ||
      filteredNodes[0] ||
      null,
    [filteredNodes, selectedId]
  );

  const selectedNodeEdges = useMemo(() => {
    if (!selectedNode) return [];
    return edges.filter(
      (e) => e.source === selectedNode.id || e.target === selectedNode.id
    );
  }, [edges, selectedNode]);

  return (
    <div
      className="km-card"
      role="region"
      aria-label="Federated Network Topology"
    >
      <div className="km-card-header">
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <h3 className="km-card-title">
              Federated Knowledge Mesh Topology
            </h3>
            <span className="km-badge verified">
              ● Live Telemetry ({nodes.length} Nodes · {edges.length} Peer Links)
            </span>
          </div>
          <div className="km-metric-sub" style={{ marginTop: 3 }}>
            Live sovereign Ed25519 node identities, peer trust handshakes, and pull-sync channels from backend registry
          </div>
        </div>

        <div
          style={{
            display: "flex",
            gap: 8,
            alignItems: "center",
            flexWrap: "wrap",
          }}
        >
          <button
            type="button"
            className={`km-btn km-btn-sm ${
              simulationMode === "query_fanout" ? "km-btn-accent" : ""
            }`}
            onClick={() =>
              setSimulationMode((m) =>
                m === "query_fanout" ? "idle" : "query_fanout"
              )
            }
          >
            ⌕ Query Fan-Out Pulse
          </button>
          <button
            type="button"
            className={`km-btn km-btn-sm ${
              simulationMode === "pull_sync" ? "km-btn-primary" : ""
            }`}
            onClick={() =>
              setSimulationMode((m) =>
                m === "pull_sync" ? "idle" : "pull_sync"
              )
            }
          >
            ⇄ Pull-Sync Packet Flow
          </button>
          <select
            aria-label="Filter topology nodes by status"
            className="km-select"
            style={{ width: 145, padding: "5px 8px", fontSize: 12 }}
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="all">All Statuses ({nodes.length})</option>
            <option value="active">Active Only</option>
            <option value="pending">Pending Handshake</option>
          </select>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={() =>
              setZoom((z) => Math.min(1.45, +(z + 0.15).toFixed(2)))
            }
            title="Zoom in"
          >
            +
          </button>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={() =>
              setZoom((z) => Math.max(0.75, +(z - 0.15).toFixed(2)))
            }
            title="Zoom out"
          >
            −
          </button>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={() => setZoom(1)}
          >
            100%
          </button>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={() => setShowTable((s) => !s)}
          >
            {showTable ? "Hide Table" : "Matrix View"}
          </button>
        </div>
      </div>

      {filteredNodes.length === 0 ? (
        <div
          style={{
            padding: 40,
            textAlign: "center",
            background: "var(--bg-secondary)",
            borderRadius: "var(--radius-md)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 6 }}>
            No Nodes Registered in Current Filter
          </div>
          <div className="km-metric-sub">
            Register a knowledge node in the &ldquo;My Nodes&rdquo; tab or connect a peer in &ldquo;Federation & Peers&rdquo; to populate the live mesh topology.
          </div>
        </div>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: selectedNode ? "1.65fr 1fr" : "1fr",
            gap: 18,
            alignItems: "stretch",
          }}
        >
          {/* Interactive SVG Canvas */}
          <div
            style={{
              background:
                "radial-gradient(circle at 50% 50%, #0E172A 0%, #070B14 100%)",
              border: "1px solid var(--border-default)",
              borderRadius: "var(--radius-md)",
              overflow: "hidden",
              position: "relative",
              minHeight: 380,
            }}
          >
            <div
              style={{
                position: "absolute",
                top: 12,
                left: 14,
                zIndex: 5,
                display: "flex",
                gap: 12,
                flexWrap: "wrap",
                padding: "6px 12px",
                borderRadius: "var(--radius-pill)",
                background: "rgba(9, 13, 24, 0.82)",
                border: "1px solid var(--border-subtle)",
                fontSize: 11,
                color: "var(--text-secondary)",
              }}
            >
              <span
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 5,
                }}
              >
                <span
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    background: "#6599FF",
                  }}
                />
                Local Anchor Node
              </span>
              <span
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 5,
                }}
              >
                <span
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    background: "#38D399",
                  }}
                />
                Ed25519 Verified Peer
              </span>
              <span
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 5,
                }}
              >
                <span
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    background: "#F5B942",
                  }}
                />
                Pending Handshake
              </span>
            </div>

            <svg
              viewBox="0 0 740 390"
              style={{
                width: "100%",
                height: 380,
                transform: `scale(${zoom})`,
                transformOrigin: "center center",
                transition: "transform 180ms ease",
                display: "block",
              }}
            >
              <defs>
                <pattern
                  id="kmGrid"
                  width="36"
                  height="36"
                  patternUnits="userSpaceOnUse"
                >
                  <path
                    d="M 36 0 L 0 0 0 36"
                    fill="none"
                    stroke="#152036"
                    strokeWidth="0.75"
                  />
                </pattern>
                <radialGradient id="nodeGlowPrimary" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#6599FF" stopOpacity="0.42" />
                  <stop offset="100%" stopColor="#6599FF" stopOpacity="0" />
                </radialGradient>
                <radialGradient id="nodeGlowVerified" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#38D399" stopOpacity="0.35" />
                  <stop offset="100%" stopColor="#38D399" stopOpacity="0" />
                </radialGradient>
              </defs>

              <rect width="740" height="390" fill="url(#kmGrid)" />

              <circle
                cx={370}
                cy={195}
                r={95}
                fill="none"
                stroke="#1A2742"
                strokeDasharray="3,6"
                strokeWidth={1}
              />
              <circle
                cx={370}
                cy={195}
                r={168}
                fill="none"
                stroke="#18243D"
                strokeDasharray="4,8"
                strokeWidth={1}
              />

              {/* Edges & Animated Packet Streams (Deduplicated to prevent badge collisions) */}
              {uniqueDisplayEdges.map((edge, idx) => {
                const src = positions[edge.source];
                const dst = positions[edge.target];
                if (!src || !dst) return null;
                const isVerifiedLink = edge.verified && edge.approved;
                const strokeColor = isVerifiedLink
                  ? "#38D399"
                  : edge.status === "pending"
                  ? "#F5B942"
                  : "#55C8D7";
                const mx = (src.x + dst.x) / 2;
                const my = (src.y + dst.y) / 2;
                const pathD = `M ${src.x} ${src.y} L ${dst.x} ${dst.y}`;
                const reversePathD = `M ${dst.x} ${dst.y} L ${src.x} ${src.y}`;

                return (
                  <g key={edge.id}>
                    {isVerifiedLink && (
                      <line
                        x1={src.x}
                        y1={src.y}
                        x2={dst.x}
                        y2={dst.y}
                        stroke={strokeColor}
                        strokeWidth={6}
                        opacity={0.12}
                      />
                    )}
                    <line
                      x1={src.x}
                      y1={src.y}
                      x2={dst.x}
                      y2={dst.y}
                      stroke={strokeColor}
                      strokeWidth={2.2}
                      strokeDasharray={edge.approved ? undefined : "6,5"}
                      opacity={0.85}
                    />

                    {simulationMode !== "idle" && isVerifiedLink && (
                      <>
                        <circle
                          r={4}
                          fill={
                            simulationMode === "query_fanout"
                              ? "#55C8D7"
                              : "#6599FF"
                          }
                        >
                          <animateMotion
                            dur={`${2.1 + idx * 0.35}s`}
                            repeatCount="indefinite"
                            path={pathD}
                          />
                        </circle>
                        <circle r={3.5} fill="#38D399">
                          <animateMotion
                            dur={`${2.4 + idx * 0.3}s`}
                            repeatCount="indefinite"
                            path={reversePathD}
                          />
                        </circle>
                      </>
                    )}

                    <g transform={`translate(${mx}, ${my})`}>
                      <rect
                        x={-54}
                        y={-11}
                        width={108}
                        height={20}
                        rx={10}
                        fill="#0B111E"
                        stroke={strokeColor}
                        strokeWidth={1}
                        opacity={0.95}
                      />
                      <text
                        x={0}
                        y={2.5}
                        fill="#D7E3FF"
                        fontSize="9.5"
                        fontWeight="600"
                        textAnchor="middle"
                      >
                        {edge.verified ? "✓ Ed25519" : edge.status}
                        {edge.latency_ms !== null
                          ? ` · ${edge.latency_ms}ms`
                          : ""}
                      </text>
                    </g>
                  </g>
                );
              })}

              {/* Nodes */}
              {filteredNodes.map((node) => {
                const pos = positions[node.id] || { x: 370, y: 195 };
                const isLocal = node.type === "local_node";
                const isSelected = selectedNode?.id === node.id;
                const strokeColor = isLocal
                  ? "#6599FF"
                  : node.status === "active"
                  ? "#38D399"
                  : "#F5B942";

                return (
                  <g
                    key={node.id}
                    transform={`translate(${pos.x}, ${pos.y})`}
                    style={{ cursor: "pointer" }}
                    onClick={() => {
                      setSelectedId(node.id);
                      onSelectNode?.(node);
                    }}
                  >
                    {isSelected && (
                      <circle
                        r={44}
                        fill={
                          isLocal
                            ? "url(#nodeGlowPrimary)"
                            : "url(#nodeGlowVerified)"
                        }
                      />
                    )}
                    {isLocal && (
                      <circle
                        className="km-pulse-circle"
                        r={24}
                        fill="none"
                        stroke="#6599FF"
                        strokeWidth={1.5}
                      />
                    )}

                    <circle
                      r={isLocal ? 24 : 20}
                      fill="#0D1526"
                      stroke={strokeColor}
                      strokeWidth={isSelected ? 3.5 : 2.2}
                    />
                    <circle r={isLocal ? 8 : 6} fill={strokeColor} />

                    <rect
                      x={-86}
                      y={isLocal ? 30 : 26}
                      width={172}
                      height={36}
                      rx={8}
                      fill="rgba(11, 17, 30, 0.92)"
                      stroke={isSelected ? strokeColor : "#22304A"}
                      strokeWidth={1}
                    />
                    <text
                      y={isLocal ? 45 : 41}
                      fill="#F3F7FF"
                      fontSize="11"
                      fontWeight="650"
                      textAnchor="middle"
                    >
                      {node.label.length > 25
                        ? `${node.label.slice(0, 24)}…`
                        : node.label}
                    </text>
                    <text
                      y={isLocal ? 59 : 55}
                      fill="#8FA1C2"
                      fontSize="9.5"
                      fontFamily="var(--font-mono)"
                      textAnchor="middle"
                    >
                      {node.id} · {node.visibility}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>

          {/* Selected Node Detailed Inspector Panel */}
          {selectedNode && (
            <div
              style={{
                background: "var(--bg-secondary)",
                border: "1px solid var(--border-default)",
                borderRadius: "var(--radius-md)",
                padding: 18,
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                gap: 14,
              }}
            >
              <div>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: 10,
                  }}
                >
                  <span className="km-metric-label">
                    Node Identity Inspector
                  </span>
                  <div style={{ display: "flex", gap: 6 }}>
                    <span className={`km-badge ${selectedNode.visibility}`}>
                      {selectedNode.visibility}
                    </span>
                    <span className={`km-badge ${selectedNode.status}`}>
                      ● {selectedNode.status}
                    </span>
                  </div>
                </div>

                <h4 style={{ margin: "0 0 6px", fontSize: 16.5 }}>
                  {selectedNode.label}
                </h4>
                <div
                  style={{
                    display: "flex",
                    gap: 6,
                    alignItems: "center",
                    flexWrap: "wrap",
                    marginBottom: 14,
                  }}
                >
                  <span className="km-mono">
                    did:kyro:{selectedNode.id}
                  </span>
                  <span className="km-badge violet">
                    {selectedNode.type === "local_node"
                      ? "Local Anchor"
                      : "Federated Peer"}
                  </span>
                </div>

                <div className="km-field">
                  <span className="km-label">HTTP Federation Endpoint</span>
                  <div className="km-mono" style={{ wordBreak: "break-all" }}>
                    {selectedNode.endpoint}
                  </div>
                </div>

                <div className="km-field">
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      marginBottom: 5,
                    }}
                  >
                    <span className="km-label" style={{ marginBottom: 0 }}>
                      Ed25519 Public Key Fingerprint (SHA-256)
                    </span>
                    {selectedNode.fingerprint && (
                      <button
                        type="button"
                        className="km-btn km-btn-sm"
                        style={{ padding: "2px 7px", fontSize: 11 }}
                        onClick={() => {
                          navigator.clipboard?.writeText(
                            selectedNode.fingerprint
                          );
                          setCopiedFp(true);
                          setTimeout(() => setCopiedFp(false), 1400);
                        }}
                      >
                        {copiedFp ? "Copied" : "Copy"}
                      </button>
                    )}
                  </div>
                  <div
                    className="km-mono"
                    style={{
                      wordBreak: "break-all",
                      fontSize: 11,
                      display: "block",
                      padding: "6px 8px",
                    }}
                  >
                    {selectedNode.fingerprint || "Pending peer key exchange"}
                  </div>
                </div>

                <div className="km-field" style={{ marginBottom: 0 }}>
                  <span className="km-label">
                    Connected Peer Channels ({selectedNodeEdges.length})
                  </span>
                  {selectedNodeEdges.length === 0 ? (
                    <div className="km-metric-sub">
                      No peer links attached to this node yet.
                    </div>
                  ) : (
                    <div
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 6,
                      }}
                    >
                      {selectedNodeEdges.map((edge) => {
                        const peerId =
                          edge.source === selectedNode.id
                            ? edge.target
                            : edge.source;
                        return (
                          <div
                            key={edge.id}
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              alignItems: "center",
                              padding: "6px 10px",
                              background: "var(--bg-elevated)",
                              borderRadius: "var(--radius-sm)",
                              border: "1px solid var(--border-subtle)",
                              fontSize: 12,
                            }}
                          >
                            <span>
                              ⇄ <span className="km-mono">{peerId}</span>
                            </span>
                            <span
                              className={`km-badge ${
                                edge.verified ? "verified" : "warning"
                              }`}
                            >
                              {edge.verified ? "Verified" : edge.status}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {showTable && filteredNodes.length > 0 && (
        <div className="km-table-wrap" style={{ marginTop: 16 }}>
          <table
            className="km-table"
            aria-label="Accessible network topology table"
          >
            <thead>
              <tr>
                <th>Node ID</th>
                <th>Name</th>
                <th>Role</th>
                <th>Endpoint</th>
                <th>Visibility</th>
                <th>Status</th>
                <th>Ed25519 Fingerprint</th>
              </tr>
            </thead>
            <tbody>
              {filteredNodes.map((n) => (
                <tr
                  key={n.id}
                  className={selectedNode?.id === n.id ? "selected-row" : ""}
                  onClick={() => setSelectedId(n.id)}
                  style={{ cursor: "pointer" }}
                >
                  <td>
                    <span className="km-mono">{n.id}</span>
                  </td>
                  <td style={{ fontWeight: 600 }}>{n.label}</td>
                  <td>{n.type}</td>
                  <td>
                    <span className="km-mono">{n.endpoint}</span>
                  </td>
                  <td>
                    <span className={`km-badge ${n.visibility}`}>
                      {n.visibility}
                    </span>
                  </td>
                  <td>
                    <span className={`km-badge ${n.status}`}>{n.status}</span>
                  </td>
                  <td>
                    <span className="km-mono">
                      {n.fingerprint ? `${n.fingerprint.slice(0, 18)}...` : "-"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
