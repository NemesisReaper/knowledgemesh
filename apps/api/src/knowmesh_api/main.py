"""KnowMesh FastAPI application factory and HTTP entry point."""

from __future__ import annotations

import json
from pathlib import Path
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from observability import observe_request, render_prometheus

from .api.v1.router import api_router
from .config import Settings, settings as default_settings
from .console_ui import render_console_html
from .service import KnowMeshService
from .store import store


class KnowMeshObservabilityMiddleware:
    """Pure ASGI middleware for request-size validation, request-ID propagation, and metrics."""

    def __init__(self, app, *, cfg: Settings, svc: KnowMeshService) -> None:
        self.app = app
        self.cfg = cfg
        self.svc = svc

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        req_id = f"req_{uuid.uuid4().hex[:12]}"
        content_len = 0
        for k, v in scope.get("headers", []):
            key_low = k.lower()
            if key_low == b"x-request-id":
                req_id = v.decode("latin-1", errors="replace")
            elif key_low == b"content-length":
                raw_len = v.decode("latin-1", errors="replace").strip()
                if raw_len.isdigit():
                    content_len = int(raw_len)

        if content_len > self.cfg.max_request_bytes:
            payload = json.dumps({
                "detail": f"Request payload exceeds limit of {self.cfg.max_request_bytes} bytes"
            }).encode("utf-8")
            await send({
                "type": "http.response.start",
                "status": 413,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"x-request-id", req_id.encode("latin-1")),
                    (b"x-knowmesh-node-id", self.cfg.node_id.encode("latin-1")),
                ],
            })
            await send({"type": "http.response.body", "body": payload})
            return

        start = time.perf_counter()
        status_code = 500

        async def _send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                headers = list(message.get("headers", []))
                headers.append((b"x-request-id", req_id.encode("latin-1")))
                headers.append((b"x-knowmesh-node-id", self.cfg.node_id.encode("latin-1")))
                message = {**message, "headers": headers}
            await send(message)

        await self.app(scope, receive, _send_wrapper)
        duration = time.perf_counter() - start
        observe_request(
            self.svc.metrics,
            method=scope.get("method", "GET"),
            route=scope.get("path", "/"),
            status_code=status_code,
            duration_seconds=duration,
        )


def create_app(
    config: Settings | None = None,
    *,
    service: KnowMeshService | None = None,
) -> FastAPI:
    cfg = config or default_settings
    svc = service or KnowMeshService(cfg)

    application = FastAPI(
        title=cfg.app_name,
        version="0.2.0",
        description="KnowMesh Federated Knowledge Infrastructure API",
    )
    application.state.settings = cfg
    application.state.service = svc
    store.bind_service(svc)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(cfg.cors_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(KnowMeshObservabilityMiddleware, cfg=cfg, svc=svc)

    application.include_router(api_router, prefix=cfg.api_prefix)

    static_dir = Path(__file__).resolve().parent / "static"
    if static_dir.exists():
        application.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @application.get("/health")
    def health() -> dict[str, object]:
        report = svc.health_registry.run().to_dict()
        return {
            "status": "ok" if report["status"] in {"healthy", "degraded"} else "unhealthy",
            "health_status": report["status"],
            "service": "knowmesh-api",
            "node_id": cfg.node_id,
            "node_name": cfg.node_name,
            "environment": cfg.environment,
            "checks": report["checks"],
        }

    @application.get("/metrics", response_class=PlainTextResponse)
    def prometheus_metrics() -> str:
        return render_prometheus(svc.metrics)

    @application.get("/console", response_class=HTMLResponse)
    @application.get("/ui", response_class=HTMLResponse)
    def console_ui() -> HTMLResponse:
        return HTMLResponse(content=render_console_html())

    @application.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, str]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept:
            return HTMLResponse(content=render_console_html())
        return {
            "name": cfg.app_name,
            "node_id": cfg.node_id,
            "console": "/console",
            "docs": "/docs",
            "health": "/health",
            "metrics": "/metrics",
        }

    return application


app = create_app()
