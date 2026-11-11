"use client";

import React, { useState } from "react";

export function OKFGraphWorkspace({
  onNavigateTab,
}: {
  onNavigateTab?: (tab: string) => void;
}) {
  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const [hoveredCardId, setHoveredCardId] = useState<string | null>("doc-md-1");
  const [activeSidebarItem, setActiveSidebarItem] = useState<string>("graph");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const documentCards = [
    {
      id: "doc-md-1",
      title: "concept-kv-quant.md",
      type: "Markdown (.md)",
      tagType: "type: concept",
      tagStatus: "status: verified",
      badgeColor: "#10B981", // emerald
      x: 160,
      y: 110,
      yaml: `---
bundle_id: bun-kv-2026
type: concept
status: verified
confidence: 0.996
---`,
      rawContent: `# INT4 KV-Cache Group Quantization
Maintains 99.6% needle retrieval accuracy up to 128k tokens with 3.7x lower HBM memory footprint.
- verified_by: did:kyro:node-a
- canonical_jcs: e3b0c44298fc1c...`,
    },
    {
      id: "doc-yaml-1",
      title: "manifest.yaml",
      type: "YAML Frontmatter",
      tagType: "type: schema",
      tagStatus: "status: verified",
      badgeColor: "#F59E0B", // warm amber
      x: 160,
      y: 390,
      yaml: `format_version: "0.2"
publisher: "node-a"
signing_suite: "Ed25519"
digest: "RFC8785-JCS"`,
      rawContent: `bundle_specification:
  okf_version: "0.2"
  canonical_serialization: "rfc8785"
  hash_algorithm: "sha256"`,
    },
    {
      id: "doc-md-2",
      title: "evidence-benchmark.md",
      type: "Markdown (.md)",
      tagType: "type: evidence",
      tagStatus: "status: verified",
      badgeColor: "#10B981",
      x: 800,
      y: 110,
      yaml: `---
source: LongBench-128k
reliability: 0.98
hardware: 8xH100 SXM5
---`,
      rawContent: `### LongBench-128k Multi-Hop Empirical Trace
Nsight profiling confirms memory bandwidth saturation drops from 94% to 26% under INT4 KV caching.`,
    },
    {
      id: "doc-yaml-2",
      title: "lineage-prov.yaml",
      type: "YAML Frontmatter",
      tagType: "type: provenance",
      tagStatus: "status: verified",
      badgeColor: "#F59E0B",
      x: 800,
      y: 390,
      yaml: `w3c_prov:
  activity: "bundle.published"
  actor: "architect@kyro"
  parent_hash: "00000000"`,
      rawContent: `provenance_chain:
  generation: 1
  hash_chain: "sha256:4f1a8c9b2d..."
  immutable_head: true`,
    },
  ];

  const agentNodes = [
    {
      id: "agent-indexer",
      label: "Agent-Indexer",
      sub: "Active Indexing (60Hz)",
      x: 480,
      y: 40,
      color: "#3B82F6",
      angle: 0,
    },
    {
      id: "agent-query-bot",
      label: "Agent-Query-Bot",
      sub: "Context Traversal",
      x: 480,
      y: 480,
      color: "#06B6D4",
      angle: 180,
    },
  ];

  return (
    <div
      className="km-okf-workspace-root"
      style={{
        display: "flex",
        height: "820px",
        backgroundColor: "#0B0F19",
        color: "#F3F7FF",
        fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        borderRadius: "var(--radius-lg)",
        border: "1px solid #1E293B",
        overflow: "hidden",
        boxShadow: "0 25px 60px -15px rgba(0, 0, 0, 0.7)",
      }}
    >
      {/* 1. Left SaaS Sidebar */}
      <aside
        style={{
          width: "72px",
          backgroundColor: "#080C14",
          borderRight: "1px solid #1E293B",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          padding: "18px 0",
          gap: "18px",
          flexShrink: 0,
        }}
      >
        <div
          style={{
            width: "40px",
            height: "40px",
            borderRadius: "10px",
            background: "linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: 800,
            fontSize: "16px",
            color: "#FFFFFF",
            boxShadow: "0 0 16px rgba(59, 130, 246, 0.45)",
            marginBottom: "12px",
          }}
        >
          OKF
        </div>

        {[
          { id: "dashboard", icon: "⊞", label: "Dashboard" },
          { id: "repositories", icon: "📁", label: "Repositories" },
          { id: "graph", icon: "🕸", label: "Knowledge Graph" },
          { id: "agents", icon: "🤖", label: "Agents" },
          { id: "settings", icon: "⚙", label: "Settings" },
        ].map((item) => {
          const isActive = activeSidebarItem === item.id;
          return (
            <button
              key={item.id}
              type="button"
              title={item.label}
              onClick={() => {
                setActiveSidebarItem(item.id);
                if (onNavigateTab && item.id === "dashboard") onNavigateTab("overview");
                if (onNavigateTab && item.id === "agents") onNavigateTab("agents");
              }}
              style={{
                width: "44px",
                height: "44px",
                borderRadius: "10px",
                border: "1px solid",
                borderColor: isActive ? "rgba(6, 182, 212, 0.5)" : "transparent",
                backgroundColor: isActive ? "rgba(6, 182, 212, 0.12)" : "transparent",
                color: isActive ? "#06B6D4" : "#64748B",
                fontSize: "18px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer",
                transition: "all 0.2s ease",
              }}
            >
              {item.icon}
            </button>
          );
        })}
      </aside>

      {/* 2. Main Workspace Layout */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        {/* Top App Header with Breadcrumbs & Action Buttons */}
        <header
          style={{
            height: "56px",
            backgroundColor: "#0D1322",
            borderBottom: "1px solid #1E293B",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "0 22px",
            gap: "16px",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "13px" }}>
            <span style={{ color: "#64748B" }}>Workspaces</span>
            <span style={{ color: "#334155" }}>/</span>
            <span style={{ color: "#64748B" }}>Production</span>
            <span style={{ color: "#334155" }}>/</span>
            <span style={{ color: "#F8FAFC", fontWeight: 600 }}>Knowledge-Base-OKF</span>
            <span
              style={{
                padding: "2px 8px",
                borderRadius: "999px",
                fontSize: "11px",
                fontWeight: 600,
                backgroundColor: "rgba(16, 185, 129, 0.15)",
                color: "#10B981",
                border: "1px solid rgba(16, 185, 129, 0.3)",
                marginLeft: "6px",
              }}
            >
              ● Live Sync
            </span>
          </div>

          {/* Search bar */}
          <div style={{ flex: 1, maxWidth: "340px", position: "relative" }}>
            <input
              type="text"
              placeholder="Search graph (Bézier nodes, claims, frontmatter)…"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: "100%",
                height: "34px",
                backgroundColor: "#080C14",
                border: "1px solid #1E293B",
                borderRadius: "8px",
                padding: "0 12px 0 32px",
                color: "#F8FAFC",
                fontSize: "12.5px",
                outline: "none",
              }}
            />
            <span
              style={{
                position: "absolute",
                left: "10px",
                top: "8px",
                color: "#64748B",
                fontSize: "14px",
              }}
            >
              ⌕
            </span>
          </div>

          {/* Right Header Actions */}
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <button
              type="button"
              className="km-btn km-btn-sm"
              style={{
                backgroundColor: "rgba(30, 41, 59, 0.6)",
                border: "1px solid #334155",
                fontSize: "12px",
              }}
            >
              ⇄ Sync Git
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm"
              style={{
                backgroundColor: "rgba(30, 41, 59, 0.6)",
                border: "1px solid #334155",
                fontSize: "12px",
              }}
            >
              ⤓ Export Bundle
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm km-btn-primary"
              style={{ fontSize: "12px", fontWeight: 600 }}
            >
              🚀 Deploy OKF
            </button>
            <div
              style={{
                width: "32px",
                height: "32px",
                borderRadius: "50%",
                background: "linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "12px",
                fontWeight: 700,
                color: "#FFFFFF",
                marginLeft: "6px",
                border: "1px solid rgba(255,255,255,0.2)",
              }}
            >
              KM
            </div>
          </div>
        </header>

        {/* 3. Main Interactive Graph Canvas */}
        <div
          style={{
            flex: 1,
            position: "relative",
            overflow: "hidden",
            backgroundColor: "#0B0F19",
          }}
        >
          {/* Subtle Dot-Grid Background Pattern */}
          <svg
            width="100%"
            height="100%"
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              pointerEvents: "none",
            }}
          >
            <defs>
              <pattern id="okfDotGrid" width="28" height="28" patternUnits="userSpaceOnUse">
                <circle cx="2" cy="2" r="1.1" fill="#1A2438" />
              </pattern>

              {/* Gradient for Bézier particle flow */}
              <linearGradient id="edgeGradCyan" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#06B6D4" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.3" />
              </linearGradient>
              <linearGradient id="edgeGradAmber" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#F59E0B" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.3" />
              </linearGradient>

              {/* Sweeping Shimmer Linear Gradient */}
              <linearGradient id="shimmerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.1" />
                <stop offset="50%" stopColor="#67E8F9" stopOpacity="0.4" />
                <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.1" />
              </linearGradient>
            </defs>
            <rect width="100%" height="100%" fill="url(#okfDotGrid)" />

            {/* Curved Bézier Connection Paths with Particle Streams */}
            {/* Center Anchor is cx=480, cy=250 */}

            {/* Path 1: Center -> doc-md-1 (top-left: 160, 110) */}
            <path
              id="path-card-1"
              d="M 480 250 C 330 250, 270 110, 160 110"
              fill="none"
              stroke="#06B6D4"
              strokeWidth="1.8"
              opacity="0.65"
            />
            {/* Cyan Particle Pulse along Path 1 */}
            <circle r="4" fill="#67E8F9">
              <animateMotion dur="2.4s" repeatCount="indefinite" path="M 480 250 C 330 250, 270 110, 160 110" />
            </circle>

            {/* Path 2: Center -> doc-yaml-1 (bottom-left: 160, 390) */}
            <path
              id="path-card-2"
              d="M 480 250 C 330 250, 270 390, 160 390"
              fill="none"
              stroke="#F59E0B"
              strokeWidth="1.8"
              opacity="0.65"
            />
            {/* Amber Particle Pulse along Path 2 */}
            <circle r="4" fill="#FBBF24">
              <animateMotion dur="2.8s" repeatCount="indefinite" path="M 480 250 C 330 250, 270 390, 160 390" />
            </circle>

            {/* Path 3: Center -> doc-md-2 (top-right: 800, 110) */}
            <path
              id="path-card-3"
              d="M 480 250 C 630 250, 690 110, 800 110"
              fill="none"
              stroke="#06B6D4"
              strokeWidth="1.8"
              opacity="0.65"
            />
            {/* Cyan Particle Pulse along Path 3 */}
            <circle r="4" fill="#67E8F9">
              <animateMotion dur="2.2s" repeatCount="indefinite" path="M 480 250 C 630 250, 690 110, 800 110" />
            </circle>

            {/* Path 4: Center -> doc-yaml-2 (bottom-right: 800, 390) */}
            <path
              id="path-card-4"
              d="M 480 250 C 630 250, 690 390, 800 390"
              fill="none"
              stroke="#F59E0B"
              strokeWidth="1.8"
              opacity="0.65"
            />
            {/* Amber Particle Pulse along Path 4 */}
            <circle r="4" fill="#FBBF24">
              <animateMotion dur="2.6s" repeatCount="indefinite" path="M 480 250 C 630 250, 690 390, 800 390" />
            </circle>

            {/* Path 5: Center -> Agent-Indexer (480, 40) */}
            <line x1="480" y1="250" x2="480" y2="40" stroke="#3B82F6" strokeWidth="1.6" strokeDasharray="4,4" opacity="0.75" />
            <circle r="3.5" fill="#3B82F6">
              <animateMotion dur="1.8s" repeatCount="indefinite" path="M 480 250 L 480 40" />
            </circle>

            {/* Path 6: Center -> Agent-Query-Bot (480, 470) */}
            <line x1="480" y1="250" x2="480" y2="470" stroke="#06B6D4" strokeWidth="1.6" strokeDasharray="4,4" opacity="0.75" />
            <circle r="3.5" fill="#06B6D4">
              <animateMotion dur="2.0s" repeatCount="indefinite" path="M 480 250 L 480 470" />
            </circle>
          </svg>

          {/* Central Anchor Node: Glowing Primary Folder "Knowledge Bundle (OKF)" */}
          <div
            className="km-float-centered"
            style={{
              position: "absolute",
              left: "480px",
              top: "250px",
              width: "210px",
              padding: "16px 20px",
              backgroundColor: "rgba(15, 23, 42, 0.85)",
              backdropFilter: "blur(12px)",
              borderRadius: "14px",
              border: "1px solid rgba(59, 130, 246, 0.5)",
              boxShadow: "0 0 32px rgba(59, 130, 246, 0.35), inset 0 0 16px rgba(103, 232, 249, 0.15)",
              display: "flex",
              flexDirection: "column",
              gap: "6px",
              zIndex: 10,
              cursor: "pointer",
            }}
          >
            {/* Sweeping Shimmer Light Sheen */}
            <div
              className="km-canvas-shimmer"
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                borderRadius: "14px",
                pointerEvents: "none",
              }}
            />
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <span style={{ fontSize: "20px" }}>📦</span>
              <span
                style={{
                  fontSize: "10.5px",
                  fontWeight: 700,
                  color: "#67E8F9",
                  backgroundColor: "rgba(6, 182, 212, 0.15)",
                  padding: "2px 8px",
                  borderRadius: "999px",
                  border: "1px solid rgba(6, 182, 212, 0.4)",
                }}
              >
                CORE ANCHOR
              </span>
            </div>
            <div style={{ fontWeight: 700, fontSize: "14px", color: "#F8FAFC" }}>
              Knowledge Bundle (OKF)
            </div>
            <div style={{ fontSize: "11px", color: "#94A3B8", fontFamily: "var(--font-mono)" }}>
              did:kyro:bundle-root
            </div>
          </div>

          {/* Glassmorphic Document Cards (.md and YAML Frontmatter) */}
          {documentCards.map((card) => {
            const isHovered = hoveredCardId === card.id;
            const isBottom = card.y > 250;
            return (
              <div
                key={card.id}
                className="km-float-centered"
                onMouseEnter={() => setHoveredCardId(card.id)}
                onMouseLeave={() => setHoveredCardId(null)}
                style={{
                  position: "absolute",
                  left: `${card.x}px`,
                  top: `${card.y}px`,
                  width: "210px",
                  padding: "14px 16px",
                  backgroundColor: isHovered
                    ? "rgba(18, 27, 48, 0.92)"
                    : "rgba(11, 18, 32, 0.80)",
                  backdropFilter: "blur(12px)",
                  borderRadius: "12px",
                  border: "1.5px solid",
                  borderColor: isHovered ? card.badgeColor : "#1E293B",
                  boxShadow: isHovered
                    ? `0 12px 30px -8px rgba(0, 0, 0, 0.8), 0 0 20px ${card.badgeColor}40`
                    : "0 8px 24px -6px rgba(0, 0, 0, 0.6)",
                  transition: "border-color 0.25s, box-shadow 0.25s",
                  cursor: "pointer",
                  zIndex: isHovered ? 25 : 12,
                }}
              >
                {/* Header */}
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    marginBottom: "8px",
                  }}
                >
                  <span
                    style={{
                      fontSize: "11px",
                      fontWeight: 700,
                      color: card.badgeColor,
                      fontFamily: "var(--font-mono)",
                    }}
                  >
                    {card.type}
                  </span>
                  <div style={{ display: "flex", gap: "4px" }}>
                    <span
                      style={{
                        fontSize: "9.5px",
                        padding: "1px 6px",
                        borderRadius: "4px",
                        backgroundColor: "rgba(255,255,255,0.06)",
                        color: "#94A3B8",
                      }}
                    >
                      {card.tagStatus}
                    </span>
                  </div>
                </div>

                {/* Title */}
                <div style={{ fontWeight: 600, fontSize: "13px", color: "#F1F5F9", marginBottom: "6px" }}>
                  {card.title}
                </div>

                {/* Monospaced Key-Value Metadata Preview */}
                <pre
                  style={{
                    margin: 0,
                    padding: "6px 8px",
                    backgroundColor: "#070B14",
                    borderRadius: "6px",
                    fontSize: "10.5px",
                    fontFamily: "var(--font-mono)",
                    color: "#94A3B8",
                    lineHeight: 1.4,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                >
                  {card.yaml}
                </pre>

                {/* Interactive Hover Expanded Tooltip */}
                {isHovered && (
                  <div
                    style={{
                      position: "absolute",
                      ...(isBottom ? { top: "103%" } : { bottom: "103%" }),
                      left: "50%",
                      transform: "translateX(-50%)",
                      width: "250px",
                      backgroundColor: "#060A14",
                      border: `1px solid ${card.badgeColor}`,
                      borderRadius: "8px",
                      padding: "10px 12px",
                      boxShadow: `0 10px 25px -5px rgba(0,0,0,0.85), 0 0 16px ${card.badgeColor}35`,
                      zIndex: 35,
                      pointerEvents: "none",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "11px",
                        fontWeight: 700,
                        color: card.badgeColor,
                        marginBottom: "4px",
                      }}
                    >
                      Raw Preview ({card.title})
                    </div>
                    <div style={{ fontSize: "11px", color: "#CBD5E1", lineHeight: 1.45 }}>
                      {card.rawContent}
                    </div>
                  </div>
                )}
              </div>
            );
          })}

          {/* Outer Edge AI Agent Nodes with Rotating Telemetry Rings & Radial Pulses */}
          {agentNodes.map((agent) => (
            <div
              key={agent.id}
              style={{
                position: "absolute",
                left: `${agent.x}px`,
                top: `${agent.y}px`,
                transform: "translate(-50%, -50%)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                zIndex: 15,
              }}
            >
              {/* Outer Radar Heartbeat Pulse Expanding Outward */}
              <div
                className="km-radar-pulse"
                style={{
                  position: "absolute",
                  width: "60px",
                  height: "60px",
                  borderRadius: "50%",
                  border: `2px solid ${agent.color}`,
                  top: "0px",
                  pointerEvents: "none",
                }}
              />

              {/* 360-Degree Rotating Telemetry Ring */}
              <div
                className="km-telemetry-ring"
                style={{
                  position: "relative",
                  width: "52px",
                  height: "52px",
                  borderRadius: "50%",
                  border: `2px dashed ${agent.color}`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: "rgba(11, 15, 25, 0.9)",
                  boxShadow: `0 0 20px ${agent.color}40`,
                }}
              >
                <div
                  style={{
                    width: "36px",
                    height: "36px",
                    borderRadius: "50%",
                    backgroundColor: "#0F172A",
                    border: `1.5px solid ${agent.color}`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "16px",
                  }}
                >
                  🤖
                </div>
              </div>

              {/* Node Label & Subtext */}
              <div
                style={{
                  marginTop: "6px",
                  textAlign: "center",
                  padding: "2px 8px",
                  backgroundColor: "rgba(11, 15, 25, 0.8)",
                  borderRadius: "4px",
                  border: "1px solid #1E293B",
                }}
              >
                <div style={{ fontSize: "11px", fontWeight: 700, color: "#F8FAFC" }}>
                  {agent.label}
                </div>
                <div style={{ fontSize: "9px", color: agent.color }}>
                  {agent.sub}
                </div>
              </div>
            </div>
          ))}

          {/* Corner Mini-Map */}
          <div
            style={{
              position: "absolute",
              bottom: "20px",
              left: "20px",
              width: "150px",
              height: "90px",
              backgroundColor: "rgba(8, 12, 20, 0.85)",
              backdropFilter: "blur(8px)",
              border: "1px solid #1E293B",
              borderRadius: "8px",
              padding: "6px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              zIndex: 25,
            }}
          >
            <div style={{ fontSize: "10px", color: "#64748B", fontWeight: 600 }}>
              CANVAS MINI-MAP
            </div>
            <div style={{ position: "relative", flex: 1, border: "1px dashed #334155", borderRadius: "4px" }}>
              {/* Dot representation of central node */}
              <div
                style={{
                  position: "absolute",
                  left: "50%",
                  top: "50%",
                  width: "8px",
                  height: "8px",
                  backgroundColor: "#3B82F6",
                  borderRadius: "50%",
                  transform: "translate(-50%, -50%)",
                }}
              />
              {/* Document card dots */}
              <div style={{ position: "absolute", left: "20%", top: "25%", width: "4px", height: "4px", backgroundColor: "#10B981" }} />
              <div style={{ position: "absolute", left: "20%", top: "75%", width: "4px", height: "4px", backgroundColor: "#F59E0B" }} />
              <div style={{ position: "absolute", left: "80%", top: "25%", width: "4px", height: "4px", backgroundColor: "#10B981" }} />
              <div style={{ position: "absolute", left: "80%", top: "75%", width: "4px", height: "4px", backgroundColor: "#F59E0B" }} />
            </div>
          </div>

          {/* Zoom Controls */}
          <div
            style={{
              position: "absolute",
              bottom: "20px",
              right: "20px",
              display: "flex",
              alignItems: "center",
              backgroundColor: "rgba(8, 12, 20, 0.85)",
              backdropFilter: "blur(8px)",
              border: "1px solid #1E293B",
              borderRadius: "8px",
              padding: "4px 8px",
              gap: "6px",
              zIndex: 25,
            }}
          >
            <button
              type="button"
              onClick={() => setZoomLevel((z) => Math.max(50, z - 10))}
              style={{
                background: "none",
                border: "none",
                color: "#94A3B8",
                cursor: "pointer",
                fontSize: "14px",
                fontWeight: 700,
              }}
            >
              −
            </button>
            <span style={{ fontSize: "11px", color: "#F8FAFC", fontFamily: "var(--font-mono)" }}>
              {zoomLevel}%
            </span>
            <button
              type="button"
              onClick={() => setZoomLevel((z) => Math.min(150, z + 10))}
              style={{
                background: "none",
                border: "none",
                color: "#94A3B8",
                cursor: "pointer",
                fontSize: "14px",
                fontWeight: 700,
              }}
            >
              +
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

