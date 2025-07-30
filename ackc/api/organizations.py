"""Organization management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import AuthError
from ..generated.api.organizations import (
    get_admin_realms_realm_organizations,
    post_admin_realms_realm_organizations,
    get_admin_realms_realm_organizations_org_id,
    put_admin_realms_realm_organizations_org_id,
    delete_admin_realms_realm_organizations_org_id,
    get_admin_realms_realm_organizations_org_id_members,
    post_admin_realms_realm_organizations_org_id_members,
)
from ..generated.models import OrganizationRepresentation
from ..generated.types import UNSET, Unset

__all__ = "OrganizationsAPI", "OrganizationsClientMixin", "OrganizationRepresentation"


class OrganizationsAPI(BaseAPI):
    """Organization management API methods."""

    def get_all(
        self,
        realm: str | None = None,
        *,
        brief_representation: Unset | bool = True,
        exact: Unset | bool = UNSET,
        first: Unset | int = 0,
        max: Unset | int = 10,
        q: Unset | str = UNSET,
        search: Unset | str = UNSET,
    ) -> list[OrganizationRepresentation] | None:
        """List organizations in a realm.
        
        Args:
            realm: The realm name
            brief_representation: Only return basic organization info (default True)
            exact: Exact match for searches
            first: Pagination offset (default 0)
            max: Maximum results to return (default 10)
            q: Query string for organization search
            search: Search string (searches organization name)
            
        Returns:
            List of organizations matching the filters
        """
        return self._sync(
            get_admin_realms_realm_organizations.sync,
            realm,
            brief_representation=brief_representation,
            exact=exact,
            first=first,
            max_=max,
            q=q,
            search=search,
        )

    async def aget_all(
        self,
        realm: str | None = None,
        *,
        brief_representation: Unset | bool = True,
        exact: Unset | bool = UNSET,
        first: Unset | int = 0,
        max: Unset | int = 10,
        q: Unset | str = UNSET,
        search: Unset | str = UNSET,
    ) -> list[OrganizationRepresentation] | None:
        """List organizations in a realm (async).
        
        Args:
            realm: The realm name
            brief_representation: Only return basic organization info (default True)
            exact: Exact match for searches
            first: Pagination offset (default 0)
            max: Maximum results to return (default 10)
            q: Query string for organization search
            search: Search string (searches organization name)
            
        Returns:
            List of organizations matching the filters
        """
        return await self._async(
            get_admin_realms_realm_organizations.asyncio,
            realm,
            brief_representation=brief_representation,
            exact=exact,
            first=first,
            max_=max,
            q=q,
            search=search,
        )

    def create(self, realm: str | None = None, org_data: dict | OrganizationRepresentation = None) -> str:
        """Create an organization (sync). Returns organization ID."""
        org_obj = org_data if isinstance(org_data, OrganizationRepresentation) else OrganizationRepresentation.from_dict(org_data)
        response = self._sync_detailed(
            post_admin_realms_realm_organizations.sync_detailed,
            realm=realm,
            body=org_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create organization: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def acreate(self, realm: str | None = None, org_data: dict | OrganizationRepresentation = None) -> str:
        """Create an organization (async). Returns organization ID."""
        org_obj = org_data if isinstance(org_data, OrganizationRepresentation) else OrganizationRepresentation.from_dict(org_data)
        response = await self._async_detailed(
            post_admin_realms_realm_organizations.asyncio_detailed,
            realm=realm,
            body=org_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create organization: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    def get(self, realm: str | None = None, org_id: str = None) -> OrganizationRepresentation | None:
        """Get an organization by ID (sync)."""
        return self._sync(
            get_admin_realms_realm_organizations_org_id.sync,
            realm=realm,
            org_id=org_id
        )

    async def aget(self, realm: str | None = None, org_id: str = None) -> OrganizationRepresentation | None:
        """Get an organization by ID (async)."""
        return await self._async(
            get_admin_realms_realm_organizations_org_id.asyncio,
            realm=realm,
            org_id=org_id
        )

    def update(self, realm: str | None = None, org_id: str = None, org_data: dict | OrganizationRepresentation = None) -> None:
        """Update an organization (sync)."""
        org_obj = org_data if isinstance(org_data, OrganizationRepresentation) else OrganizationRepresentation.from_dict(org_data)
        response = self._sync_detailed(
            put_admin_realms_realm_organizations_org_id.sync_detailed,
            realm=realm,
            org_id=org_id,
            body=org_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update organization: {response.status_code}")

    async def aupdate(self, realm: str | None = None, org_id: str = None, org_data: dict | OrganizationRepresentation = None) -> None:
        """Update an organization (async)."""
        org_obj = org_data if isinstance(org_data, OrganizationRepresentation) else OrganizationRepresentation.from_dict(org_data)
        response = await self._async_detailed(
            put_admin_realms_realm_organizations_org_id.asyncio_detailed,
            realm=realm,
            org_id=org_id,
            body=org_obj
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update organization: {response.status_code}")

    def delete(self, realm: str | None = None, org_id: str = None) -> None:
        """Delete an organization (sync)."""
        response = self._sync_detailed(
            delete_admin_realms_realm_organizations_org_id.sync_detailed,
            realm=realm,
            org_id=org_id
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete organization: {response.status_code}")

    async def adelete(self, realm: str | None = None, org_id: str = None) -> None:
        """Delete an organization (async)."""
        response = await self._async_detailed(
            delete_admin_realms_realm_organizations_org_id.asyncio_detailed,
            realm=realm,
            org_id=org_id
        )
        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete organization: {response.status_code}")

    def get_members(self, realm: str | None = None, org_id: str = None) -> list | None:
        """Get organization members (sync)."""
        return self._sync(
            get_admin_realms_realm_organizations_org_id_members.sync,
            realm=realm,
            org_id=org_id
        )

    async def aget_members(self, realm: str | None = None, org_id: str = None) -> list | None:
        """Get organization members (async)."""
        return await self._async(
            get_admin_realms_realm_organizations_org_id_members.asyncio,
            realm=realm,
            org_id=org_id
        )

    def add_member(self, realm: str | None = None, org_id: str = None, user_id: str = None) -> None:
        """Add a member to an organization (sync)."""
        response = self._sync_detailed(
            post_admin_realms_realm_organizations_org_id_members.sync_detailed,
            realm=realm,
            org_id=org_id,
            body=user_id
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to add member: {response.status_code}")

    async def aadd_member(self, realm: str | None = None, org_id: str = None, user_id: str = None) -> None:
        """Add a member to an organization (async)."""
        response = await self._async_detailed(
            post_admin_realms_realm_organizations_org_id_members.asyncio_detailed,
            realm=realm,
            org_id=org_id,
            body=user_id
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to add member: {response.status_code}")


class OrganizationsClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the OrganizationsAPI.
    """

    @cached_property
    def organizations(self) -> OrganizationsAPI:
        """Get the OrganizationsAPI instance."""
        return OrganizationsAPI(manager=self)  # type: ignore[arg-type]
