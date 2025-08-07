"""Organization management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import APIError
from ..generated.api.organizations import (
    get_admin_realms_realm_organizations,
    post_admin_realms_realm_organizations,
    get_admin_realms_realm_organizations_org_id,
    put_admin_realms_realm_organizations_org_id,
    delete_admin_realms_realm_organizations_org_id,
    get_admin_realms_realm_organizations_count,
    get_admin_realms_realm_organizations_org_id_members,
    get_admin_realms_realm_organizations_org_id_members_count,
    get_admin_realms_realm_organizations_org_id_members_member_id,
    post_admin_realms_realm_organizations_org_id_members,
    delete_admin_realms_realm_organizations_org_id_members_member_id,
    post_admin_realms_realm_organizations_org_id_members_invite_existing_user,
    post_admin_realms_realm_organizations_org_id_members_invite_user,
    get_admin_realms_realm_organizations_org_id_identity_providers,
    get_admin_realms_realm_organizations_org_id_identity_providers_alias,
    post_admin_realms_realm_organizations_org_id_identity_providers,
    delete_admin_realms_realm_organizations_org_id_identity_providers_alias,
    get_admin_realms_realm_organizations_members_member_id_organizations,
    get_admin_realms_realm_organizations_org_id_members_member_id_organizations,
)
from ..generated.models import (
    OrganizationRepresentation,
    MemberRepresentation,
    IdentityProviderRepresentation,
)
from ..generated.types import UNSET, Unset

__all__ = (
    "OrganizationsAPI",
    "OrganizationsClientMixin",
    "OrganizationRepresentation",
    "MemberRepresentation",
    "IdentityProviderRepresentation",
)


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
        """Create an organization (sync).
        
        Args:
            realm: The realm name
            org_data: Organization configuration including name and attributes
            
        Returns:
            Created organization ID
            
        Raises:
            APIError: If organization creation fails
        """
        org_obj = org_data if isinstance(org_data, OrganizationRepresentation) else OrganizationRepresentation.from_dict(org_data)
        response = self._sync_detailed(
            post_admin_realms_realm_organizations.sync_detailed,
            realm=realm,
            body=org_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create organization: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    async def acreate(self, realm: str | None = None, org_data: dict | OrganizationRepresentation = None) -> str:
        """Create an organization (async).
        
        Args:
            realm: The realm name
            org_data: Organization configuration including name and attributes
            
        Returns:
            Created organization ID
            
        Raises:
            APIError: If organization creation fails
        """
        org_obj = org_data if isinstance(org_data, OrganizationRepresentation) else OrganizationRepresentation.from_dict(org_data)
        response = await self._async_detailed(
            post_admin_realms_realm_organizations.asyncio_detailed,
            realm=realm,
            body=org_obj
        )
        if response.status_code != 201:
            raise APIError(f"Failed to create organization: {response.status_code}")
        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""

    def get(self, realm: str | None = None, org_id: str = None) -> OrganizationRepresentation | None:
        """Get an organization by ID (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            
        Returns:
            Organization representation with full details
        """
        return self._sync(
            get_admin_realms_realm_organizations_org_id.sync,
            realm=realm,
            org_id=org_id
        )

    async def aget(self, realm: str | None = None, org_id: str = None) -> OrganizationRepresentation | None:
        """Get an organization by ID (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            
        Returns:
            Organization representation with full details
        """
        return await self._async(
            get_admin_realms_realm_organizations_org_id.asyncio,
            realm=realm,
            org_id=org_id
        )

    def update(self, realm: str | None = None, org_id: str = None, org_data: dict | OrganizationRepresentation = None) -> None:
        """Update an organization (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID to update
            org_data: Updated organization configuration
            
        Raises:
            APIError: If organization update fails
        """
        org_obj = org_data if isinstance(org_data, OrganizationRepresentation) else OrganizationRepresentation.from_dict(org_data)
        response = self._sync_detailed(
            put_admin_realms_realm_organizations_org_id.sync_detailed,
            realm=realm,
            org_id=org_id,
            body=org_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update organization: {response.status_code}")

    async def aupdate(self, realm: str | None = None, org_id: str = None, org_data: dict | OrganizationRepresentation = None) -> None:
        """Update an organization (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID to update
            org_data: Updated organization configuration
            
        Raises:
            APIError: If organization update fails
        """
        org_obj = org_data if isinstance(org_data, OrganizationRepresentation) else OrganizationRepresentation.from_dict(org_data)
        response = await self._async_detailed(
            put_admin_realms_realm_organizations_org_id.asyncio_detailed,
            realm=realm,
            org_id=org_id,
            body=org_obj
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to update organization: {response.status_code}")

    def delete(self, realm: str | None = None, org_id: str = None) -> None:
        """Delete an organization (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID to delete
            
        Raises:
            APIError: If organization deletion fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_organizations_org_id.sync_detailed,
            realm=realm,
            org_id=org_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete organization: {response.status_code}")

    async def adelete(self, realm: str | None = None, org_id: str = None) -> None:
        """Delete an organization (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID to delete
            
        Raises:
            APIError: If organization deletion fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_organizations_org_id.asyncio_detailed,
            realm=realm,
            org_id=org_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to delete organization: {response.status_code}")

    def get_members(self, realm: str | None = None, org_id: str = None) -> list[MemberRepresentation] | None:
        """Get organization members (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            
        Returns:
            List of organization members
        """
        return self._sync(
            get_admin_realms_realm_organizations_org_id_members.sync,
            realm=realm,
            org_id=org_id
        )

    async def aget_members(self, realm: str | None = None, org_id: str = None) -> list[MemberRepresentation] | None:
        """Get organization members (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            
        Returns:
            List of organization members
        """
        return await self._async(
            get_admin_realms_realm_organizations_org_id_members.asyncio,
            realm=realm,
            org_id=org_id
        )

    def add_member(self, realm: str | None = None, org_id: str = None, user_id: str = None) -> None:
        """Add a member to an organization (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            user_id: User ID to add as member
            
        Raises:
            APIError: If adding member fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_organizations_org_id_members.sync_detailed,
            realm=realm,
            org_id=org_id,
            body=user_id
        )
        if response.status_code != 201:
            raise APIError(f"Failed to add member: {response.status_code}")

    async def aadd_member(self, realm: str | None = None, org_id: str = None, user_id: str = None) -> None:
        """Add a member to an organization (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            user_id: User ID to add as member
            
        Raises:
            APIError: If adding member fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_organizations_org_id_members.asyncio_detailed,
            realm=realm,
            org_id=org_id,
            body=user_id
        )
        if response.status_code != 201:
            raise APIError(f"Failed to add member: {response.status_code}")

    def remove_member(self, realm: str | None = None, *, org_id: str, member_id: str) -> None:
        """Remove a member from an organization (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            member_id: Member ID to remove
            
        Raises:
            APIError: If removing member fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_organizations_org_id_members_member_id.sync_detailed,
            realm or self.realm,
            org_id=org_id,
            member_id=member_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to remove member: {response.status_code}")

    async def aremove_member(self, realm: str | None = None, *, org_id: str, member_id: str) -> None:
        """Remove a member from an organization (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            member_id: Member ID to remove
            
        Raises:
            APIError: If removing member fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_organizations_org_id_members_member_id.asyncio_detailed,
            realm or self.realm,
            org_id=org_id,
            member_id=member_id
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to remove member: {response.status_code}")

    def get_count(self, realm: str | None = None) -> int | None:
        """Get total organization count (sync).
        
        Args:
            realm: The realm name
            
        Returns:
            Total number of organizations in the realm
        """
        result = self._sync(
            get_admin_realms_realm_organizations_count.sync,
            realm or self.realm
        )
        return result.get("count") if result else None

    async def aget_count(self, realm: str | None = None) -> int | None:
        """Get total organization count (async).
        
        Args:
            realm: The realm name
            
        Returns:
            Total number of organizations in the realm
        """
        result = await self._async(
            get_admin_realms_realm_organizations_count.asyncio,
            realm or self.realm
        )
        return result.get("count") if result else None

    def get_members_count(self, realm: str | None = None, *, org_id: str) -> int | None:
        """Get organization member count (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            
        Returns:
            Number of members in the organization
        """
        result = self._sync(
            get_admin_realms_realm_organizations_org_id_members_count.sync,
            realm or self.realm,
            org_id=org_id
        )
        return result.get("count") if result else None

    async def aget_members_count(self, realm: str | None = None, *, org_id: str) -> int | None:
        """Get organization member count (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            
        Returns:
            Number of members in the organization
        """
        result = await self._async(
            get_admin_realms_realm_organizations_org_id_members_count.asyncio,
            realm or self.realm,
            org_id=org_id
        )
        return result.get("count") if result else None

    def get_member(self, realm: str | None = None, *, org_id: str, member_id: str) -> MemberRepresentation | None:
        """Get organization member details (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            member_id: Member ID
            
        Returns:
            Member details
        """
        return self._sync(
            get_admin_realms_realm_organizations_org_id_members_member_id.sync,
            realm or self.realm,
            org_id=org_id,
            member_id=member_id
        )

    async def aget_member(self, realm: str | None = None, *, org_id: str, member_id: str) -> MemberRepresentation | None:
        """Get organization member details (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            member_id: Member ID
            
        Returns:
            Member details
        """
        return await self._async(
            get_admin_realms_realm_organizations_org_id_members_member_id.asyncio,
            realm or self.realm,
            org_id=org_id,
            member_id=member_id
        )

    def invite_existing_user(self, realm: str | None = None, *, org_id: str, user_id: str) -> None:
        """Invite existing user to organization (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            user_id: Existing user ID to invite
            
        Raises:
            APIError: If invitation fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_organizations_org_id_members_invite_existing_user.sync_detailed,
            realm or self.realm,
            org_id=org_id,
            body={"id": user_id}
        )
        if response.status_code not in (200, 201, 204):
            raise APIError(f"Failed to invite user: {response.status_code}")

    async def ainvite_existing_user(self, realm: str | None = None, *, org_id: str, user_id: str) -> None:
        """Invite existing user to organization (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            user_id: Existing user ID to invite
            
        Raises:
            APIError: If invitation fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_organizations_org_id_members_invite_existing_user.asyncio_detailed,
            realm or self.realm,
            org_id=org_id,
            body={"id": user_id}
        )
        if response.status_code not in (200, 201, 204):
            raise APIError(f"Failed to invite user: {response.status_code}")

    def invite_user(self, realm: str | None = None, *, org_id: str, email: str, first_name: str = None, last_name: str = None) -> None:
        """Invite new user to organization (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            email: Email address of new user
            first_name: User's first name (optional)
            last_name: User's last name (optional)
            
        Raises:
            APIError: If invitation fails
        """
        body = {"email": email}
        if first_name:
            body["firstName"] = first_name
        if last_name:
            body["lastName"] = last_name
            
        response = self._sync_detailed(
            post_admin_realms_realm_organizations_org_id_members_invite_user.sync_detailed,
            realm or self.realm,
            org_id=org_id,
            body=body
        )
        if response.status_code not in (200, 201, 204):
            raise APIError(f"Failed to invite new user: {response.status_code}")

    async def ainvite_user(self, realm: str | None = None, *, org_id: str, email: str, first_name: str = None, last_name: str = None) -> None:
        """Invite new user to organization (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            email: Email address of new user
            first_name: User's first name (optional)
            last_name: User's last name (optional)
            
        Raises:
            APIError: If invitation fails
        """
        body = {"email": email}
        if first_name:
            body["firstName"] = first_name
        if last_name:
            body["lastName"] = last_name
            
        response = await self._async_detailed(
            post_admin_realms_realm_organizations_org_id_members_invite_user.asyncio_detailed,
            realm or self.realm,
            org_id=org_id,
            body=body
        )
        if response.status_code not in (200, 201, 204):
            raise APIError(f"Failed to invite new user: {response.status_code}")

    # Identity Provider management
    def get_identity_providers(self, realm: str | None = None, *, org_id: str) -> list[IdentityProviderRepresentation] | None:
        """Get organization identity providers (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            
        Returns:
            List of identity providers for the organization
        """
        return self._sync(
            get_admin_realms_realm_organizations_org_id_identity_providers.sync,
            realm or self.realm,
            org_id=org_id
        )

    async def aget_identity_providers(self, realm: str | None = None, *, org_id: str) -> list[IdentityProviderRepresentation] | None:
        """Get organization identity providers (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            
        Returns:
            List of identity providers for the organization
        """
        return await self._async(
            get_admin_realms_realm_organizations_org_id_identity_providers.asyncio,
            realm or self.realm,
            org_id=org_id
        )

    def get_identity_provider(self, realm: str | None = None, *, org_id: str, alias: str) -> IdentityProviderRepresentation | None:
        """Get organization identity provider details (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            alias: Identity provider alias
            
        Returns:
            Identity provider details
        """
        return self._sync(
            get_admin_realms_realm_organizations_org_id_identity_providers_alias.sync,
            realm or self.realm,
            org_id=org_id,
            alias=alias
        )

    async def aget_identity_provider(self, realm: str | None = None, *, org_id: str, alias: str) -> IdentityProviderRepresentation | None:
        """Get organization identity provider details (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            alias: Identity provider alias
            
        Returns:
            Identity provider details
        """
        return await self._async(
            get_admin_realms_realm_organizations_org_id_identity_providers_alias.asyncio,
            realm or self.realm,
            org_id=org_id,
            alias=alias
        )

    def add_identity_provider(self, realm: str | None = None, *, org_id: str, alias: str) -> None:
        """Add identity provider to organization (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            alias: Identity provider alias to add
            
        Raises:
            APIError: If adding identity provider fails
        """
        response = self._sync_detailed(
            post_admin_realms_realm_organizations_org_id_identity_providers.sync_detailed,
            realm or self.realm,
            org_id=org_id,
            body={"alias": alias}
        )
        if response.status_code not in (200, 201, 204):
            raise APIError(f"Failed to add identity provider: {response.status_code}")

    async def aadd_identity_provider(self, realm: str | None = None, *, org_id: str, alias: str) -> None:
        """Add identity provider to organization (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            alias: Identity provider alias to add
            
        Raises:
            APIError: If adding identity provider fails
        """
        response = await self._async_detailed(
            post_admin_realms_realm_organizations_org_id_identity_providers.asyncio_detailed,
            realm or self.realm,
            org_id=org_id,
            body={"alias": alias}
        )
        if response.status_code not in (200, 201, 204):
            raise APIError(f"Failed to add identity provider: {response.status_code}")

    def remove_identity_provider(self, realm: str | None = None, *, org_id: str, alias: str) -> None:
        """Remove identity provider from organization (sync).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            alias: Identity provider alias to remove
            
        Raises:
            APIError: If removing identity provider fails
        """
        response = self._sync_detailed(
            delete_admin_realms_realm_organizations_org_id_identity_providers_alias.sync_detailed,
            realm or self.realm,
            org_id=org_id,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to remove identity provider: {response.status_code}")

    async def aremove_identity_provider(self, realm: str | None = None, *, org_id: str, alias: str) -> None:
        """Remove identity provider from organization (async).
        
        Args:
            realm: The realm name
            org_id: Organization ID
            alias: Identity provider alias to remove
            
        Raises:
            APIError: If removing identity provider fails
        """
        response = await self._async_detailed(
            delete_admin_realms_realm_organizations_org_id_identity_providers_alias.asyncio_detailed,
            realm or self.realm,
            org_id=org_id,
            alias=alias
        )
        if response.status_code not in (200, 204):
            raise APIError(f"Failed to remove identity provider: {response.status_code}")

    def get_member_organizations(self, realm: str | None = None, *, member_id: str) -> list[OrganizationRepresentation] | None:
        """Get organizations for a member (sync).
        
        Args:
            realm: The realm name
            member_id: Member ID
            
        Returns:
            List of organizations the member belongs to
        """
        return self._sync(
            get_admin_realms_realm_organizations_members_member_id_organizations.sync,
            realm or self.realm,
            member_id=member_id
        )

    async def aget_member_organizations(self, realm: str | None = None, *, member_id: str) -> list[OrganizationRepresentation] | None:
        """Get organizations for a member (async).
        
        Args:
            realm: The realm name
            member_id: Member ID
            
        Returns:
            List of organizations the member belongs to
        """
        return await self._async(
            get_admin_realms_realm_organizations_members_member_id_organizations.asyncio,
            realm or self.realm,
            member_id=member_id
        )


class OrganizationsClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the OrganizationsAPI."""

    @cached_property
    def organizations(self) -> OrganizationsAPI:
        """Get the OrganizationsAPI instance.
        
        Returns:
            OrganizationsAPI instance for managing organizations
        """
        return OrganizationsAPI(manager=self)  # type: ignore[arg-type]
