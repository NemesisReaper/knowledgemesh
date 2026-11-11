"""Simple deny-by-default role/attribute access-control engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping


class AccessControlError(ValueError):
    pass


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    PUBLISH = "publish"
    VERIFY = "verify"
    DELETE = "delete"
    ADMIN = "admin"


@dataclass(frozen=True, slots=True)
class Principal:
    id: str
    roles: frozenset[str] = frozenset()
    attributes: Mapping[str, Any] = field(default_factory=dict)
    authenticated: bool = True


@dataclass(frozen=True, slots=True)
class Resource:
    id: str
    owner_id: str | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AccessRequest:
    principal: Principal
    resource: Resource
    permission: Permission
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AccessDecision:
    allowed: bool
    reason: str
    matched_rule: str | None = None


@dataclass(frozen=True, slots=True)
class _Rule:
    role: str
    permission: Permission
    resource_attribute: str | None = None
    resource_value: Any = None


class AccessControl:
    """Explicit role grants with owner grants and deny-by-default behavior."""
    def __init__(self, *, owner_permissions: Iterable[Permission] = (
        Permission.READ, Permission.WRITE, Permission.PUBLISH, Permission.VERIFY,
    )) -> None:
        self._rules: list[_Rule] = []
        self.owner_permissions = frozenset(owner_permissions)

    def grant(self, role: str, permission: Permission, *,
              resource_attribute: str | None = None,
              resource_value: Any = None) -> None:
        if not role:
            raise AccessControlError("role is required")
        rule = _Rule(role, Permission(permission), resource_attribute, resource_value)
        if rule not in self._rules:
            self._rules.append(rule)

    def revoke(self, role: str, permission: Permission, *,
               resource_attribute: str | None = None,
               resource_value: Any = None) -> bool:
        rule = _Rule(role, Permission(permission), resource_attribute, resource_value)
        if rule not in self._rules:
            return False
        self._rules.remove(rule)
        return True

    def authorize(self, request: AccessRequest) -> AccessDecision:
        principal, resource, permission = request.principal, request.resource, request.permission
        if not principal.authenticated:
            return AccessDecision(False, "principal is not authenticated")
        if permission == Permission.ADMIN and "admin" not in principal.roles:
            return AccessDecision(False, "admin role required")
        if resource.owner_id and principal.id == resource.owner_id and permission in self.owner_permissions:
            return AccessDecision(True, "resource owner grant", "owner")
        for rule in self._rules:
            if rule.role not in principal.roles or rule.permission != permission:
                continue
            if rule.resource_attribute is not None:
                if resource.attributes.get(rule.resource_attribute) != rule.resource_value:
                    continue
            return AccessDecision(True, "matching role grant", rule.role)
        if permission == Permission.ADMIN and "admin" in principal.roles:
            return AccessDecision(True, "administrator grant", "admin")
        return AccessDecision(False, "no matching access rule")

    def check(self, principal: Principal, resource: Resource,
              permission: Permission, *, context: Mapping[str, Any] | None = None) -> bool:
        return self.authorize(AccessRequest(principal, resource, permission,
                                            context or {})).allowed
