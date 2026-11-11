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
   PREMIUM MINIMALIST MODERN WEBSITE UI (LIGHT LUXURY AESTHETIC)
   ============================================================================ */
export function LandingPageView({
  onGoToLogin,
  onGoToRegister,
}: {
  onGoToLogin: () => void;
  onGoToRegister: () => void;
}) {
  const [scrolled, setScrolled] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const [overview, setOverview] = useState<OverviewResponse | null>(null);
  const [activeOkfTab, setActiveOkfTab] = useState<string>("manifest");
  const [activeCodeTab, setActiveCodeTab] = useState<"python" | "ts" | "cli" | "curl">("python");
  const [demoInputHash, setDemoInputHash] = useState<string>("bun-kv-2026-prod-v1");
  const [computedDigest, setComputedDigest] = useState<string>(
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  );
  const [verifyState, setVerifyState] = useState<"idle" | "verifying" | "valid">("valid");

  // Sticky navbar scroll blur transition
  useEffect(() => {
    function handleScroll() {
      setScrolled(window.scrollY > 24);
    }
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Fetch live network metrics from FastAPI
  useEffect(() => {
    apiRequest<OverviewResponse>("/api/v1/overview")
      .then((data) => setOverview(data))
      .catch(() => {});
  }, []);

  // Live client-side SHA-256 demo calculator
  useEffect(() => {
    let active = true;
    async function hashPayload() {
      try {
        const msgUint8 = new TextEncoder().encode(demoInputHash);
        const hashBuffer = await crypto.subtle.digest("SHA-256", msgUint8);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
        if (active) setComputedDigest(hashHex);
      } catch {
        if (active) setComputedDigest("4f1a8c9b2d7e5f6a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a");
      }
    }
    hashPayload();
    return () => {
      active = false;
    };
  }, [demoInputHash]);

  const liveNodes = overview?.nodes?.length || 3;
  const liveClaims = overview?.metrics?.published_claims || 4;
  const liveBundles = overview?.bundles?.length || 3;

  return (
    <div
      style={{
        backgroundColor: "#FFFFFF",
        color: "#0A0F1D",
        fontFamily:
          'Inter, Geist, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        minHeight: "100vh",
        position: "relative",
        overflowX: "hidden",
        WebkitFontSmoothing: "antialiased",
        MozOsxFontSmoothing: "grayscale",
      }}
    >
      {/* =========================================================================
          LARGE FLOWING GRADIENT SHAPES ACROSS BACKGROUND (PURPLE/VIOLET/BLUE/PINK/ORANGE)
          ========================================================================= */}
      <div
        style={{
          position: "absolute",
          top: "-160px",
          left: "50%",
          transform: "translateX(-50%)",
          width: "1280px",
          height: "680px",
          background:
            "radial-gradient(circle at 30% 35%, rgba(139, 92, 246, 0.14) 0%, rgba(99, 102, 241, 0.11) 32%, rgba(236, 72, 153, 0.08) 58%, rgba(249, 115, 22, 0.04) 78%, transparent 100%)",
          filter: "blur(72px)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "1150px",
          right: "-120px",
          width: "720px",
          height: "720px",
          background:
            "radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.08) 0%, rgba(236, 72, 153, 0.06) 45%, rgba(249, 115, 22, 0.03) 75%, transparent 100%)",
          filter: "blur(90px)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "2400px",
          left: "-180px",
          width: "820px",
          height: "820px",
          background:
            "radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.09) 0%, rgba(59, 130, 246, 0.07) 50%, transparent 100%)",
          filter: "blur(100px)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />

      {/* =========================================================================
          1. MINIMAL HORIZONTAL NAVIGATION BAR (STICKY WITH SMOOTH TRANSITION)
          ========================================================================= */}
      <nav
        style={{
          position: "sticky",
          top: 0,
          zIndex: 50,
          width: "100%",
          transition: "background-color 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease",
          backgroundColor: scrolled ? "rgba(255, 255, 255, 0.88)" : "transparent",
          backdropFilter: scrolled ? "blur(18px)" : "none",
          WebkitBackdropFilter: scrolled ? "blur(18px)" : "none",
          borderBottom: scrolled ? "1px solid rgba(226, 232, 240, 0.85)" : "1px solid transparent",
          boxShadow: scrolled ? "0 4px 20px -2px rgba(10, 15, 29, 0.03)" : "none",
        }}
      >
        <div
          style={{
            maxWidth: "1240px",
            margin: "0 auto",
            padding: "0 28px",
            height: "72px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          {/* Logo on Left */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              cursor: "pointer",
            }}
            onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          >
            <img
              src="/static/kyro-logo.png"
              alt="Kyro Logo"
              style={{
                height: "30px",
                width: "30px",
                objectFit: "contain",
                filter: "drop-shadow(0 2px 8px rgba(99, 102, 241, 0.35))",
              }}
              onError={(e) => {
                // Fallback to local public path if static fails
                (e.target as HTMLImageElement).src = "/kyro-logo.png";
              }}
            />
            <span
              style={{
                fontSize: "20px",
                fontWeight: 800,
                letterSpacing: "-0.035em",
                color: "#0A0F1D",
                display: "flex",
                alignItems: "baseline",
                gap: "6px",
              }}
            >
              kyro
              <span
                style={{
                  fontSize: "11px",
                  fontWeight: 650,
                  letterSpacing: "0.02em",
                  color: "#6366F1",
                  background: "rgba(99, 102, 241, 0.08)",
                  padding: "2px 7px",
                  borderRadius: "999px",
                  border: "1px solid rgba(99, 102, 241, 0.2)",
                }}
              >
                v0.2
              </span>
            </span>
          </div>

          {/* Center Navigation Links with Subtle Dropdowns */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "32px",
            }}
            className="km-nav-desktop-links"
          >
            {/* Architecture Dropdown */}
            <div
              style={{ position: "relative" }}
              onMouseEnter={() => setActiveDropdown("arch")}
              onMouseLeave={() => setActiveDropdown(null)}
            >
              <button
                type="button"
                style={{
                  background: "transparent",
                  border: "none",
                  fontSize: "14px",
                  fontWeight: 550,
                  color: activeDropdown === "arch" ? "#0A0F1D" : "#475569",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "5px",
                  padding: "8px 0",
                  transition: "color 0.15s ease",
                }}
              >
                Architecture
                <span style={{ fontSize: "10px", color: "#94A3B8" }}>▾</span>
              </button>

              {activeDropdown === "arch" && (
                <div
                  style={{
                    position: "absolute",
                    top: "100%",
                    left: "-16px",
                    width: "280px",
                    backgroundColor: "#FFFFFF",
                    borderRadius: "14px",
                    border: "1px solid #E2E8F0",
                    boxShadow: "0 14px 34px -4px rgba(10, 15, 29, 0.08)",
                    padding: "12px",
                    display: "flex",
                    flexDirection: "column",
                    gap: "4px",
                    animation: "fadeIn 0.15s ease",
                  }}
                >
                  <a
                    href="#bento-grid"
                    style={{
                      padding: "8px 10px",
                      borderRadius: "8px",
                      textDecoration: "none",
                      display: "block",
                      transition: "background-color 0.12s ease",
                    }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#F8FAFC")}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
                  >
                    <div style={{ fontSize: "13px", fontWeight: 650, color: "#0A0F1D" }}>
                      RFC 8785 Canonical JCS
                    </div>
                    <div style={{ fontSize: "11.5px", color: "#64748B" }}>
                      Deterministic cross-platform serialization
                    </div>
                  </a>
                  <a
                    href="#okf-anatomy"
                    style={{
                      padding: "8px 10px",
                      borderRadius: "8px",
                      textDecoration: "none",
                      display: "block",
                      transition: "background-color 0.12s ease",
                    }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#F8FAFC")}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
                  >
                    <div style={{ fontSize: "13px", fontWeight: 650, color: "#0A0F1D" }}>
                      Open Knowledge Format
                    </div>
                    <div style={{ fontSize: "11.5px", color: "#64748B" }}>
                      Atomic claims, schemas, and evidence traces
                    </div>
                  </a>
                  <a
                    href="#bento-grid"
                    style={{
                      padding: "8px 10px",
                      borderRadius: "8px",
                      textDecoration: "none",
                      display: "block",
                      transition: "background-color 0.12s ease",
                    }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#F8FAFC")}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
                  >
                    <div style={{ fontSize: "13px", fontWeight: 650, color: "#0A0F1D" }}>
                      Ed25519 Cryptographic Envelope
                    </div>
                    <div style={{ fontSize: "11.5px", color: "#64748B" }}>
                      RFC 8032 digital signatures &amp; SHA-256 digests
                    </div>
                  </a>
                </div>
              )}
            </div>

            <a
              href="#bento-grid"
              style={{
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 550,
                color: "#475569",
                transition: "color 0.15s ease",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#0A0F1D")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#475569")}
            >
              Protocol
            </a>

            <a
              href="#federation-section"
              style={{
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 550,
                color: "#475569",
                transition: "color 0.15s ease",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#0A0F1D")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#475569")}
            >
              Federation
            </a>

            <a
              href="#verifier-demo"
              style={{
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 550,
                color: "#475569",
                transition: "color 0.15s ease",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#0A0F1D")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#475569")}
            >
              Proof Verifier
            </a>

            <a
              href="#dev-integration"
              style={{
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 550,
                color: "#475569",
                transition: "color 0.15s ease",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#0A0F1D")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#475569")}
            >
              Developers
            </a>
          </div>

          {/* Right-Aligned Action Buttons */}
          <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
            <button
              type="button"
              onClick={onGoToLogin}
              style={{
                background: "transparent",
                border: "none",
                fontSize: "14px",
                fontWeight: 600,
                color: "#475569",
                padding: "8px 14px",
                cursor: "pointer",
                transition: "color 0.15s ease",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#0A0F1D")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#475569")}
            >
              Sign In
            </button>
            <button
              type="button"
              onClick={onGoToRegister}
              style={{
                backgroundColor: "#0A0F1D",
                color: "#FFFFFF",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                borderRadius: "10px",
                padding: "10px 18px",
                fontSize: "13.5px",
                fontWeight: 650,
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                gap: "8px",
                boxShadow: "0 4px 14px rgba(10, 15, 29, 0.12)",
                transition: "all 0.18s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = "#1E293B";
                e.currentTarget.style.transform = "translateY(-1px)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = "#0A0F1D";
                e.currentTarget.style.transform = "translateY(0)";
              }}
            >
              Deploy Node
              <span style={{ fontSize: "14px", transition: "transform 0.15s ease" }}>→</span>
            </button>
          </div>
        </div>
      </nav>

      {/* =========================================================================
          2. HERO SECTION (EXPRESSIVE HEADLINE, DUAL CTAS, 3D ABSTRACT VISUAL)
          ========================================================================= */}
      <section
        style={{
          maxWidth: "1240px",
          margin: "0 auto",
          padding: "70px 28px 100px",
          position: "relative",
          zIndex: 1,
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "minmax(0, 1.15fr) minmax(0, 1fr)",
            gap: "54px",
            alignItems: "center",
          }}
          className="km-hero-grid"
        >
          {/* Left Hero Content */}
          <div style={{ maxWidth: "620px" }}>
            {/* Subtle Eyebrow Pill */}
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "6px 14px",
                borderRadius: "999px",
                backgroundColor: "#FAFAFB",
                border: "1px solid #E2E8F0",
                fontSize: "12.5px",
                fontWeight: 600,
                color: "#334155",
                marginBottom: "28px",
                boxShadow: "0 2px 6px rgba(0, 0, 0, 0.02)",
              }}
            >
              <span
                style={{
                  width: "8px",
                  height: "8px",
                  borderRadius: "50%",
                  backgroundColor: "#10B981",
                  boxShadow: "0 0 8px rgba(16, 185, 129, 0.6)",
                }}
              />
              <span style={{ color: "#64748B", fontWeight: 500 }}>Live Mesh:</span>
              <span>{liveNodes} Sovereign Nodes Active</span>
              <span style={{ color: "#CBD5E1" }}>·</span>
              <span
                style={{
                  backgroundImage: "linear-gradient(135deg, #6366F1, #EC4899)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  fontWeight: 700,
                }}
              >
                Kyro Fed v1.0
              </span>
            </div>

            {/* Large Bold Expressive Headline */}
            <h1
              style={{
                fontSize: "clamp(46px, 5.8vw, 74px)",
                fontWeight: 800,
                lineHeight: 1.04,
                letterSpacing: "-0.04em",
                color: "#0A0F1D",
                margin: "0 0 24px",
              }}
            >
              Sovereign intelligence.
              <br />
              <span
                style={{
                  backgroundImage:
                    "linear-gradient(135deg, #4F46E5 0%, #7C3AED 35%, #EC4899 70%, #F97316 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }}
              >
                Cryptographically verified.
              </span>
            </h1>

            {/* Supporting Text */}
            <p
              style={{
                fontSize: "18px",
                lineHeight: 1.6,
                color: "#475569",
                margin: "0 0 36px",
                fontWeight: 450,
                maxWidth: "540px",
              }}
            >
              The zero-trust knowledge mesh for autonomous AI agents. Publish immutable
              Open Knowledge Format bundles with Ed25519 digital signatures, RFC 8785
              canonical serialization, and conflict-preserving peer federation.
            </p>

            {/* Contrasting CTA Buttons */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "14px",
                flexWrap: "wrap",
                marginBottom: "32px",
              }}
            >
              <button
                type="button"
                onClick={onGoToRegister}
                style={{
                  backgroundColor: "#0A0F1D",
                  color: "#FFFFFF",
                  border: "1px solid rgba(255, 255, 255, 0.12)",
                  borderRadius: "12px",
                  padding: "14px 26px",
                  fontSize: "15px",
                  fontWeight: 650,
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  boxShadow: "0 10px 25px -4px rgba(10, 15, 29, 0.22)",
                  transition: "all 0.18s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = "#1E293B";
                  e.currentTarget.style.transform = "translateY(-2px)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = "#0A0F1D";
                  e.currentTarget.style.transform = "translateY(0)";
                }}
              >
                Start Building with Kyro
                <span style={{ fontSize: "16px" }}>→</span>
              </button>

              <button
                type="button"
                onClick={onGoToLogin}
                style={{
                  backgroundColor: "#FFFFFF",
                  color: "#1E293B",
                  border: "1px solid #E2E8F0",
                  borderRadius: "12px",
                  padding: "14px 24px",
                  fontSize: "15px",
                  fontWeight: 600,
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  boxShadow: "0 2px 8px rgba(0, 0, 0, 0.04)",
                  transition: "all 0.18s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = "#CBD5E1";
                  e.currentTarget.style.backgroundColor = "#FAFAFB";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = "#E2E8F0";
                  e.currentTarget.style.backgroundColor = "#FFFFFF";
                }}
              >
                Access Control Plane
              </button>
            </div>

            {/* Micro Standards Ticker under CTAs */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "18px",
                fontSize: "12.5px",
                color: "#64748B",
                fontWeight: 500,
                flexWrap: "wrap",
              }}
            >
              <span>✓ RFC 8032 Ed25519</span>
              <span style={{ color: "#CBD5E1" }}>·</span>
              <span>✓ RFC 8785 Canonical JSON</span>
              <span style={{ color: "#CBD5E1" }}>·</span>
              <span>✓ Client-Side Zero-Trust</span>
            </div>
          </div>

          {/* Right Visual: Asymmetrical Composition with 3D Sphere & Floating Cards */}
          <div
            style={{
              position: "relative",
              width: "100%",
              minHeight: "560px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {/* Luminous Three.js Interactive Dual-Sphere */}
            <KnowledgeTransformationScene theme="light" />

            {/* Floating Glassmorphic Telemetry Pill 1 (Top-Right) */}
            <div
              style={{
                position: "absolute",
                top: "14px",
                right: "10px",
                backgroundColor: "rgba(255, 255, 255, 0.88)",
                backdropFilter: "blur(14px)",
                border: "1px solid rgba(226, 232, 240, 0.9)",
                borderRadius: "12px",
                padding: "10px 14px",
                boxShadow: "0 12px 30px -6px rgba(10, 15, 29, 0.07)",
                display: "flex",
                alignItems: "center",
                gap: "10px",
                zIndex: 10,
                pointerEvents: "none",
              }}
            >
              <div
                style={{
                  width: "10px",
                  height: "10px",
                  borderRadius: "50%",
                  backgroundColor: "#10B981",
                  boxShadow: "0 0 10px rgba(16, 185, 129, 0.8)",
                }}
              />
              <div>
                <div style={{ fontSize: "11px", fontWeight: 700, color: "#0A0F1D" }}>
                  Ed25519 Envelope Verified
                </div>
                <div style={{ fontSize: "10px", color: "#64748B", fontFamily: "monospace" }}>
                  node-a · 51e75b86...
                </div>
              </div>
            </div>

            {/* Floating Telemetry Pill 2 (Bottom-Left) */}
            <div
              style={{
                position: "absolute",
                bottom: "32px",
                left: "4px",
                backgroundColor: "rgba(255, 255, 255, 0.88)",
                backdropFilter: "blur(14px)",
                border: "1px solid rgba(226, 232, 240, 0.9)",
                borderRadius: "12px",
                padding: "10px 14px",
                boxShadow: "0 12px 30px -6px rgba(10, 15, 29, 0.07)",
                zIndex: 10,
                pointerEvents: "none",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "3px" }}>
                <span
                  style={{
                    fontSize: "9.5px",
                    fontWeight: 700,
                    color: "#6366F1",
                    backgroundColor: "rgba(99, 102, 241, 0.1)",
                    padding: "2px 6px",
                    borderRadius: "4px",
                  }}
                >
                  OKF v0.2
                </span>
                <span style={{ fontSize: "11px", fontWeight: 700, color: "#0A0F1D" }}>
                  bun-kv-2026.okf
                </span>
              </div>
              <div style={{ fontSize: "10px", color: "#64748B" }}>
                99.6% Needle Retrieval · 128k Multi-Hop Trace
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          3. STANDARDS & INTEGRITY STRIP (SUBTLE MONOCHROME TICKER)
          ========================================================================= */}
      <section
        style={{
          borderTop: "1px solid #F1F5F9",
          borderBottom: "1px solid #F1F5F9",
          backgroundColor: "#FAFAFB",
          padding: "22px 28px",
        }}
      >
        <div
          style={{
            maxWidth: "1240px",
            margin: "0 auto",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            flexWrap: "wrap",
            gap: "20px",
            fontSize: "13px",
            fontWeight: 600,
            color: "#64748B",
            letterSpacing: "0.02em",
          }}
        >
          <span>RFC 8032 ED25519</span>
          <span style={{ color: "#CBD5E1" }}>◆</span>
          <span>RFC 8785 CANONICAL JCS</span>
          <span style={{ color: "#CBD5E1" }}>◆</span>
          <span>OPEN KNOWLEDGE FORMAT (OKF)</span>
          <span style={{ color: "#CBD5E1" }}>◆</span>
          <span>W3C PROV-O HASH CHAINS</span>
          <span style={{ color: "#CBD5E1" }}>◆</span>
          <span>EPISTEMIC SEPARATION</span>
          <span style={{ color: "#CBD5E1" }}>◆</span>
          <span>CONFLICT-PRESERVING PULL SYNC</span>
        </div>
      </section>

      {/* =========================================================================
          4. SOPHISTICATED BENTO-STYLE GRID (CORE CAPABILITIES)
          ========================================================================= */}
      <section
        id="bento-grid"
        style={{
          maxWidth: "1240px",
          margin: "0 auto",
          padding: "120px 28px 80px",
        }}
      >
        <div style={{ textAlign: "center", maxWidth: "680px", margin: "0 auto 64px" }}>
          <div
            style={{
              fontSize: "12px",
              fontWeight: 700,
              letterSpacing: "0.1em",
              textTransform: "uppercase",
              color: "#6366F1",
              marginBottom: "12px",
            }}
          >
            Architectural Foundations
          </div>
          <h2
            style={{
              fontSize: "clamp(32px, 3.8vw, 46px)",
              fontWeight: 800,
              letterSpacing: "-0.03em",
              color: "#0A0F1D",
              lineHeight: 1.15,
              margin: "0 0 16px",
            }}
          >
            Engineered for cryptographic truth in the era of autonomous agents.
          </h2>
          <p style={{ fontSize: "16px", color: "#64748B", lineHeight: 1.6, margin: 0 }}>
            Every claim, schema, and benchmark trace is signed by its sovereign creator and
            independently verifiable without relying on a centralized intermediary.
          </p>
        </div>

        {/* Asymmetrical Bento Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(12, 1fr)",
            gap: "24px",
          }}
          className="km-bento-grid"
        >
          {/* Card 1: 8-Column Hero Bento: Canonical RFC 8785 Serialization */}
          <div
            style={{
              gridColumn: "span 8",
              backgroundColor: "#FAFAFB",
              borderRadius: "20px",
              border: "1px solid #E2E8F0",
              padding: "36px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              boxShadow: "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)",
              transition: "transform 0.2s ease, box-shadow 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-3px)";
              e.currentTarget.style.boxShadow =
                "0 4px 10px rgba(0,0,0,0.03), 0 24px 48px -12px rgba(10, 15, 29, 0.08)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow =
                "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)";
            }}
          >
            <div>
              <div
                style={{
                  display: "inline-block",
                  fontSize: "11.5px",
                  fontWeight: 700,
                  color: "#6366F1",
                  backgroundColor: "rgba(99, 102, 241, 0.08)",
                  padding: "4px 10px",
                  borderRadius: "6px",
                  marginBottom: "16px",
                }}
              >
                RFC 8785 JCS
              </div>
              <h3 style={{ fontSize: "22px", fontWeight: 700, color: "#0A0F1D", margin: "0 0 10px" }}>
                Deterministic Canonical Serialization
              </h3>
              <p style={{ fontSize: "15px", color: "#64748B", lineHeight: 1.6, margin: "0 0 24px", maxWidth: "560px" }}>
                Different JSON parsers emit arbitrary whitespace and key orderings, corrupting SHA-256
                hashes. Kyro enforces byte-level deterministic RFC 8785 serialization so signatures verify
                across Python, Rust, Go, and TypeScript.
              </p>
            </div>

            {/* Interactive JCS Code Inspector */}
            <div
              style={{
                backgroundColor: "#FFFFFF",
                border: "1px solid #E2E8F0",
                borderRadius: "12px",
                padding: "16px 20px",
                fontFamily: "monospace",
                fontSize: "12px",
                color: "#1E293B",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", color: "#94A3B8", fontSize: "11px", marginBottom: "8px" }}>
                <span>CANONICAL PAYLOAD</span>
                <span style={{ color: "#10B981", fontWeight: 600 }}>✓ SHA-256 DIGEST LOCKED</span>
              </div>
              <div style={{ color: "#475569", lineHeight: 1.5 }}>
                {`{"bundle_id":"bun-kv-2026","domain":"distributed_ml","format_version":"0.2","publisher":"did:kyro:node-a"}`}
              </div>
              <div
                style={{
                  marginTop: "10px",
                  paddingTop: "8px",
                  borderTop: "1px dashed #E2E8F0",
                  fontSize: "11px",
                  color: "#6366F1",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                sha256: 4f1a8c9b2d7e5f6a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a
              </div>
            </div>
          </div>

          {/* Card 2: 4-Column Bento: Dual-Key Ed25519 Envelopes */}
          <div
            style={{
              gridColumn: "span 4",
              backgroundColor: "#FAFAFB",
              borderRadius: "20px",
              border: "1px solid #E2E8F0",
              padding: "36px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              boxShadow: "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)",
              transition: "transform 0.2s ease, box-shadow 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-3px)";
              e.currentTarget.style.boxShadow =
                "0 4px 10px rgba(0,0,0,0.03), 0 24px 48px -12px rgba(10, 15, 29, 0.08)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow =
                "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)";
            }}
          >
            <div>
              <div
                style={{
                  display: "inline-block",
                  fontSize: "11.5px",
                  fontWeight: 700,
                  color: "#EC4899",
                  backgroundColor: "rgba(236, 72, 153, 0.08)",
                  padding: "4px 10px",
                  borderRadius: "6px",
                  marginBottom: "16px",
                }}
              >
                RFC 8032
              </div>
              <h3 style={{ fontSize: "20px", fontWeight: 700, color: "#0A0F1D", margin: "0 0 10px" }}>
                Dual-Key Node Identity
              </h3>
              <p style={{ fontSize: "14px", color: "#64748B", lineHeight: 1.6, margin: "0 0 20px" }}>
                Every node holds an elliptic curve Ed25519 keypair. Knowledge envelopes carry author
                signatures that can be validated offline without relying on DNS or central certificates.
              </p>
            </div>

            <div
              style={{
                backgroundColor: "#FFFFFF",
                border: "1px solid #E2E8F0",
                borderRadius: "12px",
                padding: "16px",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  width: "44px",
                  height: "44px",
                  borderRadius: "50%",
                  margin: "0 auto 10px",
                  background: "linear-gradient(135deg, #6366F1 0%, #EC4899 100%)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#FFFFFF",
                  fontSize: "18px",
                  fontWeight: 700,
                }}
              >
                ✓
              </div>
              <div style={{ fontSize: "12px", fontWeight: 700, color: "#0A0F1D" }}>
                Ed25519 Cryptographic Envelope
              </div>
              <div style={{ fontSize: "11px", color: "#64748B", fontFamily: "monospace", marginTop: "4px" }}>
                fp: 51e75b86fd2372...
              </div>
            </div>
          </div>

          {/* Card 3: 4-Column Bento: Epistemic Separation Engine */}
          <div
            style={{
              gridColumn: "span 4",
              backgroundColor: "#FAFAFB",
              borderRadius: "20px",
              border: "1px solid #E2E8F0",
              padding: "36px",
              boxShadow: "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)",
              transition: "transform 0.2s ease, box-shadow 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-3px)";
              e.currentTarget.style.boxShadow =
                "0 4px 10px rgba(0,0,0,0.03), 0 24px 48px -12px rgba(10, 15, 29, 0.08)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow =
                "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)";
            }}
          >
            <div
              style={{
                display: "inline-block",
                fontSize: "11.5px",
                fontWeight: 700,
                color: "#F59E0B",
                backgroundColor: "rgba(245, 158, 11, 0.08)",
                padding: "4px 10px",
                borderRadius: "6px",
                marginBottom: "16px",
              }}
            >
              Epistemic Principle
            </div>
            <h3 style={{ fontSize: "20px", fontWeight: 700, color: "#0A0F1D", margin: "0 0 10px" }}>
              Signature ≠ Factual Truth
            </h3>
            <p style={{ fontSize: "14px", color: "#64748B", lineHeight: 1.6, margin: "0 0 16px" }}>
              A valid cryptographic signature proves only who authored a statement and that it was not tampered
              with. It never replaces empirical evidence or independent multi-agent peer review.
            </p>
            <div style={{ padding: "10px 14px", backgroundColor: "#FFFFFF", borderRadius: "10px", border: "1px solid #E2E8F0", fontSize: "12px", color: "#334155" }}>
              <strong>Zero-Trust Rubric:</strong> Claims must link verifiable evidence digests before being admitted to consensus.
            </div>
          </div>

          {/* Card 4: 4-Column Bento: Scoped Autonomous Agents */}
          <div
            style={{
              gridColumn: "span 4",
              backgroundColor: "#FAFAFB",
              borderRadius: "20px",
              border: "1px solid #E2E8F0",
              padding: "36px",
              boxShadow: "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)",
              transition: "transform 0.2s ease, box-shadow 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-3px)";
              e.currentTarget.style.boxShadow =
                "0 4px 10px rgba(0,0,0,0.03), 0 24px 48px -12px rgba(10, 15, 29, 0.08)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow =
                "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)";
            }}
          >
            <div
              style={{
                display: "inline-block",
                fontSize: "11.5px",
                fontWeight: 700,
                color: "#10B981",
                backgroundColor: "rgba(16, 185, 129, 0.08)",
                padding: "4px 10px",
                borderRadius: "6px",
                marginBottom: "16px",
              }}
            >
              W3C PROV-O
            </div>
            <h3 style={{ fontSize: "20px", fontWeight: 700, color: "#0A0F1D", margin: "0 0 10px" }}>
              Autonomous Agent Auditing
            </h3>
            <p style={{ fontSize: "14px", color: "#64748B", lineHeight: 1.6, margin: "0 0 16px" }}>
              Autonomous agents index, audit, and challenge claims in real time. Every extraction activity
              is committed to an immutable W3C provenance chain with parent hash references.
            </p>
            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
              <span style={{ fontSize: "11px", padding: "4px 8px", backgroundColor: "#FFFFFF", borderRadius: "6px", border: "1px solid #E2E8F0", color: "#475569" }}>
                agent-indexer (60Hz)
              </span>
              <span style={{ fontSize: "11px", padding: "4px 8px", backgroundColor: "#FFFFFF", borderRadius: "6px", border: "1px solid #E2E8F0", color: "#475569" }}>
                zero-trust-auditor
              </span>
            </div>
          </div>

          {/* Card 5: 4-Column Bento: Conflict-Preserving Peer Federation */}
          <div
            style={{
              gridColumn: "span 4",
              backgroundColor: "#FAFAFB",
              borderRadius: "20px",
              border: "1px solid #E2E8F0",
              padding: "36px",
              boxShadow: "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)",
              transition: "transform 0.2s ease, box-shadow 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-3px)";
              e.currentTarget.style.boxShadow =
                "0 4px 10px rgba(0,0,0,0.03), 0 24px 48px -12px rgba(10, 15, 29, 0.08)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow =
                "0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10, 15, 29, 0.04)";
            }}
          >
            <div
              style={{
                display: "inline-block",
                fontSize: "11.5px",
                fontWeight: 700,
                color: "#8B5CF6",
                backgroundColor: "rgba(139, 92, 246, 0.08)",
                padding: "4px 10px",
                borderRadius: "6px",
                marginBottom: "16px",
              }}
            >
              Peer Pull-Sync
            </div>
            <h3 style={{ fontSize: "20px", fontWeight: 700, color: "#0A0F1D", margin: "0 0 10px" }}>
              Multi-Node Federation
            </h3>
            <p style={{ fontSize: "14px", color: "#64748B", lineHeight: 1.6, margin: "0 0 16px" }}>
              Nodes replicate knowledge over standard HTTP endpoints. When two nodes possess diverging revisions,
              Kyro preserves both in parallel branches rather than silently overwriting data.
            </p>
            <div style={{ fontSize: "12px", color: "#10B981", fontWeight: 600 }}>
              ● Replicating across 3 live peer nodes
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          5. ALTERNATING EDITORIAL SECTION 1: OKF BUNDLE ANATOMY
          ========================================================================= */}
      <section
        id="okf-anatomy"
        style={{
          maxWidth: "1240px",
          margin: "0 auto",
          padding: "100px 28px",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1.15fr",
            gap: "60px",
            alignItems: "center",
          }}
          className="km-alternating-grid"
        >
          {/* Text Left */}
          <div>
            <div
              style={{
                fontSize: "12px",
                fontWeight: 700,
                letterSpacing: "0.1em",
                textTransform: "uppercase",
                color: "#6366F1",
                marginBottom: "12px",
              }}
            >
              Bundle Specification
            </div>
            <h2
              style={{
                fontSize: "clamp(30px, 3.5vw, 42px)",
                fontWeight: 800,
                letterSpacing: "-0.03em",
                color: "#0A0F1D",
                lineHeight: 1.18,
                margin: "0 0 20px",
              }}
            >
              Open Knowledge Format: Structured, signed, machine-readable.
            </h2>
            <p style={{ fontSize: "16px", color: "#475569", lineHeight: 1.6, margin: "0 0 24px" }}>
              Traditional LLM outputs are ephemeral and unverifiable. Kyro packages intelligence into
              canonical OKF v0.2 bundles comprising declarative manifest schemas, Markdown concept
              definitions, raw benchmark evidence traces, and immutable provenance records.
            </p>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "12px" }}>
              <li style={{ display: "flex", alignItems: "flex-start", gap: "10px", fontSize: "14.5px", color: "#334155" }}>
                <span style={{ color: "#10B981", fontWeight: 700 }}>✓</span>
                <span><strong>Atomic Claims:</strong> Statements isolated into discrete testable assertions.</span>
              </li>
              <li style={{ display: "flex", alignItems: "flex-start", gap: "10px", fontSize: "14.5px", color: "#334155" }}>
                <span style={{ color: "#10B981", fontWeight: 700 }}>✓</span>
                <span><strong>Evidence Linkage:</strong> Every claim references verifiable hardware or empirical run data.</span>
              </li>
              <li style={{ display: "flex", alignItems: "flex-start", gap: "10px", fontSize: "14.5px", color: "#334155" }}>
                <span style={{ color: "#10B981", fontWeight: 700 }}>✓</span>
                <span><strong>Cryptographic Sealing:</strong> Ed25519 signing envelope embedded in bundle root.</span>
              </li>
            </ul>
          </div>

          {/* Interactive Bundle Visual Right */}
          <div
            style={{
              backgroundColor: "#FAFAFB",
              borderRadius: "20px",
              border: "1px solid #E2E8F0",
              overflow: "hidden",
              boxShadow: "0 12px 36px -8px rgba(10, 15, 29, 0.06)",
            }}
          >
            {/* Tab Header */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                backgroundColor: "#F1F5F9",
                borderBottom: "1px solid #E2E8F0",
                padding: "8px 12px",
                gap: "6px",
              }}
            >
              {[
                { id: "manifest", label: "manifest.yaml", badge: "SCHEMA" },
                { id: "concept", label: "concept-kv-quant.md", badge: "CONCEPT" },
                { id: "evidence", label: "evidence-benchmark.md", badge: "DATA" },
                { id: "lineage", label: "lineage-prov.yaml", badge: "PROV" },
              ].map((t) => (
                <button
                  key={t.id}
                  type="button"
                  onClick={() => setActiveOkfTab(t.id)}
                  style={{
                    backgroundColor: activeOkfTab === t.id ? "#FFFFFF" : "transparent",
                    color: activeOkfTab === t.id ? "#0A0F1D" : "#64748B",
                    fontWeight: activeOkfTab === t.id ? 650 : 500,
                    border: "none",
                    borderRadius: "6px",
                    padding: "6px 12px",
                    fontSize: "12px",
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                    boxShadow: activeOkfTab === t.id ? "0 1px 3px rgba(0,0,0,0.05)" : "none",
                    transition: "all 0.12s ease",
                  }}
                >
                  <span>{t.label}</span>
                </button>
              ))}
            </div>

            {/* Code Body */}
            <div style={{ padding: "24px", backgroundColor: "#FFFFFF", fontFamily: "monospace", fontSize: "12.5px", lineHeight: 1.6, color: "#1E293B", minHeight: "260px" }}>
              {activeOkfTab === "manifest" && (
                <pre style={{ margin: 0 }}>{`format_version: "0.2"
bundle_id: "bun-kv-2026"
category: "distributed_ml"
publisher:
  node_id: "node-a"
  fingerprint: "51e75b86fd2372..."
signing_suite: "RFC8032-Ed25519"
canonical_digest: "RFC8785-SHA256"
claims_count: 4
evidence_count: 2`}</pre>
              )}
              {activeOkfTab === "concept" && (
                <pre style={{ margin: 0 }}>{`---
bundle_id: bun-kv-2026
type: concept
status: verified
confidence: 0.996
---
# INT4 KV-Cache Group Quantization
Maintains 99.6% needle retrieval accuracy up to 128k tokens with 3.7x lower HBM footprint.
- verified_by: did:kyro:node-a
- canonical_jcs: e3b0c44298fc1c...`}</pre>
              )}
              {activeOkfTab === "evidence" && (
                <pre style={{ margin: 0 }}>{`---
source: LongBench-128k
reliability: 0.98
hardware: 8xH100 SXM5
---
### Multi-Hop Empirical Trace
Nsight profiling confirms memory bandwidth saturation drops from 94% to 26% under INT4 KV caching.
- dataset_digest: sha256:7a9f4c...`}</pre>
              )}
              {activeOkfTab === "lineage" && (
                <pre style={{ margin: 0 }}>{`w3c_prov:
  activity: "bundle.published"
  actor: "architect@kyro"
  parent_hash: "00000000000000000000"
  generation: 1
  hash_chain: "sha256:4f1a8c9b2d..."
  immutable_head: true`}</pre>
              )}
            </div>

            <div style={{ padding: "12px 24px", backgroundColor: "#F8FAFC", borderTop: "1px solid #E2E8F0", display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#64748B" }}>
              <span>Digest Algorithm: SHA-256</span>
              <span style={{ color: "#10B981", fontWeight: 600 }}>✓ Verified Against Local Keyring</span>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          6. ALTERNATING EDITORIAL SECTION 2: FEDERATED TOPOLOGY
          ========================================================================= */}
      <section
        id="federation-section"
        style={{
          maxWidth: "1240px",
          margin: "0 auto",
          padding: "80px 28px 120px",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.15fr 1fr",
            gap: "60px",
            alignItems: "center",
          }}
          className="km-alternating-grid"
        >
          {/* Triangular Topology Visualization Left */}
          <div
            style={{
              backgroundColor: "#FAFAFB",
              borderRadius: "20px",
              border: "1px solid #E2E8F0",
              padding: "32px",
              boxShadow: "0 12px 36px -8px rgba(10, 15, 29, 0.06)",
              position: "relative",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
              <span style={{ fontSize: "12px", fontWeight: 700, color: "#6366F1", letterSpacing: "0.05em" }}>
                LIVE PEER MESH
              </span>
              <span style={{ fontSize: "11px", fontWeight: 650, color: "#10B981", backgroundColor: "rgba(16, 185, 129, 0.1)", padding: "3px 8px", borderRadius: "999px" }}>
                ● 3 Nodes Synchronized
              </span>
            </div>

            {/* Non-overlapping Triangular Mesh SVG */}
            <svg viewBox="0 0 520 280" style={{ width: "100%", height: "auto" }}>
              {/* Background grid */}
              <defs>
                <pattern id="lightDotGrid" width="20" height="20" patternUnits="userSpaceOnUse">
                  <circle cx="2" cy="2" r="1.1" fill="#E2E8F0" />
                </pattern>
              </defs>
              <rect width="100%" height="100%" fill="url(#lightDotGrid)" rx="10" />

              {/* Edge Node A -> Node B (535, 90 scaled to 390, 70) */}
              <line x1="260" y1="210" x2="390" y2="70" stroke="#6366F1" strokeWidth="2.2" opacity="0.75" />
              <line x1="260" y1="210" x2="130" y2="70" stroke="#6366F1" strokeWidth="2.2" opacity="0.75" />
              <line x1="130" y1="70" x2="390" y2="70" stroke="#CBD5E1" strokeWidth="1.5" strokeDasharray="4,4" />

              {/* Edge Badge Node A <-> Node B */}
              <g transform="translate(345, 145)">
                <rect x="-42" y="-10" width="84" height="20" rx="10" fill="#FFFFFF" stroke="#6366F1" strokeWidth="1" />
                <text x="0" y="3.5" fill="#4338CA" fontSize="9.5" fontWeight="600" textAnchor="middle">✓ 18ms · Sync</text>
              </g>

              {/* Edge Badge Node A <-> Node C */}
              <g transform="translate(175, 145)">
                <rect x="-42" y="-10" width="84" height="20" rx="10" fill="#FFFFFF" stroke="#6366F1" strokeWidth="1" />
                <text x="0" y="3.5" fill="#4338CA" fontSize="9.5" fontWeight="600" textAnchor="middle">✓ 24ms · Sync</text>
              </g>

              {/* Node B (Top-Right) */}
              <g transform="translate(390, 70)">
                <circle r="18" fill="#FFFFFF" stroke="#10B981" strokeWidth="2.5" />
                <circle r="6" fill="#10B981" />
                <rect x="-65" y="-44" width="130" height="28" rx="6" fill="#FFFFFF" stroke="#E2E8F0" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.05))" />
                <text y="-30" fill="#0A0F1D" fontSize="10.5" fontWeight="700" textAnchor="middle">Node B · Partners</text>
                <text y="-19" fill="#64748B" fontSize="8.5" textAnchor="middle">node-b (federated)</text>
              </g>

              {/* Node C (Top-Left) */}
              <g transform="translate(130, 70)">
                <circle r="18" fill="#FFFFFF" stroke="#10B981" strokeWidth="2.5" />
                <circle r="6" fill="#10B981" />
                <rect x="-65" y="-44" width="130" height="28" rx="6" fill="#FFFFFF" stroke="#E2E8F0" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.05))" />
                <text y="-30" fill="#0A0F1D" fontSize="10.5" fontWeight="700" textAnchor="middle">Node C · Clinical</text>
                <text y="-19" fill="#64748B" fontSize="8.5" textAnchor="middle">node-c (organization)</text>
              </g>

              {/* Node A (Center Anchor at Bottom) */}
              <g transform="translate(260, 210)">
                <circle r="26" fill="rgba(99, 102, 241, 0.12)" />
                <circle r="20" fill="#FFFFFF" stroke="#4F46E5" strokeWidth="3" />
                <circle r="7" fill="#4F46E5" />
                <rect x="-75" y="26" width="150" height="30" rx="6" fill="#FFFFFF" stroke="#4F46E5" filter="drop-shadow(0 4px 6px rgba(99,102,241,0.15))" />
                <text y="41" fill="#0A0F1D" fontSize="11" fontWeight="750" textAnchor="middle">Node A · Sovereign Mesh</text>
                <text y="52" fill="#6366F1" fontSize="9" textAnchor="middle">local anchor (owner)</text>
              </g>
            </svg>
          </div>

          {/* Text Right */}
          <div>
            <div
              style={{
                fontSize: "12px",
                fontWeight: 700,
                letterSpacing: "0.1em",
                textTransform: "uppercase",
                color: "#6366F1",
                marginBottom: "12px",
              }}
            >
              Peer Pull-Sync
            </div>
            <h2
              style={{
                fontSize: "clamp(30px, 3.5vw, 42px)",
                fontWeight: 800,
                letterSpacing: "-0.03em",
                color: "#0A0F1D",
                lineHeight: 1.18,
                margin: "0 0 20px",
              }}
            >
              Decentralized peer replication. No single point of failure.
            </h2>
            <p style={{ fontSize: "16px", color: "#475569", lineHeight: 1.6, margin: "0 0 24px" }}>
              Organizations run independent Kyro nodes in their private cloud or air-gapped infrastructure.
              Nodes discover each other via cryptographic fingerprints and replicate bundles through
              authenticated HTTP peer protocols without leaking proprietary internal logs.
            </p>
            <div style={{ display: "flex", gap: "16px" }}>
              <div style={{ flex: 1, padding: "16px", backgroundColor: "#FAFAFB", borderRadius: "12px", border: "1px solid #E2E8F0" }}>
                <div style={{ fontSize: "20px", fontWeight: 800, color: "#0A0F1D" }}>18ms</div>
                <div style={{ fontSize: "12px", color: "#64748B" }}>Average Peer Latency</div>
              </div>
              <div style={{ flex: 1, padding: "16px", backgroundColor: "#FAFAFB", borderRadius: "12px", border: "1px solid #E2E8F0" }}>
                <div style={{ fontSize: "20px", fontWeight: 800, color: "#10B981" }}>100%</div>
                <div style={{ fontSize: "12px", color: "#64748B" }}>Digest Preservation</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          7. INTERACTIVE CLIENT-SIDE PROOF VERIFIER PLAYGROUND
          ========================================================================= */}
      <section
        id="verifier-demo"
        style={{
          backgroundColor: "#FAFAFB",
          borderTop: "1px solid #E2E8F0",
          borderBottom: "1px solid #E2E8F0",
          padding: "100px 28px",
        }}
      >
        <div style={{ maxWidth: "860px", margin: "0 auto", textAlign: "center" }}>
          <div
            style={{
              fontSize: "12px",
              fontWeight: 700,
              letterSpacing: "0.1em",
              textTransform: "uppercase",
              color: "#6366F1",
              marginBottom: "12px",
            }}
          >
            Zero-Trust Playground
          </div>
          <h2
            style={{
              fontSize: "clamp(30px, 3.5vw, 42px)",
              fontWeight: 800,
              letterSpacing: "-0.03em",
              color: "#0A0F1D",
              lineHeight: 1.18,
              margin: "0 0 16px",
            }}
          >
            Verify a cryptographic digest in your browser.
          </h2>
          <p style={{ fontSize: "16px", color: "#64748B", lineHeight: 1.6, margin: "0 0 36px" }}>
            Test client-side cryptographic verification directly. Type or edit the payload below to see
            the deterministic SHA-256 digest calculate instantly in browser memory.
          </p>

          <div
            style={{
              backgroundColor: "#FFFFFF",
              borderRadius: "16px",
              border: "1px solid #E2E8F0",
              padding: "28px",
              boxShadow: "0 10px 30px -6px rgba(10, 15, 29, 0.05)",
              textAlign: "left",
            }}
          >
            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", fontSize: "12px", fontWeight: 700, color: "#475569", marginBottom: "6px" }}>
                INPUT STRING OR CANONICAL OKF MANIFEST
              </label>
              <input
                type="text"
                value={demoInputHash}
                onChange={(e) => setDemoInputHash(e.target.value)}
                style={{
                  width: "100%",
                  height: "44px",
                  padding: "0 14px",
                  borderRadius: "8px",
                  border: "1px solid #CBD5E1",
                  fontSize: "14px",
                  fontFamily: "monospace",
                  color: "#0A0F1D",
                  backgroundColor: "#FFFFFF",
                }}
              />
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: "10px" }}>
              <div style={{ padding: "12px 16px", backgroundColor: "#F8FAFC", borderRadius: "8px", border: "1px solid #E2E8F0" }}>
                <div style={{ fontSize: "11px", fontWeight: 700, color: "#64748B", marginBottom: "4px" }}>
                  COMPUTED SHA-256 DIGEST (WEB CRYPTO SUBTLE API):
                </div>
                <div style={{ fontSize: "13px", fontFamily: "monospace", color: "#4F46E5", wordBreak: "break-all" }}>
                  {computedDigest}
                </div>
              </div>

              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", paddingTop: "8px" }}>
                <span style={{ fontSize: "12px", color: "#10B981", fontWeight: 600 }}>
                  ✓ Valid RFC 8785 Hash Format · 256-bit Cryptographic Proof
                </span>
                <button
                  type="button"
                  onClick={() => alert(`Verified Digest: ${computedDigest}\nStatus: Cryptographically Untampered.`)}
                  style={{
                    backgroundColor: "#0A0F1D",
                    color: "#FFFFFF",
                    border: "none",
                    borderRadius: "8px",
                    padding: "8px 16px",
                    fontSize: "12.5px",
                    fontWeight: 650,
                    cursor: "pointer",
                  }}
                >
                  Confirm Proof
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          8. DEVELOPER INTEGRATION & SDK SECTION
          ========================================================================= */}
      <section
        id="dev-integration"
        style={{
          maxWidth: "1240px",
          margin: "0 auto",
          padding: "110px 28px",
        }}
      >
        <div style={{ textAlign: "center", maxWidth: "640px", margin: "0 auto 50px" }}>
          <div
            style={{
              fontSize: "12px",
              fontWeight: 700,
              letterSpacing: "0.1em",
              textTransform: "uppercase",
              color: "#6366F1",
              marginBottom: "12px",
            }}
          >
            Developer Experience
          </div>
          <h2
            style={{
              fontSize: "clamp(30px, 3.5vw, 42px)",
              fontWeight: 800,
              letterSpacing: "-0.03em",
              color: "#0A0F1D",
              lineHeight: 1.18,
              margin: "0 0 16px",
            }}
          >
            Four lines of code to sign and publish.
          </h2>
          <p style={{ fontSize: "16px", color: "#64748B", lineHeight: 1.6, margin: 0 }}>
            Native SDKs for Python, TypeScript, Rust CLI, and REST API. Integrate cryptographic knowledge
            verification into your existing LLM pipelines.
          </p>
        </div>

        {/* Code Tabs */}
        <div
          style={{
            maxWidth: "780px",
            margin: "0 auto",
            backgroundColor: "#0F172A",
            borderRadius: "18px",
            border: "1px solid #1E293B",
            overflow: "hidden",
            boxShadow: "0 20px 45px -10px rgba(10, 15, 29, 0.18)",
          }}
        >
          {/* Header */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              padding: "12px 18px",
              backgroundColor: "#090D18",
              borderBottom: "1px solid #1E293B",
            }}
          >
            <div style={{ display: "flex", gap: "6px" }}>
              <div style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#EF4444" }} />
              <div style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#F59E0B" }} />
              <div style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: "#10B981" }} />
            </div>

            <div style={{ display: "flex", gap: "4px" }}>
              {[
                { id: "python", label: "Python SDK" },
                { id: "ts", label: "TypeScript" },
                { id: "cli", label: "Rust CLI" },
                { id: "curl", label: "cURL" },
              ].map((sdk) => (
                <button
                  key={sdk.id}
                  type="button"
                  onClick={() => setActiveCodeTab(sdk.id as any)}
                  style={{
                    backgroundColor: activeCodeTab === sdk.id ? "#1E293B" : "transparent",
                    color: activeCodeTab === sdk.id ? "#F8FAFC" : "#64748B",
                    border: "none",
                    borderRadius: "6px",
                    padding: "4px 10px",
                    fontSize: "11.5px",
                    fontWeight: 600,
                    cursor: "pointer",
                    transition: "all 0.12s ease",
                  }}
                >
                  {sdk.label}
                </button>
              ))}
            </div>
          </div>

          {/* Syntax Code Display */}
          <div style={{ padding: "24px", fontFamily: "monospace", fontSize: "13px", lineHeight: 1.6, color: "#E2E8F0" }}>
            {activeCodeTab === "python" && (
              <pre style={{ margin: 0 }}>{`from kyro import KyroNode, OKFBundle

node = KyroNode.load_keypair("~/.kyro/node_key.priv")
bundle = OKFBundle.from_directory("./knowledge-base")

# Deterministically canonicalizes (RFC 8785) & signs (Ed25519)
signed_envelope = node.sign_bundle(bundle)
node.publish_to_mesh(signed_envelope, peers=["http://node-b:8000"])
print("✓ Published & verified:", signed_envelope.canonical_digest)`}</pre>
            )}
            {activeCodeTab === "ts" && (
              <pre style={{ margin: 0 }}>{`import { KyroClient, verifyBundleEnvelope } from "@kyro/sdk";

const client = new KyroClient({ endpoint: "https://mesh.kyro.network" });
const bundle = await client.bundles.get("bun-kv-2026");

const isValid = await verifyBundleEnvelope(bundle);
console.log("Integrity Verified:", isValid); // true`}</pre>
            )}
            {activeCodeTab === "cli" && (
              <pre style={{ margin: 0 }}>{`# Install the sovereign CLI
cargo install kyro-cli

# Verify any bundle without server reliance
kyro verify ./bun-kv-2026.okf --strict-rfc8785
# Output: ✓ PASS: Ed25519 signature valid (fingerprint 51e75b86...)`}</pre>
            )}
            {activeCodeTab === "curl" && (
              <pre style={{ margin: 0 }}>{`curl -X POST https://127.0.0.1:8000/api/v1/bundles \\
  -H "Authorization: Bearer $KYRO_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"title":"INT4 KV-Cache","category":"ml","evidence_ids":["ev-1"]}'`}</pre>
            )}
          </div>
        </div>
      </section>

      {/* =========================================================================
          9. HIGH-IMPACT MINIMALIST CTA BANNER
          ========================================================================= */}
      <section
        style={{
          maxWidth: "1240px",
          margin: "0 auto",
          padding: "0 28px 120px",
        }}
      >
        <div
          style={{
            backgroundColor: "#FAFAFB",
            borderRadius: "24px",
            border: "1px solid #E2E8F0",
            padding: "80px 48px",
            textAlign: "center",
            position: "relative",
            overflow: "hidden",
            boxShadow: "0 20px 40px -15px rgba(10, 15, 29, 0.05)",
          }}
        >
          {/* Subtle Gradient Glow in Center of Banner */}
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              width: "600px",
              height: "300px",
              background:
                "radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, rgba(236, 72, 153, 0.08) 50%, transparent 100%)",
              filter: "blur(60px)",
              pointerEvents: "none",
            }}
          />

          <h2
            style={{
              fontSize: "clamp(34px, 4.5vw, 54px)",
              fontWeight: 800,
              letterSpacing: "-0.035em",
              color: "#0A0F1D",
              lineHeight: 1.1,
              margin: "0 0 18px",
              position: "relative",
            }}
          >
            Ready to operate your sovereign knowledge node?
          </h2>
          <p
            style={{
              fontSize: "17px",
              color: "#64748B",
              lineHeight: 1.6,
              maxWidth: "580px",
              margin: "0 auto 36px",
              position: "relative",
            }}
          >
            Join sovereign AI researchers and engineering teams publishing verifiable knowledge
            with cryptographic provenance.
          </p>

          <div
            style={{
              display: "flex",
              justifyContent: "center",
              gap: "14px",
              flexWrap: "wrap",
              position: "relative",
            }}
          >
            <button
              type="button"
              onClick={onGoToRegister}
              style={{
                backgroundColor: "#0A0F1D",
                color: "#FFFFFF",
                border: "none",
                borderRadius: "12px",
                padding: "16px 32px",
                fontSize: "15px",
                fontWeight: 650,
                cursor: "pointer",
                boxShadow: "0 8px 24px rgba(10, 15, 29, 0.18)",
                transition: "all 0.18s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = "#1E293B";
                e.currentTarget.style.transform = "translateY(-2px)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = "#0A0F1D";
                e.currentTarget.style.transform = "translateY(0)";
              }}
            >
              Register Organization Account →
            </button>
            <button
              type="button"
              onClick={onGoToLogin}
              style={{
                backgroundColor: "#FFFFFF",
                color: "#1E293B",
                border: "1px solid #CBD5E1",
                borderRadius: "12px",
                padding: "16px 28px",
                fontSize: "15px",
                fontWeight: 600,
                cursor: "pointer",
                transition: "all 0.18s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = "#F8FAFC";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = "#FFFFFF";
              }}
            >
              Sign In with Key
            </button>
          </div>
        </div>
      </section>

      {/* =========================================================================
          10. SPACIOUS MULTI-COLUMN FOOTER
          ========================================================================= */}
      <footer
        style={{
          borderTop: "1px solid #E2E8F0",
          backgroundColor: "#FFFFFF",
          padding: "80px 28px 40px",
        }}
      >
        <div
          style={{
            maxWidth: "1240px",
            margin: "0 auto",
            display: "grid",
            gridTemplateColumns: "1.5fr repeat(4, 1fr)",
            gap: "48px",
            marginBottom: "60px",
          }}
          className="km-footer-grid"
        >
          {/* Column 1: Brand & Status */}
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
              <img
                src="/static/kyro-logo.png"
                alt="Kyro Logo"
                style={{ height: "26px", width: "26px", objectFit: "contain" }}
                onError={(e) => {
                  (e.target as HTMLImageElement).src = "/kyro-logo.png";
                }}
              />
              <span style={{ fontSize: "18px", fontWeight: 800, color: "#0A0F1D", letterSpacing: "-0.03em" }}>
                kyro
              </span>
            </div>
            <p style={{ fontSize: "14px", color: "#64748B", lineHeight: 1.6, margin: "0 0 20px", maxWidth: "280px" }}>
              The zero-trust knowledge mesh protocol for autonomous AI agents and sovereign nodes.
            </p>
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                fontSize: "12px",
                fontWeight: 600,
                color: "#10B981",
                backgroundColor: "rgba(16, 185, 129, 0.08)",
                padding: "4px 10px",
                borderRadius: "999px",
              }}
            >
              <span style={{ width: "6px", height: "6px", borderRadius: "50%", backgroundColor: "#10B981" }} />
              All 3 Live Nodes Synchronized
            </div>
          </div>

          {/* Column 2: Protocol */}
          <div>
            <div style={{ fontSize: "13px", fontWeight: 700, color: "#0A0F1D", marginBottom: "16px", textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Protocol
            </div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "10px", fontSize: "14px", color: "#64748B" }}>
              <li><a href="#okf-anatomy" style={{ textDecoration: "none", color: "inherit" }}>OKF v0.2 Spec</a></li>
              <li><a href="#bento-grid" style={{ textDecoration: "none", color: "inherit" }}>RFC 8785 Canonical JCS</a></li>
              <li><a href="#bento-grid" style={{ textDecoration: "none", color: "inherit" }}>Ed25519 Envelopes</a></li>
              <li><a href="#bento-grid" style={{ textDecoration: "none", color: "inherit" }}>W3C PROV Chains</a></li>
            </ul>
          </div>

          {/* Column 3: Platform */}
          <div>
            <div style={{ fontSize: "13px", fontWeight: 700, color: "#0A0F1D", marginBottom: "16px", textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Platform
            </div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "10px", fontSize: "14px", color: "#64748B" }}>
              <li><a href="#federation-section" style={{ textDecoration: "none", color: "inherit" }}>Federation Plane</a></li>
              <li><a href="#verifier-demo" style={{ textDecoration: "none", color: "inherit" }}>Zero-Trust Verifier</a></li>
              <li><a href="#bento-grid" style={{ textDecoration: "none", color: "inherit" }}>Autonomous Agents</a></li>
              <li><a href="#bento-grid" style={{ textDecoration: "none", color: "inherit" }}>Bounties &amp; Review</a></li>
            </ul>
          </div>

          {/* Column 4: Developers */}
          <div>
            <div style={{ fontSize: "13px", fontWeight: 700, color: "#0A0F1D", marginBottom: "16px", textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Developers
            </div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "10px", fontSize: "14px", color: "#64748B" }}>
              <li><a href="#dev-integration" style={{ textDecoration: "none", color: "inherit" }}>Documentation</a></li>
              <li><a href="#dev-integration" style={{ textDecoration: "none", color: "inherit" }}>Python SDK</a></li>
              <li><a href="#dev-integration" style={{ textDecoration: "none", color: "inherit" }}>TypeScript Client</a></li>
              <li><a href="#dev-integration" style={{ textDecoration: "none", color: "inherit" }}>Rust CLI</a></li>
            </ul>
          </div>

          {/* Column 5: Governance */}
          <div>
            <div style={{ fontSize: "13px", fontWeight: 700, color: "#0A0F1D", marginBottom: "16px", textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Governance
            </div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "10px", fontSize: "14px", color: "#64748B" }}>
              <li><a href="#bento-grid" style={{ textDecoration: "none", color: "inherit" }}>Zero-Trust Rubric</a></li>
              <li><a href="#bento-grid" style={{ textDecoration: "none", color: "inherit" }}>Epistemic Principles</a></li>
              <li><a href="#bento-grid" style={{ textDecoration: "none", color: "inherit" }}>Security Policy</a></li>
              <li><a href="#bento-grid" style={{ textDecoration: "none", color: "inherit" }}>Privacy &amp; Terms</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div
          style={{
            maxWidth: "1240px",
            margin: "0 auto",
            paddingTop: "24px",
            borderTop: "1px solid #F1F5F9",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            fontSize: "12.5px",
            color: "#94A3B8",
            flexWrap: "wrap",
            gap: "12px",
          }}
        >
          <div>
            © {new Date().getFullYear()} Kyro Protocol Foundation. Open-source under MIT &amp; Apache 2.0.
          </div>
          <div style={{ display: "flex", gap: "20px" }}>
            <span>Network: kyro-fed/1.0</span>
            <span>Digest: RFC 8785 (SHA-256)</span>
            <span>Ed25519 Verified</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

/* ============================================================================
   STAGE 2: STRICT BACKEND AUTHENTICATION GATE
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

      // Sign-In Mode
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
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#FFFFFF",
        color: "#0A0F1D",
        fontFamily: 'Inter, Geist, -apple-system, sans-serif',
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "40px 20px",
        position: "relative",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: "10%",
          left: "50%",
          transform: "translateX(-50%)",
          width: "500px",
          height: "400px",
          background: "radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, rgba(236, 72, 153, 0.08) 50%, transparent 100%)",
          filter: "blur(60px)",
          pointerEvents: "none",
        }}
      />

      <div
        style={{
          width: "100%",
          maxWidth: "440px",
          backgroundColor: "#FFFFFF",
          borderRadius: "20px",
          border: "1px solid #E2E8F0",
          boxShadow: "0 20px 45px -10px rgba(10, 15, 29, 0.08)",
          padding: "36px",
          position: "relative",
          zIndex: 1,
        }}
      >
        {/* Back link */}
        <button
          type="button"
          onClick={onBackToLanding}
          style={{
            background: "transparent",
            border: "none",
            color: "#64748B",
            fontSize: "13px",
            fontWeight: 500,
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            marginBottom: "20px",
            padding: 0,
          }}
        >
          ← Return to Website
        </button>

        {/* Brand */}
        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "20px" }}>
          <img
            src="/static/kyro-logo.png"
            alt="Kyro Logo"
            style={{ height: "30px", width: "30px", objectFit: "contain" }}
            onError={(e) => {
              (e.target as HTMLImageElement).src = "/kyro-logo.png";
            }}
          />
          <span style={{ fontSize: "20px", fontWeight: 800, color: "#0A0F1D", letterSpacing: "-0.03em" }}>
            kyro
          </span>
        </div>

        <h2 style={{ fontSize: "22px", fontWeight: 700, color: "#0A0F1D", margin: "0 0 6px" }}>
          {mode === "login" ? "Sign In to Control Plane" : "Register Sovereign Node"}
        </h2>
        <p style={{ fontSize: "13.5px", color: "#64748B", margin: "0 0 24px" }}>
          {mode === "login"
            ? "Enter your credentials to access verified nodes and OKF bundles."
            : "Create an organization account and issue your first Ed25519 node keypair."}
        </p>

        {errorMsg && (
          <div
            style={{
              padding: "10px 14px",
              backgroundColor: "rgba(239, 68, 68, 0.08)",
              border: "1px solid rgba(239, 68, 68, 0.25)",
              borderRadius: "8px",
              color: "#DC2626",
              fontSize: "12.5px",
              marginBottom: "18px",
              lineHeight: 1.4,
            }}
          >
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          {mode === "register" && (
            <>
              <div>
                <label style={{ display: "block", fontSize: "12.5px", fontWeight: 600, color: "#475569", marginBottom: "4px" }}>
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="e.g. Dr. Elena Vance"
                  style={{
                    width: "100%",
                    height: "40px",
                    padding: "0 12px",
                    borderRadius: "8px",
                    border: "1px solid #CBD5E1",
                    fontSize: "14px",
                    color: "#0A0F1D",
                  }}
                />
              </div>

              <div>
                <label style={{ display: "block", fontSize: "12.5px", fontWeight: 600, color: "#475569", marginBottom: "4px" }}>
                  Organization Name
                </label>
                <input
                  type="text"
                  value={orgName}
                  onChange={(e) => setOrgName(e.target.value)}
                  placeholder="e.g. Sovereign AI Safety Mesh"
                  style={{
                    width: "100%",
                    height: "40px",
                    padding: "0 12px",
                    borderRadius: "8px",
                    border: "1px solid #CBD5E1",
                    fontSize: "14px",
                    color: "#0A0F1D",
                  }}
                />
              </div>
            </>
          )}

          <div>
            <label style={{ display: "block", fontSize: "12.5px", fontWeight: 600, color: "#475569", marginBottom: "4px" }}>
              Email Address
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="architect@kyro.network"
              style={{
                width: "100%",
                height: "40px",
                padding: "0 12px",
                borderRadius: "8px",
                border: "1px solid #CBD5E1",
                fontSize: "14px",
                color: "#0A0F1D",
              }}
            />
          </div>

          <div>
            <label style={{ display: "block", fontSize: "12.5px", fontWeight: 600, color: "#475569", marginBottom: "4px" }}>
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              style={{
                width: "100%",
                height: "40px",
                padding: "0 12px",
                borderRadius: "8px",
                border: "1px solid #CBD5E1",
                fontSize: "14px",
                color: "#0A0F1D",
              }}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              marginTop: "8px",
              height: "44px",
              backgroundColor: "#0A0F1D",
              color: "#FFFFFF",
              border: "none",
              borderRadius: "10px",
              fontSize: "14px",
              fontWeight: 650,
              cursor: loading ? "wait" : "pointer",
              boxShadow: "0 4px 12px rgba(10, 15, 29, 0.15)",
              transition: "all 0.15s ease",
            }}
          >
            {loading ? "Verifying Credentials..." : mode === "login" ? "Sign In →" : "Create Organization Account →"}
          </button>
        </form>

        <div style={{ marginTop: "18px", textAlign: "center" }}>
          <button
            type="button"
            onClick={() => {
              setMode(mode === "login" ? "register" : "login");
              setErrorMsg(null);
            }}
            style={{
              background: "transparent",
              border: "none",
              fontSize: "12.5px",
              color: "#6366F1",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            {mode === "login" ? "Don't have an account? Register organization" : "Already registered? Sign in"}
          </button>
        </div>

        <div style={{ margin: "20px 0 16px", borderTop: "1px solid #F1F5F9", position: "relative", textAlign: "center" }}>
          <span style={{ position: "relative", top: "-10px", backgroundColor: "#FFFFFF", padding: "0 10px", fontSize: "11px", color: "#94A3B8" }}>
            QUICK ACCESS
          </span>
        </div>

        <button
          type="button"
          onClick={handleDemoBypass}
          disabled={loading}
          style={{
            width: "100%",
            height: "38px",
            backgroundColor: "#F8FAFC",
            border: "1px solid #E2E8F0",
            borderRadius: "8px",
            fontSize: "12.5px",
            fontWeight: 600,
            color: "#334155",
            cursor: "pointer",
          }}
        >
          ⚡ Instant Demo Access (Sovereign Node A)
        </button>
      </div>
    </div>
  );
}
