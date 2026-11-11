/**
 * Typed KnowMesh API Client for the Organization Console and Developer Portal.
 * Connects directly to the real FastAPI backend without mock production payloads.
 */

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_KNOWMESH_API_URL || "http://localhost:8000";

export interface VerificationReport {
  status: "verified" | "verification_failed" | "verification_incomplete" | string;
  trust_verification_status?: string;
  retrieved_successfully: boolean;
  integrity_verified: boolean;
  signature_verified: boolean;
  signer_recognized: boolean;
  provenance_available: boolean;
  policy_compliant: boolean;
  signer_id: string;
  key_fingerprint: string;
  content_digest: string;
  computed_digest: string;
  reasons: string[];
  epistemic_notice: string;
}

export interface NodeItem {
  id: string;
  node_id: string;
  name: string;
  description: string;
  organization_id: string | null;
  endpoint: string;
  hosting_type: string;
  visibility: "private" | "organization" | "federated" | string;
  status: string;
  capabilities: string[];
  public_key: string;
  key_fingerprint: string;
  bundle_count: number;
  peer_count: number;
  agent_count: number;
  last_seen_at: string | null;
  created_at: string;
}

export interface ClaimItem {
  id?: string;
  claim_id: string;
  bundle_id?: string;
  revision?: string;
  statement: string;
  claim_type?: string;
  domain: string;
  status: string;
  confidence?: number;
  evidence_ids: string[];
  contradictory_evidence_ids?: string[];
  source_references?: string[];
}

export interface EvidenceItem {
  id?: string;
  evidence_id: string;
  bundle_id?: string | null;
  title?: string;
  source_uri: string;
  source_type: string;
  description: string;
  content_hash?: string;
  reliability?: number;
  relation_type?: string;
}

export interface RevisionItem {
  revision_id: string;
  revision: string;
  previous_revision: string | null;
  content_digest: string;
  merkle_root: string;
  signer_id: string;
  key_fingerprint: string;
  change_note: string;
  published_at: string;
}

export interface ProvenanceEventItem {
  record_id: string;
  subject_id: string;
  action: string;
  actor_id: string;
  node_id: string;
  occurred_at: string;
  previous_hash: string | null;
  record_hash: string;
  details: Record<string, unknown>;
}

export interface BundleItem {
  id: string;
  bundle_id: string;
  title: string;
  description: string;
  content: string;
  category: string;
  tags: string[];
  organization_id: string | null;
  publisher_node_id: string;
  origin_node_id: string;
  visibility: "private" | "organization" | "federated" | string;
  status: string;
  is_archived: boolean;
  revision: string;
  current_revision: string;
  previous_revision: string | null;
  content_digest: string;
  merkle_root: string;
  signer_id: string;
  key_fingerprint: string;
  signature: Record<string, unknown>;
  claims: ClaimItem[];
  evidence: EvidenceItem[];
  okf_manifest: Record<string, unknown>;
  verification: VerificationReport;
  revisions: RevisionItem[];
  provenance: ProvenanceEventItem[];
  created_at: string;
  updated_at: string;
}

export interface PeerItem {
  id: string;
  peer_id: string;
  local_node_id: string;
  peer_node_id: string;
  name: string;
  endpoint: string;
  public_key: string;
  key_fingerprint: string;
  status: string;
  trust_level: string;
  identity_verified: boolean;
  approved: boolean;
  capabilities: string[];
  latency_ms: number | null;
  last_sync_at: string | null;
  last_error: string | null;
  created_at: string;
}

export interface CredentialItem {
  id: string;
  credential_id: string;
  name: string;
  agent_id: string | null;
  organization_id: string | null;
  key_prefix: string;
  permissions: string[];
  status: string;
  expires_at: string | null;
  revoked_at: string | null;
  last_used_at: string | null;
  created_at: string;
  secret?: string;
  warning?: string;
}

export interface AgentItem {
  id: string;
  agent_id: string;
  name: string;
  description: string;
  organization_id: string | null;
  node_id: string;
  status: string;
  permissions: string[];
  credentials: CredentialItem[];
  initial_credential?: CredentialItem;
  last_active_at: string | null;
  created_at: string;
}

export interface AuditEventItem {
  id: string;
  event_id: string;
  organization_id: string | null;
  node_id: string | null;
  actor_id: string;
  actor_type: string;
  category: string;
  action: string;
  resource_type: string;
  resource_id: string;
  outcome: string;
  request_id: string | null;
  details: Record<string, unknown>;
  created_at: string;
}

export interface OverviewResponse {
  node_id: string;
  metrics: {
    total_nodes: number;
    online_peers: number;
    total_peers: number;
    knowledge_bundles: number;
    published_claims: number;
    registered_agents: number;
    pending_reviews: number;
    sync_failures: number;
  };
  claim_review_distribution: Record<string, number>;
  topology: {
    nodes: Array<{
      id: string;
      label: string;
      type: string;
      status: string;
      endpoint: string;
      visibility: string;
      fingerprint: string;
    }>;
    edges: Array<{
      id: string;
      source: string;
      target: string;
      status: string;
      verified: boolean;
      approved: boolean;
      latency_ms: number | null;
    }>;
  };
  recent_activity: AuditEventItem[];
  recent_syncs: Array<{
    sync_id: string;
    peer_node_id: string;
    state: string;
    bundles_pulled: number;
    conflicts_detected: number;
    created_at: string;
  }>;
}

export interface SearchHit {
  resource: string;
  id: string;
  bundle_id: string;
  title: string;
  description: string;
  publisher_node: string;
  origin_node: string;
  category: string;
  revision: string;
  last_updated: string;
  score: number;
  freshness_score: number;
  access_status: string;
  verification_status: string;
  verification: VerificationReport;
  claims: ClaimItem[];
  evidence: EvidenceItem[];
  record: BundleItem;
}

export interface SearchResponse {
  query: string;
  scope: string;
  results: SearchHit[];
  total: number;
  limit: number;
  offset: number;
  trace: {
    trace_id: string;
    span_id: string;
    local_node_id: string;
    index_generation: number;
    peers_queried: Array<{
      peer_node_id: string;
      status: string;
      hits?: number;
      error?: string;
    }>;
  };
}

function getAuthHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Accept: "application/json",
  };
  if (typeof window !== "undefined") {
    const token = window.localStorage.getItem("km_access_token");
    const orgId = window.localStorage.getItem("km_org_id");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    if (orgId) {
      headers["X-KnowMesh-Org"] = orgId;
    }
  }
  return headers;
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = path.startsWith("http")
    ? path
    : `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
  const resp = await fetch(url, {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...(options.headers || {}),
    },
    cache: "no-store",
  });
  if (resp.status === 204) {
    return undefined as unknown as T;
  }
  const text = await resp.text();
  let data: unknown = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { detail: text };
  }
  if (!resp.ok) {
    const detail =
      typeof data === "object" && data !== null && "detail" in data
        ? String((data as { detail: unknown }).detail)
        : `HTTP ${resp.status}`;
    throw new Error(detail);
  }
  return data as T;
}

