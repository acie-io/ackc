"""User management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import AuthError
from ..generated.api.users import (
    get_admin_realms_realm_users,
    post_admin_realms_realm_users,
    get_admin_realms_realm_users_user_id,
    put_admin_realms_realm_users_user_id,
    delete_admin_realms_realm_users_user_id,
)
from ..generated.models import UserRepresentation
from ..generated.types import UNSET, Unset

__all__ = "UsersAPI", "UsersClientMixin", "UserRepresentation"


class UsersAPI(BaseAPI):
    """User management API methods."""

    def get_all(
        self,
        realm: str | None = None,
        *,
        brief_representation: Unset | bool = UNSET,
        email: Unset | str = UNSET,
        email_verified: Unset | bool = UNSET,
        enabled: Unset | bool = UNSET,
        exact: Unset | bool = UNSET,
        first: Unset | int = UNSET,
        first_name: Unset | str = UNSET,
        idp_alias: Unset | str = UNSET,
        idp_user_id: Unset | str = UNSET,
        last_name: Unset | str = UNSET,
        max: Unset | int = UNSET,
        q: Unset | str = UNSET,
        search: Unset | str = UNSET,
        username: Unset | str = UNSET,
    ) -> list[UserRepresentation] | None:
        """List users in a realm.
        
        Args:
            realm: The realm name
            brief_representation: Only return basic user info (default True)
            email: Filter by email address
            email_verified: Filter by verified email status
            enabled: Filter by enabled status
            exact: Exact match for username/email searches
            first: Pagination offset
            first_name: Filter by first name
            idp_alias: Filter by identity provider alias
            idp_user_id: Filter by identity provider user ID
            last_name: Filter by last name
            max: Maximum results to return (default 100)
            q: General query string for user search
            search: Search string (searches username, first/last name, email)
            username: Filter by username
            
        Returns:
            List of users matching the filters
        """
        return self._sync(
            get_admin_realms_realm_users.sync,
            realm,
            brief_representation=brief_representation,
            email=email,
            email_verified=email_verified,
            enabled=enabled,
            exact=exact,
            first=first,
            first_name=first_name,
            idp_alias=idp_alias,
            idp_user_id=idp_user_id,
            last_name=last_name,
            max_=max,
            q=q,
            search=search,
            username=username,
        )
    
    async def aget_all(
        self,
        realm: str | None = None,
        *,
        brief_representation: Unset | bool = UNSET,
        email: Unset | str = UNSET,
        email_verified: Unset | bool = UNSET,
        enabled: Unset | bool = UNSET,
        exact: Unset | bool = UNSET,
        first: Unset | int = UNSET,
        first_name: Unset | str = UNSET,
        idp_alias: Unset | str = UNSET,
        idp_user_id: Unset | str = UNSET,
        last_name: Unset | str = UNSET,
        max: Unset | int = UNSET,
        q: Unset | str = UNSET,
        search: Unset | str = UNSET,
        username: Unset | str = UNSET,
    ) -> list[UserRepresentation] | None:
        """List users in a realm (async).
        
        Args:
            realm: The realm name
            brief_representation: Only return basic user info (default True)
            email: Filter by email address
            email_verified: Filter by verified email status
            enabled: Filter by enabled status
            exact: Exact match for username/email searches
            first: Pagination offset
            first_name: Filter by first name
            idp_alias: Filter by identity provider alias
            idp_user_id: Filter by identity provider user ID
            last_name: Filter by last name
            max: Maximum results to return (default 100)
            q: General query string for user search
            search: Search string (searches username, first/last name, email)
            username: Filter by username
            
        Returns:
            List of users matching the filters
        """
        return await self._async(
            get_admin_realms_realm_users.asyncio,
            realm,
            brief_representation=brief_representation,
            email=email,
            email_verified=email_verified,
            enabled=enabled,
            exact=exact,
            first=first,
            first_name=first_name,
            idp_alias=idp_alias,
            idp_user_id=idp_user_id,
            last_name=last_name,
            max_=max,
            q=q,
            search=search,
            username=username,
        )
    
    def create(self, realm: str | None = None, *, user_data: dict | UserRepresentation) -> str:
        """Create a user (sync). Returns user ID."""
        user_obj = user_data if isinstance(user_data, UserRepresentation) else UserRepresentation.from_dict(user_data)
        response = self._sync_detailed(post_admin_realms_realm_users.sync_detailed, realm=realm or self.realm, body=user_obj)

        if response.status_code != 201:
            raise AuthError(f"Failed to create user: {response.status_code}")

        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""
    
    async def acreate(self, realm: str | None = None, *, user_data: dict | UserRepresentation) -> str:
        """Create a user (async). Returns user ID."""
        user_obj = user_data if isinstance(user_data, UserRepresentation) else UserRepresentation.from_dict(user_data)
        response = await self._async_detailed(post_admin_realms_realm_users.asyncio_detailed, realm=realm or self.realm, body=user_obj)

        if response.status_code != 201:
            raise AuthError(f"Failed to create user: {response.status_code}")

        location = response.headers.get("Location", "")
        return location.split("/")[-1] if location else ""
    
    def get(self, realm: str | None = None, *, user_id: str) -> UserRepresentation | None:
        """Get a user by ID (sync)."""
        return self._sync(get_admin_realms_realm_users_user_id.sync, realm=realm or self.realm, user_id=user_id)
    
    async def aget(self, realm: str | None = None, *, user_id: str) -> UserRepresentation | None:
        """Get a user by ID (async)."""
        return await self._async(get_admin_realms_realm_users_user_id.asyncio, realm=realm or self.realm, user_id=user_id)

    def update(self, realm: str | None = None, *, user_id: str, user_data: dict | UserRepresentation) -> None:
        """Update a user (sync)."""
        user_obj = user_data if isinstance(user_data, UserRepresentation) else UserRepresentation.from_dict(user_data)
        response = self._sync_detailed(put_admin_realms_realm_users_user_id.sync_detailed, realm=realm or self.realm, user_id=user_id, body=user_obj)

        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update user: {response.status_code}")
    
    async def aupdate(self, realm: str | None = None, *, user_id: str, user_data: dict | UserRepresentation) -> None:
        """Update a user (async)."""
        user_obj = user_data if isinstance(user_data, UserRepresentation) else UserRepresentation.from_dict(user_data)
        response = await self._async_detailed(
            put_admin_realms_realm_users_user_id.asyncio_detailed,
            realm=realm or self.realm,
            user_id=user_id,
            body=user_obj
        )

        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to update user: {response.status_code}")

    def delete(self, realm: str | None = None, *, user_id: str) -> None:
        """Delete a user (sync)."""
        response = self._sync_detailed(
            delete_admin_realms_realm_users_user_id.sync_detailed,
            realm=realm or self.realm,
            user_id=user_id
        )

        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete user: {response.status_code}")

    async def adelete(self, realm: str | None = None, *, user_id: str) -> None:
        """Delete a user (async)."""
        response = await self._async_detailed(
            delete_admin_realms_realm_users_user_id.asyncio_detailed,
            realm=realm or self.realm,
            user_id=user_id
        )

        if response.status_code not in (200, 204):
            raise AuthError(f"Failed to delete user: {response.status_code}")


class UsersClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the UsersAPI.
    """
    @cached_property
    def users(self) -> UsersAPI:
        """Get the UsersAPI instance."""
        return UsersAPI(manager=self)  # type: ignore[arg-type]
