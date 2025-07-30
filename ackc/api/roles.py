"""Role management API methods."""
from functools import cached_property

from .base import BaseAPI
from ..exceptions import AuthError
from ..generated.api.roles import (
    get_admin_realms_realm_roles,
    post_admin_realms_realm_roles,
)
from ..generated.models import RoleRepresentation
from ..generated.types import UNSET, Unset

__all__ = "RolesAPI", "RolesClientMixin", "RoleRepresentation"


class RolesAPI(BaseAPI):
    """Role management API methods."""

    def get_all(
        self,
        realm: str | None = None,
        *,
        brief_representation: Unset | bool = True,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
        search: Unset | str = '',
    ) -> list[RoleRepresentation] | None:
        """List realm roles.
        
        Args:
            realm: The realm name
            brief_representation: Only return basic role info (default True)
            first: Pagination offset
            max: Maximum results to return
            search: Search string for role name
            
        Returns:
            List of roles matching the filters
        """
        return self._sync(
            get_admin_realms_realm_roles.sync,
            realm,
            brief_representation=brief_representation,
            first=first,
            max_=max,
            search=search,
        )

    async def aget_all(
        self,
        realm: str | None = None,
        *,
        brief_representation: Unset | bool = True,
        first: Unset | int = UNSET,
        max: Unset | int = UNSET,
        search: Unset | str = '',
    ) -> list[RoleRepresentation] | None:
        """List realm roles (async).
        
        Args:
            realm: The realm name
            brief_representation: Only return basic role info (default True)
            first: Pagination offset
            max: Maximum results to return
            search: Search string for role name
            
        Returns:
            List of roles matching the filters
        """
        return await self._async(
            get_admin_realms_realm_roles.asyncio,
            realm,
            brief_representation=brief_representation,
            first=first,
            max_=max,
            search=search,
        )

    def create(self, realm: str | None = None, role_data: dict | RoleRepresentation = None) -> None:
        """Create a realm role (sync)."""
        role_obj = role_data if isinstance(role_data, RoleRepresentation) else RoleRepresentation.from_dict(role_data)
        response = self._sync_detailed(
            post_admin_realms_realm_roles.sync_detailed,
            realm=realm,
            body=role_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create role: {response.status_code}")

    async def acreate(self, realm: str | None = None, role_data: dict | RoleRepresentation = None) -> None:
        """Create a realm role (async)."""
        role_obj = role_data if isinstance(role_data, RoleRepresentation) else RoleRepresentation.from_dict(role_data)
        response = await self._async_detailed(
            post_admin_realms_realm_roles.asyncio_detailed,
            realm=realm,
            body=role_obj
        )
        if response.status_code != 201:
            raise AuthError(f"Failed to create role: {response.status_code}")


class RolesClientMixin:
    """Mixin for BaseClientManager subclasses to be connected to the RolesAPI.
    """

    @cached_property
    def roles(self) -> RolesAPI:
        """Get the RolesAPI instance."""
        return RolesAPI(manager=self)  # type: ignore[arg-type]
