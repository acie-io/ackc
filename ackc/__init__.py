"""ACIE Auth Client - High-performance Keycloak client using niquests.

This package provides a modern, async-first Python client for Keycloak with:
- Auto-generated API from OpenAPI spec
- High-performance niquests backend (HTTP/2, multiplexing)
- Type safety with Pydantic models
- Async and sync interfaces

Basic usage:
    from acie.auth.client import KeycloakClient
    
    # Client will auto-authenticate using KEYCLOAK_* env vars
    client = KeycloakClient()
    
    # Use the generated API directly
    from acie.auth.client.api.users import get_admin_realms_realm_users
    users = get_admin_realms_realm_users.sync(realm="master", client=client)
"""
from importlib.metadata import version

# Re-export the generated client classes
from .generated import AuthenticatedClient, Client
from .generated import models  # All the attrs models

# Our additions
from .keycloak import KeycloakClient
from .exceptions import (
    AuthError,
    ClientError,
    TokenExpiredError,
    UserNotFoundError,
)

__version__ = version("ackc")

__all__ = (
    # Generated exports
    "AuthenticatedClient",
    "Client",
    "models",
    # Our wrapper
    "KeycloakClient",
    # Exceptions
    "AuthError",
    "ClientError",
    "TokenExpiredError",
    "UserNotFoundError",
)