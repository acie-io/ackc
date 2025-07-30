"""Client scope management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import AuthError
from ..generated.api.client_scopes import (
    get_admin_realms_realm_client_scopes,
    post_admin_realms_realm_client_scopes,
    get_admin_realms_realm_client_scopes_client_scope_id,
    put_admin_realms_realm_client_scopes_client_scope_id,
    delete_admin_realms_realm_client_scopes_client_scope_id,
)
from ..generated.models import ClientScopeRepresentation

__all__ = "ClientScopesAPI", "ClientScopesClientMixin", "ClientScopeRepresentation"


class ClientScopesAPI(BaseAPI):
    """Client scope management API methods."""

    def get_all(self, realm: str | None = None) -> list[ClientScopeRepresentation] | None:
        """List client scopes in a realm (sync)."""
        return self._sync(get_admin_realms_realm_client_scopes.sync, realm)

    async def aget_all(self, realm: str | None = None) -> list[ClientScopeRepresentation] | None:
        """List client scopes in a realm (async)."""
        return await self._async(get_admin_realms_realm_client_scopes.asyncio, realm)

    def create(self, realm: str | None = None, scope_data: dict | ClientScopeRepresentation = None) -> str:
        """Create a client scope (sync). Returns scope ID."""
        scope_obj = scope_data if isinstance(scope_data, ClientScopeRepresentation) else ClientScopeRepresentation.from_dict(scope_data)
        response = self._sync_detailed(
            post_admin_realms_realm_client_scopes.sync_detailed,
            realm=realm,
            body=scope_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create client scope: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def acreate(self, realm: str | None = None, scope_data: dict | ClientScopeRepresentation = None) -> str:
        """Create a client scope (async). Returns scope ID."""
        scope_obj = scope_data if isinstance(scope_data, ClientScopeRepresentation) else ClientScopeRepresentation.from_dict(scope_data)
        response = await self._async_detailed(
            post_admin_realms_realm_client_scopes.asyncio_detailed,
            realm=realm,
            body=scope_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create client scope: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    def get(self, realm: str | None = None, client_scope_id: str = None) -> ClientScopeRepresentation | None:
        """Get a client scope by ID (sync)."""
        return self._sync(
            get_admin_realms_realm_client_scopes_client_scope_id.sync,
            realm=realm,
            client_scope_id=client_scope_id
        )

    async def aget(self, realm: str | None = None, client_scope_id: str = None) -> ClientScopeRepresentation | None:
        """Get a client scope by ID (async)."""
        return await self._async(
            get_admin_realms_realm_client_scopes_client_scope_id.asyncio,
            realm=realm,
            client_scope_id=client_scope_id
        )

    def update(self, realm: str | None = None, client_scope_id: str = None,
               scope_data: dict | ClientScopeRepresentation = None) -> None:
        """Update a client scope (sync)."""
        scope_obj = scope_data if isinstance(scope_data, ClientScopeRepresentation) else ClientScopeRepresentation.from_dict(scope_data)
        response = self._sync_detailed(
            put_admin_realms_realm_client_scopes_client_scope_id.sync_detailed,
            realm=realm,
            client_scope_id=client_scope_id,
            body=scope_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update client scope: {response.status_code}")

    async def aupdate(self, realm: str | None = None, client_scope_id: str = None,
                      scope_data: dict | ClientScopeRepresentation = None) -> None:
        """Update a client scope (async)."""
        scope_obj = scope_data if isinstance(scope_data, ClientScopeRepresentation) else ClientScopeRepresentation.from_dict(scope_data)
        response = await self._async_detailed(
            put_admin_realms_realm_client_scopes_client_scope_id.asyncio_detailed,
            realm=realm,
            client_scope_id=client_scope_id,
            body=scope_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update client scope: {response.status_code}")

    def delete(self, realm: str | None = None, client_scope_id: str = None) -> None:
        """Delete a client scope (sync)."""
        response = self._sync_detailed(
            delete_admin_realms_realm_client_scopes_client_scope_id.sync_detailed,
            realm=realm,
            client_scope_id=client_scope_id
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete client scope: {response.status_code}")

    async def adelete(self, realm: str | None = None, client_scope_id: str = None) -> None:
        """Delete a client scope (async)."""
        response = await self._async_detailed(
            delete_admin_realms_realm_client_scopes_client_scope_id.asyncio_detailed,
            realm=realm,
            client_scope_id=client_scope_id
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete client scope: {response.status_code}")


class ClientScopesClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the ClientScopesAPI.
    """

    @cached_property
    def client_scopes(self) -> ClientScopesAPI:
        """Get the ClientScopesAPI instance."""
        return ClientScopesAPI(manager=self)  # type: ignore[arg-type]
