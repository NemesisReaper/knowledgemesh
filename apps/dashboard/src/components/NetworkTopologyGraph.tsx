"use client";

import { useEffect, useMemo, useState } from "react";

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

type Point = { x: number; y: number };

export function NetworkTopologyGraph({
  nodes,
  edges,
  onSelectNode,
}: Props) {
  const [zoom, setZoom] = useState(1);
  const [statusFilter, setStatusFilter] = useState("all");
  const [simulationMode, setSimulationMode] = useState<
    "idle" | "query_fanout" | "pull_sync"
  >("idle");
  const [showTable, setShowTable] = useState(false);
  const [copiedFp, setCopiedFp] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(
    nodes[0]?.id ?? null
  );

  const filteredNodes = useMemo(
    () =>
      statusFilter === "all"
        ? nodes
        : nodes.filter((node) => node.status === statusFilter),
    [nodes, statusFilter]
  );

  // Keep selection valid when data or filters change.
  useEffect(() => {
    if (!filteredNodes.length) {
      setSelectedId(null);
      return;
    }

    if (!filteredNodes.some((node) => node.id === selectedId)) {
      setSelectedId(filteredNodes[0].id);
    }
  }, [filteredNodes, selectedId]);

  const selectedNode =
    filteredNodes.find((node) => node.id === selectedId) ??
    filteredNodes[0] ??
    null;

  const positions = useMemo<Record<string, Point>>(() => {
    const result: Record<string, Point> = {};
    const localNode =
      filteredNodes.find((node) => node.type === "local_node") ??
      filteredNodes[0];
    const peers = filteredNodes.filter((node) => node.id !== localNode?.id);
    const count = peers.length;
    const isTriangular = count === 2;
    const center = { x: 370, y: isTriangular ? 220 : 195 };

    if (localNode) result[localNode.id] = center;

    if (isTriangular) {
      // 2 peers: triangular layout with peers above local anchor
      result[peers[0].id] = { x: 550, y: 95 };
      result[peers[1].id] = { x: 190, y: 95 };
    } else if (count === 3) {
      // 3 peers: orthogonal T-layout (Top, Right, Left) with Center anchor
      result[peers[0].id] = { x: 370, y: 65 };
      result[peers[1].id] = { x: 620, y: 195 };
      result[peers[2].id] = { x: 120, y: 195 };
    } else {
      // General N peers: elliptical distribution
      const radiusX = count > 8 ? 240 : count > 4 ? 220 : 190;
      const radiusY = count > 8 ? 140 : 130;

      peers.forEach((node, index) => {
        const angle = (index / Math.max(count, 1)) * Math.PI * 2 - Math.PI / 2;
        result[node.id] = {
          x: Math.round(center.x + Math.cos(angle) * radiusX),
          y: Math.round(center.y + Math.sin(angle) * radiusY),
        };
      });
    }

    return result;
  }, [filteredNodes]);

  // Treat links as undirected for display and prevent duplicate visual lines.
  const uniqueDisplayEdges = useMemo(() => {
    const seen = new Set<string>();
    return edges.filter((edge) => {
      if (edge.source === edge.target) return false;
      const key = [edge.source, edge.target].sort().join("::");
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }, [edges]);

  const selectedNodeEdges = useMemo(
    () =>
      selectedNode
        ? edges.filter(
          (edge) =>
            edge.source === selectedNode.id ||
            edge.target === selectedNode.id
        )
        : [],
    [edges, selectedNode]
  );

  const handleSelectNode = (node: TopologyNode) => {
    setSelectedId(node.id);
    onSelectNode?.(node);
  };

  const copyFingerprint = async () => {
    if (!selectedNode?.fingerprint) return;

    try {
      await navigator.clipboard.writeText(selectedNode.fingerprint);
      setCopiedFp(true);
      window.setTimeout(() => setCopiedFp(false), 1400);
    } catch {
      setCopiedFp(false);
    }
  };

  return (
    <div
      className="km-card"
      role="region"
      aria-label="Federated Network Topology"
    >
      <div className="km-card-header">
        <div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              flexWrap: "wrap",
            }}
          >
            <h3 className="km-card-title">
              Federated Knowledge Mesh Topology
            </h3>
            <span className="km-badge verified">
              {nodes.length} Nodes · {edges.length} Peer Links
            </span>
          </div>
          <div className="km-metric-sub" style={{ marginTop: 3 }}>
            Node identities, peer trust handshakes, and federation channels
            reported by the backend registry
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
            className={`km-btn km-btn-sm ${simulationMode === "query_fanout" ? "km-btn-accent" : ""
              }`}
            aria-pressed={simulationMode === "query_fanout"}
            onClick={() =>
              setSimulationMode((mode) =>
                mode === "query_fanout" ? "idle" : "query_fanout"
              )
            }
          >
            ⌕ Query Fan-Out Pulse
          </button>
          <button
            type="button"
            className={`km-btn km-btn-sm ${simulationMode === "pull_sync" ? "km-btn-primary" : ""
              }`}
            aria-pressed={simulationMode === "pull_sync"}
            onClick={() =>
              setSimulationMode((mode) =>
                mode === "pull_sync" ? "idle" : "pull_sync"
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
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="all">All Statuses ({nodes.length})</option>
            <option value="active">Active Only</option>
            <option value="pending">Pending Handshake</option>
          </select>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={() => setZoom((value) => Math.min(1.45, +(value + 0.15).toFixed(2)))}
            title="Zoom in"
            aria-label="Zoom in"
          >
            +
          </button>
          <button
            type="button"
            className="km-btn km-btn-sm"
            onClick={() => setZoom((value) => Math.max(0.75, +(value - 0.15).toFixed(2)))}
            title="Zoom out"
            aria-label="Zoom out"
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
            onClick={() => setShowTable((value) => !value)}
            aria-expanded={showTable}
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
            Register a knowledge node in the &ldquo;My Nodes&rdquo; tab or
            connect a peer in &ldquo;Federation &amp; Peers&rdquo; to populate
            the network topology.
          </div>
        </div>
      ) : (
        <div
          className="km-topology-layout"
          style={{
            display: "grid",
            gridTemplateColumns: selectedNode
              ? "minmax(0, 1.65fr) minmax(260px, 1fr)"
              : "1fr",
            gap: 18,
            alignItems: "stretch",
          }}
        >
          <div
            style={{
              background:
                "radial-gradient(circle at 50% 50%, #FFFFFF 0%, #F8FAFC 100%)",
              border: "1px solid var(--border-default)",
              borderRadius: "var(--radius-lg)",
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
                background: "rgba(255, 255, 255, 0.92)",
                backdropFilter: "blur(8px)",
                border: "1px solid var(--border-default)",
                boxShadow: "0 2px 8px rgba(0, 0, 0, 0.04)",
                fontSize: 11,
                color: "var(--text-secondary)",
              }}
            >
              <Legend color="#4F46E5" label="Local Anchor Node" />
              <Legend color="#059669" label="Verified Peer" />
              <Legend color="#D97706" label="Pending Handshake" />
            </div>

            <svg
              viewBox="0 0 740 390"
              role="img"
              aria-label="Interactive diagram of local and federated knowledge nodes"
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
                  id="kmTopologyGrid"
                  width="36"
                  height="36"
                  patternUnits="userSpaceOnUse"
                >
                  <path
                    d="M 36 0 L 0 0 0 36"
                    fill="none"
                    stroke="#F1F5F9"
                    strokeWidth="1"
                  />
                </pattern>
                <radialGradient
                  id="kmNodeGlowPrimary"
                  cx="50%"
                  cy="50%"
                  r="50%"
                >
                  <stop offset="0%" stopColor="#4F46E5" stopOpacity="0.25" />
                  <stop offset="100%" stopColor="#4F46E5" stopOpacity="0" />
                </radialGradient>
                <radialGradient
                  id="kmNodeGlowVerified"
                  cx="50%"
                  cy="50%"
                  r="50%"
                >
                  <stop offset="0%" stopColor="#059669" stopOpacity="0.2" />
                  <stop offset="100%" stopColor="#059669" stopOpacity="0" />
                </radialGradient>
              </defs>

              <rect width="740" height="390" fill="url(#kmTopologyGrid)" />
              <circle
                cx={370}
                cy={195}
                r={95}
                fill="none"
                stroke="#E2E8F0"
                strokeDasharray="3,6"
              />
              <circle
                cx={370}
                cy={195}
                r={168}
                fill="none"
                stroke="#E2E8F0"
                strokeDasharray="4,8"
              />

              {uniqueDisplayEdges.map((edge, index) => {
                const source = positions[edge.source];
                const target = positions[edge.target];
                if (!source || !target) return null;

                const verified = edge.verified && edge.approved;
                const stroke = verified
                  ? "#38D399"
                  : edge.status === "pending"
                    ? "#F5B942"
                    : "#55C8D7";
                const path = `M ${source.x} ${source.y} L ${target.x} ${target.y}`;
                const reversePath = `M ${target.x} ${target.y} L ${source.x} ${source.y}`;
                const dx = target.x - source.x;
                const dy = target.y - source.y;
                const len = Math.sqrt(dx * dx + dy * dy) || 1;
                const badgeX = Math.round((source.x + target.x) / 2);
                const badgeY = Math.round((source.y + target.y) / 2);

                return (
                  <g key={edge.id}>
                    {verified && (
                      <line
                        x1={source.x}
                        y1={source.y}
                        x2={target.x}
                        y2={target.y}
                        stroke={stroke}
                        strokeWidth={6}
                        opacity={0.12}
                      />
                    )}
                    <line
                      x1={source.x}
                      y1={source.y}
                      x2={target.x}
                      y2={target.y}
                      stroke={stroke}
                      strokeWidth={2.2}
                      strokeDasharray={edge.approved ? undefined : "6,5"}
                      opacity={0.85}
                    />

                    {verified && (
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
                            dur={`${simulationMode === "idle" ? 2.8 + index * 0.4 : 1.4 + index * 0.25}s`}
                            repeatCount="indefinite"
                            path={path}
                          />
                        </circle>
                        <circle r={3.5} fill="#38D399">
                          <animateMotion
                            dur={`${simulationMode === "idle" ? 3.2 + index * 0.4 : 1.6 + index * 0.25}s`}
                            repeatCount="indefinite"
                            path={reversePath}
                          />
                        </circle>
                      </>
                    )}

                    <g transform={`translate(${badgeX}, ${badgeY})`}>
                      <rect
                        x={-54}
                        y={-11}
                        width={108}
                        height={20}
                        rx={10}
                        fill="#FFFFFF"
                        stroke={stroke}
                        strokeWidth={1}
                        opacity={0.98}
                      />
                      <text
                        x={0}
                        y={2.5}
                        fill="#0A0F1D"
                        fontSize="9.5"
                        fontWeight="650"
                        textAnchor="middle"
                      >
                        {edge.verified ? "✓ Verified" : edge.status}
                        {edge.latency_ms !== null
                          ? ` · ${edge.latency_ms}ms`
                          : ""}
                      </text>
                    </g>
                  </g>
                );
              })}

              {filteredNodes.map((node) => {
                const point = positions[node.id] ?? { x: 370, y: 195 };
                const isLocal = node.type === "local_node";
                const isSelected = selectedNode?.id === node.id;
                const stroke = isLocal
                  ? "#4F46E5"
                  : node.status === "active"
                    ? "#059669"
                    : "#D97706";

                const isUpper = point.y < (positions[filteredNodes[0]?.id]?.y ?? 195) - 20;
                const cardY = isUpper ? -52 : (isLocal ? 30 : 26);
                const textY1 = isUpper ? -37 : (isLocal ? 45 : 41);
                const textY2 = isUpper ? -23 : (isLocal ? 59 : 55);

                return (
                  <g
                    key={node.id}
                    transform={`translate(${point.x}, ${point.y})`}
                    role="button"
                    tabIndex={0}
                    aria-label={`Select node ${node.label}`}
                    aria-pressed={isSelected}
                    style={{ cursor: "pointer", outline: "none" }}
                    onClick={() => handleSelectNode(node)}
                    onKeyDown={(event) => {
                      if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        handleSelectNode(node);
                      }
                    }}
                  >
                    {isSelected && (
                      <circle
                        r={44}
                        fill={
                          isLocal
                            ? "url(#kmNodeGlowPrimary)"
                            : "url(#kmNodeGlowVerified)"
                        }
                      />
                    )}
                    {isLocal && (
                      <circle
                        className="km-pulse-circle"
                        r={24}
                        fill="none"
                        stroke="#4F46E5"
                        strokeWidth={1.5}
                      />
                    )}
                    <circle
                      r={isLocal ? 24 : 20}
                      fill="#FFFFFF"
                      stroke={stroke}
                      strokeWidth={isSelected ? 3.5 : 2.2}
                    />
                    <circle r={isLocal ? 8 : 6} fill={stroke} />
                    {(() => {
                      const fullLabel = node.label || node.id;
                      const cardWidth = Math.max(185, Math.min(270, Math.round(fullLabel.length * 7.4) + 26));
                      const cardX = -Math.round(cardWidth / 2);
                      return (
                        <>
                          <rect
                            x={cardX}
                            y={cardY}
                            width={cardWidth}
                            height={36}
                            rx={8}
                            fill="rgba(255, 255, 255, 0.95)"
                            stroke={isSelected ? stroke : "#CBD5E1"}
                          />
                          <text
                            y={textY1}
                            fill="#0A0F1D"
                            fontSize="11"
                            fontWeight="700"
                            textAnchor="middle"
                            pointerEvents="none"
                          >
                            {fullLabel}
                          </text>
                          <text
                            y={textY2}
                            fill="#64748B"
                            fontSize="9.5"
                            fontFamily="var(--font-mono)"
                            textAnchor="middle"
                            pointerEvents="none"
                          >
                            {node.id} · {node.visibility}
                          </text>
                        </>
                      );
                    })()}
                  </g>
                );
              })}
            </svg>
          </div>

          {selectedNode && (
            <aside
              aria-label="Selected node details"
              style={{
                background: "var(--bg-secondary)",
                border: "1px solid var(--border-default)",
                borderRadius: "var(--radius-md)",
                padding: 18,
                display: "flex",
                flexDirection: "column",
                gap: 14,
                minWidth: 0,
              }}
            >
              <div>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: 8,
                    flexWrap: "wrap",
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
                  <span className="km-mono">did:kyro:{selectedNode.id}</span>
                  <span className="km-badge violet">
                    {selectedNode.type === "local_node"
                      ? "Local Anchor"
                      : "Federated Peer"}
                  </span>
                </div>

                <div className="km-field">
                  <span className="km-label">HTTP Federation Endpoint</span>
                  <div className="km-mono" style={{ wordBreak: "break-all" }}>
                    {selectedNode.endpoint || "Not provided"}
                  </div>
                </div>

                <div className="km-field">
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      gap: 8,
                      marginBottom: 5,
                    }}
                  >
                    <span className="km-label" style={{ marginBottom: 0 }}>
                      Public Key Fingerprint (SHA-256)
                    </span>
                    {selectedNode.fingerprint && (
                      <button
                        type="button"
                        className="km-btn km-btn-sm"
                        style={{ padding: "2px 7px", fontSize: 11 }}
                        onClick={copyFingerprint}
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
                              gap: 8,
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
                              className={`km-badge ${edge.verified && edge.approved
                                  ? "verified"
                                  : "warning"
                                }`}
                            >
                              {edge.verified && edge.approved
                                ? "Verified"
                                : edge.status}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              </div>
            </aside>
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
                <th>Public Key Fingerprint</th>
              </tr>
            </thead>
            <tbody>
              {filteredNodes.map((node) => (
                <tr
                  key={node.id}
                  className={
                    selectedNode?.id === node.id ? "selected-row" : ""
                  }
                  onClick={() => handleSelectNode(node)}
                  style={{ cursor: "pointer" }}
                >
                  <td><span className="km-mono">{node.id}</span></td>
                  <td style={{ fontWeight: 600 }}>{node.label}</td>
                  <td>{node.type}</td>
                  <td><span className="km-mono">{node.endpoint}</span></td>
                  <td>
                    <span className={`km-badge ${node.visibility}`}>
                      {node.visibility}
                    </span>
                  </td>
                  <td>
                    <span className={`km-badge ${node.status}`}>
                      {node.status}
                    </span>
                  </td>
                  <td>
                    <span className="km-mono">
                      {node.fingerprint
                        ? `${node.fingerprint.slice(0, 18)}…`
                        : "—"}
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

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 5 }}>
      <span
        aria-hidden="true"
        style={{
          width: 8,
          height: 8,
          borderRadius: "50%",
          background: color,
        }}
      />
      {label}
    </span>
  );
}
