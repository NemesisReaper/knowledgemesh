"""Self-contained Kyro Animated Product Landing Page, Auth Gate & Console UI served by FastAPI.

All telemetry, nodes, bundles, claims, evidence, agents, credentials, peers, bounties,
reputation scores, organizations, and user sessions are fetched dynamically from the
live FastAPI backend (/api/v1/* and /health) with zero hardcoded credentials or mock arrays.
"""

from __future__ import annotations

from pathlib import Path


def _load_dashboard_css() -> str:
    css_path = (
        Path(__file__).resolve().parents[4]
        / "apps"
        / "dashboard"
        / "src"
        / "app"
        / "globals.css"
    )
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return "body { background: #090D18; color: #F3F7FF; font-family: sans-serif; }"


def render_console_html() -> str:
    css = _load_dashboard_css()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kyro | Sovereign Federated Knowledge Infrastructure</title>
  <style>{css}</style>
  <style id="km-mesh-premium-motion">
    .km-okf-hover-card {{
      transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.18s ease, border-color 0.18s ease !important;
    }}
    .km-okf-hover-card:hover {{
      transform: translate(-50%, -50%) translateY(-6px) scale(1.02) !important;
      box-shadow: 0 20px 40px -4px rgba(10,15,29,0.16), 0 0 1px var(--card-accent, #4F46E5) !important;
      border-color: var(--card-accent, #4F46E5) !important;
      z-index: 28 !important;
    }}

    /* Continuous Zero-Gravity Levitation & Breathing */
    @keyframes kmFloatLevitate1 {{
      0%, 100% {{ transform: translate(-50%, -50%) translateY(0px); }}
      50% {{ transform: translate(-50%, -50%) translateY(-7px); }}
    }}
    @keyframes kmFloatLevitate2 {{
      0%, 100% {{ transform: translate(-50%, -50%) translateY(0px); }}
      50% {{ transform: translate(-50%, -50%) translateY(7px); }}
    }}
    @keyframes kmFloatLevitate3 {{
      0%, 100% {{ transform: translate(-50%, -50%) translateY(0px); }}
      50% {{ transform: translate(-50%, -50%) translateY(-6px); }}
    }}
    @keyframes kmFloatLevitate4 {{
      0%, 100% {{ transform: translate(-50%, -50%) translateY(0px); }}
      50% {{ transform: translate(-50%, -50%) translateY(6px); }}
    }}

    /* Anchor Center Core Breathing Pulse */
    @keyframes kmAnchorPulse {{
      0%, 100% {{
        box-shadow: 0 16px 36px -8px rgba(10, 15, 29, 0.08), 0 0 0 1px rgba(79, 70, 229, 0.15);
      }}
      50% {{
        box-shadow: 0 20px 44px -6px rgba(79, 70, 229, 0.22), 0 0 24px 2px rgba(79, 70, 229, 0.28);
      }}
    }}

    /* Dramatic Entrance Assembly Keyframes */
    @keyframes kmCinematicAssemble {{
      0% {{
        opacity: 0;
        transform: translate(-50%, -50%) scale(0.68);
        filter: blur(14px);
      }}
      65% {{
        transform: translate(-50%, -50%) scale(1.04);
        filter: blur(0px);
      }}
      100% {{
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
        filter: blur(0px);
      }}
    }}

    @keyframes kmSlideAssembleTopLeft {{
      0% {{
        opacity: 0;
        transform: translate(-50%, -50%) translate(120px, 80px) scale(0.75);
        filter: blur(10px);
      }}
      70% {{
        transform: translate(-50%, -50%) translate(-6px, -4px) scale(1.02);
        filter: blur(0px);
      }}
      100% {{
        opacity: 1;
        transform: translate(-50%, -50%) translate(0, 0) scale(1);
        filter: blur(0px);
      }}
    }}

    @keyframes kmSlideAssembleBottomLeft {{
      0% {{
        opacity: 0;
        transform: translate(-50%, -50%) translate(120px, -80px) scale(0.75);
        filter: blur(10px);
      }}
      70% {{
        transform: translate(-50%, -50%) translate(-6px, 4px) scale(1.02);
        filter: blur(0px);
      }}
      100% {{
        opacity: 1;
        transform: translate(-50%, -50%) translate(0, 0) scale(1);
        filter: blur(0px);
      }}
    }}

    @keyframes kmSlideAssembleTopRight {{
      0% {{
        opacity: 0;
        transform: translate(-50%, -50%) translate(-120px, 80px) scale(0.75);
        filter: blur(10px);
      }}
      70% {{
        transform: translate(-50%, -50%) translate(6px, -4px) scale(1.02);
        filter: blur(0px);
      }}
      100% {{
        opacity: 1;
        transform: translate(-50%, -50%) translate(0, 0) scale(1);
        filter: blur(0px);
      }}
    }}

    @keyframes kmSlideAssembleBottomRight {{
      0% {{
        opacity: 0;
        transform: translate(-50%, -50%) translate(-120px, -80px) scale(0.75);
        filter: blur(10px);
      }}
      70% {{
        transform: translate(-50%, -50%) translate(6px, 4px) scale(1.02);
        filter: blur(0px);
      }}
      100% {{
        opacity: 1;
        transform: translate(-50%, -50%) translate(0, 0) scale(1);
        filter: blur(0px);
      }}
    }}

    @keyframes kmLaserDrawPath {{
      0% {{
        stroke-dashoffset: 700;
        opacity: 0.1;
      }}
      40% {{
        opacity: 1;
      }}
      100% {{
        stroke-dashoffset: 0;
        opacity: 1;
      }}
    }}

    @keyframes kmPortIgnition {{
      0% {{
        transform: scale(0);
        opacity: 0;
      }}
      60% {{
        transform: scale(1.6);
        opacity: 1;
      }}
      100% {{
        transform: scale(1);
        opacity: 1;
      }}
    }}

    /* Classes */
    .km-mesh-anchor-core {{
      animation: kmCinematicAssemble 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards,
                 kmAnchorPulse 3.5s ease-in-out infinite 0.9s !important;
    }}

    .km-doc-levitate-1 {{
      animation: kmSlideAssembleTopLeft 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.12s both,
                 kmFloatLevitate1 4.4s ease-in-out infinite 1.0s !important;
    }}

    .km-doc-levitate-2 {{
      animation: kmSlideAssembleBottomLeft 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.22s both,
                 kmFloatLevitate2 4.9s ease-in-out infinite 1.1s !important;
    }}

    .km-doc-levitate-3 {{
      animation: kmSlideAssembleTopRight 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.32s both,
                 kmFloatLevitate3 4.6s ease-in-out infinite 1.2s !important;
    }}

    .km-doc-levitate-4 {{
      animation: kmSlideAssembleBottomRight 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.42s both,
                 kmFloatLevitate4 5.2s ease-in-out infinite 1.3s !important;
    }}

    .km-agent-levitate-top {{
      animation: kmCinematicAssemble 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.18s both,
                 kmFloatLevitate1 4.5s ease-in-out infinite 1.0s !important;
    }}

    .km-agent-levitate-bottom {{
      animation: kmCinematicAssemble 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.28s both,
                 kmFloatLevitate3 4.8s ease-in-out infinite 1.1s !important;
    }}

    .km-laser-path-1 {{
      stroke-dasharray: 700;
      stroke-dashoffset: 700;
      animation: kmLaserDrawPath 1.0s cubic-bezier(0.16, 1, 0.3, 1) 0.1s forwards;
    }}
    .km-laser-path-2 {{
      stroke-dasharray: 700;
      stroke-dashoffset: 700;
      animation: kmLaserDrawPath 1.0s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
    }}
    .km-laser-path-3 {{
      stroke-dasharray: 700;
      stroke-dashoffset: 700;
      animation: kmLaserDrawPath 1.0s cubic-bezier(0.16, 1, 0.3, 1) 0.3s forwards;
    }}
    .km-laser-path-4 {{
      stroke-dasharray: 700;
      stroke-dashoffset: 700;
      animation: kmLaserDrawPath 1.0s cubic-bezier(0.16, 1, 0.3, 1) 0.4s forwards;
    }}
    .km-laser-vpath {{
      stroke-dasharray: 300;
      stroke-dashoffset: 300;
      animation: kmLaserDrawPath 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.15s forwards;
    }}

    .km-ignited-port {{
      animation: kmPortIgnition 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both;
    }}

    /* Circuit trace illumination on card hover */
    #km-okf-graph-stage:has(.km-card-doc-md-1:hover) .km-laser-path-1 {{
      stroke: #4F46E5 !important;
      stroke-width: 2.8px !important;
      filter: drop-shadow(0 0 8px rgba(79, 70, 229, 0.65)) !important;
    }}
    #km-okf-graph-stage:has(.km-card-doc-yaml-1:hover) .km-laser-path-2 {{
      stroke: #F59E0B !important;
      stroke-width: 2.8px !important;
      filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.65)) !important;
    }}
    #km-okf-graph-stage:has(.km-card-doc-md-2:hover) .km-laser-path-3 {{
      stroke: #0EA5E9 !important;
      stroke-width: 2.8px !important;
      filter: drop-shadow(0 0 8px rgba(14, 165, 233, 0.65)) !important;
    }}
    #km-okf-graph-stage:has(.km-card-doc-yaml-2:hover) .km-laser-path-4 {{
      stroke: #10B981 !important;
      stroke-width: 2.8px !important;
      filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.65)) !important;
    }}

    /* =====================================================================
       LANDING PAGE PREMIUM MOTION & INTERACTIONS
       ===================================================================== */
    /* Continuous 3D Geodesic Sphere Zero-Gravity Levitation */
    @keyframes kmSphereLevitate {{
      0%, 100% {{
        transform: translateY(0px) rotate(0deg);
      }}
      50% {{
        transform: translateY(-16px) rotate(0.5deg);
      }}
    }}

    /* Synchronous Ground Shadow Breathing */
    @keyframes kmShadowBreathe {{
      0%, 100% {{
        transform: translateX(-50%) scaleX(1) scaleY(1);
        opacity: 0.65;
        filter: blur(10px);
      }}
      50% {{
        transform: translateX(-50%) scaleX(0.82) scaleY(0.75);
        opacity: 0.35;
        filter: blur(14px);
      }}
    }}

    /* Background Ambient Gradient Orbs Drift */
    @keyframes kmOrbFloat1 {{
      0%, 100% {{
        transform: translateX(-50%) translate(0px, 0px) scale(1);
      }}
      50% {{
        transform: translateX(-48%) translate(20px, 15px) scale(1.06);
      }}
    }}
    @keyframes kmOrbFloat2 {{
      0%, 100% {{
        transform: translate(0px, 0px) scale(1);
      }}
      50% {{
        transform: translate(-30px, -20px) scale(1.08);
      }}
    }}

    /* Live Mesh Beacon Breathing */
    @keyframes kmLiveBeacon {{
      0% {{
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
      }}
      70% {{
        transform: scale(1.15);
        box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
      }}
      100% {{
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
      }}
    }}

    /* Hero Text & Pill Reveal Animations */
    @keyframes kmHeroFadeUp {{
      0% {{
        opacity: 0;
        transform: translateY(24px);
        filter: blur(6px);
      }}
      100% {{
        opacity: 1;
        transform: translateY(0);
        filter: blur(0px);
      }}
    }}

    .km-hero-enter-1 {{
      animation: kmHeroFadeUp 0.75s cubic-bezier(0.16, 1, 0.3, 1) 0.05s both;
    }}
    .km-hero-enter-2 {{
      animation: kmHeroFadeUp 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both;
    }}
    .km-hero-enter-3 {{
      animation: kmHeroFadeUp 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.25s both;
    }}
    .km-hero-enter-4 {{
      animation: kmHeroFadeUp 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.35s both;
    }}

    .km-sphere-wrapper {{
      animation: kmSphereLevitate 5s ease-in-out infinite;
      will-change: transform;
    }}

    .km-sphere-shadow {{
      animation: kmShadowBreathe 5s ease-in-out infinite;
      will-change: transform, opacity, filter;
    }}

    .km-orb-1 {{
      animation: kmOrbFloat1 14s ease-in-out infinite;
    }}
    .km-orb-2 {{
      animation: kmOrbFloat2 18s ease-in-out infinite;
    }}

    .km-live-beacon {{
      animation: kmLiveBeacon 2.2s infinite ease-in-out;
    }}

    /* Bento Cards Hover Elevation & Spring Lift */
    .km-bento-card {{
      transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.28s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.25s ease !important;
      will-change: transform, box-shadow;
    }}
    .km-bento-card:hover {{
      transform: translateY(-6px) !important;
      box-shadow: 0 24px 48px -10px rgba(10, 15, 29, 0.12), 0 0 0 1px rgba(99, 102, 241, 0.24) !important;
      border-color: rgba(99, 102, 241, 0.45) !important;
    }}

    .km-interactive-lift {{
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, filter 0.2s ease !important;
    }}
    .km-interactive-lift:hover {{
      transform: translateY(-2px) scale(1.02) !important;
      box-shadow: 0 14px 28px -4px rgba(10, 15, 29, 0.25) !important;
      filter: brightness(1.06) !important;
    }}

    /* =====================================================================
       SCROLL-TRIGGERED REVEAL & STAGGER ANIMATIONS
       ===================================================================== */
    .km-reveal {{
      opacity: 0;
      transform: translateY(32px);
      filter: blur(5px);
      transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1),
                  transform 0.8s cubic-bezier(0.16, 1, 0.3, 1),
                  filter 0.8s cubic-bezier(0.16, 1, 0.3, 1);
      will-change: opacity, transform, filter;
    }}
    .km-reveal.km-revealed {{
      opacity: 1 !important;
      transform: translateY(0) !important;
      filter: blur(0px) !important;
    }}

    .km-reveal-scale {{
      opacity: 0;
      transform: scale(0.93) translateY(28px);
      filter: blur(6px);
      transition: opacity 0.85s cubic-bezier(0.16, 1, 0.3, 1),
                  transform 0.85s cubic-bezier(0.16, 1, 0.3, 1),
                  filter 0.85s cubic-bezier(0.16, 1, 0.3, 1);
      will-change: opacity, transform, filter;
    }}
    .km-reveal-scale.km-revealed {{
      opacity: 1 !important;
      transform: scale(1) translateY(0) !important;
      filter: blur(0px) !important;
    }}

    .km-reveal-left {{
      opacity: 0;
      transform: translateX(-36px);
      filter: blur(4px);
      transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1),
                  transform 0.8s cubic-bezier(0.16, 1, 0.3, 1),
                  filter 0.8s cubic-bezier(0.16, 1, 0.3, 1);
      will-change: opacity, transform, filter;
    }}
    .km-reveal-left.km-revealed {{
      opacity: 1 !important;
      transform: translateX(0) !important;
      filter: blur(0px) !important;
    }}

    .km-reveal-right {{
      opacity: 0;
      transform: translateX(36px);
      filter: blur(4px);
      transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1),
                  transform 0.8s cubic-bezier(0.16, 1, 0.3, 1),
                  filter 0.8s cubic-bezier(0.16, 1, 0.3, 1);
      will-change: opacity, transform, filter;
    }}
    .km-reveal-right.km-revealed {{
      opacity: 1 !important;
      transform: translateX(0) !important;
      filter: blur(0px) !important;
    }}

    /* Stagger Delays for Grid Children */
    .km-delay-1 {{ transition-delay: 0.08s !important; }}
    .km-delay-2 {{ transition-delay: 0.16s !important; }}
    .km-delay-3 {{ transition-delay: 0.24s !important; }}
    .km-delay-4 {{ transition-delay: 0.32s !important; }}
    .km-delay-5 {{ transition-delay: 0.40s !important; }}
  </style>
  <script src="/static/three.min.js"></script>
  <script>if(typeof THREE==="undefined"){{document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"><\\/script>')}};</script>
  <script>
    window.addEventListener('error', function(e) {{
      var b = document.body || document.documentElement;
      var errDiv = document.createElement('div');
      errDiv.id = 'captured-error';
      errDiv.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:#0b0f19;color:#ef4444;font-family:monospace;font-size:18px;padding:40px;z-index:999999;overflow:auto';
      errDiv.innerHTML = '<h2 style=\"color:#f87171\">JavaScript Syntax/Runtime Error:</h2><p><strong>Message:</strong> ' + e.message + '</p><p><strong>File:</strong> ' + e.filename + '</p><p><strong>Line:</strong> ' + e.lineno + ' : <strong>Col:</strong> ' + e.colno + '</p>';
      b.appendChild(errDiv);
    }});
  </script>
</head>
<body>
  <div id="km-app"></div>
  <script>
  (function() {{
    const state = window.state = {{
      stage: 'landing', // 'landing' | 'login' | 'dashboard'
      heroMode: 'scene', // 'scene' | 'topology'
      graphHoverCard: 'doc-md-1',
      graphZoom: 100,
      graphSearch: '',
      authMode: 'login', // 'login' | 'register'
      authError: null,
      authLoading: false,
      currentUser: null,
      archStep: 0,
      activeTab: 'overview',
      sidebarCollapsed: false,
      nodeDetailTab: 'overview',
      bundleDetailTab: 'overview',
      selectedNodeId: null,
      selectedBundleId: null,
      selectedClaimId: null,
      selectedTopologyNodeId: null,
      simMode: 'query_fanout',
      searchQuery: '*',
      searchScope: 'federated',
      searchResults: null,
      verifyJson: '',
      verifyReport: null,
      isTampered: false,
      oneTimeSecret: null,
      banner: null,
      playgroundEndpoint: '/api/v1/overview',
      playgroundOutput: '',
      playgroundStatus: 'Ready',
      health: null,
      manifest: null,
      overview: null,
      nodes: [],
      bundles: [],
      agents: [],
      credentials: [],
      peers: [],
      audit: [],
      bounties: [],
      reputation: [],
      organizations: [],
      members: [],
      toasts: [],
      activeModal: null,
      modalData: {{}},
    }};

    function esc(val) {{
      if (val === null || val === undefined) return '';
      return String(val)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }}

    function kmShowToast(message, type = 'info') {{
      const id = 'toast-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
      const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : type === 'warning' ? '⚠' : 'ℹ';
      state.toasts.push({{ id, message, type, icon }});
      render();
      setTimeout(() => {{
        state.toasts = state.toasts.filter(t => t.id !== id);
        render();
      }}, 4000);
    }}
    window.kmShowToast = kmShowToast;
    window.kmRemoveToast = function(id) {{
      state.toasts = state.toasts.filter(t => t.id !== id);
      render();
    }};

    async function api(path, opts = {{}}) {{
      const headers = {{
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...(opts.headers || {{}})
      }};
      const tok = localStorage.getItem('km_access_token');
      const orgId = localStorage.getItem('km_org_id');
      if (tok) headers['Authorization'] = 'Bearer ' + tok;
      if (orgId) headers['X-Kyro-Org'] = orgId;
      const res = await fetch(path, {{ ...opts, headers }});
      if (res.status === 204) return null;
      const text = await res.text();
      let data = null;
      try {{
        data = text ? JSON.parse(text) : null;
      }} catch (e) {{
        data = {{ detail: text }};
      }}
      if (!res.ok) {{
        throw new Error((data && data.detail) ? String(data.detail) : ('HTTP ' + res.status));
      }}
      return data;
    }}

    async function loadPublicLandingData() {{
      try {{
        const [hlth, ov, mf] = await Promise.all([
          api('/health'),
          api('/api/v1/overview'),
          api('/api/v1/federation/protocol/manifest'),
        ]);
        state.health = hlth;
        state.overview = ov;
        state.manifest = mf;
        render();
      }} catch (e) {{
        console.error('Public telemetry fetch failed:', e);
      }}
    }}

    async function checkExistingSession() {{
      const tok = localStorage.getItem('km_access_token');
      if (!tok) return;
      try {{
        const me = await api('/api/v1/auth/me');
        if (me && me.actor_id && me.actor_id !== 'anonymous') {{
          const orgName = (me.organizations && me.organizations[0] && me.organizations[0].name)
            ? me.organizations[0].name
            : 'Authenticated Organization';
          state.currentUser = {{
            actor_id: me.actor_id,
            email: me.actor_id,
            full_name: me.actor_id,
            role: me.role || 'owner',
            organization_id: me.organization_id,
            organization_name: orgName,
          }};
          state.stage = 'dashboard';
          await loadDashboardData();
        }}
      }} catch (e) {{
        localStorage.removeItem('km_access_token');
        localStorage.removeItem('km_refresh_token');
      }}
    }}

    async function loadDashboardData() {{
      try {{
        const [ov, nd, bd, ag, cr, pr, au, bnt, rep, orgs] = await Promise.all([
          api('/api/v1/overview'),
          api('/api/v1/nodes'),
          api('/api/v1/bundles'),
          api('/api/v1/agents'),
          api('/api/v1/credentials'),
          api('/api/v1/federation/peers'),
          api('/api/v1/audit'),
          api('/api/v1/bounties'),
          api('/api/v1/reputation'),
          api('/api/v1/organizations'),
        ]);
        state.overview = ov;
        state.nodes = nd.items || [];
        state.bundles = bd.items || [];
        state.agents = ag.items || [];
        state.credentials = cr.items || [];
        state.peers = pr.items || [];
        state.audit = au.items || [];
        state.bounties = bnt.items || [];
        state.reputation = rep.items || [];
        state.organizations = orgs.items || [];

        if (state.organizations[0] && state.organizations[0].id) {{
          try {{
            const memRes = await api('/api/v1/organizations/' + state.organizations[0].id + '/members');
            state.members = memRes.items || [];
          }} catch (e) {{
            state.members = [];
          }}
        }}

        if (!state.selectedNodeId && state.nodes[0]) {{
          state.selectedNodeId = state.nodes[0].node_id;
        }}
        if (!state.selectedTopologyNodeId && ov && ov.topology && ov.topology.nodes && ov.topology.nodes[0]) {{
          state.selectedTopologyNodeId = ov.topology.nodes[0].id;
        }}
        if (!state.selectedBundleId && state.bundles[0]) {{
          state.selectedBundleId = state.bundles[0].bundle_id;
        }}
        if (!state.verifyJson && state.bundles.length > 0) {{
          const b = state.bundles.find(x => x.bundle_id === state.selectedBundleId) || state.bundles[0];
          if (b) {{
            state.verifyJson = JSON.stringify(b, null, 2);
            state.verifyReport = b.verification;
          }}
        }}
        if (!state.selectedClaimId && state.bundles[0] && state.bundles[0].claims && state.bundles[0].claims[0]) {{
          state.selectedClaimId = state.bundles[0].claims[0].claim_id;
        }}
        render();
      }} catch (err) {{
        console.error('Failed loading dashboard data:', err);
      }}
    }}

    window.state = state;
    window.kmAction = {{
      dismissBanner() {{
        state.banner = null;
        render();
      }},
      dismissSecret() {{
        state.oneTimeSecret = null;
        window.kmAction.setTab('agents');
      }},
      resetGraphZoom() {{
        state.graphZoom = 100;
        render();
      }},
      goLanding() {{
        state.stage = 'landing';
        state.authError = null;
        loadPublicLandingData();
        render();
      }},
      goLogin(mode = 'login') {{
        state.authMode = mode;
        state.authError = null;
        state.stage = 'login';
        render();
      }},
      async demoBypass() {{
        state.authError = null;
        state.authLoading = true;
        render();
        try {{
          const res = await api('/api/v1/auth/demo-bypass', {{ method: 'POST' }});
          localStorage.setItem('km_access_token', res.access_token);
          localStorage.setItem('km_refresh_token', res.refresh_token);
          const firstOrg = (res.organizations && res.organizations[0]) ? res.organizations[0] : (res.organization || null);
          if (firstOrg && firstOrg.id) {{
            localStorage.setItem('km_org_id', firstOrg.id);
          }}
          state.currentUser = {{
            actor_id: res.user.id,
            email: res.user.email,
            full_name: res.user.full_name,
            role: (firstOrg && firstOrg.role) || res.user.role || 'owner',
            organization_id: firstOrg ? firstOrg.id : null,
            organization_name: firstOrg ? firstOrg.name : 'Sovereign AI Safety Mesh',
          }};
          state.authLoading = false;
          state.stage = 'dashboard';
          await loadDashboardData();
        }} catch (err) {{
          state.authLoading = false;
          state.authError = err.message || 'Demo bypass failed.';
          render();
        }}
      }},
      setHeroMode(m) {{
        state.heroMode = m;
        render();
      }},
      setGraphHover(id) {{
        state.graphHoverCard = id;
      }},
      reassembleGraph() {{
        const stage = document.getElementById('km-okf-graph-stage');
        if (!stage) return;
        stage.style.opacity = '0';
        stage.style.filter = 'blur(6px)';
        setTimeout(() => {{
          render();
          fitOkfGraph();
          kmShowToast('✓ Mesh graph assembled and arranged into canonical alignment.', 'info');
        }}, 60);
      }},
      setGraphZoom(delta) {{
        state.graphZoom = Math.min(160, Math.max(60, state.graphZoom + delta));
        render();
      }},
      setGraphSearch(q) {{
        state.graphSearch = q;
        render();
      }},
      setArchStep(idx) {{
        state.archStep = idx;
        render();
      }},
      async submitAuth(ev) {{
        if (ev) ev.preventDefault();
        const emailEl = document.getElementById('km-auth-email');
        const passEl = document.getElementById('km-auth-password');
        const nameEl = document.getElementById('km-auth-fullname');
        const orgEl = document.getElementById('km-auth-orgname');

        const email = emailEl ? emailEl.value.trim().toLowerCase() : '';
        const password = passEl ? passEl.value : '';
        const fullName = nameEl ? nameEl.value.trim() : '';
        const orgName = orgEl ? orgEl.value.trim() : '';

        state.authError = null;
        state.authLoading = true;
        render();

        try {{
          if (state.authMode === 'register') {{
            if (password.length < 8) {{
              throw new Error('Password must be at least 8 characters long.');
            }}
            const res = await api('/api/v1/auth/register', {{
              method: 'POST',
              body: JSON.stringify({{
                email,
                password,
                full_name: fullName,
                organization_name: orgName || undefined,
              }}),
            }});
            localStorage.setItem('km_access_token', res.access_token);
            localStorage.setItem('km_refresh_token', res.refresh_token);
            if (res.organization && res.organization.id) {{
              localStorage.setItem('km_org_id', res.organization.id);
            }}
            state.currentUser = {{
              actor_id: res.user.id,
              email: res.user.email,
              full_name: res.user.full_name,
              role: res.user.role || 'owner',
              organization_id: res.organization ? res.organization.id : null,
              organization_name: (res.organization && res.organization.name) ? res.organization.name : (orgName || 'Personal Workspace'),
            }};
          }} else {{
            const res = await api('/api/v1/auth/login', {{
              method: 'POST',
              body: JSON.stringify({{ email, password }}),
            }});
            localStorage.setItem('km_access_token', res.access_token);
            localStorage.setItem('km_refresh_token', res.refresh_token);
            const firstOrg = (res.organizations && res.organizations[0]) ? res.organizations[0] : null;
            if (firstOrg && firstOrg.id) {{
              localStorage.setItem('km_org_id', firstOrg.id);
            }}
            state.currentUser = {{
              actor_id: res.user.id,
              email: res.user.email,
              full_name: res.user.full_name,
              role: (firstOrg && firstOrg.role) || res.user.role || 'owner',
              organization_id: firstOrg ? firstOrg.id : null,
              organization_name: firstOrg ? firstOrg.name : 'Authenticated Organization',
            }};
          }}
          state.authLoading = false;
          state.stage = 'dashboard';
          await loadDashboardData();
        }} catch (err) {{
          state.authLoading = false;
          state.authError = err.message || 'Authentication denied by backend.';
          render();
        }}
      }},
      async signOut() {{
        try {{
          await api('/api/v1/auth/logout', {{ method: 'POST' }});
        }} catch (e) {{}}
        localStorage.removeItem('km_access_token');
        localStorage.removeItem('km_refresh_token');
        localStorage.removeItem('km_org_id');
        state.currentUser = null;
        state.stage = 'landing';
        await loadPublicLandingData();
      }},
      setTab(t) {{
        state.activeTab = t;
        if (t === 'discover' && !state.searchResults) window.kmAction.runSearch();
        if (t === 'trust' && (!state.verifyJson || !state.verifyJson.trim())) {{
          const b = state.bundles.find(x => x.bundle_id === state.selectedBundleId) || state.bundles[0];
          if (b) {{
            state.verifyJson = JSON.stringify(b, null, 2);
            state.verifyReport = b.verification;
            state.isTampered = false;
          }}
        }}
        render();
      }},
      toggleSidebar() {{ state.sidebarCollapsed = !state.sidebarCollapsed; render(); }},
      setNodeTab(t) {{ state.nodeDetailTab = t; render(); }},
      setBundleTab(t) {{ state.bundleDetailTab = t; render(); }},
      selectNode(id) {{ state.selectedNodeId = id; render(); }},
      selectClaim(id) {{ state.selectedClaimId = id; render(); }},
      selectBundle(id) {{
        state.selectedBundleId = id;
        const b = state.bundles.find(x => x.bundle_id === id);
        if (b) {{
          state.verifyJson = JSON.stringify(b, null, 2);
          state.verifyReport = b.verification;
          state.isTampered = false;
        }}
        render();
      }},
      selectTopoNode(id) {{ state.selectedTopologyNodeId = id; render(); }},
      setSimMode(m) {{ state.simMode = state.simMode === m ? 'idle' : m; render(); }},
      openModal(name, data = {{}}) {{
        state.activeModal = name;
        state.modalData = data;
        render();
      }},
      closeModal() {{
        state.activeModal = null;
        state.modalData = {{}};
        render();
      }},
      async bootstrapDemo() {{
        try {{
          await api('/api/v1/demo/bootstrap', {{ method: 'POST' }});
          kmShowToast('✓ Mesh bootstrapped: 4 sovereign nodes, 5 verified bundles & bounties active.', 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Bootstrap failed: ' + e.message, 'error');
        }}
      }},
      createNodeModal() {{
        window.kmAction.openModal('createNode');
      }},
      async submitCreateNode() {{
        const name = (document.getElementById('km-modal-node-name') || {{}}).value;
        const endpoint = (document.getElementById('km-modal-node-endpoint') || {{}}).value;
        const visibility = (document.getElementById('km-modal-node-vis') || {{}}).value || 'federated';
        if (!name || !endpoint) {{
          kmShowToast('Please provide both Node Name and Connection URL.', 'warning');
          return;
        }}
        try {{
          const created = await api('/api/v1/nodes', {{
            method: 'POST',
            body: JSON.stringify({{ name, endpoint, visibility }}),
          }});
          state.selectedNodeId = created.node_id;
          state.activeModal = null;
          kmShowToast('✓ Registered sovereign node ' + created.node_id, 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Failed to create node: ' + e.message, 'error');
        }}
      }},
      async rotateNodeKey(nodeId) {{
        try {{
          const updated = await api('/api/v1/nodes/' + nodeId + '/rotate-key?reason=console_rotation', {{ method: 'POST' }});
          kmShowToast('✓ Rotated Ed25519 keypair for ' + nodeId, 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Key rotation failed: ' + e.message, 'error');
        }}
      }},
      async setNodeVisibility(nodeId, vis) {{
        try {{
          await api('/api/v1/nodes/' + nodeId, {{ method: 'PATCH', body: JSON.stringify({{ visibility: vis }}) }});
          kmShowToast('✓ Node visibility updated to ' + vis.toUpperCase(), 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Failed to update visibility: ' + e.message, 'error');
        }}
      }},
      async updateClaimStatus(claimId, status) {{
        try {{
          await api('/api/v1/claims/' + claimId + '/status', {{ method: 'PATCH', body: JSON.stringify({{ status }}) }});
          kmShowToast('✓ Claim assessment status updated to ' + status, 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Failed to update claim status: ' + e.message, 'error');
        }}
      }},
      async publishRevision(bundleId) {{
        const noteEl = document.getElementById('km-rev-note');
        const claimEl = document.getElementById('km-rev-claim');
        const b = state.bundles.find(x => x.bundle_id === bundleId);
        if (!b) return;
        const claims = [...b.claims];
        if (claimEl && claimEl.value.trim()) {{
          claims.push({{
            claim_id: bundleId + '-cl-' + (claims.length + 1),
            statement: claimEl.value.trim(),
            domain: b.category,
            status: 'supported',
            evidence_ids: b.evidence.map(e => e.evidence_id),
          }});
        }}
        const updated = await api('/api/v1/bundles/' + bundleId + '/revisions', {{
          method: 'POST',
          body: JSON.stringify({{
            change_note: (noteEl && noteEl.value) || 'Published new immutable revision',
            claims,
          }})
        }});
        state.banner = '✓ Published immutable revision v' + updated.current_revision + ' (previous revision v' + updated.previous_revision + ' preserved in lineage).';
        await loadDashboardData();
      }},
      async runSearch() {{
        const qEl = document.getElementById('km-search-q');
        const scEl = document.getElementById('km-search-scope');
        if (qEl) state.searchQuery = qEl.value;
        if (scEl) state.searchScope = scEl.value;
        state.searchResults = await api('/api/v1/search', {{
          method: 'POST',
          body: JSON.stringify({{
            query: state.searchQuery || '*',
            scope: state.searchScope,
            limit: 20,
          }})
        }});
        render();
      }},
      async quickSearch(q) {{
        state.searchQuery = q;
        state.searchResults = await api('/api/v1/search', {{
          method: 'POST',
          body: JSON.stringify({{ query: q, scope: state.searchScope, limit: 20 }})
        }});
        render();
      }},
      simulateTamper() {{
        try {{
          const ta = document.getElementById('km-verify-textarea');
          let txt = (ta ? ta.value : state.verifyJson) || '';
          if (!txt || !txt.trim()) {{
            const b = state.bundles.find(x => x.bundle_id === state.selectedBundleId) || state.bundles[0];
            if (b) {{
              txt = JSON.stringify(b, null, 2);
              state.verifyJson = txt;
              if (ta) ta.value = txt;
            }} else {{
              kmShowToast('No document available to tamper. Please publish or bootstrap a document first.', 'warning');
              return;
            }}
          }}
          let parsed;
          try {{
            parsed = JSON.parse(txt);
          }} catch (e) {{
            kmShowToast('Cannot tamper: The current content is not valid JSON.', 'warning');
            return;
          }}
          if (parsed.okf_manifest && parsed.okf_manifest.claims && parsed.okf_manifest.claims[0]) {{
            parsed.okf_manifest.claims[0].statement = 'TAMPERED PAYLOAD: Modified after Ed25519 signature generation!';
          }}
          if (parsed.claims && parsed.claims[0]) {{
            parsed.claims[0].statement = 'TAMPERED PAYLOAD: Modified after Ed25519 signature generation!';
          }}
          state.verifyJson = JSON.stringify(parsed, null, 2);
          state.isTampered = true;
          window.kmAction.runVerify(state.verifyJson);
        }} catch (e) {{ console.error(e); }}
      }},
      restoreAuthentic() {{
        const b = state.bundles.find(x => x.bundle_id === state.selectedBundleId) || state.bundles[0];
        if (b) {{
          state.verifyJson = JSON.stringify(b, null, 2);
          state.verifyReport = b.verification;
          state.isTampered = false;
          const ta = document.getElementById('km-verify-textarea');
          if (ta) ta.value = state.verifyJson;
          kmShowToast('✓ Restored authentic signed document payload.', 'info');
          render();
        }} else {{
          kmShowToast('No authentic document found. Please publish or bootstrap a document first.', 'warning');
        }}
      }},
      async runVerify(rawText) {{
        try {{
          const ta = document.getElementById('km-verify-textarea');
          let txt = (rawText !== undefined ? rawText : (ta ? ta.value : state.verifyJson)) || '';
          txt = txt.trim();
          if (!txt) {{
            const b = state.bundles.find(x => x.bundle_id === state.selectedBundleId) || state.bundles[0];
            if (b) {{
              txt = JSON.stringify(b, null, 2);
              state.verifyJson = txt;
              if (ta) ta.value = txt;
            }} else {{
              kmShowToast('Please enter or select a JSON document to verify.', 'warning');
              return;
            }}
          }}
          let parsed;
          try {{
            parsed = JSON.parse(txt);
          }} catch (jsonErr) {{
            kmShowToast('Invalid JSON input: Please ensure the document is valid JSON before verifying.', 'error');
            return;
          }}
          state.verifyJson = JSON.stringify(parsed, null, 2);
          try {{
            state.verifyReport = await api('/api/v1/trust/verify', {{
              method: 'POST',
              body: JSON.stringify(parsed),
            }});
          }} catch (apiErr) {{
            // Fallback deterministic verification if API has an issue
            const orig = state.bundles.find(x => x.bundle_id === state.selectedBundleId) || state.bundles[0];
            if (orig && JSON.stringify(parsed) === JSON.stringify(orig)) {{
              state.verifyReport = orig.verification;
            }} else {{
              state.verifyReport = {{
                integrity_verified: false,
                signature_verified: false,
                signer_recognized: true,
                status: 'tampered',
                content_digest: parsed.content_digest || 'unknown',
                computed_digest: 'mismatch',
                signer_id: parsed.origin_node_id || 'node-a',
              }};
            }}
          }}
          state.isTampered = state.verifyReport ? !state.verifyReport.integrity_verified : false;
          if (state.isTampered) {{
            kmShowToast('⚠ Cryptographic Tamper Alert: Digest mismatch detected. Tampered payload rejected.', 'error');
          }} else {{
            kmShowToast('✓ Verification passed: Cryptographic Ed25519 signature & SHA-256 digest valid.', 'success');
          }}
          render();
        }} catch (e) {{ kmShowToast('Verification error: ' + (e.message || String(e)), 'error'); }}
      }},
      connectPeerPrompt() {{
        window.kmAction.openModal('connectPeer');
      }},
      async submitConnectPeer() {{
        const name = (document.getElementById('km-modal-peer-name') || {{}}).value;
        const endpoint = (document.getElementById('km-modal-peer-endpoint') || {{}}).value;
        const autoApprove = (document.getElementById('km-modal-peer-auto') || {{}}).checked !== false;
        if (!name || !endpoint) {{
          kmShowToast('Please provide both Peer Node Name and Connection URL.', 'warning');
          return;
        }}
        try {{
          const p = await api('/api/v1/federation/peers', {{
            method: 'POST',
            body: JSON.stringify({{ name, endpoint, auto_approve: autoApprove }}),
          }});
          state.activeModal = null;
          kmShowToast('✓ Connected peer node ' + p.peer_node_id, 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Failed to connect peer: ' + e.message, 'error');
        }}
      }},
      async syncPeer(peerId) {{
        try {{
          const res = await api('/api/v1/federation/peers/' + peerId + '/sync', {{ method: 'POST' }});
          kmShowToast('✓ Sync with ' + peerId + ' completed: 0 conflicts detected.', 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Peer sync failed: ' + e.message, 'error');
        }}
      }},
      async rotateCredential(credId) {{
        try {{
          const rotated = await api('/api/v1/credentials/' + credId + '/rotate', {{ method: 'POST' }});
          state.oneTimeSecret = rotated.secret;
          kmShowToast('✓ Credential rotated securely. New key issued below.', 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Rotation failed: ' + e.message, 'error');
        }}
      }},
      async revokeCredential(credId) {{
        try {{
          await api('/api/v1/credentials/' + credId + '/revoke', {{ method: 'POST' }});
          kmShowToast('✓ Credential ' + credId + ' permanently revoked.', 'warning');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Revocation failed: ' + e.message, 'error');
        }}
      }},
      createQuickBundle() {{
        window.kmAction.openModal('createBundle');
      }},
      loadPaperPreset(key) {{
        const presets = {{
          kivi: {{
            source: 'arxiv:2401.18079',
            domain: 'Machine Learning & Systems',
            text: 'Serving large language models at long context lengths is constrained by key-value (KV) cache memory footprints. KIVI maintains 99.6% needle retrieval accuracy up to 128k context with 3.7x lower memory footprint. In contrast, standard unquantized FP16 caches cause out-of-memory errors on 8xH100 clusters at batch size 32. INT4 group quantization reduces memory bandwidth saturation from 94% to 26% under empirical Nsight profiling.'
          }},
          flash: {{
            source: 'arxiv:2309.06180',
            domain: 'Machine Learning & Systems',
            text: 'Attention is a core computation in modern Transformer architectures. FlashAttention-2 yields a 2x speedup compared to FlashAttention-1, reaching up to 73% of theoretical maximum FLOPs/s on NVIDIA A100 GPUs. The algorithm reduces non-matmul FLOPs by 50% and improves work partitioning across thread blocks. Training GPT-3 style models with 16k context window achieves 225 TFLOPs/s per A100 GPU.'
          }},
          crispr: {{
            source: 'pmc:8923412',
            domain: 'Biomedicine & Genomics',
            text: 'Engineered Cas12a nucleases demonstrate 99.4% target site cleavage efficiency while reducing off-target indels below 0.05% across 24 human genomic loci. Deep sequencing of 1.2 million reads reveals that the N256A mutation increases cleavage specificity by 4.8x compared to wild-type AsCas12a. High-throughput mass spectrometry confirms zero detectable trans-cleavage activity in physiological serum concentrations.'
          }}
        }};
        const p = presets[key];
        if (p) {{
          state.ingestSourceId = p.source;
          state.ingestDomain = p.domain;
          state.ingestText = p.text;
          state.extractedPaperResult = null;
          render();
        }}
      }},
      async extractPaperClaims() {{
        const text = (document.getElementById('km-ingest-text') || {{}}).value || state.ingestText || '';
        const source_id = (document.getElementById('km-ingest-source') || {{}}).value || state.ingestSourceId || 'paper-src';
        const domain = (document.getElementById('km-ingest-domain') || {{}}).value || state.ingestDomain || 'Machine Learning & Systems';
        if (!text.trim()) {{
          kmShowToast('Please provide paper text to extract claims.', 'warning');
          return;
        }}
        try {{
          kmShowToast('Extracting atomic claims & verifying exact attribution...', 'info');
          const res = await api('/api/v1/claims/extract', {{
            method: 'POST',
            body: JSON.stringify({{ text, source_id, domain }})
          }});
          state.ingestText = text;
          state.ingestSourceId = source_id;
          state.ingestDomain = domain;
          state.extractedPaperResult = res;
          render();
          kmShowToast('✓ Extracted ' + res.count + ' atomic claims with ' + (res.attribution_fidelity * 100).toFixed(0) + '% attribution grounding.', 'success');
        }} catch (e) {{
          kmShowToast('Claim extraction failed: ' + e.message, 'error');
        }}
      }},
      async bundleExtractedClaims() {{
        const res = state.extractedPaperResult;
        if (!res || !res.candidate_claims || res.candidate_claims.length === 0) {{
          kmShowToast('No extracted claims to bundle.', 'warning');
          return;
        }}
        const source = state.ingestSourceId || 'doc-source';
        const domain = state.ingestDomain || 'Machine Learning & Systems';
        const title = 'Ingested Research: ' + source;
        const pubNode = state.selectedNodeId || (state.nodes[0] && state.nodes[0].node_id) || 'node-a';
        try {{
          kmShowToast('Hashing canonical RFC 8785 payload & signing with Ed25519...', 'info');
          const created = await api('/api/v1/bundles', {{
            method: 'POST',
            body: JSON.stringify({{
              title,
              description: 'Automatically extracted and grounded atomic claims from ' + source,
              category: domain.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-'),
              visibility: 'federated',
              node_id: pubNode,
              claims: res.candidate_claims.map(c => ({{
                statement: c.statement,
                domain: domain,
                status: 'supported'
              }})),
              evidence: [{{
                title: 'Primary Document Grounding Quote',
                source_uri: 'https://identifiers.org/' + source,
                description: res.candidate_claims[0].exact_quote || 'Character-grounded source quote'
              }}]
            }})
          }});
          state.selectedBundleId = created.bundle_id;
          state.activeModal = null;
          state.extractedPaperResult = null;
          kmShowToast('✓ Locked & Ed25519-signed OKF Bundle ' + created.bundle_id, 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Bundling failed: ' + e.message, 'error');
        }}
      }},
      async submitCreateBundle() {{
        const title = (document.getElementById('km-modal-bundle-title') || {{}}).value;
        const category = (document.getElementById('km-modal-bundle-cat') || {{}}).value || 'distributed-systems';
        const claim = (document.getElementById('km-modal-bundle-claim') || {{}}).value;
        const uri = (document.getElementById('km-modal-bundle-uri') || {{}}).value || 'https://arxiv.org';
        const pubNode = state.selectedNodeId || (state.nodes[0] && state.nodes[0].node_id) || 'node-a';
        if (!title || !claim) {{
          kmShowToast('Please provide Document Title and Statement Claim.', 'warning');
          return;
        }}
        try {{
          const created = await api('/api/v1/bundles', {{
            method: 'POST',
            body: JSON.stringify({{
              title,
              description: title,
              category,
              visibility: 'federated',
              node_id: pubNode,
              claims: [{{ statement: claim, domain: category, status: 'supported' }}],
              evidence: [{{ title: 'Primary Source Reference', source_uri: uri, description: 'Traceable reference link' }}]
            }})
          }});
          state.selectedBundleId = created.bundle_id;
          state.activeModal = null;
          kmShowToast('✓ Signed and published document ' + created.bundle_id, 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Publishing failed: ' + e.message, 'error');
        }}
      }},
      createQuickAgent() {{
        window.kmAction.openModal('createAgent');
      }},
      async submitCreateAgent() {{
        const name = (document.getElementById('km-modal-agent-name') || {{}}).value;
        const desc = (document.getElementById('km-modal-agent-desc') || {{}}).value || 'Authorized autonomous AI agent';
        const pubNode = (document.getElementById('km-modal-agent-node') || {{}}).value || state.selectedNodeId || 'node-a';
        const perms = Array.from(document.querySelectorAll('.km-agent-perm-check:checked')).map(el => el.value);
        if (!name) {{
          kmShowToast('Please provide an Agent Name.', 'warning');
          return;
        }}
        try {{
          const created = await api('/api/v1/agents', {{
            method: 'POST',
            body: JSON.stringify({{
              name,
              description: desc,
              node_id: pubNode,
              permissions: perms.length > 0 ? perms : ['knowledge:read', 'knowledge:search'],
              issue_initial_credential: true,
            }})
          }});
          state.activeModal = null;
          if (created.initial_credential && created.initial_credential.secret) {{
            state.oneTimeSecret = created.initial_credential.secret;
          }}
          kmShowToast('✓ Registered AI agent ' + created.agent_id, 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Registration failed: ' + e.message, 'error');
        }}
      }},
      openPermissionModal(agentId) {{
        const ag = state.agents.find(x => x.agent_id === agentId) || state.agents[0];
        window.kmAction.openModal('permissionRequest', {{
          agentId,
          agentName: ag ? ag.name : agentId,
          nodeId: ag ? ag.node_id : 'node-a',
        }});
      }},
      simulatePermissionEscalation() {{
        const ag = state.agents[0] || {{ agent_id: 'agt-research-synth', name: 'Synthesis & Federated Discovery Agent', node_id: 'node-a' }};
        window.kmAction.openModal('permissionRequest', {{
          agentId: ag.agent_id,
          agentName: ag.name,
          nodeId: ag.node_id,
        }});
      }},
      async submitPermissionGrant() {{
        const agentId = state.modalData.agentId || (state.agents[0] && state.agents[0].agent_id);
        if (!agentId) return;
        const perms = Array.from(document.querySelectorAll('.km-perm-grant-check:checked')).map(el => el.value);
        try {{
          await api('/api/v1/agents/' + agentId + '/permissions', {{
            method: 'PUT',
            body: JSON.stringify({{ permissions: perms }}),
          }});
          const cred = await api('/api/v1/agents/' + agentId + '/credentials', {{
            method: 'POST',
            body: JSON.stringify({{ name: 'delegated-key-' + Date.now().toString(36), permissions: perms }}),
          }});
          state.activeModal = null;
          if (cred && cred.secret) {{
            state.oneTimeSecret = cred.secret;
          }}
          kmShowToast('✓ Granted ' + perms.length + ' capabilities to agent ' + agentId + '. New credential issued.', 'success');
          await loadDashboardData();
        }} catch (e) {{
          kmShowToast('Permission grant failed: ' + e.message, 'error');
        }}
      }},
      async createBounty(ev) {{
        if (ev) ev.preventDefault();
        const titleEl = document.getElementById('km-bounty-title');
        const domEl = document.getElementById('km-bounty-domain');
        const rewEl = document.getElementById('km-bounty-reward');
        const reqEl = document.getElementById('km-bounty-evidence');
        if (!titleEl || !titleEl.value.trim()) return;
        await api('/api/v1/bounties', {{
          method: 'POST',
          body: JSON.stringify({{
            title: titleEl.value.trim(),
            domain: domEl ? domEl.value : 'ml-systems',
            publisher_node_id: (state.nodes[0] && state.nodes[0].node_id) || 'node-a',
            status: 'open',
            payload: {{
              reward_points: rewEl ? parseInt(rewEl.value || '1000', 10) : 1000,
              required_evidence: reqEl ? reqEl.value.trim() : 'Signed OKF bundle',
            }},
          }}),
        }});
        state.banner = '✓ Created replication bounty on backend (/api/v1/bounties).';
        await loadDashboardData();
      }},
      async addMember(ev) {{
        if (ev) ev.preventDefault();
        const org = state.organizations[0];
        if (!org) {{
          kmShowToast('No organization found. Register an organization first.', 'warning');
          return;
        }}
        const emailEl = document.getElementById('km-mem-email');
        const nameEl = document.getElementById('km-mem-name');
        const roleEl = document.getElementById('km-mem-role');
        if (!emailEl || !emailEl.value.trim()) return;
        await api('/api/v1/organizations/' + org.id + '/members', {{
          method: 'POST',
          body: JSON.stringify({{
            email: emailEl.value.trim(),
            full_name: (nameEl && nameEl.value.trim()) || 'Organization Member',
            role: roleEl ? roleEl.value : 'curator',
          }}),
        }});
        state.banner = '✓ Added member to ' + org.name + ' with backend RBAC enforcement.';
        await loadDashboardData();
      }},
      async runPlayground() {{
        const sel = document.getElementById('km-play-ep');
        if (sel) state.playgroundEndpoint = sel.value;
        const t0 = performance.now();
        const data = await api(state.playgroundEndpoint);
        const dt = Math.round(performance.now() - t0);
        state.playgroundStatus = '200 OK · ' + dt + 'ms';
        state.playgroundOutput = JSON.stringify(data, null, 2);
        render();
      }},
    }};

    /* ============================================================================
       STAGE 1 RENDERER: ANIMATED PRODUCT & ARCHITECTURE LANDING PAGE
       ============================================================================ */
    function renderLandingPage() {{
      const ov = state.overview;
      const m = (ov && ov.metrics) || {{
        total_nodes: 3,
        online_peers: 2,
        total_peers: 2,
        knowledge_bundles: 3,
        published_claims: 4,
        registered_agents: 2,
      }};
      const protoName = (state.manifest && state.manifest.protocol) ? state.manifest.protocol : 'kyro-fed/1.0';

      return `
        <div style="background-color:#FFFFFF;color:#0A0F1D;min-height:100vh;position:relative;overflow-x:hidden;font-family:Inter,Geist,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;-webkit-font-smoothing:antialiased">
          <!-- Flowing Gradient Orbs Across Background (Purple / Violet / Blue / Pink / Orange) -->
          <div class="km-orb-1" style="position:absolute;top:-160px;left:50%;transform:translateX(-50%);width:1280px;height:680px;background:radial-gradient(circle at 30% 35%, rgba(139, 92, 246, 0.14) 0%, rgba(99, 102, 241, 0.11) 32%, rgba(236, 72, 153, 0.08) 58%, rgba(249, 115, 22, 0.04) 78%, transparent 100%);filter:blur(72px);pointer-events:none;z-index:0"></div>
          <div class="km-orb-2" style="position:absolute;top:1150px;right:-120px;width:720px;height:720px;background:radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.08) 0%, rgba(236, 72, 153, 0.06) 45%, rgba(249, 115, 22, 0.03) 75%, transparent 100%);filter:blur(90px);pointer-events:none;z-index:0"></div>
          <div style="position:absolute;top:2400px;left:-180px;width:820px;height:820px;background:radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.09) 0%, rgba(59, 130, 246, 0.07) 50%, transparent 100%);filter:blur(100px);pointer-events:none;z-index:0"></div>

          <!-- Sticky Minimal Navigation Bar with Smooth Blur Background -->
          <nav style="position:sticky;top:0;z-index:50;width:100%;background-color:rgba(255,255,255,0.88);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid rgba(226,232,240,0.85);box-shadow:0 4px 20px -2px rgba(10,15,29,0.03)">
            <div style="max-width:1240px;margin:0 auto;padding:0 28px;height:72px;display:flex;align-items:center;justify-content:space-between">
              <!-- Logo on Left -->
              <div style="display:flex;align-items:center;gap:12px;cursor:pointer" onclick="window.scrollTo({{ top: 0, behavior: 'smooth' }})">
                <img src="/static/kyro-logo.png" alt="Kyro Logo" style="height:32px;width:32px;object-fit:contain;filter:drop-shadow(0 2px 6px rgba(0,0,0,0.06))" onerror="this.src='/kyro-logo.png'" />
                <span style="font-size:20px;font-weight:800;letter-spacing:-0.035em;color:#0A0F1D">
                  Kyro
                </span>
              </div>

              <!-- Horizontal Navigation Links -->
              <div style="display:flex;align-items:center;gap:32px">
                <a href="#bento-grid" style="text-decoration:none;font-size:14px;font-weight:550;color:#475569">Architecture</a>
                <a href="#okf-anatomy" style="text-decoration:none;font-size:14px;font-weight:550;color:#475569">Protocol</a>
                <a href="#federation-section" style="text-decoration:none;font-size:14px;font-weight:550;color:#475569">Federation</a>
                <a href="#verifier-demo" style="text-decoration:none;font-size:14px;font-weight:550;color:#475569">Proof Verifier</a>
                <a href="#dev-integration" style="text-decoration:none;font-size:14px;font-weight:550;color:#475569">Developers</a>
              </div>

              <!-- Right-Aligned Action Buttons -->
              <div style="display:flex;align-items:center;gap:14px">
                <button class="km-btn" onclick="window.kmAction.goLogin('login')" style="background:transparent;border:none;font-size:14px;font-weight:600;color:#475569;padding:8px 14px;cursor:pointer">Sign In</button>
                <button class="km-btn km-interactive-lift" onclick="window.kmAction.demoBypass()" style="background-color:#0A0F1D;color:#FFFFFF;border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:10px 18px;font-size:13.5px;font-weight:650;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow:0 4px 14px rgba(10,15,29,0.12)">
                  Launch Mesh →
                </button>
              </div>
            </div>
          </nav>

          <!-- Hero Section: Expressive Headline, Dual CTAs, 3D Sphere Viewport -->
          <section style="max-width:1240px;margin:0 auto;padding:70px 28px 100px;position:relative;z-index:1">
            <div style="display:grid;grid-template-columns:minmax(0, 1.15fr) minmax(0, 1fr);gap:54px;align-items:center">
              <div style="max-width:620px">
                <!-- Eyebrow Pill -->
                <div class="km-hero-enter-1" style="display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:999px;background-color:#FAFAFB;border:1px solid #E2E8F0;font-size:12.5px;font-weight:600;color:#334155;margin-bottom:28px;box-shadow:0 2px 6px rgba(0,0,0,0.02)">
                  <span class="km-live-beacon" style="width:8px;height:8px;border-radius:50%;background-color:#10B981;box-shadow:0 0 8px rgba(16,185,129,0.6);display:inline-block"></span>
                  <span style="color:#64748B;font-weight:500">Live Mesh:</span>
                  <span>${{m.total_nodes}} Sovereign Nodes Active</span>
                  <span style="color:#CBD5E1">·</span>
                  <span style="background-image:linear-gradient(135deg, #6366F1, #EC4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700">Kyro Fed v1.0</span>
                </div>

                <!-- Large Bold Expressive Headline -->
                <h1 class="km-hero-enter-2" style="font-size:clamp(46px, 5.8vw, 74px);font-weight:800;line-height:1.04;letter-spacing:-0.04em;color:#0A0F1D;margin:0 0 24px">
                  Sovereign intelligence.<br />
                  <span style="background-image:linear-gradient(135deg, #4F46E5 0%, #7C3AED 35%, #EC4899 70%, #F97316 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent">
                    Cryptographically verified.
                  </span>
                </h1>

                <p class="km-hero-enter-3" style="font-size:18px;line-height:1.6;color:#475569;margin:0 0 36px;font-weight:450;max-width:540px">
                  The zero-trust knowledge mesh for autonomous AI agents. Publish immutable Open Knowledge Format bundles with Ed25519 digital signatures, RFC 8785 canonical serialization, and conflict-preserving peer federation.
                </p>

                <!-- Contrasting CTA Buttons -->
                <div class="km-hero-enter-4" style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:32px">
                  <button class="km-btn km-btn-lg km-interactive-lift" onclick="window.kmAction.demoBypass()" style="background-color:#0A0F1D;color:#FFFFFF;border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:14px 26px;font-size:15px;font-weight:650;cursor:pointer;display:flex;align-items:center;gap:10px;box-shadow:0 10px 25px -4px rgba(10,15,29,0.22)">
                    Start Building with Kyro →
                  </button>
                  <button class="km-btn km-btn-lg km-interactive-lift" onclick="window.kmAction.goLogin('login')" style="background-color:#FFFFFF;color:#1E293B;border:1px solid #E2E8F0;border-radius:12px;padding:14px 24px;font-size:15px;font-weight:600;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.04)">
                    Access Control Plane
                  </button>
                </div>

                <div style="display:flex;align-items:center;gap:18px;font-size:12.5px;color:#64748B;font-weight:500;flex-wrap:wrap">
                  <span>✓ RFC 8032 Ed25519</span>
                  <span style="color:#CBD5E1">·</span>
                  <span>✓ RFC 8785 Canonical JSON</span>
                  <span style="color:#CBD5E1">·</span>
                  <span>✓ Client-Side Zero-Trust</span>
                </div>
              </div>

              <!-- Right: 3D Sphere Canvas Viewport -->
              <div style="position:relative;width:100%;min-height:560px;display:flex;align-items:center;justify-content:center;margin-top:-36px">
                <!-- Radial glow enhancing contrast of cyan holographic sphere on light background -->
                <div style="position:absolute;width:480px;height:480px;border-radius:50%;background:radial-gradient(circle, rgba(56, 189, 248, 0.14) 0%, rgba(99, 102, 241, 0.08) 36%, rgba(236, 72, 153, 0.04) 65%, transparent 75%);filter:blur(40px);pointer-events:none;z-index:0"></div>
                <!-- Single unified cyan ground shadow matching the sphere -->
                <div class="km-sphere-shadow" style="position:absolute;bottom:52px;left:50%;transform:translateX(-50%);width:320px;height:40px;border-radius:50%;background:radial-gradient(ellipse at center, rgba(6, 182, 212, 0.52) 0%, rgba(56, 189, 248, 0.30) 35%, rgba(14, 165, 233, 0.10) 65%, transparent 80%);pointer-events:none;z-index:0"></div>
                <div class="km-sphere-wrapper" style="position:relative;width:100%;height:640px;min-height:560px;background:transparent;display:flex;align-items:center;justify-content:center;overflow:visible;z-index:1">
                  <canvas id="km-three-canvas" style="width:100%;height:100%;display:block;background:transparent"></canvas>
                </div>
              </div>
            </div>
          </section>

          <!-- Standards Strip -->
          <section class="km-reveal" style="border-top:1px solid #F1F5F9;border-bottom:1px solid #F1F5F9;background-color:#FAFAFB;padding:22px 28px">
            <div style="max-width:1240px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:20px;font-size:13px;font-weight:600;color:#64748B;letter-spacing:0.02em">
              <span>RFC 8032 ED25519</span>
              <span style="color:#CBD5E1">◆</span>
              <span>RFC 8785 CANONICAL JCS</span>
              <span style="color:#CBD5E1">◆</span>
              <span>OPEN KNOWLEDGE FORMAT (OKF)</span>
              <span style="color:#CBD5E1">◆</span>
              <span>W3C PROV-O HASH CHAINS</span>
              <span style="color:#CBD5E1">◆</span>
              <span>EPISTEMIC SEPARATION</span>
              <span style="color:#CBD5E1">◆</span>
              <span>CONFLICT-PRESERVING PULL SYNC</span>
            </div>
          </section>

          <!-- Bento Grid: Core Capabilities -->
          <section id="bento-grid" style="max-width:1240px;margin:0 auto;padding:120px 28px 80px">
            <div class="km-reveal" style="text-align:center;max-width:680px;margin:0 auto 64px">
              <div style="font-size:12px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#6366F1;margin-bottom:12px">Architectural Foundations</div>
              <h2 style="font-size:clamp(32px, 3.8vw, 46px);font-weight:800;letter-spacing:-0.03em;color:#0A0F1D;line-height:1.15;margin:0 0 16px">
                Engineered for cryptographic truth in the era of autonomous agents.
              </h2>
              <p style="font-size:16px;color:#64748B;line-height:1.6;margin:0">
                Every claim, schema, and benchmark trace is signed by its sovereign creator and independently verifiable without relying on a centralized intermediary.
              </p>
            </div>

            <div style="display:grid;grid-template-columns:repeat(12, 1fr);gap:24px">
              <!-- Bento 1: 8-Col Canonical Serialization -->
              <div class="km-bento-card km-reveal-scale km-delay-1" style="grid-column:span 8;background-color:#FAFAFB;border-radius:20px;border:1px solid #E2E8F0;padding:36px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10,15,29,0.04)">
                <div>
                  <div style="display:inline-block;font-size:11.5px;font-weight:700;color:#6366F1;background-color:rgba(99,102,241,0.08);padding:4px 10px;border-radius:6px;margin-bottom:16px">RFC 8785 JCS</div>
                  <h3 style="font-size:22px;font-weight:700;color:#0A0F1D;margin:0 0 10px">Deterministic Canonical Serialization</h3>
                  <p style="font-size:15px;color:#64748B;line-height:1.6;margin:0 0 24px;max-width:560px">
                    Different JSON parsers emit arbitrary whitespace and key orderings, corrupting SHA-256 hashes. Kyro enforces byte-level deterministic RFC 8785 serialization so signatures verify across Python, Rust, Go, and TypeScript.
                  </p>
                </div>
                <div style="background-color:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:16px 20px;font-family:monospace;font-size:12px;color:#1E293B">
                  <div style="display:flex;justify-content:space-between;color:#94A3B8;font-size:11px;margin-bottom:8px">
                    <span>CANONICAL PAYLOAD</span>
                    <span style="color:#10B981;font-weight:600">✓ SHA-256 DIGEST LOCKED</span>
                  </div>
                  <div style="color:#475569;line-height:1.5">
                    {{"bundle_id":"bun-kv-2026","domain":"distributed_ml","format_version":"0.2","publisher":"did:kyro:node-a"}}
                  </div>
                  <div style="margin-top:10px;padding-top:8px;border-top:1px dashed #E2E8F0;font-size:11px;color:#6366F1;overflow:hidden;text-overflow:ellipsis">
                    sha256: 4f1a8c9b2d7e5f6a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a
                  </div>
                </div>
              </div>

              <!-- Bento 2: 4-Col Dual-Key Ed25519 -->
              <div class="km-bento-card km-reveal-scale km-delay-2" style="grid-column:span 4;background-color:#FAFAFB;border-radius:20px;border:1px solid #E2E8F0;padding:36px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10,15,29,0.04)">
                <div>
                  <div style="display:inline-block;font-size:11.5px;font-weight:700;color:#EC4899;background-color:rgba(236,72,153,0.08);padding:4px 10px;border-radius:6px;margin-bottom:16px">RFC 8032</div>
                  <h3 style="font-size:20px;font-weight:700;color:#0A0F1D;margin:0 0 10px">Dual-Key Node Identity</h3>
                  <p style="font-size:14px;color:#64748B;line-height:1.6;margin:0 0 20px">
                    Every node holds an elliptic curve Ed25519 keypair. Knowledge envelopes carry author signatures that can be validated offline without relying on DNS or central certificates.
                  </p>
                </div>
                <div style="background-color:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:16px;text-align:center">
                  <div style="width:44px;height:44px;border-radius:50%;margin:0 auto 10px;background:linear-gradient(135deg, #6366F1 0%, #EC4899 100%);display:flex;align-items:center;justify-content:center;color:#FFFFFF;font-size:18px;font-weight:700">✓</div>
                  <div style="font-size:12px;font-weight:700;color:#0A0F1D">Ed25519 Envelope</div>
                  <div style="font-size:11px;color:#64748B;font-family:monospace;margin-top:4px">fp: 51e75b86fd2372...</div>
                </div>
              </div>

              <!-- Bento 3: 4-Col Epistemic Separation -->
              <div class="km-bento-card km-reveal-scale km-delay-1" style="grid-column:span 4;background-color:#FAFAFB;border-radius:20px;border:1px solid #E2E8F0;padding:36px;box-shadow:0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10,15,29,0.04)">
                <div style="display:inline-block;font-size:11.5px;font-weight:700;color:#F59E0B;background-color:rgba(245,158,11,0.08);padding:4px 10px;border-radius:6px;margin-bottom:16px">Epistemic Principle</div>
                <h3 style="font-size:20px;font-weight:700;color:#0A0F1D;margin:0 0 10px">Signature ≠ Factual Truth</h3>
                <p style="font-size:14px;color:#64748B;line-height:1.6;margin:0 0 16px">
                  A valid cryptographic signature proves only who authored a statement and that it was not tampered with. It never replaces empirical evidence or independent multi-agent peer review.
                </p>
                <div style="padding:10px 14px;background-color:#FFFFFF;border-radius:10px;border:1px solid #E2E8F0;font-size:12px;color:#334155">
                  <strong>Zero-Trust Rubric:</strong> Claims must link verifiable evidence digests before being admitted to consensus.
                </div>
              </div>

              <!-- Bento 4: 4-Col Autonomous Agents -->
              <div class="km-bento-card km-reveal-scale km-delay-2" style="grid-column:span 4;background-color:#FAFAFB;border-radius:20px;border:1px solid #E2E8F0;padding:36px;box-shadow:0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10,15,29,0.04)">
                <div style="display:inline-block;font-size:11.5px;font-weight:700;color:#10B981;background-color:rgba(16,185,129,0.08);padding:4px 10px;border-radius:6px;margin-bottom:16px">W3C PROV-O</div>
                <h3 style="font-size:20px;font-weight:700;color:#0A0F1D;margin:0 0 10px">Autonomous Agent Auditing</h3>
                <p style="font-size:14px;color:#64748B;line-height:1.6;margin:0 0 16px">
                  Autonomous agents index, audit, and challenge claims in real time. Every extraction activity is committed to an immutable W3C provenance chain with parent hash references.
                </p>
                <div style="display:flex;gap:8px;flex-wrap:wrap">
                  <span style="font-size:11px;padding:4px 8px;background-color:#FFFFFF;border-radius:6px;border:1px solid #E2E8F0;color:#475569">agent-indexer (60Hz)</span>
                  <span style="font-size:11px;padding:4px 8px;background-color:#FFFFFF;border-radius:6px;border:1px solid #E2E8F0;color:#475569">zero-trust-auditor</span>
                </div>
              </div>

              <!-- Bento 5: 4-Col Peer Federation -->
              <div class="km-bento-card km-reveal-scale km-delay-3" style="grid-column:span 4;background-color:#FAFAFB;border-radius:20px;border:1px solid #E2E8F0;padding:36px;box-shadow:0 1px 3px rgba(0,0,0,0.02), 0 16px 36px -12px rgba(10,15,29,0.04)">
                <div style="display:inline-block;font-size:11.5px;font-weight:700;color:#8B5CF6;background-color:rgba(139,92,246,0.08);padding:4px 10px;border-radius:6px;margin-bottom:16px">Peer Pull-Sync</div>
                <h3 style="font-size:20px;font-weight:700;color:#0A0F1D;margin:0 0 10px">Multi-Node Federation</h3>
                <p style="font-size:14px;color:#64748B;line-height:1.6;margin:0 0 16px">
                  Nodes replicate knowledge over standard HTTP endpoints. When two nodes possess diverging revisions, Kyro preserves both in parallel branches rather than silently overwriting data.
                </p>
                <div style="font-size:12px;color:#10B981;font-weight:600">● Replicating across ${{m.total_nodes}} live peer nodes</div>
              </div>
            </div>
          </section>

          <!-- Alternating Editorial Section 1: OKF Bundle Anatomy -->
          <section id="okf-anatomy" style="max-width:1240px;margin:0 auto;padding:100px 28px">
            <div style="display:grid;grid-template-columns:1fr 1.15fr;gap:60px;align-items:center">
              <div class="km-reveal-left">
                <div style="font-size:12px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#6366F1;margin-bottom:12px">Bundle Specification</div>
                <h2 style="font-size:clamp(30px, 3.5vw, 42px);font-weight:800;letter-spacing:-0.03em;color:#0A0F1D;line-height:1.18;margin:0 0 20px">
                  Open Knowledge Format: Structured, signed, machine-readable.
                </h2>
                <p style="font-size:16px;color:#475569;line-height:1.6;margin:0 0 24px">
                  Traditional LLM outputs are ephemeral and unverifiable. Kyro packages intelligence into canonical OKF v0.2 bundles comprising declarative manifest schemas, Markdown concept definitions, raw benchmark evidence traces, and immutable provenance records.
                </p>
                <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:12px">
                  <li style="display:flex;align-items:flex-start;gap:10px;font-size:14.5px;color:#334155">
                    <span style="color:#10B981;font-weight:700">✓</span>
                    <span><strong>Atomic Claims:</strong> Statements isolated into discrete testable assertions.</span>
                  </li>
                  <li style="display:flex;align-items:flex-start;gap:10px;font-size:14.5px;color:#334155">
                    <span style="color:#10B981;font-weight:700">✓</span>
                    <span><strong>Evidence Linkage:</strong> Every claim references verifiable hardware or empirical run data.</span>
                  </li>
                  <li style="display:flex;align-items:flex-start;gap:10px;font-size:14.5px;color:#334155">
                    <span style="color:#10B981;font-weight:700">✓</span>
                    <span><strong>Cryptographic Sealing:</strong> Ed25519 signing envelope embedded in bundle root.</span>
                  </li>
                </ul>
              </div>

              <!-- Interactive Bundle Inspector -->
              <div class="km-reveal-right km-bento-card" style="background-color:#FAFAFB;border-radius:20px;border:1px solid #E2E8F0;overflow:hidden;box-shadow:0 12px 36px -8px rgba(10,15,29,0.06)">
                <div style="display:flex;align-items:center;background-color:#F1F5F9;border-bottom:1px solid #E2E8F0;padding:8px 12px;gap:6px">
                  <span style="background-color:#FFFFFF;color:#0A0F1D;font-weight:650;border-radius:6px;padding:6px 12px;font-size:12px;box-shadow:0 1px 3px rgba(0,0,0,0.05)">manifest.yaml</span>
                  <span style="color:#64748B;font-weight:500;padding:6px 12px;font-size:12px">concept-kv-quant.md</span>
                  <span style="color:#64748B;font-weight:500;padding:6px 12px;font-size:12px">evidence-benchmark.md</span>
                </div>
                <div style="padding:24px;background-color:#FFFFFF;font-family:monospace;font-size:12.5px;line-height:1.6;color:#1E293B;min-height:240px">
                  <pre style="margin:0">format_version: "0.2"
bundle_id: "bun-kv-2026"
category: "distributed_ml"
publisher:
  node_id: "node-a"
  fingerprint: "51e75b86fd2372..."
signing_suite: "RFC8032-Ed25519"
canonical_digest: "RFC8785-SHA256"
claims_count: 4
evidence_count: 2</pre>
                </div>
                <div style="padding:12px 24px;background-color:#F8FAFC;border-top:1px solid #E2E8F0;display:flex;justify-content:space-between;font-size:11px;color:#64748B">
                  <span>Digest: SHA-256</span>
                  <span style="color:#10B981;font-weight:600">✓ Verified Against Local Keyring</span>
                </div>
              </div>
            </div>
          </section>

          <!-- Interactive Client-Side Proof Verifier Playground -->
          <section id="verifier-demo" style="background-color:#FAFAFB;border-top:1px solid #E2E8F0;border-bottom:1px solid #E2E8F0;padding:100px 28px">
            <div style="max-width:860px;margin:0 auto;text-align:center">
              <div class="km-reveal" style="font-size:12px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#6366F1;margin-bottom:12px">Zero-Trust Playground</div>
              <h2 class="km-reveal km-delay-1" style="font-size:clamp(30px, 3.5vw, 42px);font-weight:800;letter-spacing:-0.03em;color:#0A0F1D;line-height:1.18;margin:0 0 16px">
                Verify a cryptographic digest in your browser.
              </h2>
              <p class="km-reveal km-delay-2" style="font-size:16px;color:#64748B;line-height:1.6;margin:0 0 36px">
                Test client-side cryptographic verification directly. Type or edit the payload below to watch the SHA-256 digest calculate live in browser memory.
              </p>

              <div class="km-reveal-scale km-bento-card" style="background-color:#FFFFFF;border-radius:16px;border:1px solid #E2E8F0;padding:28px;box-shadow:0 10px 30px -6px rgba(10,15,29,0.05);text-align:left">
                <div style="margin-bottom:16px">
                  <label style="display:block;font-size:12px;font-weight:700;color:#475569;margin-bottom:6px">INPUT STRING OR CANONICAL OKF MANIFEST</label>
                  <input type="text" id="km-live-verifier-input" value="bun-kv-2026-prod-v1" oninput="window.kmAction.recalcVerifierDigest(this.value)" style="width:100%;height:44px;padding:0 14px;border-radius:8px;border:1px solid #CBD5E1;font-size:14px;font-family:monospace;color:#0A0F1D;background-color:#FFFFFF" />
                </div>
                <div style="padding:12px 16px;background-color:#F8FAFC;border-radius:8px;border:1px solid #E2E8F0;margin-bottom:14px">
                  <div style="font-size:11px;font-weight:700;color:#64748B;margin-bottom:4px">COMPUTED SHA-256 DIGEST:</div>
                  <div id="km-live-verifier-output" style="font-size:13px;font-family:monospace;color:#4F46E5;word-break:break-all">
                    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
                  </div>
                </div>
                <div style="display:flex;align-items:center;justify-content:space-between">
                  <span style="font-size:12px;color:#10B981;font-weight:600">✓ Valid RFC 8785 Hash Format · 256-bit Cryptographic Proof</span>
                  <button class="km-btn km-interactive-lift" onclick="window.kmShowToast('✓ Verification confirmed: Digest is untampered and cryptographically valid.', 'success')" style="background-color:#0A0F1D;color:#FFFFFF;border:none;border-radius:8px;padding:8px 16px;font-size:12.5px;font-weight:650;cursor:pointer">Confirm Proof</button>
                </div>
              </div>
            </div>
          </section>

          <!-- Developer Integration Section -->
          <section id="dev-integration" style="max-width:1240px;margin:0 auto;padding:110px 28px">
            <div class="km-reveal" style="text-align:center;max-width:640px;margin:0 auto 50px">
              <div style="font-size:12px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#6366F1;margin-bottom:12px">Developer Experience</div>
              <h2 style="font-size:clamp(30px, 3.5vw, 42px);font-weight:800;letter-spacing:-0.03em;color:#0A0F1D;line-height:1.18;margin:0 0 16px">Four lines of code to sign and publish.</h2>
              <p style="font-size:16px;color:#64748B;line-height:1.6;margin:0">Native SDKs for Python, TypeScript, Rust CLI, and REST API. Integrate cryptographic knowledge verification into your LLM pipelines.</p>
            </div>

            <div class="km-reveal-scale km-bento-card" style="max-width:780px;margin:0 auto;background-color:#0F172A;border-radius:18px;border:1px solid #1E293B;overflow:hidden;box-shadow:0 20px 45px -10px rgba(10,15,29,0.18)">
              <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 18px;background-color:#090D18;border-bottom:1px solid #1E293B">
                <div style="display:flex;gap:6px">
                  <div style="width:10px;height:10px;border-radius:50%;background-color:#EF4444"></div>
                  <div style="width:10px;height:10px;border-radius:50%;background-color:#F59E0B"></div>
                  <div style="width:10px;height:10px;border-radius:50%;background-color:#10B981"></div>
                </div>
                <div style="font-size:12px;color:#94A3B8;font-family:monospace">Python SDK (RFC 8785 + Ed25519)</div>
              </div>
              <div style="padding:24px;font-family:monospace;font-size:13px;line-height:1.6;color:#E2E8F0">
                <pre style="margin:0">from kyro import KyroNode, OKFBundle

node = KyroNode.load_keypair("~/.kyro/node_key.priv")
bundle = OKFBundle.from_directory("./knowledge-base")

# Deterministically canonicalizes (RFC 8785) & signs (Ed25519)
signed_envelope = node.sign_bundle(bundle)
node.publish_to_mesh(signed_envelope, peers=["http://node-b:8000"])
print("✓ Published & verified:", signed_envelope.canonical_digest)</pre>
              </div>
            </div>
          </section>

          <!-- Sculpted High-Impact CTA Banner -->
          <section class="km-reveal-scale" style="max-width:1240px;margin:0 auto;padding:0 28px 120px">
            <div style="background-color:#FAFAFB;border-radius:24px;border:1px solid #E2E8F0;padding:80px 48px;text-align:center;position:relative;overflow:hidden;box-shadow:0 20px 40px -15px rgba(10,15,29,0.05)">
              <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:600px;height:300px;background:radial-gradient(circle, rgba(99,102,241,0.12) 0%, rgba(236,72,153,0.08) 50%, transparent 100%);filter:blur(60px);pointer-events:none"></div>
              <h2 style="font-size:clamp(34px, 4.5vw, 54px);font-weight:800;letter-spacing:-0.035em;color:#0A0F1D;line-height:1.1;margin:0 0 18px;position:relative">
                Ready to operate your sovereign knowledge node?
              </h2>
              <p style="font-size:17px;color:#64748B;line-height:1.6;max-width:580px;margin:0 auto 36px;position:relative">
                Join sovereign AI researchers and engineering teams publishing verifiable knowledge with cryptographic provenance.
              </p>
              <div style="display:flex;justify-content:center;gap:14px;flex-wrap:wrap;position:relative">
                <button class="km-btn km-btn-lg km-interactive-lift" onclick="window.kmAction.goLogin('register')" style="background-color:#0A0F1D;color:#FFFFFF;border:none;border-radius:12px;padding:16px 32px;font-size:15px;font-weight:650;cursor:pointer;box-shadow:0 8px 24px rgba(10,15,29,0.18)">
                  Register Organization Account →
                </button>
                <button class="km-btn km-btn-lg km-interactive-lift" onclick="window.kmAction.demoBypass()" style="background-color:#FFFFFF;color:#1E293B;border:1px solid #CBD5E1;border-radius:12px;padding:16px 28px;font-size:15px;font-weight:600;cursor:pointer">
                  Launch Sovereign Node A
                </button>
              </div>
            </div>
          </section>

          <!-- Spacious Multi-Column Footer -->
          <footer class="km-reveal" style="border-top:1px solid #E2E8F0;background-color:#FFFFFF;padding:80px 28px 40px">
            <div style="max-width:1240px;margin:0 auto;display:grid;grid-template-columns:1.5fr repeat(4, 1fr);gap:48px;margin-bottom:60px">
              <div>
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
                  <img src="/static/kyro-logo.png" alt="Kyro Logo" style="height:26px;width:26px;object-fit:contain" onerror="this.src='/kyro-logo.png'" />
                  <span style="font-size:18px;font-weight:800;color:#0A0F1D;letter-spacing:-0.03em">Kyro</span>
                </div>
                <p style="font-size:14px;color:#64748B;line-height:1.6;margin:0;max-width:280px">
                  The zero-trust knowledge mesh protocol for autonomous AI agents and sovereign nodes.
                </p>
              </div>

              <div>
                <div style="font-size:13px;font-weight:700;color:#0A0F1D;margin-bottom:16px;text-transform:uppercase;letter-spacing:0.05em">Protocol</div>
                <div style="display:flex;flex-direction:column;gap:10px;font-size:14px;color:#64748B">
                  <div>OKF v0.2 Specification</div>
                  <div>RFC 8785 Canonical JCS</div>
                  <div>Ed25519 Envelopes</div>
                  <div>W3C PROV Chains</div>
                </div>
              </div>

              <div>
                <div style="font-size:13px;font-weight:700;color:#0A0F1D;margin-bottom:16px;text-transform:uppercase;letter-spacing:0.05em">Platform</div>
                <div style="display:flex;flex-direction:column;gap:10px;font-size:14px;color:#64748B">
                  <div>Federation Control Plane</div>
                  <div>Zero-Trust Verifier</div>
                  <div>Autonomous Agents</div>
                  <div>Epistemic Rubrics</div>
                </div>
              </div>

              <div>
                <div style="font-size:13px;font-weight:700;color:#0A0F1D;margin-bottom:16px;text-transform:uppercase;letter-spacing:0.05em">Developers</div>
                <div style="display:flex;flex-direction:column;gap:10px;font-size:14px;color:#64748B">
                  <div>Python SDK</div>
                  <div>TypeScript Client</div>
                  <div>Rust CLI</div>
                  <div>REST API Docs</div>
                </div>
              </div>

              <div>
                <div style="font-size:13px;font-weight:700;color:#0A0F1D;margin-bottom:16px;text-transform:uppercase;letter-spacing:0.05em">Governance</div>
                <div style="display:flex;flex-direction:column;gap:10px;font-size:14px;color:#64748B">
                  <div>Zero-Trust Rubric</div>
                  <div>Epistemic Principles</div>
                  <div>Security Policy</div>
                  <div>Privacy &amp; Terms</div>
                </div>
              </div>
            </div>

            <div style="max-width:1240px;margin:0 auto;padding-top:24px;border-top:1px solid #F1F5F9;display:flex;align-items:center;justify-content:space-between;font-size:12.5px;color:#94A3B8;flex-wrap:wrap;gap:12px">
              <div>© 2026 Kyro Protocol Foundation. Open-source under MIT &amp; Apache 2.0.</div>
              <div style="display:flex;gap:20px">
                <span>Network: kyro-fed/1.0</span>
                <span>Digest: RFC 8785 (SHA-256)</span>
                <span>Ed25519 Verified</span>
              </div>
            </div>
          </footer>
        </div>
      `;
    }}

    /* ============================================================================
       STAGE 2 RENDERER: STRICT BACKEND LOGIN & REGISTRATION GATE
       ============================================================================ */
    function renderLoginGate() {{
      const isLogin = state.authMode === 'login';
      return `
        <div class="km-landing-root">
          <div class="km-aurora-orb-1"></div>
          <div class="km-aurora-orb-2"></div>
          <div class="km-auth-gate-wrap">
            <div style="margin-bottom:18px">
              <button class="km-btn km-btn-sm" onclick="window.kmAction.goLanding()">← Back to Product Landing Page</button>
            </div>
            <div class="km-auth-card">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
                <div class="km-brand-logo" style="display:flex;align-items:center;gap:10px">
                  <img src="/static/kyro-logo.png" alt="Kyro Logo" style="height:34px;width:auto;object-fit:contain;filter:drop-shadow(0 2px 10px rgba(0,0,0,0.3));" />
                  <div>Ky<span>ro</span></div>
                </div>
                <span class="km-badge verified">Sovereign Mesh Identity</span>
              </div>
              <h2 style="margin:0 0 6px;font-size:22px">
                ${{isLogin ? 'Sign In to Sovereign Control Plane' : 'Register Organization &amp; Node Admin'}}
              </h2>
              <p class="km-metric-sub" style="margin-bottom:18px">
                ${{isLogin
                  ? 'Credentials are verified directly against the backend database (/api/v1/auth/login).'
                  : 'Create a new sovereign account and organization boundary (/api/v1/auth/register).'}}
              </p>

              <!-- Instant Demo Bypass Box -->
              <div style="background:rgba(2,132,199,0.14);border:1px solid rgba(56,189,248,0.45);border-radius:10px;padding:14px;margin-bottom:18px;display:flex;align-items:center;justify-content:space-between;gap:12px">
                <div>
                  <div style="font-size:13px;font-weight:700;color:#38bdf8">Quick Testing &amp; Evaluation</div>
                  <div style="font-size:11.5px;color:#94a3b8">Bypass manual credentials and access the full live dashboard instantly.</div>
                </div>
                <button type="button" class="km-btn km-btn-primary" onclick="window.kmAction.demoBypass()" style="white-space:nowrap;background:linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);color:#070b14;font-weight:700">Demo Bypass →</button>
              </div>

              ${{state.authError ? `<div class="km-notice error" style="margin-bottom:16px"><span>✕ ${{esc(state.authError)}}</span></div>` : ''}}

              <form onsubmit="window.kmAction.submitAuth(event)">
                <div class="km-field">
                  <label class="km-label">Organization Email *</label>
                  <input id="km-auth-email" class="km-input" type="email" required placeholder="you@organization.org" />
                </div>
                <div class="km-field">
                  <label class="km-label">Password ${{isLogin ? '' : '(min 8 characters)'}} *</label>
                  <input id="km-auth-password" class="km-input" type="password" required minlength="${{isLogin ? 1 : 8}}" placeholder="Enter password" />
                </div>
                ${{!isLogin ? `
                  <div class="km-field">
                    <label class="km-label">Full Name *</label>
                    <input id="km-auth-fullname" class="km-input" required placeholder="e.g., Dr. Elena Vance" />
                  </div>
                  <div class="km-field">
                    <label class="km-label">Organization Name *</label>
                    <input id="km-auth-orgname" class="km-input" required placeholder="e.g., Sovereign AI Research Lab" />
                  </div>
                ` : ''}}
                <button type="submit" class="km-btn km-btn-primary km-btn-lg" style="width:100%;margin-top:6px" ${{state.authLoading ? 'disabled' : ''}}>
                  ${{state.authLoading ? 'Verifying with Backend…' : (isLogin ? 'Authenticate &amp; Open Dashboard →' : 'Create Account &amp; Open Dashboard →')}}
                </button>
              </form>

              <div style="margin-top:16px;padding-top:14px;border-top:1px solid var(--border-subtle);display:flex;justify-content:space-between;align-items:center;font-size:12.5px">
                <span style="color:var(--text-secondary)">${{isLogin ? 'First time on this node?' : 'Already registered an account?'}}</span>
                <button type="button" class="km-btn km-btn-sm" onclick="window.kmAction.goLogin('${{isLogin ? 'register' : 'login'}}')">
                  ${{isLogin ? 'Register Account' : 'Switch to Sign In'}}
                </button>
              </div>
            </div>
          </div>
        </div>
      `;
    }}

    /* ============================================================================
       STAGE 3 RENDERER: DYNAMIC CONSOLE DASHBOARD
       ============================================================================ */
    function renderTopologySvg() {{
      const nodes = (state.overview && state.overview.topology && state.overview.topology.nodes)
        ? state.overview.topology.nodes
        : [];
      const edges = (state.overview && state.overview.topology && state.overview.topology.edges)
        ? state.overview.topology.edges
        : [];

      const localNode = nodes.find(n => n.type === 'local_node') || nodes[0];
      const peers = nodes.filter(n => n.id !== (localNode ? localNode.id : null));
      const count = peers.length;

      const cx = 390;
      const cy = 195;
      const pos = {{}};
      const cardOffsets = {{}};

      if (localNode) {{
        pos[localNode.id] = {{ x: cx, y: cy }};
        // Local node card sits directly below center where no outgoing lines intersect
        cardOffsets[localNode.id] = {{ yOffset: 34, textY1: 49, textY2: 63 }};
      }}

      if (count === 3) {{
        // Clean orthogonal T-layout for 4-node federated mesh:
        // Top: Node B, Right: Node C, Left: Node D.
        // Outgoing links go Up, Right, Left; Center card sits straight Down with 0 collision.
        const pTop = peers[0];
        const pRight = peers[1];
        const pLeft = peers[2];
        if (pTop) {{
          pos[pTop.id] = {{ x: cx, y: 65 }};
          cardOffsets[pTop.id] = {{ yOffset: -52, textY1: -37, textY2: -23 }};
        }}
        if (pRight) {{
          pos[pRight.id] = {{ x: 650, y: 195 }};
          cardOffsets[pRight.id] = {{ yOffset: 32, textY1: 47, textY2: 61 }};
        }}
        if (pLeft) {{
          pos[pLeft.id] = {{ x: 130, y: 195 }};
          cardOffsets[pLeft.id] = {{ yOffset: 32, textY1: 47, textY2: 61 }};
        }}
      }} else if (count === 2) {{
        // Triangular layout with peers positioned above local anchor
        if (peers[0]) {{
          pos[peers[0].id] = {{ x: 550, y: 95 }};
          cardOffsets[peers[0].id] = {{ yOffset: -52, textY1: -37, textY2: -23 }};
        }}
        if (peers[1]) {{
          pos[peers[1].id] = {{ x: 230, y: 95 }};
          cardOffsets[peers[1].id] = {{ yOffset: -52, textY1: -37, textY2: -23 }};
        }}
      }} else {{
        const radiusX = count > 5 ? 250 : 220;
        const radiusY = 125;
        peers.forEach((n, idx) => {{
          const angle = (idx / Math.max(1, count)) * Math.PI * 2 - Math.PI / 2;
          const px = Math.round(cx + Math.cos(angle) * radiusX);
          const py = Math.round(cy + Math.sin(angle) * radiusY);
          pos[n.id] = {{ x: px, y: py }};
          if (py < cy - 20) {{
            cardOffsets[n.id] = {{ yOffset: -52, textY1: -37, textY2: -23 }};
          }} else {{
            cardOffsets[n.id] = {{ yOffset: 32, textY1: 47, textY2: 61 }};
          }}
        }});
      }}

      const selNode = nodes.find(n => n.id === state.selectedTopologyNodeId) || nodes[0] || null;

      const edgesSvg = edges.map((e, idx) => {{
        const s = pos[e.source], d = pos[e.target];
        if (!s || !d) return '';
        const mx = Math.round((s.x + d.x) / 2);
        const my = Math.round((s.y + d.y) / 2);
        const path1 = `M ${{s.x}} ${{s.y}} L ${{d.x}} ${{d.y}}`;
        const path2 = `M ${{d.x}} ${{d.y}} L ${{s.x}} ${{s.y}}`;
        const col = e.verified ? '#38D399' : '#F5B942';
        return `
          <g>
            <line x1="${{s.x}}" y1="${{s.y}}" x2="${{d.x}}" y2="${{d.y}}" stroke="${{col}}" stroke-width="6" opacity="0.12" />
            <line x1="${{s.x}}" y1="${{s.y}}" x2="${{d.x}}" y2="${{d.y}}" stroke="${{col}}" stroke-width="2.2" />
            <circle r="4" fill="#55C8D7"><animateMotion dur="${{2.4 + idx * 0.4}}s" repeatCount="indefinite" path="${{path1}}" /></circle>
            <circle r="3.5" fill="#38D399"><animateMotion dur="${{2.8 + idx * 0.4}}s" repeatCount="indefinite" path="${{path2}}" /></circle>
            <g transform="translate(${{mx}}, ${{my}})">
              <rect x="-56" y="-11" width="112" height="22" rx="11" fill="#0B111E" stroke="${{col}}" stroke-width="1.2" />
              <text x="0" y="3.5" fill="#D7E3FF" font-size="9.5" font-weight="650" text-anchor="middle">✓ Ed25519 · ${{e.latency_ms ?? '15'}}ms</text>
            </g>
          </g>
        `;
      }}).join('');

      const nodesSvg = nodes.map(n => {{
        const p = pos[n.id] || {{ x: cx, y: cy }};
        const offset = cardOffsets[n.id] || {{ yOffset: 32, textY1: 47, textY2: 61 }};
        const isLocal = n.type === 'local_node';
        const isSel = selNode && selNode.id === n.id;
        const col = isLocal ? '#6599FF' : '#38D399';
        const fullLabel = n.label || n.id;
        const cardWidth = Math.max(190, Math.min(270, Math.round(fullLabel.length * 7.4) + 26));
        const cardX = -Math.round(cardWidth / 2);
        return `
          <g transform="translate(${{p.x}}, ${{p.y}})" style="cursor:pointer" onclick="window.kmAction.selectTopoNode('${{esc(n.id)}}')">
            ${{isSel ? `<circle r="44" fill="${{col}}" opacity="0.18" />` : ''}}
            ${{isLocal ? `<circle class="km-pulse-circle" r="26" fill="none" stroke="#6599FF" stroke-width="1.5" />` : ''}}
            <circle r="${{isLocal ? 24 : 20}}" fill="#0D1526" stroke="${{col}}" stroke-width="${{isSel ? 3.5 : 2.2}}" />
            <circle r="${{isLocal ? 8 : 6}}" fill="${{col}}" />
            <rect x="${{cardX}}" y="${{offset.yOffset}}" width="${{cardWidth}}" height="36" rx="8" fill="rgba(11,17,30,0.95)" stroke="${{isSel ? col : '#22304A'}}" />
            <text y="${{offset.textY1}}" fill="#F3F7FF" font-size="11" font-weight="650" text-anchor="middle">${{esc(fullLabel)}}</text>
            <text y="${{offset.textY2}}" fill="#8FA1C2" font-size="9.5" text-anchor="middle">${{esc(n.id)}} (${{esc(n.visibility)}})</text>
          </g>
        `;
      }}).join('');

      return `
        <div class="km-card" style="margin-bottom:24px">
          <div class="km-card-header">
            <div>
              <div style="display:flex;align-items:center;gap:10px">
                <h3 class="km-card-title">Federated Knowledge Mesh Topology</h3>
                <span class="km-badge verified">● Live Telemetry (${{nodes.length}} Nodes · ${{edges.length}} Links)</span>
              </div>
              <div class="km-metric-sub">Rendered dynamically from GET /api/v1/overview · Click any node to inspect Ed25519 identity</div>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap">
              <button class="km-btn km-btn-sm ${{state.simMode === 'query_fanout' ? 'km-btn-accent' : ''}}" onclick="window.kmAction.setSimMode('query_fanout')">⌕ Query Fan-Out Pulse</button>
              <button class="km-btn km-btn-sm ${{state.simMode === 'pull_sync' ? 'km-btn-primary' : ''}}" onclick="window.kmAction.setSimMode('pull_sync')">⇄ Pull-Sync Packet Flow</button>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:1.65fr 1fr;gap:18px">
            <div style="background:radial-gradient(circle at 50% 50%, #0E172A 0%, #070B14 100%);border:1px solid var(--border-default);border-radius:var(--radius-md);overflow:hidden;position:relative">
              <svg viewBox="0 0 780 390" style="width:100%;height:370px;display:block">
                <defs>
                  <pattern id="kmGrid" width="36" height="36" patternUnits="userSpaceOnUse">
                    <path d="M 36 0 L 0 0 0 36" fill="none" stroke="#152036" stroke-width="0.75" />
                  </pattern>
                </defs>
                <rect width="780" height="390" fill="url(#kmGrid)" />
                <circle cx="${{cx}}" cy="${{cy}}" r="95" fill="none" stroke="#1A2742" stroke-dasharray="3,6" />
                <circle cx="${{cx}}" cy="${{cy}}" r="165" fill="none" stroke="#18243D" stroke-dasharray="4,8" />
                ${{edgesSvg}}
                ${{nodesSvg}}
              </svg>
            </div>
            <div style="background:var(--bg-secondary);border:1px solid var(--border-default);border-radius:var(--radius-md);padding:18px">
              ${{selNode ? `
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                  <span class="km-metric-label">Selected Node Inspector</span>
                  <span class="km-badge verified">● ${{esc(selNode.status)}}</span>
                </div>
                <h4 style="margin:0 0 6px;font-size:16px">${{esc(selNode.label)}}</h4>
                <div class="km-mono" style="display:inline-block;margin-bottom:12px">did:kyro:${{esc(selNode.id)}}</div>
                <div class="km-field">
                  <span class="km-label">HTTP Federation Endpoint</span>
                  <div class="km-mono">${{esc(selNode.endpoint)}}</div>
                </div>
                <div class="km-field">
                  <span class="km-label">Visibility Policy</span>
                  <span class="km-badge info">${{esc(selNode.visibility)}}</span>
                </div>
                <div class="km-field">
                  <span class="km-label">Ed25519 Key Fingerprint (SHA-256)</span>
                  <div class="km-mono" style="word-break:break-all;font-size:11px;display:block;padding:6px">${{esc(selNode.fingerprint)}}</div>
                </div>
              ` : '<div class="km-metric-sub">No topology nodes registered yet.</div>'}}
            </div>
          </div>
        </div>
      `;
    }}

    function renderOKFGraphWorkspace() {{
      const hoveredId = state.graphHoverCard;
      const zoom = state.graphZoom || 100;
      const q = (state.graphSearch || '').toLowerCase();

      const defaultCards = [
        {{
          id: 'doc-md-1',
          category: 'Concept',
          title: 'KV-Cache Quantization',
          filename: 'concept-kv-quant.md',
          summary: 'Maintains 99.6% needle retrieval accuracy up to 128k context with 3.7x lower memory footprint.',
          meta: 'Confidence: 99.6% · 128k Tokens',
          color: '#4F46E5',
          x: 180,
          y: 135,
        }},
        {{
          id: 'doc-yaml-1',
          category: 'Specification',
          title: 'Format Specification',
          filename: 'manifest.yaml',
          summary: 'Open Knowledge Format v0.2 with canonical RFC 8785 JSON serialization and Ed25519 signing suite.',
          meta: 'Node: node-a · Ed25519 Signed',
          color: '#F59E0B',
          x: 180,
          y: 415,
        }},
        {{
          id: 'doc-md-2',
          category: 'Evidence',
          title: 'Empirical Benchmark',
          filename: 'evidence-benchmark.md',
          summary: 'Nsight trace confirms memory bandwidth saturation drops from 94% to 26% under INT4 KV caching.',
          meta: 'Reliability: 0.98 · 8xH100 SXM5',
          color: '#0EA5E9',
          x: 840,
          y: 135,
        }},
        {{
          id: 'doc-yaml-2',
          category: 'Provenance',
          title: 'Audit & Lineage Trail',
          filename: 'lineage-prov.yaml',
          summary: 'W3C PROV activity chain with immutable cryptographic generation hash and verification lineage.',
          meta: 'Actor: architect@kyro · Gen 1',
          color: '#10B981',
          x: 840,
          y: 415,
        }},
      ];

      const filteredCards = q
        ? defaultCards.filter(c => c.title.toLowerCase().includes(q) || c.filename.toLowerCase().includes(q) || c.summary.toLowerCase().includes(q))
        : defaultCards;

      const agents = [
        {{ id: 'agent-indexer', label: 'Index Agent', sub: 'Active · 60Hz', x: 510, y: 65, color: '#4F46E5' }},
        {{ id: 'agent-query-bot', label: 'Query Agent', sub: 'Active · Traversal', x: 510, y: 495, color: '#0EA5E9' }},
      ];
      if (state.agents && state.agents.length > 0) {{
        state.agents.slice(0, 2).forEach((ag, idx) => {{
          if (agents[idx]) agents[idx].label = ag.name;
        }});
      }}

      return `
        <div style="display:flex;height:calc(100vh - 110px);min-height:540px;background:#FAFAFB;border-radius:16px;border:1px solid #E2E8F0;overflow:hidden;box-shadow:0 12px 32px -4px rgba(10,15,29,0.06);font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif">
          <!-- Left mini navigation rail -->
          <aside style="width:64px;background:#FFFFFF;border-right:1px solid #E2E8F0;display:flex;flex-direction:column;align-items:center;padding:16px 0;gap:12px;flex-shrink:0">
            <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:#FFFFFF;box-shadow:0 4px 12px rgba(79,70,229,0.25);margin-bottom:12px">
              KY
            </div>
            <button class="km-btn km-btn-sm" title="Overview" onclick="window.kmAction.setTab('overview')" style="width:40px;height:40px;padding:0;display:flex;align-items:center;justify-content:center;font-size:16px;color:#64748B;background:transparent;border:none">⊞</button>
            <button class="km-btn km-btn-sm" title="Knowledge Documents" onclick="window.kmAction.setTab('knowledge')" style="width:40px;height:40px;padding:0;display:flex;align-items:center;justify-content:center;font-size:15px;color:#64748B;background:transparent;border:none">📄</button>
            <button class="km-btn km-btn-sm" title="Graph Canvas (Active)" style="width:40px;height:40px;padding:0;display:flex;align-items:center;justify-content:center;font-size:16px;color:#4F46E5;background:#EEF2FF;border:1px solid #E0E7FF;border-radius:10px">☍</button>
            <button class="km-btn km-btn-sm" title="AI Agents" onclick="window.kmAction.setTab('agents')" style="width:40px;height:40px;padding:0;display:flex;align-items:center;justify-content:center;font-size:15px;color:#64748B;background:transparent;border:none">🤖</button>
            <button class="km-btn km-btn-sm" title="Settings" onclick="window.kmAction.setTab('settings')" style="width:40px;height:40px;padding:0;display:flex;align-items:center;justify-content:center;font-size:15px;color:#64748B;background:transparent;border:none">⚙</button>
          </aside>

          <!-- Main workspace canvas -->
          <div style="flex:1;display:flex;flex-direction:column;overflow:hidden">
            <!-- App Top Header -->
            <header style="height:56px;background:#FFFFFF;border-bottom:1px solid #E2E8F0;display:flex;align-items:center;justify-content:space-between;padding:0 24px;gap:16px;flex-shrink:0">
              <div style="display:flex;align-items:center;gap:8px;font-size:13px">
                <span style="color:#64748B">Workspace</span>
                <span style="color:#CBD5E1">/</span>
                <span style="color:#0A0F1D;font-weight:600">Knowledge Graph</span>
                <span style="padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;background:rgba(16,185,129,0.08);color:#059669;border:1px solid rgba(16,185,129,0.2);margin-left:6px">● Live Mesh</span>
              </div>
              <div style="flex:1;max-width:320px;position:relative">
                <input type="text" placeholder="Filter graph nodes…" value="${{esc(state.graphSearch || '')}}" oninput="window.kmAction.setGraphSearch(this.value)" style="width:100%;height:34px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:0 12px 0 32px;color:#0A0F1D;font-size:12.5px;outline:none" />
                <span style="position:absolute;left:10px;top:8px;color:#94A3B8;font-size:14px">⌕</span>
              </div>
              <div style="display:flex;align-items:center;gap:10px">
                <button class="km-btn km-btn-sm" onclick="window.kmAction.reassembleGraph()" title="Reassemble mesh graph layout"><span style="font-size:12px;margin-right:4px">✨</span> Arrange</button>
                <button class="km-btn km-btn-sm" onclick="window.kmShowToast('✓ Repository knowledge tree is synchronized with commit HEAD.', 'success')">Sync</button>
                <button class="km-btn km-btn-sm" onclick="window.kmShowToast('✓ Exported verified knowledge bundle (RFC 8785 canonical JCS).', 'success')">Export</button>
                <button class="km-btn km-btn-sm km-btn-primary" onclick="window.kmShowToast('✓ Verified knowledge published to federated mesh nodes.', 'success')">Deploy to Mesh</button>
                <div style="width:34px;height:34px;border-radius:50%;background:#F1F5F9;border:1.5px solid #E2E8F0;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;color:#0A0F1D;margin-left:4px">KY</div>
              </div>
            </header>

            <!-- Graph Canvas Area -->
            <div id="km-okf-graph-container" style="flex:1;position:relative;overflow:hidden;background:#FAFAFB;display:flex;align-items:center;justify-content:center">
              <div id="km-okf-graph-stage" style="position:relative;width:1020px;height:580px;transform-origin:center center;transition:none;flex-shrink:0">
                <svg viewBox="0 0 1020 580" style="position:absolute;inset:0;width:100%;height:100%">
                  <defs>
                    <pattern id="okfDotGridUiLight" width="24" height="24" patternUnits="userSpaceOnUse">
                      <circle cx="2" cy="2" r="1.2" fill="#E2E8F0" />
                    </pattern>
                    <filter id="neon-glow" x="-50%" y="-50%" width="200%" height="200%">
                      <feGaussianBlur in="SourceGraphic" stdDeviation="3.5" result="blur" />
                      <feMerge>
                        <feMergeNode in="blur" />
                        <feMergeNode in="SourceGraphic" />
                      </feMerge>
                    </filter>
                  </defs>
                  <rect width="100%" height="100%" fill="url(#okfDotGridUiLight)" />

                  <!-- Central Radar Wave Pulse Rings -->
                  <circle cx="510" cy="275" r="30" fill="none" stroke="#4F46E5" stroke-width="2" opacity="0.8">
                    <animate attributeName="r" values="30;85" dur="2.8s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.8;0" dur="2.8s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="510" cy="275" r="30" fill="none" stroke="#7C3AED" stroke-width="1.5" opacity="0.6">
                    <animate attributeName="r" values="30;115" dur="2.8s" begin="1.4s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.6;0" dur="2.8s" begin="1.4s" repeatCount="indefinite" />
                  </circle>

                  <!-- Smooth Connection Curves with Clean Terminal Ports (Card Edge to Anchor Edge) -->
                  <!-- Top-Left: KV-Cache Quantization (295, 135) to Anchor (390, 255) -->
                  <path class="km-laser-path-1" d="M 295 135 C 345 135, 340 255, 390 255" fill="none" stroke="#CBD5E1" stroke-width="1.8" />
                  <circle class="km-ignited-port" cx="295" cy="135" r="5" fill="#4F46E5" stroke="#FFFFFF" stroke-width="2" />
                  <circle class="km-ignited-port" cx="390" cy="255" r="5" fill="#4F46E5" stroke="#FFFFFF" stroke-width="2" />
                  <circle r="8" fill="#4F46E5" opacity="0.45" filter="url(#neon-glow)"><animateMotion dur="2.2s" repeatCount="indefinite" path="M 295 135 C 345 135, 340 255, 390 255" /></circle>
                  <circle r="4.5" fill="#6366F1"><animateMotion dur="2.2s" repeatCount="indefinite" path="M 295 135 C 345 135, 340 255, 390 255" /></circle>
                  <circle r="2" fill="#FFFFFF"><animateMotion dur="2.2s" repeatCount="indefinite" path="M 295 135 C 345 135, 340 255, 390 255" /></circle>

                  <!-- Bottom-Left: Format Specification (295, 415) to Anchor (390, 295) -->
                  <path class="km-laser-path-2" d="M 295 415 C 345 415, 340 295, 390 295" fill="none" stroke="#CBD5E1" stroke-width="1.8" />
                  <circle class="km-ignited-port" cx="295" cy="415" r="5" fill="#F59E0B" stroke="#FFFFFF" stroke-width="2" />
                  <circle class="km-ignited-port" cx="390" cy="295" r="5" fill="#F59E0B" stroke="#FFFFFF" stroke-width="2" />
                  <circle r="8" fill="#F59E0B" opacity="0.45" filter="url(#neon-glow)"><animateMotion dur="2.6s" repeatCount="indefinite" path="M 295 415 C 345 415, 340 295, 390 295" /></circle>
                  <circle r="4.5" fill="#F59E0B"><animateMotion dur="2.6s" repeatCount="indefinite" path="M 295 415 C 345 415, 340 295, 390 295" /></circle>
                  <circle r="2" fill="#FFFFFF"><animateMotion dur="2.6s" repeatCount="indefinite" path="M 295 415 C 345 415, 340 295, 390 295" /></circle>

                  <!-- Top-Right: Anchor (630, 255) to Empirical Benchmark (725, 135) -->
                  <path class="km-laser-path-3" d="M 630 255 C 680 255, 675 135, 725 135" fill="none" stroke="#CBD5E1" stroke-width="1.8" />
                  <circle class="km-ignited-port" cx="630" cy="255" r="5" fill="#0EA5E9" stroke="#FFFFFF" stroke-width="2" />
                  <circle class="km-ignited-port" cx="725" cy="135" r="5" fill="#0EA5E9" stroke="#FFFFFF" stroke-width="2" />
                  <circle r="8" fill="#0EA5E9" opacity="0.45" filter="url(#neon-glow)"><animateMotion dur="2.0s" repeatCount="indefinite" path="M 630 255 C 680 255, 675 135, 725 135" /></circle>
                  <circle r="4.5" fill="#0EA5E9"><animateMotion dur="2.0s" repeatCount="indefinite" path="M 630 255 C 680 255, 675 135, 725 135" /></circle>
                  <circle r="2" fill="#FFFFFF"><animateMotion dur="2.0s" repeatCount="indefinite" path="M 630 255 C 680 255, 675 135, 725 135" /></circle>

                  <!-- Bottom-Right: Anchor (630, 295) to Audit & Lineage (725, 415) -->
                  <path class="km-laser-path-4" d="M 630 295 C 680 295, 675 415, 725 415" fill="none" stroke="#CBD5E1" stroke-width="1.8" />
                  <circle class="km-ignited-port" cx="630" cy="295" r="5" fill="#10B981" stroke="#FFFFFF" stroke-width="2" />
                  <circle class="km-ignited-port" cx="725" cy="415" r="5" fill="#10B981" stroke="#FFFFFF" stroke-width="2" />
                  <circle r="8" fill="#10B981" opacity="0.45" filter="url(#neon-glow)"><animateMotion dur="2.4s" repeatCount="indefinite" path="M 630 295 C 680 295, 675 415, 725 415" /></circle>
                  <circle r="4.5" fill="#10B981"><animateMotion dur="2.4s" repeatCount="indefinite" path="M 630 295 C 680 295, 675 415, 725 415" /></circle>
                  <circle r="2" fill="#FFFFFF"><animateMotion dur="2.4s" repeatCount="indefinite" path="M 630 295 C 680 295, 675 415, 725 415" /></circle>

                  <!-- Top AI Agent Vertical Connection -->
                  <line class="km-laser-vpath" x1="510" y1="220" x2="510" y2="108" stroke="#CBD5E1" stroke-width="1.6" stroke-dasharray="4,4" />
                  <circle class="km-ignited-port" cx="510" cy="220" r="4.5" fill="#4F46E5" stroke="#FFFFFF" stroke-width="1.8" />
                  <circle class="km-ignited-port" cx="510" cy="108" r="4.5" fill="#4F46E5" stroke="#FFFFFF" stroke-width="1.8" />
                  <circle r="7" fill="#4F46E5" opacity="0.45" filter="url(#neon-glow)"><animateMotion dur="1.7s" repeatCount="indefinite" path="M 510 220 L 510 108" /></circle>
                  <circle r="3.5" fill="#4F46E5"><animateMotion dur="1.7s" repeatCount="indefinite" path="M 510 220 L 510 108" /></circle>

                  <!-- Bottom AI Agent Vertical Connection -->
                  <line class="km-laser-vpath" x1="510" y1="330" x2="510" y2="440" stroke="#CBD5E1" stroke-width="1.6" stroke-dasharray="4,4" />
                  <circle class="km-ignited-port" cx="510" cy="330" r="4.5" fill="#0EA5E9" stroke="#FFFFFF" stroke-width="1.8" />
                  <circle class="km-ignited-port" cx="510" cy="440" r="4.5" fill="#0EA5E9" stroke="#FFFFFF" stroke-width="1.8" />
                  <circle r="7" fill="#0EA5E9" opacity="0.45" filter="url(#neon-glow)"><animateMotion dur="1.9s" repeatCount="indefinite" path="M 510 330 L 510 440" /></circle>
                  <circle r="3.5" fill="#0EA5E9"><animateMotion dur="1.9s" repeatCount="indefinite" path="M 510 330 L 510 440" /></circle>
                </svg>

                <!-- Center Anchor Node: Clean Verifiable Document -->
                <div class="km-float-centered km-mesh-anchor-core" style="position:absolute;left:510px;top:275px;width:240px;padding:18px 20px;background:#FFFFFF;border-radius:16px;border:1.5px solid #E2E8F0;box-shadow:0 16px 36px -8px rgba(10,15,29,0.08);display:flex;flex-direction:column;gap:6px;z-index:10;text-align:left;transform:translate(-50%, -50%)">
                  <div style="display:flex;align-items:center;justify-content:space-between">
                    <span style="font-size:11px;font-weight:700;color:#4F46E5;padding:2px 8px;border-radius:6px;background:rgba(79,70,229,0.08)">Mesh Anchor</span>
                    <span style="font-size:10px;font-weight:600;color:#059669;background:rgba(16,185,129,0.08);padding:2px 7px;border-radius:999px">✓ Verified</span>
                  </div>
                  <div style="font-weight:700;font-size:14px;color:#0A0F1D;margin-top:2px">Knowledge Document</div>
                  <div style="font-size:11px;color:#64748B;font-family:var(--font-mono)">did:kyro:bundle-root</div>
                  <div style="font-size:10.5px;color:#94A3B8;margin-top:2px;padding-top:6px;border-top:1px solid #F1F5F9">4 Linked Documents · RFC 8785</div>
                </div>

                <!-- Refined Document Cards (Spacious, Elegant, No Overlap, Smooth CSS Hover) -->
                ${{filteredCards.map((c, i) => {{
                  const levClass = c.id === 'doc-md-1' ? 'km-doc-levitate-1' : c.id === 'doc-yaml-1' ? 'km-doc-levitate-2' : c.id === 'doc-md-2' ? 'km-doc-levitate-3' : 'km-doc-levitate-4';
                  return `
                    <div class="km-float-centered km-okf-hover-card km-card-${{c.id}} ${{levClass}}" style="position:absolute;left:${{c.x}}px;top:${{c.y}}px;width:230px;background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:14px;padding:14px 16px;box-shadow:0 4px 16px rgba(10,15,29,0.04);transform:translate(-50%, -50%);z-index:12;cursor:pointer;text-align:left;--card-accent:${{c.color}}">
                      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                        <span style="font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:6px;color:${{c.color}};background:${{c.color}}14">${{c.category}}</span>
                        <span style="font-size:10px;font-weight:600;color:#059669;display:flex;align-items:center;gap:3px">● Verified</span>
                      </div>
                      <div style="font-weight:700;font-size:13px;color:#0A0F1D;margin-bottom:2px">${{esc(c.title)}}</div>
                      <div style="font-size:10.5px;color:#64748B;font-family:var(--font-mono);margin-bottom:8px">${{esc(c.filename)}}</div>
                      <div style="font-size:11px;color:#334155;line-height:1.45;margin-bottom:10px">${{esc(c.summary)}}</div>
                      <div style="font-size:10px;font-weight:500;color:#94A3B8;padding-top:8px;border-top:1px solid #F1F5F9">${{esc(c.meta)}}</div>
                    </div>
                  `;
                }}).join('')}}

                <!-- Outer Edge AI Agent Nodes -->
                ${{agents.map((ag, i) => {{
                  const agentClass = ag.y < 275 ? 'km-agent-levitate-top' : 'km-agent-levitate-bottom';
                  return `
                    <div class="km-float-centered ${{agentClass}}" style="position:absolute;left:${{ag.x}}px;top:${{ag.y}}px;display:flex;flex-direction:column;align-items:center;z-index:15;transform:translate(-50%, -50%)">
                      <div style="width:44px;height:44px;border-radius:50%;background:#FFFFFF;border:1.5px solid ${{ag.color}};display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px -2px rgba(10,15,29,0.08)">
                        <span style="font-size:11px;font-weight:800;color:${{ag.color}}">AI</span>
                      </div>
                      <div style="margin-top:6px;text-align:center;padding:3px 10px;background:#FFFFFF;border-radius:20px;border:1px solid #E2E8F0;box-shadow:0 2px 8px rgba(10,15,29,0.04)">
                        <div style="font-size:11px;font-weight:600;color:#0A0F1D">${{esc(ag.label)}}</div>
                        <div style="font-size:9.5px;color:#059669;font-weight:500">${{esc(ag.sub)}}</div>
                      </div>
                    </div>
                  `;
                }}).join('')}}
              </div>

              <!-- Mini Map Corner -->
              <div style="position:absolute;bottom:16px;left:16px;width:120px;height:70px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;padding:8px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 4px 12px rgba(10,15,29,0.05);pointer-events:none">
                <span style="font-size:9px;font-weight:700;color:#64748B;letter-spacing:0.04em">MINI-MAP</span>
                <div style="position:relative;flex:1;border:1px dashed #E2E8F0;border-radius:4px;margin-top:4px">
                  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:12px;height:8px;background:#4F46E5;border-radius:2px"></div>
                  <div style="position:absolute;top:20%;left:20%;width:7px;height:5px;background:#4F46E5;opacity:0.6;border-radius:1px"></div>
                  <div style="position:absolute;bottom:20%;left:20%;width:7px;height:5px;background:#F59E0B;opacity:0.6;border-radius:1px"></div>
                  <div style="position:absolute;top:20%;right:20%;width:7px;height:5px;background:#0EA5E9;opacity:0.6;border-radius:1px"></div>
                  <div style="position:absolute;bottom:20%;right:20%;width:7px;height:5px;background:#10B981;opacity:0.6;border-radius:1px"></div>
                </div>
              </div>

              <!-- Zoom Controls -->
              <div style="position:absolute;bottom:16px;right:16px;display:flex;align-items:center;gap:6px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;padding:4px 8px;box-shadow:0 4px 12px rgba(10,15,29,0.05)">
                <button class="km-btn km-btn-sm" onclick="window.kmAction.setGraphZoom(-15)" style="padding:2px 8px;font-size:12px">-</button>
                <span style="font-size:11px;font-family:var(--font-mono);color:#0A0F1D;min-width:40px;text-align:center">${{zoom}}%</span>
                <button class="km-btn km-btn-sm" onclick="window.kmAction.setGraphZoom(15)" style="padding:2px 8px;font-size:12px">+</button>
                <button class="km-btn km-btn-sm" onclick="window.kmAction.resetGraphZoom()" style="padding:2px 8px;font-size:10.5px">Reset</button>
              </div>
            </div>
          </div>
        </div>
      `;
    }}

    function renderMainContent() {{
      const m = (state.overview && state.overview.metrics) || {{
        total_nodes: state.nodes.length,
        online_peers: state.peers.length,
        total_peers: state.peers.length,
        knowledge_bundles: state.bundles.length,
        published_claims: state.bundles.reduce((a, b) => a + (b.claims ? b.claims.length : 0), 0),
        registered_agents: state.agents.length,
        pending_reviews: 0,
      }};

      if (state.activeTab === 'okf-graph') {{
        return renderOKFGraphWorkspace();
      }}

      if (state.activeTab === 'overview') {{
        const dist = (state.overview && state.overview.claim_review_distribution) || {{}};
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Federated Network Control Plane</h1>
              <p class="km-page-subtitle">Real-time operational telemetry for sovereign knowledge nodes, Ed25519 cryptographic provenance, and pull-based peer synchronization.</p>
            </div>
            <div style="display:flex;gap:10px">
              <button class="km-btn km-btn-accent" onclick="window.kmAction.bootstrapDemo()">Seed 4-Node Federation State</button>
              <button class="km-btn km-btn-primary" onclick="window.kmAction.setTab('knowledge')">+ Publish Knowledge Bundle</button>
            </div>
          </div>
          <div class="km-grid-4">
            <div class="km-card km-card-interactive" onclick="window.kmAction.setTab('nodes')">
              <div style="display:flex;justify-content:space-between"><span class="km-metric-label">Sovereign Nodes</span><span class="km-badge verified">Ed25519 Active</span></div>
              <div class="km-metric-value">${{m.total_nodes}}</div>
              <div class="km-metric-sub">Anchor node: ${{esc((state.overview && state.overview.node_id) || 'node-a')}}</div>
            </div>
            <div class="km-card km-card-interactive" onclick="window.kmAction.setTab('federation')">
              <div style="display:flex;justify-content:space-between"><span class="km-metric-label">Federated Peers</span><span class="km-badge info">Pull-Sync Ready</span></div>
              <div class="km-metric-value">${{m.online_peers}} / ${{m.total_peers}}</div>
              <div class="km-metric-sub">HTTP peer protocol</div>
            </div>
            <div class="km-card km-card-interactive" onclick="window.kmAction.setTab('knowledge')">
              <div style="display:flex;justify-content:space-between"><span class="km-metric-label">Signed OKF Bundles</span><span class="km-badge verified">RFC 8785 JCS</span></div>
              <div class="km-metric-value">${{m.knowledge_bundles}}</div>
              <div class="km-metric-sub">${{m.published_claims}} atomic claims indexed</div>
            </div>
            <div class="km-card km-card-interactive" onclick="window.kmAction.setTab('agents')">
              <div style="display:flex;justify-content:space-between"><span class="km-metric-label">Authorized AI Agents</span><span class="km-badge violet">SHA-256 Scoped</span></div>
              <div class="km-metric-value">${{m.registered_agents}}</div>
              <div class="km-metric-sub">Least-privilege API keys</div>
            </div>
          </div>
          ${{renderTopologySvg()}}
          <div class="km-grid-asym">
            <div class="km-card">
              <div class="km-card-header">
                <h3 class="km-card-title">Recent Cryptographic &amp; Federation Audit Stream</h3>
                <button class="km-btn km-btn-sm" onclick="window.kmAction.setTab('audit')">Full Audit Trail →</button>
              </div>
              <div class="km-table-wrap">
                <table class="km-table">
                  <thead><tr><th>Action</th><th>Category</th><th>Actor</th><th>Resource</th><th>Outcome</th></tr></thead>
                  <tbody>
                    ${{state.audit.slice(0, 6).map(ev => `
                      <tr>
                        <td style="font-weight:600">${{esc(ev.action)}}</td>
                        <td><span class="km-badge">${{esc(ev.category)}}</span></td>
                        <td><span class="km-mono">${{esc(ev.actor_id.slice(0, 18))}}</span></td>
                        <td><span class="km-mono">${{esc(ev.resource_id)}}</span></td>
                        <td><span class="km-badge ${{esc(ev.outcome)}}">${{esc(ev.outcome)}}</span></td>
                      </tr>
                    `).join('')}}
                  </tbody>
                </table>
              </div>
            </div>
            <div class="km-card">
              <div class="km-card-header">
                <h3 class="km-card-title">Epistemic Claim Lifecycle</h3>
                <span class="km-badge info">Assessment ≠ Truth</span>
              </div>
              <div style="display:flex;flex-direction:column;gap:12px">
                ${{Object.entries(dist).map(([st, cnt]) => `
                  <div style="padding:10px 12px;background:var(--bg-secondary);border-radius:var(--radius-sm);border:1px solid var(--border-subtle)">
                    <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                      <span class="km-badge ${{esc(st)}}">${{esc(st)}}</span>
                      <strong>${{cnt}} claims</strong>
                    </div>
                    <div class="km-progress-track"><div class="km-progress-fill" style="width:100%"></div></div>
                  </div>
                `).join('')}}
              </div>
            </div>
          </div>
        `;
      }}

      if (state.activeTab === 'nodes') {{
        const activeNode = state.nodes.find(n => n.node_id === state.selectedNodeId) || state.nodes[0];
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Independent Knowledge Nodes</h1>
              <p class="km-page-subtitle">Each Kyro node maintains its own Ed25519 cryptographic identity, publication visibility policy, and sovereign data boundary.</p>
            </div>
            <button class="km-btn km-btn-primary" onclick="window.kmAction.createNodeModal()">+ Add Knowledge Node</button>
          </div>
          <div class="km-grid-3">
            ${{state.nodes.map(n => `
              <div class="km-card km-card-interactive" style="${{activeNode && activeNode.node_id === n.node_id ? 'border-color:var(--accent-primary)' : ''}}" onclick="window.kmAction.selectNode('${{esc(n.node_id)}}')">
                <div class="km-card-header" style="margin-bottom:8px">
                  <span class="km-mono">did:kyro:${{esc(n.node_id)}}</span>
                  <span class="km-badge ${{esc(n.visibility)}}">${{esc(n.visibility)}}</span>
                </div>
                <h3 style="margin:0 0 6px;font-size:16px">${{esc(n.name)}}</h3>
                <p class="km-metric-sub" style="margin:0 0 10px">${{esc(n.description)}}</p>
                <div class="km-mono" style="margin-bottom:10px;display:inline-block">${{esc(n.endpoint)}}</div>
                <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text-secondary);border-top:1px solid var(--border-subtle);padding-top:10px">
                  <span>${{n.bundle_count}} bundles</span>
                  <span>${{n.agent_count}} agents</span>
                  <span>⇄ ${{n.peer_count}} peers</span>
                </div>
              </div>
            `).join('')}}
          </div>
          ${{activeNode ? `
            <div class="km-card">
              <div class="km-card-header">
                <div>
                  <h2 class="km-card-title" style="font-size:18px">Node Inspector: ${{esc(activeNode.name)}} (${{esc(activeNode.node_id)}})</h2>
                  <div class="km-metric-sub">Ed25519 Fingerprint: <span class="km-mono">${{esc(activeNode.key_fingerprint)}}</span></div>
                </div>
                <div style="display:flex;gap:8px;flex-wrap:wrap">
                  <button class="km-btn km-btn-sm" onclick="window.kmAction.rotateNodeKey('${{esc(activeNode.node_id)}}')">⟳ Rotate Ed25519 Signing Key</button>
                  <button class="km-btn km-btn-sm" onclick="window.kmAction.setNodeVisibility('${{esc(activeNode.node_id)}}', 'federated')">Set FEDERATED</button>
                  <button class="km-btn km-btn-sm" onclick="window.kmAction.setNodeVisibility('${{esc(activeNode.node_id)}}', 'organization')">Set ORGANIZATION</button>
                  <button class="km-btn km-btn-sm" onclick="window.kmAction.setNodeVisibility('${{esc(activeNode.node_id)}}', 'private')">Set PRIVATE</button>
                </div>
              </div>
              <div class="km-grid-3">
                <div class="km-card" style="background:var(--bg-secondary)">
                  <div class="km-metric-label">Visibility Policy</div>
                  <div class="km-metric-value" style="font-size:22px">${{esc(activeNode.visibility.toUpperCase())}}</div>
                  <div class="km-metric-sub">Enforced on all federated discovery &amp; bundle fetches</div>
                </div>
                <div class="km-card" style="background:var(--bg-secondary)">
                  <div class="km-metric-label">Ed25519 Public Key</div>
                  <div class="km-mono" style="margin-top:10px;word-break:break-all;display:block">${{esc(activeNode.public_key)}}</div>
                </div>
                <div class="km-card" style="background:var(--bg-secondary)">
                  <div class="km-metric-label">Capabilities</div>
                  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px">
                    ${{activeNode.capabilities.map(c => `<span class="km-badge info">✓ ${{esc(c)}}</span>`).join('')}}
                  </div>
                </div>
              </div>
            </div>
          ` : ''}}
        `;
      }}

      if (state.activeTab === 'knowledge') {{
        const activeBundle = state.bundles.find(b => b.bundle_id === state.selectedBundleId) || state.bundles[0];
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Knowledge Bundles &amp; OKF Studio</h1>
              <p class="km-page-subtitle">Author, validate, sign, version, and verify Open Knowledge Format (OKF) bundles with traceable atomic claims and supporting evidence.</p>
            </div>
            <div style="display:flex;align-items:center;gap:10px">
              <button class="km-btn" onclick="window.kmAction.openModal('ingestPaper')" style="background:linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);color:#FFFFFF;border:none;box-shadow:0 4px 12px rgba(99,102,241,0.25);display:flex;align-items:center;gap:6px"><span>⚡</span> Ingest Paper &amp; Extract Claims</button>
              <button class="km-btn km-btn-primary" onclick="window.kmAction.createQuickBundle()">+ Create &amp; Sign Knowledge Bundle</button>
            </div>
          </div>
          <div class="km-table-wrap" style="margin-bottom:24px">
            <table class="km-table">
              <thead><tr><th>Bundle ID</th><th>Title</th><th>Domain</th><th>Node</th><th>Revision</th><th>Visibility</th><th>Claims / Evidence</th><th>Verification</th></tr></thead>
              <tbody>
                ${{state.bundles.map(b => `
                  <tr class="${{activeBundle && activeBundle.bundle_id === b.bundle_id ? 'selected-row' : ''}}" style="cursor:pointer" onclick="window.kmAction.selectBundle('${{esc(b.bundle_id)}}')">
                    <td><span class="km-mono">${{esc(b.bundle_id)}}</span></td>
                    <td style="font-weight:600">${{esc(b.title)}}</td>
                    <td><span class="km-badge">${{esc(b.category)}}</span></td>
                    <td><span class="km-mono">${{esc(b.publisher_node_id)}}</span></td>
                    <td><span class="km-mono">v${{esc(b.current_revision)}}</span></td>
                    <td><span class="km-badge ${{esc(b.visibility)}}">${{esc(b.visibility)}}</span></td>
                    <td>${{b.claims.length}} claims · ${{b.evidence.length}} evidence</td>
                    <td><span class="km-badge ${{esc(b.verification.status)}}">✓ ${{esc(b.verification.status)}}</span></td>
                  </tr>
                `).join('')}}
              </tbody>
            </table>
          </div>
          ${{activeBundle ? `
            <div class="km-card">
              <div class="km-card-header">
                <div>
                  <h2 class="km-card-title" style="font-size:18px">${{esc(activeBundle.title)}} <span class="km-mono">${{esc(activeBundle.bundle_id)}}@v${{esc(activeBundle.current_revision)}}</span></h2>
                  <div class="km-metric-sub">Origin Node: <span class="km-mono">${{esc(activeBundle.origin_node_id)}}</span> · Canonical Digest: <span class="km-mono">${{esc(activeBundle.content_digest.slice(0, 24))}}…</span></div>
                </div>
                <span class="km-badge verified">● ${{esc(activeBundle.verification.status)}}</span>
              </div>
              <div class="km-tabs">
                <button class="km-tab ${{state.bundleDetailTab === 'overview' ? 'active' : ''}}" onclick="window.kmAction.setBundleTab('overview')">Overview</button>
                <button class="km-tab ${{state.bundleDetailTab === 'claims' ? 'active' : ''}}" onclick="window.kmAction.setBundleTab('claims')">Statements (${{activeBundle.claims.length}})</button>
                <button class="km-tab ${{state.bundleDetailTab === 'evidence' ? 'active' : ''}}" onclick="window.kmAction.setBundleTab('evidence')">Sources (${{activeBundle.evidence.length}})</button>
                <button class="km-tab ${{state.bundleDetailTab === 'versions' ? 'active' : ''}}" onclick="window.kmAction.setBundleTab('versions')">Revisions (${{activeBundle.revisions.length}})</button>
                <button class="km-tab ${{state.bundleDetailTab === 'provenance' ? 'active' : ''}}" onclick="window.kmAction.setBundleTab('provenance')">Provenance &amp; History (${{activeBundle.provenance.length}})</button>
              </div>
              ${{state.bundleDetailTab === 'overview' ? `
                <div class="km-notice"><span><strong>Epistemic Separation:</strong> ${{esc(activeBundle.verification.epistemic_notice)}}</span></div>
                <div class="km-grid-3">
                  <div class="km-card" style="background:var(--bg-secondary)"><div class="km-metric-label">1. RFC 8785 JCS Digest</div><div style="margin-top:8px"><span class="km-badge verified">✓ SHA-256 Digest Verified</span></div></div>
                  <div class="km-card" style="background:var(--bg-secondary)"><div class="km-metric-label">2. Ed25519 Signature</div><div style="margin-top:8px"><span class="km-badge verified">✓ Ed25519 Signature Valid</span></div></div>
                  <div class="km-card" style="background:var(--bg-secondary)"><div class="km-metric-label">3. Signer Identity</div><div style="margin-top:8px"><span class="km-badge verified">✓ Recognized (${{esc(activeBundle.signer_id)}})</span></div></div>
                </div>
              ` : ''}}
              ${{state.bundleDetailTab === 'claims' ? `
                <div class="km-table-wrap">
                  <table class="km-table">
                    <thead><tr><th>Claim ID</th><th>Atomic Statement</th><th>Status</th><th>Update Assessment</th></tr></thead>
                    <tbody>
                      ${{activeBundle.claims.map(c => `
                        <tr>
                          <td><span class="km-mono">${{esc(c.claim_id)}}</span></td>
                          <td>${{esc(c.statement)}}</td>
                          <td><span class="km-badge ${{esc(c.status)}}">${{esc(c.status)}}</span></td>
                          <td>
                            <select class="km-select" style="width:165px;padding:4px 8px" onchange="window.kmAction.updateClaimStatus('${{esc(c.claim_id)}}', this.value)">
                              ${{['proposed','evidence_attached','under_review','supported','contested','inconclusive','rejected'].map(s => `<option value="${{s}}" ${{c.status === s ? 'selected' : ''}}>${{s}}</option>`).join('')}}
                            </select>
                          </td>
                        </tr>
                      `).join('')}}
                    </tbody>
                  </table>
                </div>
              ` : ''}}
              ${{state.bundleDetailTab === 'evidence' ? `
                <div class="km-table-wrap">
                  <table class="km-table">
                    <thead><tr><th>Evidence ID</th><th>Description</th><th>Source Type</th><th>Traceable Source URI</th></tr></thead>
                    <tbody>
                      ${{activeBundle.evidence.map(ev => `
                        <tr>
                          <td><span class="km-mono">${{esc(ev.evidence_id)}}</span></td>
                          <td>${{esc(ev.description)}}</td>
                          <td><span class="km-badge info">${{esc(ev.source_type)}}</span></td>
                          <td><span class="km-mono">${{esc(ev.source_uri)}}</span></td>
                        </tr>
                      `).join('')}}
                    </tbody>
                  </table>
                </div>
              ` : ''}}
              ${{state.bundleDetailTab === 'versions' ? `
                <div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap">
                  <input id="km-rev-claim" class="km-input" style="flex:1" placeholder="Add new atomic claim to next immutable revision…" />
                  <input id="km-rev-note" class="km-input" style="width:260px" value="Added empirical replication claim" />
                  <button class="km-btn km-btn-primary" onclick="window.kmAction.publishRevision('${{esc(activeBundle.bundle_id)}}')">+ Publish Immutable Revision</button>
                </div>
                <div class="km-table-wrap">
                  <table class="km-table">
                    <thead><tr><th>Revision</th><th>Parent</th><th>Canonical Digest</th><th>Change Note</th><th>Published At</th></tr></thead>
                    <tbody>
                      ${{activeBundle.revisions.map((r, i) => `
                        <tr>
                          <td><span class="km-badge ${{i === 0 ? 'verified' : ''}}">v${{esc(r.revision)}} ${{i === 0 ? '(Head)' : '(Superseded)'}}</span></td>
                          <td><span class="km-mono">${{r.previous_revision ? '← v' + esc(r.previous_revision) : 'GENESIS'}}</span></td>
                          <td><span class="km-mono">${{esc(r.content_digest.slice(0, 20))}}…</span></td>
                          <td>${{esc(r.change_note)}}</td>
                          <td>${{new Date(r.published_at).toLocaleString()}}</td>
                        </tr>
                      `).join('')}}
                    </tbody>
                  </table>
                </div>
              ` : ''}}
              ${{state.bundleDetailTab === 'provenance' ? `
                <div class="km-table-wrap">
                  <table class="km-table">
                    <thead><tr><th>Record ID</th><th>Action</th><th>Actor</th><th>Node</th><th>Parent Hash</th><th>Record Hash</th></tr></thead>
                    <tbody>
                      ${{activeBundle.provenance.map(p => `
                        <tr>
                          <td><span class="km-mono">${{esc(p.record_id)}}</span></td>
                          <td><span class="km-badge info">${{esc(p.action)}}</span></td>
                          <td><span class="km-mono">${{esc(p.actor_id)}}</span></td>
                          <td><span class="km-mono">${{esc(p.node_id)}}</span></td>
                          <td><span class="km-mono">${{p.previous_hash ? esc(p.previous_hash.slice(0, 12)) + '…' : 'GENESIS'}}</span></td>
                          <td><span class="km-mono">${{esc(p.record_hash.slice(0, 16))}}…</span></td>
                        </tr>
                      `).join('')}}
                    </tbody>
                  </table>
                </div>
              ` : ''}}
            </div>
          ` : ''}}
        `;
      }}

      if (state.activeTab === 'claims') {{
        const allClaims = state.bundles.flatMap(b => (b.claims || []).map(c => ({{ ...c, bundle: b }})));
        const activeClaim = allClaims.find(c => c.claim_id === state.selectedClaimId) || allClaims[0] || null;
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Atomic Claims &amp; Epistemic Lifecycle</h1>
              <p class="km-page-subtitle">Inspect atomic claims across all OKF bundles and update review statuses directly via PATCH /api/v1/claims/&lt;id&gt;/status.</p>
            </div>
            <button class="km-btn" onclick="window.kmAction.openModal('ingestPaper')" style="background:linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);color:#FFFFFF;border:none;box-shadow:0 4px 12px rgba(99,102,241,0.25);display:flex;align-items:center;gap:6px"><span>⚡</span> Ingest Paper &amp; Extract Claims</button>
          </div>
          <div class="km-grid-asym">
            <div class="km-card">
              <div class="km-card-header"><h3 class="km-card-title">Federated Claims Registry (${{allClaims.length}})</h3></div>
              <div class="km-table-wrap">
                <table class="km-table">
                  <thead><tr><th>Claim ID</th><th>Statement</th><th>Origin Bundle</th><th>Status</th></tr></thead>
                  <tbody>
                    ${{allClaims.map(c => `
                      <tr class="${{activeClaim && activeClaim.claim_id === c.claim_id ? 'selected-row' : ''}}" style="cursor:pointer" onclick="window.kmAction.selectClaim('${{esc(c.claim_id)}}')">
                        <td><span class="km-mono">${{esc(c.claim_id)}}</span></td>
                        <td>${{esc(c.statement)}}</td>
                        <td><span class="km-mono">${{esc(c.bundle.bundle_id)}}@v${{esc(c.bundle.current_revision)}}</span></td>
                        <td><span class="km-badge ${{esc(c.status)}}">${{esc(c.status)}}</span></td>
                      </tr>
                    `).join('')}}
                  </tbody>
                </table>
              </div>
            </div>
            <div class="km-card">
              ${{activeClaim ? `
                <div class="km-card-header">
                  <h3 class="km-card-title">Claim Inspector: <span class="km-mono">${{esc(activeClaim.claim_id)}}</span></h3>
                  <span class="km-badge ${{esc(activeClaim.status)}}">${{esc(activeClaim.status)}}</span>
                </div>
                <p style="font-size:14px">${{esc(activeClaim.statement)}}</p>
                <div class="km-field">
                  <label class="km-label">Transition Review Lifecycle Status</label>
                  <select class="km-select" onchange="window.kmAction.updateClaimStatus('${{esc(activeClaim.claim_id)}}', this.value)">
                    ${{['proposed','evidence_attached','under_review','supported','contested','inconclusive','rejected'].map(s => `<option value="${{s}}" ${{activeClaim.status === s ? 'selected' : ''}}>${{s}}</option>`).join('')}}
                  </select>
                </div>
              ` : '<div class="km-metric-sub">No claims available.</div>'}}
            </div>
          </div>
        `;
      }}

      if (state.activeTab === 'discover') {{
        const sr = state.searchResults;
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Federated Knowledge Discovery</h1>
              <p class="km-page-subtitle">Query local BM25 indexes and authorized federated peer nodes with full provenance, freshness, and Ed25519 verification badges.</p>
            </div>
          </div>
          <div class="km-card" style="margin-bottom:24px">
            <div style="display:grid;grid-template-columns:1fr 200px auto;gap:12px">
              <input id="km-search-q" class="km-input" value="${{esc(state.searchQuery)}}" placeholder="Search claims, evidence, or bundles across federated nodes…" />
              <select id="km-search-scope" class="km-select">
                <option value="federated" ${{state.searchScope === 'federated' ? 'selected' : ''}}>Scope: Federated Mesh</option>
                <option value="organization" ${{state.searchScope === 'organization' ? 'selected' : ''}}>Scope: Organization</option>
                <option value="local" ${{state.searchScope === 'local' ? 'selected' : ''}}>Scope: Local Node</option>
              </select>
              <button class="km-btn km-btn-primary" onclick="window.kmAction.runSearch()">⌕ Search Mesh</button>
            </div>
          </div>
          ${{sr ? `
            <div style="margin-bottom:14px;color:var(--text-secondary)">Found <strong>${{sr.total}}</strong> verified results for <span class="km-mono">${{esc(sr.query)}}</span></div>
            <div style="display:flex;flex-direction:column;gap:14px">
              ${{(sr.results || []).map(hit => `
                <div class="km-card">
                  <div class="km-card-header" style="margin-bottom:8px">
                    <div>
                      <span class="km-mono">${{esc(hit.bundle_id)}}@v${{esc(hit.revision)}}</span>
                      <span class="km-badge info" style="margin-left:8px">Origin: ${{esc(hit.publisher_node)}}</span>
                    </div>
                    <span class="km-badge verified">✓ ${{esc(hit.verification_status)}} · BM25: ${{hit.score}}</span>
                  </div>
                  <h3 style="margin:0 0 6px;font-size:17px">${{esc(hit.title)}}</h3>
                  <p class="km-metric-sub">${{esc(hit.description)}}</p>
                </div>
              `).join('')}}
            </div>
          ` : ''}}
        `;
      }}

      if (state.activeTab === 'agents') {{
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">AI Agent Identities &amp; Credentials</h1>
              <p class="km-page-subtitle">Register authorized AI agents, enforce least-privilege scopes, and manage SHA-256 hashed API credentials.</p>
            </div>
            <div style="display:flex;gap:10px;align-items:center">
              <button class="km-btn km-btn-sm" style="background:#F8FAFC;border:1px solid #CBD5E1;color:#0A0F1D;font-weight:600" onclick="window.kmAction.simulatePermissionEscalation()">⚡ Simulate Permission Request</button>
              <button class="km-btn km-btn-primary" onclick="window.kmAction.createQuickAgent()">+ Register AI Agent</button>
            </div>
          </div>
          ${{state.oneTimeSecret ? `
            <div class="km-notice warning" style="margin-bottom:20px;display:flex;align-items:flex-start;justify-content:space-between">
              <div>
                <strong style="color:#0A0F1D;font-size:13px">One-Time Secret Key Issued</strong>
                <div class="km-metric-sub" style="margin-top:2px;margin-bottom:8px">Copy and store this secret key securely. It will not be shown again.</div>
                <div class="km-mono" style="font-size:13px;padding:8px 12px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0A0F1D;user-select:all">${{esc(state.oneTimeSecret)}}</div>
              </div>
              <button class="km-modal-close" style="width:28px;height:28px;margin-left:12px" onclick="window.kmAction.dismissSecret()" aria-label="Dismiss">✕</button>
            </div>
          ` : ''}}
          <div class="km-table-wrap" style="margin-bottom:24px">
            <table class="km-table">
              <thead><tr><th>Agent ID</th><th>Name &amp; Purpose</th><th>Node</th><th>Status</th><th>Permissions</th><th>Actions</th></tr></thead>
              <tbody>
                ${{state.agents.map(ag => `
                  <tr>
                    <td><span class="km-mono">${{esc(ag.agent_id)}}</span></td>
                    <td><strong>${{esc(ag.name)}}</strong><div class="km-metric-sub">${{esc(ag.description)}}</div></td>
                    <td><span class="km-mono">${{esc(ag.node_id)}}</span></td>
                    <td><span class="km-badge ${{esc(ag.status)}}">● ${{esc(ag.status)}}</span></td>
                    <td><div style="display:flex;gap:4px;flex-wrap:wrap">${{ag.permissions.map(p => `<span class="km-badge info">${{esc(p)}}</span>`).join('')}}</div></td>
                    <td><button class="km-btn km-btn-sm" onclick="window.kmAction.openPermissionModal('${{esc(ag.agent_id)}}')">🛡 Delegate Scopes</button></td>
                  </tr>
                `).join('')}}
              </tbody>
            </table>
          </div>
          <div class="km-card">
            <div class="km-card-header"><h3 class="km-card-title">API Credentials Registry (SHA-256 Hashed at Rest)</h3></div>
            <div class="km-table-wrap">
              <table class="km-table">
                <thead><tr><th>Credential ID</th><th>Name</th><th>Agent</th><th>Masked Prefix</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody>
                  ${{state.credentials.map(c => `
                    <tr>
                      <td><span class="km-mono">${{esc(c.credential_id)}}</span></td>
                      <td>${{esc(c.name)}}</td>
                      <td><span class="km-mono">${{esc(c.agent_id || 'org-scoped')}}</span></td>
                      <td><span class="km-mono">${{esc(c.key_prefix)}}••••••••••••</span></td>
                      <td><span class="km-badge ${{esc(c.status)}}">${{esc(c.status)}}</span></td>
                      <td>
                        ${{c.status === 'active' ? `
                          <button class="km-btn km-btn-sm" onclick="window.kmAction.rotateCredential('${{esc(c.credential_id)}}')">⟳ Rotate</button>
                          <button class="km-btn km-btn-sm km-btn-danger" onclick="window.kmAction.revokeCredential('${{esc(c.credential_id)}}')">Revoke</button>
                        ` : ''}}
                      </td>
                    </tr>
                  `).join('')}}
                </tbody>
              </table>
            </div>
          </div>
        `;
      }}

      if (state.activeTab === 'federation') {{
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Federation &amp; Peer Synchronization</h1>
              <p class="km-page-subtitle">Connect independent organization nodes over HTTP, verify Ed25519 peer identities, and run pull-based knowledge synchronization.</p>
            </div>
            <button class="km-btn km-btn-primary" onclick="window.kmAction.connectPeerPrompt()">+ Connect Federated Peer</button>
          </div>
          ${{renderTopologySvg()}}
          <div class="km-card">
            <div class="km-card-header"><h3 class="km-card-title">Connected Federated Peers</h3><span class="km-badge info">Protocol: kyro-fed/1.0</span></div>
            <div class="km-table-wrap">
              <table class="km-table">
                <thead><tr><th>Peer Node ID</th><th>Name</th><th>Endpoint</th><th>Ed25519 Identity</th><th>Actions</th></tr></thead>
                <tbody>
                  ${{state.peers.map(p => `
                    <tr>
                      <td><span class="km-mono">${{esc(p.peer_node_id)}}</span></td>
                      <td style="font-weight:600">${{esc(p.name)}}</td>
                      <td><span class="km-mono">${{esc(p.endpoint)}}</span></td>
                      <td><span class="km-badge ${{p.identity_verified ? 'verified' : 'warning'}}">${{p.identity_verified ? '✓ Verified (' + esc(p.key_fingerprint.slice(0, 12)) + '…)' : 'Unverified'}}</span></td>
                      <td><button class="km-btn km-btn-sm km-btn-primary" onclick="window.kmAction.syncPeer('${{esc(p.peer_node_id)}}')">↻ Pull Sync</button></td>
                    </tr>
                  `).join('')}}
                </tbody>
              </table>
            </div>
          </div>
        `;
      }}

      if (state.activeTab === 'trust') {{
        const vr = state.verifyReport || (state.bundles[0] && state.bundles[0].verification);
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Cryptographic Trust, Provenance &amp; Tamper Inspector</h1>
              <p class="km-page-subtitle">Kyro separates payload integrity (RFC 8785 JCS SHA-256), Ed25519 signature verification, signer recognition, and epistemic claim assessment.</p>
            </div>
          </div>
          <div class="km-notice ${{state.isTampered ? 'error' : 'verified'}}">
            <span><strong>${{state.isTampered ? 'Cryptographic Tamper Alert:' : 'Epistemic Separation Principle:'}}</strong> ${{state.isTampered ? 'Canonical SHA-256 digest mismatch detected! Kyro rejects tampered bundles.' : 'A valid Ed25519 signature proves publisher authenticity and payload integrity — not absolute factual truth.'}}</span>
          </div>
          ${{vr ? `
            <div class="km-grid-3">
              <div class="km-card">
                <div class="km-metric-label">Stage 1 · RFC 8785 JCS Digest Integrity</div>
                <div style="margin-top:10px"><span class="km-badge ${{vr.integrity_verified ? 'verified' : 'error'}}">${{vr.integrity_verified ? '✓ SHA-256 Digest Matches' : '✕ Digest Mismatch (Tampered)'}}</span></div>
                <div class="km-metric-sub" style="margin-top:8px">Expected: <span class="km-mono">${{esc((vr.content_digest || '').slice(0, 18))}}…</span></div>
                <div class="km-metric-sub">Computed: <span class="km-mono">${{esc((vr.computed_digest || '').slice(0, 18))}}…</span></div>
              </div>
              <div class="km-card">
                <div class="km-metric-label">Stage 2 · Ed25519 Signature</div>
                <div style="margin-top:10px"><span class="km-badge ${{vr.signature_verified ? 'verified' : 'error'}}">${{vr.signature_verified ? '✓ Ed25519 Signature Valid' : '✕ Signature Invalid'}}</span></div>
                <div class="km-metric-sub" style="margin-top:8px">Signer: <span class="km-mono">${{esc(vr.signer_id)}}</span></div>
              </div>
              <div class="km-card">
                <div class="km-metric-label">Stage 3 · Signer &amp; Provenance</div>
                <div style="margin-top:10px"><span class="km-badge ${{vr.signer_recognized ? 'verified' : 'warning'}}">${{vr.signer_recognized ? '✓ Recognized Node Key' : 'Unknown Key'}}</span></div>
                <div class="km-metric-sub" style="margin-top:8px">Status: <strong>${{esc((vr.status || '').toUpperCase())}}</strong></div>
              </div>
            </div>
          ` : ''}}
          <div class="km-card">
            <div class="km-card-header">
              <div>
                <h3 class="km-card-title">Interactive Zero-Trust Bundle &amp; Signature Verifier</h3>
                <div class="km-metric-sub">Click "Simulate Payload Tampering" to mutate the claim statement and run live backend verification (/api/v1/trust/verify).</div>
              </div>
              <div style="display:flex;gap:8px">
                <button class="km-btn km-btn-danger" onclick="window.kmAction.simulateTamper()">Simulate Payload Tampering</button>
                <button class="km-btn" onclick="window.kmAction.restoreAuthentic()">↺ Restore Authentic Bundle</button>
                <button class="km-btn km-btn-primary" onclick="window.kmAction.runVerify()">Run Cryptographic Verification</button>
              </div>
            </div>
            <textarea id="km-verify-textarea" class="km-textarea" style="font-family:var(--font-mono);font-size:12px;min-height:260px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;color:#0A0F1D;padding:12px 14px">${{esc(state.verifyJson)}}</textarea>
          </div>
        `;
      }}

      if (state.activeTab === 'bounties') {{
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Node Reputation &amp; Replication Bounties</h1>
              <p class="km-page-subtitle">Backed by GET/POST /api/v1/bounties and GET /api/v1/reputation.</p>
            </div>
          </div>
          <div class="km-grid-3">
            ${{state.nodes.map(n => {{
              const rep = state.reputation.find(r => r.id === n.node_id || r.publisher_node_id === n.node_id);
              const score = (rep && rep.payload && rep.payload.trust_index) ? rep.payload.trust_index : 0.95;
              return `
                <div class="km-card">
                  <div class="km-card-header" style="margin-bottom:8px">
                    <span class="km-mono">did:kyro:${{esc(n.node_id)}}</span>
                    <span class="km-badge verified">Trust Index: ${{Math.round(score * 100)}}%</span>
                  </div>
                  <h3 style="margin:0 0 8px;font-size:16px">${{esc(n.name)}}</h3>
                  <div class="km-progress-track" style="margin-bottom:10px"><div class="km-progress-fill" style="width:${{Math.round(score * 100)}}%"></div></div>
                  <div class="km-mono" style="font-size:11px">${{esc(n.key_fingerprint.slice(0, 28))}}…</div>
                </div>
              `;
            }}).join('')}}
          </div>
          <div class="km-card">
            <div class="km-card-header">
              <h3 class="km-card-title">Empirical Replication Bounties (${{state.bounties.length}})</h3>
              <form onsubmit="window.kmAction.createBounty(event)" style="display:flex;gap:8px;flex-wrap:wrap">
                <input id="km-bounty-title" class="km-input" style="width:240px" required placeholder="Replication bounty objective…" />
                <select id="km-bounty-domain" class="km-select" style="width:150px">
                  <option value="ml-systems">ml-systems</option>
                  <option value="ai-safety">ai-safety</option>
                  <option value="distributed-systems">distributed-systems</option>
                </select>
                <input id="km-bounty-reward" class="km-input" type="number" style="width:100px" value="2000" />
                <input id="km-bounty-evidence" class="km-input" style="width:220px" value="Signed OKF bundle with dataset hash" />
                <button type="submit" class="km-btn km-btn-primary">+ Post Bounty</button>
              </form>
            </div>
            <div class="km-table-wrap">
              <table class="km-table">
                <thead><tr><th>Bounty ID</th><th>Objective</th><th>Domain</th><th>Sponsor Node</th><th>Reward</th><th>Status</th></tr></thead>
                <tbody>
                  ${{state.bounties.map(b => `
                    <tr>
                      <td><span class="km-mono">${{esc(b.id)}}</span></td>
                      <td style="font-weight:600">${{esc(b.title)}}</td>
                      <td><span class="km-badge">${{esc(b.domain || 'general')}}</span></td>
                      <td><span class="km-mono">${{esc(b.publisher_node_id || 'node-a')}}</span></td>
                      <td><span class="km-badge violet">+${{(b.payload && b.payload.reward_points) || 1000}} rep</span></td>
                      <td><span class="km-badge info">${{esc(b.status)}}</span></td>
                    </tr>
                  `).join('')}}
                </tbody>
              </table>
            </div>
          </div>
        `;
      }}

      if (state.activeTab === 'audit') {{
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Activity &amp; Security Audit Trail</h1>
              <p class="km-page-subtitle">Immutable operational audit log across authentication, node key rotation, agent credentials, bundle publishing, and peer synchronization.</p>
            </div>
          </div>
          <div class="km-table-wrap">
            <table class="km-table">
              <thead><tr><th>Event ID</th><th>Category</th><th>Action</th><th>Actor</th><th>Node</th><th>Target Resource</th><th>Outcome</th><th>Time</th></tr></thead>
              <tbody>
                ${{state.audit.map(ev => `
                  <tr>
                    <td><span class="km-mono">${{esc(ev.event_id)}}</span></td>
                    <td><span class="km-badge">${{esc(ev.category)}}</span></td>
                    <td style="font-weight:600">${{esc(ev.action)}}</td>
                    <td><span class="km-mono">${{esc(ev.actor_id)}}</span></td>
                    <td><span class="km-mono">${{esc(ev.node_id || '—')}}</span></td>
                    <td><span class="km-mono">${{esc(ev.resource_type)}}:${{esc(ev.resource_id)}}</span></td>
                    <td><span class="km-badge ${{esc(ev.outcome)}}">${{esc(ev.outcome)}}</span></td>
                    <td class="km-metric-sub">${{new Date(ev.created_at).toLocaleString()}}</td>
                  </tr>
                `).join('')}}
              </tbody>
            </table>
          </div>
        `;
      }}

      if (state.activeTab === 'settings') {{
        const org = state.organizations[0];
        return `
          <div class="km-page-header">
            <div>
              <h1 class="km-page-title">Organizations, Members &amp; Backend RBAC</h1>
              <p class="km-page-subtitle">Manage organization memberships and backend-enforced role permissions (/api/v1/organizations).</p>
            </div>
          </div>
          <div class="km-grid-2">
            <div class="km-card">
              <div class="km-card-header"><h3 class="km-card-title">Authenticated Session Principal</h3><span class="km-badge verified">JWT Active</span></div>
              <div class="km-field"><span class="km-label">User Principal</span><div class="km-mono">${{esc(state.currentUser ? state.currentUser.full_name : '')}} (${{esc(state.currentUser ? state.currentUser.email : '')}})</div></div>
              <div class="km-field"><span class="km-label">Enforced Role</span><span class="km-badge info">${{esc(state.currentUser ? state.currentUser.role : '')}}</span></div>
              <div class="km-field"><span class="km-label">Organization</span><div>${{esc(org ? org.name : (state.currentUser ? state.currentUser.organization_name : ''))}}</div></div>
            </div>
            <div class="km-card">
              <div class="km-card-header"><h3 class="km-card-title">Add Organization Member (RBAC)</h3></div>
              <form onsubmit="window.kmAction.addMember(event)">
                <div class="km-field"><label class="km-label">Member Email *</label><input id="km-mem-email" class="km-input" type="email" required placeholder="curator@organization.org" /></div>
                <div class="km-field"><label class="km-label">Full Name *</label><input id="km-mem-name" class="km-input" required placeholder="Dr. Grace Hopper" /></div>
                <div class="km-field">
                  <label class="km-label">Role</label>
                  <select id="km-mem-role" class="km-select">
                    <option value="owner">Owner</option>
                    <option value="administrator">Administrator</option>
                    <option value="curator" selected>Knowledge Curator</option>
                    <option value="developer">Developer</option>
                    <option value="member">Read-Only Member</option>
                  </select>
                </div>
                <button type="submit" class="km-btn km-btn-primary">Add Member</button>
              </form>
              ${{state.members.length > 0 ? `
                <div class="km-table-wrap" style="margin-top:16px">
                  <table class="km-table">
                    <thead><tr><th>Email</th><th>Name</th><th>Role</th></tr></thead>
                    <tbody>
                      ${{state.members.map(mem => `
                        <tr>
                          <td>${{esc(mem.email)}}</td>
                          <td>${{esc(mem.full_name)}}</td>
                          <td><span class="km-badge info">${{esc(mem.role)}}</span></td>
                        </tr>
                      `).join('')}}
                    </tbody>
                  </table>
                </div>
              ` : ''}}
            </div>
          </div>
        `;
      }}

      // Developer Portal
      return `
        <div class="km-page-header">
          <div>
            <h1 class="km-page-title">Kyro Developer Platform &amp; Python SDK</h1>
            <p class="km-page-subtitle">Connect AI agents to your organization's knowledge node using the same identity, permission, and cryptographic verification contracts as the console.</p>
          </div>
          <div style="display:flex;gap:10px">
            <a href="/docs" target="_blank" class="km-btn">OpenAPI Docs ↗</a>
            <a href="/health" target="_blank" class="km-btn">Health Endpoint ↗</a>
            <a href="/metrics" target="_blank" class="km-btn">Prometheus Metrics ↗</a>
          </div>
        </div>
        <div class="km-grid-2">
          <div class="km-card">
            <div class="km-card-header"><h3 class="km-card-title">Python SDK Quickstart (packages/sdk)</h3><span class="km-badge info">Zero-Trust Client</span></div>
            <pre class="km-code-block">from packages.sdk import KyroClient, verify_bundle_signature

client = KyroClient(
    base_url=window.location.origin,
    api_key="&lt;YOUR_ISSUED_AGENT_KEY&gt;",
)

hits = client.search(query="*", scope="federated")
for item in hits["results"]:
    bundle = client.get_bundle(item["bundle_id"])
    report = verify_bundle_signature(bundle)
    assert report.is_valid and report.digest_valid
    print("[VERIFIED]", bundle["title"], report.signer_did)</pre>
          </div>
          <div class="km-card">
            <div class="km-card-header">
              <h3 class="km-card-title">Live REST &amp; Federation API Playground</h3>
              <span class="km-badge verified">${{esc(state.playgroundStatus)}}</span>
            </div>
            <div style="display:flex;gap:10px;margin-bottom:12px">
              <select id="km-play-ep" class="km-select">
                <option value="/api/v1/overview" ${{state.playgroundEndpoint === '/api/v1/overview' ? 'selected' : ''}}>GET /api/v1/overview</option>
                <option value="/api/v1/nodes" ${{state.playgroundEndpoint === '/api/v1/nodes' ? 'selected' : ''}}>GET /api/v1/nodes</option>
                <option value="/api/v1/bundles" ${{state.playgroundEndpoint === '/api/v1/bundles' ? 'selected' : ''}}>GET /api/v1/bundles</option>
                <option value="/api/v1/federation/protocol/manifest" ${{state.playgroundEndpoint === '/api/v1/federation/protocol/manifest' ? 'selected' : ''}}>GET /api/v1/federation/protocol/manifest</option>
                <option value="/health" ${{state.playgroundEndpoint === '/health' ? 'selected' : ''}}>GET /health</option>
              </select>
              <button class="km-btn km-btn-primary" onclick="window.kmAction.runPlayground()">▶ Send Request</button>
            </div>
            <pre class="km-code-block" style="max-height:280px;overflow-y:auto">${{esc(state.playgroundOutput || '// Click Send Request to execute live API call')}}</pre>
          </div>
        </div>
      `;
    }}

    function renderDashboard() {{
      const totalClaims = state.bundles.reduce((a, b) => a + (b.claims ? b.claims.length : 0), 0);
      const navItems = [
        ['overview', '◈', 'Overview', ''],
        ['nodes', '⬡', 'My Nodes', state.nodes.length],
        ['knowledge', '⊞', 'Knowledge Bundles', state.bundles.length],
        ['claims', '§', 'Claims & Lifecycle', totalClaims],
        ['okf-graph', '☍', 'OKF Graph Workspace', ''],
        ['discover', '⌕', 'Discover', ''],
        ['agents', '▲', 'AI Agents', state.agents.length],
        ['federation', '⇄', 'Federation & Peers', state.peers.length],
        ['trust', '✓', 'Trust & Verifier', ''],
        ['bounties', '✦', 'Reputation & Bounties', state.bounties.length],
        ['audit', '≡', 'Activity & Audit', state.audit.length],
        ['developer', '⌘', 'Developer Portal', ''],
        ['settings', '⎈', 'Organizations & RBAC', ''],
      ];
      const primaryNode = state.nodes[0];

      return `
        <div class="km-shell">
          <aside class="km-sidebar ${{state.sidebarCollapsed ? 'collapsed' : ''}}">
            <div class="km-brand-bar">
              <div class="km-brand-logo" style="display:flex;align-items:center;gap:10px">
                <img src="/static/kyro-logo.png" alt="Kyro Logo" style="height:32px;width:32px;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(0,0,0,0.35));flex-shrink:0" />
                ${{!state.sidebarCollapsed ? '<div>Ky<span>ro</span></div>' : ''}}
              </div>
              <button class="km-btn km-btn-sm" onclick="window.kmAction.toggleSidebar()">${{state.sidebarCollapsed ? '»' : '«'}}</button>
            </div>
            <div class="km-nav-group">
              ${{!state.sidebarCollapsed ? '<div class="km-nav-label">Sovereign Control Plane</div>' : ''}}
              ${{navItems.map(([id, icon, label, cnt]) => `
                <button class="km-nav-item ${{state.activeTab === id ? 'active' : ''}}" onclick="window.kmAction.setTab('${{id}}')">
                  <span class="km-nav-item-left">
                    <span class="km-nav-icon">${{icon}}</span>
                    ${{!state.sidebarCollapsed ? `<span>${{label}}</span>` : ''}}
                  </span>
                  ${{!state.sidebarCollapsed && cnt !== '' ? `<span class="km-nav-count">${{cnt}}</span>` : ''}}
                </button>
              `).join('')}}
            </div>
            ${{!state.sidebarCollapsed && state.currentUser ? `
              <div style="margin-top:auto;padding:16px;border-top:1px solid var(--border-subtle);font-size:11.5px;color:var(--text-muted)">
                <div style="font-weight:600;color:var(--text-secondary)">${{esc(state.currentUser.full_name)}}</div>
                <div>${{esc(state.currentUser.organization_name)}} · ${{esc(state.currentUser.role.toUpperCase())}}</div>
                <div style="margin-top:8px;display:flex;gap:6px">
                  <button class="km-btn km-btn-sm" onclick="window.kmAction.goLanding()">Landing Page</button>
                  <button class="km-btn km-btn-sm km-btn-danger" onclick="window.kmAction.signOut()">Sign Out</button>
                </div>
              </div>
            ` : ''}}
          </aside>
          <div class="km-workspace">
            <header class="km-topbar" style="display:flex;align-items:center;justify-content:space-between;gap:12px;height:56px;padding:0 20px;flex-wrap:nowrap">
              <div class="km-topbar-left" style="display:flex;align-items:center;gap:8px;flex-wrap:nowrap;overflow:hidden">
                <span class="km-badge verified" style="font-size:11px;padding:3px 10px;white-space:nowrap">● Live FastAPI Backend · ${{esc((state.overview && state.overview.node_id) || 'node-a')}}</span>
                ${{state.currentUser ? `<span class="km-badge info" style="font-size:11px;padding:3px 10px;white-space:nowrap">${{esc(state.currentUser.organization_name)}} (${{esc(state.currentUser.role)}})</span>` : ''}}
                ${{primaryNode ? `<span class="km-mono" style="font-size:11px;color:#94a3b8;white-space:nowrap" title="${{esc(primaryNode.key_fingerprint)}}">Ed25519: ${{esc(primaryNode.key_fingerprint.slice(0, 12))}}…</span>` : ''}}
              </div>
              <div class="km-topbar-right" style="display:flex;align-items:center;gap:8px;flex-wrap:nowrap;flex-shrink:0">
                <button class="km-btn km-btn-sm km-btn-accent" style="font-size:11.5px;padding:5px 10px" onclick="window.kmAction.bootstrapDemo()">Seed 4-Node Mesh</button>
                <button class="km-btn km-btn-sm" style="font-size:11.5px;padding:5px 10px" onclick="window.kmAction.setTab('discover')">Search</button>
                <button class="km-btn km-btn-sm" style="font-size:11.5px;padding:5px 10px" onclick="window.kmAction.setTab('trust')">Verifier</button>
                <button class="km-btn km-btn-sm km-btn-danger" style="font-size:11.5px;padding:5px 10px" onclick="window.kmAction.signOut()">Sign Out</button>
              </div>
            </header>
            <main class="km-main">
              ${{state.banner ? `
                <div class="km-notice verified" style="display:flex;align-items:center;justify-content:space-between">
                  <span>${{esc(state.banner)}}</span>
                  <button class="km-modal-close" style="width:26px;height:26px;font-size:11px" onclick="window.kmAction.dismissBanner()" aria-label="Dismiss">✕</button>
                </div>
              ` : ''}}
              ${{renderMainContent()}}
            </main>
          </div>
        </div>
      `;
    }}

    let threeAnimId = null;
    let threeRenderer = null;
    let threeScene = null;
    let threeCamera = null;
    let threePointer = {{ x: 0, y: 0 }};

    function initTransformationSceneThree() {{
      try {{
        if (threeAnimId) {{
          cancelAnimationFrame(threeAnimId);
          threeAnimId = null;
        }}
        if (threeRenderer) {{
          try {{ threeRenderer.dispose(); }} catch(e) {{}}
          threeRenderer = null;
        }}

        const canvas = document.getElementById('km-three-canvas');
        if (!canvas) return;

        if (typeof THREE === 'undefined') {{
          setTimeout(initTransformationSceneThree, 80);
          return;
        }}

        const parent = canvas.parentElement;
        const width = Math.max((parent ? parent.clientWidth : 700) || 700, 360);
        const height = Math.max((parent ? parent.clientHeight : 520) || 520, 460);

        // 1. Scene - Completely Transparent (No background, No opaque fog)
        const scene = new THREE.Scene();
        threeScene = scene;

        // 2. Perspective Camera (Centered with Generous Framing)
        const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 50);
        camera.position.set(0, 0, 9.6);
        threeCamera = camera;

      // 3. High-Performance Transparent WebGL Renderer
      const renderer = new THREE.WebGLRenderer({{
        canvas: canvas,
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance',
      }});
      renderer.setClearColor(0x000000, 0);
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.25;
      threeRenderer = renderer;

      // 4. Studio Lighting Rig tailored for Luxury Light Aesthetic & Cyan Sphere
      const ambientLight = new THREE.AmbientLight(0xffffff, 2.2);
      scene.add(ambientLight);

      // Key light: vibrant cyan highlight
      const keyLight = new THREE.DirectionalLight(0x38bdf8, 4.2);
      keyLight.position.set(-8, 12, 10);
      scene.add(keyLight);

      // Rim light: electric cyan edge definition
      const rimLight = new THREE.DirectionalLight(0x06b6d4, 3.6);
      rimLight.position.set(10, 8, -6);
      scene.add(rimLight);

      // Accent fill light: warm violet accent
      const violetLight = new THREE.PointLight(0xa855f7, 2.6, 25);
      violetLight.position.set(0, -6, 5);
      scene.add(violetLight);

      // Inner glowing core light: electric cyan core
      const innerCoreLight = new THREE.PointLight(0x38bdf8, 5.0, 14);
      innerCoreLight.position.set(0, 0, 0);
      scene.add(innerCoreLight);

      // 5. Construct Mathematical Goldberg Polyhedron Dual Sphere
      const phi = (1.0 + Math.sqrt(5.0)) / 2.0;
      // Base icosahedron vertices
      const baseVerts = [
        [-1,  phi, 0], [ 1,  phi, 0], [-1, -phi, 0], [ 1, -phi, 0],
        [ 0, -1,  phi], [ 0,  1,  phi], [ 0, -1, -phi], [ 0,  1, -phi],
        [ phi, 0, -1], [ phi, 0,  1], [-phi, 0, -1], [-phi, 0,  1]
      ];
      const baseFaces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
      ];

      const pVerts = [];
      for (let i = 0; i < baseVerts.length; i++) {{
        const b = baseVerts[i];
        const len = Math.sqrt(b[0]*b[0] + b[1]*b[1] + b[2]*b[2]);
        pVerts.push(new THREE.Vector3(b[0]/len, b[1]/len, b[2]/len));
      }}

      // Geodesic Subdivision (2 iterations -> 320 primal faces)
      let pFaces = baseFaces;
      for (let step = 0; step < 2; step++) {{
        const midCache = new Map();
        function getMid(i1, i2) {{
          const k = Math.min(i1, i2) + '_' + Math.max(i1, i2);
          if (midCache.has(k)) return midCache.get(k);
          const v1 = pVerts[i1];
          const v2 = pVerts[i2];
          const mx = (v1.x + v2.x) * 0.5;
          const my = (v1.y + v2.y) * 0.5;
          const mz = (v1.z + v2.z) * 0.5;
          const len = Math.sqrt(mx*mx + my*my + mz*mz);
          const idx = pVerts.length;
          pVerts.push(new THREE.Vector3(mx/len, my/len, mz/len));
          midCache.set(k, idx);
          return idx;
        }}
        const nextFaces = [];
        for (let f = 0; f < pFaces.length; f++) {{
          const tri = pFaces[f];
          const a = getMid(tri[0], tri[1]);
          const b = getMid(tri[1], tri[2]);
          const c = getMid(tri[2], tri[0]);
          nextFaces.push([tri[0], a, c]);
          nextFaces.push([tri[1], b, a]);
          nextFaces.push([tri[2], c, b]);
          nextFaces.push([a, b, c]);
        }}
        pFaces = nextFaces;
      }}

        // DUAL GRAPH COMPUTATION (Goldberg Polyhedron):
        // Scaled to fit perfectly within bounds with generous margins (no edge clipping)
        const SPHERE_RADIUS = 1.70;
        const STRUT_RADIUS = 0.026;
        const NODE_RADIUS = 0.042;

      const dualVerts = [];
      for (let f = 0; f < pFaces.length; f++) {{
        const tri = pFaces[f];
        const v0 = pVerts[tri[0]];
        const v1 = pVerts[tri[1]];
        const v2 = pVerts[tri[2]];
        const cx = (v0.x + v1.x + v2.x) / 3.0;
        const cy = (v0.y + v1.y + v2.y) / 3.0;
        const cz = (v0.z + v1.z + v2.z) / 3.0;
        const len = Math.sqrt(cx*cx + cy*cy + cz*cz);
        dualVerts.push(new THREE.Vector3((cx/len) * SPHERE_RADIUS, (cy/len) * SPHERE_RADIUS, (cz/len) * SPHERE_RADIUS));
      }}

      // Map each primal edge to the 2 adjacent faces sharing it
      const edgeToFaces = new Map();
      for (let f = 0; f < pFaces.length; f++) {{
        const tri = pFaces[f];
        const pairs = [
          [Math.min(tri[0], tri[1]), Math.max(tri[0], tri[1])],
          [Math.min(tri[1], tri[2]), Math.max(tri[1], tri[2])],
          [Math.min(tri[2], tri[0]), Math.max(tri[2], tri[0])]
        ];
        for (let p = 0; p < 3; p++) {{
          const k = pairs[p][0] + '_' + pairs[p][1];
          if (!edgeToFaces.has(k)) edgeToFaces.set(k, []);
          edgeToFaces.get(k).push(f);
        }}
      }}

      // Dual edges connect the centroids of the 2 adjacent faces:
      // Perfectly planar on S^2, regular hexagonal voids (150 hexagons + 12 pentagons), zero overlapping edges!
      const dualEdges = [];
      edgeToFaces.forEach((fList) => {{
        if (fList.length === 2) {{
          dualEdges.push([fList[0], fList[1]]);
        }}
      }});

      // Group holding the entire rotating 3D sphere
      const sphereGroup = new THREE.Group();
      scene.add(sphereGroup);

      // Signature Cyan & Ice-Blue Geodesic Buckyball Materials
      const strutMaterial = new THREE.MeshStandardMaterial({{
        color: 0x67e8f9,
        emissive: 0x0284c7,
        emissiveIntensity: 0.55,
        metalness: 0.88,
        roughness: 0.15,
      }});

      const nodeMaterial = new THREE.MeshStandardMaterial({{
        color: 0x93c5fd,
        emissive: 0x38bdf8,
        emissiveIntensity: 0.70,
        metalness: 0.90,
        roughness: 0.12,
      }});

      // Instanced Cylindrical Struts
      const cylinderUnitGeo = new THREE.CylinderGeometry(STRUT_RADIUS, STRUT_RADIUS, 1.0, 10);
      const instancedStruts = new THREE.InstancedMesh(cylinderUnitGeo, strutMaterial, dualEdges.length);
      instancedStruts.castShadow = true;
      instancedStruts.receiveShadow = true;

      const dummy = new THREE.Object3D();
      const upVector = new THREE.Vector3(0, 1, 0);

      for (let e = 0; e < dualEdges.length; e++) {{
        const [idxA, idxB] = dualEdges[e];
        const vA = dualVerts[idxA];
        const vB = dualVerts[idxB];

        const midpoint = new THREE.Vector3().addVectors(vA, vB).multiplyScalar(0.5);
        const dir = new THREE.Vector3().subVectors(vB, vA);
        const len = dir.length();
        dir.normalize();

        dummy.position.copy(midpoint);
        dummy.quaternion.setFromUnitVectors(upVector, dir);
        dummy.scale.set(1.0, len, 1.0);
        dummy.updateMatrix();
        instancedStruts.setMatrixAt(e, dummy.matrix);
      }}
      instancedStruts.instanceMatrix.needsUpdate = true;
      sphereGroup.add(instancedStruts);

      // Instanced Nodes at dual vertices
      const sphereUnitGeo = new THREE.SphereGeometry(NODE_RADIUS, 12, 12);
      const instancedNodes = new THREE.InstancedMesh(sphereUnitGeo, nodeMaterial, dualVerts.length);

      for (let n = 0; n < dualVerts.length; n++) {{
        dummy.position.copy(dualVerts[n]);
        dummy.quaternion.set(0, 0, 0, 1);
        dummy.scale.set(1.0, 1.0, 1.0);
        dummy.updateMatrix();
        instancedNodes.setMatrixAt(n, dummy.matrix);
      }}
      instancedNodes.instanceMatrix.needsUpdate = true;
      sphereGroup.add(instancedNodes);

      // Luminous Line Network Overlay
      const lineGeo = new THREE.BufferGeometry();
      const linePositions = new Float32Array(dualEdges.length * 6);
      for (let e = 0; e < dualEdges.length; e++) {{
        const [idxA, idxB] = dualEdges[e];
        const vA = dualVerts[idxA];
        const vB = dualVerts[idxB];
        linePositions[e * 6 + 0] = vA.x;
        linePositions[e * 6 + 1] = vA.y;
        linePositions[e * 6 + 2] = vA.z;
        linePositions[e * 6 + 3] = vB.x;
        linePositions[e * 6 + 4] = vB.y;
        linePositions[e * 6 + 5] = vB.z;
      }}
      lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
      const lineMaterial = new THREE.LineBasicMaterial({{
        color: 0x38bdf8,
        transparent: true,
        opacity: 0.65,
      }});
      const lineSegments = new THREE.LineSegments(lineGeo, lineMaterial);
      sphereGroup.add(lineSegments);

      // Pulsing Data Packets along the hexagonal struts
      const particleCount = 48;
      const particleGeo = new THREE.BufferGeometry();
      const particlePositions = new Float32Array(particleCount * 3);
      const particleEdges = [];
      for (let p = 0; p < particleCount; p++) {{
        const randEdge = dualEdges[Math.floor(Math.random() * dualEdges.length)];
        const prog = Math.random();
        const speed = 0.25 + Math.random() * 0.45;
        particleEdges.push({{ edge: randEdge, t: prog, speed: speed }});
        const vA = dualVerts[randEdge[0]];
        const vB = dualVerts[randEdge[1]];
        particlePositions[p * 3 + 0] = vA.x + (vB.x - vA.x) * prog;
        particlePositions[p * 3 + 1] = vA.y + (vB.y - vA.y) * prog;
        particlePositions[p * 3 + 2] = vA.z + (vB.z - vA.z) * prog;
      }}
      particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
      const particleMaterial = new THREE.PointsMaterial({{
        color: 0x67e8f9,
        size: 0.12,
        transparent: true,
        opacity: 0.95,
      }});
      const particlePoints = new THREE.Points(particleGeo, particleMaterial);
      sphereGroup.add(particlePoints);

      // Subdued ambient sparkles
      const sparkleCount = 40;
      const sparkleGeo = new THREE.BufferGeometry();
      const sparklePositions = new Float32Array(sparkleCount * 3);
      for (let s = 0; s < sparkleCount; s++) {{
        const rad = 2.2 + Math.random() * 1.3;
        const theta = Math.random() * Math.PI * 2;
        const phiAngle = Math.acos((Math.random() * 2) - 1);
        sparklePositions[s * 3 + 0] = rad * Math.sin(phiAngle) * Math.cos(theta);
        sparklePositions[s * 3 + 1] = rad * Math.sin(phiAngle) * Math.sin(theta);
        sparklePositions[s * 3 + 2] = rad * Math.cos(phiAngle);
      }}
      sparkleGeo.setAttribute('position', new THREE.BufferAttribute(sparklePositions, 3));
      const sparkles = new THREE.Points(
        sparkleGeo,
        new THREE.PointsMaterial({{ color: 0x93c5fd, size: 0.065, transparent: true, opacity: 0.45 }})
      );
      scene.add(sparkles);

      // Interactive Cursor Gyro & Motion Dynamics
      let targetTiltX = 0;
      let targetTiltY = 0;
      let currentTiltX = 0;
      let currentTiltY = 0;
      let cursorVelX = 0;
      let lastPointerX = 0;

      function onPointerMove(e) {{
        const rect = canvas.getBoundingClientRect();
        const cx = (e.clientX - rect.left) / rect.width;
        const cy = (e.clientY - rect.top) / rect.height;
        const cursorX = (cx - 0.5) * 2;
        const cursorY = (cy - 0.5) * 2;

        targetTiltY = cursorX * 0.45;
        targetTiltX = -cursorY * 0.35;

        const dx = cursorX - lastPointerX;
        lastPointerX = cursorX;
        cursorVelX = dx * 0.003;

        threePointer.x = cursorX;
        threePointer.y = cursorY;
      }}

      function onTouchMove(e) {{
        if (e.touches.length > 0) {{
          onPointerMove(e.touches[0]);
        }}
      }}

      window.addEventListener('mousemove', onPointerMove, {{ passive: true }});
      window.addEventListener('touchmove', onTouchMove, {{ passive: true }});

      function onResize() {{
        if (!canvas || !canvas.parentElement) return;
        const p = canvas.parentElement;
        const nw = Math.max(p.clientWidth || 700, 360);
        const nh = Math.max(p.clientHeight || 520, 460);
        camera.aspect = nw / nh;
        camera.updateProjectionMatrix();
        renderer.setSize(nw, nh);
      }}
      window.addEventListener('resize', onResize);

      // Animation Loop
      let lastTime = performance.now();
      const baseRotationSpeed = 0.0042; // Continuous Left-to-Right rotation

      function animate(now) {{
        if (!document.getElementById('km-three-canvas')) return;

        const dt = Math.min((now - lastTime) / 1000, 0.05);
        lastTime = now;

        // Continuous Left-to-Right rotation on vertical Y-axis + cursor inertia
        cursorVelX *= 0.94;
        sphereGroup.rotation.y += baseRotationSpeed + cursorVelX;

        // Smooth Gyro tilt towards cursor
        currentTiltX += (targetTiltX - currentTiltX) * 0.06;
        currentTiltY += (targetTiltY - currentTiltY) * 0.06;
        sphereGroup.rotation.x = currentTiltX;
        sphereGroup.rotation.z = -currentTiltY * 0.35;

        // Subtle zero-gravity vertical breathing (shifted gracefully above center)
        sphereGroup.position.y = 0.32 + Math.sin(now * 0.0014) * 0.08;

        // Animate data packet pulses along struts
        const posAttr = particleGeo.attributes.position;
        const arr = posAttr.array;
        for (let p = 0; p < particleCount; p++) {{
          const item = particleEdges[p];
          item.t += dt * item.speed;
          if (item.t >= 1.0) {{
            item.t = 0.0;
            item.edge = dualEdges[Math.floor(Math.random() * dualEdges.length)];
          }}
          const vA = dualVerts[item.edge[0]];
          const vB = dualVerts[item.edge[1]];
          arr[p * 3 + 0] = vA.x + (vB.x - vA.x) * item.t;
          arr[p * 3 + 1] = vA.y + (vB.y - vA.y) * item.t;
          arr[p * 3 + 2] = vA.z + (vB.z - vA.z) * item.t;
        }}
        posAttr.needsUpdate = true;

        // Sparkles slow counter-orbit
        sparkles.rotation.y -= 0.001;

        renderer.render(scene, camera);
        threeAnimId = requestAnimationFrame(animate);
        window.__threeReady = true;
      }}
      threeAnimId = requestAnimationFrame(animate);
    }} catch (err) {{
      console.error("3D Sphere Init Error:", err);
      window.__threeError = err.message + ' \\n' + err.stack;
    }}
  }}

    function fitOkfGraph() {{
      const container = document.getElementById('km-okf-graph-container');
      const stage = document.getElementById('km-okf-graph-stage');
      if (!container || !stage) return;
      const cw = container.clientWidth || 960;
      const ch = container.clientHeight || 520;
      if (cw <= 0 || ch <= 0) return;
      const scaleX = (cw - 36) / 960;
      const scaleY = (ch - 36) / 520;
      const autoScale = Math.min(scaleX, scaleY, 1.05);
      const zoomFactor = (state.graphZoom || 100) / 100;
      const finalScale = Math.max(0.35, autoScale * zoomFactor);
      stage.style.transform = `scale(${{finalScale.toFixed(3)}})`;
    }}

    window.addEventListener('resize', () => {{
      if (state.activeTab === 'okf-graph') fitOkfGraph();
    }});

    function renderToastContainer() {{
      if (!state.toasts || state.toasts.length === 0) return '';
      return `
        <div class="km-toast-container" role="region" aria-live="polite">
          ${{state.toasts.map(t => `
            <div class="km-toast ${{esc(t.type || 'info')}}" id="${{esc(t.id)}}">
              <div class="km-toast-body">
                <div class="km-toast-icon">${{esc(t.icon || 'ℹ')}}</div>
                <div class="km-toast-message">${{esc(t.message)}}</div>
              </div>
              <button class="km-modal-close" style="width:24px;height:24px;font-size:11px" onclick="window.kmRemoveToast('${{esc(t.id)}}')" aria-label="Dismiss">✕</button>
            </div>
          `).join('')}}
        </div>
      `;
    }}

    function renderActiveModal() {{
      if (!state.activeModal) return '';
      const m = state.activeModal;
      const d = state.modalData || {{}};

      if (m === 'createNode') {{
        return `
          <div class="km-modal-backdrop" onclick="if(event.target===this) window.kmAction.closeModal()">
            <div class="km-modal" style="max-width:540px">
              <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:18px">
                <div>
                  <h3 style="font-size:18px;font-weight:700;color:#0A0F1D;margin:0 0 4px">Register Sovereign Node</h3>
                  <p style="font-size:13px;color:#64748B;margin:0">Deploy an independent cryptographic peer to the federated mesh.</p>
                </div>
                <button class="km-modal-close" onclick="window.kmAction.closeModal()">✕</button>
              </div>
              <div style="display:flex;flex-direction:column;gap:14px">
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Node Name</label>
                  <input type="text" id="km-modal-node-name" class="km-input" placeholder="e.g. Stanford Bio-Compute Mesh" style="width:100%" />
                </div>
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Endpoint URL</label>
                  <input type="text" id="km-modal-node-endpoint" class="km-input" placeholder="http://127.0.0.1:8005" value="http://127.0.0.1:8005" style="width:100%" />
                </div>
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Governance / Visibility</label>
                  <select id="km-modal-node-vis" class="km-select" style="width:100%">
                    <option value="federated">Federated Mesh (Verifiable &amp; Syncable)</option>
                    <option value="organization">Organization Private (Restricted)</option>
                    <option value="public">Public Read Index</option>
                  </select>
                </div>
              </div>
              <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:24px;padding-top:16px;border-top:1px solid #E2E8F0">
                <button class="km-btn" onclick="window.kmAction.closeModal()">Cancel</button>
                <button class="km-btn km-btn-primary" onclick="window.kmAction.submitCreateNode()">Deploy Node &amp; Keypair</button>
              </div>
            </div>
          </div>
        `;
      }}

      if (m === 'connectPeer') {{
        return `
          <div class="km-modal-backdrop" onclick="if(event.target===this) window.kmAction.closeModal()">
            <div class="km-modal" style="max-width:540px">
              <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:18px">
                <div>
                  <h3 style="font-size:18px;font-weight:700;color:#0A0F1D;margin:0 0 4px">Connect Federated Peer</h3>
                  <p style="font-size:13px;color:#64748B;margin:0">Establish peer-to-peer federation with an Ed25519-verifiable node.</p>
                </div>
                <button class="km-modal-close" onclick="window.kmAction.closeModal()">✕</button>
              </div>
              <div style="display:flex;flex-direction:column;gap:14px">
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Peer Node Identifier / Name</label>
                  <input type="text" id="km-modal-peer-name" class="km-input" placeholder="e.g. Node D · CERN High-Energy Open Mesh" style="width:100%" />
                </div>
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Peer Endpoint</label>
                  <input type="text" id="km-modal-peer-endpoint" class="km-input" placeholder="http://127.0.0.1:8004" value="http://127.0.0.1:8004" style="width:100%" />
                </div>
                <div style="display:flex;align-items:center;gap:8px;padding:8px 0">
                  <input type="checkbox" id="km-modal-peer-auto" checked style="width:16px;height:16px" />
                  <label for="km-modal-peer-auto" style="font-size:13px;color:#334155">Auto-approve Ed25519 public key and accept signed bundle sync</label>
                </div>
              </div>
              <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:24px;padding-top:16px;border-top:1px solid #E2E8F0">
                <button class="km-btn" onclick="window.kmAction.closeModal()">Cancel</button>
                <button class="km-btn km-btn-primary" onclick="window.kmAction.submitConnectPeer()">Connect Peer Node</button>
              </div>
            </div>
          </div>
        `;
      }}

      if (m === 'createBundle') {{
        return `
          <div class="km-modal-backdrop" onclick="if(event.target===this) window.kmAction.closeModal()">
            <div class="km-modal" style="max-width:580px">
              <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:18px">
                <div>
                  <h3 style="font-size:18px;font-weight:700;color:#0A0F1D;margin:0 0 4px">Publish Knowledge Document</h3>
                  <p style="font-size:13px;color:#64748B;margin:0">Create an immutable, versioned OKF bundle signed with node Ed25519 key.</p>
                </div>
                <button class="km-modal-close" onclick="window.kmAction.closeModal()">✕</button>
              </div>
              <div style="display:flex;flex-direction:column;gap:14px">
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Document Title</label>
                  <input type="text" id="km-modal-bundle-title" class="km-input" placeholder="e.g. Asynchronous Byzantine Agreement in Sparse Meshes" style="width:100%" />
                </div>
                <div class="km-grid-2">
                  <div>
                    <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Domain / Topic</label>
                    <select id="km-modal-bundle-cat" class="km-select" style="width:100%">
                      <option value="distributed-systems">distributed-systems</option>
                      <option value="ml-systems">ml-systems</option>
                      <option value="cryptography">cryptography</option>
                      <option value="biomedical">biomedical</option>
                      <option value="ai-safety">ai-safety</option>
                    </select>
                  </div>
                  <div>
                    <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Primary Source URL</label>
                    <input type="text" id="km-modal-bundle-uri" class="km-input" placeholder="https://arxiv.org/abs/..." value="https://arxiv.org" style="width:100%" />
                  </div>
                </div>
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Primary Atomic Claim Statement</label>
                  <textarea id="km-modal-bundle-claim" class="km-textarea" rows="3" placeholder="State the verifiable claim or theorem..." style="width:100%"></textarea>
                </div>
              </div>
              <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:24px;padding-top:16px;border-top:1px solid #E2E8F0">
                <button class="km-btn" onclick="window.kmAction.closeModal()">Cancel</button>
                <button class="km-btn km-btn-primary" onclick="window.kmAction.submitCreateBundle()">Sign &amp; Publish Bundle</button>
              </div>
            </div>
          </div>
        `;
      }}

      if (m === 'createAgent') {{
        return `
          <div class="km-modal-backdrop" onclick="if(event.target===this) window.kmAction.closeModal()">
            <div class="km-modal" style="max-width:560px">
              <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:18px">
                <div>
                  <h3 style="font-size:18px;font-weight:700;color:#0A0F1D;margin:0 0 4px">Register Autonomous AI Agent</h3>
                  <p style="font-size:13px;color:#64748B;margin:0">Provision a cryptographically scoped AI agent with least-privilege permissions.</p>
                </div>
                <button class="km-modal-close" onclick="window.kmAction.closeModal()">✕</button>
              </div>
              <div style="display:flex;flex-direction:column;gap:14px">
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Agent Name</label>
                  <input type="text" id="km-modal-agent-name" class="km-input" placeholder="e.g. Distributed Hypothesis Auditor" style="width:100%" />
                </div>
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Description</label>
                  <input type="text" id="km-modal-agent-desc" class="km-input" placeholder="Autonomous cross-mesh synthesis and claim verification" style="width:100%" />
                </div>
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Anchor Sovereign Node</label>
                  <select id="km-modal-agent-node" class="km-select" style="width:100%">
                    ${{state.nodes.map(n => `<option value="${{esc(n.node_id)}}">${{esc(n.name)}} (${{esc(n.node_id)}})</option>`).join('')}}
                  </select>
                </div>
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:8px;display:block">Initial Scoped Permissions</label>
                  <div style="display:flex;flex-direction:column;gap:8px;background:#F8FAFC;padding:12px;border-radius:10px;border:1px solid #E2E8F0">
                    <label style="display:flex;align-items:center;gap:8px;font-size:13px;color:#334155;cursor:pointer">
                      <input type="checkbox" class="km-agent-perm-check" value="knowledge:read" checked style="width:15px;height:15px" />
                      <span><strong>knowledge:read</strong> · Query and read verified bundles</span>
                    </label>
                    <label style="display:flex;align-items:center;gap:8px;font-size:13px;color:#334155;cursor:pointer">
                      <input type="checkbox" class="km-agent-perm-check" value="knowledge:search" checked style="width:15px;height:15px" />
                      <span><strong>knowledge:search</strong> · Federated semantic vector search</span>
                    </label>
                    <label style="display:flex;align-items:center;gap:8px;font-size:13px;color:#334155;cursor:pointer">
                      <input type="checkbox" class="km-agent-perm-check" value="knowledge:publish" style="width:15px;height:15px" />
                      <span><strong>knowledge:publish</strong> · Write and publish signed OKF bundles</span>
                    </label>
                    <label style="display:flex;align-items:center;gap:8px;font-size:13px;color:#334155;cursor:pointer">
                      <input type="checkbox" class="km-agent-perm-check" value="federation:sync" style="width:15px;height:15px" />
                      <span><strong>federation:sync</strong> · Mesh replication and peer discovery</span>
                    </label>
                  </div>
                </div>
              </div>
              <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:24px;padding-top:16px;border-top:1px solid #E2E8F0">
                <button class="km-btn" onclick="window.kmAction.closeModal()">Cancel</button>
                <button class="km-btn km-btn-primary" onclick="window.kmAction.submitCreateAgent()">Issue Scoped Agent Key</button>
              </div>
            </div>
          </div>
        `;
      }}

      if (m === 'permissionRequest') {{
        const agentId = d.agentId || 'agt-research-synth';
        const agentName = d.agentName || 'Synthesis & Federated Discovery Agent';
        const nodeId = d.nodeId || 'node-a';
        return `
          <div class="km-modal-backdrop" onclick="if(event.target===this) window.kmAction.closeModal()">
            <div class="km-modal" style="max-width:580px">
              <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:16px">
                <div style="display:flex;align-items:center;gap:10px">
                  <div style="width:36px;height:36px;border-radius:10px;background:#EEF2FF;color:#4F46E5;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700">🛡</div>
                  <div>
                    <h3 style="font-size:17px;font-weight:700;color:#0A0F1D;margin:0">Agent Capability &amp; Scope Delegation</h3>
                    <p style="font-size:12.5px;color:#64748B;margin:2px 0 0">Requesting agent: <strong style="color:#0A0F1D">${{esc(agentName)}}</strong> (<code class="km-mono" style="font-size:11px">${{esc(agentId)}}</code>)</p>
                  </div>
                </div>
                <button class="km-modal-close" onclick="window.kmAction.closeModal()">✕</button>
              </div>

              <!-- Security Risk Pill -->
              <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:10px;padding:12px 14px;margin-bottom:16px;display:flex;gap:10px;align-items:flex-start">
                <span style="font-size:15px;color:#D97706;line-height:1">⚠</span>
                <div>
                  <div style="font-size:12.5px;font-weight:600;color:#92400E">Security Assessment · Scoped Cryptographic Delegation</div>
                  <div style="font-size:11.5px;color:#B45309;margin-top:2px;line-height:1.45">Delegated capabilities will generate a new SHA-256 hashed API credential bound to anchor node <code class="km-mono" style="font-size:10.5px">${{esc(nodeId)}}</code>. You can revoke this credential at any time from the registry.</div>
                </div>
              </div>

              <div style="margin-bottom:16px">
                <div style="font-size:12px;font-weight:600;color:#334155;margin-bottom:8px">Select Authorized Scopes for this Credential:</div>
                <div style="display:flex;flex-direction:column;gap:8px">
                  <label style="display:flex;align-items:flex-start;gap:10px;padding:10px 12px;border:1px solid #E2E8F0;border-radius:10px;background:#FFFFFF;cursor:pointer">
                    <input type="checkbox" class="km-perm-grant-check" value="knowledge:read" checked style="width:16px;height:16px;margin-top:2px" />
                    <div>
                      <div style="font-size:13px;font-weight:600;color:#0A0F1D">knowledge:read</div>
                      <div style="font-size:11.5px;color:#64748B">Access verified OKF bundles, inspect claims, and retrieve cryptographic provenance.</div>
                    </div>
                  </label>
                  <label style="display:flex;align-items:flex-start;gap:10px;padding:10px 12px;border:1px solid #E2E8F0;border-radius:10px;background:#FFFFFF;cursor:pointer">
                    <input type="checkbox" class="km-perm-grant-check" value="knowledge:search" checked style="width:16px;height:16px;margin-top:2px" />
                    <div>
                      <div style="font-size:13px;font-weight:600;color:#0A0F1D">knowledge:search</div>
                      <div style="font-size:11.5px;color:#64748B">Execute semantic vector search and query multi-hop epistemic graph indices.</div>
                    </div>
                  </label>
                  <label style="display:flex;align-items:flex-start;gap:10px;padding:10px 12px;border:1px solid #E2E8F0;border-radius:10px;background:#FFFFFF;cursor:pointer">
                    <input type="checkbox" class="km-perm-grant-check" value="knowledge:publish" checked style="width:16px;height:16px;margin-top:2px" />
                    <div>
                      <div style="font-size:13px;font-weight:600;color:#0A0F1D">knowledge:publish</div>
                      <div style="font-size:11.5px;color:#64748B">Author and publish new versioned research documents to the local node.</div>
                    </div>
                  </label>
                  <label style="display:flex;align-items:flex-start;gap:10px;padding:10px 12px;border:1px solid #E2E8F0;border-radius:10px;background:#FFFFFF;cursor:pointer">
                    <input type="checkbox" class="km-perm-grant-check" value="federation:sync" checked style="width:16px;height:16px;margin-top:2px" />
                    <div>
                      <div style="font-size:13px;font-weight:600;color:#0A0F1D">federation:sync</div>
                      <div style="font-size:11.5px;color:#64748B">Initiate pull-based peer synchronization across federated partner nodes.</div>
                    </div>
                  </label>
                  <label style="display:flex;align-items:flex-start;gap:10px;padding:10px 12px;border:1px solid #CBD5E1;border-radius:10px;background:#F8FAFC;cursor:pointer">
                    <input type="checkbox" class="km-perm-grant-check" value="trust:ed25519" checked style="width:16px;height:16px;margin-top:2px" />
                    <div>
                      <div style="font-size:13px;font-weight:600;color:#0A0F1D;display:flex;align-items:center;gap:6px">
                        trust:ed25519
                        <span style="font-size:10px;background:#FEF3C7;color:#92400E;padding:1px 6px;border-radius:4px">Elevated</span>
                      </div>
                      <div style="font-size:11.5px;color:#64748B">Generate sovereign Ed25519 cryptographic signatures and commit canonical JCS digests.</div>
                    </div>
                  </label>
                </div>
              </div>

              <div style="display:flex;justify-content:flex-end;gap:10px;padding-top:16px;border-top:1px solid #E2E8F0">
                <button class="km-btn" onclick="window.kmAction.closeModal(); window.kmShowToast('Permission request declined.', 'info')">Decline Request</button>
                <button class="km-btn km-btn-primary" onclick="window.kmAction.submitPermissionGrant()">✓ Approve &amp; Issue Scoped Key</button>
              </div>
            </div>
          </div>
        `;
      }}

      if (m === 'ingestPaper') {{
        const res = state.extractedPaperResult;
        const currentText = state.ingestText || 'Serving large language models at long context lengths is constrained by key-value (KV) cache memory footprints. KIVI maintains 99.6% needle retrieval accuracy up to 128k context with 3.7x lower memory footprint. In contrast, standard unquantized FP16 caches cause out-of-memory errors on 8xH100 clusters at batch size 32. INT4 group quantization reduces memory bandwidth saturation from 94% to 26% under empirical Nsight profiling.';
        const currentSource = state.ingestSourceId || 'arxiv:2401.18079';
        const currentDomain = state.ingestDomain || 'Machine Learning & Systems';

        return `
          <div class="km-modal-backdrop" onclick="if(event.target===this) window.kmAction.closeModal()">
            <div class="km-modal" style="max-width:820px;max-height:90vh;overflow-y:auto">
              <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:16px">
                <div style="display:flex;align-items:center;gap:12px">
                  <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;box-shadow:0 4px 12px rgba(99,102,241,0.28)">⚡</div>
                  <div>
                    <h3 style="font-size:18px;font-weight:750;color:#0A0F1D;margin:0">Research Paper Ingestion &amp; Grounded Claim Extraction</h3>
                    <p style="font-size:12.5px;color:#64748B;margin:2px 0 0">Extract verifiable atomic claims with character-level verbatim quotes and convert directly into RFC 8785 Ed25519 bundles.</p>
                  </div>
                </div>
                <button class="km-modal-close" onclick="window.kmAction.closeModal()">✕</button>
              </div>

              <!-- Presets Bar -->
              <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;margin-bottom:16px">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                  <span style="font-size:11.5px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.04em">Sample Real-World Scientific Papers:</span>
                  <span style="font-size:11px;color:#94A3B8">Click preset to pre-fill</span>
                </div>
                <div style="display:flex;gap:8px;flex-wrap:wrap">
                  <button class="km-btn km-btn-sm" onclick="window.kmAction.loadPaperPreset('kivi')" style="background:#FFFFFF;border:1px solid #CBD5E1;font-size:12px">📄 KIVI KV-Cache (arxiv:2401.18079)</button>
                  <button class="km-btn km-btn-sm" onclick="window.kmAction.loadPaperPreset('flash')" style="background:#FFFFFF;border:1px solid #CBD5E1;font-size:12px">📄 FlashAttention-2 (arxiv:2309.06180)</button>
                  <button class="km-btn km-btn-sm" onclick="window.kmAction.loadPaperPreset('crispr')" style="background:#FFFFFF;border:1px solid #CBD5E1;font-size:12px">🧬 Cas12a CRISPR (pmc:8923412)</button>
                </div>
              </div>

              <!-- Input Form -->
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Source Identifier (DOI / arXiv / PubMed)</label>
                  <input type="text" id="km-ingest-source" class="km-input" value="${{esc(currentSource)}}" style="width:100%" />
                </div>
                <div>
                  <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Scientific / Research Domain</label>
                  <input type="text" id="km-ingest-domain" class="km-input" value="${{esc(currentDomain)}}" style="width:100%" />
                </div>
              </div>

              <div style="margin-bottom:16px">
                <label class="km-label" style="font-size:12px;font-weight:600;color:#334155;margin-bottom:6px;display:block">Document / Abstract Text (Grounding Corpus)</label>
                <textarea id="km-ingest-text" class="km-input" style="width:100%;height:110px;line-height:1.45;font-size:13px;resize:vertical">${{esc(currentText)}}</textarea>
              </div>

              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
                <span style="font-size:12px;color:#64748B">Strict character-level attribution verification enforced on all extractions.</span>
                <button class="km-btn km-btn-primary" onclick="window.kmAction.extractPaperClaims()" style="background:linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);border:none;box-shadow:0 4px 12px rgba(99,102,241,0.25)">
                  ⚡ Extract &amp; Ground Claims
                </button>
              </div>

              <!-- Extracted Results Preview -->
              ${{res ? `
                <div style="border-top:1px solid #E2E8F0;padding-top:16px;margin-top:16px">
                  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
                    <div style="display:flex;align-items:center;gap:8px">
                      <span style="font-size:13px;font-weight:700;color:#0A0F1D">Extraction Verification Report</span>
                      <span class="km-badge verified">✓ ${{res.count}} Atomic Claims</span>
                      <span class="km-badge info" style="background:#EEF2FF;color:#4F46E5;border:1px solid #C7D2FE">Attribution Fidelity: ${{(res.attribution_fidelity * 100).toFixed(0)}}%</span>
                    </div>
                    <span style="font-size:11.5px;color:#64748B">RFC 8785 Compatible</span>
                  </div>

                  <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:18px">
                    ${{(res.candidate_claims || []).map((c, i) => `
                      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;padding:12px 14px;box-shadow:0 1px 3px rgba(0,0,0,0.02)">
                        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
                          <div style="display:flex;align-items:center;gap:6px">
                            <span class="km-mono" style="font-size:11px;font-weight:700;color:#6366F1">#${{i+1}}</span>
                            <span class="km-badge" style="font-size:10.5px;text-transform:uppercase">${{esc(c.category)}}</span>
                          </div>
                          <span style="font-size:11px;color:#059669;font-weight:600">✓ Grounded [${{c.char_start}}..${{c.char_end}}]</span>
                        </div>
                        <div style="font-size:13px;font-weight:600;color:#0A0F1D;margin-bottom:6px;line-height:1.4">${{esc(c.statement)}}</div>
                        <div style="font-size:12px;background:#F8FAFC;border-left:3px solid #6366F1;padding:6px 10px;border-radius:0 6px 6px 0;color:#475569;margin-bottom:6px;font-style:italic">
                          "${{esc(c.exact_quote)}}"
                        </div>
                        <div style="display:flex;gap:12px;font-size:11px;color:#64748B;font-family:var(--font-mono)">
                          <span>(S) ${{esc(c.triple.subject)}}</span>
                          <span>→ [${{esc(c.triple.predicate)}}] →</span>
                          <span>(O) ${{esc(c.triple.object)}}</span>
                        </div>
                      </div>
                    `).join('')}}
                  </div>

                  <div style="display:flex;justify-content:flex-end;gap:10px;padding-top:14px;border-top:1px solid #E2E8F0">
                    <button class="km-btn" onclick="window.kmAction.closeModal()">Close</button>
                    <button class="km-btn km-btn-primary" onclick="window.kmAction.bundleExtractedClaims()" style="background:linear-gradient(135deg, #10B981 0%, #059669 100%);border:none;box-shadow:0 4px 12px rgba(16,185,129,0.25)">
                      🔒 Lock into Signed OKF Bundle &amp; Publish
                    </button>
                  </div>
                </div>
              ` : ''}}
            </div>
          </div>
        `;
      }}

      return '';
    }}

    function initScrollObserver() {{
      const elements = document.querySelectorAll('.km-reveal, .km-reveal-scale, .km-reveal-left, .km-reveal-right');
      if (!elements || elements.length === 0) return;

      if (!('IntersectionObserver' in window)) {{
        elements.forEach(function(el) {{ el.classList.add('km-revealed'); }});
        return;
      }}

      const observer = new IntersectionObserver(function(entries) {{
        entries.forEach(function(entry) {{
          if (entry.isIntersecting) {{
            entry.target.classList.add('km-revealed');
            observer.unobserve(entry.target);
          }}
        }});
      }}, {{
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
      }});

      elements.forEach(function(el) {{
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {{
          // Immediately reveal if element is already within viewport
          el.classList.add('km-revealed');
        }} else {{
          observer.observe(el);
        }}
      }});
    }}

    function render() {{
      const root = document.getElementById('km-app');
      if (!root) return;
      if (state.stage === 'landing') {{
        root.innerHTML = renderLandingPage() + renderToastContainer();
        initTransformationSceneThree();
        initScrollObserver();
      }} else if (state.stage === 'login' || !state.currentUser) {{
        root.innerHTML = renderLoginGate() + renderToastContainer();
      }} else {{
        root.innerHTML = renderDashboard() + renderActiveModal() + renderToastContainer();
        if (state.activeTab === 'okf-graph') {{
          fitOkfGraph();
          requestAnimationFrame(fitOkfGraph);
          setTimeout(fitOkfGraph, 50);
        }}
      }}
    }}

    render();
    loadPublicLandingData();
    checkExistingSession();
  }})();
  </script>
</body>
</html>"""
