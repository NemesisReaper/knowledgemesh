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
  const [toast, setToast] = useState<{ id: string; message: string; type: "success" | "info" | "warning" | "error" } | null>(null);

  const showToast = (message: string, type: "success" | "info" | "warning" | "error" = "info") => {
    const id = Date.now().toString();
    setToast({ id, message, type });
    setTimeout(() => {
      setToast((curr) => (curr?.id === id ? null : curr));
    }, 3800);
  };

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
      category: "Concept",
      title: "KV-Cache Quantization",
      filename: "concept-kv-quant.md",
      summary: "Maintains 99.6% needle retrieval accuracy up to 128k context with 3.7x lower memory footprint.",
      meta: "Confidence: 99.6% · 128k Tokens",
      badgeColor: "#4F46E5",
      x: 180,
      y: 135,
    },
    {
      id: "doc-yaml-1",
      category: "Specification",
      title: "Format Specification",
      filename: "manifest.yaml",
      summary: "Open Knowledge Format v0.2 with canonical RFC 8785 JSON serialization and Ed25519 signing suite.",
      meta: "Node: node-a · Ed25519 Signed",
      badgeColor: "#F59E0B",
      x: 180,
      y: 415,
    },
    {
      id: "doc-md-2",
      category: "Evidence",
      title: "Empirical Benchmark",
      filename: "evidence-benchmark.md",
      summary: "Nsight trace confirms memory bandwidth saturation drops from 94% to 26% under INT4 KV caching.",
      meta: "Reliability: 0.98 · 8xH100 SXM5",
      badgeColor: "#0EA5E9",
      x: 840,
      y: 135,
    },
    {
      id: "doc-yaml-2",
      category: "Provenance",
      title: "Audit & Lineage Trail",
      filename: "lineage-prov.yaml",
      summary: "W3C PROV activity chain with immutable cryptographic generation hash and verification lineage.",
      meta: "Actor: architect@kyro · Gen 1",
      badgeColor: "#10B981",
      x: 840,
      y: 415,
    },
  ];

  const agentNodes = [
    {
      id: "agent-indexer",
      label: "Index Agent",
      sub: "Active · 60Hz",
      x: 510,
      y: 65,
      color: "#4F46E5",
      angle: 0,
    },
    {
      id: "agent-query-bot",
      label: "Query Agent",
      sub: "Active · Traversal",
      x: 510,
      y: 495,
      color: "#0EA5E9",
      angle: 180,
    },
  ];

  const filteredCards = searchQuery.trim()
    ? documentCards.filter(
        (c) =>
          c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          c.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
          c.summary.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : documentCards;

  return (
    <div
      className="km-okf-workspace-root"
      style={{
        display: "flex",
        height: "calc(100vh - 110px)",
        minHeight: "520px",
        backgroundColor: "#FAFAFB",
        color: "#0A0F1D",
        fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        borderRadius: "var(--radius-lg)",
        border: "1px solid #E2E8F0",
        overflow: "hidden",
        boxShadow: "var(--shadow-card)",
      }}
    >
      {/* 1. Left SaaS Sidebar */}
      <aside
        style={{
          width: "72px",
          backgroundColor: "#FFFFFF",
          borderRight: "1px solid #E2E8F0",
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
            background: "linear-gradient(135deg, #4F46E5 0%, #0284C7 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: 800,
            fontSize: "16px",
            color: "#FFFFFF",
            boxShadow: "0 4px 14px rgba(79, 70, 229, 0.25)",
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
                  ? "1px solid #E2E8F0"
                  : "1px solid transparent",
              backgroundColor:
                activeSidebarItem === item.id
                  ? "#F8FAFC"
                  : "transparent",
              color: activeSidebarItem === item.id ? "#4F46E5" : "#64748B",
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
            backgroundColor: "#FFFFFF",
            borderBottom: "1px solid #E2E8F0",
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
            <span style={{ color: "#CBD5E1" }}>/</span>
            <span style={{ color: "#64748B" }}>Production</span>
            <span style={{ color: "#CBD5E1" }}>/</span>
            <span style={{ color: "#0A0F1D", fontWeight: 700 }}>Knowledge-Base-OKF</span>
            <span
              style={{
                marginLeft: "8px",
                padding: "2px 8px",
                borderRadius: "999px",
                fontSize: "11px",
                fontWeight: 600,
                backgroundColor: "rgba(16, 185, 129, 0.12)",
                color: "#059669",
                border: "1px solid rgba(16, 185, 129, 0.25)",
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
                backgroundColor: "#F8FAFC",
                border: "1px solid #E2E8F0",
                borderRadius: "8px",
                padding: "0 12px 0 32px",
                color: "#0A0F1D",
                fontSize: "12.5px",
                outline: "none",
              }}
            />
            <span style={{ position: "absolute", left: "10px", top: "8px", color: "#94A3B8", fontSize: "14px" }}>
              ⌕
            </span>
          </div>

          {/* Actions */}
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => showToast("✓ OKF Git repository synchronized with commit HEAD.", "success")}
            >
              Sync Git
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm"
              onClick={() => showToast("✓ Exported canonical RFC 8785 JCS bundle to downloads.", "success")}
            >
              Export Bundle
            </button>
            <button
              type="button"
              className="km-btn km-btn-sm km-btn-primary"
              onClick={() => showToast("✓ Verified OKF bundle deployed and broadcasted to mesh.", "success")}
            >
              Deploy
            </button>

            {/* Profile Pill */}
            <div
              style={{
                width: "32px",
                height: "32px",
                borderRadius: "50%",
                background: "linear-gradient(135deg, #4F46E5 0%, #0284C7 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "12px",
                fontWeight: 700,
                color: "#FFFFFF",
                marginLeft: "6px",
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
            backgroundColor: "#F8FAFC",
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
              width: "1020px",
              height: "580px",
              transform: `scale(${stageScale.toFixed(3)})`,
              transformOrigin: "center center",
              transition: "transform 0.12s ease",
              flexShrink: 0,
            }}
          >
            {/* Subtle Dot-Grid Background Pattern */}
            <svg
              viewBox="0 0 1020 580"
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
                  <circle cx="2" cy="2" r="1.2" fill="#E2E8F0" />
                </pattern>
                <filter id="neon-glow-react" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur in="SourceGraphic" stdDeviation="3.5" result="blur" />
                  <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
              </defs>
              <rect width="100%" height="100%" fill="url(#okfDotGrid2)" />

              {/* Central Radar Pulse Waves */}
              <circle cx="510" cy="275" r="30" fill="none" stroke="#4F46E5" strokeWidth="2" opacity="0.8">
                <animate attributeName="r" values="30;85" dur="2.8s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.8;0" dur="2.8s" repeatCount="indefinite" />
              </circle>
              <circle cx="510" cy="275" r="30" fill="none" stroke="#7C3AED" strokeWidth="1.5" opacity="0.6">
                <animate attributeName="r" values="30;115" dur="2.8s" begin="1.4s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.6;0" dur="2.8s" begin="1.4s" repeatCount="indefinite" />
              </circle>

              {/* Smooth Curved Connections with Terminal Port Anchors */}
              {/* Top-Left: KV-Cache Quantization (295, 135) to Anchor (390, 255) */}
              <path
                className="km-laser-path-1"
                d="M 295 135 C 345 135, 340 255, 390 255"
                fill="none"
                stroke="#CBD5E1"
                strokeWidth="1.8"
              />
              <circle className="km-ignited-port" cx="295" cy="135" r="5" fill="#4F46E5" stroke="#FFFFFF" strokeWidth="2" />
              <circle className="km-ignited-port" cx="390" cy="255" r="5" fill="#4F46E5" stroke="#FFFFFF" strokeWidth="2" />
              <circle r="8" fill="#4F46E5" opacity="0.45" filter="url(#neon-glow-react)">
                <animateMotion dur="2.2s" repeatCount="indefinite" path="M 295 135 C 345 135, 340 255, 390 255" />
              </circle>
              <circle r="4.5" fill="#6366F1">
                <animateMotion dur="2.2s" repeatCount="indefinite" path="M 295 135 C 345 135, 340 255, 390 255" />
              </circle>
              <circle r="2" fill="#FFFFFF">
                <animateMotion dur="2.2s" repeatCount="indefinite" path="M 295 135 C 345 135, 340 255, 390 255" />
              </circle>

              {/* Bottom-Left: Format Specification (295, 415) to Anchor (390, 295) */}
              <path
                className="km-laser-path-2"
                d="M 295 415 C 345 415, 340 295, 390 295"
                fill="none"
                stroke="#CBD5E1"
                strokeWidth="1.8"
              />
              <circle className="km-ignited-port" cx="295" cy="415" r="5" fill="#F59E0B" stroke="#FFFFFF" strokeWidth="2" />
              <circle className="km-ignited-port" cx="390" cy="295" r="5" fill="#F59E0B" stroke="#FFFFFF" strokeWidth="2" />
              <circle r="8" fill="#F59E0B" opacity="0.45" filter="url(#neon-glow-react)">
                <animateMotion dur="2.6s" repeatCount="indefinite" path="M 295 415 C 345 415, 340 295, 390 295" />
              </circle>
              <circle r="4.5" fill="#F59E0B">
                <animateMotion dur="2.6s" repeatCount="indefinite" path="M 295 415 C 345 415, 340 295, 390 295" />
              </circle>
              <circle r="2" fill="#FFFFFF">
                <animateMotion dur="2.6s" repeatCount="indefinite" path="M 295 415 C 345 415, 340 295, 390 295" />
              </circle>

              {/* Top-Right: Anchor (630, 255) to Empirical Benchmark (725, 135) */}
              <path
                className="km-laser-path-3"
                d="M 630 255 C 680 255, 675 135, 725 135"
                fill="none"
                stroke="#CBD5E1"
                strokeWidth="1.8"
              />
              <circle className="km-ignited-port" cx="630" cy="255" r="5" fill="#0EA5E9" stroke="#FFFFFF" strokeWidth="2" />
              <circle className="km-ignited-port" cx="725" cy="135" r="5" fill="#0EA5E9" stroke="#FFFFFF" strokeWidth="2" />
              <circle r="8" fill="#0EA5E9" opacity="0.45" filter="url(#neon-glow-react)">
                <animateMotion dur="2.0s" repeatCount="indefinite" path="M 630 255 C 680 255, 675 135, 725 135" />
              </circle>
              <circle r="4.5" fill="#0EA5E9">
                <animateMotion dur="2.0s" repeatCount="indefinite" path="M 630 255 C 680 255, 675 135, 725 135" />
              </circle>
              <circle r="2" fill="#FFFFFF">
                <animateMotion dur="2.0s" repeatCount="indefinite" path="M 630 255 C 680 255, 675 135, 725 135" />
              </circle>

              {/* Bottom-Right: Anchor (630, 295) to Audit & Lineage (725, 415) */}
              <path
                className="km-laser-path-4"
                d="M 630 295 C 680 295, 675 415, 725 415"
                fill="none"
                stroke="#CBD5E1"
                strokeWidth="1.8"
              />
              <circle className="km-ignited-port" cx="630" cy="295" r="5" fill="#10B981" stroke="#FFFFFF" strokeWidth="2" />
              <circle className="km-ignited-port" cx="725" cy="415" r="5" fill="#10B981" stroke="#FFFFFF" strokeWidth="2" />
              <circle r="8" fill="#10B981" opacity="0.45" filter="url(#neon-glow-react)">
                <animateMotion dur="2.4s" repeatCount="indefinite" path="M 630 295 C 680 295, 675 415, 725 415" />
              </circle>
              <circle r="4.5" fill="#10B981">
                <animateMotion dur="2.4s" repeatCount="indefinite" path="M 630 295 C 680 295, 675 415, 725 415" />
              </circle>
              <circle r="2" fill="#FFFFFF">
                <animateMotion dur="2.4s" repeatCount="indefinite" path="M 630 295 C 680 295, 675 415, 725 415" />
              </circle>

              {/* Top AI Agent Vertical Connection */}
              <line className="km-laser-vpath" x1="510" y1="220" x2="510" y2="108" stroke="#CBD5E1" strokeWidth="1.6" strokeDasharray="4,4" />
              <circle className="km-ignited-port" cx="510" cy="220" r="4.5" fill="#4F46E5" stroke="#FFFFFF" strokeWidth="1.8" />
              <circle className="km-ignited-port" cx="510" cy="108" r="4.5" fill="#4F46E5" stroke="#FFFFFF" strokeWidth="1.8" />
              <circle r="7" fill="#4F46E5" opacity="0.45" filter="url(#neon-glow-react)">
                <animateMotion dur="1.7s" repeatCount="indefinite" path="M 510 220 L 510 108" />
              </circle>
              <circle r="3.5" fill="#4F46E5">
                <animateMotion dur="1.7s" repeatCount="indefinite" path="M 510 220 L 510 108" />
              </circle>

              {/* Bottom AI Agent Vertical Connection */}
              <line className="km-laser-vpath" x1="510" y1="330" x2="510" y2="440" stroke="#CBD5E1" strokeWidth="1.6" strokeDasharray="4,4" />
              <circle className="km-ignited-port" cx="510" cy="330" r="4.5" fill="#0EA5E9" stroke="#FFFFFF" strokeWidth="1.8" />
              <circle className="km-ignited-port" cx="510" cy="440" r="4.5" fill="#0EA5E9" stroke="#FFFFFF" strokeWidth="1.8" />
              <circle r="7" fill="#0EA5E9" opacity="0.45" filter="url(#neon-glow-react)">
                <animateMotion dur="1.9s" repeatCount="indefinite" path="M 510 330 L 510 440" />
              </circle>
              <circle r="3.5" fill="#0EA5E9">
                <animateMotion dur="1.9s" repeatCount="indefinite" path="M 510 330 L 510 440" />
              </circle>
            </svg>

            {/* Central Anchor Node: Clean Verifiable Document */}
            <div
              className="km-float-centered km-assemble-anchor"
              style={{
                position: "absolute",
                left: "510px",
                top: "275px",
                width: "240px",
                padding: "18px 20px",
                backgroundColor: "#FFFFFF",
                borderRadius: "16px",
                border: "1.5px solid #E2E8F0",
                boxShadow: "0 16px 36px -8px rgba(10, 15, 29, 0.08)",
                display: "flex",
                flexDirection: "column",
                gap: "6px",
                zIndex: 10,
                textAlign: "left",
                transform: "translate(-50%, -50%)",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <span
                  style={{
                    fontSize: "11px",
                    fontWeight: 700,
                    color: "#4F46E5",
                    padding: "2px 8px",
                    borderRadius: "6px",
                    backgroundColor: "rgba(79, 70, 229, 0.08)",
                  }}
                >
                  Mesh Anchor
                </span>
                <span
                  style={{
                    fontSize: "10px",
                    fontWeight: 600,
                    color: "#059669",
                    backgroundColor: "rgba(16, 185, 129, 0.08)",
                    padding: "2px 7px",
                    borderRadius: "999px",
                  }}
                >
                  ✓ Verified
                </span>
              </div>
              <div style={{ fontWeight: 700, fontSize: "14px", color: "#0A0F1D", marginTop: "2px" }}>
                Knowledge Document
              </div>
              <div style={{ fontSize: "11px", color: "#64748B", fontFamily: "var(--font-mono)" }}>
                did:kyro:bundle-root
              </div>
              <div style={{ fontSize: "10.5px", color: "#94A3B8", marginTop: "2px", paddingTop: "6px", borderTop: "1px solid #F1F5F9" }}>
                4 Linked Documents · RFC 8785
              </div>
            </div>

            {/* Document Cards */}
            {filteredCards.map((card) => {
              const isHovered = hoveredCardId === card.id;
              const animClass = card.x < 510 ? (card.y < 275 ? 'km-assemble-top-left' : 'km-assemble-bottom-left') : (card.y < 275 ? 'km-assemble-top-right' : 'km-assemble-bottom-right');
              return (
                <div
                  key={card.id}
                  className={`km-float-centered km-card-${card.id} ${animClass}`}
                  onMouseEnter={() => setHoveredCardId(card.id)}
                  onMouseLeave={() => setHoveredCardId(null)}
                  style={{
                    position: "absolute",
                    left: `${card.x}px`,
                    top: `${card.y}px`,
                    width: "230px",
                    padding: "14px 16px",
                    backgroundColor: "#FFFFFF",
                    borderRadius: "14px",
                    border: "1.5px solid",
                    borderColor: isHovered ? card.badgeColor : "#E2E8F0",
                    boxShadow: isHovered
                      ? `0 16px 32px -4px rgba(10, 15, 29, 0.1), 0 0 1px ${card.badgeColor}`
                      : "0 4px 16px rgba(10, 15, 29, 0.04)",
                    transform: `translate(-50%, -50%) ${isHovered ? "translateY(-3px)" : "translateY(0)"}`,
                    transition: "all 0.18s cubic-bezier(0.16, 1, 0.3, 1)",
                    cursor: "pointer",
                    zIndex: isHovered ? 25 : 12,
                    textAlign: "left",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                    <span
                      style={{
                        fontSize: "10.5px",
                        fontWeight: 700,
                        padding: "2px 8px",
                        borderRadius: "6px",
                        color: card.badgeColor,
                        backgroundColor: `${card.badgeColor}14`,
                      }}
                    >
                      {card.category}
                    </span>
                    <span style={{ fontSize: "10px", fontWeight: 600, color: "#059669", display: "flex", alignItems: "center", gap: "3px" }}>
                      ● Verified
                    </span>
                  </div>
                  <div style={{ fontWeight: 700, fontSize: "13px", color: "#0A0F1D", marginBottom: "2px" }}>
                    {card.title}
                  </div>
                  <div style={{ fontSize: "10.5px", color: "#64748B", fontFamily: "var(--font-mono)", marginBottom: "8px" }}>
                    {card.filename}
                  </div>
                  <div style={{ fontSize: "11px", color: "#334155", lineHeight: 1.45, marginBottom: "10px" }}>
                    {card.summary}
                  </div>
                  <div style={{ fontSize: "10px", fontWeight: 500, color: "#94A3B8", paddingTop: "8px", borderTop: "1px solid #F1F5F9" }}>
                    {card.meta}
                  </div>
                </div>
              );
            })}

            {/* AI Agent Nodes */}
            {agentNodes.map((agent) => {
              const animClass = agent.y < 275 ? 'km-assemble-agent-top' : 'km-assemble-agent-bottom';
              return (
                <div
                  key={agent.id}
                  className={`km-float-centered ${animClass}`}
                  style={{
                    position: "absolute",
                    left: `${agent.x}px`,
                    top: `${agent.y}px`,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    zIndex: 15,
                    transform: "translate(-50%, -50%)",
                  }}
                >
                <div
                  style={{
                    width: "44px",
                    height: "44px",
                    borderRadius: "50%",
                    backgroundColor: "#FFFFFF",
                    border: `1.5px solid ${agent.color}`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    boxShadow: "0 8px 20px -2px rgba(10, 15, 29, 0.08)",
                  }}
                >
                  <span style={{ fontSize: "11px", fontWeight: 800, color: agent.color }}>
                    AI
                  </span>
                </div>
                <div
                  style={{
                    marginTop: "6px",
                    textAlign: "center",
                    padding: "3px 10px",
                    backgroundColor: "#FFFFFF",
                    borderRadius: "20px",
                    border: "1px solid #E2E8F0",
                    boxShadow: "0 2px 8px rgba(10, 15, 29, 0.04)",
                  }}
                >
                  <div style={{ fontSize: "11px", fontWeight: 600, color: "#0A0F1D" }}>
                    {agent.label}
                  </div>
                  <div style={{ fontSize: "9.5px", color: "#059669", fontWeight: 500 }}>
                    {agent.sub}
                  </div>
                </div>
              </div>
              );
            })}
          </div>

          {/* Canvas Mini-Map */}
          <div
            style={{
              position: "absolute",
              bottom: "16px",
              left: "16px",
              width: "120px",
              height: "70px",
              backgroundColor: "rgba(255, 255, 255, 0.92)",
              border: "1px solid #E2E8F0",
              borderRadius: "8px",
              padding: "6px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              pointerEvents: "none",
              zIndex: 25,
              boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
            }}
          >
            <span style={{ fontSize: "9px", fontWeight: 750, color: "#64748B", letterSpacing: "0.05em" }}>
              GRAPH MINI-MAP
            </span>
            <div style={{ position: "relative", flex: 1, border: "1px dashed #CBD5E1", borderRadius: "3px", marginTop: "4px", backgroundColor: "#F8FAFC" }}>
              <div style={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%,-50%)", width: "12px", height: "8px", backgroundColor: "#4F46E5", borderRadius: "1px" }} />
              <div style={{ position: "absolute", top: "20%", left: "20%", width: "6px", height: "4px", backgroundColor: "#059669", borderRadius: "1px" }} />
              <div style={{ position: "absolute", bottom: "20%", left: "20%", width: "6px", height: "4px", backgroundColor: "#D97706", borderRadius: "1px" }} />
              <div style={{ position: "absolute", top: "20%", right: "20%", width: "6px", height: "4px", backgroundColor: "#059669", borderRadius: "1px" }} />
              <div style={{ position: "absolute", bottom: "20%", right: "20%", width: "6px", height: "4px", backgroundColor: "#D97706", borderRadius: "1px" }} />
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
              backgroundColor: "rgba(255, 255, 255, 0.95)",
              border: "1px solid #E2E8F0",
              borderRadius: "8px",
              padding: "4px 8px",
              zIndex: 25,
              boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
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
            <span style={{ fontSize: "11px", fontFamily: "var(--font-mono)", color: "#334155", minWidth: "40px", textAlign: "center" }}>
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

      {toast && (
        <div className="km-toast-container" role="region" aria-live="polite">
          <div className={`km-toast ${toast.type}`}>
            <div className="km-toast-body">
              <div className="km-toast-icon">
                {toast.type === "success" ? "✓" : toast.type === "error" ? "✕" : toast.type === "warning" ? "⚠" : "ℹ"}
              </div>
              <div className="km-toast-message">{toast.message}</div>
            </div>
            <button
              type="button"
              className="km-modal-close"
              style={{ width: "24px", height: "24px", fontSize: "11px" }}
              onClick={() => setToast(null)}
              aria-label="Dismiss"
            >
              ✕
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
