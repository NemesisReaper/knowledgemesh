"""Exceptions raised by the KnowMesh Python SDK."""

from __future__ import annotations


class SDKError(Exception):
    """Base exception for KnowMesh SDK errors."""

    def __init__(self, message: str, *, status_code: int | None = None, details: object = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class SDKConnectionError(SDKError):
    """Raised when the KnowMesh node cannot be reached."""


class SDKNotFoundError(SDKError):
    """Raised when a requested resource returns HTTP 404."""


class SDKValidationError(SDKError):
    """Raised when client input or server response fails validation."""


class SDKVerificationError(SDKError):
    """Raised when cryptographic or digest verification of a bundle fails."""

