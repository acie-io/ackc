"""Client (application) management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import AuthError
from ..generated.api.clients import (
    get_admin_realms_realm_clients,
    post_admin_realms_realm_clients,
    get_admin_realms_realm_clients_client_uuid,
)
from ..generated.models import ClientRepresentation
from ..generated.types import UNSET, Unset

__all__ = "ClientsAPI", "ClientsClientMixin", "ClientRepresentation"


class ClientsAPI(BaseAPI):
    """Client (application) management API methods."""

    def get_all(
        self,
        realm: str | None = None,
        *,
        client_id: Unset | str = UNSET,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
        q: Unset | str = UNSET,
        search: Unset | bool = False,
        viewable_only: Unset | bool = False,
    ) -> list[ClientRepresentation] | None:
        """List clients in a realm.
        
        Args:
            realm: The realm name
            client_id: Filter by client ID (not UUID)
            first: Pagination offset
            max: Maximum results to return
            q: Query string for client search
            search: Boolean flag to enable searching
            viewable_only: Only return viewable clients
            
        Returns:
            List of clients matching the filters
        """
        return self._sync(
            get_admin_realms_realm_clients.sync,
            realm,
            client_id=client_id,
            first=first,
            max_=max,
            q=q,
            search=search,
            viewable_only=viewable_only,
        )

    async def aget_all(
        self,
        realm: str | None = None,
        *,
        client_id: Unset | str = UNSET,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
        q: Unset | str = UNSET,
        search: Unset | bool = False,
        viewable_only: Unset | bool = False,
    ) -> list[ClientRepresentation] | None:
        """List clients in a realm (async).
        
        Args:
            realm: The realm name
            client_id: Filter by client ID (not UUID)
            first: Pagination offset
            max: Maximum results to return
            q: Query string for client search
            search: Boolean flag to enable searching
            viewable_only: Only return viewable clients
            
        Returns:
            List of clients matching the filters
        """
        return await self._async(
            get_admin_realms_realm_clients.asyncio,
            realm,
            client_id=client_id,
            first=first,
            max_=max,
            q=q,
            search=search,
            viewable_only=viewable_only,
        )

    def create(self, realm: str | None = None, client_data: dict | ClientRepresentation = None) -> str:
        """Create a client (sync). Returns client UUID."""
        client_obj = client_data if isinstance(client_data, ClientRepresentation) else ClientRepresentation.from_dict(client_data)
        response = self._sync_detailed(
            post_admin_realms_realm_clients.sync_detailed,
            realm=realm,
            body=client_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create client: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def acreate(self, realm: str | None = None, client_data: dict | ClientRepresentation = None) -> str:
        """Create a client (async). Returns client UUID."""
        client_obj = client_data if isinstance(client_data, ClientRepresentation) else ClientRepresentation.from_dict(client_data)
        response = await self._async_detailed(
            post_admin_realms_realm_clients.asyncio_detailed,
            realm=realm,
            body=client_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create client: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    def get(self, realm: str | None = None, client_uuid: str = None) -> ClientRepresentation | None:
        """Get a client by UUID (sync)."""
        return self._sync(
            get_admin_realms_realm_clients_client_uuid.sync,
            realm=realm,
            client_uuid=client_uuid
        )

    async def aget(self, realm: str | None = None, client_uuid: str = None) -> ClientRepresentation | None:
        """Get a client by UUID (async)."""
        return await self._async(
            get_admin_realms_realm_clients_client_uuid.asyncio,
            realm=realm,
            client_uuid=client_uuid
        )


class ClientsClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the ClientsAPI.
    """

    @cached_property
    def clients(self) -> ClientsAPI:
        """Get the ClientsAPI instance."""
        return ClientsAPI(manager=self)  # type: ignore[arg-type]
