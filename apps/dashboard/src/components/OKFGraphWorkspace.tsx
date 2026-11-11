"use client";

import React, { useEffect, useRef, useState } from "react";

export function OKFGraphWorkspace({
  onNavigateTab,
}: {
  onNavigateTab?: (tab: string) => void;
}) {
  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const [hoveredCardId, setHoveredCardId] = useState<string | null>("doc-md-1");
  const [activeSidebarItem, setActiveSidebarItem] = useState<string>("graph");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [stageScale, setStageScale] = useState<number>(1);

  // Dynamic auto-fit scaling so the entire illustration is 100% visible
  useEffect(() => {
    function computeScale() {
      if (!containerRef.current) return;
      const cw = containerRef.current.clientWidth || 960;
      const ch = containerRef.current.clientHeight || 520;
      const autoScale = Math.min((cw - 36) / 960, (ch - 36) / 520, 1.05);
      const zoomFactor = zoomLevel / 100;
      setStageScale(Math.max(0.35, autoScale * zoomFactor));
    }

    computeScale();
    const ro = new ResizeObserver(computeScale);
    if (containerRef.current) ro.observe(containerRef.current);
    window.addEventListener("resize", computeScale);

    return () => {
      ro.disconnect();
      window.removeEventListener("resize", computeScale);
    };
  }, [zoomLevel]);

  const documentCards = [
    {
      id: "doc-md-1",
      title: "concept-kv-quant.md",
      type: "Markdown (.md)",
      tagType: "type: concept",
      tagStatus: "status: verified",
      badgeColor: "#10B981", // emerald
      x: 180,
      y: 125,
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
      x: 180,
      y: 375,
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
      x: 780,
      y: 125,
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
      x: 780,
      y: 375,
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
      y: 55,
      color: "#3B82F6",
      angle: 0,
    },
    {
      id: "agent-query-bot",
      label: "Agent-Query-Bot",
      sub: "Context Traversal",
      x: 480,
      y: 445,
      color: "#06B6D4",
      angle: 180,
    },
  ];

  const filteredCards = searchQuery.trim()
    ? documentCards.filter(
        (c) =>
          c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          c.yaml.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : documentCards;

  return (
    <div
      className="km-okf-workspace-root"
      style={{
        display: "flex",
        height: "calc(100vh - 110px)",
        minHeight: "520px",
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
          backgroundColor: "#070B14",
          borderRight: "1px solid #1E293B",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          padding: "16px 0",
          gap: "12px",
          flexShrink: 0,
        }}
      >
        <div
          style={{
            width: "42px",
            height: "42px",
            borderRadius: "10px",
            background: "linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: 800,
            fontSize: "16px",
            color: "#FFFFFF",
            boxShadow: "0 0 16px rgba(59, 130, 246, 0.4)",
            marginBottom: "8px",
          }}
        >
          KY
        </div>

        {[
          { id: "overview", icon: "⊞", title: "Overview", tab: "overview" },
          { id: "repo", icon: "⊞", title: "Repositories", tab: "knowledge" },
          { id: "graph", icon: "☍", title: "Knowledge Graph", tab: "okf-graph" },
          { id: "agents", icon: "▲", title: "AI Agents", tab: "agents" },
          { id: "settings", icon: "⎈", title: "Settings", tab: "settings" },
        ].map((item) => (
          <button
            key={item.id}
            type="button"
            title={item.title}
            onClick={() => {
              setActiveSidebarItem(item.id);
              if (onNavigateTab && item.tab) onNavigateTab(item.tab);
            }}
            style={{
              width: "44px",
              height: "44px",
              borderRadius: "10px",
              border:
                activeSidebarItem === item.id
                  ? "1px solid rgba(6, 182, 212, 0.5)"
                  : "none",
              backgroundColor:
                activeSidebarItem === item.id
                  ? "rgba(6, 182, 212, 0.12)"
                  : "transparent",
              color: activeSidebarItem === item.id ? "#06B6D4" : "#64748B",
              fontSize: "18px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              transition: "all 0.15s ease",
            }}
          >
            {item.icon}
          </button>
        ))}
      </aside>

      {/* 2. Main Workspace Layout */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}
      >
        {/* Workspace Top Header Bar */}
        <header
          style={{
            height: "56px",
            backgroundColor: "#0D1322",
            borderBottom: "1px solid #1E293B",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "0 20px",
            gap: "16px",
            flexShrink: 0,
          }}
        >
          {/* Breadcrumb / Path */}
          <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "13px" }}>
            <span style={{ color: "#64748B" }}>Workspaces</span>
            <span style={{ color: "#334155" }}>/</span>
            <span style={{ color: "#64748B" }}>Production</span>
            <span style={{ color: "#334155" }}>/</span>
            <span style={{ color: "#F8FAFC", fontWeight: 600 }}>Knowledge-Base-OKF</span>
            <span
              style={{
                marginLeft: "8px",
                padding: "2px 8px",
                borderRadius: "999px",
                fontSize: "11px",
                fontWeight: 600,
                backgroundColor: "rgba(16, 185, 129, 0.15)",
                color: "#10B981",
                border: "1px solid rgba(16, 185, 129, 0.3)",
              }}
            >
              ● Live Sync
            </span>
          </div>

          {/* Search graph */}
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
            <span style={{ position: "absolute", left: "10px", top: "8px", color: "#64748B", fontSize: "14px" }}>
              ⌕
            </span>
          </div>

          {/* Actions */}
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => alert("Git Sync: OKF repository synchronized with commit HEAD.")}
            >
              Sync Git
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => alert("Export Bundle: Canonical RFC 8785 JCS payload downloaded.")}
            >
              Export Bundle
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm km-btn-primary"
              onClick={() => alert("Deploy: Verified OKF knowledge published to federated mesh.")}
            >
              Deploy
            </button>

            {/* Profile Pill */}
            <div
              style={{
                width: "32px",
                height: "32px",
                borderRadius: "50%",
                background: "linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "12px",
                fontWeight: 700,
                color: "#FFFFFF",
                marginLeft: "6px",
                border: "1.5px solid rgba(6, 182, 212, 0.6)",
              }}
            >
              KY
            </div>
          </div>
        </header>

        {/* 3. Main Interactive Graph Canvas (Auto-Scaling Stage Wrapper) */}
        <div
          ref={containerRef}
          style={{
            flex: 1,
            position: "relative",
            overflow: "hidden",
            backgroundColor: "#080C14",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            minHeight: 0,
            minWidth: 0,
            width: "100%",
            height: "100%",
          }}
        >
          {/* Stage scaled dynamically to guarantee 100% visibility */}
          <div
            style={{
              position: "relative",
              width: "960px",
              height: "520px",
              transform: `scale(${stageScale.toFixed(3)})`,
              transformOrigin: "center center",
              transition: "transform 0.12s ease",
              flexShrink: 0,
            }}
          >
            {/* Subtle Dot-Grid Background Pattern */}
            <svg
              viewBox="0 0 960 520"
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
                <pattern id="okfDotGrid2" width="24" height="24" patternUnits="userSpaceOnUse">
                  <circle cx="2" cy="2" r="1.2" fill="#1E293B" opacity="0.65" />
                </pattern>
              </defs>
              <rect width="100%" height="100%" fill="url(#okfDotGrid2)" />

              {/* Curved Bézier Connection Paths with Particle Streams */}
              {/* Path 1: Center (480, 250) -> Top-Left Card (180, 125) */}
              <path
                d="M 480 250 C 330 250, 270 125, 180 125"
                fill="none"
                stroke="#06B6D4"
                strokeWidth="1.8"
                opacity="0.65"
              />
              <circle r="4" fill="#67E8F9">
                <animateMotion dur="2.4s" repeatCount="indefinite" path="M 480 250 C 330 250, 270 125, 180 125" />
              </circle>

              {/* Path 2: Center (480, 250) -> Bottom-Left Card (180, 375) */}
              <path
                d="M 480 250 C 330 250, 270 375, 180 375"
                fill="none"
                stroke="#F59E0B"
                strokeWidth="1.8"
                opacity="0.65"
              />
              <circle r="4" fill="#FBBF24">
                <animateMotion dur="2.8s" repeatCount="indefinite" path="M 480 250 C 330 250, 270 375, 180 375" />
              </circle>

              {/* Path 3: Center (480, 250) -> Top-Right Card (780, 125) */}
              <path
                d="M 480 250 C 630 250, 690 125, 780 125"
                fill="none"
                stroke="#06B6D4"
                strokeWidth="1.8"
                opacity="0.65"
              />
              <circle r="4" fill="#67E8F9">
                <animateMotion dur="2.2s" repeatCount="indefinite" path="M 480 250 C 630 250, 690 125, 780 125" />
              </circle>

              {/* Path 4: Center (480, 250) -> Bottom-Right Card (780, 375) */}
              <path
                d="M 480 250 C 630 250, 690 375, 780 375"
                fill="none"
                stroke="#F59E0B"
                strokeWidth="1.8"
                opacity="0.65"
              />
              <circle r="4" fill="#FBBF24">
                <animateMotion dur="2.6s" repeatCount="indefinite" path="M 480 250 C 630 250, 690 375, 780 375" />
              </circle>

              {/* Path 5: Center -> Top Agent (480, 55) */}
              <line x1="480" y1="250" x2="480" y2="55" stroke="#3B82F6" strokeWidth="1.6" strokeDasharray="4,4" opacity="0.75" />
              <circle r="3.5" fill="#3B82F6">
                <animateMotion dur="1.8s" repeatCount="indefinite" path="M 480 250 L 480 55" />
              </circle>

              {/* Path 6: Center -> Bottom Agent (480, 445) */}
              <line x1="480" y1="250" x2="480" y2="445" stroke="#06B6D4" strokeWidth="1.6" strokeDasharray="4,4" opacity="0.75" />
              <circle r="3.5" fill="#06B6D4">
                <animateMotion dur="2.0s" repeatCount="indefinite" path="M 480 250 L 480 445" />
              </circle>
            </svg>

            {/* Central Anchor Node: Glowing Primary Folder */}
            <div
              className="km-float-centered"
              style={{
                position: "absolute",
                left: "480px",
                top: "250px",
                width: "210px",
                padding: "16px 20px",
                backgroundColor: "rgba(15, 23, 42, 0.92)",
                backdropFilter: "blur(14px)",
                borderRadius: "14px",
                border: "1.5px solid rgba(59, 130, 246, 0.65)",
                boxShadow: "0 0 32px rgba(59, 130, 246, 0.4)",
                display: "flex",
                flexDirection: "column",
                gap: "6px",
                zIndex: 10,
              }}
            >
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <span style={{ fontSize: "12px", fontWeight: 800, color: "#38bdf8", padding: "2px 7px", borderRadius: "5px", background: "rgba(56,189,248,0.18)", border: "1px solid rgba(56,189,248,0.4)" }}>
                  OKF
                </span>
                <span
                  style={{
                    fontSize: "10px",
                    fontWeight: 700,
                    color: "#67E8F9",
                    backgroundColor: "rgba(6, 182, 212, 0.18)",
                    padding: "2px 8px",
                    borderRadius: "999px",
                    border: "1px solid rgba(6, 182, 212, 0.45)",
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

            {/* Glassmorphic Document Cards */}
            {filteredCards.map((card) => {
              const isHovered = hoveredCardId === card.id;
              const isBottom = card.y > 250;
              return (
                <div
                  key={card.id}
                  className="km-float-centered"
                  onMouseEnter={() => setHoveredCardId(card.id)}
                  style={{
                    position: "absolute",
                    left: `${card.x}px`,
                    top: `${card.y}px`,
                    width: "210px",
                    padding: "12px 14px",
                    backgroundColor: "rgba(14, 20, 35, 0.88)",
                    backdropFilter: "blur(12px)",
                    borderRadius: "12px",
                    border: "1.5px solid",
                    borderColor: isHovered ? card.badgeColor : "rgba(101, 153, 255, 0.25)",
                    boxShadow: isHovered
                      ? `0 10px 24px -4px rgba(0, 0, 0, 0.7), 0 0 18px ${card.badgeColor}45`
                      : "var(--shadow-card)",
                    transition: "border-color 0.2s, box-shadow 0.2s",
                    cursor: "pointer",
                    zIndex: isHovered ? 25 : 12,
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                    <span style={{ fontSize: "10px", fontWeight: 700, padding: "2px 6px", borderRadius: "4px", color: card.badgeColor, backgroundColor: `${card.badgeColor}20` }}>
                      {card.title.endsWith(".md") ? ".md" : "YAML"}
                    </span>
                    <div style={{ display: "flex", gap: "4px" }}>
                      <span style={{ fontSize: "9px", padding: "1px 5px", borderRadius: "3px", background: "rgba(255,255,255,0.06)", color: "#94A3B8" }}>
                        {card.tagType}
                      </span>
                      <span style={{ fontSize: "9px", padding: "1px 5px", borderRadius: "3px", background: "rgba(255,255,255,0.06)", color: "#94A3B8" }}>
                        {card.tagStatus}
                      </span>
                    </div>
                  </div>
                  <div style={{ fontWeight: 600, fontSize: "12.5px", color: "#F1F5F9", marginBottom: "6px" }}>
                    {card.title}
                  </div>
                  <pre
                    style={{
                      margin: 0,
                      padding: "6px 8px",
                      backgroundColor: "#070B14",
                      borderRadius: "6px",
                      fontSize: "10px",
                      fontFamily: "var(--font-mono)",
                      color: "#94A3B8",
                      lineHeight: 1.35,
                      overflow: "hidden",
                    }}
                  >
                    {card.yaml}
                  </pre>

                  {/* INWARD-OPENING TOOLTIP (NEVER CLIPS OUT OF STAGE) */}
                  {isHovered && (
                    <div
                      style={{
                        position: "absolute",
                        ...(isBottom ? { bottom: "103%" } : { top: "103%" }),
                        left: "50%",
                        transform: "translateX(-50%)",
                        width: "240px",
                        maxHeight: "140px",
                        overflowY: "auto",
                        backgroundColor: "#060A14",
                        border: `1px solid ${card.badgeColor}`,
                        borderRadius: "8px",
                        padding: "10px 12px",
                        boxShadow: `0 12px 28px -4px rgba(0,0,0,0.85), 0 0 16px ${card.badgeColor}35`,
                        zIndex: 35,
                        pointerEvents: "none",
                      }}
                    >
                      <div style={{ fontSize: "11px", fontWeight: 700, color: card.badgeColor, marginBottom: "4px" }}>
                        Raw Preview ({card.title})
                      </div>
                      <div style={{ fontSize: "10.5px", color: "#CBD5E1", lineHeight: 1.4 }}>
                        {card.rawContent}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}

            {/* AI Agent Nodes */}
            {agentNodes.map((agent) => (
              <div
                key={agent.id}
                className="km-float-centered"
                style={{
                  position: "absolute",
                  left: `${agent.x}px`,
                  top: `${agent.y}px`,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  zIndex: 15,
                }}
              >
                <div
                  className="km-radar-pulse"
                  style={{
                    position: "absolute",
                    width: "58px",
                    height: "58px",
                    borderRadius: "50%",
                    border: `2px solid ${agent.color}`,
                    top: "0px",
                    pointerEvents: "none",
                  }}
                />
                <div
                  className="km-telemetry-ring"
                  style={{
                    position: "relative",
                    width: "50px",
                    height: "50px",
                    borderRadius: "50%",
                    border: `2px dashed ${agent.color}`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    backgroundColor: "rgba(11, 15, 25, 0.92)",
                    boxShadow: `0 0 20px ${agent.color}45`,
                  }}
                >
                  <div
                    style={{
                      width: "34px",
                      height: "34px",
                      borderRadius: "50%",
                      backgroundColor: "#0F172A",
                      border: `1.5px solid ${agent.color}`,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "11px",
                      fontWeight: 800,
                      color: agent.color,
                    }}
                  >
                    AI
                  </div>
                </div>
                <div
                  style={{
                    marginTop: "6px",
                    textAlign: "center",
                    padding: "2px 8px",
                    backgroundColor: "rgba(11, 15, 25, 0.9)",
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
          </div>

          {/* Canvas Mini-Map */}
          <div
            style={{
              position: "absolute",
              bottom: "16px",
              left: "16px",
              width: "120px",
              height: "70px",
              backgroundColor: "rgba(11, 15, 25, 0.88)",
              border: "1px solid #1E293B",
              borderRadius: "6px",
              padding: "6px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              pointerEvents: "none",
              zIndex: 25,
            }}
          >
            <span style={{ fontSize: "9px", fontWeight: 700, color: "#64748B", letterSpacing: "0.05em" }}>
              GRAPH MINI-MAP
            </span>
            <div style={{ position: "relative", flex: 1, border: "1px dashed #334155", borderRadius: "3px", marginTop: "4px" }}>
              <div style={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%,-50%)", width: "12px", height: "8px", backgroundColor: "#3B82F6", borderRadius: "1px" }} />
              <div style={{ position: "absolute", top: "20%", left: "20%", width: "6px", height: "4px", backgroundColor: "#10B981", borderRadius: "1px" }} />
              <div style={{ position: "absolute", bottom: "20%", left: "20%", width: "6px", height: "4px", backgroundColor: "#F59E0B", borderRadius: "1px" }} />
              <div style={{ position: "absolute", top: "20%", right: "20%", width: "6px", height: "4px", backgroundColor: "#10B981", borderRadius: "1px" }} />
              <div style={{ position: "absolute", bottom: "20%", right: "20%", width: "6px", height: "4px", backgroundColor: "#F59E0B", borderRadius: "1px" }} />
            </div>
          </div>

          {/* Zoom Controls */}
          <div
            style={{
              position: "absolute",
              bottom: "16px",
              right: "16px",
              display: "flex",
              alignItems: "center",
              gap: "6px",
              backgroundColor: "rgba(11, 15, 25, 0.92)",
              border: "1px solid #1E293B",
              borderRadius: "8px",
              padding: "4px 8px",
              zIndex: 25,
            }}
          >
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => setZoomLevel((z) => Math.max(50, z - 10))}
              style={{ padding: "2px 8px" }}
            >
              −
            </button>
            <span style={{ fontSize: "11px", fontFamily: "var(--font-mono)", color: "#94A3B8", minWidth: "40px", textAlign: "center" }}>
              {zoomLevel}%
            </span>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => setZoomLevel((z) => Math.min(150, z + 10))}
              style={{ padding: "2px 8px" }}
            >
              +
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => setZoomLevel(100)}
              style={{ padding: "2px 8px", fontSize: "10px" }}
            >
              Reset
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
