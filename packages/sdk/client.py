"""HTTP and pluggable-transport client for KnowMesh nodes."""

from __future__ import annotations

import json
import time
from typing import Any, Callable, Mapping
import urllib.error
import urllib.parse
import urllib.request

from .exceptions import (
    SDKConnectionError,
    SDKError,
    SDKNotFoundError,
    SDKValidationError,
)

TransportCallable = Callable[[str, str, Mapping[str, Any] | None, Mapping[str, str]], tuple[int, Any]]


class KnowMeshClient:
    """Client for interacting with a KnowMesh API node."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        *,
        api_key: str | None = None,
        token: str | None = None,
        api_prefix: str = "/api/v1",
        timeout_seconds: float = 10.0,
        max_retries: int = 2,
        headers: Mapping[str, str] | None = None,
        transport: TransportCallable | None = None,
    ) -> None:
        if not base_url or not base_url.strip():
            raise SDKValidationError("base_url is required")
        if timeout_seconds <= 0:
            raise SDKValidationError("timeout_seconds must be positive")
        self.base_url = base_url.rstrip("/")
        self.api_prefix = "/" + api_prefix.strip("/") if api_prefix.strip("/") else ""
        self.timeout_seconds = float(timeout_seconds)
        self.max_retries = max(0, int(max_retries))
        base_headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if api_key:
            base_headers["X-KnowMesh-Key"] = api_key
        if token:
            base_headers["Authorization"] = f"Bearer {token}"
        if headers:
            base_headers.update(headers)
        self.headers = base_headers
        self._transport = transport

    def _build_url(self, path: str, params: Mapping[str, Any] | None = None) -> str:
        normalized = path if path.startswith("/") else f"/{path}"
        if not normalized.startswith(self.api_prefix) and normalized not in {"/health", "/metrics"}:
            full_path = f"{self.api_prefix}{normalized}"
        else:
            full_path = normalized
        url = f"{self.base_url}{full_path}"
        if params:
            filtered = {k: v for k, v in params.items() if v is not None}
            if filtered:
                url = f"{url}?{urllib.parse.urlencode(filtered)}"
        return url

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Mapping[str, Any] | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        method_upper = method.upper()
        url = self._build_url(path, params=params)
        if self._transport is not None:
            status, payload = self._transport(method_upper, url, json_body, self.headers)
            return self._handle_response(status, payload)

        data = json.dumps(dict(json_body)).encode("utf-8") if json_body is not None else None
        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            req = urllib.request.Request(url, data=data, headers=self.headers, method=method_upper)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                    raw = resp.read().decode("utf-8")
                    parsed = json.loads(raw) if raw else None
                    return self._handle_response(resp.status, parsed)
            except urllib.error.HTTPError as exc:
                raw_err = exc.read().decode("utf-8", errors="replace")
                try:
                    parsed_err = json.loads(raw_err) if raw_err else {"detail": exc.reason}
                except Exception:
                    parsed_err = {"detail": raw_err or str(exc.reason)}
                if exc.code in {429, 502, 503, 504} and attempt < self.max_retries:
                    time.sleep(0.1 * (2**attempt))
                    continue
                return self._handle_response(exc.code, parsed_err)
            except urllib.error.URLError as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    time.sleep(0.1 * (2**attempt))
                    continue
                raise SDKConnectionError(f"Failed to connect to {url}: {exc.reason}") from exc
        raise SDKConnectionError(f"Failed to connect to {url}: {last_exc}")

    @staticmethod
    def _handle_response(status: int, payload: Any) -> Any:
        if status == 404:
            raise SDKNotFoundError("Resource not found", status_code=404, details=payload)
        if status == 422 or status == 400:
            raise SDKValidationError("Validation error", status_code=status, details=payload)
        if status >= 400:
            raise SDKError(f"HTTP {status} error", status_code=status, details=payload)
        return payload

    def health(self) -> dict[str, Any]:
        return self.request("GET", "/health")

    def get_node_identity(self, node_id: str | None = None) -> dict[str, Any]:
        if node_id:
            return self.request("GET", f"/nodes/{node_id}/identity")
        return self.request("GET", "/federation/identity")

    def validate_okf(self, manifest_data: Mapping[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/okf/validate", json_body=manifest_data)

    def publish_bundle(self, bundle_data: Mapping[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/bundles", json_body=bundle_data)

    def publish_revision(self, bundle_id: str, revision_data: Mapping[str, Any]) -> dict[str, Any]:
        return self.request("POST", f"/bundles/{bundle_id}/revisions", json_body=revision_data)

    def get_bundle(self, bundle_id: str, *, revision: str | None = None) -> dict[str, Any]:
        return self.request("GET", f"/bundles/{bundle_id}", params={"revision": revision})

    def list_bundles(self, *, limit: int = 50, offset: int = 0, q: str | None = None) -> dict[str, Any]:
        return self.request("GET", "/bundles", params={"limit": limit, "offset": offset, "q": q})

    def search(
        self,
        query: str,
        *,
        limit: int = 10,
        scope: str = "local",
        category: str | None = None,
        node_id: str | None = None,
        verification_state: str | None = None,
        evidence_required: bool = False,
    ) -> dict[str, Any]:
        return self.request(
            "POST",
            "/search",
            json_body={
                "query": query,
                "limit": limit,
                "scope": scope,
                "category": category,
                "node_id": node_id,
                "verification_state": verification_state,
                "evidence_required": evidence_required,
            },
        )

    def discover_federated(self, query: str, *, limit: int = 10) -> dict[str, Any]:
        return self.search(query, limit=limit, scope="federated")

    def verify_bundle(self, bundle_or_payload: Mapping[str, Any], *, public_key: str | None = None) -> dict[str, Any]:
        body = dict(bundle_or_payload)
        if public_key:
            body["public_key"] = public_key
        return self.request("POST", "/trust/verify", json_body=body)
