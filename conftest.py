"""Root pytest configuration providing sandbox-safe ASGI TestClient transport on Windows."""

from __future__ import annotations

import anyio.to_thread
import httpx
import starlette.testclient


async def _inline_run_sync(func, *args, abandon_on_cancel: bool = False, cancellable: bool = False, limiter=None):
    return func(*args)


class DirectASGITransport(httpx.BaseTransport):
    """In-process synchronous ASGI transport that avoids socket.socketpair() loopback in Windows sandboxes."""

    def __init__(self, app, raise_app_exceptions: bool = True) -> None:
        self.app = app
        self.raise_app_exceptions = raise_app_exceptions

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        body = request.read()
        headers = [(k.lower(), v) for k, v in request.headers.raw]
        scope = {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1",
            "method": request.method,
            "scheme": request.url.scheme or "http",
            "path": request.url.path,
            "raw_path": request.url.raw_path.split(b"?")[0],
            "query_string": request.url.query,
            "root_path": "",
            "headers": headers,
            "client": ("127.0.0.1", 50000),
            "server": (request.url.host or "testserver", request.url.port or 80),
            "state": {},
        }
        messages: list[dict] = []
        sent = False

        async def receive():
            nonlocal sent
            if not sent:
                sent = True
                return {"type": "http.request", "body": body, "more_body": False}
            return {"type": "http.disconnect"}

        async def send(message):
            messages.append(message)

        orig_run_sync = anyio.to_thread.run_sync
        anyio.to_thread.run_sync = _inline_run_sync
        try:
            coro = self.app(scope, receive, send)
            try:
                while True:
                    coro.send(None)
            except StopIteration:
                pass
            except Exception:
                if self.raise_app_exceptions:
                    raise
                return httpx.Response(status_code=500, content=b"Internal Server Error", request=request)
        finally:
            anyio.to_thread.run_sync = orig_run_sync

        status_code = 500
        resp_headers: list[tuple[bytes, bytes]] = []
        body_chunks: list[bytes] = []
        for msg in messages:
            if msg["type"] == "http.response.start":
                status_code = msg["status"]
                resp_headers = list(msg.get("headers", []))
            elif msg["type"] == "http.response.body":
                body_chunks.append(msg.get("body", b""))

        return httpx.Response(
            status_code=status_code,
            headers=[(k.decode("latin-1"), v.decode("latin-1")) for k, v in resp_headers],
            content=b"".join(body_chunks),
            request=request,
        )


class SandboxSafeTestClient(httpx.Client):
    """Drop-in replacement for starlette.testclient.TestClient using DirectASGITransport."""

    __test__ = False

    def __init__(
        self,
        app,
        base_url: str = "http://testserver",
        raise_server_exceptions: bool = True,
        root_path: str = "",
        backend: str = "asyncio",
        backend_options: dict | None = None,
        cookies=None,
        headers: dict[str, str] | None = None,
        follow_redirects: bool = True,
        **kwargs,
    ) -> None:
        transport = DirectASGITransport(app, raise_app_exceptions=raise_server_exceptions)
        default_headers = {"user-agent": "testclient"}
        if headers:
            default_headers.update(headers)
        super().__init__(
            base_url=base_url,
            headers=default_headers,
            transport=transport,
            follow_redirects=follow_redirects,
            cookies=cookies,
        )
        self.app = app

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


starlette.testclient.TestClient = SandboxSafeTestClient
try:
    import fastapi.testclient

    fastapi.testclient.TestClient = SandboxSafeTestClient
except Exception:
    pass
